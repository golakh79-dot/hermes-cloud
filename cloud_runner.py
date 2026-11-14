import os, sys, time, shutil, subprocess, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

HERMES_HOME = "/tmp/hermes_home"
os.environ["HERMES_HOME"] = HERMES_HOME
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

def bootstrap_cloud_home():
    if not os.path.exists(HERMES_HOME):
        shutil.copytree("/app/bundled_home", HERMES_HOME)
        print(f"[INIT] Copied bundled_home (skills, SOUL, memories) to {HERMES_HOME}", flush=True)
    
    # تنظیم داینامیک مدل و آدرس AI در config.yaml اگر در پنل Hostless تغییر داده شده باشند
    cfg_path = os.path.join(HERMES_HOME, "config.yaml")
    if os.path.exists(cfg_path):
        with open(cfg_path, "r", encoding="utf-8") as f:
            cfg = f.read()
        model_name = os.getenv("HERMES_MODEL", "llama-3.3-70b-versatile")
        base_url = os.getenv("AI_BASE_URL", "https://api.groq.com/openai/v1")
        cfg = cfg.replace("llama-3.3-70b-versatile", model_name).replace("https://api.groq.com/openai/v1", base_url)
        with open(cfg_path, "w", encoding="utf-8") as f:
            f.write(cfg)

    # ساخت فایل .env در مسیر قابل‌نوشتن /tmp/hermes_home/.env برای خواندن کامل توسط هسته Hermes
    env_lines = []
    for k, v in os.environ.items():
        if v and any(p in k for p in ["TOKEN", "KEY", "URL", "ID", "MODEL", "ALLOWED", "CHANNEL", "HERMES", "OPENAI", "GROQ", "OPENROUTER"]):
            env_lines.append(f"{k}={v}")
    with open(os.path.join(HERMES_HOME, ".env"), "w", encoding="utf-8") as f:
        f.write("\n".join(env_lines) + "\n")
    print("[ENV] Wrote writable .env inside /tmp/hermes_home/.env", flush=True)

PORT = int(os.getenv("PORT", "8080"))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Cloud Hermes Agent Core: ACTIVE 24/7")
    def log_message(self, format, *args): return

def run_hermes_gateway():
    while True:
        print("[🚀 GATEWAY] Starting Hermes Core Gateway (Telegram + 41 Skills)...", flush=True)
        # اجرای مستقیم cli.py gateway run
        env = os.environ.copy(); env["PYTHONPATH"] = "/app"; proc = subprocess.Popen([sys.executable, "-X", "utf8", "/app/cli.py", "gateway", "run"], cwd="/app", env=env)
        proc.wait()
        print(f"[⚠️ GATEWAY] Exited ({proc.returncode}). Auto-healing in 5s...", flush=True)
        time.sleep(5)

def run_optional_worker(script_rel_path):
    full_path = os.path.join(HERMES_HOME, script_rel_path)
    while True:
        if os.path.exists(full_path):
            print(f"[WORKER] Starting {script_rel_path}...", flush=True)
            p = subprocess.Popen([sys.executable, "-X", "utf8", full_path])
            p.wait()
        time.sleep(10)

if __name__ == "__main__":
    bootstrap_cloud_home()
    threading.Thread(target=lambda: HTTPServer(("0.0.0.0", PORT), HealthHandler).serve_forever(), daemon=True).start()
    threading.Thread(target=run_hermes_gateway, daemon=True).start()

    if os.getenv("ENABLE_TWITTER_BOT", "false").lower() == "true":
        threading.Thread(target=run_optional_worker, args=("scripts/twitter_telegram_bot_panel.py",), daemon=True).start()
    if os.getenv("ENABLE_WURK", "false").lower() == "true":
        threading.Thread(target=run_optional_worker, args=("scripts/wurk_agent.py",), daemon=True).start()

    while True:
        time.sleep(60)

