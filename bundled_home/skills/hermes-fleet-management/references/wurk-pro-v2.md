# WURK Pro v2.0 Deployment Reference

This reference covers the dual-thread autonomous agent deployment pattern implemented in WURK Pro v2.0 (`scripts/wurk_agent.py`).

## Architecture Overview

```
WURK Pro v2.0
├── background_worker (Thread 1)
│   ├── Polls WURK API every 30s (zero LLM tokens)
│   ├── Filters jobs by keywords (bug, code, python, ai, etc.)
│   ├── Quality scores each job (0-100)
│   ├── Invokes 9Router (Nemotron 3.5 Super VL) ONLY for new unsubmitted tasks
│   ├── Strips AI-isms from LLM output (markdown, thinking blocks, "as an AI", "here is", etc.)
│   ├── Human-like delay: sleep(25s) before submission
│   └── Submits via POST /jobs/{id}/submissions
├── telegram_listener (Thread 2)
│   ├── Inline menu: 📊 Stats | ⏳ Pending | ✅ Approved | ❌ Rejected | 🔄 Refresh
│   ├── Manual approval for quality > 80 or reward > threshold
│   ├── Real-time instance control (stop/restart/status)
│   └── Chat ID restricted to admin (452259540)
├── Instance Lock
│   └── TCP port 59422 (socket.bind) — single instance enforcement
└── State Persistence
    └── wurk_pro_state.json (mode, pending_approvals, submitted_jobs, seen_jobs)
```

## SIWS Authentication Flow (Solana Sign-In With X)

```python
# 1. Get challenge
POST https://api.wurk.fun/solana/siwx/account-create
  Body: {"wallet": "<pubkey>", "domain": "wurk.fun", "nonce": "<random>"}
  → Returns: challenge, nonce

# 2. Sign with Ed25519 private key
message = challenge + nonce
signature = ed25519_sign(private_key, message)

# 3. Verify
POST https://api.wurk.fun/solana/siwx/account-create
  Header: X-Signature: <base64>
  Header: SIGN-IN-WITH-X: <base64(message+signature)>
  Body: {"wallet": "<pubkey>", "domain": "wurk.fun", "nonce": "<nonce>"}
  → Returns: api_key (X-API-Key for all subsequent calls)

# Cache: Token cached in wurk_session_cache.json with 12-min TTL (720s)
```

## Job Filtering Keywords (from source)

```python
KEYWORDS = [
    'bug', 'fix', 'error', 'issue', 'debug',
    'code', 'script', 'python', 'function', 'api',
    'implement', 'feature', 'refactor', 'optimize',
    'test', 'unit', 'integration', 'documentation',
    'research', 'analyze', 'review', 'ai', 'ml',
    'model', 'training', 'inference', 'prompt',
    'llm', 'agent', 'automation', 'bot', 'crawl',
    'scrape', 'parse', 'extract', 'transform'
]
```

## Quality Scoring (0-100)

- Base score from keyword match density
- Bonus for clear deliverables, test cases, examples
- Penalty for vague requirements, missing context
- Threshold > 80 → requires manual Telegram approval
- Threshold > threshold_reward → requires manual Telegram approval

## Deployment Checklist (derived from session)

1. **Syntax check**: `python -m py_compile wurk_agent.py`
2. **Foreground smoke test**: `python wurk_agent.py` (10-15s)
   - Must show: `[WURK-BOT] Wurk.fun Pro v2.0 on @secondxHermesbot is fully ONLINE!`
   - Must show: `[WURK-BOT] Telegram Bot Listener for @secondxHermesbot started.`
   - Must show: `[WURK-BOT] Background Wurk Scanner loop started.`
   - Must show: `[WURK-BOT] Port lock 59422 acquired.`
3. **Install missing deps** if smoke test fails on imports
4. **Background launch**: `Start-Process pythonw.exe -ArgumentList "wurk_agent.py" -WindowStyle Hidden`
5. **Post-launch verify** (within 10s):
   - `netstat -ano | findstr 59422` → LISTENING
   - Log contains startup markers
   - `bot.getMe()` returns valid username
6. **Update fleet_status.json** with PID, version="Pro v2.0", port=59422

## Key Files

| File | Purpose |
|------|---------|
| `scripts/wurk_agent.py` | Main Pro v2.0 script (700+ lines) |
| `wurk_agent.log` | Runtime logs (format: `[WURK-BOT] ...`) |
| `wurk_pro_state.json` | Shared state between threads |
| `wurk_session_cache.json` | SIWS token cache (12-min TTL) |
| `wurk_success_tracker.json` | Earnings log (2,720 WURK earned 2026-11-04) |
| `wurk_rate_limit_state.json` | Rate-limit cooldown (13 errors, cooldown until 1793771942) |
| `.env` | `WURK_BOT_TOKEN=8786109587:AAHZRf8PLVKOapGokRtDZwNoBQ7MxdMR230` |
| `scripts/deploy_wurk_pro.ps1` | PowerShell deploy script (677 lines) |

## Telegram Commands (admin only: 452259540)

- `/start` — Main menu with inline keyboard
- `/stats` — Real-time stats (polled, submitted, approved, rejected, earnings)
- `/pending` — List pending approvals
- `/approve <id>` — Approve submission
- `/reject <id>` — Reject submission
- `/mode auto|manual` — Toggle approval mode
- `/stop` — Stop background worker
- `/restart` — Restart both threads

## Port Allocation

| Bot | Port | Token Env Var |
|-----|------|---------------|
| @Hermixxbot (Twitter Hub) | 59421 | TWITTER_BOT_TOKEN |
| @secondxHermesbot (WURK Pro) | 59422 | WURK_BOT_TOKEN |
| New hermes | N/A | TELEGRAM_BOT_TOKEN |

## Common Issues & Fixes

| Issue | Cause | Fix |
|-------|-------|-----|
| `ModuleNotFoundError: python-docx` / `jina` | Deploy script skipped foreground smoke test | `pip install python-docx jina` then redeploy |
| `401 Unauthorized` on getUpdates | Placeholder token `8786109587:***` in `.env` | Replace with real token from @BotFather |
| Port 59422 not LISTENING | Process crashed silently on import error | Run foreground smoke test first |
| `fleet_status.json` shows stale PID | Watchdog only checks PID existence | Watchdog must verify lock port + log markers |
| SIWS 402 challenge loop | Token expired, no cache | Use `wurk_session_cache.json` 12-min TTL cache |

## Zero-Token Polling Rule

**Background worker MUST NOT call LLM during polling.** Only invoke 9Router when:
1. New job discovered (not in `seen_jobs`)
2. Job passes keyword filter
3. Job not already submitted (`submitted_jobs`)
4. Job status == "open"

Polling interval: 30 seconds. Zero LLM tokens used per cycle unless new task found.