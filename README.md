# Mogrov website

This repository holds the static site for `mogrov.com`. The deployable files are in `public/`:

- `/` — Mogrov
- `/devtrack/` — DevTrack landing page
- `/downloads/devtrack/` — redirect to the latest GitHub release; installer scripts remain local
- `/wiki/` — documentation index for both projects
- `/wiki/devtrack/` — DevTrack documentation and Markdown guides
- `/wiki/runtime-narrative/` — Runtime Narrative documentation
- `/runtime-narrative/` — Runtime Narrative

Zivra is intentionally excluded.

The shared design goal, work sequence, and acceptance checks are in [DESIGN_PLAN.md](DESIGN_PLAN.md).
Each page uses its own header and theme control, with a compact breadcrumb on
deeper pages. Shared styles and behavior are in `assets/css/mogrov-system.css`
and `assets/js/mogrov-system.js`. Product styles still own their content and demos.
The documentation index template is `scripts/wiki-index.html`.
Mogrov owns the DevTrack and Runtime Narrative landing pages and both public wikis.
The product repositories keep their code, release, and package metadata; they do not host
separate websites. Legacy project paths redirect internally to the relevant Mogrov page or wiki.
The published site has no outbound links or runtime CDN dependencies. Third-party browser
libraries used by the existing designs and wiki are checked into `assets/vendor/`.

## Preview and check

From the repository root, run `node scripts/serve.js` and open
`http://127.0.0.1:8000/`. This preview also redirects the old documentation
paths. Run `python scripts/check_site.py public` to check local links and assets.

## Refresh from source

The Mogrov homepage, both project sites, and all public documentation
are maintained in this repository. Edit `sites/devtrack/` and `sites/runtime-narrative/`
for the project landing pages. Edit `downloads/devtrack/` for the DevTrack
installer scripts and `scripts/sync_sites.py` for download redirects. Edit
`documentation/devtrack/` and
`documentation/runtime-narrative/` for the wikis. The Runtime Narrative authoring guide
is `documentation/runtime-narrative/CONTRIBUTING.md`.
The copies under `public/` are published snapshots. To refresh them, make a new output
directory with:

```text
python scripts/sync_sites.py <mogrov-repo> <new-output-directory>
python scripts/check_site.py <new-output-directory>
```

Review the new output, then replace `public/` with it. The sync script rewrites paths for
the shared domain and marks DevTrack's development as paused. It never modifies the source
repository or an existing output directory.

## One deployment

Publish only Mogrov's `public/` directory. It contains all three landing pages, both
wikis, internal redirects, and project assets. DevTrack releases remain in its code
repository; the Runtime Narrative Python package remains on PyPI. No project-specific website
deployment or edge routing is needed.

## Cloudflare Pages

Connect this repository to Cloudflare Pages using the production branch, no framework,
no build command, and `public` as the output directory. Add `mogrov.com` as the custom
domain. The domain can remain registered at Hostinger; Cloudflare Pages requires its
nameservers for the apex domain. Copy any existing email DNS records before switching
nameservers. `_headers` and `_redirects` live in `public/`.
