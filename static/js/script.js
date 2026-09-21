/**
 * script.js  –  Blessing Akanni Portfolio
 * All animations respect prefers-reduced-motion.
 * No external dependencies – plain ES2020.
 */

'use strict';

/* ── helpers ─────────────────────────────────────────────────────────────── */
const $  = (sel, ctx = document) => ctx.querySelector(sel);
const $$ = (sel, ctx = document) => [...ctx.querySelectorAll(sel)];
const reducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

/* ── Scroll-progress bar ──────────────────────────────────────────────────── */
const scrollBar = $('#scroll-progress');

function updateScrollBar() {
  const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
  const pct = scrollHeight === clientHeight
    ? 0
    : (scrollTop / (scrollHeight - clientHeight)) * 100;
  scrollBar.style.width = pct + '%';
}

/* ── Sticky header ────────────────────────────────────────────────────────── */
const header = $('.header');

function updateHeader() {
  header.classList.toggle('scrolled', window.scrollY > 100);
}

/* ── Scroll event (throttled via rAF) ────────────────────────────────────── */
let rafPending = false;

window.addEventListener('scroll', () => {
  if (rafPending) return;
  rafPending = true;
  requestAnimationFrame(() => {
    updateScrollBar();
    updateHeader();
    rafPending = false;
  });
}, { passive: true });

updateScrollBar();
updateHeader();

/* ── Mobile hamburger menu ────────────────────────────────────────────────── */
const hamburger  = $('#hamburger');
const navbar     = $('#navbar');
const navOverlay = $('#nav-overlay');

function openMenu() {
  navbar.classList.add('open');
  navOverlay.classList.add('active');
  hamburger.classList.add('open');
  hamburger.setAttribute('aria-expanded', 'true');
  navOverlay.removeAttribute('aria-hidden');
  document.body.style.overflow = 'hidden';
}

function closeMenu() {
  navbar.classList.remove('open');
  navOverlay.classList.remove('active');
  hamburger.classList.remove('open');
  hamburger.setAttribute('aria-expanded', 'false');
  navOverlay.setAttribute('aria-hidden', 'true');
  document.body.style.overflow = '';
}

hamburger.addEventListener('click', () =>
  hamburger.classList.contains('open') ? closeMenu() : openMenu()
);
navOverlay.addEventListener('click', closeMenu);

// Close on nav link click (mobile)
$$('.nav-link').forEach(link => link.addEventListener('click', closeMenu));

// Keyboard: Escape closes menu
document.addEventListener('keydown', e => {
  if (e.key === 'Escape') closeMenu();
});

/* ── Active nav highlight (scroll spy) ───────────────────────────────────── */
const sections  = $$('section[id]');
const navLinks  = $$('.nav-link');

const spyObserver = new IntersectionObserver(entries => {
  entries.forEach(entry => {
    if (!entry.isIntersecting) return;
    const id = entry.target.getAttribute('id');
    navLinks.forEach(l => {
      l.classList.toggle('active', l.getAttribute('href') === `#${id}`);
    });
  });
}, { rootMargin: '-40% 0px -55% 0px' });

sections.forEach(s => spyObserver.observe(s));

/* ── Reveal-on-scroll (IntersectionObserver) ─────────────────────────────── */
if (reducedMotion) {
  // Make everything visible immediately
  $$('.reveal').forEach(el => el.classList.add('visible'));
} else {
  const revealObs = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      entry.target.classList.add('visible');
      obs.unobserve(entry.target);   // play once
    });
  }, { threshold: 0.12 });

  $$('.reveal').forEach(el => revealObs.observe(el));
}

/* ── Typing effect ────────────────────────────────────────────────────────── */
(function initTyping() {
  const el = $('#typing-text');
  if (!el) return;

  const roles = window.ROLES || ['Programmer'];
  let roleIdx = 0, charIdx = 0, deleting = false;

  function tick() {
    const current = roles[roleIdx];

    if (deleting) {
      charIdx--;
      el.textContent = current.slice(0, charIdx);
      if (charIdx === 0) {
        deleting = false;
        roleIdx  = (roleIdx + 1) % roles.length;
        setTimeout(tick, 500);
        return;
      }
      setTimeout(tick, reducedMotion ? 0 : 60);
    } else {
      charIdx++;
      el.textContent = current.slice(0, charIdx);
      if (charIdx === current.length) {
        deleting = true;
        setTimeout(tick, reducedMotion ? 0 : 2000);
        return;
      }
      setTimeout(tick, reducedMotion ? 0 : 110);
    }
  }

  if (reducedMotion) {
    el.textContent = roles[0];
  } else {
    setTimeout(tick, 800);
  }
}());

