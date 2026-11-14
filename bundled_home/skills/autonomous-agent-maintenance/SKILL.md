---
name: autonomous-agent-maintenance
description: "Use to maintain persistent background Windows agents."
version: 1.0.0
author: Hermes Agent
platforms: [windows]
---

# Autonomous Background Worker Maintenance

Use for maintaining persistent autonomous agents (WURK, AgentHansa, Polyester, etc.) on Windows that run in the background without UI.

## Persistent Maintenance Workflow

### 1. Robust Supervision & Job Object Breakaway
Windows Job Objects terminate child processes when the parent shell or command exits. To maintain true persistence:
- Use a persistent supervisor script (`master_watchdog.py`) launched via independent process creation flags.
- When launching child processes via `subprocess.Popen` on Windows, use creation flags that break away from the parent Job Object to prevent termination upon command exit:
  ```python
  CREATE_NO_WINDOW = 0x08000000
  DETACHED_PROCESS = 0x00000008
  CREATE_BREAKAWAY_FROM_JOB = 0x01000000
  creationflags = CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_BREAKAWAY_FROM_JOB
  ```
- **NEVER** use `/dev/null` or `subprocess.DEVNULL` for stderr/stdout of workers if you want to debug crashes; always redirect to persistent log files.

### 2. UTF-8 & Environment Configuration
Windows background processes often fail due to locale-specific character encoding errors.
- Always force UTF-8 for child processes via `os.environ`:
  ```python
  env = {**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"}
  ```
- Invoke python with `-X utf8` and `-u` (unbuffered) to force standard library support and avoid log lag:
  `[sys.executable, "-X", "utf8", "-u", script_path]`

### 3. Debugging & Diagnostic Path
When workers "disappear":
1. **Verify processes**: `tasklist | findstr python`
2. **Log isolation**: Redact credentials from logs, but redirect *all* stdout/stderr of workers to dedicated log files.
3. **Timeout Testing**: When testing workers, avoid infinite blocking `subprocess.Popen` without health checks. Use `subprocess.run(..., timeout=N)` or manual health-check pings to identify deadlocks.

### 4. Telegram Bot Token Management (Session 2026-11-05)
**Context**: User updated Telegram bot token for @Hermixxbot from placeholder to valid token and resolved 401 Unauthorized errors.

**Procedure**:
- Always store the valid bot token from BotFather in the `BOT_TOKEN` variable in `twitter_telegram_bot_panel.py` (or equivalent script).
- If the bot returns `HTTP Error 401: Unauthorized`, verify the token endpoint explicitly via `tg_api('getMe')` to distinguish a dead token from an implementation bug.
- Update the token in the script and restart the process — do not rely on `.env` reload alone, as the Python process may cache the old token.
- Restart the worker via the watchdog (`master_watchdog.py`) after token update to ensure clean process detachment.

**Pitfall**: Using `subprocess.DEVNULL` for stderr/stdout hides `SyntaxError` and `ModuleNotFoundError`, creating silent failure loops. Always redirect to persistent log files (`twitter_hub.log`, `wurk_agent.log`, etc.).

**Verification**: After token update, send a test message via `/sendMessage` API to confirm connectivity before relying on the bot for critical tasks.

## Pitfalls
- **Job Object Child Termination**: Shell background operators (`&`) or normal `subprocess.Popen` without breakaway flags will cause Windows to kill background Python workers as soon as the shell session completes. Use breakaway creation flags.
- **Output Truncation**: Redirecting stderr to `NUL` or `/dev/null` hides `SyntaxError` or `ModuleNotFoundError`, creating a "silent failure" loop. Always pipe stderr to a persistent disk log.
- **Path Resolution**: Never use hardcoded relative paths. Use absolute paths joined from the Hermes home directory (e.g., `os.path.join(HOME_DIR, "scripts", "worker.py")`).
- **Rate-Limit Backoff State Persistence**: Persist rate-limit cooldown state to JSON (e.g., `wurk_rate_limit_state.json`) with `cooldown_until` timestamp; on restart, honor the remaining cooldown instead of immediately hammering the API. Stateless restarts after a crash cause immediate 429 floods, extending bans and wasting cycles.
- **Stale Registration Logic**: In agent registration flows, check for existing valid `api_key` in state **before** any HTTP call; return early if present. The AgentHansa agent crashed in a 60s retry loop because `register()` sent malformed POST bodies on every iteration despite a valid cached key — the early-return guard was placed after the HTTP call.
- **Fleet Status Drift**: `fleet_status.json` must reflect **actual process health** (liveness + progress), not just PID existence. The watchdog reported AgentHansa as "running" (PID 4024) while it was stuck in a registration retry loop — PID alive ≠ agent functional.
- **Zero-Balance Trading Loops**: Market-making agents must check `available > threshold` before entering order placement logic; log and skip cycles cleanly when dry. Polyester trader generated 14k+ "Insufficient funds" log lines per hour because it attempted orders on zero balances every 15s.

