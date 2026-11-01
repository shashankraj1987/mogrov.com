"""Check published routes, anchors, assets, and outbound dependencies."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import re
import sys


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.ids = set()

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get("id"):
            self.ids.add(attrs["id"])
        if tag == "a" and attrs.get("name"):
            self.ids.add(attrs["name"])
        for name, value in attrs.items():
            if name in ("href", "src") and value:
                self.urls.append(value)


root = Path(sys.argv[1]).resolve()
missing = []
checked = 0
for route in ("index.html", "devtrack/index.html", "runtime-narrative/index.html",
              "wiki/index.html", "wiki/devtrack/index.html", "wiki/runtime-narrative/index.html",
              "downloads/devtrack/install.sh",
              "downloads/devtrack/install.ps1"):
    if not (root / route).is_file():
        missing.append(f"required route missing: {route}")
redirects_text = (root / "_redirects").read_text(encoding="utf-8")
for route in ("/download/devtrack", "/download/devtrack/", "/downloads/devtrack",
              "/downloads/devtrack/", "/devtrack/download.html"):
    if f"{route} https://github.com/sraj0501/Devtrack_/releases/latest 302" not in redirects_text:
        missing.append(f"missing GitHub release redirect: {route}")
pages = {}
for page in root.rglob("*.html"):
    parser = Links()
    parser.feed(page.read_text(encoding="utf-8"))
    pages[page] = parser
devtrack_wiki = root / "wiki/devtrack/index.html"
if devtrack_wiki.is_file():
    wiki_content = devtrack_wiki.read_text(encoding="utf-8")
    for guide in (root / "wiki/devtrack/docs").glob("*.md"):
        if not re.search(r"\bid:\s*['\"]" + re.escape(guide.stem) + r"['\"]", wiki_content):
            missing.append(f"wiki/devtrack/docs/{guide.name} -> missing from wiki navigation")
for page, parser in pages.items():
    relative = page.relative_to(root).as_posix()
    content = page.read_text(encoding="utf-8")
    if 'id="mogrov-project-switcher"' in content:
        missing.append(f"{relative} -> redundant project bar")
    theme_control = (
        'id="mogrov-global-theme"' if relative in ("devtrack/index.html", "wiki/index.html") else
        'id="theme-toggle"' if relative.startswith(("runtime-narrative/", "wiki/runtime-narrative/")) else
        'id="themeToggle"' if relative == "wiki/devtrack/index.html" else
        'id="darkModeToggle"' if relative == "wiki/devtrack/privacy.html" else
        'data-theme-toggle'
    )
    if theme_control not in content or "mogrov-theme" not in content:
        missing.append(f"{relative} -> missing theme control")
    if relative == "index.html":
        if 'href="/" class="flex items-center gap-2.5 group" aria-label="Mogrov home"' not in content:
            missing.append("index.html -> missing home-linked brand")
    else:
        breadcrumb = re.search(r'<nav\b[^>]*aria-label="Breadcrumb"[^>]*>(.*?)</nav>', content, re.S)
        if not breadcrumb or not re.search(r'<a\s+[^>]*href="/"[^>]*>Mogrov</a>', breadcrumb.group(1)):
            missing.append(f"{relative} -> missing Mogrov breadcrumb")
        elif 'aria-current="page"' not in breadcrumb.group(1):
            missing.append(f"{relative} -> breadcrumb has no current page")
    base = "https://mogrov.com/" + page.relative_to(root).as_posix()
    for url in parser.urls:
        absolute = urlsplit(urljoin(base, url))
        if absolute.scheme not in ("https", "http") or absolute.netloc != "mogrov.com":
            missing.append(f"{page.relative_to(root)} -> outbound {url}")
            continue
        candidate = root / unquote(absolute.path).lstrip("/")
        if candidate.is_dir():
            candidate /= "index.html"
        checked += 1
        if not candidate.is_file() and absolute.path not in ("/downloads/devtrack", "/downloads/devtrack/"):
            missing.append(f"{page.relative_to(root)} -> {url}")
        elif absolute.fragment and candidate.suffix == ".html" and absolute.fragment not in pages.get(candidate, Links()).ids:
            missing.append(f"{page.relative_to(root)} -> missing anchor {url}")
    for url in re.findall(r'''\b(?:href|src)\s*=\s*["'](https?://[^"']+|mailto:[^"']+)["']''', content):
        if url.startswith("https://mogrov.com/"):
            continue
        item = f"{page.relative_to(root)} -> outbound {url}"
        if item not in missing:
            missing.append(item)
for css in root.rglob("*.css"):
    content = css.read_text(encoding="utf-8")
    if re.search(r"@import\s+url\(['\"]?https?://|url\(['\"]?https?://", content):
        missing.append(f"{css.relative_to(root)} -> outbound CSS asset")
for path in root.rglob("*"):
    if not path.is_file() or "vendor" in path.parts:
        continue
    if path.suffix == ".md":
        content = path.read_text(encoding="utf-8")
        if re.search(r"(?<!!)\[[^]]+\]\(https?://", content):
            missing.append(f"{path.relative_to(root)} -> outbound Markdown link")
    if path.suffix == ".js":
        content = path.read_text(encoding="utf-8")
        if re.search(r"(?:fetch\(|location\.href\s*=)\s*[`'\"](?:https?://|mailto:)", content):
            missing.append(f"{path.relative_to(root)} -> outbound JavaScript request")
redirects = root / "_redirects"
if redirects.exists():
    for line in redirects.read_text(encoding="utf-8").splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        fields = line.split()
        if len(fields) < 2:
            missing.append(f"_redirects -> invalid {line}")
            continue
        target = fields[1]
        if target == "https://github.com/sraj0501/Devtrack_/releases/latest":
            continue
        if not target.startswith("/"):
            missing.append(f"_redirects -> outbound {line}")
        elif ":" not in target:
            candidate = root / target.lstrip("/")
            if candidate.is_dir():
                candidate /= "index.html"
            if not candidate.is_file():
                missing.append(f"_redirects -> missing target {line}")
print(f"Checked {checked} local links across {len(pages)} pages")
for item in missing[:80]:
    print(item)
if missing:
    print(f"Missing: {len(missing)}")
    sys.exit(1)
