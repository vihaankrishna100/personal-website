#!/usr/bin/env python3
"""
Refresh the commit-graph data baked into index.html.

Reads the public contributions calendar from github.com — no token, no
API key, nothing to expire. That endpoint is also what a visitor sees on
your profile, so the numbers on the site match the numbers on GitHub.

    python3 scripts/refresh_commits.py [username]

Runs locally and in CI (see .github/workflows/refresh-commits.yml).
Standard library only.
"""

import json
import os
import re
import sys
import urllib.request

USER = sys.argv[1] if len(sys.argv) > 1 else "vihaankrishna100"
HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PAGE = os.path.join(HERE, "index.html")
URL = f"https://github.com/users/{USER}/contributions"


def fetch(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "refresh-commits (personal site build)",
        "Accept": "text/html",
    })
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse(html):
    """-> (ordered list of (date, count), first_date)"""
    cells = {}
    for m in re.finditer(
            r'data-date="(\d{4}-\d{2}-\d{2})"\s+id="(contribution-day-component-\d+-\d+)"', html):
        cells[m.group(2)] = m.group(1)

    tips = {}
    for m in re.finditer(
            r'for="(contribution-day-component-\d+-\d+)"[^>]*>\s*(.*?)\s*</tool-tip>', html, re.S):
        tips[m.group(1)] = m.group(2)

    days = {}
    for cid, date in cells.items():
        text = tips.get(cid, "")
        n = re.match(r"(\d[\d,]*)\s+contribution", text)
        days[date] = int(n.group(1).replace(",", "")) if n else 0

    if not days:
        sys.exit("Could not parse any days — GitHub's markup may have changed.")
    return days


def render(days):
    nz = {d: c for d, c in sorted(days.items()) if c > 0}
    rows, row = [], []
    for k, v in nz.items():
        row.append(f'"{k}": {v}')
        if len(row) == 4:
            rows.append("    " + ", ".join(row))
            row = []
    if row:
        rows.append("    " + ", ".join(row))

    return (
        "var GH = {\n"
        f'  start: "{min(days)}",\n'
        f"  days: {len(days)},\n"
        "  counts: {\n" + ",\n".join(rows) + "\n  }\n"
        "};"
    ), nz


def main():
    days = parse(fetch(URL))
    block, nz = render(days)

    html = open(PAGE, encoding="utf-8").read()
    new, n = re.subn(r"var GH = \{.*?\n\};", lambda _: block, html, count=1, flags=re.S)
    if n != 1:
        sys.exit('Could not find the "var GH = { ... };" block in index.html')

    if new == html:
        print(f"No change — {sum(nz.values())} contributions across {len(nz)} days.")
        return

    open(PAGE, "w", encoding="utf-8").write(new)
    print(f"Updated: {sum(nz.values())} contributions across {len(nz)} active days, "
          f"through {max(days)}.")


if __name__ == "__main__":
    main()
