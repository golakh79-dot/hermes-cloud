---
name: wurk-agent-operations
description: "Workflow for managing the WURK autonomous agent (wurk.fun)."
version: 1.0.0
---

# WURK Autonomous Agent Operations

Procedures for operating the WURK agent, managing SIWE authentication, and handling job submission.

## Authentication & API Workflow
- **Auth Method**: Use Sign-In-With-Solana (SIWS) via `SIGN-IN-WITH-X` header. The platform accepts empty `accepts: []` arrays for free-tier authentication, requiring no complex EIP-191/ED25519 signature verification on the client side for standard access.
- **Rate Limiting**: The platform enforces strict 429 rate limits.
  - Implement exponential backoff for 429 responses.
  - Respect the `SUBMISSION_COOLDOWN` constant (minimum 35s between submissions).
- **JSON Stability**: API responses often contain extra trailing data/multiple JSON chunks. When parsing responses with `json.loads`, use regex (`re.search(r'\{.*\}', raw)`) to extract the primary object if the raw stream is malformed.

## Submission Workflow
- **Filtering**: Automatically skip jobs containing high-friction keywords (e.g., "screenshot", "photo", "KYC", "video", "join discord"). Focus on `basic` mode and `random` selection tasks.
- **Content Generation**: Use a local LLM (9Router) to generate submissions. Use a persona-driven system prompt: "You are an expert human Web3 freelancer. Complete the task concisely, naturally, and directly without any AI filler, intro, or robotic dashes."
- **Uniqueness**: Never use static templates. Always route the job description to the LLM to ensure each submission is unique and contextual, minimizing "spam" classification.

## Pro Architecture (Dual-Thread + Telegram Control) — WURK Pro v2.0+
**Use when**: Building production-grade autonomous hunters that need manual oversight, state persistence, and zero-downtime deploys.
- **Dual-thread design**: `background_worker` (job polling loop) + `telegram_listener` (control plane) running in same process via `asyncio.gather()`.
- **Port lock**: Bind TCP localhost port at startup (WURK Pro = 59422) to enforce single instance.
- **State persistence**: Flat JSON file (`wurk_pro_state.json`) with `BotState` dataclass — cycle count, volume, jobs seen/submitted, pending approvals, recent successes, consecutive zero cycles, last error, uptime.
- **Manual approval gate**: High-value jobs (payout >= threshold) go to `pending_approvals` and require Telegram inline-button approval before submission.
- **Quality scoring**: 0-100 score per submission based on task match, payout, difficulty; logged with each submission.
- **AI Judge**: Optional second LLM pass to score/validate before approval gate.
- **Graceful shutdown**: `save_state()` on exit; `load_state()` on restart preserves approvals and submitted jobs.

## PowerShell Deploy Script Pattern
Create a companion `.ps1` deploy script per bot (e.g., `deploy_wurk_pro.ps1`):
1. Kill existing instances on lock port + by script name via `Get-CimInstance`
2. Setup `.env` with template + user placeholders; verify required vars present (`WURK_BOT_TOKEN`, `ADMIN_CHAT_ID`, etc.)
3. Install Python deps (`python-telegram-bot`, `jina-sdk`, etc.)
4. Syntax check: `python -m py_compile script.py`
5. Initialize state JSON if missing (backup existing)
6. Start as background **PowerShell Job** with `Tee-Object` for log capture
7. Verify startup: wait 3-5s, check port lock (`netstat`), check process via `Get-CimInstance`, tail log for startup markers

## Windows Background Bot Integration (per python-background-bots skill)
- **Instance Lock**: Socket bind on unique localhost port at module import (WURK Pro = 59422)
- **Startup Token Validation**: Call `bot.getMe()` immediately — log bot username, exit if invalid
- **Webhook Cleanup**: `deleteWebhook` with `drop_pending_updates=False` before `getUpdates` polling
- **Graceful Error Handling**: Wrap main `asyncio.gather()` in broad try/except that logs and sleeps, never crashes
- **Verify Background Survival**: After start, check port lock + process + log markers within 10s
- **Log Spam Prevention**: Track `consecutive_zero_cycles` in state; when >= 5, reduce log frequency to every 10th cycle, skip API calls entirely

## Pitfalls
- **HTTP 400 Bad Request**: If a submission returns 400, it usually indicates the payload is missing a required format or failed a server-side automated check. Stop submitting that job ID immediately to prevent flagging.
- **AttributeError (Imports)**: When patching `wurk_agent.py`, ensure the script is reloaded via `importlib.reload(wurk_agent)` in the active session to verify changes. Avoid polluting `sys.path` with multiple redundant directories; stick to the absolute path of the script under `scripts/`.
- **JSONDecodeError**: Always wrap `r.read().decode()` in robust parsing logic; never trust that a single API call will return a strictly valid single JSON string.
- **Rate-Limit Backoff State Persistence**: Persist rate-limit cooldown state to JSON (e.g., `wurk_rate_limit_state.json`) with `cooldown_until` timestamp; on restart, honor the remaining cooldown instead of immediately hammering the API. Stateless restarts after a crash cause immediate 429 floods, extending bans and wasting cycles.
- **SIWS Session Caching**: Cache authenticated `apikey` in `wurk_session_cache.json` with 12-minute TTL (720s). On startup, load cache; if `time.time() < expires`, reuse `apikey` without re-auth. This reduces SIWX auth calls and avoids `SIWX_ACCOUNT_RATE_LIMITED` errors.
- **LLM Output Sanitization**: LLM responses for job submissions must be aggressively post-processed to strip JSON structures, thinking blocks (```json, ```), reasoning tags, and AI meta-talk ("as an AI", "here is", "step 1", etc.). Raw LLM output contains markdown, JSON wrappers, and robotic phrasing that fails WURK's human-review checks.
- **Human-Like Submission Delay**: Add a 25-second delay before each submission to mimic human typing/reading pace. Instant submissions appear bot-like and increase rejection risk.
