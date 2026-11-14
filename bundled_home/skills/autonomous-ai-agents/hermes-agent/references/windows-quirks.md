# Windows-Specific Quirks

Hermes runs natively on Windows (PowerShell, cmd, Windows Terminal, git-bash
mintty, VS Code integrated terminal). Most of it just works, but a handful
of differences between Win32 and POSIX have bitten us — document new ones
here as you hit them so the next person (or the next session) doesn't
rediscover them from scratch.

### Input / Keybindings

**Alt+Enter doesn't insert a newline** — Windows Terminal (and mintty) grab it
for fullscreen before prompt_toolkit sees it. Use **Ctrl+Enter** instead (the
CLI binds it to newline on Windows; raw Ctrl+J does the same, harmlessly).
To inspect how your terminal reports a keystroke, run
`python scripts/keystroke_diagnostic.py` from the repo root.

### Config / Files

**HTTP 400 "No models provided" on first run** — `config.yaml` was saved with
a UTF-8 BOM (Notepad does this). Re-save as UTF-8 without BOM;
`hermes config edit` writes correctly.

### `execute_code` / Sandbox

**WinError 10106** from the sandbox child process — it can't create an
`AF_INET` socket. Root cause is usually Hermes's env scrubber dropping
`SYSTEMROOT`/`WINDIR`/`COMSPEC` (Python's `socket` needs `SYSTEMROOT` to find
`mswsock.dll`), not a broken Winsock LSP. The `_WINDOWS_ESSENTIAL_ENV_VARS`
allowlist in `tools/code_execution_env.py` covers it; if you still hit it,
echo `os.environ` inside an `execute_code` block to confirm `SYSTEMROOT` is set.

### Testing on Windows

Prepare the checkout through PM first. With its Python 3.14, build an independent
test environment at a fresh path:

```powershell
python -m pm.build_env --source . --out .venv --group dev --group test
```

The output must not exist. Before regeneration, stop its processes and explicitly
remove only that disposable environment. Do not install into the application
payload or modify a selected dependency generation.

Run the canonical runner through Git Bash:

```bash
scripts/run_tests.sh tests/foo/test_bar.py -v --tb=short
```

The runner discovers `.venv/Scripts/python.exe`, clears credentials and
`PYTHONPATH`, and isolates each test file. For an external test environment,
set `HERMES_PYTHON` to its Python executable. PM shell activation alone does
not supply pytest after the runner clears `PYTHONPATH`.

### Path / Filesystem

**Line endings.** Git may warn `LF will be replaced by CRLF`. Cosmetic — the
repo's `.gitattributes` normalizes. Don't let editors auto-convert committed
POSIX-newline files to CRLF.

**Forward slashes work almost everywhere.** `C:/Users/...` is accepted by
every Hermes tool and most Windows APIs. Prefer forward slashes in code
and logs — avoids shell-escaping backslashes in bash.

### Python Module Resolution on Windows

**`python -m hub` fails with "No module named hub" when cwd is inside the package dir.**

When the working directory IS the package directory (e.g., `scripts/hub/`), Python cannot find the module via `-m` because it adds the parent of the package to `sys.path`, not the cwd. Fix: use `python __main__.py` instead, or `cd .. && python -m hub`.

**Entry point scripts should use `__main__.py` as the executable target** in launchers (`run_hub.bat`, `run_hub.sh`) to avoid this class of issue entirely.

### Portalocker on Windows

**`portalocker` requires `pywin32` (specifically `pywintypes`) for Win32Locker.**

If `pywin32` is not installed, `portalocker.lock()` raises `ImportError: pywintypes is required for Win32Locker but not found.`

**Fix:** Wrap all portalocker calls in a try/except with a silent fallback:
```python
try:
    import portalocker
    HAS_PORTALOCKER = True
except ImportError:
    HAS_PORTALOCKER = False
    portalocker = None

def _try_lock(f, mode):
    if not HAS_PORTALOCKER or portalocker is None:
        return False
    try:
        portalocker.lock(f, mode)
        return True
    except Exception:
        return False
```
Advisory locking is best-effort — the hub runs correctly without it, just without cross-process locking guarantees.

### Subprocess Creation Flags

**Never use `CREATE_NEW_CONSOLE` for background workers.** It spawns visible CMD windows that clutter the desktop and break clean shutdown.

