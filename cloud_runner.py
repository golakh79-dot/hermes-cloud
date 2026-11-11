import os, sys, time, subprocess, threading
from http.server import HTTPServer, BaseHTTPRequestHandler

RUN_TWITTER = os.getenv("ENABLE_TWITTER_BOT", "true").lower() == "true"
RUN_POLYESTER = os.getenv("ENABLE_POLYESTER", "false").lower() == "true"
RUN_WURK = os.getenv("ENABLE_WURK", "false").lower() == "true"
PORT = int(os.getenv("PORT", "8080"))

class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hermes Cloud Node: ACTIVE 24/7")
    def log_message(self, format, *args):
        return

def start_health_server():
    HTTPServer(("0.0.0.0", PORT), HealthHandler).serve_forever()

def supervise_script(script_name):
    while True:
        proc = subprocess.Popen([sys.executable, "-X", "utf8", script_name])
        proc.wait()
        time.sleep(10)

if __name__ == "__main__":
    threading.Thread(target=start_health_server, daemon=True).start()
    if RUN_TWITTER and os.path.exists("twitter_telegram_bot_panel.py"):
        threading.Thread(target=supervise_script, args=("twitter_telegram_bot_panel.py",), daemon=True).start()
    if RUN_POLYESTER and os.path.exists("polyester_trader.py"):
        threading.Thread(target=supervise_script, args=("polyester_trader.py",), daemon=True).start()
    if RUN_WURK and os.path.exists("wurk_agent.py"):
        threading.Thread(target=supervise_script, args=("wurk_agent.py",), daemon=True).start()
    while True:
        time.sleep(60)
