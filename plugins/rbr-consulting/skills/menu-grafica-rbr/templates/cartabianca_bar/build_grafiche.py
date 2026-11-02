# -*- coding: utf-8 -*-
"""Tabelloni dei 7 bar Cartabianca — v5 STILE EATALY (Marco 05/10, riferimenti «La pizza di Eataly», «La caffetteria di Eataly»).
Solo 3 tabelloni orizzontali A3/70x50: il caffè, la pasticceria, il bar (niente dopo pranzo, aperitivo, strisce).
Posizionamento: «i sommelier del caffè». Serif classico (Cormorant Garamond + EB Garamond), titoli maiuscoli marrone,
nomi in maiuscoletto color caramello, descrizioni in corsivo, prezzo allineato a destra senza zeri finali,
foto scontornate su bianco (img/grafiche/<nome>.png, fatte con ChatGPT + rembg), cornice puntinata solo sul n.1.
Dati (prezzi PREZZO FINALE, costi, ordine per margine) da build_formati.py: qui cambia solo la grafica.
Copia della v4 «pulita sans» nello scratchpad della sessione 05/10."""
import base64, html, os
from weasyprint import HTML
import build_formati as b

HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
eur = b.eur
pulisci = lambda n: n.replace(b.VEG, '').strip()

def foto(nome, cls=''):
    """foto scontornata se c'è il file, altrimenti niente (mai riquadri vuoti in stampa)"""
    for ext in ('webp', 'png', 'jpg'):
        f = os.path.join(HERE, 'img', 'grafiche', f'{nome}.{ext}')
        if os.path.exists(f):
            mime = 'jpeg' if ext == 'jpg' else ext
            return f'<img class="ft {cls}" src="data:image/{mime};base64,{base64.b64encode(open(f, "rb").read()).decode()}" alt="">'
    return ''

def riga(nome, prezzo, sub='', n1=False):
    s = f'<span class="d">{E(sub)}</span>' if sub else ''
    return f'<div class="r{" uno" if n1 else ""}"><div class="n"><span class="nm">{E(nome)}</span>{s}</div><div class="p">{prezzo}</div></div>'

def lista(lst):
    return ''.join(riga(pulisci(v['nome']), eur(v['prezzo']), v.get('sub', ''), v['n1']) for v in b.ordina(lst))

def sez(titolo, corpo):
    return f'<div class="sez"><h2>{titolo}</h2>{corpo}</div>'

def misure(righe):
    f = lambda x: eur(x) if x else ''
    tr = ''.join(f'<tr class="{"uno" if v["n1"] else ""}"><td class="n"><span class="nm">{E(pulisci(v["nome"]))}</span></td><td>{f(v["prezzo"])}</td>'
                 f'<td>{f(v["prezzo"] + v["md"]) if v["md"] else ""}</td><td>{f(v["prezzo"] + v["gr"]) if v["gr"] else ""}</td></tr>' for v in righe)
    return f'<table class="misure"><thead><tr><th></th><th>piccolo</th><th>medio</th><th>grande</th></tr></thead><tbody>{tr}</tbody></table>'

def perche(domanda, testo, voci):
    cols = ''.join(f'<div><b>{E(a)}</b><span>{E(c)}</span></div>' for a, c in voci)
    return f'<div class="perche"><p class="pq">{domanda}</p><p class="pt">{testo}</p><div class="pv">{cols}</div></div>'

def combo(titolo, testo, prezzo):
    return f'<div class="combo"><p class="ct">{titolo}</p><p class="cd">{testo} <span class="cp">{prezzo}</span></p></div>'

def testa(occ, titolo):
    return f'<div class="testa"><p class="occ">{occ}</p><h1>{titolo}</h1></div>'

LOGO = f'<img class="logo" src="{b.LOGO}" alt="Cartabianca Cafè">'
VEGNOTA = f'Cappuccino e latte macchiato anche con bevanda vegetale di soia o avena, + {eur(b.VEG_EXTRA)}'

