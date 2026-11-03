# -*- coding: utf-8 -*-
"""Carta Antipapa 2026 — libro A4 a 8 facciate (2 fogli A3 piegati), abbondanza 3 mm.

Revisione 07/10/2026 (stampa):
- brand REALE dai post Instagram @antipapafondi 2026: bordeaux #690F33, corallo #E63D2A, verde #08311F, lilla #8C83D0;
  logo = wordmark vero «ANTIPAPA · BEATO RISTORO» ricavato dal post «ANTI FAME» (brand/logo_antipapa_wordmark_*.png);
  titoli in bastone tondo monolinea (Tilt Neon) come il lettering dei post, testo Archivo.
- foto SOLO vere (post Instagram). Nessuna foto vera coerente con un piatto in carta → piatti senza foto;
  le foto vere della tavola e della sala vanno su Experience e retro.
- contenuti = proposta piatti 07/10 (serve il sì di Luca). Niente paste d'autore / grandi secondi: non sono in cassa.
- allergeni: i numeri accanto ai piatti erano STIMATI → tolti finché la cucina non li valida; resta la legenda.
Uso: python3 antipapa.py -> antipapa.html (artifact doppia vista) + Menu_Antipapa_2026.pdf
"""
import os
from comune import pf, e, ordina, foto, BASE

BLEED = 3
COPERTO = 2.5
BIANCO, ROSSO = '#E4D08A', '#7E1B33'


def calice(col, w=2.3):
    return (f'<svg class="ic" width="{w}mm" height="{w*1.5:.2f}mm" viewBox="0 0 16 24"><path d="M3 2h10c0 5-1.6 7.6-4 8.4V20h3v1.6H4V20h3v-9.6C4.6 9.6 3 7 3 2z" '
            f'fill="none" stroke="currentColor" stroke-width="1.2" stroke-linejoin="round"/><path d="M3.4 3.4h9.2c-.15 3.3-1.3 5.3-4.6 5.9C4.7 8.7 3.55 6.7 3.4 3.4z" fill="{col}"/></svg>')


