"""
app.py – Flask application entry point.
Run:  python app.py
"""

import json
import os
import re
import secrets
import time
from collections import defaultdict
from datetime import datetime
from pathlib import Path

from flask import (
    Flask,
    abort,
    jsonify,
    render_template,
    request,
    session,
)

import data

# ── App setup ────────────────────────────────────────────────────────────────
app = Flask(__name__)

# SECRET_KEY: read from environment; fall back to a random key for local dev.
# In production, set the SECRET_KEY environment variable to a long random string.
app.secret_key = os.environ.get("SECRET_KEY") or secrets.token_hex(32)

# ── Security headers ─────────────────────────────────────────────────────────
CSP = (
    "default-src 'self'; "
    "script-src 'self' 'unsafe-inline'; "          # inline JS for canvas/particles
    "style-src 'self' 'unsafe-inline' "
    "https://fonts.googleapis.com "
    "https://unpkg.com; "
    "font-src 'self' "
    "https://fonts.gstatic.com "
    "https://unpkg.com; "
    "img-src 'self' data:; "
    "connect-src 'self'; "
    "frame-ancestors 'none';"
)

@app.after_request
def set_security_headers(response):
    response.headers["Content-Security-Policy"] = CSP
    response.headers["X-Content-Type-Options"]  = "nosniff"
    response.headers["X-Frame-Options"]          = "DENY"
    response.headers["Referrer-Policy"]          = "strict-origin-when-cross-origin"
    return response


# ── In-memory rate limiter ────────────────────────────────────────────────────
# Maps IP → list of Unix timestamps for recent requests.
_rate_store: dict[str, list[float]] = defaultdict(list)
RATE_LIMIT   = 5      # max submissions
RATE_WINDOW  = 600    # seconds (10 minutes)


def _is_rate_limited(ip: str) -> bool:
    now = time.time()
    timestamps = [t for t in _rate_store[ip] if now - t < RATE_WINDOW]
    _rate_store[ip] = timestamps
    if len(timestamps) >= RATE_LIMIT:
        return True
    _rate_store[ip].append(now)
    return False


# ── Helpers ───────────────────────────────────────────────────────────────────
EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
MESSAGES_FILE = Path(__file__).parent / "messages.jsonl"


def _append_message(payload: dict):
    with MESSAGES_FILE.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(payload) + "\n")


# ── Routes ────────────────────────────────────────────────────────────────────
@app.route("/")
def index():
    # Generate a CSRF token and store it in the session.
    if "csrf_token" not in session:
        session["csrf_token"] = secrets.token_hex(32)

    return render_template(
        "index.html",
        owner=data.OWNER,
        roles=data.ROLES,
        socials=data.SOCIALS,
        skills=data.SKILLS,
        learning=data.LEARNING,
        services=data.SERVICES,
        counters=data.COUNTERS,
        projects=data.PROJECTS,
        timeline=data.TIMELINE,
        security_note=data.SECURITY_NOTE,
        csrf_token=session["csrf_token"],
        current_year=datetime.now().year,
    )


@app.route("/contact", methods=["POST"])
def contact():
    # ── CSRF check ────────────────────────────────────────────────────────────
    token = request.form.get("csrf_token", "")
    if not token or token != session.get("csrf_token"):
        return jsonify({"ok": False, "error": "Invalid request (CSRF)."}), 403

    # Rotate token after use
    session["csrf_token"] = secrets.token_hex(32)

    # ── Honeypot ──────────────────────────────────────────────────────────────
    if request.form.get("website", ""):   # bots fill hidden fields
        return jsonify({"ok": True, "message": "Thanks! We'll be in touch."}), 200

    # ── Rate limit ────────────────────────────────────────────────────────────
    ip = request.remote_addr or "unknown"
    if _is_rate_limited(ip):
        return jsonify({"ok": False, "error": "Too many messages. Try again later."}), 429

    # ── Validation ────────────────────────────────────────────────────────────
    full_name = request.form.get("full_name", "").strip()[:120]
    email     = request.form.get("email",     "").strip()[:254]
    subject   = request.form.get("subject",   "").strip()[:200]
    message   = request.form.get("message",   "").strip()[:2000]

    errors = {}
    if len(full_name) < 2:
        errors["full_name"] = "Name must be at least 2 characters."
    if not EMAIL_RE.match(email):
        errors["email"] = "Please enter a valid email address."
    if len(subject) < 2:
        errors["subject"] = "Subject must be at least 2 characters."
    if len(message) < 10:
        errors["message"] = "Message must be at least 10 characters."

    if errors:
        return jsonify({"ok": False, "errors": errors}), 422

    # ── Persist ───────────────────────────────────────────────────────────────
    _append_message({
        "ts":        datetime.utcnow().isoformat(),
        "ip":        ip,
        "full_name": full_name,
        "email":     email,
        "subject":   subject,
        "message":   message,
    })

    return jsonify({"ok": True, "message": "Thanks! I'll get back to you soon."}), 200


# ── Error handlers ────────────────────────────────────────────────────────────
@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html", current_year=datetime.now().year), 404

@app.errorhandler(403)
def forbidden(e):
    return jsonify({"ok": False, "error": "Forbidden."}), 403

@app.errorhandler(429)
def too_many(e):
    return jsonify({"ok": False, "error": "Too many requests."}), 429


# ── Entry point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    import socket
    debug_mode = os.environ.get("FLASK_DEBUG", "0") == "1"

    # Resolve the machine's LAN IP so it can be accessed from phones/tablets
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        lan_ip = s.getsockname()[0]
        s.close()
    except Exception:
        lan_ip = "127.0.0.1"

    print(f"\n  Local:   http://127.0.0.1:5000")
    print(f"  Network: http://{lan_ip}:5000  ← open this on your phone\n")

    # Bind on 0.0.0.0 so all network interfaces are reachable
    app.run(host="0.0.0.0", port=5000, debug=debug_mode)
