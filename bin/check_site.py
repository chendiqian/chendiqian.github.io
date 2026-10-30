#!/usr/bin/env python3
"""Check the generated public profile pages without extra dependencies or network access."""
import json
import sys
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit

ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "_site"
PAGES = ("/", "/publications/", "/cv/")


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.ids = []
        self.references = []
        self.feed(path.read_text(encoding="utf-8"))

    def handle_starttag(self, tag, attributes):
        attrs = dict(attributes)
        if attrs.get("id"):
            self.ids.append(attrs["id"])
        for key in (("href",) if tag in ("a", "link") else ("src",) if tag in ("img", "script") else ()):
            if attrs.get(key):
                self.references.append(attrs[key])


def local_path(url):
    path = SITE / unquote(urlsplit(url).path).lstrip("/")
    if path.is_dir():
        path = path / "index.html"
    return path


def main():
    errors = []
    try:
        json.loads((ROOT / "assets/json/resume.json").read_text())
    except (ValueError, OSError) as exc:
        errors.append(f"Invalid CV JSON: {exc}")
    parsed = {}
    for url in PAGES:
        path = local_path(url)
        if not path.is_file():
            errors.append(f"Missing generated page: {url}; run the Jekyll build first")
            continue
        page = parsed.setdefault(path, Page(path))
        for name, count in Counter(page.ids).items():
            if count > 1:
                errors.append(f"{url}: duplicate HTML id {name!r}")
        for reference in page.references:
            parts = urlsplit(reference)
            if parts.scheme or parts.netloc:
                continue
            destination = urljoin(url, reference)
            target = local_path(destination)
            if not target.is_file():
                errors.append(f"{url}: missing local target {reference!r}")
                continue
            fragment = unquote(urlsplit(destination).fragment)
            if fragment and target.suffix == ".html":
                if target not in parsed:
                    parsed[target] = Page(target)
                if fragment not in parsed[target].ids:
                    errors.append(f"{url}: missing fragment in {reference!r}")
    if errors:
        print("Site checks failed:\n" + "\n".join(f"- {error}" for error in errors), file=sys.stderr)
        return 1
    print("Site checks passed: CV JSON, profile pages, internal links, local assets, fragments, and IDs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
