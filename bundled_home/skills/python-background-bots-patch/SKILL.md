---
name: python-background-bots-patch
description: Use when managing Windows Python background bots safely.
---

# Python Background Bots on Windows

## Rules
- Never use `taskkill /IM python.exe` indiscriminately because it kills the Hermes gateway itself. Target specific PIDs or script filenames via PowerShell filters:
  `Get-CimInstance Win32_Process | Where-Object { $_.CommandLine -like '*script_name.py*' } | Stop-Process -Force`
- Always clear Telegram webhooks (`deleteWebhook`) before polling or starting a new bot instance to prevent HTTP 409 Conflict errors.
- Use `Start-Process pythonw.exe -ArgumentList 'path/to/script.py'` to spawn detached background processes on Windows so terminals do not block and bots run 24/7.
- All persistent autonomous scripts must reside on non-system drives (e.g., `D:\`) to avoid C:\ drive permissions or cleanup issues.
- **Verify Background Process Survival**: After `Start-Process pythonw.exe`, check the instance lock port (`netstat -ano | findstr LOCK_PORT`) and log file for startup markers within 10s. If absent, run `python script.py` in foreground first to surface import/syntax errors.
- **Validate Real Tokens in Deploy Scripts**: Deployment scripts writing `.env` must verify tokens are real (not `***` placeholders) via `bot.getMe()` before marking deploy success.
