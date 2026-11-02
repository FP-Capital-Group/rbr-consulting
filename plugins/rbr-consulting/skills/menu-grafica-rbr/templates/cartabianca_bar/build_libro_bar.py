# -*- coding: utf-8 -*-
"""Menu del bar Cartabianca A LIBRO (Marco + Luciano 06/10/2026): sostituisce la carta A4 da tavolo di build_bar_eataly.py.
4 facciate A4 verticali, stesso stile Eataly dei tabelloni (foto, font, colori, contenuti e prezzi di build_grafiche/build_formati):
  1. copertina pulita: scritta Cartabianca (senza tricolore, dubbio di Luciano), «i sommelier del caffè», foto del caffè
  2. interno sinistra: IN ALTO il caffè, IN BASSO la pasticceria
  3. interno destra:  IN ALTO il brunch (dove cade l'occhio, Luciano), IN BASSO il bar
  4. retro: logo ufficiale, «i sommelier del caffè», note (bevanda vegetale, allergeni, torte su ordinazione)
Regole: ordine per margine col n.1 al 2° posto (build_formati.ordina), un solo segno (cornice puntinata rossa) sul n.1,
le combo su fascia crema senza cornice; prezzi PREZZO FINALE via ../prezzi_live.json (lanciare prima ../prezzi_live.py);
senza zeri finali; niente marchi (Nutella, Red Bull, Campari tolti dai nomi); dove c'è la descrizione il prezzo va in fondo
alla descrizione («… | 9,5»), dove non c'è resta in colonna a destra.
07/10/2026: brunch rifatto SOLO con prodotti presenti in Cassa in Cloud; caffè, mignon, crema e salati allineati alla cassa
(vedi blocco «07/10/2026» sotto).
07/10/2026 (Marco + Emiliano): il brunch è SOLO un pilota a Panciatichi → DUE versioni del libro:
  · standard per gli altri 6 bar (OUT): interno destra = IL BAR su tutta la pagina (salati + toast e focaccine in alto, da bere in basso)
  · Panciatichi (OUT_PANC): come prima, brunch in alto + bar in basso (nessun uovo alla Benedict, nessun pancake «fatto in casa»)
Uso: python3 build_libro_bar.py  →  Menu_Bar_Libro_Cartabianca_2026.pdf + Menu_Bar_Libro_PANCIATICHI_Cartabianca_2026.pdf
Non tocca gli altri script né i loro PDF."""
import html, os
from weasyprint import HTML
import build_grafiche as g

b = g.b
HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
eur = b.eur
OUT = 'Menu_Bar_Libro_Cartabianca_2026.pdf'                         # 6 bar, senza brunch
OUT_PANC = 'Menu_Bar_Libro_PANCIATICHI_Cartabianca_2026.pdf'  # solo Panciatichi, con brunch

# niente marchi nei nomi (regola RBR): solo qui, gli altri formati restano come sono
SENZA_MARCHI = {'Crostata pistacchio e Nutella': 'Crostata pistacchio e nocciola', 'Red Bull': 'Energy drink', 'Campari soda': 'Bitter soda'}
def nome(n): n = g.pulisci(n); return SENZA_MARCHI.get(n, n)

def riga(v):
    uno = ' uno' if v['n1'] else ''
    if v.get('sub'):  # descrizione → prezzo in fondo alla descrizione (feedback Luciano 06/10)
        return (f'<div class="r ds{uno}"><p class="nm">{E(nome(v["nome"]))}</p>'
                f'<p class="d">{E(v["sub"])} <span class="sep">|</span> <span class="pz">{eur(v["prezzo"])}</span></p></div>')
    # senza descrizione: «NOME | prezzo» sulla stessa riga, mai in colonna (Marco 06/10)
    return f'<div class="r ds{uno}"><p class="nm">{E(nome(v["nome"]))} <span class="sep">|</span> <span class="pz">{eur(v["prezzo"])}</span></p></div>'

def lista(titolo, lst): return f'<div class="sez"><h2>{titolo}</h2>{"".join(riga(v) for v in b.ordina(lst))}</div>'

