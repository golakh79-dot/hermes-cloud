import os, re, sys, time, json, html, base64, socket, threading
import urllib.parse, urllib.request, urllib.error
from datetime import datetime
import base58
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

HOME_DIR = os.getenv("HERMES_HOME", "/tmp/hermes_home")
ENV_FILE = os.path.join(HOME_DIR, ".env")
TRACKER_FILE = os.path.join(HOME_DIR, "wurk_success_tracker.json")
STATE_FILE = os.path.join(HOME_DIR, "wurk_pro_state.json")
SESSION_CACHE_FILE = os.path.join(HOME_DIR, "wurk_session_cache.json")
LOG_FILE = os.path.join(HOME_DIR, "wurk_agent.log")

ADMIN_CHAT_ID = 452259540
WALLET_ADDRESS = "2GpP2ULc728inyuP2V7CinMi2wjsSzqfQotbiw9pktE8"
ROUTER_CHAT_URL = "http://127.0.0.1:20128/v1/chat/completions"
LOCK_PORT = 59422

SIWE_AUTH_URL = "https://api.wurk.fun/solana/siwx/account-create"
JOBS_LIST_URL = "https://api.wurk.fun/jobs/available?limit=25"
JOB_DETAIL_URL = "https://api.wurk.fun/jobs/{}"
SUBMIT_URL = "https://api.wurk.fun/jobs/{}/submissions"

_INSTANCE_SOCKET = None
_LOCK = threading.Lock()

def acquire_lock():
    global _INSTANCE_SOCKET
    _INSTANCE_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _INSTANCE_SOCKET.bind(("127.0.0.1", LOCK_PORT))
        _INSTANCE_SOCKET.listen(1)
        return True
    except socket.error:
        return False

def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [WURK-BOT] {msg}"
    print(line, flush=True)
    try:
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(line + "\n")
    except Exception:
        pass

def load_env_var(keys):
    if os.path.exists(ENV_FILE):
        with open(ENV_FILE, "r", encoding="utf-8", errors="ignore") as f:
            for line in f:
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                if k.strip() in keys:
                    val = v.strip().strip('"').strip("'")
                    if val:
                        return val
    return ""

def get_private_key():
    k = load_env_var(["WURK_PRIVATE_KEY_B58", "SOLANA_PRIVATE_KEY"])
    if not k:
        raise RuntimeError("WURK_PRIVATE_KEY_B58 missing in .env!")
    return k

def get_bot_token():
    return load_env_var(["WURK_BOT_TOKEN"]) or "8786109587:AAHZRf8PLVKOapGokRtDZwNoBQ7MxdMR230"

def get_router_key():
    return load_env_var(["RAMP_ROUTER_API_KEY", "OPENAI_API_KEY", "ROUTER_API_KEY"]) or "9router-local"

def load_json(path, default):
    if os.path.exists(path):
        try:
            with open(path, "r", encoding="utf-8", errors="ignore") as f:
                return json.load(f)
        except Exception:
            pass
    return default

def save_json(path, data):
    with _LOCK:
        tmp = path + ".tmp"
        try:
            with open(tmp, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=2, ensure_ascii=False)
            os.replace(tmp, path)
        except Exception as e:
            log(f"Save JSON warning ({path}): {e}")

def get_state():
    default = {
        "mode": "SMART",  # SMART (auto low, ask high), MANUAL (ask all), AUTO (auto all >=85 score)
        "high_value_threshold_sol": 0.03,
        "high_value_threshold_usd": 3.0,
        "min_quality_score": 85,
        "seen_jobs": [],
        "pending_approvals": {},
        "submitted_jobs": {}
    }
    st = load_json(STATE_FILE, default)
    for k, v in default.items():
        st.setdefault(k, v)
    return st

def tg_call(method, payload):
    token = get_bot_token()
    url = f"https://api.telegram.org/bot{token}/{method}"
    try:
        req = urllib.request.Request(url, data=json.dumps(payload).encode("utf-8"), headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read().decode("utf-8"))
    except Exception as e:
        log(f"TG call {method} notice: {e}")
        return {"ok": False}