# 1 · IL CAFFÈ — posizionamento: i sommelier del caffè
P1 = (f'<section class="poster a3"><div class="cols"><div class="sx">{foto("caffe", "eroe")}'
      + perche('Perché il nostro caffè è così buono?',
               'Siamo i sommelier del caffè: scegliamo la miscela, la maciniamo al momento e la estraiamo tazza per tazza, come si fa con un grande vino.',
               [('La miscela', 'scelta da noi'), ('Macinato', 'al momento'), ('L’estrazione', 'tazza per tazza'), ('Il latte', 'montato a mano')])
      + f'</div><div class="dx">{testa("i sommelier del caffè", "Il caffè")}'
      f'<div class="due"><div>{sez("Al banco", lista(b.TAZZINE))}</div><div class="largo">{sez("In tazza", misure(b.ordina(b.TZ)))}</div></div>'
      f'<p class="nota-p">{VEGNOTA}</p></div></div>{LOGO}</section>')

# 2 · LA PASTICCERIA
P2 = (f'<section class="poster a3"><div class="cols"><div class="sx">{foto("pasticceria", "eroe")}'
      + perche('Perché la nostra pasticceria è così buona?',
               'Ogni mattina la sforna il nostro laboratorio: impasti lievitati con calma, creme fatte da noi, frutta fresca di stagione.',
               [('Il laboratorio', 'tutte le mattine'), ('Le creme', 'fatte da noi'), ('La frutta', 'fresca di stagione')])
      + combo('La colazione completa', 'cappuccino, spremuta d’arancia e una pasta farcita', eur(b.COLAZ))
      + f'</div><div class="dx">{testa("ogni mattina dal nostro laboratorio", "La pasticceria")}'
      f'<div class="due"><div>{sez("La colazione", lista(b.COLAZIONE))}</div><div>{sez("Fette e monoporzioni", lista(b.FETTE))}</div></div>'
      f'</div></div>{LOGO}</section>')

# 3 · IL BAR (salati e da bere)
P3 = (f'<section class="poster a3"><div class="cols"><div class="sx">{foto("salati", "eroe")}'
      + combo('Col caffè', 'un dolcetto della nostra pasticceria', '2,7')
      + combo('Il cappuccino', 'medio 2,1 · grande', '2,5')
      + f'</div><div class="dx">{testa("a ogni ora del giorno", "Il bar")}'
      f'<div class="due"><div>{sez("I salati", lista(b.SALATI))}</div><div>{sez("Da bere", lista(b.BERE))}</div></div>'
      f'</div></div>{LOGO}</section>')

# 4 · LA COLAZIONE SALATA / BRUNCH (proposta nuova 05/10: prodotti e prezzi da approvare, food cost = STIMA RBR)
UOVA = [b.V('Uova strapazzate', 7.0, 1.20, 'con il pane tostato del nostro laboratorio'),
        b.V('Omelette', 8.0, 1.80, 'prosciutto cotto e formaggio, oppure verdure di stagione'),
        b.V('Avocado toast', 9.5, 2.80, 'pane tostato, avocado, uovo o salmone affumicato')]
FORNO = [b.V('Pancakes salati', 10.0, 2.40, 'con uova strapazzate, bacon e formaggio'),
         b.V('Pancakes', 8.5, 1.60, 'con sciroppo d’acero e frutta fresca'),  # 07/10 Emiliano: pancakes da prodotto pronto, non fatti in casa
         b.V('Tagliere di salumi e formaggi', 12.0, 4.00, 'salumi e formaggi toscani, confettura di frutta'),
         b.V('Pane tostato, burro e marmellata', 4.0, 0.60, 'il pane del nostro laboratorio')]
