import os
import requests
from flask import Flask

app = Flask(__name__)

USERNAME = os.environ.get("LT_USERNAME")
PASSWORD = os.environ.get("LT_PASSWORD")

BASE_URL = "https://ltcw01.lokaltog.dk"

@app.route("/")
def home():
    return "Service running"

@app.route("/run", methods=["GET"])
def run_automation():
    if not USERNAME or not PASSWORD:
        return "Missing credentials"

    try:
        with requests.Session() as session:

            # Step 1: Get login page (to get cookies)
            session.get(BASE_URL)

            # Step 2: Login
            login_payload = {
                "username": USERNAME,
                "password": PASSWORD,
                "login": "Logon"
            }

            login_response = session.post(BASE_URL, data=login_payload)

            if login_response.status_code != 200:
                return "Login failed"

            # Step 3: Trigger Tilmeld action
            tilmeld_payload = {
                "type": "1",
                "step": "request"
            }

            response = session.post(BASE_URL, data=tilmeld_payload)

            if response.status_code == 200:
                return "Success"
            else:
                return "Tilmeld failed"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
