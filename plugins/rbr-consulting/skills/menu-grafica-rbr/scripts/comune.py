# -*- coding: utf-8 -*-
"""Funzioni comuni alle carte Giurges e Antipapa (regole RBR ottobre 2026).

Regole applicate (da Cartabianca, decise da Marco):
- max 7 voci per categoria; ordine per margine: n.2 primo, n.1 secondo, poi a scendere, n.3 IN FONDO
- evidenziato solo il n.1 (cornice sottile) e foto solo sul n.1
- prezzo piccolo, stesso carattere della descrizione, «descrizione | 14,5»: niente €, niente ,00, max un decimale
- abbinamento (birra/vino) solo sui primi due della lista
- niente occhielli, sottotitoli, badge; testo legale piccolo su ogni pagina
"""
import os, html

BASE = os.path.dirname(os.path.abspath(__file__))
IMG = os.path.join(BASE, 'foto_vere')  # SOLO foto vere del cliente (Instagram/locale). Le ChatGPT in img/ non si usano più (07/10)


def pf(x):
    """14.0 -> '14' · 14.5 -> '14,5' · 1.5 -> '1,5'"""
    if isinstance(x, str):
        return x
    x = round(float(x), 1)
    return str(int(x)) if x == int(x) else f'{x:.1f}'.replace('.', ',')


def e(s):
    return html.escape(s or '', quote=False)


def ordina(piatti):
    """piatti con chiave 'm' (margine, None = sconosciuto). Ordine RBR: n.2, n.1, n.4…, n.3 in fondo.
    I piatti senza margine restano in coda nell'ordine dato (prima del n.3)."""
    noti = sorted([p for p in piatti if p.get('m') is not None], key=lambda p: -p['m'])
    ignoti = [p for p in piatti if p.get('m') is None]
    for i, p in enumerate(noti):
        p['rank'] = i + 1
    if len(noti) >= 3:
        out = [noti[1], noti[0]] + noti[3:] + ignoti + [noti[2]]
    elif len(noti) == 2:
        out = [noti[1], noti[0]] + ignoti
    else:
        out = noti + ignoti
    return out


def foto(nome):
    """percorso relativo della FOTO VERA se esiste in foto_vere/, altrimenti None (niente segnaposto)"""
    for ext in ('jpg', 'png', 'webp'):
        f = os.path.join(IMG, f'{nome}.{ext}')
        if os.path.exists(f):
            return f'foto_vere/{nome}.{ext}'
    return None

