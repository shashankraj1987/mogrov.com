"""Check local HTML links and assets in a static site directory."""

from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urljoin, urlsplit, unquote
import sys


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        for name, value in attrs:
            if name in ("href", "src") and value:
                self.urls.append(value)


root = Path(sys.argv[1]).resolve()
missing = []
checked = 0
for page in root.rglob("*.html"):
    parser = Links()
    parser.feed(page.read_text(encoding="utf-8"))
    base = "https://mogrov.com/" + page.relative_to(root).as_posix()
    for url in parser.urls:
        absolute = urlsplit(urljoin(base, url))
        if absolute.netloc != "mogrov.com" or not absolute.path:
            continue
        candidate = root / unquote(absolute.path).lstrip("/")
        if candidate.is_dir():
            candidate /= "index.html"
        checked += 1
        if not candidate.is_file():
            missing.append(f"{page.relative_to(root)} -> {url}")
print(f"Checked {checked} local links across {sum(1 for _ in root.rglob('*.html'))} pages")
for item in missing[:80]:
    print(item)
if missing:
    print(f"Missing: {len(missing)}")
    sys.exit(1)
