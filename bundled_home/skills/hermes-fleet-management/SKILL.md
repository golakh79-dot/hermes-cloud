---
name: hermes-fleet-management
version: 1.1.0
author: alireza
license: MIT
description: "Manage background agent fleets (local and cloud)."
metadata:
  hermes:
    tags: [hermes, fleet, watchdog, maintenance, background-agents, cloud-migration]
---

# Hermes Fleet Management - Always-On Rules

## When to Use This Skill
Use when you have multiple background processes (autonomous agents like WURK, AgentHansa, Polyester) that need to run 24/7. This covers both local Windows supervision and cloud-based autonomous orchestration (Molab/GPU).

## Core Procedures

### 1. Watchdog Orchestration (Local)
Always implement a master watchdog script (`master_watchdog.py`) when managing 2+ background agents on Windows.
- **Process monitor**: Use `subprocess.Popen` to launch agents if `process.poll() is not None`.
- **Output redirection**: Always log `stdout`/`stderr` to dedicated files (e.g., `agent.log`). Never use `DEVNULL` during active development.
- **Unicode Safety**: Use `sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')` at the start of all scripts.

### 2. Cloud Migration Strategy
When moving agents from local Windows to isolated cloud containers (e.g., Molab, GPU environments):
- **Avoid Network-Dependent Tunnels**: `npx`/`marimo-pair` bridges often fail in restricted environments due to TTY constraints or WAF. 
- **Direct File Injection (Bundling)**: Use a `deploy_all_to_molab.py` bundling script that reads local `.py` files and writes them directly to the remote container environment. This bypasses network-level authorization walls.
- **Master Runner Pattern**: Implement a remote `master_runner.py` that executes `subprocess.Popen` in an infinite loop (`while True`) to manage agent persistence. This maintains execution continuity even if the IDE/Notebook session is suspended or idle.
- **Modular AI Models**: Classify models into `reasoning`, `coding`, and `general` categories. Use an `active_model.config` symlink or copy method for dynamic switching controlled by a `model_switcher.py`.

### 3. Dual-Thread Autonomous Agent Deployment (WURK Pro v2.0 Pattern)
For agents with Telegram control and background polling:
1. **Pre-deploy validation**: Run `python -m py_compile script.py` to catch syntax errors.
2. **Foreground smoke test**: Run `python script.py` for 10-15s to surface import errors (`ModuleNotFoundError`), token validation failures (`bot.getMe()` 401), and port lock acquisition.
3. **Install missing deps**: `pip install <missing>` if smoke test fails on imports.
4. **Background launch**: Only after smoke test passes, use `Start-Process pythonw.exe -WindowStyle Hidden`.
5. **Post-launch verification**: Within 10s, verify (a) instance lock port is LISTENING (`netstat -ano | findstr LOCK_PORT`), (b) log contains startup markers (`[BOT-NAME] ... started`), (c) `bot.getMe()` returns valid username.
6. **Update fleet_status.json**: Record PID, status="running", version, port, timestamp.

**Why**: The WURK Pro v2.0 deploy script skipped steps 2-3 — `Start-Process` launched a process that crashed immediately on missing `python-docx` and `jina` imports, but the deploy script reported exit 0. The bot was only confirmed running after manual foreground run revealed and fixed the missing deps.

## Pitfalls & Gotchas

### ✅ Pitfall: Terminal Cleanup
Rule: Never use `subprocess.DEVNULL` for detached process `stdout`/`stderr` if you need to debug crashes.
Why: `DEVNULL` hides tracebacks, creating silent failure loops. 

### ✅ Pitfall: Tunnel Instability
Rule: Prefer Direct File Injection via script bundling over network-dependent `npx`/`marimo-pair` tunnels when managing highly-isolated cloud containers. 
Why: Network tunnels in cloud IDEs often require interactive auth that isn't supported in headless autonomous flows. Bundling code ensures zero-auth deployment.

### ✅ Pitfall: Python Pathing
Rule: Use absolute paths in `master_watchdog.py`.
Why: Relative paths fail when the watchdog is launched from a different context or the Windows Task Scheduler.

