# CLAUDE.md — Mogrov.com

## Project overview

Mogrov.com is the marketing / landing site for **Mogrov**, a developer-first tools collective (named in homage to mathematician Andrey Kolmogorov). The site presents the company's mission, projects (e.g. `runtime-narrative` on PyPI, `DevTrack`), founder profile, and a contact form. It is a single self-contained HTML file — no build step, no backend, no dependencies installed locally; everything loads from CDNs.

## Codebase map

| Path | Purpose |
|---|---|
| `index.html` | The entire site. Contains markup, inline Tailwind config, inline CSS (`<style>`), and inline JS (`<script>`) for all six views. |

The single file is organized in document order as:

| Region (in `index.html`) | What it holds |
|---|---|
| `<head>` → `tailwind.config` | Tokyo Night color palette, custom animations (`float`, `shimmer`, `pulse-slow`) |
| `<head>` → `<style>` | Theme styles: `.glass`, `.bg-grid`, `.text-gradient`, `.btn-shimmer`, `.resume-paper`, view-transition classes, cursor blink |
| `<nav>` | Fixed top nav with view buttons (`onclick="switchView(...)"`) and theme toggle |
| `<main id="view-*">` ×6 | The SPA views: `home`, `about`, `projects`, `contact`, `history`, `resume` |
| trailing `<script>` | `switchView()` router, `runTerminalSimulation()`, `runProtocolAnimation()` typing effects, theme toggle handler |

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
                 index.html (one file)
                 ┌─────────────────────────────┐
   CDN scripts ──▶  Tailwind (cdn.tailwindcss)  │
   (runtime)    │  Lucide icons (unpkg)         │
                │  Google Fonts                 │
                ├─────────────────────────────┤
   markup ──────▶  <nav> + 6 <main id=view-*>  │
                ├─────────────────────────────┤
   behavior ────▶  switchView() router         │
                │   → toggles .hidden-view      │
                │   → re-runs terminal anim     │
                │  theme toggle (dark/light)    │
                └─────────────────────────────┘
```

- **Client-side "SPA"**: all six views ship in the DOM at once. `switchView(name)` hides all `#view-*` elements (adds `.hidden-view`) and reveals the selected one with a fade/translate transition. There is no router, no URL change, no server.
- **Theming**: dark/light is driven by `dark`/`light` classes on `<html>`. Tailwind is configured with `darkMode: 'class'`. The toggle swaps the two classes; there is currently **no persistence** (theme resets on reload).
- **Icons**: `lucide.createIcons()` runs once on load to replace `<i data-lucide="...">` placeholders.

## Key patterns

- **Everything inline** — markup, styles, and behavior live in `index.html`. Keep additions consistent with this single-file approach unless deliberately introducing a build step.
- **Tokyo Night palette** — colors are defined once in `tailwind.config` (`tokyo.*`) and referenced as `dark:text-tokyo-blue` etc. Light mode uses standard Tailwind blues/purples. Add new colors to the config block, not as one-off hex values.
- **Adding a view** — (1) add a `<main id="view-NAME" class="... view-transition hidden-view">`, (2) add a nav `<button onclick="switchView('NAME')" id="nav-NAME">`, (3) register both in the `views` and `navLinks` maps inside `switchView()`.
- **Animations** — typing effects (`runTerminalSimulation`, `runProtocolAnimation`) are plain `setTimeout` loops; re-triggered for the home view on each `switchView('home')`.
- **No persistence / no state library** — DOM is the state. Theme preference is not saved (a known gap).

## Session completion status

**Done**
- Full single-page site with six views, Tokyo Night theme, dark/light toggle, terminal/typing animations, responsive nav.

**In progress / known gaps**
- Theme toggle does not persist across reloads (no `localStorage`).
- Contact form is non-functional (`onsubmit` is prevented; no backend/handler).
- No build pipeline — Tailwind via CDN is not production-optimized.
