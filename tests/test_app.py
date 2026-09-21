"""
tests/test_app.py  –  Flask test-client suite for the portfolio.

Run:  python -m pytest tests/ -v
      (from the project root, inside the venv)
"""

import json
import sys
import os

# Ensure project root is on the path when running from tests/
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    flask_app.config['WTF_CSRF_ENABLED'] = False  # we test CSRF manually
    with flask_app.test_client() as c:
        yield c


# ── §1  GET / returns 200 and key sections ──────────────────────────────────
def test_homepage_ok(client):
    r = client.get('/')
    assert r.status_code == 200
    body = r.data.decode()
    assert 'Blessing Akanni' in body
    assert 'id="home"'     in body
    assert 'id="about"'    in body
    assert 'id="skills"'   in body
    assert 'id="contact"'  in body


# ── §2  Static assets are served ────────────────────────────────────────────
def test_static_css(client):
    r = client.get('/static/css/style.css')
    assert r.status_code == 200
    assert b'--bg:' in r.data


def test_static_js(client):
    r = client.get('/static/js/script.js')
    assert r.status_code == 200
    assert b'initTyping' in r.data


def test_static_svg(client):
    r = client.get('/static/img/project-placeholder.svg')
    assert r.status_code == 200


# ── §3  404 custom page ──────────────────────────────────────────────────────
def test_404_page(client):
    r = client.get('/this-page-does-not-exist')
    assert r.status_code == 404
    body = r.data.decode()
    assert '404' in body
    assert 'Back to Home' in body


# ── §4  POST /contact – missing CSRF token → 403 ────────────────────────────
def test_contact_missing_csrf(client):
    r = client.post('/contact', data={
        'full_name': 'Alice',
        'email':     'alice@example.com',
        'subject':   'Hi',
        'message':   'This is a test message with enough length.',
        # csrf_token intentionally omitted
    })
    assert r.status_code == 403
    body = json.loads(r.data)
    assert body['ok'] is False


# ── §5  POST /contact – wrong CSRF token → 403 ──────────────────────────────
def test_contact_wrong_csrf(client):
    # First visit to get a real session
    client.get('/')
    r = client.post('/contact', data={
        'full_name':  'Bob',
        'email':      'bob@example.com',
        'subject':    'Test',
        'message':    'Another test message long enough.',
        'csrf_token': 'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
    })
    assert r.status_code == 403


# ── §6  POST /contact – honeypot filled → silently OK (bot trap) ─────────────
def test_contact_honeypot(client):
    # Get a real CSRF token first
    r_get = client.get('/')
    body  = r_get.data.decode()
    import re
    m = re.search(r'name="csrf_token" value="([a-f0-9]+)"', body)
    assert m, "CSRF token not found in page HTML"
    token = m.group(1)

    r = client.post('/contact', data={
        'full_name':  'Botty McBot',
        'email':      'bot@spam.com',
        'subject':    'Buy now',
        'message':    'Click this link to win a prize!',
        'csrf_token': token,
        'website':    'http://spam.example.com',  # honeypot filled
    })
    assert r.status_code == 200
    body = json.loads(r.data)
    # Server responds OK to fool the bot, but nothing is stored
    assert body['ok'] is True


# ── §7  POST /contact – short / invalid fields → 422 ────────────────────────
def test_contact_invalid_fields(client):
    r_get = client.get('/')
    body  = r_get.data.decode()
    import re
    m = re.search(r'name="csrf_token" value="([a-f0-9]+)"', body)
    token = m.group(1)

    r = client.post('/contact', data={
        'full_name':  'A',            # too short
        'email':      'not-an-email', # invalid
        'subject':    'X',            # too short
        'message':    'short',        # too short
        'csrf_token': token,
        'website':    '',
    })
    assert r.status_code == 422
    data = json.loads(r.data)
    assert data['ok'] is False
    assert 'errors' in data
    assert 'full_name' in data['errors']
    assert 'email'     in data['errors']
    assert 'subject'   in data['errors']
    assert 'message'   in data['errors']


# ── §8  POST /contact – valid submission → 200 ──────────────────────────────
def test_contact_valid(client, tmp_path, monkeypatch):
    import pathlib
    # Redirect message storage to a temp file
    tmp_file = tmp_path / 'messages.jsonl'
    monkeypatch.setattr('app.MESSAGES_FILE', tmp_file)

    r_get = client.get('/')
    body  = r_get.data.decode()
    import re
    m = re.search(r'name="csrf_token" value="([a-f0-9]+)"', body)
    token = m.group(1)

    r = client.post('/contact', data={
        'full_name':  'Blessing Tester',
        'email':      'test@example.com',
        'subject':    'Hello there',
        'message':    'This is a valid test message, long enough to pass.',
        'csrf_token': token,
        'website':    '',
    })
    assert r.status_code == 200
    data = json.loads(r.data)
    assert data['ok'] is True

    # Check the message was written to the file
    lines = tmp_file.read_text().strip().splitlines()
    assert len(lines) == 1
    saved = json.loads(lines[0])
    assert saved['full_name'] == 'Blessing Tester'
    assert saved['email']     == 'test@example.com'
