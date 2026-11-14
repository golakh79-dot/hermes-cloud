---
name: python-background-bots
description: Use when managing Windows Python background bots safely.
---

# Python Background Bots on Windows

## Rules
- Never use `taskkill /IM python.exe` indiscriminately because it kills the Hermes gateway itself. Target specific PIDs or script filenames via PowerShell.
- Always clear Telegram webhooks (`deleteWebhook`) before polling or starting a new bot instance to prevent HTTP 409 Conflict errors.
- Use `Start-Process pythonw.exe` to spawn detached background processes on Windows so terminals do not block and bots run 24/7.
- **Instance Lock**: Every bot script must acquire a socket/port lock (e.g., `socket.bind(("127.0.0.1", LOCK_PORT))`) on startup. Exit cleanly if lock is held by another instance — prevents 409 conflicts and duplicate polling.
- **Startup Token Validation**: Call `bot.getMe()` (or equivalent Telegram API) immediately after loading the token. Log the bot username and exit with code 1 if invalid — prevents silent dead polling loops.
- **Graceful Error Handling**: Wrap the main polling loop in broad `try/except` that logs errors and sleeps briefly, never crashes the process. Background bots must self-heal.
- **Webhook Cleanup**: Always call `deleteWebhook` with `drop_pending_updates=False` on startup to ensure clean `getUpdates` polling.
- **Verify Background Process Survival**: After `Start-Process pythonw.exe`, check the instance lock port (`netstat -ano | findstr LOCK_PORT`) and log file for startup markers within 10s. If absent, run `python script.py` in foreground first to surface import/syntax errors.
- **Validate Real Tokens in Deploy Scripts**: Deployment scripts writing `.env` must verify tokens are real (not `***` placeholders) via `bot.getMe()` before marking deploy success.

## Recommended Deployment Pattern — PowerShell Deploy Script (Full)
Create a `.ps1` deploy script per bot that handles:
1. Kill existing instances on lock port + by script name
2. Setup `.env` with template + user placeholders
3. Install Python deps (`polyester-sdk`, `python-telegram-bot`, etc.)
4. Syntax check: `python -m py_compile script.py`
5. Initialize state JSON if missing
6. Start as background **PowerShell Job** (not pythonw) for log capture:
```powershell
$job = Start-Job -ScriptBlock {
    param($scriptFile, $logFile)
    & $env:PythonExe $scriptFile 2>&1 | Tee-Object -FilePath $logFile -Append
} -ArgumentList $ScriptFile, $LogFile -Name "BotName"
```
7. Verify startup: wait 3-5s, check port lock (`netstat -ano | findstr LOCK_PORT`), check process via `Get-CimInstance`, tail log for startup markers

## Process Management
```powershell
# Find ONLY your bot by command line (not all python)
Get-CimInstance Win32_Process -Filter "Name LIKE 'python%'" | Where-Object { $_.CommandLine -like '*script_name.py*' } | Select-Object ProcessId, CommandLine

# Verify port lock ownership
netstat -ano | findstr LOCK_PORT
# Then map PID -> command line:
Get-CimInstance Win32_Process -Filter "ProcessId=<PID>" | Select-Object ProcessId,CommandLine
```

## Dual-Thread Bot Architecture (Background Worker + Telegram Listener)
- Run both loops in **same process** via `asyncio.gather(background_worker(), telegram_listener())`
- **Port lock**: Bind `socket.bind(("127.0.0.1", LOCK_PORT))` at module import — exit if held
- **State persistence**: Flat JSON (`bot_pro_state.json`) with dataclass — cycle count, pending approvals, submitted orders, recent fills, consecutive zero cycles, last error, uptime
- **Manual approval gate**: High-value operations (notional >= threshold) → `pending_approvals` dict → require Telegram inline-button approval before execution
- **Monitoring mode**: When all balances zero for >5 cycles, switch to `monitoring` mode — log once per 10 cycles, skip API calls entirely
- **Quality scoring**: 0-100 per operation based on spread, notional, liquidity — log with each action
- **Graceful shutdown**: `save_state()` on exit; `load_state()` on restart preserves approvals and submitted items

