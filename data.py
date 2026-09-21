# data.py  –  ALL editable content for the portfolio.
# Edit this file to update the site without touching any template or Python logic.

# ── Owner ────────────────────────────────────────────────────────────────────
OWNER = {
    "name": "Blessing Akanni",
    "age": 16,
    "tagline": "Building the web. Breaking it (legally). Defending it.",
    "bio": (
        "I'm Blessing — 16 years old, self-taught, and obsessed with how things "
        "work. I write Python and JavaScript by day, poke at CTF challenges by "
        "night, and believe the best way to defend systems is to understand how "
        "they break. Currently levelling up in Linux, networking, and web security."
    ),
    "email": "blessing@example.com",  # TODO: Blessing to fill
    "location": "Nigeria",             # TODO: Blessing to fill
}

# ── Typing-effect roles ───────────────────────────────────────────────────────
ROLES = [
    "Programmer",
    "Software Engineer",
    "Ethical Hacker",
    "Cybersecurity Learner",
]

# ── Social links (set url to "#" until you have real profiles) ────────────────
# icon: Boxicons class name, e.g. "bx bxl-github"
SOCIALS = [
    {"label": "GitHub",   "icon": "bx bxl-github",   "url": "#"},  # TODO: Blessing to fill
    {"label": "Twitter",  "icon": "bx bxl-twitter",  "url": "#"},  # TODO: Blessing to fill
    {"label": "LinkedIn", "icon": "bx bxl-linkedin",  "url": "#"},  # TODO: Blessing to fill
    {"label": "YouTube",  "icon": "bx bxl-youtube",  "url": "#"},  # TODO: Blessing to fill
]

# ── Skills (progress bars) ────────────────────────────────────────────────────
# percent drives both the label AND the bar width – they can never disagree.
SKILLS = [
    {"name": "HTML",            "percent": 90},
    {"name": "CSS",             "percent": 80},
    {"name": "JavaScript",      "percent": 65},
    {"name": "Python",          "percent": 75},
    {"name": "Web Design",      "percent": 95},
    {"name": "Web Development", "percent": 65},
    {"name": "Graphic Design",  "percent": 85},
    {"name": "SEO Marketing",   "percent": 60},
]

# ── Currently-learning chips (no percentages) ─────────────────────────────────
LEARNING = [
    "Linux",
    "Networking Basics",
    "OWASP Top 10",
    "Git",
    "Secure Coding",
    "Burp Suite",
    "Wireshark",
    "Nmap",
]

# ── What I Do cards ───────────────────────────────────────────────────────────
SERVICES = [
    {
        "icon": "bx bx-code-alt",
        "title": "Programmer",
        "desc": (
            "I write clean, readable code in Python and JavaScript. "
            "I love automating repetitive tasks and building tools that "
            "actually solve real problems."
        ),
    },
    {
        "icon": "bx bx-layer",
        "title": "Software Engineer",
        "desc": (
            "I design and build full-stack web applications — from "
            "database schemas to polished UIs — with a focus on "
            "maintainability and performance."
        ),
    },
    {
        "icon": "bx bx-shield-quarter",
        "title": "Ethical Hacker",
        "desc": (
            "I practise offensive security strictly in legal environments: "
            "CTF competitions, TryHackMe, Hack The Box, and my own home lab. "
            "Understanding attacks is how I learn to prevent them."
        ),
    },
    {
        "icon": "bx bx-lock-alt",
        "title": "Cybersecurity Learner",
        "desc": (
            "Security is built in, not bolted on. I study defensive "
            "techniques — secure coding, OWASP Top 10, and network "
            "monitoring — to write software that's safe from the ground up."
        ),
    },
]

# ── Animated counters ─────────────────────────────────────────────────────────
COUNTERS = [
    {"label": "Projects",      "value": 5,    "suffix": "+"},
    {"label": "Languages",     "value": 5,    "suffix": ""},
    {"label": "CTF / Labs",    "value": 10,   "suffix": "+"},
    {"label": "Hours Coding",  "value": 800,  "suffix": "+"},
]

