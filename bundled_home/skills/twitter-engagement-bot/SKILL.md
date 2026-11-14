---
name: twitter-engagement-bot
version: 1.0.0
author: alireza
license: MIT
description: "Autonomous engagement hub for Web3 Twitter/X activity."
metadata:
  hermes:
    tags: [twitter, engagement, automation, 9router, web3, engagement]
---

# Twitter Engagement Bot - Always-On Rules

## When to Use This Skill
Use when managing an autonomous bot that polls Twitter/X accounts, analyzes posts for Web3 relevance, and provides human-like engagement (replies) or daily digests using a local 9Router brain.

## Workflow
1. **Instance Lock**: Every script must acquire a file or socket lock (e.g., port 59421) on startup to prevent `Conflict 409` errors from multiple running instances.
2. **Layered Ingestion**: Combine multiple scraping sources (Twitter syndication, Jina Reader, 9Router `/web/fetch`) to ensure post discovery even if one channel is blocked.
3. **Time/Virality Engine**: Filter posts by age (e.g., < 20 min) and score virality using a local LLM to prioritize high-impact engagement.
4. **Humanization/Anti-Slop**: Sanitize output to remove LLM-isms ("landscape", "tapestry", "game-changer") and punctuation, ensuring replies feel like authentic Web3 community participation.
5. **Interactive Controls**: Use Telegram inline keyboards for the control panel (Toggle radar, scan now, alpha generation, model switching).
6. **Background Operation**: Always use `pythonw.exe` with `-WindowStyle Hidden` for deployment to keep the process running without terminal locking.

## Pitfalls & Best Practices
- **Never Kill Python**: Never use `taskkill /F /IM python.exe` or `Stop-Process -Name python*` in commands that might kill the agent itself. Use specific process filtering (e.g., by command line) to isolate the target agent.
- **Conflict 409 Avoidance**: Always bind a static socket/lock port on startup.
- **Sanitization**: Human replies must be strictly one-liner, lowercase-friendly, zero punctuation (no periods/hashtags/emojis), to avoid being flagged by automated spam filters.
- **Error Handling**: Use broad `try/except` blocks in polling loops to prevent crashes; log errors instead of exiting.
- **Webhook Management**: Call `deleteWebhook` on Telegram bot initialization to ensure clean `getUpdates` polling.
- **LLM JSON Extraction**: LLM outputs frequently include thinking blocks (`<thinking>...</thinking>`), markdown fences (```json), or mixed text. Always wrap LLM calls with a robust extractor that strips these artifacts, finds the first `{...}` block, and falls back to fixing trailing commas/single quotes before giving up. This prevents `json.JSONDecodeError: Expecting value` and `Extra data` crashes.
- **Exponential Backoff on Rate Limits**: Both 9Router chat calls and Twitter Syndication API calls must implement retry with exponential backoff (base 2s, max 3 attempts). HTTP 429 from Syndication API is expected under load; retry silently with backoff instead of logging as fatal.
- **Startup Token Validation**: Validate Telegram bot token on startup via `getMe` call. Fail fast with a clear log message if invalid — prevents silent polling loops that never receive updates.
- **Layered Fallback Ingestion**: Syndication API is the primary source; when it returns no tweets or hits persistent errors, fall back to Jina Reader (`r.jina.ai`) scraping. This two-layer approach ensures post discovery even when one channel is blocked.

## Deployment
Use `pythonw.exe` for background execution in a Windows environment to avoid keeping consoles open:
```powershell
Start-Process pythonw.exe -ArgumentList "path/to/script.py" -WindowStyle Hidden
```
