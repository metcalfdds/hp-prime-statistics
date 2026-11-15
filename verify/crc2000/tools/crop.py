# crop.py (set CRC_PDF to the book's PDF) PAGE "text to find" OUT.png [left right up down] [zoom] : render the part of a page around the first hit of a text
import sys, os, fitz
fitz.TOOLS.mupdf_display_errors(False)
pno = int(sys.argv[1]); key = sys.argv[2]; out = sys.argv[3]
l, r, u, d = [float(x) for x in sys.argv[4:8]] if len(sys.argv) >= 8 else (40, 300, 20, 60)
zoom = float(sys.argv[8]) if len(sys.argv) > 8 else 2.5
doc = fitz.open(os.environ['CRC_PDF'])           # the reader's own copy of the book
pg = doc[pno - 1]
hits = pg.search_for(key)
if not hits:
    print('no hit for', key, 'page rect', pg.rect, 'rotation', pg.rotation); sys.exit(1)
h = hits[int(sys.argv[9]) if len(sys.argv) > 9 else 0]
clip = fitz.Rect(h.x0 - l, h.y0 - u, h.x1 + r, h.y1 + d) & pg.rect
pix = pg.get_pixmap(matrix=fitz.Matrix(zoom, zoom), clip=clip)
pix.save(out)
print(out, pix.width, pix.height, 'hits', len(hits))
