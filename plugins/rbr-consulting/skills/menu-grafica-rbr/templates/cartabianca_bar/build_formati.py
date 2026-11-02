# -*- coding: utf-8 -*-
"""Grafiche del bar Cartabianca — stile lavagna Eataly × sito cartabianca.ristoranteonline.ai (Lora + DM Sans, marrone caffè su crema).
6 formati, TUTTI ORIZZONTALI (Marco 03/10): 3 poster A3 (caffè, pasticceria, aperitivo), lavagna 16:9, cartellino A5 dopo pranzo, striscia banco.
(Tolto il 03/10 il cartellino A5 «lo chef propone»: Marco non vuole mettere in mostra i piatti dello chef, margine non controllato.)
Prezzi: colonna PREZZO FINALE del tab «Prezzi BAR» (../prezzi_live.json); se il prodotto non c'è, prezzo medio di cassa (segnalato).
Regole RBR: in ogni lista ordine per margine (n.2 in cima, n.1 al 2° posto con l'asticella rossa, poi a scendere), max 7 voci,
al massimo una foto per grafica e solo sul n.1, niente riquadri: i blocchi speciali su fascia crema.
Costi: pasticceria e salati dal file «02 - Food Cost Bar» / «02 - Food Cost Panini Bar»; caffetteria e bevande = STIMA RBR (il food cost bar non c'è).
Uscita: formati_bar.html (artifact doppia vista, foto in base64) + Grafiche_Bar_Cartabianca_2026.pdf (una pagina per formato, misura vera)."""
import base64, html, json, os
from weasyprint import HTML

HERE = os.path.dirname(os.path.abspath(__file__))
E = html.escape
IVA = 1.1
def intero(x): return f"{round(x):,}".replace(',', '.')
def img64(f):
    p = os.path.join(HERE, 'img', f); ext = 'png' if f.endswith('png') else 'jpeg'
    return f"data:image/{ext};base64," + base64.b64encode(open(p, 'rb').read()).decode()
LOGO = img64('logo_hd_2400.png')  # logo ufficiale da PDF, trasparente
FOTO = {k: img64(v) for k, v in dict(cannoli='mignon_cannoli.jpg', sfoglie='mignon_sfogliatelle.jpg', cocktail='stock_cocktail.jpg',
                                       cheese='torta_cheesecake_frutti_neri.jpg', schiacciata='schiacciata_fiorentina.jpg', buffet='blog_gran-buffet-con-piatti-espressi.jpg').items()}

PL = {r['Prodotto'].strip().lower(): r for r in json.load(open(os.path.join(os.path.dirname(HERE), 'prezzi_live.json'), encoding='utf-8'))['Prezzi BAR']}
def pf(prodotto, ripiego):
    r = PL.get(prodotto.lower()); v = r and r.get('PREZZO FINALE')
    return float(v) if isinstance(v, (int, float)) and v > 0 else ripiego
def eur(x):
    """prezzo senza zeri finali, come la carta del pranzo (Marco 05/10): 2 · 2,7 · 22,5"""
    return (f'{x:.2f}'.rstrip('0').rstrip('.')).replace('.', ',')

# ---- leve (venduto CIC 7 bar mar-ago 2026 ×2)
CAPP, CAFFE, ALTRE_TAZZE, SPREM = 145_162, 508_642, 33_000, 8_834
SPR = pf('Spremuta Arancia', 3.70); CAPPU = 1.60; FARC = 1.50
COLAZ = CAPPU + SPR + FARC
L_MIS = CAPP * (0.08 * (0.50 / IVA - 0.06) + 0.03 * (0.90 / IVA - 0.12)) + ALTRE_TAZZE * 0.08 * (0.45 / IVA - 0.06)
L_SPR = SPREM * 0.15 * (1.50 / IVA - 0.55)
L_DOLC = CAFFE * 0.02 * (1.40 / IVA - 0.76)
L_COLAZ = CAPP * 0.01 * (SPR / IVA - 0.55)
LEVE = [('Le tre misure: medio +0,50 e grande +0,90 sul cappuccino (8 e 3 su 100), medio sulle altre tazze', 'poster del caffè · striscia', L_MIS),
        (f'Spremuta grande {eur(SPR + 1.5)} (15 su 100)', 'poster del caffè', L_SPR),
        ('Col caffè un dolcetto a 2,70 (2 caffè in più su 100 con il mignon)', 'striscia banco · lavagna', L_DOLC),
        ('La colazione completa: una spremuta in più ogni 100 cappuccini', 'poster pasticceria · striscia', L_COLAZ)]
TOT = sum(x[2] for x in LEVE)

def V(nome, prezzo, costo, sub='', iva=IVA, cassa=False):
    """voce di listino: prezzo, costo (food cost o stima) → margine per l'ordine"""
    return dict(nome=nome, prezzo=prezzo, m=prezzo / iva - costo, sub=sub, cassa=cassa)
def ordina(lst):
    r = sorted(lst, key=lambda v: -v['m'])
    for i, v in enumerate(r): v['rank'] = i + 1; v['n1'] = i == 0
    if len(r) > 1: r[0], r[1] = r[1], r[0]
    return r
def voce(nome, prezzo='', sub='', n1=False):
    s = f'<span class="vs">{E(sub)}</span>' if sub else ''
    p = f'<span class="pz"> <span class="bar">|</span> <span class="vp">{prezzo}</span></span>' if prezzo else ''
    return f'<p class="v{" asta" if n1 else ""}"><span class="vn">{E(nome)}</span>{p}{s}</p>'
