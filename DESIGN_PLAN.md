# Mogrov site design goal

## Outcome

Mogrov, DevTrack, and Runtime Narrative feel like one website. Every content page
has an obvious route to Mogrov home and a breadcrumb that shows its location.
DevTrack keeps its current hero layout, watermark, animation, terminal, and calls
to action while adopting Mogrov's blue and violet palette.

## Work sequence

1. **Shared foundation:** Use the same color tokens, type families, spacing scale,
   buttons, card surfaces, header controls, footer treatment, and light/dark theme
   preference. Keep product-specific names, demos, and content.
2. **Navigation:** Put a visible Mogrov home link in every header. Show
   `Mogrov / Product / Docs / Page` breadcrumbs where applicable, including
   project pages, wikis, blog, and founder pages. Keep the current page marked
   for assistive technology. Keep the extra project switcher bar out of the
   published pages; project links remain in the Mogrov project list and footers.
3. **Landing pages:** Apply the shared shell to Mogrov, DevTrack, and Runtime
   Narrative. Preserve DevTrack's hero composition in both readable light and
   dark themes. Align buttons, section rhythm, cards, and footers.
4. **Supporting pages:** Align the documentation index, both wikis, blog, and
   founder page. Ensure dynamic blog post and DevTrack wiki breadcrumbs show
   the current title.
5. **Publishable build:** Rebuild `public/` from canonical source with
   `scripts/sync_sites.py`, then run `scripts/check_site.py`. Keep download
   redirects pointed at the latest DevTrack GitHub release.

## Acceptance

- All published HTML pages except the Mogrov homepage show a visible breadcrumb
  with a working Mogrov home link. The homepage brand links to `/`.
- Project links and breadcrumbs are usable by keyboard and on narrow screens.
- One theme choice persists when moving between all three project pages and
  both documentation areas; light and dark variants remain readable.
- DevTrack's hero structure and behavior remain recognizable and functional.
- Desktop and mobile views of all three landing pages and representative wiki,
  blog, and founder pages are visually reviewed in both themes.
- The built site's links, assets, redirects, and installer routes pass checks;
  no old standalone website or runtime CDN dependency is introduced.

`public/` is generated output. Source edits belong in the root pages,
`sites/`, `documentation/`, `blog/`, `assets/`, and `scripts/`.