def misure(titolo, righe):
    """tazze in tre misure: niente tabella a colonne (Marco 06/10), le misure stanno sotto il nome come una descrizione"""
    pz = lambda x: f'<span class="pz">{eur(x)}</span>'
    out = ''
    for v in righe:
        uno = ' uno' if v['n1'] else ''
        if not v['md'] and not v['gr']:
            out += f'<div class="r ds{uno}"><p class="nm">{E(nome(v["nome"]))} <span class="sep">|</span> {pz(v["prezzo"])}</p></div>'
            continue
        m = [f'piccolo {pz(v["prezzo"])}'] + ([f'medio {pz(v["prezzo"] + v["md"])}'] if v['md'] else []) + ([f'grande {pz(v["prezzo"] + v["gr"])}'] if v['gr'] else [])
        out += f'<div class="r ds{uno}"><p class="nm">{E(nome(v["nome"]))}</p><p class="d">{" · ".join(m)}</p></div>'
    return f'<div class="sez"><h2>{titolo}</h2>{out}</div>'

def combo(titolo, testo, prezzo):
    return f'<div class="combo"><p class="ct">{titolo}</p><p class="cd">{testo} <span class="sep">|</span> <span class="pz">{prezzo}</span></p></div>'

def combo2(titolo, misure):
    """08/10: misure con prezzo ognuna, senza « | » solo sull'ultima"""
    return f'<div class="combo"><p class="ct">{titolo}</p><p class="cd">{misure}</p></div>'

def meta(cls, occ, titolo, foto, sx, dx, sotto=''):
    return (f'<div class="meta {cls}"><div class="mt"><div class="mt-t"><p class="occ">{occ}</p><h1>{titolo}</h1></div>{g.foto(foto, "mf")}</div>'
            f'<div class="due"><div class="c1">{sx}</div><div class="c2">{dx}</div></div>{sotto}</div>')

# ---- 07/10/2026: solo voci che la cassa ha davvero, prezzi = cassa o PREZZO FINALE (mai sotto la cassa) ----
# caffè macchiato: in cassa non esiste, si batte come «Caffe» 1,30 → una riga sola; crema di caffè in cassa 3,50 (non 3,40);
# mignon in cassa 1,20 (non 1,40); «Schiacciatina 12*18 club/tonno» cancellata dalla cassa → «Mezzaluna club o tonno» (foglio 6)
TAZZINE = [b.V('Caffè o caffè macchiato', 1.30, 0.17, cassa=True), b.V('Decaffeinato', 1.60, 0.20, cassa=True),
           b.V('Crema di caffè', 3.50, 0.45, 'fredda e cremosa', cassa=True)]
MIGNON_CASSA = 1.20
COLAZIONE = [dict(v, prezzo=MIGNON_CASSA, m=MIGNON_CASSA / b.IVA - 0.20) if v['nome'] == 'Mignon' else v for v in b.COLAZIONE]
SALATI = b.SALATI  # 08/10: la «Ciabattina club o tonno» (in cassa Mezzaluna Club) è già in build_formati
COL_CAFFE = 1.30 + MIGNON_CASSA  # caffè + mignon a prezzo pieno di cassa
# brunch: solo prodotti presenti in Cassa in Cloud (avocado toast e omelette nel PRANZO., tagliere nei TAGLIERI., toast e focaccine nei SALATI.)
# food cost = STIMA RBR (pane, avocado, uova, salumi e fior di latte ai prezzi del listino bar); i piatti proposti il 05/10
# (uovo alla Benedict, uova strapazzate, pancakes, pane burro e marmellata) NON sono in cassa: fuori finché non li creano
PIATTI_BRUNCH = [b.V('Avocado toast', 13.00, 1.60, 'pane tostato, avocado e uovo all’occhio di bue', cassa=True),
                 b.V('Omelette', b.pf('Omelette Cotto e Fontina + Buffet', 12.50), 3.15, 'prosciutto cotto e fontina, oppure spinaci e formaggio, con le verdure del buffet'),
                 b.V('Tagliere della terra', b.pf('Tagliere Terra', 9.00), 2.60, 'salumi e formaggi')]
FORNO_BRUNCH = [b.V('Toast', b.pf('Toast', 4.00), 0.80),
                b.V('Focaccina crudo e fior di latte', 3.70, 1.30, cassa=True),
                b.V('Focaccina cotto e fior di latte', 3.70, 1.10, cassa=True)]