def tg_notify(text, reply_markup=None):
    payload = {
        "chat_id": ADMIN_CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
        "disable_web_page_preview": True
    }
    if reply_markup:
        payload["reply_markup"] = reply_markup
    return tg_call("sendMessage", payload)

def register_commands():
    cmds = [
        {"command": "wurk", "description": "🛸 داشبورد زنده و وضعیت Wurk.fun"},
        {"command": "wurk_scan", "description": "⚡ اسکن فوری و بررسی تسک های جدید"},
        {"command": "wurk_pending", "description": "⏳ لیست پروژه های منتظر تایید شما"},
        {"command": "wurk_mode", "description": "⚙️ تغییر حالت (SMART / MANUAL / AUTO)"}
    ]
    tg_call("setMyCommands", {"commands": cmds})

def http_request(url, headers=None, data=None, method="GET", timeout=30, max_retries=3, allow_402=False):
    headers = headers or {}
    headers.setdefault("User-Agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36")
    for attempt in range(max_retries):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                raw = r.read().decode("utf-8")
                return json.loads(raw) if raw else {}
        except urllib.error.HTTPError as e:
            raw = e.read().decode("utf-8", errors="ignore") if e.fp else "{}"
            if allow_402 and e.code == 402:
                try:
                    return json.loads(raw)
                except Exception:
                    return {"raw": raw}
            if e.code in (429, 502, 503, 504) and attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            raise urllib.error.HTTPError(url, e.code, raw, e.headers, e.fp)
        except Exception:
            if attempt < max_retries - 1:
                time.sleep(2 ** (attempt + 1))
                continue
            raise
    return {}

def load_siws_session():
    cache = load_json(SESSION_CACHE_FILE, {})
    if cache.get("apikey") and time.time() < cache.get("expires", 0):
        return cache["apikey"]
    return ""

def save_siws_session(apikey, ttl=720):
    save_json(SESSION_CACHE_FILE, {"apikey": apikey, "expires": time.time() + ttl})

def sign_siws(challenge_obj):
    seed = base58.b58decode(get_private_key())[:32]
    priv = Ed25519PrivateKey.from_private_bytes(seed)
    ext = (challenge_obj or {}).get("extensions", {}).get("sign-in-with-x", {})
    info = ext.get("info", {})
    sup = (ext.get("supportedChains") or [{}])[0]
    cid_full = sup.get("chainId", "solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp")
    cid_msg = cid_full.split(":", 1)[-1]
    domain = info.get("domain", "api.wurk.fun")
    uri = info.get("uri", SIWE_AUTH_URL)
    ver = info.get("version", "1")
    stmt = info.get("statement", "Sign in to create or access your WURK account")
    nonce, iat = info.get("nonce", ""), info.get("issuedAt", "")
    exp, nbf = info.get("expirationTime"), info.get("notBefore")
    res_list = info.get("resources", [])
    lines = [
        f"{domain} wants you to sign in with your Solana account:",
        WALLET_ADDRESS, "", stmt, "",
        f"URI: {uri}", f"Version: {ver}", f"Chain ID: {cid_msg}",
        f"Nonce: {nonce}", f"Issued At: {iat}"
    ]
    if nbf: lines.append(f"Not Before: {nbf}")
    if exp: lines.append(f"Expiration Time: {exp}")
    if res_list:
        lines.append("Resources:")
        for r in res_list: lines.append(f"- {r}")
    sig_b58 = base58.b58encode(priv.sign("\n".join(lines).encode("utf-8"))).decode()
    payload = {
        "domain": domain, "address": WALLET_ADDRESS, "statement": stmt,
        "uri": uri, "version": ver, "chainId": cid_full, "type": "ed25519",
        "nonce": nonce, "issuedAt": iat, "signature": sig_b58, "signatureScheme": "siws"
    }
    if nbf: payload["notBefore"] = nbf
    if exp: payload["expirationTime"] = exp
    if res_list: payload["resources"] = res_list
    return base64.b64encode(json.dumps(payload).encode()).decode()

