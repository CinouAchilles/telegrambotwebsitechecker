from playwright.sync_api import sync_playwright
from dotenv import load_dotenv
import requests
import os
import time
import subprocess

# Load environment variables
load_dotenv()

URL = os.getenv("URL")
TG_TOKEN = os.getenv("TG_TOKEN")
TG_CHAT_ID = os.getenv("TG_CHAT_ID")
KEYWORD = os.getenv("KEYWORD")
ERROR_KEYWORD = os.getenv("ERROR_KEYWORD")
SUCCESS_KEYWORD = os.getenv("SUCCESS_KEYWORD")

CHECK_INTERVAL = 900  # seconds (15 minutes)

if os.path.exists("/.dockerenv"):
    # Keep browser binaries in a stable location inside Docker containers.
    os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/ms-playwright")

# Validate required environment variables
if not all([URL, TG_TOKEN, TG_CHAT_ID, KEYWORD]):
    raise ValueError("Missing required environment variables. Please check .env file.")

def send_telegram(msg):
    if not msg:
        return

    try:
        response = requests.post(
            f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage",
            json={"chat_id": TG_CHAT_ID, "text": msg},
            timeout=10
        )
        response.raise_for_status()
    except Exception as e:
        print("Telegram error:", e)

alert_active = True  # assumes keyword exists initially

def check_site(page):
    global alert_active

    print(time.strftime("%Y-%m-%d %H:%M:%S"), "Checking...")

    try:
        page.goto(URL, timeout=30000)
        # Wait until network is idle, more reliable than fixed timeout
        page.wait_for_load_state("networkidle")
    except Exception as e:
        print("Page load error:", e)
        return

    html = page.content()
    print("Length:", len(html))

    # Case-insensitive keyword search
    if KEYWORD.lower() in html.lower():
        send_telegram(ERROR_KEYWORD or f"Keyword detected again at {URL}")
        alert_active = True
    else:
        if alert_active:
            success_message = SUCCESS_KEYWORD or "Keyword no longer found"
            print(success_message)
            send_telegram(
                f"{success_message}\n{URL}"
            )
            alert_active = False
        else:
            print("No change")


def launch_chromium_with_recovery(playwright):
    for attempt in range(2):
        try:
            return playwright.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
        except Exception as e:
            is_first_attempt = attempt == 0
            missing_browser = "Executable doesn't exist" in str(e)

            if is_first_attempt and missing_browser:
                print("Chromium executable missing. Installing Chromium and retrying...")
                subprocess.run(["python", "-m", "playwright", "install", "chromium"], check=True)
                continue

            raise

if __name__ == "__main__":
    send_telegram("🟢 bot started!")

    with sync_playwright() as p:
        browser = launch_chromium_with_recovery(p)
        page = browser.new_page()

        while True:
            try:
                check_site(page)
            except Exception as e:
                print("Error:", e)
                send_telegram(f"⚠️ Bot error: {e}")

            time.sleep(CHECK_INTERVAL)