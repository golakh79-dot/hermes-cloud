---
name: elysium-token-launch
description: "Launch tokens on Elysium via Montra/o1 for HYPE fees."
version: 1.0.0
author: alireza
license: MIT
metadata:
  hermes:
    tags: [elysium, hyperliquid, hyperEVM, montra, o1exchange, token-launch, launchpad, memecoin, creator-fee]
    homepage: "https://montramarkets.xyz"
---

# Elysium Token Launch - Always-On Rules

## When to Use This Skill
**Use when**: You need to research, compare, or deploy tokens on Elysium L2 (HyperEVM) using launchpads like Montra Markets or o1 Exchange. This covers the full workflow from platform comparison to live deployment with Creator Fee capture.

## Prerequisites
1. EVM wallet (MetaMask) with HYPE on Elysium Mainnet (Chain ID: 99901)
2. Minimum 0.1 HYPE for gas + launch fees
3. Telegram bot token (optional, for Pro dual-thread bots)
4. Image/logo asset ready (PNG/WebP, square, <2MB)

## Platform Comparison Matrix (Elysium Launchpads)

| Feature | Montra Markets | o1 Exchange | Bankr |
|---|---|---|---|
| **Launch URL** | `https://montramarkets.xyz/launch` | `https://o1.exchange/create` | N/A |
| **Chain ID** | 99901 (Elysium) | 99901 (Elysium) | 99901 (Elysium) |
| **Launch Fee** | Variable (pool init) | **Fixed 0.025 HYPE** | N/A |
| **Dev Buy (Atomic)** | ❌ Manual after launch | ✅ **Atomic Dev Buy (HYPE/USDC)** | ❌ |
| **Creator Fee** | Set to "You" (1% swap fees in HYPE) | 50% creator / 30% platform / 20% referrer | N/A |
| **Anti-snipe** | None | 99% → 1% over 20s | N/A |
| **Launch Status** | 🟢 Active | 🟢 Active | 🔴 **Disabled** ("Launch v3 pending") |
| **Best For** | Simple meme launches, zero config | Pro launches, sniper protection, Dev Buy |

## Critical Pitfalls & Rules

### ✅ Pitfall: Bankr Does NOT Support Elysium Launches
**Rule**: Never attempt to launch tokens on Elysium via Bankr (`bankr.bot`).
**Why**: Official Bankr OpenAPI spec (`LaunchChain` enum) explicitly states: `"Launches on elysium are refused until Bankr Launch v3 goes live there."` Only Base, Robinhood, Arbitrum, Arc are active.
**Fix**: Use Montra Markets or o1 Exchange only.

### ✅ Pitfall: Montra Requires Manual Dev Buy for Sniper Detection
**Rule**: On Montra, you MUST perform a manual buy immediately after launch (same block if possible) or snipers/agents will ignore the token.
**Why**: Montra has no Atomic Dev Buy. Snipers scan for tokens with initial liquidity + first buy in same tx. Without Dev Buy, token appears abandoned.
**Fix**: After clicking Launch on Montra, immediately execute a buy (even 0.01 HYPE) via the Montra UI or direct Uniswap v4 router.

### ✅ Pitfall: Creator Fee Must Be Set to "You" on Montra
**Rule**: In Montra launch form, **Fees → You** (not "Community" or "Burn").
**Why**: Only "You" routes 1% swap fees to your wallet in HYPE gas tokens. Other options send fees elsewhere.
**Fix**: Verify the fee recipient address matches your wallet before confirming launch.

### ✅ Pitfall: o1 Exchange Atomic Dev Buy Requires Paired Asset
**Rule**: On o1 Exchange, Dev Buy currency must match the paired asset:
- HYPE-paired launch → Dev Buy in HYPE
- USDC-paired launch → Dev Buy in USDC (Elysium has NO HYPE/USDC Uniswap v3 pool)
**Why**: The `ElysiumSwapXLaunchBuyAdapter` only routes Dev Buy into the selected quote currency pool.
**Fix**: Ensure you have the paired asset balance before launching with Dev Buy.