/* ── Terminal typewriter (About section) ─────────────────────────────────── */
(function initTerminal() {
  const out = $('#terminal-output');
  if (!out) return;

  const lines = [
    { prompt: true,  text: 'whoami' },
    { prompt: false, text: 'blessing' },
    { prompt: true,  text: 'cat about.txt' },
    { prompt: false, text: '16 years old. Self-taught coder.' },
    { prompt: false, text: 'Loves Python, web dev & security.' },
    { prompt: false, text: 'Learning to build & defend.' },
    { prompt: true,  text: '' },   // blinking cursor line
  ];

  let lineIdx = 0, charIdx = 0;

  function renderLines() {
    out.innerHTML = '';
    for (let i = 0; i < lineIdx; i++) {
      const div  = document.createElement('div');
      const line = lines[i];
      if (line.prompt) {
        div.innerHTML = `<span class="prompt">$</span> ${line.text}`;
      } else {
        div.textContent = line.text;
      }
      out.appendChild(div);
    }
    // current line being typed
    if (lineIdx < lines.length) {
      const line = lines[lineIdx];
      const div  = document.createElement('div');
      const partial = line.text.slice(0, charIdx);
      if (line.prompt) {
        div.innerHTML = `<span class="prompt">$</span> ${partial}<span class="cursor">|</span>`;
      } else {
        div.innerHTML = `${partial}<span class="cursor">|</span>`;
      }
      out.appendChild(div);
    }
  }

  // Only start when the about section is visible
  const aboutSec = $('#about');
  let started = false;

  function startTerminal() {
    if (started) return;
    started = true;

    if (reducedMotion) {
      lines.forEach(l => {
        const div = document.createElement('div');
        div.innerHTML = l.prompt
          ? `<span class="prompt">$</span> ${l.text}`
          : l.text;
        out.appendChild(div);
      });
      return;
    }

    function type() {
      if (lineIdx >= lines.length) return;
      const line = lines[lineIdx];
      if (charIdx < line.text.length) {
        charIdx++;
        renderLines();
        setTimeout(type, 65);
      } else {
        lineIdx++;
        charIdx = 0;
        renderLines();
        setTimeout(type, lineIdx < lines.length ? 350 : 0);
      }
    }
    setTimeout(type, 600);
  }

  const termObs = new IntersectionObserver(entries => {
    if (entries[0].isIntersecting) {
      startTerminal();
      termObs.disconnect();
    }
  }, { threshold: 0.3 });

  if (aboutSec) termObs.observe(aboutSec);
}());

/* ── Animated counters ────────────────────────────────────────────────────── */
(function initCounters() {
  const items = $$('.counter-value');
  if (!items.length) return;

  function animateCounter(el) {
    const target = parseInt(el.dataset.target, 10);
    const suffix = el.dataset.suffix || '';
    if (reducedMotion) { el.textContent = target + suffix; return; }

    const duration = 1500;
    const start    = performance.now();

    function step(now) {
      const elapsed = now - start;
      const progress = Math.min(elapsed / duration, 1);
      // ease-out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.round(eased * target) + suffix;
      if (progress < 1) requestAnimationFrame(step);
    }
    requestAnimationFrame(step);
  }

  const ctrObs = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      animateCounter(entry.target);
      obs.unobserve(entry.target);
    });
  }, { threshold: 0.5 });

  items.forEach(el => ctrObs.observe(el));
}());

/* ── Skill-bar fill animation ─────────────────────────────────────────────── */
(function initSkillBars() {
  const fills = $$('.skill-fill');
  if (!fills.length) return;

  const barObs = new IntersectionObserver((entries, obs) => {
    entries.forEach(entry => {
      if (!entry.isIntersecting) return;
      const fill = entry.target;
      if (reducedMotion) {
        fill.style.width = fill.dataset.width + '%';
      } else {
        // small delay so the transition is visible after reveal
        requestAnimationFrame(() => {
          fill.style.width = fill.dataset.width + '%';
        });
      }
      obs.unobserve(entry.target);
    });
  }, { threshold: 0.3 });

  fills.forEach(el => barObs.observe(el));
}());

/* ── Tilt / lift on project cards ─────────────────────────────────────────── */
(function initTilt() {
  if (reducedMotion) return;
  $$('.tilt-card').forEach(card => {
    card.addEventListener('mousemove', e => {
      const rect   = card.getBoundingClientRect();
      const cx     = rect.left + rect.width  / 2;
      const cy     = rect.top  + rect.height / 2;
      const dx     = (e.clientX - cx) / (rect.width  / 2);
      const dy     = (e.clientY - cy) / (rect.height / 2);
      const rotX   = -dy * 6;
      const rotY   =  dx * 6;
      card.style.transform = `translateY(-6px) rotateX(${rotX}deg) rotateY(${rotY}deg)`;
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = '';
    });
  });
}());

