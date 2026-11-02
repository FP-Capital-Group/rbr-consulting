# Versione TIPOGRAFIA delle carte: ogni pagina A4 (210x297) su 216x303 mm = 3 mm di abbondanza per lato.
# L'abbondanza prende il colore del bordo della pagina (rosso pieno sulle pagine rosse, bianco sulle altre),
# così dopo il taglio non resta il filo bianco. Uso: python3 stampa_abbondanza.py in.pdf out.pdf
import io, sys, subprocess, tempfile, os
from pypdf import PdfReader, PdfWriter, Transformation
from reportlab.pdfgen import canvas
from PIL import Image
MM = 72 / 25.4; B = 3 * MM
src = sys.argv[1]; rd = PdfReader(src); wr = PdfWriter()
tmp = tempfile.mkdtemp()
subprocess.run(['pdftoppm', '-png', '-r', '20', src, os.path.join(tmp, 'p')], check=True)
imgs = sorted(f for f in os.listdir(tmp) if f.endswith('.png'))
for i, pg in enumerate(rd.pages):
    w, h = float(pg.mediabox.width), float(pg.mediabox.height)
    im = Image.open(os.path.join(tmp, imgs[i])).convert('RGB'); W, H = im.size
    px = [im.getpixel((x, y)) for x in range(W) for y in (0, H - 1)] + [im.getpixel((x, y)) for y in range(H) for x in (0, W - 1)]
    col = [sum(c[k] for c in px) / len(px) / 255 for k in range(3)]
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(w + 2 * B, h + 2 * B))
    c.setFillColorRGB(*col); c.rect(0, 0, w + 2 * B, h + 2 * B, stroke=0, fill=1); c.save()
    bg = PdfReader(buf).pages[0]
    bg.merge_transformed_page(pg, Transformation().translate(B, B))
    wr.add_page(bg)
wr.compress_identical_objects(); wr.write(sys.argv[2])
print('OK', sys.argv[2], len(rd.pages), 'pagine', round((w + 2 * B) / MM), 'x', round((h + 2 * B) / MM), 'mm')

