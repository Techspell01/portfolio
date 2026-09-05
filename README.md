# Portfolio — Harinand AS

A single-file portfolio site. No framework, no build step, no dependencies.

**Live:** https://techspell01.github.io/portfolio/

---

## Files

| File | What it is |
|---|---|
| `index.html` | **The whole site.** HTML, CSS, JS and the portrait all in one file. This is the file you edit and the file GitHub Pages serves. |
| `og-card.png` | The 1200×630 preview image LinkedIn, WhatsApp and Slack show when the link is pasted. Referenced by `og:image`. |
| `portrait.jpg` | The cropped photo. The site doesn't load it — the image is embedded inside `index.html` — but `og-card.png` is built from it. |
| `tools/embed_photo.py` | Swaps in a different portrait. |
| `tools/make_og_card.py` | Rebuilds `og-card.png`. Downloads the fonts on first run. |
| `tools/make_artifact.py` | Regenerates the Claude preview version. Not needed for deploying. |
| `.nojekyll` | Tells GitHub Pages to serve the files as-is instead of running Jekyll. |

The photo is a base64 `data:` URI inside `index.html`. That's why there's no images folder — the site is genuinely one file you could email to someone.

---

## Deploying a change

```bash
git add -A
git commit -m "what changed"
git push
```

GitHub Pages rebuilds automatically. Give it 30–60 seconds, then hard-refresh
(`Ctrl+Shift+R`) — the browser caches the old page aggressively.

To preview before pushing, just open `index.html` in a browser. Everything works
from `file://` — there is no server to run.

---

## Editing

Open `index.html` in any editor and search for the landmark text below.

### Contact details
Search `mailto:` — email, phone (`tel:`) and LinkedIn are three `<a class="ccard">`
links next to each other.

### Add a project
Find `<!-- ==================== WORK ====================` and copy an existing
`<article class="tile tinted s6">` block.

**The one rule that matters:** inside a `.bento` grid, the `s3`…`s12` classes are
column widths out of 12, and **each row must add up to 12.** The Work grid currently
runs `12` / `6+6` / `4+4+4` / `8+4`. If you add a tile without rebalancing, you get a
half-empty row.

### Change a card's colour
Each tile carries its own accent as `style="--c:240 128 42"` — plain **R G B**
numbers, no `rgb()`, no commas. The tint, border, chips and hover glow all derive
from it. Existing hues:

| | |
|---|---|
| `240 128 42` saffron | `224 69 123` rose |
| `15 168 150` teal | `124 92 255` violet |
| `236 90 82` coral | `31 169 196` cyan |
| `66 99 235` indigo | `168 200 30` lime |

### Move the final-year project forward
In the capstone section, the current phase is `<div class="phase now">`. Move the
`now` class to whichever phase you've reached. Also update the
`<span class="pill when">Plan v1 · Aug 2026</span>` above it.

### Update the numbers
The hero stats animate up to whatever is in `data-count="10"`. Change the number
there, and change the visible text next to it to match.

### Add a section
Three places must agree, or the roadmap rail breaks:
1. `<section class="section" id="yourid">`
2. the `SEC` array near the top of the `<script>` — `{id:'yourid', label:'LABEL', c:'R G B'}`
3. a `<a href="#yourid">` in `<nav class="nav">`

Keep rail labels to about 8 characters — longer ones overflow the 112px rail.

### Replace the photo
```bash
python tools/embed_photo.py "C:/path/to/new-photo.jpg"
```
Check `portrait.jpg` afterwards to see the crop it chose. If the framing is off,
run it again with explicit pixel coordinates from the original image:
```bash
python tools/embed_photo.py "C:/path/to/new-photo.jpg" --box 175 505 675 1172
```

### Update the link-preview card
The text on `og-card.png` lives at the top of `tools/make_og_card.py` (`EYEBROW`,
`NAME`, `LEAD`, `CHIPS`, `URL`). Edit those, then:
```bash
python tools/make_og_card.py
```
Commit the new `og-card.png` and push. **Social sites cache previews hard** — after
pushing, paste your URL into these to force a refresh:

- LinkedIn — https://www.linkedin.com/post-inspector/
- Facebook / WhatsApp — https://developers.facebook.com/tools/debug/
- Twitter/X — https://cards-dev.twitter.com/validator

If you change the site's headline, change the card's `LEAD` to match — a preview
that contradicts the page looks worse than no preview.

---

## How the page is built

- **Themes.** Every colour is a CSS custom property defined in `:root`. Dark mode
  redefines only the tokens, in two places — a `prefers-color-scheme` media query
  and a `[data-theme="dark"]` block — so both the OS setting and the manual toggle
  work. Never hard-code a colour in a rule; add a token.
- **The roadmap rail.** The winding road is generated in JS at the viewport's real
  pixel size, so it never distorts. Milestone dots are positioned at each section's
  actual share of the page scroll, so the rail is a true map of where you are. Below
  1000px it becomes a dock at the bottom of the screen.
- **3D tilt** is a shared `perspective` on each `.bento` with per-tile
  `rotateX/rotateY` from the pointer. Disabled on touch devices and for anyone with
  reduced-motion turned on.
- **Reveal on scroll** only hides tiles that start below the fold, so the page is
  never blank on first paint or in a link preview.
- **Glass buttons** use `backdrop-filter` plus an inset top highlight and a `::before`
  sheen. All of it runs through the `--glass-*` tokens.

## Gotchas

- `_artifact.html` is generated and git-ignored. Don't edit it.
- Fonts come from Google Fonts over the network — the page falls back to system
  faces offline, which looks different but stays readable.
- Editing the embedded photo's base64 by hand will corrupt it. Use the script.
