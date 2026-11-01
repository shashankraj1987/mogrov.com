"""Assemble the static Mogrov site and its project pages.

Run from any directory: python sync_sites.py MOGROV_REPO OUTPUT
The output is a deployable, self-contained static directory.
"""

from pathlib import Path
import re
import shutil
import sys


def copy_tree(source: Path, destination: Path, *ignored: str) -> None:
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".git", "netlify.toml", *ignored))


def main() -> None:
    mogrov = Path(sys.argv[1]).resolve()
    output = Path(sys.argv[2]).resolve()
    if output.exists():
        raise ValueError(f"Output already exists: {output}")

    output.mkdir(parents=True)
    for name in ("index.html", "founder.html"):
        shutil.copy2(mogrov / name, output / name)
    for name in ("assets", "blog", "downloads"):
        copy_tree(mogrov / name, output / name)
    copy_tree(mogrov / "sites" / "runtime-narrative", output / "runtime-narrative")
    copy_tree(mogrov / "sites" / "devtrack", output / "devtrack", "_redirects")
    wiki = output / "wiki"
    wiki.mkdir()
    copy_tree(mogrov / "documentation" / "devtrack", wiki / "devtrack")
    copy_tree(mogrov / "documentation" / "runtime-narrative", wiki / "runtime-narrative", "CONTRIBUTING.md")
    shutil.copy2(wiki / "runtime-narrative" / "installation.html", wiki / "runtime-narrative" / "index.html")

    # Runtime Narrative assumed it owned the domain root. Give its assets and
    # documentation a dedicated prefix, including links created in JavaScript.
    for path in (output / "runtime-narrative").rglob("*"):
        if path.suffix not in (".html", ".js", ".css"):
            continue
        content = path.read_text(encoding="utf-8")
        for marker in ('"', "'"):
            for target in ("assets/", "docs/", "index.html"):
                content = content.replace(f"{marker}/{target}", f"{marker}/runtime-narrative/{target}")
        content = content.replace('href="/"', 'href="/runtime-narrative/"')
        if path.suffix == ".html":
            content = content.replace(
                '<nav class="topbar-nav">',
                '<nav class="topbar-nav"><a href="/">Mogrov</a>',
            )
        path.write_text(content, encoding="utf-8")

    (output / "_headers").write_text(
        "/*\n  X-Frame-Options: DENY\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n",
        encoding="utf-8",
    )
    (output / "_redirects").write_text(
        "/download/devtrack /downloads/devtrack/ 301\n"
        "/download/devtrack/ /downloads/devtrack/ 301\n"
        "/devtrack/download.html /downloads/devtrack/ 301\n"
        "/devtrack/privacy.html /wiki/devtrack/privacy.html 301\n"
        "/devtrack/wiki.html /wiki/devtrack/ 301\n"
        "/runtime-narrative/docs /wiki/runtime-narrative/ 301\n"
        "/runtime-narrative/docs/ /wiki/runtime-narrative/ 301\n"
        "/runtime-narrative/docs/:page /wiki/runtime-narrative/:page 301\n",
        encoding="utf-8",
    )
    shutil.copy2(
        Path(__file__).with_name("project-switcher.css"),
        output / "assets" / "css" / "project-switcher.css",
    )
    for page in output.rglob("*.html"):
        relative = page.relative_to(output).as_posix()
        active = ("DevTrack" if relative.startswith(("devtrack/", "wiki/devtrack/")) else
                  "Runtime Narrative" if relative.startswith(("runtime-narrative/", "wiki/runtime-narrative/")) else
                  "Mogrov")
        links = [("Mogrov", "/"), ("DevTrack", "/devtrack/"),
                 ("Runtime Narrative", "/runtime-narrative/")]
        nav = '<nav id="mogrov-project-switcher" aria-label="Mogrov projects">' + "".join(
            f'<a href="{href}"' + (' aria-current="page"' if label == active else '') +
            f'>{label}</a>' for label, href in links
        ) + '</nav>'
        content = page.read_text(encoding="utf-8")
        content = content.replace("/runtime-narrative/docs/", "/wiki/runtime-narrative/")
        if relative.startswith("wiki/runtime-narrative/"):
            content = content.replace('"/assets/', '"/runtime-narrative/assets/')
            content = content.replace("'/assets/", "'/runtime-narrative/assets/")
            content = content.replace('"/docs/', '"/wiki/runtime-narrative/')
            content = content.replace("'/docs/", "'/wiki/runtime-narrative/")
            content = content.replace('href="/index.html"', 'href="/runtime-narrative/index.html"')
            content = content.replace('<nav class="topbar-nav">', '<nav class="topbar-nav"><a href="/">Mogrov</a>')
        if relative == "wiki/devtrack/index.html":
            content = content.replace('href="assets/', 'href="/assets/devtrack/')
        if relative == "wiki/runtime-narrative/index.html":
            content = content.replace('href="/wiki/runtime-narrative/installation.html" class="active"',
                                      'href="/wiki/runtime-narrative/" class="active"')
        if "</head>" not in content or "</body>" not in content:
            raise ValueError(f"Missing document structure: {page}")
        content = content.replace(
            "</head>",
            '<link rel="stylesheet" href="/assets/css/project-switcher.css">\n</head>',
            1,
        )
        content = re.sub(r"</body>", nav + "\n</body>", content, count=1)
        page.write_text(content, encoding="utf-8")
    shutil.copy2(Path(__file__).with_name("wiki-index.html"), output / "wiki" / "index.html")
    for path in (output / "runtime-narrative" / "assets").rglob("*.js"):
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace("/runtime-narrative/docs/", "/wiki/runtime-narrative/"), encoding="utf-8")
    for path in (output / "blog").rglob("*.md"):
        content = path.read_text(encoding="utf-8")
        path.write_text(content.replace("/devtrack/wiki.html", "/wiki/devtrack/"), encoding="utf-8")
    print(f"Built {output}")


if __name__ == "__main__":
    main()
