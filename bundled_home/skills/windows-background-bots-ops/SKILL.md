---
name: windows-background-bots-ops
description: Use when managing Windows Python background bots safely.
---

# Windows Background Bots Ops

## Rules
- Never use `taskkill /IM python.exe` indiscriminately because it kills the Hermes gateway itself. Target specific PIDs or script filenames via PowerShell.
- Always clear Telegram webhooks (`deleteWebhook`) before polling or starting a new bot instance to prevent HTTP 409 Conflict errors.
- Use `Start-Process pythonw.exe` to spawn detached background processes on Windows so terminals do not block and bots run 24/7.
- Always embed persistent state handling (`json` state files) to track processed items and prevent duplicate triggers across bot restarts.