def voci(lst): return ''.join(voce(v['nome'], eur(v['prezzo']), v['sub'], v['n1']) for v in ordina(lst))
def mk(lst):
    """riga per la vista consulente: ordine e margini"""
    return ' · '.join(f"{v['rank']}° {E(v['nome'])} {eur(v['m'])}{' (cassa)' if v['cassa'] else ''}" for v in sorted(lst, key=lambda v: v['rank']))

def titolo(pre, forte, sotto='', cls=''):
    st = f'<p class="tsub">{sotto}</p>' if sotto else ''
    return f'<div class="tit {cls}"><h1><em>{pre}</em> {forte}</h1>{st}</div>'

def nota(t): return f'<p class="nota">{t}</p>'
def foto(k, cls=''): return f'<div class="ph {cls}" style="background-image:url({FOTO[k]})"></div>'
LOGO_H = f'<img class="logo" src="{LOGO}" alt="Cartabianca Cafè">'
VEG = '<span class="veg" title="anche con bevanda vegetale">◐</span>'
VEG_EXTRA = pf('Latte Macchiato Soia', 2.70) - pf('Latte Macchiato', 2.20)
NOTE_PIEDE = (f'<p class="piede"><span class="veg">◐</span> Anche con bevanda vegetale di soia o avena, +{eur(VEG_EXTRA)}. Ingredienti e allergeni: '
              'chiedete al nostro personale. I prezzi sono in euro.</p>')

CUP = """<svg class="cup" viewBox="0 0 200 150" aria-hidden="true"><ellipse cx="100" cy="128" rx="88" ry="16" fill="none" stroke="currentColor" stroke-width="2.4"/>
<path d="M42 52h104v26c0 30-23 50-52 50s-52-20-52-50z" fill="none" stroke="currentColor" stroke-width="2.4"/>
<path d="M146 62c22 0 22 30 0 30" fill="none" stroke="currentColor" stroke-width="2.4"/><ellipse cx="94" cy="52" rx="52" ry="8" fill="currentColor" opacity=".22"/>
<path d="M78 34c-6-8 6-12 0-22M98 34c-6-8 6-12 0-22M118 34c-6-8 6-12 0-22" fill="none" stroke="currentColor" stroke-width="2" opacity=".5"/></svg>"""

# ---------- 1 · poster «il caffè» (autunno: niente shakerato)
TAZZINE = [V('Caffè', 1.30, 0.15, cassa=True), V('Caffè macchiato', 1.40, 0.18, cassa=True), V('Decaffeinato', 1.60, 0.20, cassa=True),
           V('Crema di caffè', 3.40, 0.45, 'fredda e cremosa', cassa=True)]
TAZZE = [  # nome, piccolo, +medio, +grande, costo piccolo (STIMA RBR)
    ('Spremuta d’arancia', SPR, None, 1.50, 0.55), ('Tè e infusi', pf('The Coccole', 3.50), None, None, 0.35),
    ('Latte macchiato ' + VEG, pf('Latte Macchiato', 2.20), 0.50, 0.90, 0.30), ('Caffè americano', pf('Americano', 2.00), 0.40, None, 0.15),
    ('Ginseng', pf('Ginseng', 2.00), 0.50, None, 0.30), ('Orzo', pf('Orzo', 1.70), 0.50, None, 0.15), ('Cappuccino ' + VEG, CAPPU, 0.50, 0.90, 0.25)]
TZ = ordina([dict(nome=n, prezzo=p, m=p / IVA - c, md=md, gr=gr, sub='', cassa=n.startswith('Cappuccino')) for n, p, md, gr, c in TAZZE])
def taglie(righe):
    f = lambda x: eur(x) if x else ''
    tr = ''.join(f'<tr class="{"asta" if v["n1"] else ""}"><td class="tn">{v["nome"]}</td><td class="tp">{f(v["prezzo"])}</td>'
                 f'<td class="tp">{f(v["prezzo"] + v["md"]) if v["md"] else ""}</td><td class="tp">{f(v["prezzo"] + v["gr"]) if v["gr"] else ""}</td></tr>' for v in righe)
    return f'<table class="taglie"><thead><tr><th></th><th>piccolo</th><th>medio</th><th>grande</th></tr></thead><tbody>{tr}</tbody></table>'
P1 = f"""<section class="poster a3">{titolo('scopri il', 'CAFFÈ CARTABIANCA', 'dalla prima tazzina del mattino')}
<div class="oriz"><div class="g-caffe"><div>{voci(TAZZINE)}</div>{CUP}</div>
{taglie(TZ)}</div>
{NOTE_PIEDE}{LOGO_H}</section>"""
n1 = nota(f'<b>Poster A3 orizzontale / 70×50.</b> Ordine per margine (n.1 al 2° posto con l\'asticella): tazzine {mk(TAZZINE)}; tazze {mk(TZ)}. '
          'Costi caffetteria = STIMA RBR (nel file 02 non c\'è il food cost del bar). Shakerato tolto (autunno), latte bianco tolto (max 7 righe). '
          f'<b>Le tre misure: +{intero(L_MIS)} €/anno</b> · <b>Spremuta grande: +{intero(L_SPR)} €/anno</b> (15 su 100). '
          f'Bevanda vegetale +{eur(VEG_EXTRA)} come in cassa (prima c\'era scritto +0,10: errore). Caffè, macchiato, deca, crema e cappuccino non sono nel foglio: prezzi medi di cassa.')

