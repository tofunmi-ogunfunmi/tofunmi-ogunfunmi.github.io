"""
Pulls the 7 embedded (base64) microscopy images out of your OLD index.html
and saves them to images/gallery/ so the new index.html can find them.

Usage (run from your website folder):
    python extract_gallery_images.py old_index.html
Optional: add --inline to also write index_single_file.html, which puts the
images back inside the new page as data URIs (no images/ folder needed).
"""
import base64, os, re, sys

NAMES = ["0-sem-eds-cross-section", "1-fib-sem-tomography", "2-bse-sem-ag-eds",
         "3-sem-fracture", "4-dic-strain", "5-sem-microstructure", "6-sem-nmc-rgo"]

old = open(sys.argv[1], encoding="utf-8").read()
os.makedirs("images/gallery", exist_ok=True)
uris = {}
for i, name in enumerate(NAMES):
    m = re.search(r'id="gimg%d"\s+src="(data:image/(\w+);base64,([^"]+))"' % i, old)
    if not m:
        print("Could not find image gimg%d" % i); continue
    uri, ext, b64 = m.groups()
    ext = "jpg" if ext == "jpeg" else ext
    path = "images/gallery/%s.%s" % (name, ext)
    open(path, "wb").write(base64.b64decode(b64))
    uris["images/gallery/%s.jpg" % name] = uri
    print("Saved", path)

if "--inline" in sys.argv:
    new = open("index.html", encoding="utf-8").read()
    for path, uri in uris.items():
        new = new.replace('"%s"' % path, '"%s"' % uri)
    open("index_single_file.html", "w", encoding="utf-8").write(new)
    print("Wrote index_single_file.html")
