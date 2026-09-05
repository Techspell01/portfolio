"""
Replace the portrait in index.html with a different photo.

    python tools/embed_photo.py path/to/photo.jpg
    python tools/embed_photo.py path/to/photo.jpg --box 175 505 675 1172

The photo is embedded directly into index.html as a base64 data: URI, which is
why the site stays a single file with no image folder to deploy.

With no --box, the script takes a 3:4 portrait crop from the horizontal centre,
starting a little below the top - a reasonable guess for a head-and-shoulders
shot. If the framing comes out wrong, run it again with explicit
--box LEFT TOP RIGHT BOTTOM pixel coordinates from the original image.

Requires Pillow:  pip install pillow
"""
import base64, io, os, re, sys

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is not installed. Run:  pip install pillow")

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INDEX = os.path.join(HERE, "index.html")

args = [a for a in sys.argv[1:]]
if not args:
    sys.exit(__doc__)

photo = args[0]
box = None
if "--box" in args:
    i = args.index("--box")
    try:
        box = tuple(int(v) for v in args[i + 1:i + 5])
        if len(box) != 4:
            raise ValueError
    except ValueError:
        sys.exit("--box needs four integers: LEFT TOP RIGHT BOTTOM")

im = Image.open(photo).convert("RGB")
W, H = im.size

if box is None:
    # 3:4 portrait, centred horizontally, starting 15% down
    top = int(H * 0.15)
    avail_h = H - top
    crop_h = min(avail_h, int(W * 4 / 3))
    crop_w = int(crop_h * 3 / 4)
    left = max(0, (W - crop_w) // 2)
    box = (left, top, left + crop_w, top + crop_h)

crop = im.crop(box)
if crop.width > 620:                       # cap the embedded size
    crop = crop.resize((620, int(620 * crop.height / crop.width)), Image.LANCZOS)

buf = io.BytesIO()
crop.save(buf, "JPEG", quality=82, optimize=True, progressive=True)
uri = "data:image/jpeg;base64," + base64.b64encode(buf.getvalue()).decode()

html = io.open(INDEX, encoding="utf-8").read()
new, n = re.subn(r'src="data:image/[^"]*"', 'src="' + uri + '"', html, count=1)
if not n:
    sys.exit("Could not find the existing portrait in index.html "
             '(looked for src="data:image/...").')

io.open(INDEX, "w", encoding="utf-8").write(new)
crop.save(os.path.join(HERE, "portrait.jpg"), quality=90)
print("Embedded %s  crop=%s  size=%dx%d  %d KB"
      % (os.path.basename(photo), box, crop.width, crop.height, len(buf.getvalue()) // 1024))
print("Saved the crop to portrait.jpg so you can check the framing.")
