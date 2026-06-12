# CLAUDE.md — Mogrov.com

## Project overview

Mogrov.com is the marketing / landing site for **Mogrov**, a developer-first tools collective (named in homage to mathematician Andrey Kolmogorov). The site presents the company's mission, projects (e.g. `runtime-narrative` on PyPI, `DevTrack`), founder profile, and a contact form. It is a single self-contained HTML file — no build step, no backend, no dependencies installed locally; everything loads from CDNs.

## Codebase map

| Path | Purpose |
|---|---|
| `index.html` | Main landing page (scrollable sections: hero, features, projects, mission, contact). |
| `founder.html` | Dedicated founder profile page (Shashank Raj). Links back to `index.html`. |
| `assets/js/tailwind-config.js` | Shared Tailwind CDN config: Tokyo Night + brand color palettes, fonts, animations. |
| `assets/css/site.css` | Shared stylesheet: theme vars, `.glass`, `.bg-grid`, `.btn-shimmer`, nav, animations. |
| `assets/js/site.js` | Shared behavior: theme toggle (with `localStorage` persistence), Lucide icon init, nav scroll effects. |

## Build & run commands

There is **no build system**. The site is static and dependency-free locally (Tailwind, Lucide, and Google Fonts load via CDN).

```bash
# Run locally — just open the file
start index.html              # Windows

# Or serve over HTTP (needed if a browser blocks file:// for any feature)
python -m http.server 8000    # then visit http://localhost:8000
npx serve .                   # alternative
```

No install, lint, format, or test commands exist. If a toolchain is added later (e.g. a Tailwind CLI build to replace the CDN), document it here.

## Architecture

```
   CDN (Tailwind, Lucide, Google Fonts)
          │
          ▼
   assets/js/tailwind-config.js  ←── loaded by every page
   assets/css/site.css           ←── loaded by every page
   assets/js/site.js             ←── loaded by every page
          │
          ├── index.html    (main landing — scrollable sections)
          └── founder.html  (founder profile page)
```

- **Multi-page static site**: `index.html` and `founder.html` are separate HTML documents that share the `assets/` files. Navigation between pages is standard anchor links (no SPA router).
- **Theming**: dark/light is driven by `dark`/`light` classes on `<html>`. An inline `<head>` snippet reads `localStorage` before first paint to avoid flash. `assets/js/site.js` wires toggle buttons and keeps `localStorage` in sync.
- **Icons**: `lucide.createIcons()` runs in `site.js` on `DOMContentLoaded`.
- **Tailwind**: config is in `assets/js/tailwind-config.js`, assigned to `tailwind.config` after the CDN script loads.

## Key patterns

- **Shared assets first** — any styles, behavior, or Tailwind config that applies to more than one page belongs in `assets/`. Page-specific markup stays in its own HTML file.
- **Tokyo Night palette** — colors are defined in `assets/js/tailwind-config.js` (`tokyo.*` for dark, `brand.*` for light). Reference via Tailwind classes (`dark:text-tokyo-blue`). Add new colors to the config, not as one-off hex values.
- **Adding a page** — (1) create `pagename.html` at root, (2) include the three shared `assets/` files in `<head>`, (3) add the inline theme-init snippet before them to avoid flash, (4) add nav links from/to the existing pages.
- **Theme persistence** — `assets/js/site.js` persists choice to `localStorage` under key `mogrov-theme`. The inline `<head>` snippet on each page reads this key before paint.
- **No build step / no state library** — DOM is the state. Tailwind via CDN is not production-optimized (known gap).

## Session completion status

**Done**
- Multi-page static site: `index.html` (main landing) + `founder.html` (founder profile).
- Shared asset extraction: `assets/css/site.css`, `assets/js/site.js`, `assets/js/tailwind-config.js`.
- Tokyo Night dark / light theme with `localStorage` persistence across pages.

**In progress / known gaps**
- Contact form is non-functional (no backend/handler).
- No build pipeline — Tailwind via CDN is not production-optimized.