# ---------- 2 · poster «la pasticceria»
COLAZIONE = [V('Bombolone o ciambella', pf('Bombolone/Ciambella', 1.80), 0.40), V('Cookie', pf('Cookies', 2.50), 0.40),
             V('Pasta vuota', 1.40, 0.20, cassa=True), V('Mignon', 1.40, 0.20, cassa=True),
             V('Pasta farcita', FARC, 0.30, 'crema, marmellata o cioccolato', cassa=True), V('Treccia alle noci', pf('Treccia NOCI', 1.80), 0.68),
             V('Biscotto', pf('Biscotto pz', 0.90), 0.10)]
FETTE = [V('Millefoglie', pf('Millefoglie Monoporzione', 3.20), 0.21), V('Torta di mele', pf('Torta di Mele Monoporzione', 3.70), 0.54),
         V('Crostata mora e albicocca', pf('Crostata Mora Albicocca', 3.50), 0.54), V('Crostatina alla frutta', pf('Crostatina frutta', 3.20), 0.46),
         V('Crostata pistacchio e Nutella', pf('Crostata Pistacchio e Nutella', 3.20), 0.54), V('Cannolo siciliano', pf('Cannolo Siciliano', 3.20), 0.65),
         V('Tiramisù', pf('Tiramisù Monoporzione', 3.20), 0.66)]
P2 = f"""<section class="poster a3">{titolo('la nostra', 'PASTICCERIA', 'la fa ogni giorno il laboratorio Cartabianca')}
<div class="g-pas3"><div><p class="sezt">la colazione</p>{voci(COLAZIONE)}</div>
<div><p class="sezt">le fette e le monoporzioni</p>{voci(FETTE)}</div>
<div><div class="phx"><span>FOTO · {E(ordina(FETTE)[1]['nome'])}</span></div>
<div class="fascia"><p class="sezt">la colazione completa</p><p class="ct">cappuccino, spremuta d’arancia e una pasta farcita <span class="bar">|</span> <b>{eur(COLAZ)}</b></p></div></div></div>
<p class="piede">Le torte intere si ordinano anche online, da ritirare in sede. Ingredienti e allergeni: chiedete al nostro personale.</p>{LOGO_H}</section>"""
n2 = nota(f'<b>Poster A3 orizzontale.</b> Colazione: {mk(COLAZIONE)}. Fette: {mk(FETTE)}. Food cost ingredienti dal file 02 Bar (torta di mele e cookie stimati). '
          f'Tolti frittella ripiena (pochi pezzi) e bignè (margine più basso, resta nella carta del pranzo). Una sola foto, sul n.1 delle fette: da scattare. '
          f'<b>Colazione completa {eur(COLAZ)}: +{intero(L_COLAZ)} €/anno</b> (somma dei tre prezzi, nessuno sconto; prima c\'era 6,60 con i prezzi vecchi).')

# ---------- 3 · lavagna 16:9 (salati: costi del file Panini, più realistici delle card SALATI)
SALATI = [V('Ripiena', pf('Ripiena', 4.00), 0.42), V('Ciabattina club o tonno', pf('Mezzaluna Club', 6.00), 2.00),
          V('Pizza al trancio', pf('Pizza Trancio', 4.00), 0.45), V('Tramezzino club', pf('Tramezzino Clubsandwich', 5.00), 1.37),
          V('Schiacciata mortadella', 5.00, 1.31), V('Cornetto salato', pf('Cornetto Salato', 3.70), 0.90),
          V('Schiacciata crudo o cotto', 5.00, 1.76)]  # 08/10 Marco: mortadella e crudo/cotto a 5; «Ripiena» senza «schiacciata»; mezzaluna → «Ciabattina»
BERE = [V('Bibita in bottiglia', pf('Bibita Bottiglia 50cl', 3.70), 0.70), V('Spremuta d’arancia', SPR, 0.55),
        V('Analcolico', pf('Analcolico Bottiglia Vetro', 3.60), 0.90), V('Red Bull', pf('RedBull', 4.00), 1.30),
        V('Campari soda', pf('Campari Soda', 3.90), 0.90, iva=1.22), V('Succo di frutta', pf('Succo di Frutta', 3.00), 0.50),
        V('Birra', 3.80, 1.00, iva=1.22, cassa=True)]
P3 = f"""<section class="poster h169"><div class="h-top">{titolo('il bar', 'CARTABIANCA', '', 'sx')}{LOGO_H}</div>
<div class="g3">
 <div><p class="sezt">i salati</p>{voci(SALATI)}</div>
 <div><p class="sezt">da bere</p>{voci(BERE)}</div>
 <div class="fascia col"><p class="sezt">col caffè</p><p class="evid">un dolcetto <span class="bar">|</span> <b>2,7</b></p>
 <p class="sezt">il cappuccino</p><p class="evid">medio <b>2,1</b> · grande <b>2,5</b></p>
 <p class="sezt">la colazione completa</p><p class="evid">cappuccino, spremuta e pasta <span class="bar">|</span> <b>{eur(COLAZ)}</b></p></div>
</div></section>"""
n3 = nota(f'<b>Lavagna 16:9</b> (TV dietro il banco o stampa 100×56). Salati: {mk(SALATI)}. Da bere: {mk(BERE)}. '
          'Costi salati dal file «02 - Food Cost Panini Bar» dove c\'è (le card SALATI sono sottostimate); bevande = STIMA RBR. '
          'Tolta la baguette bresaola (food cost 52%), estathé e acqua (max 7: si chiedono comunque). Niente foto: nessuna foto vera del n.1.')

