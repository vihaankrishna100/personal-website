# Prompt: port the commit surface to another site

Paste everything below the line into a coding session opened on the target site's repo.
It points back at this repo as the reference implementation and records the bugs hit
while building the original, so they don't get rediscovered.

---

# Task: add a 3D GitHub contribution surface to this site

Port the "A year of commits" figure from my personal site into this project, adapted to
this codebase's stack and styling.

Reference implementation (public, read it before writing anything):
https://github.com/vihaankrishna100/personal-website
- `index.html` — search for `COMMIT SURFACE` (markup, CSS, and the renderer script),
  `var GH = {` (embedded data), `var LANGS` (language bar)
- `scripts/refresh_commits.py` — data fetch + in-place rewrite
- `.github/workflows/refresh-commits.yml` — daily refresh Action

Start by inspecting this repo (stack, styling system, theme handling, deploy target) and
tell me how you'll adapt it before editing. GitHub username: `vihaankrishna100`
(confirm with me if this site should show a different account).

## What it is
The last ~52 weeks of GitHub contributions as a 53×7 grid extruded into 3D, drawn with
plain Canvas 2D — no Three.js or other libraries. Drag to rotate, wheel to zoom, hover a
bar for "N commits · YYYY-MM-DD". Below it: total contributions, active days, longest
streak, and a language breakdown bar.

## Data — do it this way, not via the API
- Source: the public page `https://github.com/users/<user>/contributions`. No token, no
  API key, nothing to expire.
- Do NOT use the GraphQL `contributionsCollection` API. It buckets days in UTC while the
  profile page uses local time, so late-evening commits land a day off and the site stops
  matching the profile.
- Parse: each `<td>` carries `data-date="YYYY-MM-DD"` and `id="contribution-day-component-X-Y"`;
  the count is in the `<tool-tip for="<that id>">` text ("7 contributions on …" /
  "No contributions on …"). `data-level` is only a 0–4 bucket, not a count.
- Embed the result in the page as a sparse block — only non-zero days:
  `var GH = { start: "YYYY-MM-DD", days: 368, counts: { "2026-09-09": 11, ... } };`
  The page must work as a static file with no runtime fetch.
- The refresh script: stdlib only; validate the username against GitHub's rule
  (`^[A-Za-z0-9](?:[A-Za-z0-9-]{0,37}[A-Za-z0-9])?$`) before building the URL; refuse any
  response whose final URL isn't `https://github.com`; exit non-zero if zero days parse or
  the `var GH` block isn't found exactly once; be idempotent (second run reports "no change").

## Daily refresh
GitHub Actions workflow: `schedule` cron once daily plus `workflow_dispatch`;
`permissions: contents: write`; a `concurrency` group; `actions/checkout` pinned to a full
commit SHA (the job can push to main); commit as `github-actions[bot]` only if `git diff`
shows a change. If this site isn't deployed from GitHub, tell me and propose the
equivalent for its host instead.

## Renderer requirements (each of these was a real bug in the first version)
- **Auto-fit at every angle.** Project the 8 corners of the grid's bounding box (height
  0 to max bar) at the current yaw/pitch, then derive scale and offset from that box.
  A fixed scale runs the ribbon off the canvas once it's rotated.
- Painter's algorithm: depth-sort cells far→near each draw. Zero-count days are thin flat
  plates; only non-zero days extrude, with two darker side-face shades.
- Hover hit-testing: point-in-polygon on each cell's projected top face, checking
  nearest-first.
- Drag rotates yaw freely; clamp pitch (≈0.22–1.42 rad). Use pointer events with pointer
  capture so it works for mouse and touch.
- Wheel zoom must `preventDefault()` **only when the zoom actually changes** — at the
  min/max limit let the page scroll, or the canvas traps scrolling.
- If the site has any smooth-scroll/wheel-hijacking script, exclude this canvas from it.
- Handle devicePixelRatio (cap at 2), redraw on resize, and redraw on theme change.
- Redraw on demand only — no continuous animation loop. One short eased intro spin the
  first time it scrolls into view; skip it under `prefers-reduced-motion`.
- Colour: a 5-step ramp per theme. Dark theme needs its own ramp — don't reuse light values.

## Language bar
In my site `LANGS` is hardcoded. Here, either keep it static or compute it — but note that
bytes-per-language across repos is dominated by Jupyter notebooks (saved outputs inflate
them), so label what the percentages measure.

## Acceptance criteria
1. Run the refresh script twice: first run updates the block, second reports no change.
2. Hover several bars and confirm the dates/counts match the GitHub profile graph exactly.
3. Rotate to extreme angles and zoom to both limits: grid always stays in frame, the page
   still scrolls at the zoom limits.
4. Works in light and dark theme, on a phone width, and with reduced motion on.
5. No console errors; no new runtime dependencies.
6. Trigger the workflow once manually to prove the push path works. Tip: set one day in
   the `GH` block to a wrong value first, so the run has something to correct — otherwise
   it reports "unchanged" and never exercises the commit step.

## Constraints
- Match this repo's existing conventions, framework, and styling rather than pasting my
  site's CSS wholesale.
- Don't touch unrelated files.
- Ask me before any commit, push, or workflow dispatch.
- Once the Action is live it commits to main on its own, so local pushes may be rejected
  as behind — `git pull --rebase`, never force-push over it.
