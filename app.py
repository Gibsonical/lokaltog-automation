import os
from flask import Flask
from playwright.sync_api import sync_playwright

app = Flask(__name__)

# Read credentials from Render environment variables
USERNAME = os.environ.get("LT_USERNAME")
PASSWORD = os.environ.get("LT_PASSWORD")

TARGET_URL = "https://ltcw01.lokaltog.dk"

@app.route("/run", methods=["GET"])
def run_automation():
    if not USERNAME or not PASSWORD:
        return "Error: Missing environment variables."

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )
            page = browser.new_page()

            # Go to login page
            page.goto(TARGET_URL, timeout=60000)

            # Fill login form
            page.fill("input[type='text']", USERNAME)
            page.fill("input[type='password']", PASSWORD)

            # Click login button
            page.click("#btnLogin")

            # Wait until page fully loads after login
            page.wait_for_load_state("networkidle")

            # Wait for Tilmeld button to appear
            page.wait_for_selector("button:has-text('Tilmeld')", timeout=30000)

            # Click Tilmeld
            page.click("button:has-text('Tilmeld')")

            browser.close()

        return "Success"

    except Exception as e:
        return f"Error: {str(e)}"