# ---------- 4 · quadrato «dopo pranzo» (gli stessi dolci della carta del pranzo)
DOLCI_DP = [dict(v) for v in FETTE if v['nome'] == 'Millefoglie'] + [dict(v) for v in FETTE if v['nome'] in ('Crostata mora e albicocca', 'Crostatina alla frutta', 'Crostata pistacchio e Nutella')]
AMARI = [V('Amaro', pf('Amaro', 4.50), 0.50, iva=1.22), V('Grappa', 4.50, 0.60, iva=1.22, cassa=True), V('Limoncello', 4.00, 0.40, iva=1.22, cassa=True)]
P4 = f"""<section class="poster a5o"><div class="q-pieno">{titolo('dopo', 'PRANZO', 'prima di tornare al lavoro')}
<div class="g2"><div><p class="sezt">un dolce</p>{voci(DOLCI_DP)}</div><div><p class="sezt">un amaro</p>{voci(AMARI)}
<div class="fascia"><p class="ct">caffè e un mignon <span class="bar">|</span> <b>2,7</b></p></div></div></div>{LOGO_H}</div></section>"""
n4 = nota(f'<b>Cartellino A5 orizzontale</b> (sul tavolo del pranzo). Dolci: {mk(DOLCI_DP)}. Amari: {mk(AMARI)}. '
          'Senza foto (prima c\'erano i cannoli, che non sono il n.1). Stessa leva della carta del pranzo: non la contiamo due volte.')

# ---------- 5 · quadrato «l'aperitivo»
APE = [V('Tagliere di terra', pf('Tagliere Terra', 9.00), 2.36), V('Aperitivo a buffet', pf('Aperitivo Buffet', 9.50), 1.77, 'con un drink'),
       V('Calice di Franciacorta', pf('Franciacorta Brut Le Vedute Bicch.', 8.50), 2.00, iva=1.22),
       V('Spritz Aperol, Campari o Hugo', 8.00, 1.60, iva=1.22, cassa=True), V('Gin tonic o Negroni', 8.00, 1.90, iva=1.22, cassa=True),
       V('Calice di Prosecco', pf('Prosecco Infinitum Cuvee BICC', 6.50), 0.90, iva=1.22)]
BOTT = pf('Prosecco Infinitum Cuvee BOTT', 22.50)
P5 = f"""<section class="poster a3 scuro">{titolo('l’ora', 'DELL’APERITIVO', 'a fine giornata, al banco o al tavolo')}
<div class="g2a"><div>{voci(APE)}</div><div><p class="sezt">per la compagnia</p>{voce('Prosecco, la bottiglia', eur(BOTT))}{voce('Franciacorta, la bottiglia', '36')}</div></div>{LOGO_H}</section>"""
n5 = nota(f'<b>Poster A3 orizzontale</b> (vetrina). {mk(APE)}. Senza foto: il cocktail era una foto di stock e quella del buffet sul sito è una locandina con le scritte. '
          f'Spritz, gin e bottiglia di Franciacorta non sono nel foglio: prezzi di cassa. Quattro calici di Prosecco fanno {eur(4 * 6.5)}: la bottiglia a {eur(BOTT)} si vende da sola ai gruppi.')

# ---------- 6 · striscia banco
P7 = f"""<section class="poster striscia"><div class="g3s">
<div><p class="sezt">col caffè</p><p class="big">un dolcetto <span class="bar">|</span> <b>2,7</b></p></div>
<div><p class="sezt">il cappuccino</p><p class="big">medio <b>2,1</b> · grande <b>2,5</b></p></div>
<div><p class="sezt">la colazione completa</p><p class="big">cappuccino, spremuta e pasta <span class="bar">|</span> <b>{eur(COLAZ)}</b></p></div></div></section>"""
n7 = nota(f'<b>Striscia 297×105</b> sul bancone, davanti alla macchina del caffè. <b>Col caffè un dolcetto: +{intero(L_DOLC)} €/anno</b> '
          '(2 caffè su 100 con un mignon; margine ~0,51 con il costo del laboratorio).')

PEZZI = [('Poster orizzontale · A3 o 70×50 · il caffè', P1, n1), ('Poster orizzontale · A3 o 70×50 · la pasticceria', P2, n2),
         ('Lavagna orizzontale 16:9 · TV o 100×56', P3, n3), ('Cartellino orizzontale A5 · tavolo del pranzo', P4, n4), ('Poster orizzontale · A3 o 70×50 · vetrina', P5, n5),
         ('Striscia orizzontale · banco', P7, n7)]