# 08/10 Marco: brunch Panciatichi = i piatti proposti da noi tranne l'uovo alla Benedict.
# Avocado toast, omelette e tagliere al prezzo di CASSA (mai sotto); uova strapazzate, pancakes e pane burro e marmellata
# NON sono in cassa: prezzo proposta RBR, da creare in cassa prima della stampa.
_PB = {v['nome']: v for v in PIATTI_BRUNCH}
BRUNCH_UOVA = [g.UOVA[0], _PB['Omelette'], _PB['Avocado toast']]
BRUNCH_FORNO = [g.FORNO[0], g.FORNO[1], _PB['Tagliere della terra'], g.FORNO[3]]

CAFFE = meta('caffe', 'i sommelier del caffè', 'Il caffè', 'caffe',
             lista('Al banco', TAZZINE) + f'<p class="nota-p">Cappuccino e latte macchiato anche con bevanda vegetale di soia o avena, + {eur(b.VEG_EXTRA)}</p>',
             misure('In tazza', b.ordina(b.TZ)))
PASTICCERIA = meta('past', 'ogni mattina dal nostro laboratorio', 'La pasticceria', 'pasticceria',
                   lista('La colazione', COLAZIONE), lista('Fette e monoporzioni', b.FETTE),
                   combo('La colazione completa', 'cappuccino, spremuta d’arancia e una pasta farcita', eur(b.COLAZ)))
BRUNCH = meta('brunch', 'colazione salata e brunch', 'Il brunch', 'avocado_toast',
              lista('Le uova', BRUNCH_UOVA), lista('Dal forno e dalla dispensa', BRUNCH_FORNO),  # 08/10 Marco: i piatti nostri (senza Benedict), prezzi di cassa dove esistono
              combo('Il brunch completo', 'un piatto a scelta con spremuta d’arancia e cappuccino', f'+ {eur(b.SPR + b.CAPPU)}'))
BAR = meta('bar', 'a ogni ora del giorno', 'Il bar', 'salati',
           lista('I salati', SALATI), lista('Da bere', b.BERE),
           combo('Col caffè', 'un mignon della nostra pasticceria', eur(COL_CAFFE)))

# ---- 07/10: versione 6 bar, IL BAR su tutta la facciata destra (solo voci già nei dati: salati, toast e focaccine di cassa, bevande)
SALATI_FORNO = meta('bar pieno', 'a ogni ora del giorno', 'Il bar', 'salati',
                    lista('I salati', SALATI), lista('Toast e focaccine', FORNO_BRUNCH)
                    + combo('Col caffè', 'un mignon della nostra pasticceria', eur(COL_CAFFE)))
_bere = b.ordina(b.BERE); _meta_bere = (len(_bere) + 1) // 2
def righe(lst): return ''.join(riga(v) for v in lst)
DA_BERE = (f'<div class="meta bere pieno"><div class="mt"><div class="mt-t"><p class="occ">fresco, al banco o al tavolo</p><h1>Da bere</h1></div></div>'
           f'<div class="due"><div class="c1"><div class="sez"><h2>Le bevande</h2>{righe(_bere[:_meta_bere])}</div></div>'
           f'<div class="c2"><div class="sez"><h2>&nbsp;</h2>{righe(_bere[_meta_bere:])}</div></div></div>'
           + '<div class="combi">' + combo2('Il cappuccino', 'piccolo ' + eur(b.CAPPU) + ' · medio ' + eur(b.CAPPU + 0.50) + ' · grande ' + eur(b.CAPPU + 0.90))
           + combo2('La spremuta d’arancia', 'piccola ' + eur(b.SPR) + ' · grande ' + eur(b.SPR + 1.50)) + '</div></div>')

def copertina(sotto):
    return ('<section class="pag cop"><div class="cop-c">'
            '<p class="cop-occ">i sommelier del caffè</p><h1 class="cop-tit">Cartabianca</h1><p class="cop-cafe">cafè</p>'
            f'{g.foto("caffe", "cop-ft")}'
            f'<p class="cop-sotto">{sotto}</p></div></section>')
INTERNO_SX = f'<section class="pag int sx">{CAFFE}<div class="taglio"></div>{PASTICCERIA}</section>'
INTERNO_DX_PANC = f'<section class="pag int dx">{BRUNCH}<div class="taglio"></div>{BAR}</section>'
INTERNO_DX_6 = f'<section class="pag int dx">{SALATI_FORNO}<div class="taglio"></div>{DA_BERE}</section>'
RETRO = ('<section class="pag retro"><div class="ret-c">'
         f'<img class="ret-logo" src="{b.LOGO}" alt="Cartabianca Cafè">'
         '<p class="ret-occ">i sommelier del caffè</p>'
         '<div class="ret-note"><p>Le torte intere si ordinano anche online, da ritirare in sede.</p>'
         '<p>Ingredienti e allergeni: chiedete al nostro personale.</p><p>I prezzi sono in euro.</p></div>'
         '<p class="ret-sito">cartabiancacafe.it</p></div></section>')

