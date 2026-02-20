from flask import Flask
from playwright.sync_api import sync_playwright

import os

app = Flask(__name__)

USERNAME = os.environ.get("LOKALTOG_USER")
PASSWORD = os.environ.get("LOKALTOG_PASS")
BASE_URL = "https://ltcw01.lokaltog.dk"

@app.route("/")
def home():
    return "Automation ready. Use /run"

@app.route("/run")
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        # Go to login page
        page.goto(f"{BASE_URL}/Admin?_m=HTMLAuthenticate")

        # Fill username/password and log in
        page.fill("#loginName", USERNAME)
        page.fill("#loginPassword", PASSWORD)
        page.click("#btnLogin")

        # Wait for admin page to load
        page.wait_for_load_state("networkidle")

        # Click the Tilmeld button
        page.click(".Cmd_Default")  # this is the Tilmeld button

        browser.close()

    return "Tilmeld clicked successfully!"
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
