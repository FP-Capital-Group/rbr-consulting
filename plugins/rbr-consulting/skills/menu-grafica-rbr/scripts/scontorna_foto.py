# -*- coding: utf-8 -*-
"""Foto piatto da menu, GRATIS e in locale (rembg, niente API a pagamento).
Toglie lo sfondo a una foto vera (anche dal telefono) e la mette su bianco puro con un riflesso morbido «su vetro»,
come le foto delle carte Tennis/Club. Il piatto resta quello vero: niente ritocchi AI.
Uso:  tools/.venv_rembg/bin/python tools/scontorna_foto.py <foto.jpg> <uscita.png> [--quadrata] [--senza-riflesso]
Modello birefnet-general (~900 MB, già scaricato in ~/.rembg/models). Ambiente: tools/.venv_rembg (Python 3.12, creato con uv)."""
import sys
from PIL import Image, ImageFilter, ImageOps
from rembg import remove, new_session
import os
MODELLO = os.environ.get('REMBG_MODELLO', 'birefnet-general')  # il più preciso (anche bianco su bianco); più leggero: isnet-general-use

def scontorna(src, out, quadrata=False, riflesso=True):
    im = ImageOps.exif_transpose(Image.open(src)).convert('RGB')
    im.thumbnail((2200, 2200))
    cut = remove(im, session=new_session(MODELLO), post_process_mask=True)
    cut = cut.crop(cut.getbbox())
    w, h = cut.size
    W = int(w * 1.18); H = int(W * (1 if quadrata else 0.75))
    if h * 1.45 > H:                      # piatto alto: allarga la tela
        H = int(h * 1.45); W = int(H / (1 if quadrata else 0.75))
    tela = Image.new('RGBA', (W, H), (255, 255, 255, 255))
    x = (W - w) // 2; y = int((H - h) * (0.30 if riflesso else 0.5))
    # ombra morbida sotto il piatto
    ombra = Image.new('RGBA', (w, h), (0, 0, 0, 0)); a = cut.split()[3].point(lambda v: int(v * 0.22))
    ombra.putalpha(a); ombra = ombra.resize((w, max(1, h // 6))).filter(ImageFilter.GaussianBlur(max(4, w // 40)))
    tela.alpha_composite(ombra, (x, y + h - ombra.size[1] // 2))
    if riflesso:                          # riflesso capovolto che sfuma
        rif = ImageOps.flip(cut).crop((0, 0, w, int(h * 0.35)))
        grad = Image.linear_gradient('L').resize(rif.size).point(lambda v: int((255 - v) * 0.18))
        ra = rif.split()[3]; rif.putalpha(Image.composite(grad, Image.new('L', rif.size, 0), ra))
        tela.alpha_composite(rif, (x, y + h + 2))
    tela.alpha_composite(cut, (x, y))
    tela.convert('RGB').save(out, quality=92)
    print('OK', out, tela.size)

if __name__ == '__main__':
    a = [x for x in sys.argv[1:] if not x.startswith('--')]
    scontorna(a[0], a[1], quadrata='--quadrata' in sys.argv, riflesso='--senza-riflesso' not in sys.argv)

