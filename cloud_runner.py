import os, sys, time, subprocess, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

def sync_env_file():
    env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env")
    lines = []
    for k, v in os.environ.items():
        if any(p in k for p in ["TOKEN", "KEY", "URL", "ID", "MODEL", "PROXY", "ALLOWED", "CHANNEL", "WURK", "POLYESTER", "ROUTER", "OPENAI", "GROQ", "GEMINI"]):
            lines.append(f"{k}={v}")
    
    tw = os.getenv("TWITTER_BOT_TOKEN") or os.getenv("TELEGRAM_BOT_TOKEN")
    if tw:
        if "TWITTER_BOT_TOKEN=" not in "\n".join(lines): lines.append(f"TWITTER_BOT_TOKEN={tw}")
        if "TELEGRAM_BOT_TOKEN=" not in "\n".join(lines): lines.append(f"TELEGRAM_BOT_TOKEN={tw}")

    ai_url = os.getenv("AI_BASE_URL") or os.getenv("OPENAI_BASE_URL") or os.getenv("ROUTER_BASE_URL")
    if ai_url:
        for u_key in ["AI_BASE_URL", "OPENAI_BASE_URL", "LLM_BASE_URL", "ROUTER_BASE_URL"]:
            lines.append(f"{u_key}={ai_url}")

    ai_key = os.getenv("OPENAI_API_KEY") or os.getenv("ROUTER_API_KEY") or os.getenv("GROQ_API_KEY") or os.getenv("OPENROUTER_API_KEY")
    if ai_key:
        for k_key in ["OPENAI_API_KEY", "ROUTER_API_KEY", "CUSTOM_API_KEY"]:
            lines.append(f"{k_key}={ai_key}")

    with open(env_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"[ENV] Generated {env_path} with {len(lines)} keys.", flush=True)

RUN_TWITTER = os.getenv("ENABLE_TWITTER_BOT", "true").lower() == "true"
RUN_POLYESTER = os.getenv("ENABLE_POLYESTER", "false").lower() == "true"
RUN_WURK = os.getenv("ENABLE_WURK", "false").lower() == "true"
PORT = int(os.getenv("PORT", "8080"))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Cloud Node: ACTIVE 24/7")
    def log_message(self, format, *args): return

def supervise(script):
    while True:
        print(f"[SUPERVISOR] Starting {script}...", flush=True)
        p = subprocess.Popen([sys.executable, "-X", "utf8", script])
        p.wait()
        print(f"[SUPERVISOR] {script} exited ({p.returncode}). Restarting in 10s...", flush=True)
        time.sleep(10)

if __name__ == "__main__":
    sync_env_file()
    threading.Thread(target=lambda: HTTPServer(("0.0.0.0", PORT), HealthHandler).serve_forever(), daemon=True).start()
    if RUN_TWITTER and os.path.exists("twitter_telegram_bot_panel.py"):
        threading.Thread(target=supervise, args=("twitter_telegram_bot_panel.py",), daemon=True).start()
    if RUN_POLYESTER and os.path.exists("polyester_trader.py"):
        threading.Thread(target=supervise, args=("polyester_trader.py",), daemon=True).start()
    if RUN_WURK and os.path.exists("wurk_agent.py"):
        threading.Thread(target=supervise, args=("wurk_agent.py",), daemon=True).start()
    while True: time.sleep(60)