**Correct flags for detached background processes on Windows:**
```python
CREATE_NO_WINDOW = 0x08000000
DETACHED_PROCESS = 0x00000008
CREATE_BREAKAWAY_FROM_JOB = 0x01000000
creationflags = CREATE_NO_WINDOW | DETACHED_PROCESS | CREATE_BREAKAWAY_FROM_JOB
```
On Unix, use `start_new_session=True` instead.

Always redirect stdout/stderr to persistent log files (not `subprocess.DEVNULL`) — hidden output masks `SyntaxError`, `ModuleNotFoundError`, and other startup failures, creating silent crash loops.

### Regex Replacement Strings in Raw Strings

**`re.sub` replacement strings treat backslashes specially, even inside raw strings.**

In a raw string `r"\n"`, the two characters backslash+n are literal. But when used as a *replacement* in `re.sub`, the regex engine interprets `\n` as the newline escape.

```python
# WRONG — SyntaxError or wrong replacement
code = re.sub(r"pattern", r"\n", text)

# CORRECT — double the backslash in replacement
code = re.sub(r"pattern", r"\\n", text)
# OR use a non-raw string for replacement
code = re.sub(r"pattern", "\n", text)
```
This bit `sanitize_python_code()` in `doctor.py` — markdown fence stripping used `r"\n"` in replacement and produced invalid escape sequences.

**Also applies to `re.sub(r"```\n", r"\n", text)` — the replacement `r"\n"` is interpreted as literal backslash+n. Fix: use `"\n"` (non-raw) or `r"\\n"` for the replacement parameter.**

### BOT_TOKEN Format Validation

**Telegram bot tokens MUST contain a colon** (format: `123456:ABC-DEF...`).

`pydantic-settings` validates on load; `telebot.TeleBot()` validates on init. If using a test token in `.env`, ensure it matches the pattern: `os.environ["BOT_TOKEN"] = "123456:ABC-DEF-GHI-JKL"`.

### Admin ID Type

**ADMIN_ID must be an integer**, not a string. `pydantic-settings` handles the coercion from `.env` string to int, but manual overrides in code must pass `int`.

### .env Path Resolution in pydantic-settings

**`SettingsConfigDict(env_file=".env")` resolves relative to the *working directory*, not the module file.**

When running `python -m hub` from a parent directory, the .env is not found because cwd is the parent. Fix: use absolute path from `__file__`:
```python
model_config = SettingsConfigDict(
    env_file=Path(__file__).parent / ".env",
    env_file_encoding="utf-8",
    extra="ignore"
)
```
This ensures the .env is always loaded from the same directory as the settings module.

### Circular Import in telegram_ui

**`from telegram_ui import run_system_cleanup` inside `telegram_ui.py` creates a circular reference** if `guardian.py` also imports it.

Fix: define `run_system_cleanup` as a standalone function in `telegram_ui.py` (no self-import) and import from the module in `guardian.py`:
```python
# telegram_ui.py - standalone, no self-import
def run_system_cleanup(bot: telebot.TeleBot):
    ...

# guardian.py
from telegram_ui import run_system_cleanup
```

### Batch File Line Continuation

**In `.bat` files, a line ending with backslash continues to the next line.**

The command `pip install -r hub\requirements.txt` split across two lines caused "Permission denied / not recognized" errors. Fix: keep each command on a single line:
```bat
pip install -r hub\requirements.txt --quiet
```
Not:
```bat
pip install -r hub\
equirements.txt --quiet
```

### Windows Golden Rules (User-Mandated, Session 2026-11-10)

**Context**: User provided 5 hard-won rules for all Windows agent scripts. These are non-negotiable conventions that should be enforced in every script, launcher, and config.

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
- Single-instance: Bind TCP port at startup (see Port Lock pattern in autonomous-agent-maintenance)

### Module Resolution: python -m vs __main__.py

**`python -m hub` fails with "No module named hub" when cwd is inside the package dir.**

When the working directory IS the package directory (e.g., `scripts/hub/`), Python cannot find the module via `-m` because it adds the parent of the package to `sys.path`, not the cwd. Fix: use `python __main__.py` instead, or `cd .. && python -m hub`.

**Entry point scripts should use `__main__.py` as the executable target** in launchers (`run_hub.bat`, `run_hub.sh`) to avoid this class of issue entirely.

