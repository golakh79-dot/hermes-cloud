---
name: windows-quirks
description: "Use to fix Windows agent crashes and bot 409 conflicts."
---

# Windows Quirks & Bot Reliability

When running autonomous agents and Telegram bot panels on Windows, follow these rules to avoid crashes, encoding errors, and Telegram API conflicts:

### Console Output & Unicode
*   **Avoid Emojis in Print:** Windows default terminal crashes on non-ASCII characters like emojis.
*   **The 'Safe-Print' Rule:** Always use `.encode('ascii', 'ignore').decode('ascii')` on any string containing dynamic content before printing to stdout.
*   **Logging:** Save the full content to log files using `encoding='utf-8'`, but keep console output ASCII-only.
*   **Environment Variables:** Always set `PYTHONUTF8=1`, `PYTHONIOENCODING=utf-8`, and `PYTHONUNBUFFERED=1` when spawning Python background processes on Windows.

### File Handling & Document Code Extraction
*   **Sanitizing Docx Code:** When extracting Python code snippets from Word documents (`.docx`), automatically strip smart quotes, en-dashes (`–`), capitalized keywords (`Def`, `Import`), and verify compilation with `py_compile` before deployment.
*   **Forward Slashes:** Always use forward slashes (`/`) for paths even on Windows.
*   **Encoding:** Explicitly define `encoding='utf-8'` in all `open()` calls.

### Telegram Bot Reliability & 409 Conflict Prevention
*   **Single-Instance Socket Lock:** Bind a dedicated local port via `socket.socket(socket.AF_INET, socket.SOCK_STREAM)` at startup to prevent duplicate polling instances and Telegram `409 Conflict` errors.
*   **Webhook Clearance & Offset Sync:** Always call `setWebhook?url=` and sync initial offset via `getUpdates?offset=-1` to clear stale backlog updates and prevent polling conflicts.
*   **Process Ghost Cleanup:** Before restarting a Telegram bot or background worker, explicitly terminate all competing Python instances matching the script name using Windows CIM/WMI commands.
*   **Verify Background Process Survival After `Start-Process`:** When launching with `Start-Process pythonw.exe -WindowStyle Hidden`, the console detaches and import/syntax errors crash the process silently. Always verify within 10s: (a) instance lock port is LISTENING (`netstat -ano | findstr LOCK_PORT`), (b) log file contains startup markers, (c) `bot.getMe()` returns valid username. If verification fails, run `python script.py` in foreground first to surface errors.
*   **Validate Real Tokens in Deploy Scripts:** Deployment scripts that write `.env` must verify tokens are real (not `***` placeholders) by calling `bot.getMe()` before marking deploy success. The WURK Pro v2.0 deploy script wrote a placeholder token and reported success while the bot returned `401 Unauthorized` on polling.
*   **PowerShell Job + Tee-Object Pattern (Preferred over `pythonw.exe`):** Deploy scripts should start bots as PowerShell background Jobs with `Tee-Object` for log capture:
    ```powershell
    $job = Start-Job -ScriptBlock { param($scriptFile, $logFile) & $env:PythonExe $scriptFile 2>&1 | Tee-Object -FilePath $logFile -Append } -ArgumentList $ScriptFile, $LogFile -Name "BotName"
    ```
    This keeps logs visible, avoids silent crashes, and enables `Get-Job`/`Stop-Job` management.
*   **Port Lock Verification:** After bot start, confirm `netstat -ano | findstr LOCK_PORT` shows the expected PID, then verify via `Get-CimInstance Win32_Process -Filter "ProcessId=<PID>" | Select-Object ProcessId,CommandLine` that the correct script is running.
*   **Startup Marker Logging:** Bot scripts must log a distinct startup marker (e.g., `[BOT-NAME] Telegram listener started on port XXXXX`) within 5 seconds. Deploy scripts tail the log to confirm.

### API Credentials & Validation
*   **Token Persistence & Verification:** Restart the Python process immediately after updating tokens or scripts. Verify connectivity via `/getMe` endpoint before full deployment.
