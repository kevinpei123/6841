#!/usr/bin/env python3
from flask import Flask, request, make_response
import os

app = Flask(__name__)

@app.after_request
def add_csp(resp):
    resp.headers['Content-Security-Policy'] = "default-src 'self'; script-src 'self'"
    return resp

@app.route("/")
def index():
    q = request.args.get("q", "")
    safe = q.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
    page = (
        "<h3>Search</h3>"
        "<form>"
          "<input name=q value=\"" + safe + "\">"
          "<button>go</button>"
        "</form>"
        "<script>"
          "let query = \"" + q + "\";"
          "console.log('User searched:', query);"
        "</script>"
    )
    return page

@app.route("/admin")
def admin():
    FLAG = os.getenv("FLAG") or "flag{xss_csp}"
    resp = make_response("admin panel")
    resp.headers['Set-Cookie'] = "flag=" + FLAG + "; Path=/; Secure"
    return resp

@app.route("/c")
def collect():
    stolen = request.args.get("c")
    print("Stolen: " + stolen)
    return "ok"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
