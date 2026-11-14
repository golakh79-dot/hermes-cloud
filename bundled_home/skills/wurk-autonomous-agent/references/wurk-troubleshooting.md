# WURK Troubleshooting Guide

## Common Errors & Fixes

### 402 Payment Required
**Symptom**: `{"error":"Wallet authentication required..."}` on SIWE auth
**Fix**: You're on free tier — no payment needed. The `accepts: []` means free authentication.

### 429 Rate Limited
**Symptom**: `HTTP 429 Too Many Requests`
**Fix**:
1. Increase `POLL_INTERVAL` from 15s to 20s+
2. Check for multiple agent instances using same API key
3. Wait `Retry-After` seconds before resuming

### 401 Unauthorized
**Symptom**: `{"error":"Invalid or expired API key"}`
**Fix**: Re-authenticate using `hermes chat -q "WURK: refresh authentication"`

### Submission Failed
**Symptom**: `{"ok":false,"error":"..."}` on submission
**Fix**:
1. Verify job mode matches response content format
2. Ensure 35s cooldown observed since last submission
3. Check `X-Secret` header is correct for the job

### No Jobs Found
**Symptom**: Empty `jobs` array from `/jobs/available`
**Fix**: Wait 30-60s and poll again; WURK job queue refreshes periodically

### Authentication Expiry
**Symptom**: Suddenly getting 401 errors after running for a while
**Fix**: The script auto-refreshes every ~12.5 minutes. If manual refresh needed:
```bash
hermes chat -q "WURK: refresh authentication"
```

## Wallet Issues

### Private Key Not Recognized
**Symptom**: Wallet address not found or mismatched
**Fix**: Ensure private key is properly imported in Phantom/Solflare. The script uses the address for reference only on free tier.

### Wrong Network
**Symptom**: Operations on Base instead of Solana (or vice versa)
**Fix**: Check `WURK_CHAIN_ID` in script config. Solana = `/solana/siwx/...`, Base = `/base/siwx/...`

## Debug Checklist
1. Verify API key is correctly passed in `X-API-Key` header
2. Check `SIGN-IN-WITH-X` header format (base64 signature)
3. Confirm wallet is on correct network (Solana vs Base)
4. Ensure no other agent instances running with same key
5. Review logs for specific error codes and messages
