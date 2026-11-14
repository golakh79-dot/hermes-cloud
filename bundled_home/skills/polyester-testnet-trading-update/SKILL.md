---
name: polyester-testnet-trading
description: "Spot trading on Polyester Testnet via Python SDK."
version: 1.1.0
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

## Prerequisites
1. Polyester Testnet account with X + Discord connected (for paper assets)
2. API Key created in the Polyester app (API section in sidebar) with Spot trading permission enabled
3. Python SDK installed: `pip install polyester-sdk` (in the correct venv)
4. Credentials: API Key ID (ak_...), API Private Key (64-char hex Ed25519), Account ID (username)

## Trading Workflow & Operational Rules

### 1. Connection & Strategy
- **Environment**: Always use `POLYESTER_TESTNET_ENVIRONMENT`. Base URL: `https://api.testnet.polyester.com`.
- **Asset ID Mapping**: Polyester API balance endpoint returns numeric `asset_id`:
  - `1: BTC`, `2: ETH`, `3: SOL`, `6: XRP`, `17: USDT`, `18: USDC`. Map `asset_id` to symbol string before checking balance thresholds.
- **Script Locations**:
  - Legacy trader script: `D:/HERMES/Hermes_Portable_Data/home/agents/polyester_trader.py`
  - Pro trader script: `D:/HERMES/Hermes_Portable_Data/home/scripts/polyester_pro_trader.py`
  - Deploy script: `D:/HERMES/Hermes_Portable_Data/home/scripts/deploy_polyester_pro.ps1`
- **Strategy Tuning**:
  - **VIP Volume**: To gain VIP points or climb ladders, ensure `target_notional >= 250.0`.
  - **Pair Selection**: Focus on BTC-USDT and XRP-USDT for reliability. If encountering `Insufficient funds` for specific volatile pairs (BNB, DOGE, etc.), filter for `"USDT"` pairs only or confirm specific asset ownership in portfolio.
  - **Trade Type**: Always use `order_type="limit"` (market orders often fail).
  - **Price Precision**: Use `round(price, 2)` for limits.
  - **Data types**: Pass `qty` and `price` as string literals (`str(val)`).

### 2. Pro Architecture (Dual-Thread + Telegram Control)
**Use when**: Building production-grade autonomous traders that need manual oversight, state persistence, and zero-downtime deploys.
- **Dual-thread design**: `background_worker` (trading loop) + `telegram_listener` (control plane) running in same process via `asyncio.gather()`.
- **Port lock**: Bind TCP localhost port at startup (WURK=59422, Twitter=59421, Polyester Pro=59423) to enforce single instance.
- **State persistence**: Flat JSON file (`polyester_pro_state.json`) with `BotState` dataclass — cycle count, volume, trades, pending approvals, submitted orders, recent fills, consecutive zero cycles, last error, uptime.
- **Manual approval gate**: Orders with notional >= `HIGH_VALUE_THRESHOLD` (default $100) go to `pending_approvals` and require Telegram inline-button approval before submission.
- **Monitoring mode**: When all balances zero for >5 cycles, switch to `monitoring` mode — log once per 10 cycles, skip API order calls entirely.
- **Quality scoring**: 0-100 score per order based on spread tightness, notional size, pair liquidity; logged with each order.
- **Graceful shutdown**: `save_state()` on exit; `load_state()` on restart preserves approvals and submitted orders.

### 3. Implementation Template
Refer to `scripts/polyester_pro_trader.py` for the Pro v1.0 implementation.
- **Cycle Time**: Adjust `asyncio.sleep()` for API rate limiting (default 15s).
- **Log Location**: Always write to `D:/HERMES/Hermes_Portable_Data/home/scripts/polyester_pro_trader.log`.
- **Environment vars**: All credentials via `.env` — `POLYESTER_API_KEY_ID`, `POLYESTER_API_PRIVATE_KEY`, `POLYESTER_ACCOUNT_ID`, `POLYESTER_BOT_TOKEN`, `ADMIN_CHAT_ID`. Never hardcode.

### 4. PowerShell Deploy Script Pattern
Create a companion `.ps1` deploy script per bot (e.g., `deploy_polyester_pro.ps1`):
1. Kill existing instances on lock port + by script name via `Get-CimInstance`
2. Setup `.env` with template + user placeholders; verify required vars present
3. Install Python deps (`polyester-sdk`, `python-telegram-bot`, etc.)
4. Syntax check: `python -m py_compile script.py`
5. Initialize state JSON if missing (backup existing)
6. Start as background **PowerShell Job** with `Tee-Object` for log capture
7. Verify startup: wait 3-5s, check port lock (`netstat`), check process via `Get-CimInstance`, tail log for startup markers