### ✅ Pitfall: Elysium Bridge Withdrawal = ~5.5 Days
**Rule**: HYPE bridged from Elysium → HyperEVM takes ~5.5 days (Optimistic Checkpoint).
**Why**: Withdrawals are subject to Elysium's challenge period. Plan liquidity needs accordingly.
**Fix**: Keep operating capital on Elysium; only bridge profits you can lock for 6+ days.

## Launch Workflow: o1 Exchange (Recommended for Pro)

1. **Prepare**: HYPE on Elysium in MetaMask. Logo image ready. Token name/symbol/description.
2. **Navigate**: `https://o1.exchange/create`
3. **Connect**: MetaMask → Switch to Elysium Mainnet (Chain ID 99901).
4. **Select Product**: Standard (fee-sharing) or Tax (custom taxes/dividends).
5. **Paired Asset**: HYPE (recommended for native gas fee capture).
6. **Atomic Dev Buy**: Enable → Enter amount (e.g., 0.1–0.5 HYPE). This executes in same tx as launch.
7. **Fee Recipient**: Your wallet (default).
8. **Launch**: Sign transaction (0.025 HYPE fee + Dev Buy amount + gas).
9. **Verify**: Check `https://o1.exchange/token/<address>` for pool, trading, fee claims.
10. **Claim Fees**: Profile page → Claim (pays in paired currency: HYPE).

## Launch Workflow: Montra Markets (Simple / Zero Config)

1. **Prepare**: HYPE on Elysium. Logo ready.
2. **Navigate**: `https://montramarkets.xyz/launch`
3. **Connect**: MetaMask → Elysium.
4. **Fill Form**: Name, Symbol, Description, Image.
5. **Fees Section**: **CRITICAL** → Select **"You"** for Creator Fee.
6. **Launch**: Confirm transaction.
7. **IMMEDIATE DEV BUY**: In same browser tab, execute a buy (min 0.01 HYPE) within seconds.
8. **Monitor**: Check dashboard for volume, fees claimable in HYPE.

## Token Concept Generation for Elysium

**Themes that attract volume on Elysium**:
- **Protocol/Native tools**: ElyScan, ELY LOCK, HyperPurr (scanner, locking, mascot)
- **AI + Crypto hybrid**: $ELYAI, $LIQAI, $PURRAI (AI agent narratives)
- **Meme + Protocol**: Liquid Pepe, Liquid Island (liquidity + meme)
- **Ecosystem inside jokes**: eaccat, Eacc Lynx (e/acc culture)

**Logo Prompt Template**:
> `Futuristic neon-glowing [MASCOT/OBJECT] analyzing a hologram blockchain sphere, electric cyan and purple theme, 3D vector logo design, dark sleek background, octane render 8k`

**Launch Cost**: ~0.025 HYPE (o1) or variable (Montra) ≈ **$0.30–0.50** per launch.

## Post-Launch Monitoring

- **Volume Target**: First 5 min critical. If no buys in 5 min, token likely dead.
- **Fee Accrual**: Check Creator Fee dashboard (Montra) or Profile → Claims (o1).
- **Liquidity**: Pool is permanent (full supply in single range). No rug possible by creator.
- **Bridge Planning**: If moving fees to HyperEVM, initiate withdrawal early (5.5 day delay).

## Related Skills
- `autonomous-agent-maintenance` — For deploying Pro dual-thread bots to monitor launches
- `polyester-testnet-trading-update` — For trading launched tokens on Polyester
- `wurk-autonomous-agent` — For earning USDC to fund HYPE purchases
- `grounded-citations` — For citing platform docs in launch reports

## References
- `references/montra-launchpad.md` — Montra Markets launch form fields, fee settings, dashboard
- `references/o1exchange-launchpad.md` — o1 Exchange Standard/Tax products, Dev Buy, factory addresses
- `references/elysium-network.md` — Chain ID, RPC, gas token HYPE, bridge timing, explorer
- `references/token-concepts.md` — Proven token themes, logo prompts, naming patterns for Elysium