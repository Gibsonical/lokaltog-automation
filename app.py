import os
from flask import Flask, request
from playwright.sync_api import sync_playwright

app = Flask(__name__)

USERNAME = os.environ.get("LT_USERNAME")
PASSWORD = os.environ.get("LT_PASSWORD")

TARGET_URL = "https://ltcw01.lokaltog.dk"

@app.route("/run", methods=["GET"])
def run_automation():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(TARGET_URL)

# Fill login form
page.fill("input[type='text']", USERNAME)
page.fill("input[type='password']", PASSWORD)

# Click login button using ID
page.click("#btnLogin")

page.wait_for_load_state("networkidle")

            browser.close()

        return "Success"

    except Exception as e:
        return f"Error: {str(e)}"
