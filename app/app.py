from flask import Flask, render_template
import os
import socket

app = Flask(__name__)

@app.route("/")
def index():
    hostname = socket.gethostname()
    version  = os.getenv("APP_VERSION", "1.0.0")
    return render_template("index.html", hostname=hostname, version=version)

@app.route("/health")
def health():
    return {"status": "healthy"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
