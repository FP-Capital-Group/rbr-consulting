# -*- coding: utf-8 -*-
"""BOZZA volantino «Il brunch» — pilota SOLO a Panciatichi (08/10/2026).
Marco 07/10: togliere il brunch da tutte le grafiche e fare un volantino a parte per Panciatichi; i piatti (6-8) li sceglie Emiliano.
Quindi questa è solo la STRUTTURA: 8 posti piatto, dentro solo ciò che è già in Cassa in Cloud (avocado toast, omelette,
tagliere della terra: prezzi = libro bar del 07/10) + pancake da prodotto pronto (Emiliano 07/10, prezzo da definire);
gli altri posti restano vuoti e il foglio porta la scritta BOZZA finché Emiliano non manda piatti, prezzi e orari.
Niente uovo alla Benedict (Emiliano 07/10) e quindi niente foto con la Benedict: foto = avocado toast.
Stile = libro del bar (Eataly: Cormorant/EB Garamond, marroncino, fondo crema). Non tocca gli altri script né i loro PDF.
Uso: python3 build_volantino_brunch_bozza.py [uscita.pdf]"""
import html, os, sys
from weasyprint import HTML
import build_grafiche as g
import build_libro_bar as lb

b = g.b
HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
eur = b.eur
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'Volantino_Brunch_Panciatichi_BOZZA.pdf')

# piatti già in cassa (stessi dati del libro bar Panciatichi del 07/10)
IN_CASSA = [(v['nome'], v['sub'], eur(v['prezzo'])) for v in lb.PIATTI_BRUNCH]
POSTI = IN_CASSA + [('Pancake', 'prodotto pronto, con le guarnizioni da scegliere', None)] + [None] * 4  # 8 posti in tutto

def riga(i, p):
    if p is None:
        return (f'<div class="r vuoto"><p class="num">{i}</p><div><p class="nm">piatto da definire</p>'
                f'<p class="d">lo sceglie Emiliano · nome, ingredienti e prezzo</p></div></div>')
    nome, desc, prezzo = p
    coda = f' <span class="sep">|</span> <span class="pz">{prezzo}</span>' if prezzo else ' <span class="sep">|</span> <span class="manca">prezzo da definire</span>'
    tag = '<span class="tag">già in cassa</span>' if prezzo else '<span class="tag no">da creare in cassa</span>'
    return (f'<div class="r"><p class="num">{i}</p><div><p class="nm">{E(nome)} {tag}</p>'
            f'<p class="d">{E(desc)}{coda}</p></div></div>')

righe = ''.join(riga(i + 1, p) for i, p in enumerate(POSTI))
meta = len(POSTI) // 2
CORPO = (f'<div class="due"><div>{"".join(riga(i + 1, p) for i, p in enumerate(POSTI[:meta]))}</div>'
         f'<div>{"".join(riga(i + 1 + meta, p) for i, p in enumerate(POSTI[meta:]))}</div></div>')

