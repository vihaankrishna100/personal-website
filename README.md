# Personal website

One page, one file. Everything is in **`index.html`** — no build step, no
framework, no npm. The only external thing it loads is Google Fonts.

## Files

| File | What it is |
|------|------------|
| `index.html` | The whole site |
| `scripts/refresh_commits.py` | Re-pulls your commit data into the page |
| `.github/workflows/` | Runs that script daily so the graph stays current |
| `favicon.*`, `apple-touch-icon.png` | Browser-tab icons — a circular crop of your photo |
| `make-favicon.py` | Regenerates those icons from `photo.jpg` |
| `photo.jpg` | Your headshot, shown in the sidebar |
| `shots/*` | Project screenshots, pulled from the project repos |
| `life/*` | **You add these.** Photos for the montage under the intro |

## Editing the text

Open `index.html` in a text editor. Content sits under labelled comment blocks:

```
SIDEBAR · HOME · ABOUT · FOCUS · EXPERIENCE · COMMIT SURFACE
INITIATIVES · PROJECTS · TOOLKIT · CONTACT
```

Change the words between the tags and save. Double-click `index.html` to preview.

- **Highlighted phrases** in the intro are `<span class="hl">…</span>`.
- **Timeline entries** are `<div class="tl-item">`: `tl-when` / `tl-role` /
  `tl-org` / `tl-note`.
- **Section numbers** (`§ 1 · About`) are just text in the `.kicker` div —
  renumber by hand if you add or remove a section.

## Projects

Each project is one `<div class="feature">` (big, graphic beside the copy) or
one `<article>` inside `.grid2` (half width). Add `class="feature flip"` to put
the graphic on the right instead of the left.

The graphic in each `.shot` is a hand-drawn SVG schematic of what the project
actually does. **To use a real screenshot instead**, just drop a PNG at the path
already referenced — e.g. `shots/alzdetector.png`. The `<img>` sits on top of
the SVG and takes over automatically; until the file exists it removes itself
and you see the diagram. Paths currently expected:

```
shots/pypath.jpg        <- live, from SaiC123/mypypath (PyPath's own repo)
shots/learnai.jpg       <- live, captured from learnai-forsyth.vercel.app
shots/weave.jpg         <- live, captured by running the app locally
shots/advisor.jpg       <- live, captured by running the app locally
shots/alzdetector.png   <- live, from the AlzDetector repo
shots/finsight.png      <- live, from the FinSight-AI repo
shots/feynmind.png      <- live, from the FeynMind-AI repo

```

Every project on the site shows a real app screenshot. Four come from their own GitHub repos;
LearnAI's is a headless-Chrome capture of the live site, since its repo holds
brand banners rather than screenshots.
PyPath's comes from `SaiC123/mypypath`, the repo it actually lives in — there
is no PyPath repo on your account. Weave and Financial Advisor LLM have no images committed, so those two were
captured by running each app locally and screenshotting it.
they fall back to the hand-drawn SVG diagram. To swap one of those in later:
save the file at the path above and uncomment the `<img>` line sitting right
there in `index.html` — the image sits on top of the diagram and takes over.


`style="--h: 265"` on a `.shot` sets that graphic's colour (any hue, 0–360).

## The commit surface

The 52×7 contribution grid is extruded into 3D and drawn with plain canvas — no
Three.js. Drag to rotate, scroll to zoom, hover a bar for that day. It auto-fits
the frame at any angle and re-colours itself when you switch theme.

The data is baked into the page in the `var GH = { … }` block so the site works
as a static file with no API key.

**It updates itself.** A GitHub Action runs daily at 06:17 UTC, re-reads your
public contributions calendar, and commits only if the graph actually changed.
There is no token to create — it reads the same public page a visitor sees, so
the numbers on your site always match the numbers on your GitHub profile.

To update it by hand:

```bash
python3 scripts/refresh_commits.py
```

You can also trigger the Action manually from the repo's **Actions** tab.

