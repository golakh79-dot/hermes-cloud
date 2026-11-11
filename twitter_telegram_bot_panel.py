import os, re, sys, time, json, html, socket, threading
import urllib.parse, urllib.request, urllib.error
from datetime import datetime

HOME_DIR = r"D:\HERMES\Hermes_Portable_Data\home"
STATE_FILE = os.path.join(HOME_DIR, "twitter_targets.json")
ENV_FILE = os.path.join(HOME_DIR, ".env")
LOG_FILE = os.path.join(HOME_DIR, "twitter_hub.log")

ADMIN_CHAT_ID = 452259540
ROUTER_BASE = os.getenv("AI_BASE_URL", "http://127.0.0.1:20128/v1")
ROUTER_CHAT_URL = f"{ROUTER_BASE}/chat/completions"
LOCK_PORT = 59421

SLOP_WORDS = [
    "delve", "testament", "game-changer", "game changer", "landscape",
    "tapestry", "undeniable", "bullish on this", "revolutionary", "paradigm",
    "synergy", "beacon", "unleash", "elevate", "unlocking", "seamless", "thrilled"
]

_INSTANCE_SOCKET = None
_STATE_LOCK = threading.Lock()
TWEET_CACHE = {}

def acquire_single_instance_lock():
    global _INSTANCE_SOCKET
    _INSTANCE_SOCKET = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        _INSTANCE_SOCKET.bind(("127.0.0.1", LOCK_PORT))
        _INSTANCE_SOCKET.listen(1)
        return True
    except socket.error:
        return False

def log(msg):
    line = f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] [TWITTER-V7.2] {msg}"
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
                    if val and val != "PUT_YOUR_SECOND_BOT_TOKEN_HERE":
                        return val
    return ""

def get_bot_token():
    tok = load_env_var(["TWITTER_BOT_TOKEN", "HERMIXX_BOT_TOKEN", "TWITTER_TELEGRAM_TOKEN"])
    if tok:
        return tok
    raise RuntimeError("TWITTER_BOT_TOKEN not found in .env!")

def get_router_key():
    k = load_env_var(["RAMP_ROUTER_API_KEY", "OPENAI_API_KEY", "ROUTER_API_KEY"])
    return k if k else "sk-36e11762c99c8bad-xacbo0-bc0d894f"

def default_state():
    return {
        "targets": ["soneium", "startale", "RobinhoodApp", "arc_network"],
        "my_accounts": ["Aliz_rez"],
        "style_dna": "Casual Web3 builder and alpha hunter, ultra-concise single-line replies, lowercase friendly, zero corporate fluff",
        "seen_tweets": [],
        "recent_digest": [],
        "discovered": [],
        "active_model": "HERMES",
        "radar_enabled": True,
        "max_age_minutes": 30,
        "waiting_input": None
    }

def safe_parse_first_json(raw_str):
    if not raw_str:
        return {}
    s = raw_str.strip()
    decoder = json.JSONDecoder()
    idx = s.find("{")
    while idx != -1:
        try:
            obj, _ = decoder.raw_decode(s, idx)
            if isinstance(obj, dict):
                return obj
        except Exception:
            pass
        idx = s.find("{", idx + 1)
    return {}

def load_state():
    st = default_state()
    with _STATE_LOCK:
        if os.path.exists(STATE_FILE):
            try:
                with open(STATE_FILE, "r", encoding="utf-8", errors="ignore") as f:
                    raw = f.read()
                saved = safe_parse_first_json(raw)
                if saved:
                    st.update(saved)
            except Exception as e:
                log(f"State reset notice: {e}")
    return st

def save_state(st):
    with _STATE_LOCK:
        st["seen_tweets"] = st.get("seen_tweets", [])[-500:]
        st["recent_digest"] = st.get("recent_digest", [])[-40:]
        st["discovered"] = st.get("discovered", [])[-50:]
        tmp_file = STATE_FILE + ".tmp"
        try:
            with open(tmp_file, "w", encoding="utf-8") as f:
                json.dump(st, f, indent=2, ensure_ascii=False)
            os.replace(tmp_file, STATE_FILE)
        except Exception as e:
            log(f"Save state warning: {e}")

def tg_call(token, method, payload=None):
    url = f"https://api.telegram.org/bot{token}/{method}"
    data = json.dumps(payload or {}).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"}, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            body = r.read().decode("utf-8", errors="ignore")
            return safe_parse_first_json(body)
    except urllib.error.HTTPError as e:
        err_body = e.read().decode("utf-8", errors="ignore")
        log(f"TG HTTP Error {e.code} on {method}: {err_body}")
        return {"ok": False, "error_code": e.code, "description": err_body}
    except Exception as e:
        log(f"TG Error on {method}: {e}")
        return {"ok": False}

def register_bot_commands(token):
    commands = [
        {"command": "panel", "description": "🛸 باز کردن پنل فرماندهی زنده توییتر"},
        {"command": "targets", "description": "🎯 لیست اکانت های هدف و دریافت آخرین پست"},
        {"command": "scan", "description": "⚡ اسکن فوری تمام اکانت های هدف"},
        {"command": "dna", "description": "🧬 تنظیم اکانت شخصی و کلون لحن (Style DNA)"},
        {"command": "alpha", "description": "✍️ ساخت پست و ترد روزانه از اخبار امروز"},
        {"command": "discover", "description": "🛰 رادار کشف پروژه ها و اکانت های جدید"},
        {"command": "status", "description": "📊 وضعیت اتصال 9Router و رادار زنده"}
    ]
    if tg_call(token, "setMyCommands", {"commands": commands}).get("ok"):
        log("✅ Telegram bottom-left Hamburger Menu registered!")

def send_or_edit(token, chat_id, text, reply_markup=None, message_id=None):
    payload = {"chat_id": chat_id, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}
    if reply_markup:
        payload["reply_markup"] = reply_markup
    if message_id:
        payload["message_id"] = message_id
        res = tg_call(token, "editMessageText", payload)
        if res.get("ok"):
            return res
    return tg_call(token, "sendMessage", payload)