# ------------------------------------------------------------ DATI
# m = margine € a porzione (file 02, IVA scorporata) · pz = gen-ago 2026 iPratico · descrizioni = nome battuto in cassa / schede chef
ANTIPASTI = [
    dict(n='Tagliere di culatello', d='Culatello della macelleria Mattei, la nostra giardiniera, focaccia calda', due=True, p=26, m=15.44, pz=381,
         vino=('Maria Ernesta Berucci', '«Raphael» Cesanese del Piglio', ROSSO), mk='per 2: 7,72 a persona · FC 36%: rivedere la grammatura'),
    dict(n='Antipasto conviviale', d='Gli antipasti della casa, da dividere: sei portate', p='21', d2='quattro portate', p2=15, m=11.57, pz=1274,
         vino=("D'Ausilio", "Costa d'Ulisse Syrah", ROSSO),
         mk='RIENTRA: 720 + 554 pz ≈ 23.000 €, il primo incasso degli antipasti · margine da FC di Luca (6 portate 7,2 €) · cosa c\'è dentro: da confermare'),
    dict(n='Carpaccio di picanha', d='Picanha marinata, chimichurri ai friggitelli', p=14, m=8.71, pz=113, mk='FC 31,5%'),
    dict(n='La parmigiana', d='Melanzane fritte, pomodoro, mozzarella, parmigiano', p=11, m=7.42, pz=564, mk='il n.1 degli antipasti per pezzi'),
    dict(n='Crocchetta di baccalà', d='Baccalà e patate, scarola e olive', p=11, m=7.17, pz=98),
    dict(n='Polpette di salsiccia', d='Ripiene di provola, al pomodoro', p=10, m=None, pz=275, mk='RIENTRA: 275 pz a 9,9 · piatto autunnale a lotti'),
    dict(n='Frittelle di cavolfiore', d='Fritte al momento', p=4, m=None, pz=98, mk='RIENTRA: versione autunnale delle frittelle (zucchine 302 pz a 4)'),
]
MARITOZZI = [
    dict(n='Maritozzo porchettato', d='Pancia di maiale porchettata, cipolla caramellata, sedano riccio di Sperlonga', p=12, m=8.6, pz=197,
         mk='margine STIMATO · 197 pz'),
    dict(n='Maritozzo alla fondana', d='Broccoletti, salsiccia, pecorino', p=11, m=8.2, pz=136, mk='margine STIMATO'),
    dict(n='Maritozzo con tartare di manzo', d='Battuta al coltello, salsa tartara', p=10, m=7.03, pz=79),
]
PASTE = [
    dict(n="Gnocchi ripieni di cacio e pepe all'amatriciana", d='Pomodoro, guanciale croccante, pecorino', p=16, m=11.01, pz=537,
         vino=('Maria Ernesta Berucci', "«L'Onda» Cesanese del Piglio", ROSSO), mk='STAR'),
    dict(n='Ziti alla genovese', d='Cappello del prete e cipolla cotti per ore, fonduta di pecorino', p=14, m=10.67, pz=425,
         vino=('Gulfi', "Rossojbleo Nero d'Avola", ROSSO)),
    dict(n='Raviolo di stracotto', d='Ripieno di stracotto di manzo, spuma di patate', p=15, m=None, pz=144,
         mk='RIENTRA: 144 pz a 14,7 · usa la carne e il fondo del brasato'),
    dict(n='Gnocchi con zucca e porcini', d='Crema di zucca, funghi porcini, nocciole', p=14, m=None, pz=29,
         mk='LA PASTA DI STAGIONE: già battuta in cassa (29 pz) · la cucina può cambiarla'),
    dict(n='Mezze maniche alla carbonara', d='Guanciale, tuorlo, pecorino, pepe', p=15, m=10.59, pz=905, mk='il primo più ordinato'),
]
SECONDI = [
    dict(n='Costoletta di vitello alla milanese', d="Alta, con l'osso, panatura dorata, insalata di sedano, salsa olandese", due=True, p=32,
         m=20.22, pz=329, vino=('La Luna del Casale', 'Alessandro', ROSSO), mk='10,11 a persona'),
    dict(n='Polpo scottato', d='Crema di piselli, datterini arrosto', p=20, m=15.01, pz=105,
         vino=('Siddùra', 'Spèra Vermentino di Gallura', BIANCO), mk='FC 18% · la foto Instagram del polpo è con un\'altra crema: non usata'),
    dict(n='Brasato di manzo', d='Cappello del prete, purè di patate, cavolo nero, fondo bruno', p=19, m=13.35, pz=1176,
         mk='il piatto più venduto del locale: +1 € = +1.603 €/anno'),
    dict(n='Rollè di maialino', d='Pancetta, funghi e cicoria', p=17, m=None, pz=213, mk='RIENTRA: 213 pz a 16,95 · brasato a lotti'),
    dict(n='Pollo alla cacciatora', d='Olive nere di Gaeta, lardo di montagna', p=14, m=None, pz=140, mk='RIENTRA: 140 pz a 13,8 · a lotti'),
    dict(n='Baccalà fritto', d='Salsa di yogurt greco e lime', p=19, m=12.43, pz=271),
]
DOLCI = [  # margini non noti: ordine per pezzi (m = solo per ordinare, non è un margine)
    dict(n='Profiterole al tiramisù', d='Bignè, crema al mascarpone, caffè, cacao', p=7, m=5, pz=227),
    dict(n='Maritozzo al tiramisù', d='Crema al mascarpone, caffè, cacao', p=7, m=4, pz=152),
    dict(n='Semifreddo alla nocciola', d='Salsa al cacao, crumble al cioccolato', p=7, m=3, pz=136, mk='RIENTRA'),
    dict(n='Anticucciolone', d='', p=7, m=2, pz=86, mk='RIENTRA · descrizione da chiedere alla cucina'),
    dict(n='Torta di zucca', d='Con gelato alla vaniglia', p=7, m=1, pz=76, mk='RIENTRA · dolce d\'autunno'),
]
AMARI = [('Erbes Izzi Gran Riserva', 5), ('Erbes Izzi', 5), ('Jefferson', 5), ('Amaro del Capo', 4), ('Montenegro', 4),
         ('Jägermeister', 4), ('Limoncello', 4)]
