#!/usr/bin/env python3
"""Fail unless index.html has exactly one accessibility-statement link.

The link must have the exact href and exact text, and no target attribute.
Usage: python3 scripts/check-a11y-link.py [path-to-index.html]
"""
import sys
from html.parser import HTMLParser

HREF = "https://aimprove.co.il/accessibility-statement/"
TEXT = "הצהרת נגישות"


class Finder(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self._open = None

    def handle_starttag(self, tag, attrs):
        if tag == "a" and dict(attrs).get("href") == HREF:
            self._open = {"attrs": dict(attrs), "text": ""}

    def handle_data(self, data):
        if self._open is not None:
            self._open["text"] += data

    def handle_endtag(self, tag):
        if tag == "a" and self._open is not None:
            self.links.append(self._open)
            self._open = None


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "index.html"
    with open(path, encoding="utf-8") as f:
        parser = Finder()
        parser.feed(f.read())
    errors = []
    if len(parser.links) != 1:
        errors.append("expected exactly 1 link to %s, found %d" % (HREF, len(parser.links)))
    for link in parser.links:
        if link["text"] != TEXT:
            errors.append("link text is %r, expected %r" % (link["text"], TEXT))
        if "target" in link["attrs"]:
            errors.append("link must not have a target attribute")
    if errors:
        print("FAIL: " + "; ".join(errors))
        return 1
    print("OK: one accessibility-statement link, exact text, no target")
    return 0


if __name__ == "__main__":
    sys.exit(main())
