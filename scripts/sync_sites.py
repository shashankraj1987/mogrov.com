"""Assemble the static Mogrov site and its project pages.

Run from any directory: python sync_sites.py MOGROV_REPO OUTPUT
The output is a deployable, self-contained static directory.
"""

from pathlib import Path
from html import escape
import re
import shutil
import sys


def copy_tree(source: Path, destination: Path, *ignored: str) -> None:
    shutil.copytree(source, destination, ignore=shutil.ignore_patterns(".git", "netlify.toml", *ignored))


def breadcrumb(relative: str) -> str:
    if relative == "index.html":
        return ""
    parts = [("Mogrov", "/")]
    if relative == "founder.html":
        parts.append(("Founder", None))
    elif relative.startswith("blog/"):
        parts.append(("Blog", "/blog/" if relative != "blog/index.html" else None))
        if relative == "blog/post.html":
            parts.append(("Post", None))
    elif relative.startswith(("devtrack/", "wiki/devtrack/")):
        parts.append(("DevTrack", "/devtrack/" if relative != "devtrack/index.html" else None))
        if relative.startswith("wiki/"):
            parts.append(("Docs", "/wiki/devtrack/" if relative != "wiki/devtrack/index.html" else None))
            if relative.endswith("privacy.html"):
                parts.append(("Privacy", None))
    elif relative.startswith(("runtime-narrative/", "wiki/runtime-narrative/")):
        parts.append(("Runtime Narrative", "/runtime-narrative/" if relative != "runtime-narrative/index.html" else None))
        if relative.startswith("wiki/"):
            parts.append(("Docs", "/wiki/runtime-narrative/" if relative != "wiki/runtime-narrative/index.html" else None))
            if relative != "wiki/runtime-narrative/index.html":
                label = Path(relative).stem.replace("-", " ").title()
                parts.append((label, None))
    elif relative == "wiki/index.html":
        parts.append(("Documentation", None))
    else:
        return ""
    items = []
    for label, href in parts:
        if href:
            items.append(f'<li><a href="{href}">{escape(label)}</a></li>')
        else:
            items.append(f'<li aria-current="page">{escape(label)}</li>')
    overlay = ' mg-overlay' if relative.startswith(("blog/", "devtrack/")) or relative == "founder.html" else ""
    return f'<nav id="mogrov-site-path" class="{overlay.strip()}" aria-label="Breadcrumb"><ol>' + "".join(items) + '</ol></nav>'


def insert_breadcrumb(content: str, relative: str) -> str:
    trail = breadcrumb(relative)
    if not trail or relative == "wiki/devtrack/index.html":
        return content
    if relative == "wiki/index.html":
        marker = '<main class="wiki-shell">'
        return content.replace(marker, trail + "\n" + marker, 1)
    marker = "</header>" if relative.startswith(("runtime-narrative/", "wiki/runtime-narrative/")) else "</nav>"
    if marker not in content:
        raise ValueError(f"Breadcrumb insertion point missing: {relative}")
    return content.replace(marker, marker + "\n" + trail, 1)


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
        path.write_text(content, encoding="utf-8")

    (output / "_headers").write_text(
        "/*\n  X-Frame-Options: DENY\n  X-Content-Type-Options: nosniff\n  Referrer-Policy: strict-origin-when-cross-origin\n  Permissions-Policy: camera=(), microphone=(), geolocation=()\n",
        encoding="utf-8",
    )
    (output / "_redirects").write_text(
        "/download/devtrack https://github.com/sraj0501/Devtrack_/releases/latest 302\n"
        "/download/devtrack/ https://github.com/sraj0501/Devtrack_/releases/latest 302\n"
        "/downloads/devtrack https://github.com/sraj0501/Devtrack_/releases/latest 302\n"
        "/downloads/devtrack/ https://github.com/sraj0501/Devtrack_/releases/latest 302!\n"
        "/devtrack/download.html https://github.com/sraj0501/Devtrack_/releases/latest 302\n"
        "/devtrack/privacy.html /wiki/devtrack/privacy.html 301\n"
        "/devtrack/wiki.html /wiki/devtrack/ 301\n"
        "/runtime-narrative/docs /wiki/runtime-narrative/ 301\n"
        "/runtime-narrative/docs/ /wiki/runtime-narrative/ 301\n"
        "/runtime-narrative/docs/:page /wiki/runtime-narrative/:page 301\n",
        encoding="utf-8",
    )
    for page in output.rglob("*.html"):
        relative = page.relative_to(output).as_posix()
        content = page.read_text(encoding="utf-8")
        content = content.replace("/runtime-narrative/docs/", "/wiki/runtime-narrative/")
        if relative.startswith("wiki/runtime-narrative/"):
            content = content.replace('"/assets/', '"/runtime-narrative/assets/')
            content = content.replace("'/assets/", "'/runtime-narrative/assets/")
            content = content.replace('"/docs/', '"/wiki/runtime-narrative/')
            content = content.replace("'/docs/", "'/wiki/runtime-narrative/")
            content = content.replace('href="/index.html"', 'href="/runtime-narrative/index.html"')
        if relative == "wiki/devtrack/index.html":
            content = content.replace('href="assets/', 'href="/assets/devtrack/')
        if relative == "wiki/runtime-narrative/index.html":
            content = content.replace('href="/wiki/runtime-narrative/installation.html" class="active"',
                                      'href="/wiki/runtime-narrative/" class="active"')
        if "</head>" not in content or "</body>" not in content:
            raise ValueError(f"Missing document structure: {page}")
        theme_boot = (
            "<script>(function(){try{var t=localStorage.getItem('mogrov-theme')||'light';"
            "var r=document.documentElement;r.classList.add(t);r.setAttribute('data-theme',t);"
            "}catch(e){document.documentElement.classList.add('light');"
            "document.documentElement.setAttribute('data-theme','light');}})();</script>"
        )
        content = content.replace("<head>", "<head>\n" + theme_boot, 1)
        content = content.replace(
            "</head>",
            '<link rel="stylesheet" href="/assets/css/mogrov-system.css">\n</head>',
            1,
        )
        content = content.replace("</body>", '<script src="/assets/js/mogrov-system.js"></script>\n</body>', 1)
        content = insert_breadcrumb(content, relative)
        area = ("wiki-devtrack" if relative == "wiki/devtrack/index.html" else
                "devtrack" if relative.startswith("devtrack/") else
                "wiki-runtime" if relative.startswith("wiki/runtime-narrative/") else
                "runtime" if relative.startswith("runtime-narrative/") else "mogrov")
        if area in ("devtrack", "runtime", "wiki-runtime") and "</footer>" in content:
            footer_links = (
                '<div class="mogrov-footer-links" aria-label="Mogrov pages">'
                '<a href="/">Mogrov</a><a href="/devtrack/">DevTrack</a>'
                '<a href="/runtime-narrative/">Runtime Narrative</a>'
                '<a href="/wiki/">Documentation</a></div>'
            )
            content = content.replace("</footer>", footer_links + "\n</footer>", 1)
        content = re.sub(r"<body(?=[\s>])", f'<body data-mogrov-area="{area}"', content, count=1)
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