DISTILLATI = [('Grappa bianca', 4), ('Grappa barricata', 4), ('Passito', 5)]
BERE = [('Acqua naturale o frizzante', 2), ('Birra Raffo 20 cl', 4), ('Birra Raffo 40 cl', 6), ('Calice bianco o rosso', 5),
        ('Calice di prosecco', 4.5), ('Caffè', 1.5)]
ALLERGENI = ['Glutine', 'Crostacei', 'Uova', 'Pesce', 'Arachidi', 'Soia', 'Latte', 'Frutta a guscio', 'Sedano', 'Senape', 'Sesamo',
             'Solfiti', 'Lupini', 'Molluschi']
LEGALE = (f'Servizio e coperto {pf(COPERTO)} a persona. Allergeni: chiedete a chi vi serve (elenco a pagina 7). '
          'Alcuni prodotti possono essere surgelati all\'origine o abbattuti in loco come da procedure HACCP (reg. CE 852/04).')


# ------------------------------------------------------------ RENDER
def piatto(p, i):
    uno = p.get('rank') == 1
    f = foto(p['f']) if (uno and p.get('f')) else None
    cls = 'p' + (' uno' if uno else '') + (' cf' if f else '')
    h = [f'<div class="{cls}">']
    if f:
        h.append(f'<img class="fp" src="{f}" alt="">')
    rk = f'<span class="rank">{p["rank"]}°</span>' if p.get('rank') else ''
    due = ' per due' if p.get('due') else ''
    desc = e(p['d'])
    if not desc:  # niente descrizione: il prezzo resta piccolo, attaccato al nome
        h.append(f'<div class="nome">{rk}{e(p["n"])}<span class="pzn"> | {pf(p["p"])}</span></div>')
    else:
        h.append(f'<div class="nome">{rk}{e(p["n"])}</div>')
    prezzo = f'<span class="pz">{" | " if desc else "| "}{due.strip() + " " if due else ""}{pf(p["p"])}</span>'
    if p.get('d2'):
        prezzo += f', {e(p["d2"])}<span class="pz"> | {pf(p["p2"])}</span>'
    if desc:
        h.append(f'<div class="desc">{desc}{prezzo}</div>')
    if i < 2 and p.get('vino'):
        c, v, col = p['vino']
        h.append(f'<div class="abb">{calice(col)}<b>{e(c)}</b> {e(v)}</div>')
    mk = []
    if p.get('m') is not None and p['m'] > 5:
        mk.append(f'margine {pf(p["m"])}')
    if p.get('pz'):
        mk.append(f'{p["pz"]} pz')
    if p.get('mk'):
        mk.append(p['mk'])
    if mk:
        h.append(f'<div class="mk">{" · ".join(mk)}</div>')
    h.append('</div>')
    return ''.join(h)


def lista(pp, ordine=True):
    pp = ordina(pp) if ordine else pp
    return '<div class="piatti">' + ''.join(piatto(p, i) for i, p in enumerate(pp)) + '</div>'


def nota(t):
    return f'<p class="nota">{t}</p>'


def pag(cls, corpo, n=None, legale=True):
    leg = f'<p class="legale">{LEGALE}</p>' if legale else ''
    num = f'<span class="num">{n}</span>' if n else ''
    return f'<section class="pag {cls}">{corpo}{leg}{num}</section>'


WM = 'brand/logo_antipapa_wordmark_{}.png'


