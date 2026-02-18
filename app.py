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

            # ---- LOGIN SECTION ----
            page.fill("input[type='text']", USERNAME)
            page.fill("input[type='password']", PASSWORD)
            page.click("button[type='submit']")

            page.wait_for_load_state("networkidle")

            # ---- CLICK TARGET BUTTON ----
            # You will update this selector later once we inspect the page
            page.click("button#targetButton")

            browser.close()

        return "Success"

    except Exception as e:
        return f"Error: {str(e)}"
