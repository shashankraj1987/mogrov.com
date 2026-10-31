# Mogrov website

This repository holds the static site for `mogrov.com`. The deployable files are in `public/`:

- `/` — Mogrov
- `/devtrack/` — DevTrack landing page
- `/wiki/` — documentation index for both projects
- `/wiki/devtrack/` — DevTrack documentation and Markdown guides
- `/wiki/runtime-narrative/` — Runtime Narrative documentation
- `/download/devtrack/` — redirect to the latest DevTrack GitHub release
- `/downloads/devtrack/` — DevTrack install scripts
- `/runtime-narrative/` — Runtime Narrative

Zivra is intentionally excluded.

Every HTML page has the same project switcher. Its shared stylesheet is
`public/assets/css/project-switcher.css`; each project's own styles stay separate.
The documentation index template is `scripts/wiki-index.html`.
DevTrack has an independently deployable landing page in its own repository's `website/`.
Mogrov retains the combined-site routes and owns both wikis. Its `/devtrack/` route serves a snapshot of that landing page. Legacy DevTrack URLs
redirect to the wiki, privacy page, installer scripts, or latest GitHub release.

## Preview and check

From the repository root, run `node scripts/serve.js` and open
`http://127.0.0.1:8000/`. This preview also redirects the old documentation
paths. Run `python scripts/check_site.py public` to check local links and assets.

## Refresh from source

The Mogrov root pages, assets, DevTrack installer scripts, Runtime Narrative project site,
and all public documentation are maintained in this repository.
Edit `documentation/devtrack/` and `documentation/runtime-narrative/` for the wikis.
The DevTrack repository has an independent `website/` output; keep `sites/devtrack/`
as its Mogrov snapshot. The Runtime Narrative repository has an independent `website/` output. Keep `sites/runtime-narrative/` as its Mogrov snapshot and sync site changes between the two before refreshing `public/`.
Its authoring guide is `documentation/runtime-narrative/CONTRIBUTING.md`.
The copies under `public/` are published snapshots. To refresh them, make a new output
directory with:

```text
python scripts/sync_sites.py <mogrov-repo> <new-output-directory>
python scripts/check_site.py <new-output-directory>
```

Review the new output, then replace `public/` with it. The sync script rewrites paths for
the shared domain and marks DevTrack's development as paused. It never modifies the source
repository or an existing output directory.

## Independent deployment outputs

Each repository has its own static hosting output: Mogrov `public/`, DevTrack `website/`, and Runtime Narrative `website/`. Each can be deployed from its own branch and hosting project. Mogrov remains the only documentation origin. The Mogrov `public/` output includes snapshots at `/devtrack/` and `/runtime-narrative/`. Serving those exact paths directly from separate hosting projects would require edge routing. Until then, the combined output serves all three paths from one deployment.

## Cloudflare Pages

Connect this repository to Cloudflare Pages using the production branch, no framework,
no build command, and `public` as the output directory. Add `mogrov.com` as the custom
domain. The domain can remain registered at Hostinger; Cloudflare Pages requires its
nameservers for the apex domain. Copy any existing email DNS records before switching
nameservers. `_headers` and `_redirects` live in `public/`.

The static contact form is unconfigured. The `mailto:admin@mogrov.com` link works only
while that mailbox is maintained.
