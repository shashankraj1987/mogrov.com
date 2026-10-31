# Mogrov repository

- `README.md` describes the current site and deployment layout.
- Edit the root Mogrov pages, `sites/devtrack/`, `sites/runtime-narrative/`, and
  `documentation/` as the canonical source. `public/` is generated and published.
- Rebuild into a new directory with `python scripts/sync_sites.py . <output>`.
  Check it with `python scripts/check_site.py <output>` before replacing `public/`.
- Keep DevTrack and Runtime Narrative at `/devtrack/` and `/runtime-narrative/`.
  Keep their documentation under `/wiki/`.
- Keep published navigation, redirects, scripts, styles, and fonts on Mogrov.
  Do not reintroduce outbound website links, CDN requests, or old standalone domains.
- Do not commit credentials, private environment files, login sessions, or generated
  chat databases.