## Token Validation Before Deploy
Deployment scripts MUST verify bot tokens are real (not `***` placeholders) via Telegram API:
```powershell
curl -s "https://api.telegram.org/bot$TOKEN/getMe" | Select-String '"ok":true'
```
Exit with clear error if invalid — prevents silent dead polling loops.

## Log Spam Prevention for Zero-Balance Traders
- Track `consecutive_zero_cycles` in state
- When >= 5: reduce log frequency to every 10th cycle, skip API order calls entirely
- Log single "monitoring mode" line instead of per-cycle "Insufficient funds"
- Resume normal frequency when balance > threshold

## Pitfalls Learned (Hermes Hub v2.0 Refactor)
- **.env path resolution**: `SettingsConfigDict(env_file=".env")` resolves relative to the *working directory*, not the module file. When running `python -m hub` from a parent directory, the .env is not found. Fix: `env_file=Path(__file__).parent / ".env"` in `model_config` so it always loads from the hub directory.
- **Batch file line continuation**: In `.bat` files, a line ending with backslash continues to the next line. The command `pip install -r hub\requirements.txt` split across two lines caused "Permission denied / not recognized" errors. Fix: keep each command on a single line.
- **Circular import in telegram_ui**: `from telegram_ui import run_system_cleanup` inside the same module creates a circular reference if `guardian.py` also imports it. Fix: define `run_system_cleanup` as a standalone function in `telegram_ui.py` (no self-import) and import from the module in `guardian.py`.
- **sanitize_python_code import**: `main.py` imported `sanitize_python_code` from `doctor` but the public API is `validate_and_repair`. Fix: either export `sanitize_python_code` from `doctor.__init__` or use the public API.
- **Process manager log redirection**: Opening log files in `"a"` mode without `buffering=1` causes delayed writes. Fix: `open(log_path, "a", buffering=1, encoding="utf-8")` for line-buffered output.
- **PID registry cleanup**: On graceful stop, remove the PID from `state["pid_registry"]` inside the state lock, not after — otherwise a concurrent guardian heal job may see a stale PID and attempt to restart an already-stopping process.
- **Regex escaping in re.sub replacements**: Raw strings in replacement patterns treat backslashes specially. Use double backslashes (`\\n`) in replacement strings, or use non-raw strings for replacements.
- **Entry point convention**: `python -m hub` fails with `No module named hub` when cwd is the hub dir. Use `python __main__.py` from the hub directory, or run `python -m hub` from the parent directory (`scripts/`).
- **Orphaned process sync on startup**: Guardian auto-heal loop fires false positives if PID registry is empty while scripts are already running (orphaned from previous hub instance). Fix: in `ProcessManager.__init__`, scan `psutil.process_iter()` for matching script names and populate PID registry before guardian starts.
- **Log file handle leak**: In `start_script`, log file opened with `open(log_path, "a")` but never closed after successful spawn — handle leaks and prevents proper cleanup. Fix: track open handles in `self._log_files[script_name] = log_file` and close them after process starts, or use context managers properly.
- **is_running fallback to cmdline scan**: PID registry can be stale (process died but registry not updated) or empty (orphaned processes). Fix: `is_running()` should fallback to scanning cmdline for script name when PID registry check fails.
- **Portalocker pywin32 dependency on Windows**: `portalocker` requires `pywin32` which may be missing or broken. Fix: lazy import with try/except and fallback to `threading.RLock` for thread safety only (no cross-process locking).
- **Backup file filtering in script discovery**: `discover_scripts()` must exclude `.bak.*` files (created during edits) or they appear as manageable scripts. Fix: add `and ".bak." not in fname` filter.