def pagine():
    P = []
    P.append(pag('vino cop', f'''<img class="wm" src="{WM.format('corallo')}" alt="Antipapa · Beato Ristoro">
<div class="claim">Cucina e vini di sostanza</div>
<div class="cop-dove">Fondi · davanti al castello</div>''', legale=False))
    P.append(pag('stretta', f'''<h2>Antipasti</h2>{lista(ANTIPASTI)}
{nota('<b>Rientra l\'Antipasto conviviale</b>: 1.274 pz ≈ 23.000 €, il primo incasso degli antipasti, mancava nella bozza. Rientrano polpette di salsiccia (275) e frittelle di cavolfiore (autunno). Fuori i piatti estivi e quelli a pochi pezzi. Nessuna foto: non c\'è una foto vera coerente con questi piatti.')}
<h2 class="h2s">I nostri maritozzi</h2>{lista(MARITOZZI)}
<div class="fascia"><b>Focaccia calda</b> da accompagnare a tutto<span class="pz"> | 3,5</span></div>
{nota('Fuori il maritozzo al baccalà. La focaccia è il prodotto n.1 del locale (2.298 pz): da 2,95 a 3,5 = +1.896 €/anno.')}''', 2))
    P.append(pag('verde exp', f'''<img class="exp-wm" src="{WM.format('crema')}" alt="">
<div class="exp-t">Antipapa<br>Experience</div>
<p class="exp-s">Ci pensiamo noi: cinque portate dalla nostra carta</p>
<div class="portate">
<div class="pt"><span>I</span>Maritozzo con tartare di manzo</div>
<div class="pt"><span>II</span>Un antipasto di stagione scelto dalla cucina</div>
<div class="pt"><span>III</span>Mezze maniche alla carbonara</div>
<div class="pt"><span>IV</span>Brasato di manzo con purè di patate</div>
<div class="pt"><span>V</span>Un dolce della casa</div></div>
<div class="exp-p"><s>64</s> 58 <small>a persona</small></div>
<p class="exp-n">minimo due persone · bevande escluse · con quattro calici in abbinamento +25</p>
{nota('<b>Experience</b>: cinque portate già in carta, zero referenze nuove in cucina. +6.459 €/anno al 6% dei coperti a cena.')}''', 3))
    P.append(pag('ampia', f'''<h2>Le paste</h2>
<div class="fame"><p class="ft">Che fame hai?</p>
<table><tr><td><svg viewBox="0 0 32 24" width="8mm"><circle cx="16" cy="12" r="7" fill="none" stroke="currentColor" stroke-width="1.4"/></svg><b>Classica</b><span>100 g · inclusa</span></td>
<td><svg viewBox="0 0 32 24" width="10mm"><circle cx="16" cy="12" r="10" fill="none" stroke="currentColor" stroke-width="1.4"/></svg><b>Rafforzata</b><span>150 g · +4</span></td>
<td><svg viewBox="0 0 40 24" width="13mm"><circle cx="14" cy="12" r="10.5" fill="none" stroke="currentColor" stroke-width="1.4"/><path d="M25 12h13" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg><b>Padellone</b><span>220 g in padella · +6</span></td></tr></table></div>
{lista(PASTE)}
{nota('<b>Paste a 4 fisse + 1 di stagione.</b> Rientra il raviolo di stracotto (144 pz, usa il brasato). La pasta di stagione è quella che la cucina batte già (gnocchi zucca e porcini). Fuori le paste estive e quelle con frutti di mare freschi da stoccare. Le 3 paste d\'autore (astice, ricciola, risotto) restano fuori finché la cucina non è stabile: non sono in cassa.')}''', 4))
    P.append(pag('ampia', f'''<h2>I secondi</h2>{lista(SECONDI)}
{nota('Rientrano rollè di maialino (213) e pollo alla cacciatora (140): brasati a lotti. Fuori galletto (48), moscardini, rollè di agnello, pancia, baccalà al vapore. Costata, filetto e ricciola fuori: non sono in cassa.')}''', 5))
    am = ''.join(f'<div class="am"><b>{e(n)}</b><span class="pz"> | {pf(p)}</span></div>' for n, p in AMARI)
    di = ''.join(f'<div class="am"><b>{e(n)}</b><span class="pz"> | {pf(p)}</span></div>' for n, p in DISTILLATI)
    P.append(pag('media', f'''<h2>I dolci</h2>{lista(DOLCI)}
{nota('<b>Dolci a 5, tutti in cassa</b>: rientrano semifreddo alla nocciola (136), anticucciolone, torta di zucca. Fuori i maritozzi dolci deboli (panna 43, cacao 63). Ordine per pezzi: i margini dei dolci non ci sono.')}
<h2 class="h2s">Prima di uscire</h2><div class="due">{am}</div>
<h2 class="h2s">Grappe e passito</h2><div class="due">{di}</div>''', 6))
    be = ''.join(f'<div class="am"><b>{e(n)}</b><span class="pz"> | {pf(p)}</span></div>' for n, p in BERE)
    al = ''.join(f'<li><b>{i}</b> {a}</li>' for i, a in enumerate(ALLERGENI, 1))
    P.append(pag('media bere', f'''<h2>Da bere</h2><div class="due">{be}</div>
<p class="vini">La carta dei vini è a parte: chiedetela, vi aiutiamo a scegliere.</p>
<h2 class="h2s">Allergeni</h2>
<p class="alg-i">Nei nostri piatti possono esserci questi allergeni. Chiedete a chi vi serve: vi diciamo piatto per piatto cosa contiene.</p>
<ol class="alg">{al}</ol>
<p class="haccp">Servizio e coperto {pf(COPERTO)} a persona. Se avete allergie o intolleranze ditelo a chi vi serve prima di ordinare. Alcuni prodotti possono essere surgelati all'origine o abbattuti in loco come previsto dalle procedure HACCP (reg. CE 852/04).</p>
{nota('Allergeni: i numeri accanto ai piatti erano stimati da noi. Tolti finché la cucina non li valida (stessa scelta di Giurgés: scheda a parte in cassa).')}''', 7, legale=False))
    P.append(pag('vino retro', f'''<img class="ret-foto" src="foto_vere/a_sala_ig.jpg" alt="">
<img class="wm wm-s" src="{WM.format('corallo')}" alt="Antipapa">
<div class="info"><p><b>Via Ippolito de' Medici 7</b><br>Fondi, davanti al castello</p>
<p><b>351 432 4634</b><br>per prenotare</p><p><b>@antipapafondi</b></p></div>''', legale=False))
    return P


