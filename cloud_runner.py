import os, sys, time, shutil, subprocess, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

HERMES_HOME = "/tmp/hermes_home"
os.environ["HERMES_HOME"] = HERMES_HOME
os.environ["PYTHONPATH"] = "/app"
os.environ["PYTHONUTF8"] = "1"
os.environ["PYTHONUNBUFFERED"] = "1"

if "/app" not in sys.path:
    sys.path.insert(0, "/app")

def bootstrap_cloud_home():
    if not os.path.exists(HERMES_HOME):
        shutil.copytree("/app/bundled_home", HERMES_HOME)
        print(f"[INIT] Copied bundled_home to {HERMES_HOME}", flush=True)

    # نوشتن متغیرهای محیطی در فایل .env داخل مسیر قابل نوشتن
    env_lines = []
    for k, v in os.environ.items():
        if v and any(p in k for p in ["TOKEN", "KEY", "URL", "ID", "MODEL", "ALLOWED", "CHANNEL", "OPENAI", "GROQ"]):
            env_lines.append(f"{k}={v}")
    with open(os.path.join(HERMES_HOME, ".env"), "w", encoding="utf-8") as f:
        f.write("\n".join(env_lines) + "\n")
    print("[ENV] Wrote writable .env", flush=True)

PORT = int(os.getenv("PORT", "8080"))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Cloud Hermes Telegram Bot: ACTIVE 24/7")
    def log_message(self, format, *args): return

def run_direct_telegram_bot():
    bot_script = os.path.join(HERMES_HOME, "scripts", "twitter_telegram_bot_panel.py")
    while True:
        if os.path.exists(bot_script):
            print("[🚀 BOT] Starting Direct Telegram Bot Panel...", flush=True)
            env = os.environ.copy()
            env["PYTHONPATH"] = "/app"
            proc = subprocess.Popen([sys.executable, "-X", "utf8", bot_script], cwd=os.path.dirname(bot_script), env=env)
            proc.wait()
            print(f"[⚠️ BOT] Exited ({proc.returncode}). Restarting in 5s...", flush=True)
        else:
            print(f"[❌ ERROR] Bot script not found at {bot_script}", flush=True)
        time.sleep(5)

if __name__ == "__main__":
    bootstrap_cloud_home()
    threading.Thread(target=lambda: HTTPServer(("0.0.0.0", PORT), HealthHandler).serve_forever(), daemon=True).start()
    run_direct_telegram_bot()
