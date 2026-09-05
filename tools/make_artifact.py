"""
Regenerates _artifact.html from index.html.

index.html is the real site - the file you edit and the file GitHub Pages serves.
Claude's Artifact preview needs the same page WITHOUT the <!doctype>/<html>/<head>/<body>
wrapper (it supplies its own), so this script strips that and writes _artifact.html.

You only need this if you want the claude.ai preview link refreshed.
Deploying to GitHub Pages does not need it at all.

    python tools/make_artifact.py
"""
import io, os, sys

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = os.path.join(HERE, "index.html")
dst = os.path.join(HERE, "_artifact.html")

html = io.open(src, encoding="utf-8").read()

try:
    start = html.index("<title>")
    head_end = html.index("</style>", start) + len("</style>")
    body_start = html.index("<body>") + len("<body>")
    body_end = html.rindex("</body>")
except ValueError:
    sys.exit("index.html is missing <title>, </style>, or <body> - cannot split it.")

head = html[start:head_end]
body = html[body_start:body_end].strip()

io.open(dst, "w", encoding="utf-8").write(head + "\n\n" + body + "\n")
print("wrote _artifact.html (%d KB) from index.html" % (os.path.getsize(dst) // 1024))