## Pro Architecture Patterns (Dual-Thread + Telegram Control)

**Use when**: Building production-grade autonomous traders/workers that need manual oversight, state persistence, and zero-downtime deploys. Applied to WURK Pro v2.0 and Polyester Pro v1.0.

### 1. Dual-Thread Design
- **Pattern**: `background_worker` (core loop) + `telegram_listener` (control plane) running in same process via `asyncio.gather()`.
- **Why**: Single process, shared memory (`bot_state` with `threading.Lock`), no IPC overhead. Telegram provides real-time control (pause/resume, approve/reject, status, volume) without external dependencies.
- **Implementation**: Both coroutines share a `BotState` dataclass protected by `state_lock = threading.Lock()`. All mutations wrapped in `with state_lock:`.

### 2. Port Lock (Single-Instance Enforcement)
- **Pattern**: Bind TCP localhost port at startup (`socket.bind(("127.0.0.1", LOCK_PORT))`). Unique port per bot: WURK=59422, Twitter=59421, Polyester Pro=59423.
- **Why**: Prevents accidental duplicate instances. Deploy script kills existing processes on that port before starting.
- **Verification**: `netstat -ano | findstr :<PORT>` shows LISTENING with owning PID.

### 3. State Persistence (Flat JSON + Dataclass)
- **Pattern**: `BotState` dataclass with `to_dict()`/`from_dict()` serialization. Saved to `<bot>_pro_state.json` in Hermes home.
- **Fields**: mode, cycle_count, total_volume, total_trades, successful/failed trades, pending_approvals, submitted_orders, recent_fills, consecutive_zero_cycles, last_error, started_at.
- **Atomic writes**: `save_state()` called inside `state_lock`; deploy script backs up existing state before overwrite.
- **Graceful recovery**: `load_state()` on restart preserves pending approvals and submitted orders.

### 4. Manual Approval Gate
- **Pattern**: Orders with notional >= `HIGH_VALUE_THRESHOLD` go to `pending_approvals` dict. Telegram inline buttons (`approve:<cid>`, `reject:<cid>`) move order to submitted or discard.
- **Why**: Human-in-the-loop for high-value/risky actions without blocking the background loop.
- **Staleness protection**: Add `max_approval_age_seconds` config; on startup, reject stale approvals and notify admin.

### 5. Monitoring Mode (Zero-Balance Spam Prevention)
- **Pattern**: Track `consecutive_zero_cycles`. When >= 5: switch `mode="monitoring"`, log once per 10 cycles, skip all API order calls.
- **Why**: Prevents 14k+ log lines/hour of "Insufficient funds" spam. Resumes active trading automatically when balance > threshold.

### 5. Quality Scoring (0-100)
- **Pattern**: `calc_quality_score(symbol, side, price, qty, spread_pct)` — factors: spread tightness, notional size, pair liquidity. Logged with every order.
- **Why**: Enables post-hoc analysis of trade quality; can feed into adaptive spread strategies.

### 6. Deploy Script Standards (PowerShell)
- **Steps**: Kill existing on port → Setup .env with validation → Check Python deps → Syntax check (`python -m py_compile`) → Init state file → Start as background Job → Verify port lock + log tail.
- **Validation**: Required env vars checked before start; clear error if missing. Supports `-ForceRestart`, `-SkipPortCheck`, `-CustomEnvPath`.