CSS = open(os.path.join(BASE, 'antipapa.css'), encoding='utf-8').read()
FONTS = 'https://fonts.googleapis.com/css2?family=Tilt+Neon&family=Archivo:ital,wght@0,300;0,400;0,500;0,600;1,400&display=swap'


def pagina():
    P = pagine()
    viste = [('Copertina', [P[0]]), ('Si apre', P[1:3]), ('', P[3:5]), ('', P[5:7]), ('Retro', [P[7]])]
    corpo = ''.join(f'<div class="spread"><p class="etichetta">{t}</p><div class="doppia">{"".join(pp)}</div></div>' for t, pp in viste)
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carta Antipapa 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>{CSS}</style></head><body>
<div class="bar"><b>ANTIPAPA</b><span>Carta 2026 · libro A4 8 facciate · bozza di stampa RBR · serve il sì di Luca</span>
<div class="toggle"><button id="bCli" aria-pressed="true">Vista cliente</button><button id="bCon" aria-pressed="false">Vista consulente</button></div></div>
<div class="piano">{corpo}</div>
<script>(function(){{var b=document.body,c=document.getElementById('bCli'),r=document.getElementById('bCon');
function s(x){{b.classList.toggle('rbr',x);c.setAttribute('aria-pressed',!x);r.setAttribute('aria-pressed',x)}}
c.onclick=function(){{s(false)}};r.onclick=function(){{s(true)}}}})();</script>
</body></html>'''


def stampa(html_path, out):
    from weasyprint import HTML, CSS as WCSS
    css = f'''@page{{size:210mm 297mm;margin:0;bleed:{BLEED}mm;marks:crop}}
@page vino{{background:#690F33}} @page verde{{background:#08311F}}
html,body{{background:#fff !important}} .bar,.etichetta,.nota,.mk,.rank,script{{display:none !important}}
.piano{{padding:0 !important}} .spread,.doppia{{display:block !important;margin:0 !important;box-shadow:none !important}}
.pag{{page-break-after:always;margin:0 !important;box-shadow:none !important}}
.pag.vino{{page:vino}} .pag.verde{{page:verde}}
'''
    doc = HTML(filename=html_path, base_url=BASE).render(stylesheets=[WCSS(string=css)])
    doc.write_pdf(out)
    return len(doc.pages)


if __name__ == '__main__':
    h = os.path.join(BASE, 'antipapa.html')
    open(h, 'w', encoding='utf-8').write(pagina())
    n = stampa(h, os.path.join(BASE, 'Menu_Antipapa_2026.pdf'))
    print('OK antipapa.html · PDF', n, 'pagine', '' if n == 8 else '⚠️ ATTESE 8')

