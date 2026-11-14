import os
import sys
import time
import uuid
import random
import asyncio
import socket
import logging
import traceback

HOME_DIR = os.getenv("HERMES_HOME", "/tmp/hermes_home")
LOG_FILE = os.path.join(HOME_DIR, "scripts", "polyester_trader.log")
LOCK_PORT = 59423

API_KEY_ID = "ak_7d0a74c4acfa0a230055dfd6d63aff8d"
API_PRIVATE_KEY = "de5c1ada164e6cacd3cef66cd4b4f9df7db53902de00680fd91c0500b80f7bdd"
ACCOUNT_ID = "AcidicTie"

os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    filename=LOG_FILE,
    filemode="a",
    format="%(asctime)s - %(levelname)s - %(message)s",
    encoding="utf-8"
)
logger = logging.getLogger("PolyesterBot")

def log(msg):
    print(msg, flush=True)
    try:
        logger.info(msg)
    except Exception:
        pass

_LOCK_SOCK = None
def acquire_single_instance():
    global _LOCK_SOCK
    _LOCK_SOCK = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _LOCK_SOCK.bind(("127.0.0.1", LOCK_PORT))
        _LOCK_SOCK.listen(1)
        return True
    except Exception:
        return False

from polyester import AsyncPolyester, POLYESTER_TESTNET_ENVIRONMENT

# جدول دقیق و واقعی آیدی دارایی های پلی استر (کشف شده از تطبیق دقیق مقادیر کیف پول شما)
TRUE_ASSET_MAP = {
    1: "USDT",
    2: "USDC",
    3: "BTC",
    4: "SOL",
    6: "ETH",
    17: "XRP",
    18: "LTC",
    20: "BCH",
    23: "HYPE",
    24: "POL"
}

ACTIVE_MARKETS = [
    "XRP-USDT",
    "POL-USDT",
    "LTC-USDT",
    "BCH-USDT",
    "HYPE-USDT",
    "SOL-USDT",
    "ETH-USDT",
    "BTC-USDT"
]

SELL_CAP = {
    "BTC": 0.0005,
    "ETH": 0.008,
    "SOL": 0.25,
    "XRP": 25.0,
    "POL": 200.0,
    "LTC": 0.35,
    "BCH": 0.08,
    "HYPE": 0.25
}

async def sync_dynamic_assets(client):
    """استعلام خودکار نام دارایی ها از سرور در صورت وجود متد در SDK"""
    for attr in ("assets", "instruments", "markets", "market_data"):
        svc = getattr(client, attr, None)
        if not svc:
            continue
        for fn_name in ("list", "get_assets", "list_assets"):
            fn = getattr(svc, fn_name, None)
            if callable(fn):
                try:
                    res = await fn()
                    items = getattr(res, "assets", None) or getattr(res, "data", None) or res
                    if isinstance(items, (list, tuple)):
                        for it in items:
                            aid = getattr(it, "asset_id", None) or getattr(it, "id", None)
                            sym = getattr(it, "symbol", None) or getattr(it, "name", None)
                            if aid is not None and sym:
                                TRUE_ASSET_MAP[int(aid)] = str(sym).upper()
                except Exception:
                    pass

async def cancel_all_open_orders(client):
    try:
        if hasattr(client.orders, "cancel_all"):
            await client.orders.cancel_all()
            await asyncio.sleep(0.3)
    except Exception:
        pass

async def check_balances(client):
    balances = {}
    try:
        res = await client.balances.list()
        bal_list = getattr(res, "balances", None) or res
        parts = []
        for b in bal_list:
            aid = getattr(b, "asset_id", None)
            if aid is None and isinstance(b, dict):
                aid = b.get("asset_id")
            avail_raw = getattr(b, "available", "0")
            if hasattr(avail_raw, "as_decimal"):
                val = float(avail_raw.as_decimal())
            else:
                f_raw = float(avail_raw)
                val = f_raw / 1e18 if f_raw > 1e8 else f_raw
            sym = TRUE_ASSET_MAP.get(int(aid) if aid is not None else -1, f"ASSET_{aid}")
            balances[sym] = val
            if val > 0.0001:
                parts.append(f"{sym}: {val:.4f}")
        log("[BALANCES] " + (" | ".join(parts) if parts else "Empty"))
    except Exception as e:
        log(f"[BALANCE ERR] {e}")
    return balances

async def get_price(client, symbol):
    try:
        trades = await client.market_data.get_trades(symbol=symbol, limit=1)
        t_list = getattr(trades, "trades", None) or trades
        if t_list:
            p = t_list[0].price
            return float(p.as_decimal()) if hasattr(p, "as_decimal") else float(p)
    except Exception:
        pass
    return None

