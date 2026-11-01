/* One theme preference for Mogrov, both products, and their documentation. */
(function () {
  'use strict';
  var button = document.getElementById('mogrov-global-theme');
  if (!button) return;
  var root = document.documentElement;
  var area = document.body.getAttribute('data-mogrov-area');

  function currentTheme() {
    return root.classList.contains('dark') ? 'dark' : 'light';
  }

  function renderButton() {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    button.setAttribute('aria-label', 'Switch to ' + next + ' theme');
    button.setAttribute('title', 'Switch to ' + next + ' theme');
    button.textContent = next === 'light' ? '☀' : '☾';
  }

  button.addEventListener('click', function () {
    var next = currentTheme() === 'dark' ? 'light' : 'dark';
    if (area === 'wiki-devtrack' && typeof window.setTheme === 'function') {
      window.setTheme(next);
    } else {
      root.classList.toggle('dark', next === 'dark');
      root.classList.toggle('light', next !== 'dark');
      root.setAttribute('data-theme', next);
      try { localStorage.setItem('mogrov-theme', next); } catch (e) {}
    }
    renderButton();
  });

  new MutationObserver(renderButton).observe(root, { attributes: true, attributeFilter: ['class', 'data-theme'] });
  renderButton();
})();