def clean_human_reply(text):
    if not text:
        return ""
    text = text.strip().split("\n")[0].strip()
    text = re.sub(r"^(?:reply\s*\d*|quote|option\s*\d*)\s*[:\-]\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"#[A-Za-z0-9_]+", "", text)
    text = re.sub(r"[\U00010000-\U0010ffff]", "", text)
    text = re.sub(r"[\u2600-\u27BF]", "", text)
    text = text.replace("—", " ").replace("–", " ").replace("-", " ")
    text = re.sub(r'[."\'!?;:،؛«»()\[\]{}*`~]', "", text)
    for w in SLOP_WORDS:
        text = re.sub(rf"\b{re.escape(w)}\b", "", text, flags=re.IGNORECASE)
    return re.sub(r"\s+", " ", text).strip()

def decode_9router_http_body(raw_http_text):
    """Handles single JSON, concatenated JSONs (Extra data), or SSE data: chunks from 9Router."""
    if not raw_http_text:
        return ""
    decoder = json.JSONDecoder()
    collected_content = []
    # Check if SSE stream format (data: {...})
    if "data:" in raw_http_text and "choices" in raw_http_text:
        for line in raw_http_text.splitlines():
            line = line.strip()
            if line.startswith("data:") and "[DONE]" not in line:
                obj = safe_parse_first_json(line[5:])
                choices = obj.get("choices", [])
                if choices:
                    delta = choices[0].get("delta") or choices[0].get("message") or {}
                    c = delta.get("content") or ""
                    if c:
                        collected_content.append(c)
        if collected_content:
            return "".join(collected_content).strip()

    # Scan all JSON objects in raw_http_text using raw_decode (Immune to Extra Data error!)
    idx = 0
    best_text = ""
    while idx < len(raw_http_text):
        brace = raw_http_text.find("{", idx)
        if brace == -1:
            break
        try:
            obj, end_idx = decoder.raw_decode(raw_http_text, brace)
            idx = end_idx
            if isinstance(obj, dict) and "choices" in obj and obj["choices"]:
                msg = obj["choices"][0].get("message") or obj["choices"][0].get("delta") or {}
                c = msg.get("content") or msg.get("reasoning_content") or ""
                if c:
                    best_text += c
        except Exception:
            idx = brace + 1
    return best_text.strip() if best_text else raw_http_text.strip()

def ask_9router(prompt, system_prompt, model="HERMES"):
    models_to_try = [model, "gemini/gemini-3.6-flash", "groq/openai/gpt-oss-120b", "nvidia/nvidia/nemotron-3-ultra-550b-a55b"]
    seen_m = set()
    ordered_models = [m for m in models_to_try if not (m in seen_m or seen_m.add(m))]

    last_err = None
    for m_name in ordered_models:
        payload = {
            "model": m_name,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.65,
            "stream": False
        }
        req = urllib.request.Request(
            ROUTER_CHAT_URL,
            data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {get_router_key()}"},
            method="POST"
        )
        try:
            with urllib.request.urlopen(req, timeout=50) as r:
                raw_body = r.read().decode("utf-8", errors="ignore")
            out = decode_9router_http_body(raw_body)
            out = re.sub(r"<think>.*?</think>", "", out, flags=re.DOTALL | re.IGNORECASE).strip()
            if out:
                return out
        except Exception as e:
            last_err = e
            log(f"Model {m_name} notice: {e} -> trying next fallback...")
            time.sleep(1)
    raise RuntimeError(f"All 9Router models failed: {last_err}")

def parse_tagged_ai_output(raw_text):
    """Bulletproof tag + JSON hybrid parser. Never fails on Extra Data or formatting."""
    res = {
        "fa_translation": "",
        "fa_summary": "",
        "virality_score": 9,
        "reply1_en": "",
        "reply1_fa": "",
        "reply2_en": "",
        "reply2_fa": "",
        "quote_en": "",
        "quote_fa": ""
    }
    # First try tagged format
    patterns = {
        "fa_translation": r"FA_TRANS\s*:\s*(.+)",
        "fa_summary": r"FA_SUM\s*:\s*(.+)",
        "virality_score": r"SCORE\s*:\s*(\d+)",
        "reply1_en": r"REPLY1_EN\s*:\s*(.+)",
        "reply1_fa": r"REPLY1_FA\s*:\s*(.+)",
        "reply2_en": r"REPLY2_EN\s*:\s*(.+)",
        "reply2_fa": r"REPLY2_FA\s*:\s*(.+)",
        "quote_en": r"QUOTE_EN\s*:\s*(.+)",
        "quote_fa": r"QUOTE_FA\s*:\s*(.+)"
    }
    for k, pat in patterns.items():
        m = re.search(pat, raw_text, flags=re.IGNORECASE)
        if m:
            val = m.group(1).strip()
            res[k] = int(val) if k == "virality_score" and val.isdigit() else val

    # If model output JSON anyway, extract from JSON
    if not res["reply1_en"]:
        j = safe_parse_first_json(raw_text)
        if j:
            for k in res:
                if k in j and j[k]:
                    res[k] = j[k]

    # Fallback if still empty
    if not res["fa_translation"]:
        lines = [ln.strip() for ln in raw_text.splitlines() if ln.strip()]
        res["fa_translation"] = lines[0] if lines else "ترجمه پست آماده شد"
    if not res["fa_summary"]:
        res["fa_summary"] = "آپدیت مهم اکوسیستم و فرصت تعامل بالا"
    res["reply1_en"] = clean_human_reply(str(res["reply1_en"] or "real builders keep shipping through everything"))
    res["reply2_en"] = clean_human_reply(str(res["reply2_en"] or "ecosystem momentum is getting hard to ignore right now"))
    res["quote_en"] = clean_human_reply(str(res["quote_en"] or "worth paying attention to what the team is rolling out here"))
    if not res["reply1_fa"]:
        res["reply1_fa"] = "سازندگان واقعی در هر شرایطی به ساختن ادامه می دهند"
    if not res["reply2_fa"]:
        res["reply2_fa"] = "شتاب رشد این اکوسیستم دیگر قابل چشم پوشی نیست"
    if not res["quote_fa"]:
        res["quote_fa"] = "ارزش دارد به چیزی که این تیم در حال پیاده سازی آن است دقت کنیم"
    return res

def analyze_tweet_and_generate_replies(username, tweet_text, style_dna, model, angle_hint=""):
    sys_p = (
        "You are an elite Web3 builder, alpha researcher, and X ghostwriter.\n"
        "Respond using EXACTLY these 9 labeled lines (one per line, no markdown blocks, no extra chatter):\n"
        "FA_TRANS: <fluent Persian translation of the post>\n"
        "FA_SUM: <1-line sharp Persian summary/alpha takeaway>\n"
        "SCORE: <number 1 to 10>\n"
        "REPLY1_EN: <Builder/Technical 1-line English reply, ZERO punctuation, no periods, no dashes, no emojis>\n"
        "REPLY1_FA: <Persian translation of REPLY1_EN>\n"
        "REPLY2_EN: <Witty/High-Engagement 1-line English reply, ZERO punctuation, no periods, no dashes, no emojis>\n"
        "REPLY2_FA: <Persian translation of REPLY2_EN>\n"
        "QUOTE_EN: <1-line English Quote-Tweet caption, ZERO punctuation, no periods, no dashes, no emojis>\n"
        "QUOTE_FA: <Persian translation of QUOTE_EN>\n\n"
        f"User Style DNA: {style_dna}\n{angle_hint}"
    )
    raw = ask_9router(f"Account: @{username}\nPost text:\n{tweet_text[:900]}", sys_p, model=model)
    return parse_tagged_ai_output(raw)

def tweet_time_info(tweet_id_str):
    try:
        tid = int(tweet_id_str)
        ts_ms = (tid >> 22) + 1288834974657
        age_min = max(0.5, (int(time.time() * 1000) - ts_ms) / 60000.0)
        dt_str = datetime.fromtimestamp(ts_ms / 1000.0).strftime("%Y-%m-%d %H:%M")
        if age_min < 60:
            human_age = f"{int(age_min)} دقیقه پیش ({dt_str})"
        elif age_min < 1440:
            hrs = int(age_min // 60)
            mins = int(age_min % 60)
            human_age = f"{hrs} ساعت و {mins} دقیقه پیش ({dt_str})"
        else:
            days = int(age_min // 1440)
            human_age = f"{days} روز پیش ({dt_str})"
        return age_min, human_age
    except Exception:
        return 999999.0, "نامشخص"

def fetch_latest_tweets(username):
    username = username.lstrip("@").strip()
    tweets = []
    try:
        j_url = f"https://r.jina.ai/https://x.com/{username}"
        req = urllib.request.Request(j_url, headers={"User-Agent": "Mozilla/5.0", "X-Return-Format": "markdown"})
        with urllib.request.urlopen(req, timeout=20) as r:
            md = r.read().decode("utf-8", errors="ignore")
        seen_ids = set()
        for m in re.finditer(rf"https?://(?:x|twitter)\.com/{re.escape(username)}/status/(\d{{15,22}})", md, re.IGNORECASE):
            tid = m.group(1)
            if tid in seen_ids:
                continue
            seen_ids.add(tid)
            chunk = md[max(0, m.start() - 650):m.start()].strip()
            lines = [
                ln.strip() for ln in chunk.split("\n")
                if len(ln.strip()) > 15
                and not ln.strip().startswith(("![", "[![", "Title:", "URL Source:"))
                and "pinned" not in ln.lower()[:15]
            ]
            snippet = " ".join(lines[-2:]) if len(lines) >= 2 else (lines[-1] if lines else f"Update from @{username}")
            snippet = re.sub(r"\[([^\]]+)\]\([^\)]+\)", r"\1", snippet).strip()
            tw = {"id": tid, "text": snippet[:700], "user": username}
            tweets.append(tw)
            TWEET_CACHE[tid] = tw
        if tweets:
            tweets.sort(key=lambda x: int(x["id"]), reverse=True)
            log(f"Fetched {len(tweets)} live posts for @{username} (latest ID: {tweets[0]['id']})")
            return tweets
    except Exception as e:
        log(f"Jina fetch notice for @{username}: {e}")
    return tweets

def fetch_single_tweet_by_url(user, tid):
    if tid in TWEET_CACHE:
        return TWEET_CACHE[tid]
    tws = fetch_latest_tweets(user)
    for t in tws:
        if t["id"] == tid:
            return t
    return {"id": tid, "text": f"Post {tid} from @{user}", "user": user}

def extract_mentions(text, current_targets, my_accounts):
    found = re.findall(r"@([A-Za-z0-9_]{3,15})", text or "")
    existing = {x.lower() for x in (current_targets + my_accounts)}
    return [u for u in set(found) if u.lower() not in existing]

def send_tweet_alert(token, st, tw, angle_hint="", edit_mid=None):
    user, tid, txt = tw["user"], tw["id"], tw["text"]
    TWEET_CACHE[tid] = tw
    age_min, human_age = tweet_time_info(tid)
    st.setdefault("recent_digest", []).append({"user": user, "id": tid, "text": txt})
    for m_user in extract_mentions(txt, st["targets"], st["my_accounts"]):
        if m_user not in st["discovered"]:
            st["discovered"].append(m_user)
    save_state(st)

    try:
        ai = analyze_tweet_and_generate_replies(user, txt, st["style_dna"], st["active_model"], angle_hint=angle_hint)
    except Exception as e:
        log(f"AI generation error for {tid}: {e}")
        if edit_mid:
            send_or_edit(token, ADMIN_CHAT_ID, f"⚠️ خطا در ارتباط با 9Router برای @{html.escape(user)}:\n<code>{html.escape(str(e))}</code>", build_main_menu(st)[1], edit_mid)
        return False

    r1_en, r1_fa = ai["reply1_en"], ai["reply1_fa"]
    r2_en, r2_fa = ai["reply2_en"], ai["reply2_fa"]
    q_en, q_fa = ai["quote_en"], ai["quote_fa"]
    fa_trans, fa_sum = ai["fa_translation"], ai["fa_summary"]
    v_score = ai["virality_score"]

    t_url = f"https://x.com/{user}/status/{tid}"
    intent1 = f"https://x.com/intent/tweet?in_reply_to={tid}&text={urllib.parse.quote(r1_en)}"
    intent2 = f"https://x.com/intent/tweet?in_reply_to={tid}&text={urllib.parse.quote(r2_en)}"
    intent_q = f"https://x.com/intent/tweet?url={urllib.parse.quote(t_url)}&text={urllib.parse.quote(q_en)}"

    msg = (
        f"🎯 <b>اکانت:</b> <a href='https://x.com/{user}'>@{html.escape(user)}</a>\n"
        f"🕒 <b>زمان انتشار:</b> {html.escape(human_age)} | 🔥 <b>وایرالیتی:</b> {v_score}/10\n"
        f"🔗 <a href='{t_url}'>مشاهده مستقیم پست در X</a>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📝 <b>متن اصلی پست:</b>\n<code>{html.escape(txt[:550])}</code>\n\n"
        f"🇮🇷 <b>ترجمه فارسی:</b>\n{html.escape(fa_trans)}\n\n"
        f"💡 <b>تحلیل و نکته (Alpha):</b> {html.escape(fa_sum)}\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🛠 <b>کامنت ۱ (فنی/Builder — لمس برای کپی):</b>\n"
        f"<code>{html.escape(r1_en)}</code>\n"
        f"🔹 <i>ترجمه: {html.escape(r1_fa)}</i>\n\n"
        f"⚡ <b>کامنت ۲ (وایرال/تعاملی — لمس برای کپی):</b>\n"
        f"<code>{html.escape(r2_en)}</code>\n"
        f"🔸 <i>ترجمه: {html.escape(r2_fa)}</i>\n\n"
        f"🔁 <b>پیشنهاد Quote-Tweet (کوت کردن پست):</b>\n"
        f"<code>{html.escape(q_en)}</code>\n"
        f"▫️ <i>ترجمه: {html.escape(q_fa)}</i>"
    )
    kb = {
        "inline_keyboard": [
            [{"text": "🚀 ارسال کامنت ۱ در X", "url": intent1}, {"text": "🚀 ارسال کامنت ۲ در X", "url": intent2}],
            [{"text": "🔁 کوت کردن پست در X", "url": intent_q}],
            [{"text": "🔄 کامنت های جدید", "callback_data": f"regen:{user}:{tid}"}, {"text": "🔥 لحن تیزتر/کوتاه تر", "callback_data": f"sharp:{user}:{tid}"}],
            [{"text": f"📜 ۳ پست آخر @{user}", "callback_data": f"hist:{user}"}, {"text": "🎯 لیست اهداف", "callback_data": "menu:targets"}],
            [{"text": "🏠 برگشت به پنل اصلی", "callback_data": "menu:main"}]
        ]
    }
    send_or_edit(token, ADMIN_CHAT_ID, msg, reply_markup=kb, message_id=edit_mid)
    log(f"✅ Delivered live card & replies for @{user} ({tid})!")
    return True

def generate_daily_alpha_post(st):
    digest = st.get("recent_digest", [])
    if not digest:
        return "هنوز پستی در حافظه امروز ذخیره نشده است. ابتدا روی یکی از اکانت های هدف کلیک کنید."
    context_str = "\n".join([f"@{d['user']}: {d['text'][:200]}" for d in digest[-10:]])
    sys_p = (
        "You are a Web3 content creator matching this Style DNA: " + st.get("style_dna", "") + "\n"
        "Based on today's updates from target accounts, write:\n"
        "1. Two standalone single-line English X posts (ZERO punctuation, no periods, no dashes, no hashtags) + Persian translations.\n"
        "2. A high-engagement 3-part English micro-thread + brief Persian explanation."
    )
    return ask_9router(f"Today's Web3 ecosystem updates:\n{context_str}", sys_p, model=st.get("active_model", "HERMES"))

def run_radar_scan(token, force_latest=False):
    st = load_state()
    max_age = float(st.get("max_age_minutes", 30))
    found_count = 0
    for target in list(st.get("targets", [])):
        tweets = fetch_latest_tweets(target)
        if not tweets:
            continue
        tw = tweets[0]
        tid = tw["id"]
        age_min, _ = tweet_time_info(tid)
        if not force_latest and tid in st["seen_tweets"]:
            continue
        if age_min <= max_age or force_latest:
            if send_tweet_alert(token, st, tw):
                if tid not in st["seen_tweets"]:
                    st["seen_tweets"].append(tid)
                save_state(st)
                found_count += 1
    save_state(st)
    return found_count

def background_worker(token):
    log("Background Live Radar v7.2 started.")
    while True:
        try:
            st = load_state()
            if st.get("radar_enabled", True):
                run_radar_scan(token, force_latest=False)
        except Exception as e:
            log(f"Radar worker error: {e}")
        time.sleep(180)

def build_main_menu(st):
    status_icon = f"🟢 فعال (پست های زیر {st.get('max_age_minutes', 30)} دقیقه)" if st.get("radar_enabled", True) else "🔴 متوقف"
    targets_preview = " ، ".join([f"@{t}" for t in st.get("targets", [])[:6]]) or "خالی"
    text = (
        f"🛸 <b>مرکز فرماندهی زنده توییتر هرمس (v7.2 Ultimate)</b>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📡 <b>وضعیت رادار خودکار:</b> {status_icon}\n"
        f"🧠 <b>موتور هوش مصنوعی:</b> <code>{html.escape(st.get('active_model', 'HERMES'))}</code>\n"
        f"🎯 <b>اهداف تحت رصد ({len(st.get('targets', []))}):</b> {html.escape(targets_preview)}\n"
        f"👤 <b>اکانت شخصی من:</b> {', '.join('@'+a for a in st.get('my_accounts', [])) or 'ثبت نشده'}\n"
        f"🧬 <b>لحن اختصاصی (Style DNA):</b>\n<i>{html.escape(st.get('style_dna', '')[:140])}</i>\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"💡 <i>هر زمان لینک یک توییت یا @username را در چت بفرستید، درجا آخرین پستش با ترجمه و کامنت آماده می شود!</i>"
    )
    kb = {
        "inline_keyboard": [
            [{"text": "🎯 ورود به لیست اکانت ها (دریافت زنده آخرین پست هر هدف)", "callback_data": "menu:targets"}],
            [{"text": "⚡ اسکن فوری همه اهداف", "callback_data": "act:scan_now"}, {"text": "🔄 روشن/خاموش رادار", "callback_data": "act:toggle_radar"}],
            [{"text": "👤 اکانت من و کلون لحن (DNA)", "callback_data": "menu:my_acc"}, {"text": "⏱ تنظیم بازه زمانی رادار", "callback_data": "menu:time"}],
            [{"text": "✍️ ساخت پست/ترد روزانه", "callback_data": "act:daily_alpha"}, {"text": f"🛰 کشف اکانت ({len(st.get('discovered', []))})", "callback_data": "menu:discover"}]
        ]
    }
    return text, kb

def build_targets_menu(st):
    rows = []
    for u in st.get("targets", []):
        rows.append([
            {"text": f"🎯 @{u} (⚡ آخرین پست زنده)", "callback_data": f"fetch_one:{u}"},
            {"text": "📜 ۳ پست آخر", "callback_data": f"hist:{u}"},
            {"text": "❌", "callback_data": f"del_t:{u}"}
        ])
    rows.append([{"text": "➕ افزودن اکانت هدف جدید", "callback_data": "inp:add_target"}])
    rows.append([{"text": "⚡ اسکن یکجای تمام اهداف بالا", "callback_data": "act:scan_now"}])
    rows.append([{"text": "🔙 بازگشت به پنل اصلی", "callback_data": "menu:main"}])
    txt = (
        "🎯 <b>لیست اکانت های هدف (رصد زنده):</b>\n\n"
        "👇 روی نام هر اکانت بزنید تا <b>آخرین پست آن</b> به همراه زمان دقیق، ترجمه فارسی و ۳ کامنت آماده با لحن شما درجا نمایش داده شود:"
    )
    return txt, {"inline_keyboard": rows}

def handle_callback(token, cb):
    cid, mid, data = cb["message"]["chat"]["id"], cb["message"]["message_id"], cb.get("data", "").strip()
    tg_call(token, "answerCallbackQuery", {"callback_query_id": cb["id"]})
    st = load_state()
    st["waiting_input"] = None
    save_state(st)

    if data == "menu:main":
        txt, kb = build_main_menu(st)
        send_or_edit(token, cid, txt, kb, mid)
    elif data == "act:toggle_radar":
        st["radar_enabled"] = not st.get("radar_enabled", True)
        save_state(st)
        txt, kb = build_main_menu(st)
        send_or_edit(token, cid, txt, kb, mid)
    elif data == "menu:time":
        kb = {
            "inline_keyboard": [
                [{"text": "⏱ ۱۵ دقیقه", "callback_data": "set_age:15"}, {"text": "⏱ ۳۰ دقیقه", "callback_data": "set_age:30"}, {"text": "⏱ ۶۰ دقیقه", "callback_data": "set_age:60"}],
                [{"text": "⏱ ۳ ساعت", "callback_data": "set_age:180"}, {"text": "⏱ ۱۲ ساعت", "callback_data": "set_age:720"}, {"text": "⏱ ۲۴ ساعت", "callback_data": "set_age:1440"}],
                [{"text": "🔙 بازگشت", "callback_data": "menu:main"}]
            ]
        }
        send_or_edit(token, cid, f"⏱ <b>بازه فعلی رادار خودکار:</b> پست های جدیدتر از <b>{st.get('max_age_minutes', 30)} دقیقه</b>", kb, mid)
    elif data.startswith("set_age:"):
        mins = int(data.split(":")[1])
        st["max_age_minutes"] = mins
        save_state(st)
        txt, kb = build_main_menu(st)
        send_or_edit(token, cid, f"✅ بازه رادار روی <b>{mins} دقیقه</b> تنظیم شد!\n\n" + txt, kb, mid)
    elif data == "menu:targets":
        txt, kb = build_targets_menu(st)
        send_or_edit(token, cid, txt, kb, mid)
    elif data.startswith("fetch_one:"):
        u = data.split(":", 1)[1]
        send_or_edit(token, cid, f"📡 <b>در حال استخراج زنده آخرین پست @{html.escape(u)} و تولید کامنت...</b>", None, mid)
        tws = fetch_latest_tweets(u)
        if not tws:
            txt, kb = build_targets_menu(st)
            send_or_edit(token, cid, f"⚠️ پستی از @{html.escape(u)} دریافت نشد.\n\n" + txt, kb, mid)
            return
        send_tweet_alert(token, st, tws[0], edit_mid=mid)
    elif data.startswith("hist:"):
        u = data.split(":", 1)[1]
        send_or_edit(token, cid, f"📜 <b>در حال دریافت ۳ پست آخر @{html.escape(u)}...</b>", None, mid)
        tws = fetch_latest_tweets(u)[:3]
        if not tws:
            txt, kb = build_targets_menu(st)
            send_or_edit(token, cid, f"⚠️ پستی برای @{html.escape(u)} یافت نشد.\n\n" + txt, kb, mid)
            return
        lines = [f"📜 <b>۳ پست آخر اکانت @{html.escape(u)}:</b>\n<i>روی دکمه هر پست بزنید تا ترجمه و کامنت هایش ساخته شود:</i>\n"]
        btn_rows = []
        for idx, t in enumerate(tws, 1):
            _, h_age = tweet_time_info(t["id"])
            lines.append(f"<b>{idx}. ({html.escape(h_age)}):</b>\n<code>{html.escape(t['text'][:180])}...</code>\n")
            btn_rows.append([{"text": f"💬 ترجمه و کامنت پست شماره {idx}", "callback_data": f"anlz:{u}:{t['id']}"}])
        btn_rows.append([{"text": "🎯 برگشت به لیست اهداف", "callback_data": "menu:targets"}, {"text": "🏠 پنل اصلی", "callback_data": "menu:main"}])
        send_or_edit(token, cid, "\n".join(lines), {"inline_keyboard": btn_rows}, mid)
    elif data.startswith("anlz:"):
        _, u, tid = data.split(":", 2)
        send_or_edit(token, cid, f"🧠 <b>در حال ترجمه و ساخت کامنت برای پست @{html.escape(u)}...</b>", None, mid)
        tw = fetch_single_tweet_by_url(u, tid)
        send_tweet_alert(token, st, tw, edit_mid=mid)
    elif data == "act:scan_now":
        send_or_edit(token, cid, "⚡ <b>در حال اسکن فوری تمام اکانت های هدف...</b>", None, mid)
        cnt = run_radar_scan(token, force_latest=True)
        txt, kb = build_main_menu(load_state())
        send_or_edit(token, cid, f"✅ <b>اسکن فوری تکمیل شد ({cnt} پست تحلیل و ارسال شد).</b>\n\n" + txt, kb)
    elif data == "act:daily_alpha":
        send_or_edit(token, cid, "⏳ <b>در حال نوشتن پست و ترد روزانه بر اساس اخبار اهداف شما...</b>", None, mid)
        alpha_post = generate_daily_alpha_post(st)
        kb = {"inline_keyboard": [[{"text": "🔄 تولید مجدد", "callback_data": "act:daily_alpha"}, {"text": "🔙 بازگشت", "callback_data": "menu:main"}]]}
        send_or_edit(token, cid, f"✍️ <b>پیشنهاد پست و ترد روزانه:</b>\n\n{html.escape(alpha_post)}", kb, mid)
    elif data.startswith("del_t:"):
        u = data.split(":", 1)[1]
        st["targets"] = [x for x in st["targets"] if x.lower() != u.lower()]
        save_state(st)
        txt, kb = build_targets_menu(st)
        send_or_edit(token, cid, f"✅ اکانت @{html.escape(u)} حذف شد.\n\n" + txt, kb, mid)
    elif data == "inp:add_target":
        st["waiting_input"] = "add_target"
        save_state(st)
        send_or_edit(token, cid, "✏️ <b>یوزرنیم اکانت هدف را بفرستید (می توانید چند اکانت با فاصله بفرستید):</b>", {"inline_keyboard": [[{"text": "🔙 انصراف", "callback_data": "menu:targets"}]]}, mid)
    elif data == "menu:my_acc":
        accs = st.get("my_accounts", [])
        rows = [[{"text": f"@{a}", "url": f"https://x.com/{a}"}, {"text": "🧬 کلون لحن از پست هایم", "callback_data": f"dna:{a}"}, {"text": "❌", "callback_data": f"del_my:{a}"}] for a in accs]
        rows.append([{"text": "➕ افزودن یوزرنیم اکانت توییتر خودم", "callback_data": "inp:add_my"}])
        rows.append([{"text": "✍️ ویرایش دستی Style DNA", "callback_data": "inp:edit_dna"}])
        rows.append([{"text": "🔙 بازگشت به پنل اصلی", "callback_data": "menu:main"}])
        msg = f"👤 <b>اکانت شخصی و مهندسی لحن (Style DNA):</b>\n\n<code>{html.escape(st.get('style_dna', ''))}</code>"
        send_or_edit(token, cid, msg, {"inline_keyboard": rows}, mid)
    elif data == "inp:add_my":
        st["waiting_input"] = "add_my"
        save_state(st)
        send_or_edit(token, cid, "✏️ <b>یوزرنیم اکانت توییتر خودتان را بفرستید:</b>", {"inline_keyboard": [[{"text": "🔙 انصراف", "callback_data": "menu:my_acc"}]]}, mid)
    elif data == "inp:edit_dna":
        st["waiting_input"] = "edit_dna"
        save_state(st)
        send_or_edit(token, cid, "✏️ <b>توصیف لحن یا نمونه کامنت های دلخواهتان را بفرستید:</b>", {"inline_keyboard": [[{"text": "🔙 انصراف", "callback_data": "menu:my_acc"}]]}, mid)
    elif data.startswith("del_my:"):
        u = data.split(":", 1)[1]
        st["my_accounts"] = [x for x in st["my_accounts"] if x.lower() != u.lower()]
        save_state(st)
        handle_callback(token, {**cb, "data": "menu:my_acc"})
    elif data.startswith("dna:"):
        u = data.split(":", 1)[1]
        send_or_edit(token, cid, f"🧬 <b>در حال آنالیز پست های @{html.escape(u)} و استخراج لحن شما...</b>", None, mid)
        tws = fetch_latest_tweets(u)
        sample = "\n".join(t["text"] for t in tws[:8])
        if sample:
            st["style_dna"] = ask_9router(f"Summarize the exact writing style and tone of these posts in 25 English words:\n{sample}", "Linguistic profiler.", st["active_model"])
            save_state(st)
        handle_callback(token, {**cb, "data": "menu:my_acc"})
    elif data == "menu:discover":
        rows = [[{"text": f"@{u}", "url": f"https://x.com/{u}"}, {"text": "⚡ آخرین پست", "callback_data": f"fetch_one:{u}"}, {"text": "➕ افزودن به اهداف", "callback_data": f"add_disc:{u}"}] for u in st.get("discovered", [])[-10:]]
        rows.append([{"text": "🔙 بازگشت", "callback_data": "menu:main"}])
        send_or_edit(token, cid, "🛰 <b>اکانت های کشف شده در پست های اهداف شما:</b>", {"inline_keyboard": rows}, mid)
    elif data.startswith("add_disc:"):
        u = data.split(":", 1)[1]
        if u not in st["targets"]:
            st["targets"].append(u)
        if u in st["discovered"]:
            st["discovered"].remove(u)
        save_state(st)
        handle_callback(token, {**cb, "data": "menu:discover"})
    elif data.startswith("regen:") or data.startswith("sharp:"):
        parts = data.split(":")
        if len(parts) == 3:
            mode, u, tid = parts[0], parts[1], parts[2]
            send_or_edit(token, cid, f"🔄 <b>در حال ساخت کامنت های جدید برای @{html.escape(u)}...</b>", None, mid)
            tw = fetch_single_tweet_by_url(u, tid)
            hint = "Make replies ULTRA short (under 8 words), lowercase, punchy alpha vibe." if mode == "sharp" else "Generate fresh creative reply angles."
            send_tweet_alert(token, st, tw, angle_hint=hint, edit_mid=mid)

def handle_text_message(token, cid, txt):
    st = load_state()
    if txt in ("/start", "/panel", "/menu"):
        st["waiting_input"] = None
        save_state(st)
        m_txt, kb = build_main_menu(st)
        send_or_edit(token, cid, m_txt, kb)
        return
    if txt == "/targets":
        t_txt, kb = build_targets_menu(st)
        send_or_edit(token, cid, t_txt, kb)
        return
    if txt == "/scan":
        send_or_edit(token, cid, "⚡ <b>در حال اسکن فوری تمام اکانت های هدف...</b>")
        cnt = run_radar_scan(token, force_latest=True)
        m_txt, kb = build_main_menu(load_state())
        send_or_edit(token, cid, f"✅ اسکن فوری انجام شد ({cnt} پست تحلیل شد).\n\n" + m_txt, kb)
        return
    if txt == "/dna":
        st["waiting_input"] = "edit_dna"
        save_state(st)
        send_or_edit(token, cid, f"🧬 <b>لحن فعلی شما:</b>\n<code>{html.escape(st.get('style_dna', ''))}</code>\n\n✏️ توصیف لحن جدیدتان را بفرستید:", {"inline_keyboard": [[{"text": "🔙 بازگشت", "callback_data": "menu:main"}]]})
        return
    if txt == "/alpha":
        send_or_edit(token, cid, "⏳ <b>در حال ساخت پست/ترد روزانه...</b>")
        alpha_post = generate_daily_alpha_post(st)
        kb = {"inline_keyboard": [[{"text": "🔙 بازگشت", "callback_data": "menu:main"}]]}
        send_or_edit(token, cid, f"✍️ <b>پیشنهاد پست و ترد روزانه:</b>\n\n{html.escape(alpha_post)}", kb)
        return
    if txt == "/discover":
        rows = [[{"text": f"@{u}", "url": f"https://x.com/{u}"}, {"text": "⚡ آخرین پست", "callback_data": f"fetch_one:{u}"}, {"text": "➕ افزودن", "callback_data": f"add_disc:{u}"}] for u in st.get("discovered", [])[-10:]]
        rows.append([{"text": "🔙 بازگشت", "callback_data": "menu:main"}])
        send_or_edit(token, cid, "🛰 <b>اکانت های کشف شده:</b>", {"inline_keyboard": rows})
        return
    if txt == "/status":
        send_or_edit(token, cid, f"✅ <b>ربات v7.2 Ultimate آنلاین است!</b>\n🧠 کامبو: <code>{st.get('active_model')}</code>\n🎯 اهداف: {len(st.get('targets', []))}\n📦 پست های کش شده: {len(TWEET_CACHE)}", build_main_menu(st)[1])
        return

    url_m = re.search(r"https?://(?:x|twitter)\.com/([A-Za-z0-9_]+)/status/(\d{15,22})", txt)
    if url_m and not st.get("waiting_input"):
        u, tid = url_m.group(1), url_m.group(2)
        wait_msg = send_or_edit(token, cid, f"🔗 <b>لینک پست @{html.escape(u)} دریافت شد! در حال ترجمه و ساخت کامنت...</b>")
        mid = wait_msg.get("result", {}).get("message_id")
        tw = fetch_single_tweet_by_url(u, tid)
        send_tweet_alert(token, st, tw, edit_mid=mid)
        return

    if st.get("waiting_input") == "add_target" and txt:
        raw_items = re.split(r"[\s,،\n]+", txt)
        added = []
        for item in raw_items:
            u = item.lstrip("@").split("/")[-1].strip()
            if u and re.match(r"^[A-Za-z0-9_]{1,15}$", u) and u.lower() not in [x.lower() for x in st["targets"]]:
                st["targets"].append(u)
                added.append(u)
        st["waiting_input"] = None
        save_state(st)
        t_txt, kb = build_targets_menu(st)
        send_or_edit(token, cid, f"✅ اضافه شد: <b>{', '.join('@'+a for a in added)}</b>\n\n" + t_txt, kb)
        return
    elif st.get("waiting_input") == "add_my" and txt:
        u = txt.lstrip("@").split("/")[-1].strip()
        if u and u not in st["my_accounts"]:
            st["my_accounts"].append(u)
        st["waiting_input"] = None
        save_state(st)
        m_txt, kb = build_main_menu(st)
        send_or_edit(token, cid, f"✅ اکانت شخصی <b>@{html.escape(u)}</b> ثبت شد!\n\n" + m_txt, kb)
        return
    elif st.get("waiting_input") == "edit_dna" and txt:
        st["style_dna"] = txt
        st["waiting_input"] = None
        save_state(st)
        m_txt, kb = build_main_menu(st)
        send_or_edit(token, cid, "✅ <b>لحن اختصاصی شما آپدیت شد!</b>\n\n" + m_txt, kb)
        return

    if txt.startswith("@") and len(txt) < 25 and " " not in txt:
        u = txt.lstrip("@").strip()
        wait_msg = send_or_edit(token, cid, f"📡 <b>در حال دریافت زنده آخرین پست @{html.escape(u)} و تولید کامنت...</b>")
        mid = wait_msg.get("result", {}).get("message_id")
        tws = fetch_latest_tweets(u)
        if tws:
            send_tweet_alert(token, st, tws[0], edit_mid=mid)
        else:
            send_or_edit(token, cid, f"⚠️ پستی برای @{html.escape(u)} پیدا نشد.", build_main_menu(st)[1], mid)



# === [HERMES V9.5 SAFE OVERRIDE START] ===
from datetime import datetime, timezone

def _v95_clean_html(raw_html):
    text = re.sub(r"<br\s*/?>", "\n", raw_html, flags=re.IGNORECASE)
    text = re.sub(r"<[^>]+>", "", text)
    return html.unescape(text).strip()

def fetch_exact_status_v95(username, tid):
    """واکشی مستقیم تک‌پست از روی Tweet ID بدون اسکن پروفایل"""
    tid = str(tid).strip()
    u_clean = (username or "i").lstrip("@").strip()
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/124.0.0.0"}

    # ۱. FxTwitter / VxTwitter JSON API
    for host in ["api.fxtwitter.com", "api.vxtwitter.com"]:
        try:
            url = f"https://{host}/{u_clean}/status/{tid}"
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=10) as resp:
                data = json.loads(resp.read().decode("utf-8", errors="replace"))
                tw = data.get("tweet") if isinstance(data.get("tweet"), dict) else data
                txt = (tw.get("text") or tw.get("full_text") or "").strip()
                if txt and "PostsReplies" not in txt:
                    author = (tw.get("author") or {}).get("screen_name") or tw.get("user_screen_name") or u_clean
                    is_rep = bool(tw.get("replying_to") or tw.get("replying_to_status"))
                    return {"id": tid, "user": author, "text": txt, "url": f"https://x.com/{author}/status/{tid}", "is_reply": is_rep}
        except Exception as e:
            log(f"[v95 {host}] {e}")

    # ۲. Syndication API
    try:
        syn_url = f"https://cdn.syndication.twimg.com/tweet-result?id={tid}&lang=en&token=a"
        req = urllib.request.Request(syn_url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
            txt = (data.get("text") or "").strip()
            if txt:
                author = (data.get("user") or {}).get("screen_name") or u_clean
                is_rep = bool(data.get("in_reply_to_status_id_str") or data.get("in_reply_to_screen_name"))
                return {"id": tid, "user": author, "text": txt, "url": f"https://x.com/{author}/status/{tid}", "is_reply": is_rep}
    except Exception as e:
        log(f"[v95 Syndication] {e}")

    # ۳. Twitter Publish oEmbed
    try:
        t_url = f"https://twitter.com/{u_clean}/status/{tid}"
        oembed_url = f"https://publish.twitter.com/oembed?url={urllib.parse.quote(t_url)}&omit_script=true"
        req = urllib.request.Request(oembed_url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=10) as resp:
            data = json.loads(resp.read().decode("utf-8", errors="replace"))
            m_p = re.search(r"<p[^>]*>(.*?)</p>", data.get("html", ""), re.DOTALL | re.IGNORECASE)
            if m_p:
                txt = _v95_clean_html(m_p.group(1))
                if txt:
                    return {"id": tid, "user": u_clean, "text": txt, "url": f"https://x.com/{u_clean}/status/{tid}", "is_reply": False}
    except Exception:
        pass

    return None

def fetch_latest_tweets(username):
    """استخراج آخرین پست اورجینال پروفایل بر اساس تاریخ دقیق آپلود (Snowflake ID) بدون پست پین‌شده و بدون ریپلای"""
    u = username.lstrip("@").strip()
    hdrs = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)", "X-No-Cache": "true"}
    found_ids = set()

    try:
        j_url = f"https://r.jina.ai/https://x.com/{u}"
        req = urllib.request.Request(j_url, headers=hdrs)
        with urllib.request.urlopen(req, timeout=18) as resp:
            md = resp.read().decode("utf-8", errors="replace")

        pat = re.compile(rf"https?://(?:x|twitter)\.com/{re.escape(u)}/status/(\d{{15,22}})", re.IGNORECASE)
        for m in pat.finditer(md):
            tid_s = m.group(1)
            before = md[max(0, m.start() - 240):m.start()].lower()
            if "pinned" in before[-150:]:
                continue
            found_ids.add(int(tid_s))
    except Exception as e:
        log(f"[v95 Profile Scan] {e}")

    # مرتب‌سازی نزولی بر اساس عدد Tweet ID (بزرگترین عدد = جدیدترین پست آپلود شده به ثانیه)
    for tid_int in sorted(found_ids, reverse=True):
        tw = fetch_exact_status_v95(u, str(tid_int))
        if not tw:
            continue
        if tw["user"].lower() != u.lower() or tw.get("is_reply"):
            continue
        if "PostsReplies" in tw["text"] or "RepliesReposts" in tw["text"]:
            continue
        return [tw]

    return []

_base_handle_text_message = handle_text_message

def handle_text_message(token, cid, txt):
    txt_s = (txt or "").strip()
    m_direct = re.search(r"https?://(?:www\.|mobile\.)?(?:x|twitter)\.com/([A-Za-z0-9_]+)/status/(\d{15,22})", txt_s, re.IGNORECASE)
    if m_direct:
        u_d, tid_d = m_direct.group(1), m_direct.group(2)
        st = load_state()
        st["chat_id"] = cid
        save_state(st)
        w_msg = send_or_edit(token, cid, f"🎯 <b>در حال استخراج مستقیم پست <code>{tid_d}</code> از @{html.escape(u_d)}...</b>")
        mid = (w_msg or {}).get("result", {}).get("message_id")
        exact = fetch_exact_status_v95(u_d, tid_d)
        if exact:
            send_tweet_alert(token, st, exact, edit_mid=mid)
        else:
            send_or_edit(token, cid, f"⚠️ <b>خطا در خواندن پست <code>{tid_d}</code>.</b>", build_main_menu(st)[1], mid)
        return
    return _base_handle_text_message(token, cid, txt)
# === [HERMES V9.5 SAFE OVERRIDE END] ===


def main():
    if not acquire_single_instance_lock():
        log("Port 59421 is locked by another instance. Exiting cleanly.")
        sys.exit(0)
    token = get_bot_token()
    tg_call(token, "deleteWebhook", {"drop_pending_updates": False})
    register_bot_commands(token)
    threading.Thread(target=background_worker, args=(token,), daemon=True).start()
    offset = 0
    log("Twitter Hub Bot v7.2 Ultimate is ONLINE and polling cleanly!")
    while True:
        res = tg_call(token, "getUpdates", {"offset": offset, "timeout": 20})
        if not res.get("ok"):
            time.sleep(4)
            continue
        for upd in res.get("result", []):
            offset = upd["update_id"] + 1
            if "callback_query" in upd:
                threading.Thread(target=handle_callback, args=(token, upd["callback_query"]), daemon=True).start()
            elif "message" in upd:
                msg = upd["message"]
                cid = msg.get("chat", {}).get("id")
                if cid != ADMIN_CHAT_ID:
                    continue
                txt = (msg.get("text") or "").strip()
                if txt:
                    threading.Thread(target=handle_text_message, args=(token, cid, txt), daemon=True).start()

if __name__ == "__main__":
    main()
