#!/usr/bin/env bash
# Refresh the commit-history data embedded in index.html.
# Requires the GitHub CLI, signed in:  gh auth login
set -euo pipefail

USER_LOGIN="${1:-vihaankrishna100}"
HERE="$(cd "$(dirname "$0")" && pwd)"

echo "Fetching contributions for $USER_LOGIN ..."
gh api graphql -f query="
{
  user(login: \"$USER_LOGIN\") {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount } }
      }
    }
  }
}" > /tmp/gh-contrib.json

python3 - "$HERE/index.html" <<'PY'
import json, re, sys

path = sys.argv[1]
cal = json.load(open('/tmp/gh-contrib.json'))['data']['user'] \
        ['contributionsCollection']['contributionCalendar']
days = [d for w in cal['weeks'] for d in w['contributionDays']]
nz = {d['date']: d['contributionCount'] for d in days if d['contributionCount'] > 0}

lines, row = [], []
for i, (k, v) in enumerate(sorted(nz.items())):
    row.append(f'"{k}": {v}')
    if len(row) == 4:
        lines.append('    ' + ', '.join(row)); row = []
if row:
    lines.append('    ' + ', '.join(row))

block = (
    'var GH = {\n'
    f'  start: "{days[0]["date"]}",\n'
    f'  days: {len(days)},\n'
    '  counts: {\n' + ',\n'.join(lines) + '\n  }\n'
    '};'
)

html = open(path, encoding='utf-8').read()
new, n = re.subn(r'var GH = \{.*?\n\};', block, html, count=1, flags=re.S)
if n != 1:
    sys.exit('Could not find the "var GH = { ... };" block in index.html')
open(path, 'w', encoding='utf-8').write(new)
print(f'Updated: {cal["totalContributions"]} contributions, '
      f'{len(nz)} active days, through {days[-1]["date"]}')
PY

echo "Done. Reload the page to see it."