### 5. Windows Background Bot Integration (per python-background-bots skill)
- **Instance Lock**: Socket bind on unique localhost port at module import (Polyester Pro = 59423)
- **Startup Token Validation**: Call `bot.getMe()` immediately — log bot username, exit if invalid
- **Webhook Cleanup**: `deleteWebhook` with `drop_pending_updates=False` before `getUpdates` polling
- **Graceful Error Handling**: Wrap main `asyncio.gather()` in broad try/except that logs and sleeps, never crashes
- **Verify Background Survival**: After start, check port lock + process + log markers within 10s
- **Log Spam Prevention**: Track `consecutive_zero_cycles` in state; when >= 5, reduce log frequency to every 10th cycle, skip API calls entirely

## Pitfalls & Fixes

### ✅ Pitfall: Insufficient Funds / Balance in Trading Account
**Rule**: If hitting `Insufficient funds` despite having a high "Unified Trading" balance, ensure the bot is targeting the correct sub-account or that assets are in the `trading` bucket, not just `funding`.
**Mechanism**: API check: `await client.balances.list()`.

### ✅ Pitfall: Wrong Environment
**Rule**: Using devnet URL causes authentication failure.
**Fix**: Explicitly set `environment=POLYESTER_TESTNET_ENVIRONMENT`.

### ✅ Pitfall: Market Orders Fail
**Rule**: "Service temporarily unavailable" error.
**Fix**: Use `order_type="limit"`.

### ✅ Pitfall: Price Object Handling
**Rule**: Price is a `Price` object.
**Fix**: Use `.as_decimal()` for float conversion.

### ✅ Pitfall: Min Notional Validation
**Rule**: Trades under $5 are rejected.
**Fix**: Compute `qty = target_notional / last_price` where `target_notional >= 5.0`.

### ✅ Pitfall: Invalid Qty Format
**Rule**: "qty must be a valid decimal string" error happens when passing too many decimal places for the asset.
**Fix**: Round `qty` to 4 decimal places for BTC/XRP.

### ✅ Pitfall: Zero-Balance Trading Loops
**Rule**: Market-making agents must check `available > threshold` before entering order placement logic; log and skip cycles cleanly when dry.
**Why**: Polyester trader generated 14k+ "Insufficient funds" log lines per hour because it attempted orders on zero balances every 15s.
**Fix**: In `run_cycle()`, guard order placement with `if usdt_balance >= 10.0:` and `if base_balance * price >= 5.0:` checks (as in current code), but add an early `continue` with a single log line per cycle when all balances are zero — avoids log spam.

### ✅ Pitfall: Log Spam on Persistent Zero Balance
**Rule**: When all trading balances are zero for > 5 consecutive cycles, switch to "monitoring mode" — log once per 10 cycles instead of every cycle, and skip API order calls entirely.
**Why**: The current Polyester trader (`polyester_trader.py`) logs "Insufficient funds" on every 15s cycle with zero USDT/token balance, creating 14k+ log lines/hour. This fills disk and obscures real events.
**Fix**: Add a `consecutive_zero_cycles` counter in state; when >= 5, reduce log frequency to every 10th cycle and skip `client.orders.create()` calls entirely until balance > threshold.

### ✅ Pitfall: Pro Deployment — Missing Telegram Bot Token
**Rule**: The Pro dual-thread architecture requires a dedicated Telegram bot token (`POLYESTER_BOT_TOKEN`) for the control plane. Without it, `telegram_listener` logs a warning and disables itself, leaving only background trading with no manual oversight.
**Fix**: Create bot via @BotFather, add token to `.env` before deploy. Deploy script validates required vars and exits with clear error if missing.

### ✅ Pitfall: Pro Deployment — Port Lock Conflict
**Rule**: Each autonomous bot must own a unique localhost port for single-instance enforcement (WURK=59422, Twitter=59421, Polyester Pro=59423). Reusing a port causes silent bind failure and the second instance exits.
**Fix**: Assign unique ports per bot in code and deploy script. Kill existing processes on that port before starting new instance.

### ✅ Pitfall: Pro Deployment — State File Corruption on Concurrent Writes
**Rule**: `save_state()` called from both `background_worker` and `telegram_listener` callbacks can race. Use a `threading.Lock` (or `asyncio.Lock`) around all state mutations and serialization.
**Fix**: Wrap `bot_state` mutations in `with state_lock:` and call `save_state()` inside the lock. The Pro template includes this pattern.

### ✅ Pitfall: Pro Deployment — Manual Approval Staleness
**Rule**: Pending approvals persist across restarts via `polyester_pro_state.json`. If an approval sits too long (>1 hour), the market price may have moved significantly, making the order undesirable.
**Fix**: Add `max_approval_age_seconds` config; on startup, reject stale approvals and log them. Notify admin via Telegram.
