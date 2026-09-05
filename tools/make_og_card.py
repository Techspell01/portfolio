"""
Generates og-card.png - the 1200x630 preview image that LinkedIn, WhatsApp,
Slack and Twitter show when someone pastes the portfolio link.

    python tools/make_og_card.py

Reads the portrait from portrait.jpg and the fonts from tools/fonts/.
Rerun it whenever the headline text below changes, then commit og-card.png.

Requires Pillow:  pip install pillow
"""
import os, sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageFilter
except ImportError:
    sys.exit("Pillow is not installed. Run:  pip install pillow")

HERE  = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTS = os.path.join(HERE, "tools", "fonts")

# The card uses the same three faces as the site. They are fetched from the
# upstream Google Fonts repo on first run rather than committed, so the repo
# stays small. Needs a network connection the first time only.
FONT_SOURCES = {
    "Bricolage-var.ttf":  "ofl/bricolagegrotesque/BricolageGrotesque[opsz,wdth,wght].ttf",
    "Instrument-var.ttf": "ofl/instrumentsans/InstrumentSans[wdth,wght].ttf",
    "DMMono-500.ttf":     "ofl/dmmono/DMMono-Medium.ttf",
}

def ensure_fonts():
    import urllib.request
    from urllib.parse import quote
    base = "https://raw.githubusercontent.com/google/fonts/main/"
    os.makedirs(FONTS, exist_ok=True)
    for name, path in FONT_SOURCES.items():
        dest = os.path.join(FONTS, name)
        if os.path.exists(dest) and os.path.getsize(dest) > 10000:
            continue
        print("downloading", name, "...")
        try:
            data = urllib.request.urlopen(base + quote(path, safe="/"), timeout=60).read()
        except Exception as e:
            sys.exit("Could not download %s (%s). Check your connection." % (name, e))
        if data[:4] != b"\x00\x01\x00\x00":
            sys.exit("%s did not come back as a TrueType file." % name)
        open(dest, "wb").write(data)

ensure_fonts()

# ---- content -------------------------------------------------------------
EYEBROW = "PRODUCT ENGINEER  ·  KERALA, INDIA"
NAME    = "Harinand AS"
LEAD    = ("Ten projects shipped since March 2026, four of them live. "
           "Now building an offline capsize detector for Kerala fishing boats.")
CHIPS   = ["React", "TypeScript", "Expo", "Gemini", "LangGraph", "Python"]
URL     = "techspell01.github.io/portfolio"

# ---- palette (matches the site's dark theme) ----------------------------
BG      = (11, 13, 20)
SURFACE = (22, 26, 38)
INK     = (237, 239, 248)
INK2    = (196, 201, 220)
MUTED   = (139, 146, 173)
ACCENT  = (255, 157, 77)
LINE    = (38, 43, 60)

W, H = 1200, 630
PAD   = 66

def font(name, size, axes=None):
    """axes must be given in the order the font declares them:
       Bricolage = [optical size, weight, width];  Instrument = [width, weight]."""
    f = ImageFont.truetype(os.path.join(FONTS, name), size)
    if axes:
        f.set_variation_by_axes(axes)
    return f

f_name   = font("Bricolage-var.ttf", 88, [96, 800, 100])
f_lead   = font("Instrument-var.ttf", 27, [100, 400])
f_eyebrow= font("DMMono-500.ttf", 19)
f_chip   = font("DMMono-500.ttf", 17)
f_url    = font("DMMono-500.ttf", 22)

card = Image.new("RGB", (W, H), BG)

# --- ambient glow, echoing the hero mesh ---------------------------------
glow = Image.new("RGB", (W, H), BG)
g = ImageDraw.Draw(glow)
g.ellipse([-180, -260, 460, 380], fill=(70, 40, 16))
g.ellipse([560, 300, 1180, 900], fill=(34, 24, 52))
card = Image.blend(card, glow.filter(ImageFilter.GaussianBlur(150)), 0.85)
d = ImageDraw.Draw(card)

# --- portrait, right side ------------------------------------------------
PX, PY, PW, PH = 762, PAD, 372, H - PAD * 2
port = Image.open(os.path.join(HERE, "portrait.jpg")).convert("RGB")
scale = max(PW / port.width, PH / port.height)
port = port.resize((round(port.width * scale), round(port.height * scale)), Image.LANCZOS)
left = (port.width - PW) // 2
top  = int((port.height - PH) * 0.10)          # bias upward, keeps the face high
port = port.crop((left, top, left + PW, top + PH))

mask = Image.new("L", (PW, PH), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, PW - 1, PH - 1], radius=26, fill=255)
card.paste(port, (PX, PY), mask)
d.rounded_rectangle([PX, PY, PX + PW - 1, PY + PH - 1], radius=26,
                    outline=(112, 76, 46), width=2)   # accent at low opacity over BG

# --- text column ---------------------------------------------------------
x = PAD
maxw = PX - PAD - 54

y = 132
d.text((x, y), EYEBROW, font=f_eyebrow, fill=MUTED)

y += 46
d.text((x, y), NAME, font=f_name, fill=INK)

y += 112
d.rounded_rectangle([x, y, x + 66, y + 5], radius=3, fill=ACCENT)

# wrap the lead paragraph
y += 34
words, line, lines = LEAD.split(), "", []
for w in words:
    t = (line + " " + w).strip()
    if d.textlength(t, font=f_lead) <= maxw:
        line = t
    else:
        lines.append(line); line = w
lines.append(line)
for ln in lines:
    d.text((x, y), ln, font=f_lead, fill=INK2)
    y += 38

# --- tech chips ----------------------------------------------------------
cy = H - 152
cx = x
for c in CHIPS:
    tw = d.textlength(c, font=f_chip)
    if cx + tw + 26 > PX - 54:
        break
    d.rounded_rectangle([cx, cy, cx + tw + 24, cy + 34], radius=9,
                        fill=SURFACE, outline=LINE, width=1)
    d.text((cx + 12, cy + 9), c, font=f_chip, fill=INK2)
    cx += tw + 34

# --- url -----------------------------------------------------------------
d.text((x, H - 88), URL, font=f_url, fill=ACCENT)

out = os.path.join(HERE, "og-card.png")
card.save(out, "PNG", optimize=True)
print("wrote og-card.png  %dx%d  %d KB" % (W, H, os.path.getsize(out) // 1024))
