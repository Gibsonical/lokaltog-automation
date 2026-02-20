from flask import Flask
import requests
import re

app = Flask(__name__)

BASE_URL = "https://ltcw01.lokaltog.dk"
LOGIN_URL = BASE_URL + "/Admin?_m=HTMLAuthenticate"

USERNAME = "24335"
PASSWORD = "1955"

@app.route("/")
def home():
    return "Use /run"

@app.route("/run")
def run():
    try:
        with requests.Session() as session:

            # 1️⃣ Load login page
            session.get(BASE_URL)

            # 2️⃣ Login
            login_payload = {
                "username": USERNAME,
                "password": PASSWORD,
                "loginScreenMode": "0",
                "login": "Logon"
            }

            login_response = session.post(LOGIN_URL, data=login_payload)

            if "Logon" in login_response.text:
                return "Login failed"

            # 3️⃣ Load admin page to get dynamic values
            admin_page = session.get(BASE_URL + "/Admin")
            html = admin_page.text

            # Extract _s value
            s_match = re.search(r"_s:\s*'([^']+)'", html)
            pid_match = re.search(r"_pid:\s*'([^']+)'", html)

            if not s_match or not pid_match:
                return "Could not extract session values"

            s_value = s_match.group(1)
            pid_value = pid_match.group(1)

            # 4️⃣ Send Tilmeld request
            tilmeld_payload = {
                "_evn": "0",
                "_m": "ProcessRequest",
                "_s": s_value,
                "_pid": pid_value,
                "_evq": "7",
                "_times": "",
                "_focus": pid_value,
                "_fragment": f"{pid_value},attend,0,0",
                "_evm": "2"
            }

            response = session.post(BASE_URL + "/Admin", data=tilmeld_payload)

            return "Tilmeld request sent successfully"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run()
