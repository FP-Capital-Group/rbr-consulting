# -*- coding: utf-8 -*-
"""Foto ChatGPT (~/Downloads/menu_<nome>.png) -> originale in foto_chatgpt/ + versione scontornata trasparente in img/<nome>.png.
Uso: tools/.venv_rembg/bin/python prep_foto.py   (lavora solo sui file nuovi)"""
import os, glob, shutil
from PIL import Image
from rembg import remove, new_session
B = os.path.dirname(os.path.abspath(__file__))
S = None
for f in sorted(glob.glob(os.path.expanduser('~/Downloads/menu_*.png'))):
    nome = os.path.basename(f)[5:-4]
    orig = os.path.join(B, 'foto_chatgpt', nome + '.png'); out = os.path.join(B, 'img', nome + '.png')
    if not os.path.exists(orig):
        shutil.move(f, orig)
    else:
        os.remove(f)
    if nome == 'g_aggiunte':                      # un'immagine 3:1 -> tre tondi
        im = Image.open(orig).convert('RGB'); w3 = im.width // 3
        for k, n in enumerate(['g_agg_bacon', 'g_agg_cheddar', 'g_agg_guanciale']):
            t = im.crop((k*w3, 0, (k+1)*w3, im.height)); s = min(t.size)
            t = t.crop(((t.width-s)//2, (t.height-s)//2, (t.width+s)//2, (t.height+s)//2)).resize((600, 600))
            t.save(os.path.join(B, 'img', n + '.png')); print('OK tondo', n)
        continue
    if nome.endswith('_t') and os.path.exists(os.path.join(B, 'img', nome[:-2] + '.png')) and os.path.getmtime(os.path.join(B, 'img', nome[:-2] + '.png')) > os.path.getmtime(orig):
        continue
    if nome.endswith('_t') and Image.open(orig).mode != 'RGBA':
        out = os.path.join(B, 'img', nome[:-2] + '.png')   # scacchiera finta: scontorna con rembg
    elif nome.endswith('_t'):                       # PNG trasparente fatto da ChatGPT: solo ritaglio
        im = Image.open(orig).convert('RGBA'); im = im.crop(im.split()[3].point(lambda v: 255 if v > 8 else 0).getbbox())
        im.thumbnail((1100, 1100)); im.save(os.path.join(B, 'img', nome[:-2] + '.png'), optimize=True)
        print('OK trasparente', nome[:-2], im.size); continue
    if os.path.exists(out):
        continue
    S = S or new_session('birefnet-general')
    im = Image.open(orig).convert('RGB'); im.thumbnail((1400, 1400))
    cut = remove(im, session=S, post_process_mask=True)
    cut = cut.crop(cut.getbbox())
    if nome.startswith(('g_agg', 'a_agg')):        # aggiunte: tondo pieno, niente scontorno
        im2 = Image.open(orig).convert('RGB'); s = min(im2.size)
        im2 = im2.crop(((im2.width - s)//2, (im2.height - s)//2, (im2.width + s)//2, (im2.height + s)//2)).resize((700, 700))
        im2.save(out); print('OK tondo', nome); continue
    cut.thumbnail((1100, 1100)); cut.save(out, optimize=True); print('OK', nome, cut.size)