### 7. Logging Standards
- **Format**: `[TIMESTAMP] [TAG] message` — TAG = `[WORKER]`, `[TG]`, `[ORDER]`, `[APPROVAL]`, `[BALANCE]`, `[MODE]`, `[LOCK]`.
- **Encoding**: UTF-8 file, ASCII-safe stdout (`msg.encode('ascii', 'ignore').decode('ascii')`).
- **Location**: `scripts/<bot>_pro_trader.log` for Pro versions.

## Modular Agent Hub Architecture (Hermes Hub v2.0)

**Use when**: Replacing a monolithic bot script with a clean, secure, maintainable modular hub that manages multiple background workers via Telegram.

## Windows Golden Rules (User-Mandated, Session 2026-11-10)

**Context**: User provided 5 hard-won rules for all Windows agent scripts. These are non-negotiable conventions.

1. **PATHS**: Never use bare backslashes (\r, \n, \t, \a, \b) in paths — use `os.path.join` or Raw Strings (r"...")
2. **SINGLE-INSTANCE**: Every 24/7 bot must have single-instance lock (token/port) to prevent double-run
3. **ANTI-DIE LOOP**: All network loops (Telegram, Web3, exchange) must be in `while True` with `try/except` + `sleep` for auto-recovery
4. **UTF-8 EVERYWHERE**: Open files with `encoding="utf-8"`; run Python with `-X utf8` flag for emoji/Persian support
5. **STANDARD LOCATION**: Main executable scripts go in `D:/HERMES/Hermes_Portable_Data/home/scripts` (or modular subfolder with bug-free launcher)

### Enforcement in Code
- `config.py`: `env_file=Path(__file__).parent / ".env"` (absolute path from module)
- `run_hub.bat`: `cd /d "%~dp0"` then `python __main__.py` (no `-m` when cwd is package dir)
- `process_mgr.py`: `creationflags = CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_BREAKAWAY_FROM_JOB`
- All `open()` calls: `encoding="utf-8"`
- Child env: `PYTHONIOENCODING=utf-8`, `PYTHONUTF8=1`
- Single-instance: Bind TCP port at startup (see Port Lock pattern above)

### Pitfalls Learned (This Session)
- **Batch file line continuation**: In `.bat` files, a line ending with backslash continues to the next line. `pip install -r hub\requirements.txt` split across lines caused "Permission denied / not recognized" errors. Fix: keep each command on a single line.
- **Module resolution**: `python -m hub` fails with `No module named hub` when cwd is the hub dir. Use `python __main__.py` or run from parent dir.
- **Portalocker on Windows**: Requires `pywin32`. Without it, `portalocker.lock()` raises `ImportError: pywintypes`. Always wrap in try/except with silent fallback.
- **Regex escaping in `re.sub` replacements**: Raw strings in replacement treat backslashes specially. `r"\n"` → two chars `\` + `n`, but regex engine interprets as newline. Fix: use `"\n"` (non-raw) or `r"\\n"` for replacements. Affected `sanitize_python_code()` markdown fence stripping.
- **Circular import in telegram_ui**: `from telegram_ui import run_system_cleanup` inside the same module creates a circular reference if `guardian.py` also imports it. Fix: define `run_system_cleanup` as a standalone function (no self-import) and import from the module in `guardian.py`.
- **Process manager log handle leak**: `start_script` opens log file but never closes it on success path, leaking handles. Fix: close log file after successful process launch.
- **PID registry bootstrap (critical)**: On hub startup, `pid_registry` is empty but workers may already be running (from previous hub instance). Guardian sees empty registry → treats all as "down" → restart loops while ports are occupied. Fix: in `ProcessManager.__init__`, scan existing processes via `psutil` for known scripts and populate `pid_registry` before guardian starts.
- **`is_running()` fallback**: Current implementation only trusts `pid_registry`. If registry is stale/empty, it returns False even if process is alive. Fix: add cmdline-based fallback scan when PID not in registry or process gone — verify via `psutil.process_iter()` matching script name in cmdline.

## Modular Agent Hub Architecture (Hermes Hub v2.0)

### Structure
```
scripts/hub/
├── __init__.py          # Package marker
├── __main__.py          # Entry point (run via `python __main__.py` from hub dir)
├── config.py            # pydantic-settings, .env loading, validation
├── state.py             # Thread-safe JSON + portalocker (with fallback)
├── process_mgr.py       # Process lifecycle: start/stop/restart/log/status
├── doctor.py            # Code sanitize, AST validate, optional AI repair
├── telegram_ui.py       # Handlers, keyboards, HTML escaping
├── guardian.py          # APScheduler background jobs (auto-heal, cleanup)
├── requirements.txt     # Pinned deps
├── run_hub.bat / .sh    # Launchers
└── .env.example         # Template
```

### Key Patterns

#### 1. Config: pydantic-settings + .env (never hardcode)
```python
# config.py
class Settings(BaseSettings):
    bot_token: str
    admin_id: int
    router_url: str = "http://127.0.0.1:20128/v1/chat/completions"
    home_dir: Path = Path("D:/HERMES/Hermes_Portable_Data/home")
    scripts_dir: Path = Field(default_factory=lambda: Path("${HOME_DIR}/scripts"))
    # ...
    model_config = SettingsConfigDict(env_file=Path(__file__).parent / ".env", env_file_encoding="utf-8", extra="ignore")
