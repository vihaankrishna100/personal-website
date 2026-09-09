# Personal website

One page, one file. Everything is in **`index.html`** — no build step, no
framework, no npm. The only external thing it loads is Google Fonts.

## Files

| File | What it is |
|------|------------|
| `index.html` | The whole site |
| `refresh-github.sh` | Re-pulls your commit data into the page |
| `favicon.*`, `apple-touch-icon.png` | Browser-tab icons — a circular crop of your photo |
| `make-favicon.py` | Regenerates those icons from `photo.jpg` |
| `photo.jpg` | Your headshot, shown in the sidebar |
| `shots/*.png` | Project screenshots, pulled from the project repos |

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
shots/alzdetector.png   <- live, from the AlzDetector repo
shots/finsight.png      <- live, from the FinSight-AI repo
shots/feynmind.png      <- live, from the FeynMind-AI repo

shots/learnai.png                         <- not yet; diagram shown instead
shots/weave.png     shots/advisor.png     <- not yet; diagram shown instead
shots/notebooks.png                       <- not yet; diagram shown instead
```

Four projects show real app screenshots taken from their own GitHub repos.
PyPath's comes from `SaiC123/mypypath`, the repo it actually lives in — there
is no PyPath repo on your account. The other four have no images in their repos, so
they fall back to the hand-drawn SVG diagram. To swap one of those in later:
save the file at the path above and uncomment the `<img>` line sitting right
there in `index.html` — the image sits on top of the diagram and takes over.


`style="--h: 265"` on a `.shot` sets that graphic's colour (any hue, 0–360).

## The commit surface

The 52×7 contribution grid is extruded into 3D and drawn with plain canvas — no
Three.js. Drag to rotate, scroll to zoom, hover a bar for that day. It auto-fits
the frame at any angle and re-colours itself when you switch theme.

The data is baked into the page in the `var GH = { … }` block so the site works
as a static file with no API key. To update it:

```bash
./refresh-github.sh
```

That rewrites the `GH` block in place with fresh numbers from `gh api`. It needs
the GitHub CLI signed in (`gh auth login`). Pass a different username as the
first argument if you ever need to.

The language percentages just below it are in `var LANGS = [ … ]` — those are
by bytes across your public repos, which is why Jupyter Notebook is so high
(notebook files carry their saved output inline). Edit that array if you'd
rather show a different mix.

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

## Still to double-check

- **LinkedIn URL** is a guess: `linkedin.com/in/vihaan-krishna`. It appears in
  the sidebar, the intro, and Contact.

## Publishing (free)

- **GitHub Pages:** push this folder to a repo → Settings → Pages → deploy from
  `main` / root.
- **Netlify / Vercel:** drag the folder onto the dashboard.