### ✅ Pitfall: Rate-Limit Backoff State Persistence
Rule: Persist rate-limit cooldown state to JSON (e.g., `wurk_rate_limit_state.json`) with `cooldown_until` timestamp; on restart, honor the remaining cooldown instead of immediately hammering the API.
Why: Stateless restarts after a crash cause immediate 429 floods, extending bans and wasting cycles.

### ✅ Pitfall: Stale Registration Logic
Rule: In agent registration flows, check for existing valid `api_key` in state **before** any HTTP call; return early if present.
Why: The AgentHansa agent crashed in a 60s retry loop because `register()` sent malformed POST bodies on every iteration despite a valid cached key — the early-return guard was placed after the HTTP call.

### ✅ Pitfall: Fleet Status Drift
Rule: `fleet_status.json` must reflect **actual process health** (liveness + progress), not just PID existence.
Why: The watchdog reported AgentHansa as "running" (PID 4024) while it was stuck in a registration retry loop — PID alive ≠ agent functional.

### ✅ Pitfall: Silent Background Process Crash on Windows
Rule: When using `Start-Process pythonw.exe -WindowStyle Hidden`, always verify the process stays alive by checking the instance lock port (e.g., `netstat -ano | findstr LOCK_PORT`) and log file for startup markers within 10 seconds. If missing, run the script in foreground (`python script.py`) first to surface import errors (`ModuleNotFoundError`, syntax errors) before backgrounding.
Why: `Start-Process` detaches the console; import errors crash the process silently with no visible stderr, leaving a stale port lock or no lock at all. The WURK Pro v2.0 deploy script exhibited this — `python-docx` and `jina` missing caused immediate exit, but the deploy script reported success (exit 0).

### ✅ Pitfall: Placeholder Token in Deploy Scripts
Rule: Deployment scripts that write `.env` must validate the real token is present (not `***` or placeholder) and call `bot.getMe()` before considering the bot "deployed."
Why: The WURK Pro v2.0 deploy script wrote `WURK_BOT_TOKEN=8786109587:***` to `.env`. The process started but Telegram API returned `401 Unauthorized` on `getUpdates` — the bot polled silently with zero functionality until the real token was supplied.

### ✅ Lesson: Dual-Thread Autonomous Agent Pattern
Rule: For autonomous agents with Telegram control, use a dual-thread architecture: (1) `background_worker` — polling loop (zero-LLM tokens) that discovers tasks, scores quality, and queues submissions; (2) `telegram_listener` — inline menu for manual approval/reject, real-time stats, instance control. Persist shared state in a single JSON file (e.g., `wurk_pro_state.json`).
Why: WURK Pro v2.0 implemented this cleanly — the background thread polls WURK API every 30s without LLM calls, only invoking 9Router for new unsubmitted tasks. The Telegram thread handles human-in-the-loop decisions for high-value tasks (quality > 80 or reward > threshold).

### ✅ Pitfall: Zero-Balance Trading Loops
Rule: Market-making agents must check `available > threshold` before entering order placement logic; log and skip cycles cleanly when dry.
Why: Polyester trader generated 14k+ "Insufficient funds" log lines per hour because it attempted orders on zero balances every 15s.

### ⚠️ User Preference: AgentHansa Disabled
Rule: AgentHansa is **permanently disabled** per user directive. Do not implement, run, or recommend AgentHansa workflows in fleet management.
Why: User explicitly removed AgentHansa files (`agenthansa_agent.py`, `agenthansa_state.json`, `agenthansa_agent.log`) and updated `fleet_status.json` to remove the worker. The platform's aggressive rate limits (422/429 on registration), mandatory alliance selection, email verification prerequisite for wallet setup, and challenge/verify registration flow make it high-maintenance compared to WURK.
Fix: Remove AgentHansa references from watchdog and fleet orchestration. If re-enabling is requested, implement manual website registration first (avoids API rate limits), then use the verified API key directly in state.

## Revision History
- v1.1.0: Added Cloud Migration and Direct File Injection procedures for high-performance GPU environments.
- v1.0.0: Initial release — standard procedures for Watchdog, Windows persistence, and Unicode safety.