async def place_smart_order(client, symbol, side, price, available_qty):
    base = symbol.split("-", 1)[0]
    if side == "sell":
        cap = SELL_CAP.get(base, 1.0)
        # اطمینان از اینکه ارزش فروش حداقل ۱۳ دلار است ولی از سقف امن رد نمی شود
        min_qty_for_notional = 13.0 / price
        if available_qty < min_qty_for_notional:
            return 0.0
        q_test = max(min_qty_for_notional, min(available_qty * 0.20, cap))
        q_test = min(q_test, available_qty * 0.90)
    else:
        spend = min(available_qty * 0.45, 14.0)
        if spend < 11.5:
            return 0.0
        q_test = spend / price

    # تست اعشار مختلف برای هماهنگی با هر مارکت (مثلاً POL قیمت 0.088 دارد و نیاز به 4 رقم اعشار قیمت دارد)
    p_decimals = [4, 3, 2] if price < 1.0 else ([2, 1, 3] if price < 100 else [2, 1, 0])
    q_decimals = [1, 0, 2] if q_test >= 10 else [4, 3, 2]

    for p_dec in p_decimals:
        for q_dec in q_decimals:
            p_str = str(round(price, p_dec))
            q_str = str(round(q_test, q_dec) if q_dec > 0 else int(round(q_test)))
            if float(q_str) <= 0 or float(p_str) <= 0:
                continue
            try:
                cid = f"v71-{side[:1]}-{uuid.uuid4().hex[:6]}"
                await client.orders.create(
                    symbol=symbol,
                    side=side,
                    order_type="limit",
                    tif="gtc",
                    qty=q_str,
                    price=p_str,
                    client_order_id=cid
                )
                usd_vol = float(q_str) * float(p_str)
                log(f"✅ [EXECUTED] {side.upper()} {q_str} {symbol} @ ${p_str} (~${usd_vol:,.2f} Vol)")
                return usd_vol
            except Exception as e:
                err_msg = str(e).lower()
                if any(k in err_msg for k in ("tick", "step", "precision", "invalid", "decimal", "lot")):
                    continue
                log(f"[SKIP {symbol} {side.upper()}] q={q_str}, p={p_str} -> {e}")
                return 0.0
    return 0.0

async def run_cycle(client, cycle_num, stats):
    await cancel_all_open_orders(client)
    balances = await check_balances(client)
    if not balances:
        return

    usdt_free = balances.get("USDT", 0.0)
    usdc_free = balances.get("USDC", 0.0)
    shuffled = list(ACTIVE_MARKETS)
    random.shuffle(shuffled)

    cycle_trades = 0
    for sym in shuffled:
        base, quote = sym.split("-", 1)
        base_free = balances.get(base, 0.0)
        price = await get_price(client, sym)
        if not price or price <= 0:
            continue

        # ۱. ابتدا فروش پینگ پنگی توکن های موجود برای تولید حجم و شارژ مداوم USDT
        if (base_free * price) >= 13.5:
            vol = await place_smart_order(client, sym, "sell", price, base_free)
            if vol > 0:
                stats["trades"] += 1
                stats["volume"] += vol
                cycle_trades += 1
                usdt_free += vol * 0.95
                await asyncio.sleep(0.35)

        # ۲. خرید پینگ پنگی با USDT واقعی آزاد
        if usdt_free >= 13.0:
            vol = await place_smart_order(client, sym, "buy", price, usdt_free)
            if vol > 0:
                stats["trades"] += 1
                stats["volume"] += vol
                usdt_free = max(0.0, usdt_free - vol)
                balances["USDT"] = usdt_free
                cycle_trades += 1
                await asyncio.sleep(0.35)

        # ۳. استفاده از 750 USDC در صورت فعال بودن جفت ارز USDC در صرافی
        if usdc_free >= 15.0:
            usdc_sym = f"{base}-USDC"
            u_price = await get_price(client, usdc_sym)
            if u_price and u_price > 0:
                vol = await place_smart_order(client, usdc_sym, "buy", u_price, usdc_free)
                if vol > 0:
                    stats["trades"] += 1
                    stats["volume"] += vol
                    usdc_free = max(0.0, usdc_free - vol)
                    balances["USDC"] = usdc_free
                    cycle_trades += 1
                    await asyncio.sleep(0.35)

    log(f"📊 [VIP STATS] Cycle #{cycle_num} | Cycle Trades: {cycle_trades} | Total Trades: {stats['trades']} | Total Volume: ${stats['volume']:,.2f}")

async def main():
    if not acquire_single_instance():
        log("[INFO] Another instance is already running on port 59423.")
        return

    log("=== 🚀 POLYESTER IMMORTAL 24/7 GRINDER v7.1 (TRUE-ASSET-MAP) ===")
    stats = {"trades": 0, "volume": 0.0}
    c = 0

    while True:
        try:
            client = AsyncPolyester(
                api_key_id=API_KEY_ID,
                api_private_key=API_PRIVATE_KEY,
                environment=POLYESTER_TESTNET_ENVIRONMENT
            )
            async with client:
                await sync_dynamic_assets(client)
                log("[CONNECTED] Session established & True Asset IDs loaded.")
                while True:
                    c += 1
                    log(f"\n--- [CYCLE {c}] ---")
                    try:
                        await run_cycle(client, c, stats)
                    except Exception as cycle_e:
                        log(f"[CYCLE WARN] {cycle_e}")
                    await asyncio.sleep(random.randint(10, 14))
        except KeyboardInterrupt:
            log("[STOP] Stopped manually by user.")
            break
        except Exception as conn_e:
            log(f"[RECONNECTING] Connection lost ({conn_e}). Retrying in 8 seconds...")
            await asyncio.sleep(8)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except Exception as fatal_e:
        log(f"[FATAL] {fatal_e}\n{traceback.format_exc()}")
        input("\nPress Enter to close window...")

