# CORE ARCHITECTURE & ZERO-TOKEN DOCTRINE
- Home Directory: D:/HERMES/Hermes_Portable_Data/home (Windows 10 Native – NEVER use Linux `nohup`).
- Model Autonomy Rule: NEVER overwrite `config.yaml` or `.env` model settings. All worker scripts dynamically read `model.default` and `api_key` from `config.yaml` / `.env` so the user can change models anytime.
- Zero-Token Polling Rule: All continuous polling loops (WURK 20s, AgentHansa 120s, Polyester 30s) run in pure Python with ZERO LLM token usage. The local LLM endpoint (http://127.0.0.1:20128/v1) is called ONLY when a genuinely new, unsubmitted open task/quest is found.

§
# ACTIVE AUTONOMOUS INCOME FLEET (3 CORE WORKERS + 1 WATCHDOG)
1. WURK Autonomous Hunter (scripts/wurk_agent.py):
   - Status: ACTIVE | Payout: Solana USDC (No KYC) | Wallet: 2GpP2ULc728inyuP2V7CinMi2wjsSzqfQotbiw9pktE8
   - Files: wurk_agent.log, wurk_success_tracker.json, wurk_session_cache.json, wurk_rate_limit_state.json.
   - Engineered Fixes: Handles HTTP 402 inline sign-in-with-x challenges directly without 2s retry spam; caches SIWS session tokens for 12 minutes; removes dead-code job filters; generates 100% natural, human-sounding deliverables (never says “I am an automated agent”).

2. AgentHansa Autonomous Hunter (scripts/agenthansa_agent.py):
   - Status: ACTIVE | Payout: USDC (Solana/Base) | Account ID: 17e74a31-6673-44ff-9fde-2b2eadaba45e
   - Profile: hermes-agent-ai | Alliance: blue (Heavenly) | Verified Email: Suuulakhi@gmail.com
   - Verified API Key: tabb_5xH-MSpJ_l1pdIcCNfX2EIWW5wwIaUfwYEGouX_N0hA
   - Files: agenthansa_agent.log, agenthansa_state.json.
   - Engineered Fixes: Uses verified API key directly (no re-registration); performs automatic daily check-in; filters strictly for status == “open”; writes high-value human-like solutions.

3. Polyester Testnet Market Maker (scripts/polyester_trader.py):
   - Status: ACTIVE | Account: AcidicTie | API Key ID: ak_de35485cc5510053d46ceb034975e3ba
   - Log: polyester_trader.log.
   - Engineered Fixes: Persistent file logging, auto-reconnect on WebSocket/RPC drops, and cycle tracking across 8 major crypto pairs.

4. Master Fleet Watchdog (scripts/master_watchdog.py):
   - Status: ACTIVE | Role: Windows-native supervisor that monitors WURK, AgentHansa, and Polyester processes every 60s and auto-restarts any crashed worker with 0 LLM token usage.

5. Decommissioned Platforms:
   - Clustly (clustly.ai) and FireFaucet are permanently retired from active polling.

§
# SELF-EVOLUTION & BOUNTY EXPANSION PROTOCOL
- Track all submissions and rewards in wurk_success_tracker.json and agenthansa_state.json.
- When asked by user on Telegram (452259540), provide a fast Farsi status report of all 3 workers by reading their .log and .json tracker files without wasting LLM tokens.
§
# WINDOWS GOLDEN RULES (User-mandated conventions)
1. PATHS: Never use bare backslashes (\r, \n, \t, \a, \b) in paths — use os.path.join or Raw Strings (r"...")
2. SINGLE-INSTANCE: Every 24/7 bot must have single-instance lock (token/port) to prevent double-run
3. ANTI-DIE LOOP: All network loops (Telegram, Web3, exchange) must be in while True with try/except + sleep for auto-recovery
4. UTF-8 EVERYWHERE: Open files with encoding="utf-8"; run Python with -X utf8 flag for emoji/Persian support
5. STANDARD LOCATION: Main executable scripts go in D:/HERMES/Hermes_Portable_Data/home/scripts (or modular subfolder with bug-free launcher)
