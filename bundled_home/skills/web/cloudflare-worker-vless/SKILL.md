---
name: cloudflare-worker-vless
category: web
description: Deploy free VLESS proxy on Cloudflare Workers.
version: 1.0.0
author: Hermes Agent
license: MIT
tags: [cloudflare, worker, vless, proxy, serverless, free-tier]
related_skills: []
---

# Cloudflare Worker VLESS Proxy

**Use when** the user needs a free, serverless VLESS proxy on Cloudflare Workers with zero infrastructure cost.

## Procedure
1. **Verify API token** works:
   ```bash
   curl -H "Authorization: Bearer $TOKEN" https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/scripts
   ```

2. **Generate a UUID** for the user (use system UUID generator, not hardcoded).

3. **Use a clean, tested worker script** (module syntax, ES modules):
   - The canonical Free-VLESS script from GitHub has bugs — use a clean implementation instead
   - Reference: `references/clean-worker.js` (tested, working implementation)
   - Key features: VLESS over WebSocket, TLS, UUID auth, `cloudflare:sockets` TCP outbound, proper error handling
   - **Must deploy as module** (`application/javascript+module` via multipart form with `filename="worker.js"`)

4. **Deploy via multipart upload** (required for ES modules):
   ```bash
   curl -X PUT "https://api.cloudflare.com/client/v4/accounts/$ACCOUNT_ID/workers/scripts/$SCRIPT_NAME" \
     -H "Authorization: Bearer $TOKEN" \
     -F 'metadata={"main_module": "worker.js", "compatibility_date": "2026-10-05", "compatibility_flags": ["nodejs_compat"]}' \
     -F 'worker.js=@worker.js;type=application/javascript+module;filename="worker.js"'
   ```
   - **Must use `application/javascript+module`** content type in the form part
   - **Must include `filename="worker.js"`** in the form part
   - **Must include `compatibility_flags: ["nodejs_compat"]`** for `cloudflare:sockets` to work
   - The `workers_dev` flag in metadata is ignored; subdomain must be enabled manually in Dashboard

5. **Enable workers.dev subdomain** (one-time per account):
   - User must visit Dashboard → Workers & Pages → Overview → "Create your workers.dev subdomain"
   - Then for each Worker: Settings → Domains & Routes → Enable workers.dev
   - Cannot be automated via API with standard tokens

6. **Construct config URLs** after subdomain is active:
   - Worker URL: `https://$SCRIPT_NAME.$SUBDOMAIN.workers.dev`
   - Config endpoint: `https://$WORKER_URL/ws` (or custom path)
   - Returns both v2ray link and Clash Meta YAML

## Pitfalls
- **Module deployment requires multipart/form-data** — plain `application/javascript` fails with "Cannot use import statement outside a module". Use `-F` with `type=application/javascript+module` AND include `filename="worker.js"` in the form part.
- **workers.dev subdomain cannot be created via API** with User API Tokens — user must do it once in Dashboard (Settings → Domains & Routes → Enable workers.dev).
- **ProxyIP fallback** (`cdn.xn--b6gac.eu.org`) improves connectivity in restricted networks; keep it configurable via `PROXYIP` env var.
- **UUID must be valid v4 format** — validate with regex before deployment to avoid worker crashes.
- **WebSocket upgrade header check** — worker only proxies on `Upgrade: websocket` requests; HTTP GET to `/$UUID` returns config.
- **Error 1101 (Worker threw exception)** — the canonical Free-VLESS script from GitHub has bugs in UUID validation and `cloudflare:sockets` import that cause runtime crashes. Use a clean, tested implementation instead.
- **`cloudflare:sockets` connect() does not accept a second options object** — passing `{ allowHalfOpen: false }` (or any options object) as the second argument crashes the worker with error 1101. Use `connect({ hostname, port })` only.
- **Error 1042 (No Worker serving workers.dev URL)** — the Worker's workers.dev route is disabled by default. Must be enabled manually in Dashboard.
- **Invalid API Token** — verify token with `/user/tokens/verify` before any deployment; User API Tokens with Workers:Edit may still be rejected if scoped incorrectly.
- **Error 10013 (Unknown error during deploy)** — when the API token is invalid or the account has issues, all deployments fail with this generic error. Token must have `Account > Workers Scripts > Edit` permission.
- **Compatibility date** — set to a recent date (e.g., `2026-10-05`) to ensure modern runtime features like `cloudflare:sockets` work.
- **Account-level workers.dev subdomain** — the subdomain (`<account>.workers.dev`) must be created once in Dashboard before any Worker can use it.

## Iran-Specific Configuration (Hamrah / Irancell / Rightel)
For Iranian mobile networks, the following parameters are critical to bypass DPI:
- **SNI = Host = Worker domain** (e.g., `vless-clean.aawfzdxeert.workers.dev`) — must match exactly
- **Path = `/ws`** — matches the worker's WebSocket endpoint
- **TLS 1.3 + WebSocket on port 443** — standard HTTPS, least likely to be blocked
- **Fingerprint = `chrome`** — prevents TLS fingerprint detection
- **No custom domain required** — `workers.dev` subdomain works directly and is free

Config template for Iran:
```
vless://$UUID@$HOST:443?encryption=none&security=tls&sni=$HOST&fp=chrome&type=ws&host=$HOST&path=%2Fws#IR-VLESS
```
Clash Meta YAML:
```yaml
- type: vless
  name: IR-VLESS
  server: $HOST
  port: 443
  uuid: $UUID
  network: ws
  tls: true
  udp: false
  sni: $HOST
  client-fingerprint: chrome
  ws-opts:
    path: "/ws"
    headers:
      host: $HOST
```

## User Preferences (this user)
- Bilingual English/Farsi communication
- Free tier only, no VPS purchase
- Uses Cloudflare account with R2 (has API token, Account ID)
- Prefers direct technical resolution without filler
- Windows 10/11 environment
- Active autonomous income fleet — values zero-token, persistent operation

## References
- `references/clean-worker.js` — Clean, tested VLESS worker implementation (use this instead of GitHub version)
- `templates/wrangler.jsonc` — Wrangler configuration template for local development with `wrangler deploy`