```

#### 2. State: Thread-safe JSON with portalocker fallback
```python
# state.py
try:
    import portalocker
    HAS_PORTALOCKER = True
except ImportError:
    HAS_PORTALOCKER = False
    portalocker = None

def _try_lock(self, f, mode):
    if not HAS_PORTALOCKER or portalocker is None:
        return False
    try:
        portalocker.lock(f, mode)
        return True
    except Exception:
        return False
```
Portalocker requires `pywin32` on Windows. The fallback ensures the hub runs even without it — advisory locking is best-effort.

#### 3. Process Management: No CREATE_NEW_CONSOLE
```python
# process_mgr.py
proc = subprocess.Popen(
    [sys.executable, "-u", script_path],
    stdout=log_file,
    stderr=log_file,
    creationflags=0,  # No CREATE_NEW_CONSOLE
    start_new_session=True,  # Unix: detach from parent
    env={**os.environ, "PYTHONIOENCODING": "utf-8", "PYTHONUTF8": "1"},
)
```
Redirect stdout/stderr to rotating log files. Track PIDs in state (`pid_registry`). Graceful stop: `SIGTERM` → wait timeout → `SIGKILL`.

#### 4. Code Doctor: Sanitize → Validate → Repair
```python
# doctor.py
def sanitize_python_code(raw_text: str) -> Tuple[str, bool, str]:
    # Strip BOM, markdown fences, normalize whitespace, fix smart quotes
    # Return (clean_code, is_valid, message)

def validate_and_repair(raw_code: str) -> Tuple[str, bool, str]:
    clean, ok, msg = sanitize_python_code(raw_code)
    if ok: return clean, True, msg
    ai_fixed = try_ai_repair(clean, msg)  # 9Router, run in ThreadPoolExecutor
    if ai_fixed and ast.parse(ai_fixed):
        return ai_fixed, True, f"AI repaired: {msg}"
    return clean, False, msg
```

**Pitfall**: Raw strings in `re.sub` patterns. Use double backslashes in replacement:
```python
# WRONG: r"\n" inside replacement → SyntaxError
# CORRECT:
code = re.sub(r"^```(?:python|py)?\s*\n", "", code, flags=re.IGNORECASE)
code = re.sub(r"\n```\s*$", "", code)
```

#### 5. Telegram UI: HTML escaping + Inline Keyboards
```python
# telegram_ui.py
@staticmethod
def escape_html(text: str) -> str:
    return html.escape(text)

# Use parse_mode="HTML" — NOT markdown (avoids escaping hell)
# Cache panel for 3s to avoid flood
```

#### 6. Guardian: APScheduler BackgroundScheduler
```python
# guardian.py
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger

scheduler.add_job(auto_heal_job, IntervalTrigger(seconds=settings.heal_interval_sec))
scheduler.add_job(cleanup_job, IntervalTrigger(seconds=settings.heal_interval_sec * settings.cleanup_interval_cycles))
```

#### 7. Entry Point: __main__.py with Signal Handling
```python
# __main__.py
def main():
    setup_logging()
    bot = telebot.TeleBot(settings.bot_token)
    # ... init components
    signal.signal(signal.SIGINT, _signal_handler)
    signal.signal(signal.SIGTERM, _signal_handler)
    if hasattr(signal, "SIGBREAK"):
        signal.signal(signal.SIGBREAK, _signal_handler)
    bot.infinity_polling(timeout=30, long_polling_timeout=20)
```
Run via `python __main__.py` — **not** `python -m hub` (avoids module resolution issues when run from hub/ dir).

#### 8. Launchers
```bat
:: run_hub.bat
cd /d "%~dp0"
if not exist .env (notepad .env & goto :eof)
pip install -r requirements.txt --quiet
python __main__.py
pause
```

### Pitfalls Learned
- **Portalocker on Windows**: Requires `pywin32`. Without it, `portalocker.lock()` raises `ImportError: pywintypes`. Always wrap in try/except with silent fallback.
- **Regex escaping in `re.sub` replacements**: Raw strings in replacement treat backslashes specially. `r"\n"` → two chars `\` + `n`, but regex engine interprets as newline. Fix: use `"\n"` (non-raw) or `r"\\n"` for replacements. Affected `sanitize_python_code()` markdown fence stripping.
- **Entry point**: `python -m hub` fails with `No module named hub` when cwd is the hub dir. Use `python __main__.py` or run from parent dir.
- **BOT_TOKEN format**: Must contain colon (`123:ABC`). pydantic-settings validates; telebot validates on init.
- **Admin ID**: Must be int. Load from .env → state on startup.
- **Create flags**: `CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_BREAKAWAY_FROM_JOB` for true background detachment on Windows.
- **UTF-8**: Force `PYTHONIOENCODING=utf-8` and `PYTHONUTF8=1` in child env; use `-u` flag for unbuffered output.
- **Log rotation**: Use `RotatingFileHandler` (5MB, 3 backups) — prevents log corruption from manual truncation.
- **.env path resolution**: `SettingsConfigDict(env_file=".env")` resolves relative to the *working directory*, not the module file. Fix: `env_file=Path(__file__).parent / ".env"` in `model_config`.
- **Batch file line continuation**: In `.bat` files, a line ending with backslash continues to the next line. Keep each command on a single line.
- **Circular import in telegram_ui**: `from telegram_ui import run_system_cleanup` inside the same module creates a circular reference if `guardian.py` also imports it. Fix: define `run_system_cleanup` as a standalone function (no self-import) and import from the module in `guardian.py`.
- **sanitize_python_code import**: `main.py` imported `sanitize_python_code` from `doctor` but the public API is `validate_and_repair`. Fix: either export `sanitize_python_code` from `doctor.__init__` or use the public API.
- **Process manager log redirection**: Opening log files in `"a"` mode without `buffering=1` causes delayed writes. Fix: `open(log_path, "a", buffering=1, encoding="utf-8")` for line-buffered output. Also: **the log file handle must be closed after successful process launch** — `start_script` opens `log_f` but never closes it on success path, leaking handles.
- **PID registry cleanup**: On graceful stop, remove the PID from `state["pid_registry"]` inside the state lock, not after — otherwise a concurrent guardian heal job may see a stale PID and attempt to restart an already-stopping process.
- **PID registry bootstrap (critical)**: On hub startup, `pid_registry` is empty but workers may already be running (from previous hub instance). Guardian sees empty registry → treats all as "down" → restart loops while ports are occupied. Fix: in `ProcessManager.__init__`, scan existing processes via `psutil` for known scripts and populate `pid_registry` before guardian starts.
- **`is_running()` fallback**: Current implementation only trusts `pid_registry`. If registry is stale/empty, it returns False even if process is alive. Fix: add cmdline-based fallback scan when PID not in registry or process gone — verify via `psutil.process_iter()` matching script name in cmdline.