CSS = r"""
/* stile lavagna Eataly × sito Cartabianca: crema e marrone caffè, Lora corsivo + DM Sans maiuscolo */
:root{--crema:#F5EFE0;--latte:#FFFDF8;--caffe:#4A2617;--inchiostro:#1E1A17;--soft:#7A6A5E;--linea:#E3D9C6;--verde:#3E7C59;--grafite:#2A221D;
 --serif:'Lora',Georgia,serif;--sans:'DM Sans','Helvetica Neue',Arial,sans-serif}
*{box-sizing:border-box}
body{margin:0;background:var(--grafite);color:var(--inchiostro);font-family:var(--sans)}
.top{position:sticky;top:env(safe-area-inset-top,0px);z-index:9;display:flex;flex-wrap:wrap;gap:10px 18px;align-items:center;justify-content:space-between;padding:11px 20px;background:rgba(30,24,20,.96);color:#F5EFE0;border-bottom:1px solid rgba(255,255,255,.12)}
.top b{letter-spacing:.3em;font-size:14px} .top .s{font-size:12px;letter-spacing:.12em;text-transform:uppercase;color:rgba(245,239,224,.62)}
.toggle{display:flex;border:1px solid rgba(255,255,255,.26);border-radius:999px;overflow:hidden}
.toggle button{font-family:var(--sans);font-weight:600;font-size:11.5px;letter-spacing:.1em;text-transform:uppercase;padding:7px 16px;border:0;cursor:pointer;background:transparent;color:rgba(245,239,224,.66)}
.toggle button[aria-pressed="true"]{background:var(--crema);color:var(--caffe)}
.toggle button:focus-visible{outline:2px solid var(--crema);outline-offset:2px}
.wrap{padding-block:28px 70px;padding-inline:16px;max-width:1180px;margin:0 auto;display:flex;flex-direction:column;gap:42px}
.pezzo{display:flex;flex-direction:column;gap:12px;min-width:0}
.et{font-size:11px;font-weight:600;letter-spacing:.24em;text-transform:uppercase;color:rgba(245,239,224,.55);margin:0}
.fit{width:100%;overflow:hidden}
.poster{position:relative;overflow:hidden;box-shadow:0 26px 64px -22px rgba(0,0,0,.85);transform-origin:top left;background:var(--latte);color:var(--inchiostro)}
.nota{display:none;font-size:14px;line-height:1.55;color:#10241A;background:#CBE7D4;border-radius:10px;padding:12px 16px;margin:0;max-width:80ch}
body.rbr .nota{display:block}
.riep{display:none;background:var(--crema);border-radius:10px;padding:18px 22px} body.rbr .riep{display:block}
.riep h3{font-weight:500;font-size:15px;margin:0 0 10px} .riep h3 b{color:#1F6B3F}
.riep table{width:100%;border-collapse:collapse;font-size:13.5px} .riep td{padding:6px 8px;border-top:1px solid var(--linea);vertical-align:top}
.riep td.n{text-align:right;font-weight:700;white-space:nowrap;font-variant-numeric:tabular-nums} .riep td.d{color:var(--soft)}
.riep p{font-size:12px;color:var(--soft);margin:10px 0 0;line-height:1.5}

/* misure vere in mm */
.a3{width:297mm;height:420mm;padding:26mm 26mm 22mm}
.h169{width:400mm;height:225mm;padding:16mm 22mm}
.q30{width:300mm;height:300mm;padding:0}
.a5{width:148mm;height:210mm;padding:14mm 14mm}
.striscia{width:297mm;height:105mm;padding:12mm 16mm;background:var(--crema)}
.tit{text-align:center;margin:0 0 12mm}
.tit h1{margin:0;font-family:var(--sans);font-weight:700;color:var(--caffe);font-size:34pt;letter-spacing:.01em;line-height:1.1}
.tit h1 em{font-family:var(--serif);font-style:italic;font-weight:400;color:var(--inchiostro);font-size:.78em;letter-spacing:0}
.tsub{margin:3mm 0 0;font-weight:700;font-size:10.5pt;letter-spacing:.06em;text-transform:uppercase}
.tit.sx{text-align:left;margin:0}
.v{margin:0 0 5mm;font-size:15pt;letter-spacing:.02em;text-transform:uppercase;line-height:1.25}
.vn{font-weight:500} .bar{color:var(--soft);font-weight:400} .vp{font-weight:500;font-variant-numeric:tabular-nums}
.vs{display:block;text-transform:none;letter-spacing:0;font-family:var(--serif);font-style:italic;font-size:11pt;color:var(--soft)}
.veg{color:var(--verde);font-size:.9em}
.sezt{font-family:var(--serif);font-style:italic;font-size:17pt;color:var(--caffe);margin:0 0 4mm}
.g2{display:grid;grid-template-columns:1fr 1fr;gap:0 12mm}
.g3{display:grid;grid-template-columns:1fr 1fr 1.05fr;gap:0 14mm;margin-top:10mm}
.ph{background-size:cover;background-position:center;border-radius:2mm}
.logo{display:block;height:9mm;width:auto;margin:0 auto}
.a3 .logo,.a5 .logo{position:absolute;left:0;right:0;bottom:12mm}
.piede{position:absolute;left:26mm;right:26mm;bottom:26mm;margin:0;font-size:10pt;line-height:1.5;color:var(--soft)}
/* 1 caffè */
.g-caffe{display:grid;grid-template-columns:1fr 92mm;gap:8mm;align-items:center;margin-bottom:12mm}
.cup{width:92mm;color:var(--caffe)}
table.taglie{width:100%;border-collapse:collapse}
.taglie th{font-size:9pt;font-weight:500;letter-spacing:.14em;text-transform:uppercase;text-decoration:underline;text-underline-offset:2mm;color:var(--soft);padding:0 0 4mm;text-align:center;width:24mm}
.taglie td{padding:2.6mm 0}
.tn{font-size:15pt;font-weight:500;text-transform:uppercase;letter-spacing:.02em}
.tp{text-align:center;font-size:15pt;font-variant-numeric:tabular-nums}
/* 2 pasticceria */
.g-pas{display:grid;grid-template-columns:1fr 100mm;gap:10mm;margin-bottom:8mm}
.g-pas .ph.alto{height:70mm;margin-bottom:5mm} .g-pas .ph.basso{height:70mm}
.sez{border-top:.8pt solid var(--linea);padding-top:7mm;margin-bottom:6mm}
.sez .v{font-size:13.5pt;margin-bottom:4mm}
.combo{background:var(--crema);border-radius:2mm;padding:6mm 8mm}
.combo .ct{margin:0;font-size:14pt;text-transform:uppercase;letter-spacing:.02em}
/* 3 lavagna */
.h-top{display:flex;justify-content:space-between;align-items:center;border-bottom:.8pt solid var(--linea);padding-bottom:6mm}
.h-top .logo{margin:0;height:11mm} .h169 .tit h1{font-size:30pt}
.h169 .v{font-size:14pt;margin-bottom:4.2mm}
.ph-col .ph{height:92mm;margin-bottom:6mm}
.evid{font-size:17pt;text-transform:uppercase;font-weight:700;color:var(--caffe);margin:0 0 2mm}
.evid2{font-family:var(--serif);font-style:italic;font-size:13pt;margin:0;color:var(--soft)}
/* 4 5 quadrati */
.q30 .q-sx{position:absolute;left:0;top:0;bottom:0;width:170mm;padding:24mm 16mm 20mm 24mm}
.q30 .q-dx{position:absolute;right:0;top:0;bottom:0;width:130mm;border-radius:0}
.q30 .tit{text-align:left;margin-bottom:10mm} .q30 .tit h1{font-size:28pt}
.q30 .v{font-size:12.5pt;margin-bottom:3.6mm}
.q30 .sep{height:.8pt;background:var(--linea);margin:5mm 0 6mm}
.q30 .logo{position:absolute;left:24mm;bottom:16mm;margin:0}
.q30.scuro{background:var(--caffe);color:var(--crema)}
.q30.scuro .tit h1,.q30.scuro .sezt{color:var(--crema)} .q30.scuro .tit h1 em{color:#E9DCC4} .q30.scuro .bar,.q30.scuro .vs{color:rgba(245,239,224,.6)}
.q30.scuro .sep{background:rgba(245,239,224,.25)} .q30.scuro .logo{background:var(--latte);padding:2mm 3mm;border-radius:1mm;height:11mm}
/* 6 chef */
.a5 .tit{margin-bottom:8mm} .a5 .tit h1{font-size:20pt}
.a5 .lab{font-size:9.5pt;font-weight:700;letter-spacing:.14em;text-transform:uppercase;margin:6mm 0 0}
.a5 .riga{border-bottom:.8pt solid var(--linea);height:13mm}
/* 7 striscia */
.g3s{display:grid;grid-template-columns:1fr 1.15fr 1.45fr;gap:10mm;height:100%;align-items:center;text-align:center}
.striscia .sezt{font-size:14pt;margin-bottom:2mm}
.striscia .big{font-size:15pt;text-transform:uppercase;letter-spacing:.02em;margin:0} .striscia .big b{color:var(--caffe)}

/* scala per i formati grandi */
.a3 .tit h1{font-size:50pt} .a3 .tsub{font-size:13pt} .a3 .tit{margin-bottom:16mm}
.a3 .v{font-size:21pt;margin-bottom:6.5mm} .a3 .vs{font-size:14pt}
.a3 .tn,.a3 .tp{font-size:21pt} .a3 .taglie td{padding:4mm 0} .a3 .taglie th{font-size:12pt;width:34mm}
.a3 .cup{width:110mm} .a3 .g-caffe{grid-template-columns:1fr 110mm;margin-bottom:16mm}
.a3 .sezt{font-size:24pt} .a3 .sez .v{font-size:17pt;margin-bottom:5mm}
.a3 .combo .ct{font-size:18pt} .a3 .piede{font-size:12pt;bottom:28mm} .a3 .logo{height:13mm}
.a3 .g-pas{grid-template-columns:1fr 110mm} .a3 .g-pas .ph.alto,.a3 .g-pas .ph.basso{height:84mm}
.h169 .tit h1{font-size:42pt} .h169 .v{font-size:18pt;margin-bottom:5.4mm} .h169 .sezt{font-size:24pt} .h169 .h-top .logo{height:15mm}
.h169 .ph-col .ph{height:100mm} .h169 .evid{font-size:21pt} .h169 .evid2{font-size:15pt}
.q30 .tit h1{font-size:38pt} .q30 .tsub{font-size:12pt} .q30 .v{font-size:17pt;margin-bottom:5mm} .q30 .vs{font-size:13pt} .q30 .sezt{font-size:21pt} .q30 .logo{height:12mm}
.a5 .tit h1{font-size:24pt} .a5 .lab{font-size:11pt} .a5 .riga{height:15mm}
.striscia .big{font-size:20pt} .striscia .sezt{font-size:17pt}

/* regole RBR 03/10: un solo segno (asticella rossa sul n.1), una foto al massimo, blocchi speciali su fascia crema */
:root{--rosso:#A6192E}
.v.asta{border-left:2.4pt solid var(--rosso);padding-left:4mm;margin-left:-6.4mm}
.taglie tr.asta td.tn{border-left:2.4pt solid var(--rosso);padding-left:4mm}
.taglie{margin-left:-6.4mm;width:calc(100% + 6.4mm)} .taglie td.tn{border-left:2.4pt solid transparent;padding-left:4mm}
.pz{white-space:nowrap}
.fascia{background:var(--crema);padding:6mm 8mm;margin-top:6mm}
.fascia .ct{margin:0;font-size:14pt;text-transform:uppercase;letter-spacing:.02em}
.a3 .fascia .ct{font-size:18pt}
.fascia.col{margin-top:0;padding:8mm 9mm;display:flex;flex-direction:column;gap:2mm}
.fascia.col .sezt{margin:3mm 0 0} .fascia.col .sezt:first-child{margin-top:0}
.fascia.col .evid{font-size:17pt;font-weight:500;color:var(--inchiostro);text-transform:uppercase;margin:0}
.fascia.col .evid b{color:var(--caffe)}
.phx{margin-top:5mm;height:58mm;border:.8pt dashed #D9CDBD;border-radius:2mm;display:flex;align-items:flex-end;justify-content:center;padding-bottom:3mm}
.phx span{font-size:8pt;letter-spacing:.2em;text-transform:uppercase;color:var(--soft)}
.a3 .g-pas{grid-template-columns:1fr 1fr;gap:16mm}
.a3 .g-pas .sezt{margin-bottom:6mm}
.q30.tipo .q-pieno{position:absolute;top:0;left:0;right:0;bottom:0;padding:26mm 26mm 24mm}
.q30.tipo .g2{gap:0 16mm;margin-top:4mm}
.q30.tipo .fascia{margin-top:8mm}
.q30.tipo .fascia .ct{font-size:15pt}
.q30.tipo .logo{left:26mm}
.q30.scuro .v.asta{border-left-color:#E9DCC4}
/* ===== tutto ORIZZONTALE ===== */
.a3{width:420mm !important;height:297mm !important;padding:20mm 28mm 20mm !important}
.a3 .tit{margin-bottom:12mm}
.oriz{display:grid;grid-template-columns:1fr 1.25fr;gap:22mm;align-items:start}
.oriz .g-caffe{display:block;margin:0} .oriz .cup{display:block;width:90mm;margin:10mm 0 0 10mm}
.a3 .oriz .taglie td{padding:3.6mm 0}
.g-pas3{display:grid;grid-template-columns:1fr 1.15fr 1fr;gap:16mm;align-items:start}
.g-pas3 .phx{height:110mm;margin:0 0 8mm}
.g-pas3 .fascia{margin:0}
.a3.scuro{background:var(--caffe);color:var(--crema)}
.a3.scuro .tit h1,.a3.scuro .sezt{color:var(--crema)} .a3.scuro .tit h1 em{color:#E9DCC4} .a3.scuro .bar,.a3.scuro .vs{color:rgba(245,239,224,.6)}
.a3.scuro .v.asta{border-left-color:#E9DCC4} .a3.scuro .logo{background:var(--latte);padding:2mm 3mm;border-radius:1mm}
.g2a{display:grid;grid-template-columns:1.3fr 1fr;gap:24mm;margin-top:6mm}
.a3 .g2a .v{font-size:23pt;margin-bottom:8mm}
.a5o{width:210mm;height:148mm;padding:0}
.a5o .q-pieno{position:absolute;top:0;left:0;right:0;bottom:0;padding:13mm 16mm 12mm}
.a5o .tit{text-align:left;margin:0 0 6mm} .a5o .tit h1{font-size:28pt} .a5o .tsub{font-size:9pt}
.a5o .g2{grid-template-columns:1.25fr 1fr;gap:0 12mm}
.a5o .v{font-size:12.5pt;margin-bottom:3.6mm} .a5o .sezt{font-size:16pt;margin-bottom:3.6mm}
.a5o .v.asta{margin-left:-5mm;padding-left:3.4mm}
.a5o .fascia{margin-top:3mm;padding:3mm 5mm} .a5o .fascia .ct{font-size:11pt}
.a5o .logo{position:absolute;right:16mm;top:14mm;height:9mm;margin:0}
.a3 .tit h1{font-size:60pt} .a3 .tsub{font-size:15pt} .a3 .tit{margin-bottom:16mm}
.a3 .v{font-size:25pt;margin-bottom:8.5mm} .a3 .vs{font-size:15pt} .a3 .sezt{font-size:30pt;margin-bottom:8mm}
.a3 .tn,.a3 .tp{font-size:25pt} .a3 .oriz .taglie td{padding:5mm 0} .a3 .taglie th{font-size:13pt;width:40mm}
.a3 .oriz .cup{width:120mm;margin-top:14mm}
.a3 .fascia .ct{font-size:20pt} .a3 .piede{font-size:13pt;bottom:24mm}
.a3 .g2a .v{font-size:29pt;margin-bottom:11mm} .a3 .g2a{margin-top:12mm}
.a5o .v{font-size:16pt;margin-bottom:4.4mm} .a5o .sezt{font-size:20pt} .a5o .tit h1{font-size:32pt}
.a5o .fascia{margin-top:5mm} .a5o .fascia .ct{font-size:15pt}
.q30.tipo .tit h1{font-size:58pt} .q30.tipo .tsub{font-size:15pt} .q30.tipo .tit{margin-bottom:14mm}
.q30.tipo .v{font-size:25pt;margin-bottom:7mm} .q30.tipo .vs{font-size:16pt} .q30.tipo .sezt{font-size:32pt;margin-bottom:7mm}
.q30.tipo .fascia .ct{font-size:21pt}
.q30.tipo .q-pieno .logo{position:absolute;left:26mm;right:auto;bottom:18mm;top:auto;margin:0;height:14mm}
.q30.tipo .g2{grid-template-columns:1.25fr 1fr}
.q30.scuro.tipo .sep{margin:8mm 0}
.h169 .v{font-size:20pt;margin-bottom:6.6mm} .h169 .sezt{font-size:26pt;margin-bottom:6mm} .h169 .g3{margin-top:12mm}
.fascia.col .evid{font-size:19pt}
.striscia .big{font-size:20pt} .g3s{grid-template-columns:1fr 1.3fr 1.5fr}
.a3 .taglie td{padding:5.4mm 0} .a3 .g-caffe{margin-bottom:22mm}
/* ===== STILE EATALY × CARTABIANCA BAR (05/10): pulito, marrone caffè, crema; stesse regole della carta del pranzo ===== */
:root{--crema:#F4EDE1;--latte:#FBF8F2;--caffe:#4A2617;--caffe2:#6B4A36;--soft:#8C7764;--linea:#D9CBB8;--rosso:#A6192E}
.poster{background:var(--latte) !important;color:var(--caffe) !important}
.poster::before{content:"";position:absolute;inset:7mm;top:7mm;left:7mm;right:7mm;bottom:7mm;border:.6pt solid var(--linea);pointer-events:none}
.tit h1{font-family:var(--sans) !important;font-weight:600 !important;letter-spacing:.14em !important;text-transform:uppercase;color:var(--caffe) !important}
.tit h1 em{font-family:var(--serif) !important;font-style:italic !important;font-weight:400 !important;letter-spacing:0 !important;text-transform:none;color:var(--caffe2) !important}
.tsub{font-family:var(--serif) !important;font-style:italic;font-weight:400 !important;letter-spacing:0 !important;text-transform:none !important;color:var(--soft) !important}
.tit::after{content:"";display:block;width:22mm;height:.8pt;background:var(--caffe);margin:5mm auto 0;opacity:.5}
.tit.sx::after,.q30 .tit::after,.a5o .tit::after{margin-left:0}
.sezt{font-family:var(--sans) !important;font-style:normal !important;font-weight:600;letter-spacing:.22em;text-transform:uppercase;font-size:11pt !important;color:var(--caffe2) !important;
  border-bottom:.6pt solid var(--linea);padding-bottom:2.4mm}
.a3 .sezt{font-size:14pt !important}
.v{color:var(--caffe) !important}
.vn{font-weight:500 !important}
.bar{color:var(--linea) !important}
.vp{font-family:var(--serif);font-style:italic;font-weight:400 !important;color:var(--soft)}
.vs{color:var(--soft) !important}
.v.asta{border-left-color:var(--rosso) !important}
.taglie th{color:var(--soft) !important;text-decoration:none !important;border-bottom:.6pt solid var(--linea);font-family:var(--sans)}
.taglie td{border-bottom:.4pt solid #EEE5D8}
.tp{font-family:var(--serif);font-style:italic;color:var(--soft)}
.tn{color:var(--caffe)}
.cup{color:var(--caffe2) !important;opacity:.85}
.fascia,.combo,.striscia{background:var(--crema) !important}
.fascia .ct,.combo .ct,.striscia .big,.evid{color:var(--caffe) !important}
.fascia b,.evid b,.striscia .big b{font-family:var(--serif);font-style:italic;font-weight:400;color:var(--caffe2)}
.piede{color:var(--soft) !important}
.phx{border-color:var(--linea) !important;background:var(--crema)}
/* aperitivo: la versione scura diventa marrone caffè pieno, testo crema */
.a3.scuro{background:var(--caffe) !important;color:var(--crema) !important}
.a3.scuro::before{border-color:rgba(244,237,225,.35)}
.a3.scuro .tit h1,.a3.scuro .v,.a3.scuro .sezt{color:var(--crema) !important}
.a3.scuro .tit h1 em,.a3.scuro .vp,.a3.scuro .vs,.a3.scuro .tsub{color:#D9C7AE !important}
.a3.scuro .sezt{border-bottom-color:rgba(244,237,225,.3)}
.a3.scuro .tit::after{background:var(--crema)}
.a3.scuro .bar{color:rgba(244,237,225,.35) !important}
.a3.scuro .v.asta{border-left-color:#E9DCC4 !important}
.h-top{border-bottom-color:var(--linea) !important}

"""

