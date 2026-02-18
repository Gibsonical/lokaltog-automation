from flask import Flask
import requests

app = Flask(__name__)

LOGIN_URL = "https://ltcw01.lokaltog.dk/Admin?_m=HTMLAuthenticate"
BASE_URL = "https://ltcw01.lokaltog.dk"

USERNAME = "24335"
PASSWORD = "1955"

@app.route("/")
def home():
    return "Automation running. Use /run"

@app.route("/run")
def run():
    try:
        with requests.Session() as session:

            # Step 1 – Load login page to get cookies
            session.get(BASE_URL)

            # Step 2 – Login
            login_payload = {
                "username": USERNAME,
                "password": PASSWORD,
                "loginScreenMode": "0",
                "login": "Logon"
            }

            response = session.post(LOGIN_URL, data=login_payload)

            if "Logon" in response.text:
                return "Login failed"

            # Step 3 – Click the Tilmeld button
            # This button triggers:
            # fe(event||target,1000009,{type:'1',step:'request'})

            tilmeld_payload = {
                "_m": "HTMLRequest",
                "commandId": "1000009",
                "type": "1",
                "step": "request"
            }

            tilmeld_response = session.post(BASE_URL + "/Admin", data=tilmeld_payload)

            return "Success – Tilmeld triggered!"

    except Exception as e:
        return f"Error: {str(e)}"

if __name__ == "__main__":
    app.run()