CSS = r"""
@page{size:210mm 297mm;margin:0}
:root{--fondo:#FFFDF9;--titolo:#4A2617;--nome:#8A5A2B;--testo:#4A3A2E;--soft:#8C7A6A;--linea:#E7DCCB;--crema:#F4EDE1;--punti:#A6192E;
  --serif:'Cormorant Garamond','EB Garamond',Garamond,Georgia,serif;--tf:'EB Garamond',Garamond,Georgia,serif}
*{box-sizing:border-box}
html,body{margin:0;background:var(--fondo)}
body{font-family:var(--tf);color:var(--testo)}
p{margin:0}
.pag{position:relative;width:210mm;height:297mm;overflow:hidden;background:var(--fondo);page-break-after:always}
.pag:last-child{page-break-after:auto}
.pag::before{content:"";position:absolute;top:6mm;left:6mm;right:6mm;bottom:6mm;border:.5pt solid var(--linea)}
/* ---- copertina ---- */
.cop-c,.ret-c{position:absolute;top:0;left:0;right:0;bottom:0;text-align:center;padding:0 20mm}
.cop-occ{margin-top:62mm;font-family:var(--serif);font-style:italic;font-weight:500;font-size:19pt;color:var(--titolo)}
.cop-tit{margin:2mm 0 0;font-family:var(--serif);font-weight:500;font-size:52pt;letter-spacing:.12em;text-transform:uppercase;color:var(--titolo);line-height:1}
.cop-cafe{margin-top:2mm;font-family:var(--serif);font-style:italic;font-size:17pt;color:var(--nome)}
.cop-ft{display:block;width:118mm;height:auto;margin:22mm auto 0}
.cop-sotto{position:absolute;left:0;right:0;bottom:30mm;font-family:var(--serif);font-size:11.5pt;letter-spacing:.26em;text-transform:uppercase;color:var(--nome)}
/* ---- retro ---- */
.ret-logo{display:block;height:13mm;width:auto;margin:118mm auto 0}
.ret-occ{margin-top:7mm;font-family:var(--serif);font-style:italic;font-weight:500;font-size:15pt;color:var(--titolo)}
.ret-note{position:absolute;left:0;right:0;bottom:34mm;font-style:italic;font-size:10pt;line-height:1.6;color:var(--soft)}
.ret-sito{position:absolute;left:0;right:0;bottom:22mm;font-family:var(--serif);font-size:10pt;letter-spacing:.22em;text-transform:uppercase;color:var(--nome)}
/* ---- interno: due metà per facciata ---- */
.int{padding:13mm 15mm 12mm}
.meta{height:132mm;position:relative}
.taglio{height:.6pt;background:var(--linea);margin:3mm 18mm 5mm}
.mt{display:flex;align-items:center;justify-content:space-between;gap:6mm;margin-bottom:3mm;height:30mm}
.mt-t{flex:1 1 auto}
.occ{font-family:var(--serif);font-style:italic;font-weight:500;font-size:12.5pt;color:var(--titolo)}
.mt h1{margin:.5mm 0 0;font-family:var(--serif);font-weight:500;font-size:27pt;letter-spacing:.08em;text-transform:uppercase;color:var(--titolo);line-height:1}
.mt h1::after{content:"";display:block;width:16mm;height:.7pt;background:var(--titolo);opacity:.45;margin-top:2.6mm}
.mf{flex:0 0 auto;display:block;height:30mm;width:auto;max-width:56mm;object-fit:contain}
.due{display:flex;gap:9mm}
.due>div{flex:1 1 0;min-width:0}
.caffe .due .c1{flex:.78 1 0} .caffe .due .c2{flex:1.22 1 0}
.sez h2{margin:0 0 1.2mm;padding-bottom:1mm;border-bottom:.5pt solid var(--linea);font-family:var(--serif);font-weight:500;font-style:italic;font-size:14pt;color:var(--titolo)}
.r{display:flex;justify-content:space-between;align-items:baseline;gap:3mm;padding:1.25mm 0}
.nm{font-family:var(--serif);font-weight:600;font-size:9.6pt;letter-spacing:.06em;text-transform:uppercase;color:var(--nome)}
.r .p{flex:0 0 auto;font-size:10.5pt;text-align:right}
.r.ds{display:block}
.r.ds .nm{display:block}
.r .d{font-style:italic;font-size:9.4pt;line-height:1.25;margin-top:.3mm}
.sep{color:var(--linea);font-style:normal}
.pz{font-style:normal;font-size:10.5pt;white-space:nowrap}
.r.uno{border:1pt dotted var(--punti);padding:1.25mm 2.6mm;margin:.4mm -2.6mm}
table.misure{width:100%;border-collapse:collapse}
.misure th{font-family:var(--serif);font-style:italic;font-weight:500;font-size:9pt;color:var(--soft);text-align:right;padding:0 0 .6mm;width:12mm}
.misure th:first-child{width:auto}
.misure td{padding:1.25mm 0;text-align:right;font-size:10.5pt}
.misure td.n{text-align:left;white-space:nowrap}
.misure tr.uno td{border-top:1pt dotted var(--punti);border-bottom:1pt dotted var(--punti)}
.nota-p{margin-top:3.5mm;font-style:italic;font-size:9pt;line-height:1.3;color:var(--soft)}
.combo{background:var(--crema);padding:2.6mm 5mm;text-align:center;margin-top:3.5mm}
.combo .ct{font-family:var(--serif);font-weight:600;font-size:9pt;letter-spacing:.16em;text-transform:uppercase;color:var(--nome)}
.combo .cd{margin-top:.5mm;font-style:italic;font-size:10.5pt}
.nm{font-size:10.2pt} .r .p,.pz,.misure td{font-size:11pt} .r .d{font-size:9.8pt}
.r{padding:1.45mm 0} .misure td{padding:1.6mm 0} .r.uno{padding:1.45mm 2.6mm}
.caffe .r,.caffe .misure td{padding-top:2.2mm;padding-bottom:2.2mm}
/* 06/10 (Marco): prezzo SEMPRE in coda (alla descrizione o al nome), mai in colonna; discreto: più piccolo, mai bold, colore tenue */
.pz,.nm .pz,.r .d .pz,.combo .pz{font-family:var(--tf);font-style:normal;font-weight:400;font-size:8.8pt !important;letter-spacing:0;text-transform:none;color:var(--soft)}
.nm .sep,.r .d .sep,.combo .sep{font-weight:400;margin:0 .3mm}
.caffe .r{padding-top:1.3mm;padding-bottom:1.3mm}
.caffe .r.ds .d{margin-top:0}
.brunch .r{padding:2mm 0} .brunch .r.uno{padding:2mm 2.6mm}
/* 07/10 versione 6 bar: il bar riempie tutta la facciata destra, righe più ariose */
.pieno .r{padding:3.3mm 0} .pieno .r.uno{padding:3.3mm 2.6mm}
.pieno .combo{margin-top:6mm} .combi{display:flex;gap:9mm} .combi .combo{flex:1 1 0}
.pieno .nm{font-size:11pt}
.bere .mt{height:24mm} .bere .r{padding:3.9mm 0} .bere .r.uno{padding:3.9mm 2.6mm} .bere .combo{margin-top:9mm}
"""
FONTS = g.FONTS

def html_doc(panciatichi=False):
    cop = copertina('caffè · pasticceria · brunch · bar' if panciatichi else 'caffè · pasticceria · bar')
    dx = INTERNO_DX_PANC if panciatichi else INTERNO_DX_6
    return (f'<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Menu del bar a libro · Cartabianca</title>{FONTS}<style>{CSS}</style></head><body>'
            + cop + INTERNO_SX + dx + RETRO + '</body></html>')

if __name__ == '__main__':
    from pypdf import PdfReader
    for panc, out, h in ((False, OUT, '_libro_bar.html'), (True, OUT_PANC, '_libro_bar_panciatichi.html')):
        doc = html_doc(panc)
        open(os.path.join(HERE, h), 'w', encoding='utf-8').write(doc)
        HTML(string=doc, base_url=HERE).write_pdf(os.path.join(HERE, out))
        print('OK', out, len(PdfReader(os.path.join(HERE, out)).pages), 'pagine')