def authenticate_wurk():
    cached = load_siws_session()
    if cached:
        return cached
    log("Authenticating with WURK via Solana SIWS...")
    ch = http_request(SIWE_AUTH_URL, data=b"{}", headers={"Content-Type": "application/json"}, method="POST", allow_402=True)
    hdr = sign_siws(ch)
    res = http_request(SIWE_AUTH_URL, data=b"{}", headers={"Content-Type": "application/json", "SIGN-IN-WITH-X": hdr}, method="POST")
    apikey = res.get("apikey", "")
    if not apikey:
        raise RuntimeError(f"SIWS Auth failed: {res}")
    save_siws_session(apikey)
    log(f"✅ SIWS Authenticated! Account: {res.get('accountId', 'OK')}")
    return apikey

def decode_9router_body(raw_text):
    if not raw_text:
        return ""
    decoder = json.JSONDecoder()
    idx = 0
    out = ""
    while idx < len(raw_text):
        brace = raw_text.find("{", idx)
        if brace == -1:
            break
        try:
            obj, end_idx = decoder.raw_decode(raw_text, brace)
            idx = end_idx
            if isinstance(obj, dict) and "choices" in obj and obj["choices"]:
                msg = obj["choices"][0].get("message") or obj["choices"][0].get("delta") or {}
                c = msg.get("content") or msg.get("reasoning_content") or ""
                if c:
                    out += c
        except Exception:
            idx = brace + 1
    res = out.strip() if out else raw_text.strip()
    return re.sub(r"<think>.*?</think>", "", res, flags=re.DOTALL | re.IGNORECASE).strip()