/* ── Hero canvas: particle network ───────────────────────────────────────── */
(function initCanvas() {
  const canvas = $('#hero-canvas');
  if (!canvas) return;

  // Disable on small screens for performance
  if (window.innerWidth < 768 || reducedMotion) {
    canvas.style.display = 'none';
    return;
  }

  const ctx  = canvas.getContext('2d');
  const CYAN = '#00abf0';
  const N    = 60;   // particle count

  let W, H, particles, raf;

  function resize() {
    const home = canvas.closest('.home') || canvas.parentElement;
    W = canvas.width  = home.offsetWidth;
    H = canvas.height = home.offsetHeight;
  }

  class Particle {
    constructor() { this.reset(); }
    reset() {
      this.x  = Math.random() * W;
      this.y  = Math.random() * H;
      this.vx = (Math.random() - 0.5) * 0.5;
      this.vy = (Math.random() - 0.5) * 0.5;
      this.r  = Math.random() * 2 + 1;
    }
    update() {
      this.x += this.vx;
      this.y += this.vy;
      if (this.x < 0 || this.x > W) this.vx *= -1;
      if (this.y < 0 || this.y > H) this.vy *= -1;
    }
    draw() {
      ctx.beginPath();
      ctx.arc(this.x, this.y, this.r, 0, Math.PI * 2);
      ctx.fillStyle = CYAN;
      ctx.globalAlpha = 0.5;
      ctx.fill();
      ctx.globalAlpha = 1;
    }
  }

  function init() {
    resize();
    particles = Array.from({ length: N }, () => new Particle());
  }

  function drawLines() {
    for (let i = 0; i < particles.length; i++) {
      for (let j = i + 1; j < particles.length; j++) {
        const dx   = particles[i].x - particles[j].x;
        const dy   = particles[i].y - particles[j].y;
        const dist = Math.hypot(dx, dy);
        if (dist < 130) {
          ctx.beginPath();
          ctx.moveTo(particles[i].x, particles[i].y);
          ctx.lineTo(particles[j].x, particles[j].y);
          ctx.strokeStyle = CYAN;
          ctx.globalAlpha = 1 - dist / 130;
          ctx.lineWidth   = 0.5;
          ctx.stroke();
          ctx.globalAlpha = 1;
        }
      }
    }
  }

  function loop() {
    ctx.clearRect(0, 0, W, H);
    particles.forEach(p => { p.update(); p.draw(); });
    drawLines();
    raf = requestAnimationFrame(loop);
  }

  // Pause when tab is hidden
  document.addEventListener('visibilitychange', () => {
    if (document.hidden) {
      cancelAnimationFrame(raf);
    } else {
      raf = requestAnimationFrame(loop);
    }
  });

  window.addEventListener('resize', () => {
    resize();
    particles.forEach(p => p.reset());
  }, { passive: true });

  init();
  loop();
}());

/* ── Contact form (fetch + CSRF + toast) ─────────────────────────────────── */
(function initContactForm() {
  const form      = $('#contact-form');
  const toast     = $('#toast');
  const submitBtn = $('#submit-btn');
  if (!form) return;

  function showToast(msg, isError = false) {
    toast.textContent = msg;
    toast.classList.toggle('error', isError);
    toast.classList.add('show');
    setTimeout(() => toast.classList.remove('show'), 4500);
  }

  function clearErrors() {
    $$('.field-error', form).forEach(el => el.textContent = '');
    $$('input, textarea', form).forEach(el => el.removeAttribute('aria-invalid'));
  }

  function showErrors(errors) {
    Object.entries(errors).forEach(([field, msg]) => {
      const el = $(`#err-${field}`, form);
      const inp = $(`#${field}`, form);
      if (el)  el.textContent = msg;
      if (inp) {
        inp.setAttribute('aria-invalid', 'true');
        inp.focus();
      }
    });
  }

  form.addEventListener('submit', async e => {
    e.preventDefault();
    clearErrors();

    submitBtn.disabled    = true;
    submitBtn.textContent = 'Sending…';

    try {
      const resp = await fetch('/contact', {
        method:  'POST',
        body:    new FormData(form),
        headers: { 'X-Requested-With': 'XMLHttpRequest' },
      });

      const data = await resp.json();

      if (data.ok) {
        showToast(data.message || 'Message sent!');
        form.reset();
        // Update CSRF token returned in next page load is not needed;
        // server rotates it in session; next submit will fail if they
        // submit without reloading, so we reload the token via a hidden
        // approach: fetch the token from the page's hidden field won't
        // work after reset. We just refresh the token from the server.
        // Simple approach: refresh CSRF from a quick GET
        refreshCsrfToken();
      } else if (data.errors) {
        showErrors(data.errors);
        showToast('Please fix the highlighted fields.', true);
      } else {
        showToast(data.error || 'Something went wrong.', true);
      }
    } catch (err) {
      showToast('Network error. Please try again.', true);
    } finally {
      submitBtn.disabled    = false;
      submitBtn.innerHTML   = 'Send Message <i class="bx bx-send" aria-hidden="true"></i>';
    }
  });

  async function refreshCsrfToken() {
    try {
      const r    = await fetch('/');
      const text = await r.text();
      const match = text.match(/name="csrf_token" value="([a-f0-9]+)"/);
      if (match) {
        const field = $('input[name="csrf_token"]', form);
        if (field) field.value = match[1];
      }
    } catch (_) { /* best-effort */ }
  }
}());
