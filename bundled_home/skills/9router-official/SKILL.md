---
name: 9router-official
description: Use 9Router for AI chat, image, TTS, search, and fetch.
---

# 9Router

Local/remote AI gateway exposing OpenAI-compatible REST. One key, many providers, auto-fallback.

## Setup

```bash
export NINEROUTER_URL="http://localhost:20128"
export NINEROUTER_KEY="sk-..."
```

All requests: `${NINEROUTER_URL}/v1/...`
Verify: `curl $NINEROUTER_URL/api/health` → `{"ok":true}`
