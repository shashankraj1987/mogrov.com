# Browser dependencies

The deployed pages load these checked-in files from `/assets/vendor/`. The website
does not load JavaScript, CSS, fonts, or icons from external CDNs at runtime.

| Local files | Upstream distribution | License |
| --- | --- | --- |
| `tailwind.js` | `https://cdn.tailwindcss.com` | MIT |
| `lucide.min.js` | Lucide 1.65.0 UMD bundle | ISC |
| `marked.min.js` | Marked 9.1.6 | MIT |
| `highlight.min.js`, `highlight-light.min.css`, `highlight-dark.min.css` | highlight.js 11.9.0 | BSD-3-Clause |
| `mermaid.min.js` | Mermaid 11 browser bundle | MIT |
| `fontawesome.min.css`, `fa-solid-900.woff2` | Font Awesome Free 6.5.1 | Code: MIT; font: SIL OFL 1.1 |

Refresh the files together with their references in the source pages and rerun
`scripts/check_site.py public` after rebuilding. Do not replace these paths with
CDN URLs; the published site is intentionally self-contained.