P4 = (f'<section class="poster a3"><div class="cols"><div class="sx">{foto("brunch", "eroe")}'
      + perche('Perché la nostra colazione salata è così buona?',
               'Il pane lo sforna il nostro laboratorio, le uova le cuciniamo al momento, i salumi e i formaggi li scegliamo in Toscana.',
               [('Il pane', 'del nostro laboratorio'), ('Le uova', 'cucinate al momento'), ('I salumi', 'toscani')])
      + combo('Il brunch completo', 'un piatto a scelta, spremuta d’arancia e cappuccino', f'+ {eur(b.SPR + b.CAPPU)}')
      + f'</div><div class="dx">{testa("colazione salata e brunch", "Il brunch")}'
      f'<div class="due"><div>{sez("Le uova", lista(UOVA))}</div><div>{sez("Dal forno e dalla dispensa", lista(FORNO))}</div></div>'
      f'</div></div>{LOGO}</section>')
from build_formati import nota as _nota
def _mk(l): return ' · '.join(f"{v['rank']}° {E(v['nome'])} {eur(v['m'])}" for v in sorted(b.ordina(l), key=lambda v: v['rank']))
n_brunch = _nota('<b>Tabellone nuovo, proposta RBR</b> sullo spunto di Marco (colazione salata / brunch). Prodotti e prezzi da approvare con Cartabianca; '
                 f'food cost STIMA RBR (nessuna ricetta del cliente). Margini: uova {_mk(UOVA)}; forno {_mk(FORNO)}. '
                 f'Brunch completo = piatto + spremuta + cappuccino al prezzo pieno (+{eur(b.SPR + b.CAPPU)}), nessuno sconto. '
                 'Leva non contata: serve prima la prova in 1-2 bar (consigliati quelli con più colazioni nel weekend).')

# 07/10 Marco + Emiliano: il brunch è un PILOTA SOLO A PANCIATICHI (via l'uovo alla Benedict) → fuori dai tabelloni di tutti i bar,
# tabellone a parte «Brunch Panciatichi» (PEZZI_PANCIATICHI) generato in un PDF suo da build_bar_eataly.py
PEZZI = [('Tabellone orizzontale · A3 o 70×50 · il caffè', P1, b.n1), ('Tabellone orizzontale · A3 o 70×50 · la pasticceria', P2, b.n2),
         ('Tabellone orizzontale · A3 o 70×50 · il bar', P3, b.n3),
]
PEZZI_PANCIATICHI = [('Solo Panciatichi · tabellone orizzontale A3 · il brunch (pilota)', P4, n_brunch)]

