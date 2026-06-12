/* ==========================================================================
   mogrov.com — shared behavior
   Defensive: every feature guards for missing elements so this one file
   works on index.html, founder.html and the blog pages.
   ========================================================================== */
(function () {
  'use strict';

  /* ---- Theme toggle (persisted across pages) ----
     An inline <head> snippet sets the initial class before paint to avoid
     a flash; here we wire the toggle button and keep localStorage in sync. */
  var THEME_KEY = 'mogrov-theme';
  function currentTheme() {
    return document.documentElement.classList.contains('dark') ? 'dark' : 'light';
  }
  function applyTheme(theme) {
    var root = document.documentElement;
    root.classList.toggle('dark', theme === 'dark');
    root.classList.toggle('light', theme !== 'dark');
    try { localStorage.setItem(THEME_KEY, theme); } catch (e) {}
  }
  function wireThemeToggles() {
    var btns = document.querySelectorAll('[data-theme-toggle]');
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        applyTheme(currentTheme() === 'dark' ? 'light' : 'dark');
      });
    });
  }

  /* ---- Mobile menu ---- */
  function wireMobileMenu() {
    var btn = document.querySelector('[data-menu-toggle]');
    var menu = document.querySelector('[data-mobile-menu]');
    if (!btn || !menu) return;
    btn.addEventListener('click', function () {
      menu.classList.toggle('hidden');
    });
    menu.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { menu.classList.add('hidden'); });
    });
  }

  /* ---- Scroll reveal ---- */
  function wireReveal() {
    var items = document.querySelectorAll('.reveal');
    if (!items.length) return;
    if (!('IntersectionObserver' in window)) {
      items.forEach(function (el) { el.classList.add('is-visible'); });
      return;
    }
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.12, rootMargin: '0px 0px -8% 0px' });
    items.forEach(function (el) { io.observe(el); });
  }

  /* ---- Active nav link on scroll (single-scroll home only) ---- */
  function wireScrollSpy() {
    var links = document.querySelectorAll('[data-spy]');
    if (!links.length) return;
    var sections = [];
    links.forEach(function (l) {
      var id = l.getAttribute('data-spy');
      var sec = document.getElementById(id);
      if (sec) sections.push({ id: id, el: sec, link: l });
    });
    if (!sections.length) return;
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          links.forEach(function (l) { l.classList.remove('active'); });
          var match = sections.find(function (s) { return s.el === entry.target; });
          if (match) match.link.classList.add('active');
        }
      });
    }, { threshold: 0.5 });
    sections.forEach(function (s) { io.observe(s.el); });
  }

  /* ---- Terminal install simulation ---- */
  function runTerminalSimulation() {
    var textEl = document.getElementById('terminal-text');
    var outEl = document.getElementById('terminal-output');
    if (!textEl || !outEl) return;
    var full = textEl.getAttribute('data-type') || 'pip install runtime-narrative';
    var i = 0;
    textEl.textContent = '';
    outEl.style.opacity = '0';
    (function type() {
      if (i < full.length) {
        textEl.textContent += full[i++];
        setTimeout(type, 70);
      } else {
        setTimeout(function () { outEl.style.opacity = '1'; }, 450);
      }
    })();
  }

  /* ---- Rotating "protocol" label ---- */
  function runProtocolAnimation() {
    var el = document.getElementById('protocol-text');
    if (!el) return;
    var values = ['built_for_developers', 'solving_friction', 'offline_first', 'bottom_up'];
    var vIdx = 0, charIdx = 0, deleting = false;
    (function tick() {
      var cur = values[vIdx];
      if (!deleting) {
        el.textContent = cur.substring(0, charIdx + 1); charIdx++;
        if (charIdx === cur.length) { deleting = true; setTimeout(tick, 1800); }
        else setTimeout(tick, 90);
      } else {
        el.textContent = cur.substring(0, charIdx - 1); charIdx--;
        if (charIdx === 0) { deleting = false; vIdx = (vIdx + 1) % values.length; setTimeout(tick, 450); }
        else setTimeout(tick, 45);
      }
    })();
  }

  /* ---- Contact form (Web3Forms) ----
     Set your access key on the form via data-access-key (see index.html).
     Submits via fetch with no page reload; shows inline status. */
  function wireContactForm() {
    var form = document.querySelector('[data-contact-form]');
    if (!form) return;
    var statusEl = form.querySelector('[data-form-status]');
    var submitBtn = form.querySelector('button[type="submit"]');
    var key = form.getAttribute('data-access-key') || '';

    function setStatus(msg, kind) {
      if (!statusEl) return;
      statusEl.textContent = msg;
      statusEl.style.color = kind === 'error' ? '#f7768e' : (kind === 'ok' ? '#9ece6a' : 'var(--muted)');
    }

    form.addEventListener('submit', function (e) {
      e.preventDefault();
      if (!key || key.indexOf('YOUR_WEB3FORMS') === 0) {
        setStatus('Form not configured yet — add your Web3Forms access key.', 'error');
        return;
      }
      var data = new FormData(form);
      data.append('access_key', key);
      var original = submitBtn ? submitBtn.textContent : '';
      if (submitBtn) { submitBtn.disabled = true; submitBtn.textContent = 'Sending…'; }
      setStatus('Sending…', 'info');

      fetch('https://api.web3forms.com/submit', {
        method: 'POST',
        headers: { Accept: 'application/json' },
        body: data,
      })
        .then(function (r) { return r.json(); })
        .then(function (json) {
          if (json.success) {
            form.reset();
            setStatus('Message sent — thanks, we’ll be in touch.', 'ok');
          } else {
            setStatus(json.message || 'Something went wrong. Email admin@mogrov.com instead.', 'error');
          }
        })
        .catch(function () {
          setStatus('Network error. Email admin@mogrov.com instead.', 'error');
        })
        .finally(function () {
          if (submitBtn) { submitBtn.disabled = false; submitBtn.textContent = original; }
        });
    });
  }

  /* ---- Boot ---- */
  function boot() {
    if (window.lucide && typeof window.lucide.createIcons === 'function') {
      window.lucide.createIcons();
    }
    wireThemeToggles();
    wireMobileMenu();
    wireReveal();
    wireScrollSpy();
    wireContactForm();
    runTerminalSimulation();
    runProtocolAnimation();
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