CSS = r"""
@page{size:210mm 297mm;margin:0}
:root{--fondo:#FFFDF9;--titolo:#4A2617;--nome:#8A5A2B;--testo:#4A3A2E;--soft:#8C7A6A;--linea:#E7DCCB;--crema:#F4EDE1;--rosso:#A6192E;
  --serif:'Cormorant Garamond','EB Garamond',Garamond,Georgia,serif;--tf:'EB Garamond',Garamond,Georgia,serif}
*{box-sizing:border-box} html,body{margin:0;background:var(--fondo)} body{font-family:var(--tf);color:var(--testo)} p{margin:0}
.pag{position:relative;width:210mm;height:297mm;overflow:hidden;background:var(--fondo)}
.pag::before{content:"";position:absolute;top:6mm;left:6mm;right:6mm;bottom:6mm;border:.5pt solid var(--linea)}
.bozza-fascia{position:absolute;top:0;left:0;right:0;background:var(--rosso);color:#fff;text-align:center;padding:2.6mm 10mm;
  font-family:var(--tf);font-size:10pt;letter-spacing:.04em;z-index:3}
.bozza-fascia b{letter-spacing:.2em}
.filigrana{position:absolute;top:118mm;left:-20mm;right:-20mm;text-align:center;transform:rotate(-28deg);font-family:var(--serif);
  font-size:150pt;font-weight:600;letter-spacing:.12em;color:var(--rosso);opacity:.07;z-index:2}
.c{position:relative;padding:22mm 18mm 0;text-align:center;z-index:1}
.occ{font-family:var(--serif);font-style:italic;font-weight:500;font-size:16pt;color:var(--titolo)}
h1{margin:1mm 0 0;font-family:var(--serif);font-weight:500;font-size:46pt;letter-spacing:.12em;text-transform:uppercase;color:var(--titolo);line-height:1}
.sotto{margin-top:2mm;font-family:var(--serif);font-style:italic;font-size:14pt;color:var(--nome)}
.ft{display:block;height:62mm;width:auto;max-width:150mm;margin:6mm auto 2mm;object-fit:contain}
.due{display:flex;gap:9mm;text-align:left;margin-top:5mm}
.due>div{flex:1 1 0;min-width:0}
.r{display:flex;gap:3mm;align-items:flex-start;padding:2.4mm 0;border-bottom:.5pt solid var(--linea);min-height:15mm}
.num{flex:0 0 6mm;font-family:var(--serif);font-size:13pt;color:var(--soft);line-height:1.2}
.nm{font-family:var(--serif);font-weight:600;font-size:11pt;letter-spacing:.06em;text-transform:uppercase;color:var(--nome)}
.d{font-style:italic;font-size:10pt;line-height:1.3;margin-top:.4mm}
.sep{color:var(--linea);font-style:normal}
.pz{font-style:normal;font-size:9pt;color:var(--soft)}
.manca{font-style:normal;font-size:8.6pt;color:var(--rosso)}
.tag{display:inline-block;margin-left:1.5mm;padding:.2mm 1.6mm;border:.5pt solid var(--soft);border-radius:2mm;font-family:var(--tf);
  font-weight:400;font-size:6.8pt;letter-spacing:.04em;text-transform:none;color:var(--soft);vertical-align:middle}
.tag.no{border-color:var(--rosso);color:var(--rosso)}
.vuoto .nm,.vuoto .d{color:#B9A99A}
.vuoto{border-bottom:.5pt dashed #CDBBA8}
.combo{background:var(--crema);padding:3mm 6mm;margin:7mm 10mm 0;text-align:center}
.combo .ct{font-family:var(--serif);font-weight:600;font-size:9.6pt;letter-spacing:.16em;text-transform:uppercase;color:var(--nome)}
.combo .cd{margin-top:.6mm;font-style:italic;font-size:11pt}
.orari{margin-top:6mm;font-family:var(--serif);font-size:11pt;letter-spacing:.2em;text-transform:uppercase;color:var(--rosso)}
.logo{position:absolute;left:0;right:0;bottom:16mm;text-align:center;z-index:1}
.logo img{height:11mm;width:auto}
.logo p{margin-top:2.5mm;font-family:var(--serif);font-size:9.5pt;letter-spacing:.22em;text-transform:uppercase;color:var(--nome)}
"""

DOC = (f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Volantino brunch Panciatichi · BOZZA</title>{g.FONTS}<style>{CSS}</style></head><body>'
       '<section class="pag">'
       '<div class="bozza-fascia"><b>BOZZA</b> · struttura del volantino · i piatti definitivi (6-8), i prezzi e gli orari li manda Emiliano · non stampare</div>'
       '<div class="filigrana">BOZZA</div>'
       '<div class="c">'
       '<p class="occ">colazione salata e brunch</p><h1>Il brunch</h1><p class="sotto">solo a Panciatichi</p>'
       f'{g.foto("avocado_toast", "ft")}'
       f'{CORPO}'
       f'<div class="combo"><p class="ct">Il brunch completo</p><p class="cd">un piatto a scelta con spremuta d’arancia e cappuccino '
       f'<span class="sep">|</span> <span class="pz">+ {eur(b.SPR + b.CAPPU)}</span></p></div>'
       '<p class="orari">giorni e orari del brunch: da definire</p>'
       '</div>'
       f'<div class="logo"><img src="{b.LOGO}" alt="Cartabianca Cafè"><p>Cartabianca Panciatichi</p></div>'
       '</section></body></html>')

if __name__ == '__main__':
    HTML(string=DOC, base_url=HERE).write_pdf(OUT)
    from pypdf import PdfReader
    print('OK', OUT, len(PdfReader(OUT).pages), 'pagina')

