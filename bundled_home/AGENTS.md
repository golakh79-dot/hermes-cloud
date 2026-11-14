# 👤 USER PROFILE & SYSTEM ARCHITECTURE (ALIREZA)

## 1. Identity & Communication Style
- **Name:** علیرضا (Alireza)
- **Language:** Always respond in fluent, natural Persian (فارسی روان و دقیق). Never mix Korean/Vietnamese/Chinese characters in Persian text.
- **User Expectation:** Alireza speaks in concise, casual Persian ("عاميانه"). You must immediately infer his technical intent without asking unnecessary questions, execute the task cleanly, and report real results.
- **Zero Hallucination Rule:** Never guess PIDs, file contents, or command outputs. Always run PowerShell/Python verification commands first.

## 2. Hardware & Environment
- **OS:** Windows 10 (HP Mini-PC)
- **Home Directory:** `D:\HERMES\Hermes_Portable_Data\home`
- **Scripts Directory:** `D:\HERMES\Hermes_Portable_Data\home\scripts`
- **Backups Directory:** `D:\HERMES\Hermes_Portable_Data\home\backups`
- **AI Gateway (9Router):** Running locally on `http://127.0.0.1:20128/v1` with Combo `HERMES` (Gemini 3.6 Flash + NVIDIA Nemotron 550B + Groq GPT-OSS 120B).

## 3. Active Bots & Scripts Inventory
1. **Main Agent Bot (`New hermes`):** Uses `TELEGRAM_BOT_TOKEN` in `.env`.
2. **Twitter Live Command Center (`@Hermixxbot` / `Hermes`):**
   - Script: `D:\HERMES\Hermes_Portable_Data\home\scripts\twitter_telegram_bot_panel.py`
   - Log: `D:\HERMES\Hermes_Portable_Data\home\twitter_hub.log`
   - State: `D:\HERMES\Hermes_Portable_Data\home\twitter_targets.json`
   - Single-Instance Lock Port: `59421`
   - Uses `TWITTER_BOT_TOKEN` in `.env` (Never mix with `TELEGRAM_BOT_TOKEN`!).
3. **Other Automation Scripts in `scripts/`:**
   - `wurk_agent.py` (Micro-task automation on wurk.fun)
   - `polyester_trader.py` & `polyester_trader.log`

# 🧠 LESSONS LEARNED & ENGINEERING RULES (PERSISTENT MEMORY)

## [2026-11-08] Core Operational Rules
1. **SAFE FILE EDITING (CRITICAL):**
   - NEVER overwrite a script >100 lines directly without backing it up first to `D:\HERMES\Hermes_Portable_Data\home\backups\<filename>_<timestamp>.bak`.
   - When modifying Python files, ALWAYS write via a clean Python helper script using `encoding="utf-8"` (do not use fragile bash/cmd echo escaping).
   - ALWAYS run `python -m py_compile <file.py>` after editing. If syntax fails, immediately restore from `.bak` or fix before running.

2. **9ROUTER & LLM PARSING:**
   - 9Router on port 20128 can return SSE chunks or multiple JSON objects. When writing scripts that call `http://127.0.0.1:20128/v1/chat/completions`, use `json.JSONDecoder().raw_decode` or tagged line formats (`FA_TRANS:`, `REPLY1_EN:`) instead of greedy regex `\{.*\}` to avoid `Extra data` errors.
   - Do not use OpenRouter free models (50/day limit causes HTTP 429). Stick to `HERMES` combo (Gemini + Groq + NVIDIA NIM).

3. **TELEGRAM BOT CONFLICT (409) PREVENTION:**
   - `New hermes` uses `TELEGRAM_BOT_TOKEN`.
   - `@Hermixxbot` (Twitter bot) uses `TWITTER_BOT_TOKEN` and locks TCP port `59421`.
   - Before restarting `twitter_telegram_bot_panel.py`, always kill old instances matching its command line so port 59421 is freed cleanly.

---
name: core-evolution
description: Persistent Long-Term Memory, User Context, and Safe Coding Protocol for Hermes. Always read this before coding or system administration.
---

# Hermes Self-Evolution & Safe Coding Skill

1. **Read Persistent Memory First:**
   Whenever Alireza gives you a casual or high-level instruction, first check his environment and rules by running:
   `python -X utf8 "D:\HERMES\Hermes_Portable_Data\home\brain\memory_manager.py" read`

2. **Safe File Modification Protocol (Zero-Corruption):**
   - Before modifying ANY existing script in `scripts/`, ALWAYS take a snapshot backup first:
     `python -X utf8 "D:\HERMES\Hermes_Portable_Data\home\brain\memory_manager.py" backup "D:\HERMES\Hermes_Portable_Data\home\scripts\<filename>"`
   - After writing or updating any `.py` file, ALWAYS verify syntax before running:
     `python -m py_compile "D:\HERMES\Hermes_Portable_Data\home\scripts\<filename>"`

3. **Record New Experiences Automatically:**
   Whenever you solve a bug, discover a new preference from Alireza, or build a new workflow, permanently save the lesson by running:
   `python -X utf8 "D:\HERMES\Hermes_Portable_Data\home\brain\memory_manager.py" learn "<concise summary of what was learned>"`