CSS = r"""
:root{--fondo:#FFFDF9;--titolo:#4A2617;--nome:#8A5A2B;--testo:#4A3A2E;--soft:#8C7A6A;--linea:#E7DCCB;--punti:#A6192E;
  --serif:'Cormorant Garamond','EB Garamond',Garamond,Georgia,serif;--tf:'EB Garamond',Garamond,Georgia,serif}
*{box-sizing:border-box}
body{margin:0;background:#2A221D;font-family:var(--tf)}
.poster{position:relative;overflow:hidden;background:var(--fondo);color:var(--testo);font-family:var(--tf)}
.a3{width:420mm;height:297mm;padding:22mm 26mm}
.cols{display:flex;gap:20mm;height:100%}
.sx{flex:0 0 112mm;display:flex;flex-direction:column;justify-content:center;gap:10mm}
.dx{flex:1 1 auto;min-width:0}
.ft.eroe{display:block;width:112mm;height:auto;max-height:95mm;object-fit:contain;margin:0 auto}
.testa{text-align:center;margin:0 0 11mm}
.occ{margin:0;font-family:var(--serif);font-style:italic;font-weight:500;font-size:22pt;color:var(--titolo)}
.testa h1{margin:1mm 0 0;font-family:var(--serif);font-weight:500;font-size:44pt;letter-spacing:.06em;text-transform:uppercase;color:var(--titolo);line-height:1.05}
.perche{text-align:center;margin-top:7mm}
.pq{margin:0 0 3mm;font-family:var(--serif);font-style:italic;font-weight:500;font-size:21pt;color:var(--titolo)}
.pt{margin:0 0 5mm;font-style:italic;font-size:12.5pt;line-height:1.45}
.pv{display:flex;justify-content:space-between;gap:4mm;border-top:.6pt solid var(--linea);border-bottom:.6pt solid var(--linea);padding:3mm 0}
.pv div{flex:1;display:flex;flex-direction:column;align-items:center}
.pv b{font-family:var(--serif);font-weight:600;font-size:9.5pt;letter-spacing:.14em;text-transform:uppercase;color:var(--nome)}
.pv span{font-size:10.5pt;font-style:italic}
.due{display:flex;gap:15mm}
.due>div{flex:1 1 0;min-width:0}
.due>div.largo{flex:1.35 1 0}
.sez h2{margin:0 0 3mm;padding-bottom:2mm;border-bottom:.6pt solid var(--linea);font-family:var(--serif);font-weight:500;font-style:italic;font-size:22pt;color:var(--titolo)}
.r{display:flex;justify-content:space-between;align-items:baseline;gap:6mm;padding:2.5mm 0}
.r .n{flex:1 1 auto}
.nm{font-family:var(--serif);font-weight:600;font-size:15.5pt;letter-spacing:.07em;text-transform:uppercase;color:var(--nome)}
.r .d{display:block;font-style:italic;font-size:12pt;margin-top:.4mm}
.r .p{flex:0 0 auto;font-size:16pt;text-align:right;min-width:14mm}
.r.uno{border:1.1pt dotted var(--punti);padding:2.5mm 4mm;margin:1mm -4mm}
table.misure{width:100%;border-collapse:collapse}
.misure th{font-family:var(--serif);font-style:italic;font-weight:500;font-size:12pt;color:var(--soft);text-align:right;padding:0 0 2mm;width:20mm}
.misure th:first-child{width:auto}
.misure td{padding:2.5mm 0;text-align:right;font-size:16pt}
.misure td.n{text-align:left;white-space:nowrap}
.misure tr.uno td{border-top:1.1pt dotted var(--punti);border-bottom:1.1pt dotted var(--punti)}
.nota-p{margin:6mm 0 0;font-style:italic;font-size:11pt;color:var(--soft);text-align:center}
.combo{border:1.1pt dotted var(--punti);padding:4mm 6mm;text-align:center}
.combo .ct{margin:0;font-family:var(--serif);font-weight:600;font-size:12pt;letter-spacing:.14em;text-transform:uppercase;color:var(--nome)}
.combo .cd{margin:1mm 0 0;font-style:italic;font-size:13.5pt}
.combo .cp{font-style:normal;margin-left:3mm;font-size:15pt}
.logo{position:absolute;right:26mm;bottom:11mm;height:8mm;width:auto}
.nm{font-size:20pt} .r .p,.misure td{font-size:20pt} .r{padding:4.8mm 0} .misure td{padding:4.8mm 0} .combo .cp{white-space:nowrap}
.ft.eroe{max-height:92mm;width:120mm} .sx{flex-basis:120mm;display:block;padding-top:16mm} .sx>*{margin-bottom:9mm} .pv{flex-wrap:nowrap} .pv span{line-height:1.2} .r .d{font-size:13.5pt}
.sez h2{font-size:26pt;margin-bottom:4mm} .testa h1{font-size:54pt;white-space:nowrap} .testa{margin-bottom:14mm}
.misure th{font-size:13pt;width:22mm} .nota-p{font-size:12pt}
.r.uno{padding-left:4mm !important;padding-right:4mm !important}
.top{position:sticky;top:0;z-index:9;display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between;padding:11px 20px;background:rgba(30,24,20,.96);color:#F5EFE0;font-family:'DM Sans',Arial,sans-serif}
.top b{letter-spacing:.3em;font-size:14px} .top .s{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:rgba(245,239,224,.62)}
.toggle{display:flex;border:1px solid rgba(255,255,255,.26);border-radius:999px;overflow:hidden}
.toggle button{font-family:inherit;font-weight:600;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;padding:7px 16px;border:0;cursor:pointer;background:transparent;color:rgba(245,239,224,.66)}
.toggle button[aria-pressed="true"]{background:#F5EFE0;color:#3B2417}
.wrap{padding:28px 16px 70px;max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:42px}
.pezzo{display:flex;flex-direction:column;gap:12px;min-width:0}
.et{font-family:'DM Sans',Arial,sans-serif;font-size:11px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:rgba(245,239,224,.55);margin:0}
.fit{width:100%;overflow:hidden} .fit .poster{transform-origin:top left;box-shadow:0 26px 64px -22px rgba(0,0,0,.85)}
.nota{display:none;font-family:'DM Sans',Arial,sans-serif;font-size:14px;line-height:1.55;color:#10241A;background:#CBE7D4;border-radius:10px;padding:12px 16px;margin:0;max-width:80ch}
body.rbr .nota{display:block}
.riep{display:none;font-family:'DM Sans',Arial,sans-serif;background:#F5EFE0;border-radius:10px;padding:18px 22px} body.rbr .riep{display:block}
.riep h3{font-weight:500;font-size:15px;margin:0 0 10px} .riep h3 b{color:#1F6B3F}
.riep table{width:100%;border-collapse:collapse;font-size:13.5px} .riep td{padding:6px 8px;border-top:1px solid #E3D7C7;vertical-align:top}
.riep td.n{text-align:right;font-weight:700;white-space:nowrap} .riep td.d{color:#7A5F4B}
"""
PRINT = "@page{margin:0;size:420mm 297mm} body{background:#fff} .poster{page-break-after:always}"
FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=EB+Garamond:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;600&display=swap">')

