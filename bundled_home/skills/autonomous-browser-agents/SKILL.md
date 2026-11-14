---
name: autonomous-browser-agents
description: Use when building browser agents to bypass bot walls.
---
# Autonomous Browser-Based Agent Strategy
- Use `playwright` for all autonomous web interactions to bypass Cloudflare/bot protections that block bare HTTP requests.
- Wrap all automated browser tasks in a persistent session with headers that mimic a real user agent.
- WURK agent: Utilize a headless Chromium session to navigate, click, and interact with the WURK platform, including handling SIWS (Sign-In With X) challenges.
- Twitter/X agent: Adopt the same browser-first approach to scrape content and perform interactions (replies/growth) that standard API requests now fail to handle due to 401/403 blocks.
- Implementation: Scripts must run as persistent daemon processes with visual logging to `runmanually` windows.