One caveat worth knowing: GitHub disables scheduled workflows in repos with no
activity for 60 days. Pushing anything (or running the Action by hand) resets
that clock.

The language percentages just below it are in `var LANGS = [ … ]` — those are
by bytes across your public repos, which is why Jupyter Notebook is so high
(notebook files carry their saved output inline). Edit that array if you'd
rather show a different mix.

## The montage under the intro

Six groups of photos. Hovering any tile lifts its whole group and names it;
tapping does the same on a phone; tabbing works too, since each tile is a real
button.

**There are no photos in it yet** — it renders labelled placeholder tiles until
you add some. To fill it in:

1. Drop images in `life/` (any shape, tiles crop to fill; ~800px on the long
   edge is plenty).
2. Find the `LIFE` array near the bottom of `index.html` and list the filenames:

```js
{ id: "food", label: "Food", hue: 25, note: "Most of my good ideas ...",
  photos: ["life/food-1.jpg", "life/food-2.jpg"], spans: ["w2", "", ""] },
```

- `note` is the line that appears on hover — **these are placeholder wording,
  written to be replaced. Put them in your own words.**
- `spans` sets the tile shapes: `w2`/`w3` wider, `h2` taller, `""` a single square.
- `hue` is that group's colour (0–360).
- Add or remove whole groups by editing the array — nothing else needs changing.

## The toolkit grid

The brand marks come from [Simple Icons](https://simpleicons.org), whose icon
files are CC0. The trademarks themselves belong to their owners — they appear
here purely to say "I build with this", which is ordinary nominative use.

Each tile carries two colours: `--brand` is the official one, and `--brand-dk`
is a lightened stand-in used only on the dark theme, for marks that would
otherwise be invisible (Next.js is pure black, pandas and NumPy are near-black).

To add a tool: copy a `.tool` block, swap the `<path d="...">` for the icon's
path from `simple-icons/icons/<slug>.svg`, and set `--brand` to its hex.

## Colours, fonts, motion

- Palette and fonts: the `:root` block at the top of `<style>`. Dark values are
  listed twice on purpose — once for "your system is dark", once for the manual
  toggle — so both paths work.
- **Dark mode** is a real toggle in the sidebar. It defaults to your system
  setting and remembers your choice in `localStorage`.
- **Slow scroll**: the page eases toward where the wheel asks for instead of
  jumping. `FEEL` in the script at the bottom controls the weight — lower is
  slower and heavier, higher is snappier. Touch and keyboard keep their native
  behaviour, and the commit surface keeps its scroll-to-zoom.
- **Parallax**: hero elements carry `data-depth="0.3"` etc. — bigger number,
  more drift as you scroll. Remove the attribute to pin an element.
- **Figures draw themselves in** when they scroll into view. Inside any project
  diagram, an element opts in with a class: `draw` (traces a line), `rise`
  (grows up from its base), `pop` (springs in), `fade`, or `flow` (dashes that
  travel along a connector, for data moving between stages). `style="--i:3"`
  staggers it — higher number, later start.
- **The faint moving lines** behind the intro: `FLOW_INTENSITY` in the script at
  the bottom (`0` turns it off).
- Everything animated stops for visitors who have "reduce motion" turned on.

## Contact

The email `vvihaankrishna@gmail.com` is wired into three places: the sidebar
**Email me** button, the "Email" chip in the intro, and the Contact section —
where it's also a one-click **Copy** button. The Contact link opens the visitor's
mail app with the subject pre-filled.

There is **no résumé on the site**, by design. The file was deleted rather than
just unlinked, because anything left in this folder stays downloadable by URL
once you publish — an unlinked `resume.pdf` is still a public `resume.pdf`. If
you ever want to share it, send it directly rather than putting it back here.

If you'd rather have a proper contact *form* (name / message / send) instead of
a mailto link, that needs a form-handling service since this is a static site —
say the word and I'll wire one up.

## Publishing (free)

- **GitHub Pages:** push this folder to a repo → Settings → Pages → deploy from
  `main` / root.
- **Netlify / Vercel:** drag the folder onto the dashboard.
