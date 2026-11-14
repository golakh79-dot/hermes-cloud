---
name: polyester-testnet-trading
description: "Spot trading on Polyester Testnet via Python SDK."
version: 1.0.0
author: alireza
license: MIT
metadata:
  hermes:
    tags: [trading, dex, polyester, testnet, cryptocurrency, automation]
    homepage: "https://testnet.polyester.com"
---

# Polyester Testnet Trading - Always-On Rules

## When to Use This Skill
**Use when**: You need to automate spot trading on Polyester Testnet (testnet.polyester.com) using the Python SDK.
**Don't use when**: You need mainnet trading or a different DEX.

## Prerequisites
1. Polyester Testnet account with X + Discord connected (for paper assets)
2. API Key created in the Polyester app (API section in sidebar) with Spot trading permission enabled
3. Python SDK installed: `pip install polyester-sdk` (in the correct venv)
4. Credentials: API Key ID (ak_...), API Private Key (64-char hex Ed25519), Account ID (username)

## Critical Setup
- **Environment**: Always use `POLYESTER_TESTNET_ENVIRONMENT` (not default devnet). Base URL: `https://api.testnet.polyester.com`
- **Wire format**: Use `wire_format="json"` for debugging (default is binary protobuf)
- **Python**: Must use the venv python, not system python. Check `which python`.

## Authentication
- Ed25519 signature using API key ID + 64-char hex private key
- The SDK handles signing internally via `AsyncPolyester(api_key_id=..., api_private_key=..., default_account_id=..., environment=POLYESTER_TESTNET_ENVIRONMENT)`
- Verify the private key matches the public key: derive pubkey with `Ed25519PrivateKey.from_private_bytes(bytes.fromhex(priv_hex))` and compare to the provided public key.

## Trading Workflow

### 1. Connect and verify
```python
async with AsyncPolyester(
    environment=POLYESTER_TESTNET_ENVIRONMENT,
    api_key_id=API_KEY_ID,
    api_private_key=API_PRIVATE_KEY,
    default_account_id=ACCOUNT_ID,
    wire_format="json",
) as client:
    await client.wait_for_catalogs()
    balances = await client.balances.list()
```

### 2. Get market price
```python
trades = await client.market_data.get_trades(symbol="BTC-USDT", limit=1)
last_price = float(trades.trades[0].price.as_decimal())
```
- `get_trades` takes **keyword-only** arguments: `symbol=`, `limit=`
- Price is a `Price` object — use `.as_decimal()` to get float, not `float(price)`

### 3. Place orders
```python
# Limit order (market orders may fail with "Service temporarily unavailable")
result = await client.orders.create(
    symbol="BTC-USDT",
    side="buy",  # or "sell"
    order_type="limit",
    tif="gtc",
    qty=str(qty),  # string, not float
    price=str(price),
    client_order_id=f"bot-{uuid.uuid4().hex[:8]}",
)
```
- Use **decimal strings** for qty and price, never floats
- Market orders may fail with "Service temporarily unavailable" — prefer limit orders
- Min notional is $5 per order — compute qty as `target_notional / last_price`
- `client_order_id` is optional but recommended for reconciliation

### 4. Available services
- `client.market_data` — get_trades, get_candles, get_spot_config
- `client.balances` — list, list_holds
- `client.orders` — create, cancel, cancel_all, list_open, list_history, batch_create
- `client.realtime` — websocket subscriptions

## Pitfalls

### ✅ Pitfall: Wrong Environment
**Rule**: Always use `POLYESTER_TESTNET_ENVIRONMENT`. The default is devnet.
**Why**: Using devnet API URL with testnet credentials causes SIGNATURE_INVALID or wrong balances.
**Fix**: Pass `environment=POLYESTER_TESTNET_ENVIRONMENT` explicitly.

### ✅ Pitfall: Market Orders Fail
**Rule**: Market orders may return "Service temporarily unavailable". Use limit orders instead.
**Why**: The orders service appears to have issues with market order type on testnet.
**Fix**: Use `order_type="limit"` with a price slightly above/below market.

### ✅ Pitfall: Price Object
**Rule**: Trade price is a `Price` object, not a string/float.
**Why**: `float(trades.trades[0].price)` raises TypeError.
**Fix**: Use `float(trades.trades[0].price.as_decimal())`.

### ✅ Pitfall: get_trades Signature
**Rule**: `get_trades` takes keyword-only arguments.
**Why**: `get_trades(symbol, limit=1)` raises TypeError.
**Fix**: Use `get_trades(symbol="BTC-USDT", limit=1)`.

### ✅ Pitfall: Min Notional
**Rule**: Each order must meet minimum notional ($5). Tiny quantities get rejected.
**Why**: Server validates `minNotionalQuote` per pair.
**Fix**: Compute `qty = target_notional / last_price` with target_notional >= 5.

### ✅ Pitfall: Python Interpreter
**Rule**: Must use the venv python, not system python.
**Why**: `polyester-sdk` is installed in the venv, not system site-packages.
**Fix**: Use `/path/to/venv/Scripts/python` explicitly.

### ✅ Pitfall: Decimal Strings
**Rule**: Pass `qty` and `price` as strings, never floats.
**Why**: Floats cause precision issues and server rejection.
**Fix**: Always `str(qty)` and `str(price)`.

## Configuration
- API Key ID: `ak_...` (from API section in sidebar)
- API Private Key: 64-char hex Ed25519 (shown once at creation)
- Account ID: username (from Profile)
- Environment: testnet (chain 888169)

## Autonomous Trading Bot

For 24/7 automated trading, use `scripts/polyester_trader.py`:

```bash
# Start in background
/path/to/venv/Scripts/python -u scripts/polyester_trader.py &
```

The bot trades on 8 pairs (BTC, ETH, SOL, XRP, BNB, DOGE, LTC, AVAX) with limit orders placed ±0.5% around market price, $10 notional per order, cycling every 30s. Each order gets a unique `client_order_id` (uuid-based). Market orders may fail with "Service temporarily unavailable" — the bot uses limit orders exclusively.

**Key parameters to tune:**
- `PAIRS` list — which markets to trade
- `target_notional` — dollar amount per order (min $5)
- Sleep interval between cycles (default 30s)
- Price offset (default 0.5% from market)
