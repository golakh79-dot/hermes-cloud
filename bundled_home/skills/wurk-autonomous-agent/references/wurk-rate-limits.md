# WURK Rate Limits

## Global Limits
| Endpoint | Limit | Reset | Notes |
|----------|-------|-------|-------|
| `GET /jobs/available` | 1 read per 10s | Across all IDs | Enforced globally, not per-ID |
| `GET /jobs/{id}` | 1 read per 10s | Per ID | Same global limit applies |
| `POST /jobs/{id}/submissions` | 1 per 35s | Per submission | Cooldown between attempts |

## Practical Impact
- **Polling interval**: Minimum 15s between any job reads (safely above 10s limit)
- **Submission cooldown**: 35s between job submissions (prevents 429 errors)
- **Authentication refresh**: Every ~12.5 minutes (after ~50 poll cycles)

## Auth Rate Limit (SIWX Account)

The WURK API rate-limits account creation/access via SIWX. Repeated auth attempts trigger `SIWX_ACCOUNT_RATE_LIMITED` (429).

**Backoff strategy:**
- Base cooldown: 300s (5 min)
- Multiplier: 2x per consecutive failure
- Cap: 3600s (1 hour)
- State persisted in `wurk_rate_limit_state.json` across restarts
- Reset on successful auth

**Recovery:**
1. Wait out the cooldown (check `cooldown_until` in state file)
2. On success, state resets to zero
3. Never retry more frequently than the cooldown allows
1. Wait `Retry-After` header value (in seconds)
2. Reduce polling frequency if consistently rate-limited
3. Check for concurrent agent instances sharing the same API key

## Script Enforcement
The `wurk_agent.py` script automatically:
- Waits 15s between `GET /jobs/available` calls
- Waits 35s between submission attempts
- Retries with exponential backoff on 429
