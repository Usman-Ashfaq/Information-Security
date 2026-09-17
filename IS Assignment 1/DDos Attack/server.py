from flask import Flask
import time

app = Flask(__name__)

@app.route("/")
def home():
    time.sleep(0.1)
    return "Server is working"

@app.route("/health")
def health():
    return "OK"

app.run(host="0.0.0.0", port=5000)