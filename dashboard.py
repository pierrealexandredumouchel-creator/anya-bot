from flask import Flask, render_template, jsonify
import subprocess, os

app = Flask(__name__)

@app.route("/")
def home():
    status = subprocess.getoutput("systemctl is-active anya.service")
    return render_template("index.html", status=status)

@app.route("/logs")
def logs():
    log = subprocess.getoutput("tail -n 50 /var/log/anya.log")
    return jsonify({"log": log})

@app.route("/restart")
def restart():
    os.system("systemctl restart anya.service")
    return jsonify({"status": "restarted"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