PRINT = """@page{margin:0} @page pa3{size:420mm 297mm;margin:0} @page pa5o{size:210mm 148mm;margin:0} @page ph169{size:400mm 225mm;margin:0} @page pq30{size:300mm 300mm;margin:0}
@page pstr{size:297mm 105mm;margin:0}
body{background:#fff} .a3{page:pa3} .h169{page:ph169} .q30{page:pq30} .striscia{page:pstr} .a5o{page:pa5o}
.poster{box-shadow:none;page-break-after:always}
.h-top{display:block;overflow:hidden} .h-top .tit{float:left} .h-top .logo{float:right;margin-top:3mm}"""

FONTS = ('<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
         '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;500;600;700&display=swap">')

def artifact():
    righe = ''.join(f'<tr><td>{E(a)}</td><td class="d">{b}</td><td class="n">+{intero(c)} €</td></tr>' for a, b, c in LEVE)
    riep = (f'<div class="riep"><h3>Grafiche del bar: <b>+{intero(TOT)} €/anno</b> di margine nuovo</h3><table>{righe}</table>'
            '<p>Venduto Cassa in Cloud 7 bar, marzo–agosto 2026 ×2 (145.000 cappuccini, 508.000 caffè, 8.800 spremute l’anno) · prezzi = colonna PREZZO FINALE del tab «Prezzi BAR» '
            '(foglio «Prezzi definitivi»); gli aumenti di prezzo del bar sono contati a parte · dopo pranzo già contato nella carta del pranzo · foto dal sito Cartabianca.</p></div>')
    pezzi = ''.join(f'<div class="pezzo"><p class="et">{E(t)}</p><div class="fit">{p}</div>{n}</div>' for t, p, n in PEZZI)
    return f'''<title>Grafiche Bar Cartabianca</title>{FONTS}<style>{CSS}</style>
<div class="top"><div><b>CARTABIANCA</b> <span class="s">· grafiche del bar · 6 formati · proposta RBR</span></div>
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
    print('TOT', round(TOT)); [print(f'  {round(c):>6}  {a}') for a, b, c in LEVE]