# ── Projects ──────────────────────────────────────────────────────────────────
# img: filename inside static/img/ (replace project-placeholder.svg with real screenshots)
PROJECTS = [
    {
        "title": "School Management System",
        "desc": (
            "A full desktop-grade web app that handles student enrolment, "
            "class scheduling, grade tracking, and teacher management — "
            "everything a school needs in one clean dashboard. Built to run "
            "offline on school hardware with zero cloud dependency."
        ),
        "tech": ["Python", "Flask", "SQLite", "HTML", "CSS"],
        "img":  "project-placeholder.svg",   # TODO: add screenshot
        "live": "#",                          # TODO: add live / demo link
        "code": "#",                          # TODO: add repo link
    },
    {
        "title": "Church Desktop App",
        "desc": (
            "A desktop application built for a local church to manage "
            "membership records, attendance, tithe logs, and event "
            "announcements. Designed to be simple enough for non-technical "
            "staff to use every Sunday without training."
        ),
        "tech": ["Python", "Tkinter", "SQLite"],
        "img":  "project-placeholder.svg",   # TODO: add screenshot
        "live": "#",
        "code": "#",                          # TODO: add repo link
    },
    {
        "title": "Guest House Management System",
        "desc": (
            "A Django-powered booking and management platform for a guest "
            "house — room availability calendar, guest check-in/check-out, "
            "invoice generation, and an admin dashboard with occupancy "
            "reports. Secure login with role-based access control."
        ),
        "tech": ["Python", "Django", "PostgreSQL", "Bootstrap"],
        "img":  "project-placeholder.svg",   # TODO: add screenshot
        "live": "#",                          # TODO: add live / demo link
        "code": "#",                          # TODO: add repo link
    },
    {
        "title": "Video Call App",
        "desc": (
            "A real-time peer-to-peer video calling application with "
            "room-based sessions. Users create or join a room with a code, "
            "and the app handles signalling, connection negotiation, and "
            "live audio/video streams — all in the browser, no installs."
        ),
        "tech": ["JavaScript", "WebRTC", "Node.js", "Socket.io"],
        "img":  "project-placeholder.svg",   # TODO: add screenshot
        "live": "#",                          # TODO: add live / demo link
        "code": "#",                          # TODO: add repo link
    },
    {
        "title": "This Portfolio",
        "desc": (
            "The very site you're reading — built with Flask, secured with "
            "CSRF protection, rate limiting, and strict CSP headers. "
            "Single-page, mobile-first, zero frameworks. "
            "Every animation is GPU-accelerated and respects prefers-reduced-motion."
        ),
        "tech": ["Python", "Flask", "CSS", "JavaScript"],
        "img":  "project-placeholder.svg",
        "live": "#",
        "code": "#",                          # TODO: add repo link
    },
]

# ── My Journey timeline ───────────────────────────────────────────────────────
TIMELINE = [
    {
        "year":  "2022",
        "title": "The Spark — First Line of Code",
        "desc": (
            "It started with curiosity and a YouTube tutorial. I wrote "
            "my first Python script — a simple calculator — and something "
            "clicked. I stayed up until 2 a.m. just to make it work. "
            "That night changed everything."
        ),
    },
    {
        "year":  "2022",
        "title": "First Website Goes Live",
        "desc": (
            "Months of watching, reading, and breaking things led to my "
            "first real HTML & CSS website. It wasn't perfect — but seeing "
            "it load in a browser for the first time was one of the best "
            "feelings I've ever had. I was hooked on building."
        ),
    },
    {
        "year":  "2023",
        "title": "Python Gets Serious",
        "desc": (
            "I moved beyond scripting and started building real software — "
            "desktop apps with Tkinter, data tools, and automation scripts. "
            "I shipped the Church Desktop App and the School Management "
            "System, both used by real people, which taught me more than "
            "any tutorial ever could."
        ),
    },
    {
        "year":  "2023",
        "title": "Discovered the Web's Dark Side (Ethically)",
        "desc": (
            "A CTF challenge introduced me to cybersecurity. I started on "
            "TryHackMe, learned what SQL injection actually looks like "
            "under the hood, and realised that writing secure code requires "
            "understanding how it breaks. The defensive mindset was born."
        ),
    },
    {
        "year":  "2024",
        "title": "Django, Databases & Real Deployments",
        "desc": (
            "I levelled up from Flask prototypes to Django production apps. "
            "The Guest House Management System was my most complex project "
            "yet — role-based auth, relational data, invoice generation. "
            "I learned that good software is 20% code and 80% thinking."
        ),
    },
    {
        "year":  "2024",
        "title": "Real-Time & WebRTC",
        "desc": (
            "I challenged myself to build something live — a video call app "
            "using WebRTC and Socket.io. Debugging peer connections across "
            "networks was brutally hard and incredibly satisfying. "
            "It taught me networking from the inside out."
        ),
    },
    {
        "year":  "Now",
        "title": "Security + Software — The Full Picture",
        "desc": (
            "At 16, I'm building full-stack applications, practising "
            "ethical hacking in legal labs, and learning that the best "
            "engineers think like attackers. The goal isn't just to build "
            "things — it's to build things that last and can't be broken "
            "by someone who thinks the way I do."
        ),
    },
]

# ── Security note shown in the footer ────────────────────────────────────────
# Only list things that are genuinely implemented in app.py.
SECURITY_NOTE = [
    "CSRF token on every form submission",
    "Honeypot field to block bots",
    "Per-IP rate limiting on contact form (5 / 10 min)",
    "Input validation and length caps server-side",
    "Security headers: CSP, X-Frame-Options, nosniff, Referrer-Policy",
    "No secrets in source code (SECRET_KEY from environment)",
]
