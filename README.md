# Blessing Akanni – Portfolio

Personal portfolio built with Flask. Clean, mobile-first, single-page.

---

## Quick Start (Windows)

```powershell
# 1. Create and activate a virtual environment
python -m venv venv
venv\Scripts\activate

# 2. Install dependencies (Flask only)
pip install -r requirements.txt

# 3. Run the development server
python app.py
```

Open **http://127.0.0.1:5000** in your browser.

To stop the server press `Ctrl + C`.

---

## Project Structure

```
portfolio/
  app.py               Flask app, routes, security, contact endpoint
  data.py              ← EDIT THIS to update all site content
  requirements.txt     Flask==3.1.3
  messages.jsonl       Contact messages (created at runtime, git-ignored)
  templates/
    base.html          Shared layout (nav, footer, scripts)
    index.html         All page sections
    404.html           Custom 404 error page
  static/
    css/style.css      All styles (mobile-first)
    js/script.js       Animations, typing effect, canvas, contact form
    img/               Profile photos + project screenshots
  tests/
    test_app.py        Flask test-client suite
```

---

## How to Edit Content

**All editable content lives in `data.py`.**  
Open it and look for the sections below. Lines marked `# TODO: Blessing to fill`
are placeholders that need your real information.

| Variable     | What it controls                          |
|--------------|-------------------------------------------|
| `OWNER`      | Your name, bio, email, location           |
| `ROLES`      | Words that cycle in the typing effect     |
| `SOCIALS`    | Social media links and icons              |
| `SKILLS`     | Skill names and percentage values         |
| `LEARNING`   | "Currently learning" chip labels          |
| `SERVICES`   | "What I Do" card titles and descriptions  |
| `COUNTERS`   | Animated counter numbers (projects, etc.) |
| `PROJECTS`   | Project cards (title, desc, tech, links)  |
| `TIMELINE`   | "My Journey" timeline entries             |
| `SECURITY_NOTE` | Footer security note bullets           |

---

## Adding a Project

1. Add a screenshot image to `static/img/` (e.g. `my-project.png`).
2. Find the `PROJECTS` list in `data.py`.
3. Edit one of the placeholder entries:

```python
{
    "title": "My Awesome Project",
    "desc":  "A brief description of what it does.",
    "tech":  ["Python", "Flask", "SQLite"],
    "img":   "my-project.png",      # filename inside static/img/
    "live":  "https://your-live-url.com",
    "code":  "https://github.com/you/repo",
},
```

---

## Running Tests

```powershell
# Inside the venv, from the project root
pip install pytest
python -m pytest tests/ -v
```

---

## Production Notes

- Set the `SECRET_KEY` environment variable to a long random string before deploying.
- Set `FLASK_DEBUG=0` (or leave unset) in production — debug mode is off by default.
- `messages.jsonl` stores contact form submissions locally. Back it up or swap
  `_append_message()` in `app.py` for email/database storage.
- Add a proper WSGI server (e.g. Gunicorn on Linux, Waitress on Windows) for production.

---

## Ethical Hacking Disclaimer

Security practice on this site refers exclusively to legal environments:
CTF competitions, TryHackMe, Hack The Box, personal home labs, and
responsible disclosure programmes. No exploit code, no real targets.