def ask_9router(prompt, system_prompt, temp=0.4):
    models = ["HERMES", "gemini/gemini-3.6-flash", "groq/openai/gpt-oss-120b", "nvidia/nvidia/nemotron-3-ultra-550b-a55b"]
    for m in models:
        payload = {
            "model": m,
            "messages": [{"role": "system", "content": system_prompt}, {"role": "user", "content": prompt}],
            "temperature": temp,
            "stream": False
        }
        req = urllib.request.Request(
            ROUTER_CHAT_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {get_router_key()}"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                body = r.read().decode("utf-8", errors="ignore")
            ans = decode_9router_body(body)
            if ans:
                return ans
        except Exception as e:
            log(f"9Router model {m} notice: {e}")
            time.sleep(1)
    raise RuntimeError("All 9Router models failed")

def fetch_live_urls_context(text):
    urls = re.findall(r"https?://[^\s)\]>\"']+", text or "")
    contexts = []
    for u in urls[:2]:
        try:
            j_url = f"https://r.jina.ai/{u}"
            req = urllib.request.Request(j_url, headers={"User-Agent": "Mozilla/5.0", "X-Return-Format": "markdown"})
            with urllib.request.urlopen(req, timeout=15) as r:
                md = r.read().decode("utf-8", errors="ignore")
            contexts.append(f"--- LIVE WEB CONTENT FROM {u} ---\n{md[:1800]}")
        except Exception:
            pass
    return "\n\n".join(contexts)

def should_skip_job(title, desc):
    full = f"{title}\n{desc}".lower()
    hard_blocks = [
        "kyc", "verify identity", "selfie", "id card", "passport", "driver license",
        "video recording", "record a video", "voice recording", "private key", "seed phrase"
    ]
    for b in hard_blocks:
        if b in full:
            return True, f"Blocked keyword: {b}"
    return False, ""

def classify_skill(title, desc):
    full = f"{title}\n{desc}".lower()
    if any(w in full for w in ["code", "script", "python", "javascript", "solidity", "rust", "function", "regex", "json", "smart contract", "bug", "api"]):
        return "💻 CODING & TECH"
    if any(w in full for w in ["research", "analyze", "compare", "audit", "find", "list", "report", "tokenomics", "on-chain"]):
        return "🔍 DEEP RESEARCH"
    if any(w in full for w in ["tweet", "thread", "post", "article", "blog", "copy", "write", "summary", "translate"]):
        return "✍️ WEB3 CONTENT"
    return "🧠 GENERAL AGENT"

def execute_skill_and_audit(job):
    title = job.get("title", "Untitled")
    desc = job.get("description", "")
    reqs = job.get("requirements") or job.get("deliverable") or ""
    skill = classify_skill(title, desc)
    web_ctx = fetch_live_urls_context(f"{desc}\n{reqs}")

    sys_exec = (
        f"You are an elite autonomous Web3 Agent executing a paid bounty on Wurk.fun (Skill Mode: {skill}).\n"
        "CRITICAL RULES:\n"
        "1. Follow EVERY single instruction, format constraint, word count, or structure requested by the client.\n"
        "2. Do NOT add meta-commentary like 'Here is your deliverable' or 'Sure, I can help'. Output ONLY the exact final work ready for submission.\n"
        "3. If the task asks for code/JSON, provide clean, complete, production-ready code/JSON. If it asks for a social post/article, write like a real human Web3 native."
    )
    user_prompt = f"JOB TITLE: {title}\n\nDESCRIPTION:\n{desc}\n\nREQUIREMENTS:\n{reqs}"
    if web_ctx:
        user_prompt += f"\n\nLIVE WEB CONTEXT FETCHED FROM URLS:\n{web_ctx}"

    draft_deliverable = ask_9router(user_prompt, sys_exec, temp=0.45)

    sys_critic = (
        "You are a Strict Bounty Quality Auditor. Review the job description and our drafted deliverable.\n"
        "Output ONLY these 4 tagged lines:\n"
        "FA_DESC: <1-2 line fluent Persian explanation of what the job wants>\n"
        "SCORE: <integer 0 to 100 indicating how accurately the deliverable satisfies all requirements>\n"
        "REASON: <1-line Persian reason for the score>\n"
        "IMPROVED: <KEEP if score>=90, otherwise provide the fixed/improved final deliverable in one line or block>"
    )
    audit_raw = ask_9router(f"JOB:\n{title} - {desc[:800]}\n\nDRAFT DELIVERABLE:\n{draft_deliverable[:2000]}", sys_critic, temp=0.2)

    fa_desc = "انجام تسک تخصصی وب۳"
    score = 90
    reason = "مطابقت کامل با خواسته کارفرما"
    m_fa = re.search(r"FA_DESC\s*:\s*(.+)", audit_raw)
    if m_fa: fa_desc = m_fa.group(1).strip()
    m_sc = re.search(r"SCORE\s*:\s*(\d+)", audit_raw)
    if m_sc: score = int(m_sc.group(1))
    m_rs = re.search(r"REASON\s*:\s*(.+)", audit_raw)
    if m_rs: reason = m_rs.group(1).strip()

    final_work = re.sub(r"^(?:here is|sure|deliverable\s*:|output\s*:).*?\n", "", draft_deliverable.strip(), flags=re.IGNORECASE).strip()
    return {
        "skill": skill,
        "fa_desc": fa_desc,
        "score": score,
        "reason": reason,
        "deliverable": final_work
    }

def submit_job_to_wurk(apikey, jid, content):
    url = SUBMIT_URL.format(jid)
    headers = {"X-API-Key": apikey, "Content-Type": "application/json"}
    body = json.dumps({"content": content, "deliverable": content}).encode("utf-8")
    return http_request(url, headers=headers, data=body, method="POST")

def is_high_value(reward_val, asset_str, st):
    try:
        val = float(reward_val or 0)
    except Exception:
        val = 0.0
    asset = (asset_str or "SOL").upper()
    if "SOL" in asset and val >= float(st.get("high_value_threshold_sol", 0.03)):
        return True
    if any(u in asset for u in ["USD", "USDC", "USDT"]) and val >= float(st.get("high_value_threshold_usd", 3.0)):
        return True
    return False

def check_submitted_payouts(apikey):
    st = get_state()
    submitted = st.get("submitted_jobs", {})
    changed = False
    for jid, info in list(submitted.items()):
        if info.get("finalized"):
            continue
        try:
            detail = http_request(JOB_DETAIL_URL.format(jid), headers={"X-API-Key": apikey})
            status_str = str(detail.get("userSubmissionStatus") or detail.get("status") or "").lower()
            if any(w in status_str for w in ["approved", "paid", "completed", "accepted", "won"]):
                info["status"] = "APPROVED & PAID 💰"
                info["finalized"] = True
                changed = True
                tg_notify(
                    f"💰🎉 <b>تبریک! پروژه تایید و پرداخت شد!</b>\n"
                    f"━━━━━━━━━━━━━━━━━━\n"
                    f"📌 <b>عنوان:</b> {html.escape(info.get('title', jid))}\n"
                    f"💵 <b>پاداش دریافتی:</b> <b>{info.get('reward')} {info.get('asset')}</b>\n"
                    f"🏦 <b>کیف پول:</b> <code>{WALLET_ADDRESS[:8]}...{WALLET_ADDRESS[-6:]}</code>"
                )
            elif "reject" in status_str:
                info["status"] = "REJECTED ❌"
                info["finalized"] = True
                changed = True
        except Exception:
            pass
    if changed:
        save_json(STATE_FILE, st)

def process_single_job(apikey, job_summary, force_manual=False):
    st = get_state()
    jid = str(job_summary.get("id") or job_summary.get("_id") or "")
    if not jid or jid in st["seen_jobs"]:
        return False

    detail = http_request(JOB_DETAIL_URL.format(jid), headers={"X-API-Key": apikey})
    job = detail if isinstance(detail, dict) and detail.get("title") else job_summary
    title = job.get("title", "Untitled Job")
    desc = job.get("description", "")
    reward = job.get("reward") or job.get("amount") or job.get("bounty") or 0
    asset = job.get("asset") or job.get("currency") or "SOL"

    skip, skip_reason = should_skip_job(title, desc)
    if skip:
        st["seen_jobs"].append(jid)
        save_json(STATE_FILE, st)
        log(f"Skipped job {jid} ({skip_reason})")
        return False

    log(f"Evaluating job {jid}: {title} ({reward} {asset})...")
    res = execute_skill_and_audit(job)
    high_val = is_high_value(reward, asset, st)
    mode = st.get("mode", "SMART")

    need_manual_approval = (
        force_manual
        or mode == "MANUAL"
        or (mode == "SMART" and high_val)
        or res["score"] < int(st.get("min_quality_score", 85))
    )

    if need_manual_approval:
        st["seen_jobs"].append(jid)
        st["pending_approvals"][jid] = {
            "id": jid, "title": title, "reward": reward, "asset": asset,
            "skill": res["skill"], "fa_desc": res["fa_desc"],
            "score": res["score"], "deliverable": res["deliverable"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M")
        }
        save_json(STATE_FILE, st)
        badge = "💎 پروژه گران قیمت (نیاز به تایید شما)" if high_val else "🛡️ گیت کنترل کیفیت (منتظر تایید شما)"
        msg = (
            f"🛸 <b>WURK.FUN | {badge}</b>\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📌 <b>عنوان:</b> <b>{html.escape(title)}</b>\n"
            f"💰 <b>پاداش:</b> <b>{reward} {html.escape(str(asset))}</b> | 🛠 <b>اسکیل:</b> {res['skill']}\n"
            f"🎯 <b>امتیاز داور کیفیت:</b> <b>{res['score']}/100</b> ({html.escape(res['reason'])})\n\n"
            f"🇮🇷 <b>توضیح فارسی کار:</b>\n{html.escape(res['fa_desc'])}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📝 <b>خروجی آماده شده برای ارسال:</b>\n"
            f"<code>{html.escape(res['deliverable'][:1200])}</code>\n\n"
            f"👉 <i>برای تایید و ارسال این پروژه، روی دکمه زیر بزنید:</i>"
        )
        kb = {
            "inline_keyboard": [
                [{"text": f"🚀 تایید و سابمیت نهایی ({reward} {asset})", "callback_data": f"wurk_sub:{jid}"}],
                [{"text": "❌ رد کردن تسک", "callback_data": f"wurk_skip:{jid}"}]
            ]
        }
        tg_notify(msg, kb)
        return True

    log(f"Auto-submitting job {jid} (Score {res['score']}/100)...")
    time.sleep(10)
    sub_res = submit_job_to_wurk(apikey, jid, res["deliverable"])
    st["seen_jobs"].append(jid)
    st["submitted_jobs"][jid] = {
        "title": title, "reward": reward, "asset": asset,
        "skill": res["skill"], "score": res["score"],
        "status": "SUBMITTED ⏳ (در انتظار تایید کارفرما)",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "finalized": False
    }
    save_json(STATE_FILE, st)

    legacy = load_json(TRACKER_FILE, {"submissions": []})
    if isinstance(legacy, dict):
        legacy.setdefault("submissions", []).append({
            "job_id": jid, "title": title, "reward": reward, "asset": asset,
            "skill": res["skill"], "timestamp": datetime.now().isoformat(), "status": "submitted"
        })
        save_json(TRACKER_FILE, legacy)

    msg = (
        f"✅ <b>WURK.FUN | کار انجام و با موفقیت ارسال شد!</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📌 <b>پروژه:</b> <b>{html.escape(title)}</b>\n"
        f"💵 <b>پاداش:</b> <b>{reward} {html.escape(str(asset))}</b> | 🛠 <b>اسکیل:</b> {res['skill']}\n"
        f"🎯 <b>امتیاز دقت:</b> <b>{res['score']}/100</b>\n\n"
        f"🇮🇷 <b>خلاصه کار:</b> {html.escape(res['fa_desc'])}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📤 <b>خروجی ارسال شده:</b>\n<code>{html.escape(res['deliverable'][:900])}</code>"
    )
    tg_notify(msg)
    return True

def approve_pending_job(jid):
    st = get_state()
    item = st.get("pending_approvals", {}).get(jid)
    if not item:
        return f"⚠️ تسک {jid} در لیست انتظار پیدا نشد."
    apikey = authenticate_wurk()
    submit_job_to_wurk(apikey, jid, item["deliverable"])
    del st["pending_approvals"][jid]
    st["submitted_jobs"][jid] = {
        "title": item["title"], "reward": item["reward"], "asset": item["asset"],
        "skill": item["skill"], "score": item["score"],
        "status": "SUBMITTED ⏳ (تایید شده توسط شما)",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "finalized": False
    }
    save_json(STATE_FILE, st)
    return f"🚀 پروژه «{item['title']}» با پاداش {item['reward']} {item['asset']} با موفقیت در Wurk.fun سابمیت شد!"

def skip_pending_job(jid):
    st = get_state()
    if jid in st.get("pending_approvals", {}):
        del st["pending_approvals"][jid]
        save_json(STATE_FILE, st)
        return f"❌ تسک {jid} رد شد و از لیست انتظار پاک شد."
    return "تسک مورد نظر یافت نشد."

def print_status_report():
    st = get_state()
    sub = st.get("submitted_jobs", {})
    pend = st.get("pending_approvals", {})
    lines = [
        f"🛸 <b>داشبورد زنده Wurk.fun Pro v2.0</b>",
        f"⚙️ <b>حالت فعلی:</b> <code>{st.get('mode', 'SMART')}</code>",
        f"🏦 <b>کیف پول:</b> <code>{WALLET_ADDRESS[:6]}...{WALLET_ADDRESS[-4:]}</code>",
        f"📤 <b>کارهای ارسال شده:</b> {len(sub)} مورد",
        f"⏳ <b>پروژه های منتظر تایید شما:</b> {len(pend)} مورد\n"
    ]
    if pend:
        lines.append("⏳ <b>لیست پروژه های منتظر تایید:</b>")
        for jid, info in list(pend.items())[-3:]:
            lines.append(f"• <b>{html.escape(info['title'][:30])}</b> ({info['reward']} {info['asset']}) ➔ /wurk_submit_{jid}")
    return "\n".join(lines)

def run_scanner():
    try:
        apikey = authenticate_wurk()
        check_submitted_payouts(apikey)
        res = http_request(JOBS_LIST_URL, headers={"X-API-Key": apikey})
        jobs = res if isinstance(res, list) else (res.get("jobs") or res.get("data") or [])
        count = 0
        for j in jobs:
            try:
                if process_single_job(apikey, j):
                    count += 1
            except Exception as je:
                log(f"Job processing notice: {je}")
        return f"✅ اسکن انجام شد. {len(jobs)} تسک بررسی شد ({count} تسک جدید پردازش شد)."
    except Exception as e:
        return f"⚠️ خطا در اسکن: {e}"

def telegram_listener():
    offset = 0
    log("Telegram Bot Listener for @secondxHermesbot started.")
    while True:
        try:
            res = tg_call("getUpdates", {"offset": offset, "timeout": 25})
            if not res.get("ok"):
                time.sleep(3)
                continue
            for upd in res.get("result", []):
                offset = upd["update_id"] + 1
                if "callback_query" in upd:
                    cb = upd["callback_query"]
                    cid = cb["message"]["chat"]["id"]
                    data = cb.get("data", "")
                    tg_call("answerCallbackQuery", {"callback_query_id": cb["id"]})
                    if data.startswith("wurk_sub:"):
                        jid = data.split(":", 1)[1]
                        ans = approve_pending_job(jid)
                        tg_notify(ans)
                    elif data.startswith("wurk_skip:"):
                        jid = data.split(":", 1)[1]
                        ans = skip_pending_job(jid)
                        tg_notify(ans)
                elif "message" in upd:
                    msg = upd["message"]
                    cid = msg.get("chat", {}).get("id")
                    if cid != ADMIN_CHAT_ID:
                        continue
                    txt = (msg.get("text") or "").strip()
                    if txt in ("/wurk", "/panel", "/start"):
                        tg_notify(print_status_report())
                    elif txt == "/wurk_scan":
                        tg_notify("⚡ در حال اسکن فوری تسک های Wurk.fun...")
                        rep = run_scanner()
                        tg_notify(rep)
                    elif txt == "/wurk_pending":
                        st = get_state()
                        pend = st.get("pending_approvals", {})
                        if not pend:
                            tg_notify("✅ هیچ پروژه منتظر تاییدی وجود ندارد.")
                        else:
                            for jid, info in pend.items():
                                msg = (
                                    f"⏳ <b>پروژه منتظر تایید:</b>\n"
                                    f"📌 {html.escape(info['title'])}\n"
                                    f"💰 پاداش: {info['reward']} {info['asset']}\n"
                                    f"👉 <b>دستور تایید:</b> <code>/wurk_submit_{jid}</code>"
                                )
                                kb = {"inline_keyboard": [[{"text": "🚀 تایید نهایی", "callback_data": f"wurk_sub:{jid}"}, {"text": "❌ رد", "callback_data": f"wurk_skip:{jid}"}]]}
                                tg_notify(msg, kb)
                    elif txt.startswith("/wurk_submit_"):
                        jid = txt.split("_")[-1]
                        ans = approve_pending_job(jid)
                        tg_notify(ans)
                    elif txt.startswith("/wurk_mode_"):
                        m = txt.split("_")[-1].upper()
                        if m in ("SMART", "MANUAL", "AUTO"):
                            st = get_state()
                            st["mode"] = m
                            save_json(STATE_FILE, st)
                            tg_notify(f"✅ حالت Wurk Pro روی <b>{m}</b> تنظیم شد.")
        except Exception as e:
            log(f"Telegram listener error: {e}")
            time.sleep(5)

def background_worker():
    log("Background Wurk Scanner loop started.")
    while True:
        try:
            run_scanner()
        except Exception as e:
            log(f"Background worker error: {e}")
        time.sleep(120)

def main():
    if not acquire_lock():
        log("Port 59422 already locked. Exiting cleanly.")
        sys.exit(0)
    register_commands()
    threading.Thread(target=telegram_listener, daemon=True).start()
    threading.Thread(target=background_worker, daemon=True).start()
    log("Wurk.fun Pro v2.0 on @secondxHermesbot is fully ONLINE!")
    while True:
        time.sleep(60)

if __name__ == "__main__":
    main()

