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
              "downloads/devtrack/index.html", "downloads/devtrack/install.sh",
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
for page, parser in pages.items():
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
        if not candidate.is_file():
            missing.append(f"{page.relative_to(root)} -> {url}")
        elif absolute.fragment and candidate.suffix == ".html" and absolute.fragment not in pages.get(candidate, Links()).ids:
            missing.append(f"{page.relative_to(root)} -> missing anchor {url}")
    content = page.read_text(encoding="utf-8")
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
