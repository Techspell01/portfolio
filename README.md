# Portfolio — Harinand AS

A single-file portfolio site that plays like a streaming series: an opening title
sequence, a "Who's watching?" screen, projects as Originals, the journey as
Seasons, a Top 10 and a "To be continued…" ending. No framework, no build step,
no dependencies.

**Live:** https://techspell01.github.io/portfolio/

---

## Files

| File | What it is |
|---|---|
| `index.html` | **The whole site.** HTML, CSS, JS and the portrait all in one file. This is the file you edit and the file GitHub Pages serves. |
| `og-card.png` | The 1200×630 preview image LinkedIn, WhatsApp and Slack show when the link is pasted. Referenced by `og:image`. |
| `portrait.jpg` | The cropped photo. The site doesn't load it — the image is embedded inside `index.html` — but `og-card.png` is built from it. |
| `Harinand-AS-Resume.pdf` | The résumé the nav, hero (Recruiter profile) and Credits link to. |
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
from `file://` — there is no server to run. Add `?skip` to the URL to go straight
past the opening and the profile screen.

---

## Editing

**Almost all content is data near the top of the `<script>` at the bottom of
`index.html`.** Change it there and every card, overlay and rail picks it up.

| To change… | Edit |
|---|---|
| A project (title, logline, numbers, story, stack, links) | `TITLES` — the six with `featured:true` are the Originals; the rest are "More titles" |
| Which projects appear in "More titles", and their order | `MORE` |
| The "Who's watching?" profiles, the Originals order and section order per profile | `PROFILES` (`og` = Originals order, `secs` = section order) |
| The journey | `SEASONS` — each season has `eps` (episodes); `open:'voc'` adds a ▶ that opens that project |
| The Top 10 row | `TOP10` — `[project id, label, big number, line]` |
| Skills | `GENRES` — `seen` lists the project ids it shows up in |
| The ▶ Play Intro highlight reel | `REEL` |
| The "Continue Exploring" cards | `SECMETA` |

Things that are plain HTML instead: the hero (search `BILLBOARD`), the Credits
cards (search `CREDITS`) and the contact links (search `TO BE CONTINUED`).

### Counts
"15 titles · 7 live · 2 internships" appears in the hero meta row, the `REEL`, the
`TOP10`, the meta description and `og-card.png`. Change them together.

### Colours
One accent drives the whole site: `--acc`, `--acc-2` and `--acc-rgb` in `:root`.
Each project's key art takes its own palette from `pal:[dark, mid, deepest, accent]`
in `TITLES`, and a motif from `motif:` (drawn by the `motif()` function).

### Replace the photo
```bash
python tools/embed_photo.py "C:/path/to/new-photo.jpg"
```
Check `portrait.jpg` afterwards to see the crop it chose. If the framing is off,
run it again with explicit pixel coordinates from the original image:
```bash
python tools/embed_photo.py "C:/path/to/new-photo.jpg" --box 175 505 675 1172
```
The photo is embedded once, in the billboard `<img id="portrait">`; the opening,
the profile avatar and the intro reel all reuse it.

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

---

## How the page is built

- **Stages.** First visit in a browser session: opening titles → "Who's watching?"
  → home. The chosen profile is kept in `sessionStorage`, so a reload goes straight
  home. "Replay opening" at the bottom runs it again.
- **Originals** pin on desktop and scroll sideways as you scroll down; on touch,
  small screens and reduced motion they're a normal swipe row.
- **Key art** is generated: layered gradients plus an SVG motif per project. No
  stock images.
- **Reduced motion** is respected: no grain, no pinned scroll, no reveal animations,
  and the opening jumps to its last frame.
- It's a streaming-*style* page and uses no streaming service's name or logo.

## Gotchas

- `_artifact.html` is generated and git-ignored. Don't edit it.
- Fonts (Bebas Neue, Inter) come from Google Fonts — offline the page falls back
  to system faces, which looks different but stays readable.
- Editing the embedded photo's base64 by hand will corrupt it. Use the script.