def artifact():
    righe = ''.join(f'<tr><td>{E(a)}</td><td class="d">{x}</td><td class="n">+{b.intero(c)} €</td></tr>' for a, x, c in b.LEVE)
    riep = f'<div class="riep"><h3>Tabelloni del bar: <b>+{b.intero(b.TOT)} €/anno</b> di margine nuovo</h3><table>{righe}</table></div>'
    pezzi = ''.join(f'<div class="pezzo"><p class="et">{E(t)}</p><div class="fit">{p}</div>{n}</div>' for t, p, n in PEZZI)
    return f'''<title>Grafiche Bar Cartabianca</title>{FONTS}<style>{CSS}</style>
<div class="top"><div><b>CARTABIANCA</b> <span class="s">· tabelloni del bar · caffè, pasticceria, bar · proposta RBR</span></div>
<div class="toggle" role="group" aria-label="Vista"><button id="bCli" aria-pressed="true">Vista cliente</button><button id="bCon" aria-pressed="false">Vista consulente</button></div></div>
<div class="wrap">{riep}{pezzi}</div>
<script>
(function(){{
 var b=document.body,c1=document.getElementById('bCli'),c2=document.getElementById('bCon');
 function set(x){{b.classList.toggle('rbr',x);c1.setAttribute('aria-pressed',String(!x));c2.setAttribute('aria-pressed',String(x));}}
 c1.addEventListener('click',function(){{set(false)}});c2.addEventListener('click',function(){{set(true)}});
 function fit(){{document.querySelectorAll('.fit').forEach(function(f){{var p=f.firstElementChild;p.style.transform='none';
   var k=Math.min(1,f.clientWidth/p.offsetWidth);p.style.transform='scale('+k+')';f.style.height=(p.offsetHeight*k)+'px';}});}}
 window.addEventListener('resize',fit);if(document.fonts&&document.fonts.ready)document.fonts.ready.then(fit);fit();
}})();
</script>'''

if __name__ == '__main__':
    open(os.path.join(HERE, 'formati_bar.html'), 'w', encoding='utf-8').write(artifact())
    doc = f'<!doctype html><html lang="it"><head><meta charset="utf-8">{FONTS}<style>{CSS}{PRINT}</style></head><body>' + ''.join(p for _, p, _ in PEZZI) + '</body></html>'
    HTML(string=doc, base_url=HERE).write_pdf(os.path.join(HERE, 'Grafiche_Bar_Cartabianca_2026.pdf'))
    print('OK tabelloni v5 stile Eataly')

