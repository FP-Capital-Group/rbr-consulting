# -*- coding: utf-8 -*-
"""Carta Giurgés 2026 — soffietto 3 ante e mezza, formato del vecchio menu Mister Pizza:
580 x 297 mm rifilato, ante 160 + 160 + 160 + 100 (fronte), retro speculare 100 + 160 + 160 + 160.

Revisione 07/10/2026 (stampa):
- brand REALE da Instagram @giurges_ (post 2026): terracotta #CB6028, ruggine #A4441C, crema #F2E8DA;
  titoli bastoni pesanti stretti come i post (Bricolage Grotesque 800, larghezza 75), testo Oswald,
  corsivo a mano Caveat Brush (come «sorsi e mozzichi»). Logo vero (lettering crema) su terracotta.
- foto SOLO vere (post Instagram del locale, cartella foto_vere/). Piatto senza foto vera = senza foto.
- contenuti = proposta piatti 07/10 (consegne/2026-10-07/giurges_antipapa_proposta_piatti_2026-10-07.md),
  da far confermare a Luca. Coperto 2,5.
Uso: python3 giurges.py  -> giurges.html (artifact, doppia vista) + Menu_Giurges_2026.pdf (stampa, abbondanza 3 mm)
"""
import os
from comune import pf, e, ordina, foto, BASE

ANTE_F = [160, 160, 160, 100]
ANTE_R = [100, 160, 160, 160]
BLEED = 3
COPERTO = 2.5

# colore del boccale per stile di birra
BIRRA = {'Helles': '#E8B923', 'Tipopils': '#E8B923', 'Leo Weiss': '#F0DFA8', 'Alma': '#C87A2A',
         'Sogno Lucido': '#D89A2E', 'Extra Hop': '#C87A2A', 'Amber Shock': '#A8431C'}


def boccale(col, w=2.6):
    return (f'<svg class="ic" width="{w}mm" height="{w*1.2:.2f}mm" viewBox="0 0 20 24"><path d="M4 3h11v17a2 2 0 01-2 2H6a2 2 0 01-2-2V3z" '
            f'fill="{col}" stroke="#3A2219" stroke-width="1.3"/><path d="M15 7h2.5a1.5 1.5 0 011.5 1.5v4a1.5 1.5 0 01-1.5 1.5H15" '
            f'fill="none" stroke="#3A2219" stroke-width="1.3"/><path d="M4 3c0-1.1 2.4-2 5.5-2S15 1.9 15 3" fill="#FFF6E0" stroke="#3A2219" stroke-width="1.3"/></svg>')


def calice(col, w=2.2):
    return (f'<svg class="ic" width="{w}mm" height="{w*1.5:.2f}mm" viewBox="0 0 16 24"><path d="M3 2h10c0 5-1.6 7.6-4 8.4V20h3v1.6H4V20h3v-9.6C4.6 9.6 3 7 3 2z" '
            f'fill="none" stroke="#3A2219" stroke-width="1.2" stroke-linejoin="round"/><path d="M3.4 3.4h9.2c-.15 3.3-1.3 5.3-4.6 5.9C4.7 8.7 3.55 6.7 3.4 3.4z" fill="{col}"/></svg>')


# ---------------------------------------------------------------- DATI
# m = margine € a porzione (file 02 / stima) · pz = pezzi gen-30 ago 2026 (Smart Manager) · cassa = prezzo medio battuto
# f = nome della foto VERA in foto_vere/ (se manca, niente foto)
ANTIPASTI = [
    dict(n='Il 30 CM', d='Trenta centimetri di panino, da dividere in due', p=20, m=10.75, pz=152, cassa=17.27, birra='Amber Shock',
         mk='FC 41% · da 18 a 20 · per 2: 5,38 a persona · nessuna foto vera: niente foto'),
    dict(n='Il Cestino Goloso', d='Crocchette, alette, dippers e polpette, da dividere', p=14.5, m=10.13, pz=564, cassa=14.09, birra='Helles',
         mk='FC 24% · STAR'),
    dict(n='Tartare di Manzo', d='Battuta al coltello, tuorlo marinato, senape antica', p=14, m=8.02, pz=127, cassa=13.0,
         mk='PUZZLE: margine alto, vende poco → resta e va spinta'),
    dict(n='Pollo Crock', d='Bocconcini di pollo in panatura croccante, salsa della casa', p=9.5, m=6.77, pz=1137, cassa=8.57, mk='FC 22% · STAR'),
    dict(n='Cheddar e Bacon', d='Patate dipper, cheddar fuso, bacon croccante, erba cipollina', p=8.5, m=5.73, pz=677, cassa=7.94, mk='FC 28% · PLOWHORSE'),
    dict(n='Polpette di Melanzane', d='Fritte al momento, cuore di provola, basilico', p=8, m=5.18, pz=339, mk='FC 29%'),
    dict(n='Patate Fritte Dipper', d='Tagliate spesse con la buccia, sale grosso', p=5.5, m=4.09, pz=1222, cassa=4.99, mk='FC 20% · il più ordinato del locale'),
]
INSALATE = [
    dict(n='Pollo Salad', d='Pollo grigliato, insalata mista, pomodorini, mais, salsa allo yogurt', p=13.5, m=None, pz=184, cassa=13.35,
         mk='in cassa 13,35: portato a 13,5'),
    dict(n='Insalata di Brace', d='Straccetti di scottona alla griglia, rucola, grana, pomodorini', p=15, m=None, pz=0,
         mk='NOVITÀ (serve il sì di Luca) · stessa carne della Tagliata, nessuna materia prima nuova'),
]
CONTORNI = [
    dict(n='Patate al burro', d='Novelle, burro e rosmarino', p=6, m=4.70, pz=164),
    dict(n='Cicoria ripassata', d='Aglio e peperoncino', p=6, m=4.45, pz=148),
    dict(n='Insalata mista', d='Verdure di stagione', p=5, m=4.05, pz=54),
    dict(n='Pannocchia alla griglia', d='Con burro salato', p=5, m=3.35, pz=76),
]
GROSSI = [
    dict(n='Il Fondano Reale', d='Il nostro Fondano, rinforzato con le ribs sfilacciate in salsa BBQ', p=24, m=14.2, birra='Extra Hop',
         mk='NOVITÀ (sì di Luca) · margine stimato · oggi «Il Fondano» 196 pz a 15'),
    dict(n='Brace e Burrata', d='La nostra Tagliata di scottona alla brace, con la burrata', p=23, m=13.6, birra='Sogno Lucido',
         mk='NOVITÀ (sì di Luca) · margine stimato · burrata da confermare in dispensa'),
    dict(n='Il Sovrano', d='Doppio burger di scottona, doppio cheddar, guanciale croccante', p=22, m=13.0,
         mk='NOVITÀ (sì di Luca) · margine stimato · tutto già in linea'),
]
PANINI = [
    dict(n='Un Americano a Roma', d='Bun al latte, burger di manzo, cipolla caramellata, pomodoro, provola affumicata, guanciale, maionese al pomodoro',
         p=14.5, m=9.30, pz=918, cassa=14.0, birra='Tipopils', taglie=True, f='g_americano_ig', mk='FC 31% · foto vera dal post Instagram del 01/10'),
    dict(n='Camembert Crispy', d='Camembert impanato e fritto, confettura di cipolle, insalata', p=13, m=9.14, pz=100, cassa=13.0, birra='Alma',
         mk='FC 23% · rende più dello Smoderato e vende 16 volte meno'),
    dict(n='Lo Smoderato', d='Burger di scottona, cheddar, bacon, cipolla croccante, salsa Giurgés', p=14.5, m=8.80, pz=1649, cassa=13.51,
         taglie=True, mk='FC 34% · il piatto n.1 del locale · L\'Esagerato (73 pz a 19) diventa la taglia XL'),
    dict(n='Pollo Cornflakes', d='Petto di pollo in panatura di cornflakes, insalata, salsa allo yogurt', p=13, m=None, pz=526, cassa=12.99,
         mk='scheda ricetta mancante'),
    dict(n='Porchetta Pork', d='Il panino con la nostra porchetta', p=15, m=None, pz=209, cassa=14.7,
         mk='RIENTRA: 209 pz ≈ 3.071 € · ingredienti da confermare con Luca'),
    dict(n='Sandwich Ribs', d='Costine sfilacciate in salsa BBQ, cipolla croccante, salsa della casa', p=15, m=None, pz=141, cassa=15.0,
         mk='141 pz in cassa ma non era in carta · ingredienti da confermare'),
    dict(n='Burrito Messico-Fondano', d='Tortilla, carne speziata, fagioli neri, cheddar, guacamole', p=13.5, m=None, pz=251, cassa=13.5,
         mk='in cassa 13,5'),
]
GRIGLIA = [
    dict(n='La Tagliata', d='Controfiletto di scottona, rucola, grana, riduzione al balsamico', p=25, m=13.68, pz=343, cassa=24.61,
         birra='Amber Shock', mk='FC 40% · nessuna foto vera della tagliata: niente foto'),
    dict(n='Stinco di Maiale', d='Intero, cotto lentamente, croccante fuori', p=19.5, m=13.52, pz=305, cassa=19.49, birra='Leo Weiss',
         mk='era 19 in carta sotto la cassa (19,49): portato a 19,5'),
    dict(n='Ribs BBQ', d='Costine di maiale, sei ore a bassa temperatura, glassa BBQ', p=15.5, m=10.89, pz=430, cassa=15.35,
         mk='era 15 sotto la cassa (15,35): portato a 15,5'),
    dict(n='Coscia Mediterranea', d='Coscia di pollo marinata alle erbe, limone, olive taggiasche', p=14, m=9.63, pz=392, cassa=13.21, mk='FC 24%'),
    dict(n='Bombette allo Spiedo', d='Involtini di capocollo ripieni di caciocavallo', p=14, m=None, pz=273, cassa=13.98, mk='scheda ricetta mancante'),
]
SPINA = [  # nome, stile, formati
    ('Helles', 'Chiara', [('20 cl', 3), ('40 cl', 5)]),
    ('Tipopils', 'Chiara luppolata', [('30 cl', 4.5), ('50 cl', 6.5)]),
    ('Leo Weiss', 'Bianca di frumento', [('30 cl', 4.8), ('50 cl', 7)]),
    ('Alma', 'Ambrata', [('40 cl', 6)]),
    ('Sogno Lucido', 'Dorata forte', [('30 cl', 5.5), ('50 cl', 8)]),
    ('Extra Hop', 'Ambrata luppolata', [('30 cl', 5), ('50 cl', 6.5)]),
    ('Amber Shock', 'Rossa doppio malto', [('30 cl', 6), ('50 cl', 8)]),
]
VINI = [  # nome, dettaglio, calice, bottiglia, colore calice
    ('Tonaghe', 'Cannonau di Sardegna', 5.5, 24, '#7E1B33'),
    ('Tyrsos', '', 5.5, 23, '#7E1B33'),
    ('150 Tramonti', 'Primitivo, Puglia', 5.5, 26, '#7E1B33'),
    ('40 Soli', 'Negroamaro, Puglia', 5.5, 24, '#7E1B33'),
    ('753', 'Sangiovese, Lazio', 5.5, 24, '#7E1B33'),
    ('Mastarna', 'Chardonnay', 5.5, 24, '#E4D08A'),
    ('Jagur Bernardi', 'Bollicina', 5.5, 19, '#F2E7C4'),
]
DOLCI = [
    dict(n='Tiramisù', d='Savoiardi, caffè, crema al mascarpone, cacao', p=6, m=4.05, pz=81),
    dict(n='Brownies', d='Cioccolato fondente e noci pecan, tiepido', p=6, m=3.95, pz=141),
    dict(n='Cheesecake', d='Nutella, Lotus, frutti di bosco o caramello salato', p=6, m=3.75, pz=888,
         mk='4 gusti in cassa: 888 pz, la famiglia più venduta · Lotus (231) rientra · pistacchio fuori'),
    dict(n='Tortino al cioccolato', d='Cuore caldo, gelato alla vaniglia', p=6.5, m=None, pz=174),
    dict(n='Semifreddo Snickers', d='Arachidi, caramello, cioccolato al latte', p=6, m=None, pz=108),
    dict(n='Crêpes', d='Nutella e granella, oppure pistacchio', p=5.5, m=None, pz=275, mk='in cassa 5: proposta 5,5'),
]
AMARI = [('Valhalla', 5), ('Jefferson', 5), ('Erbes Izzo', 5), ('Amaro Formidabile', 6), ('Amaro del Capo', 4),
         ('Jägermeister', 4), ('Limoncello', 4)]
MENU = [
    dict(t='GIURGÉS', steps=['Un antipasto', 'Un panino', 'Un dolce'], p=24, barrato=29, mk='era 21: −28% sulla carta, ora −17% · +2,7 di margine a menù'),
    dict(t='GIURGÉS GRIGLIA', steps=['Un antipasto', 'Un piatto dalla griglia', 'Un contorno', 'Un dolce'], p=31, barrato=37,
         mk='era 28: −24%, ora −16% · +2,7 a menù'),
    dict(t='PEZZO GROSSO', steps=['Un antipasto', 'Un Pezzo Grosso', 'Un dolce', 'Un calice di vino'], p=37, barrato=43, oro=True,
         mk='era 34: −21%, ora −14% · +2,7 a menù'),
]
TAGLIE = [('M', 'inclusa'), ('L', '+4'), ('XL', '+7')]
AGGIUNTE = [('Bacon croccante', 2), ('Cheddar fuso', 1.5), ('Guanciale', 2.5)]
LEGALE = (f'Servizio e coperto {pf(COPERTO)} a persona. Allergeni: chiedete al personale la lista completa. '
          'Alcuni prodotti possono essere surgelati all\'origine o abbattuti in loco come da procedure HACCP (reg. CE 852/04).')


# ---------------------------------------------------------------- RENDER
def piatto(p, i):
    uno = p.get('rank') == 1
    f = foto(p['f']) if (uno and p.get('f')) else None
    cls = 'p' + (' uno' if uno else '') + (' cf' if f else '')
    h = [f'<div class="{cls}">']
    if f:
        h.append(f'<img class="fp" src="{f}" alt="">')
    nome = f'<span class="rank">{p["rank"]}°</span>' if p.get('rank') else ''
    nome += e(p['n'])
    if p.get('taglie'):
        nome += ' <span class="tg">' + ''.join(f'<i>{t}</i>' for t, _ in TAGLIE) + '</span>'
    h.append(f'<div class="nome">{nome}</div>')
    h.append(f'<div class="desc">{e(p["d"])}<span class="pz"> | {pf(p["p"])}</span></div>')
    if i < 2 and p.get('birra'):
        h.append(f'<div class="abb">{boccale(BIRRA[p["birra"]])}{e(p["birra"])}</div>')
    mk = []
    if p.get('m') is not None:
        mk.append(f'margine {pf(p["m"])}')
    if p.get('pz'):
        mk.append(f'{p["pz"]} pz')
    if p.get('cassa'):
        mk.append(f'cassa {pf(p["cassa"])}')
    if p.get('mk'):
        mk.append(p['mk'])
    if mk:
        h.append(f'<div class="mk">{" · ".join(mk)}</div>')
    h.append('</div>')
    return ''.join(h)


def lista(piatti, ordine=True):
    pp = ordina(piatti) if ordine else piatti
    return '<div class="piatti">' + ''.join(piatto(p, i) for i, p in enumerate(pp)) + '</div>'


def nota(t):
    return f'<p class="nota">{t}</p>'


def legale(cls='legale'):
    return f'<p class="{cls}">{LEGALE}</p>'


def fronte():
    a1 = f'''<section class="anta a1" style="left:0;width:{ANTE_F[0]}mm">
  <h2>Antipasti</h2>{lista(ANTIPASTI)}
  {nota('<b>Antipasti a 7</b>: il 30 CM (n.1 per margine) in seconda posizione e in cornice. Fuori Caciocavallo e salsiccia (FC 35%), Frittata cacio e pepe, Metà 30 CM, Arancino, Alette, Crudo&Carbo, Gorgonzola e tartufo, Crocchetta, Puorkettozzo. Nessuna foto: non esiste una foto vera del 30 CM.')}
  <h2 class="h2s">Le insalate</h2>{lista(INSALATE, False)}
  {nota('Fuori il Polpo Salad (24 pz in 8 mesi: polpo da tenere solo per lei). Entra l\'Insalata di Brace, con la carne della Tagliata.')}
  <h2 class="h2s">I contorni</h2><div class="due">{lista(CONTORNI)}</div>
  {legale()}
</section>'''
    gros = ''.join(piatto(p, i) for i, p in enumerate(ordina(GROSSI)))
    tg = ' · '.join(f'<span class="tgl"><i>{t}</i> {v}</span>' for t, v in TAGLIE)
    agg = ' · '.join(f'<span class="ag"><b>{e(n)}</b> +{pf(pr)}</span>' for n, pr in AGGIUNTE)
    a2 = f'''<section class="anta a2" style="left:{ANTE_F[0]}mm;width:{ANTE_F[1]}mm">
  <div class="grossi"><h2>I Pezzi Grossi</h2>{gros}</div>
  {nota('<b>Pezzi Grossi = novità della call del 1/10, fatte solo con quello che la cucina ha già.</b> Servono il sì di Luca e la conferma della burrata. Ancoraggio: dopo aver letto 24, un panino da 14,5 sembra il prezzo giusto. Bastano 8 clienti su 100: +2.109 €/anno.')}
  <h2>I Panini</h2>
  <p class="tgleg">{tg} <span class="tgx">doppio e triplo burger</span></p>
  {lista(PANINI)}
  <p class="bimbo"><b>Panino bimbo</b> cotoletta, hamburger o würstel, con le patatine<span class="pz"> | 7</span></p>
  <p class="aggiunte"><span class="agt">La vuoi ancora più buona?</span> {agg}</p>
  {nota('Rientra il Porchetta Pork (209 pz, ≈3.071 €). Fuori Panino hamburger semplice (resta nel menù bimbi), Broccolino, Guancia Boom, Pollo rustico, Rampollo; L\'Esagerato diventa la taglia XL. Foto solo sul n.1 (Americano a Roma): è la foto vera del post Instagram del 1/10.')}
  {legale()}
</section>'''
    spina = ''.join(f'<div class="lr">{boccale(BIRRA[n], 3)}<span class="ln"><b>{e(n)}</b> {e(s)}</span>'
                    f'<span class="lp"> · {" · ".join(f"{c} {pf(v)}" for c, v in fm)}</span></div>' for n, s, fm in SPINA)
    vini = ''.join(f'<div class="lr">{calice(col, 2.4)}<span class="ln"><b>{e(n)}</b> {e(d)}</span>'
                   f'<span class="lp"> · calice {pf(c)} · bottiglia {pf(b)}</span></div>' for n, d, c, b, col in VINI)
    a3 = f'''<section class="anta a3" style="left:{sum(ANTE_F[:2])}mm;width:{ANTE_F[2]}mm">
  <h2>Dalla Griglia</h2>{lista(GRIGLIA)}
  {nota('Fuori il Petto di pollo. Stinco e Ribs erano in carta sotto il prezzo che la cassa batte già. La Tagliata (n.1) è senza foto: non c\'è una foto vera.')}
  <h2 class="h2s">Alla spina</h2><div class="lst">{spina}</div>
  <h2 class="h2s">I vini</h2><div class="lst">{vini}</div>
  {nota('Vini sul venduto: il calice più venduto (Tyrsos) non era in carta. Calice 5,5.')}
  {legale()}
</section>'''
    menu = ''.join(f'''<div class="combo{' oro' if m.get('oro') else ''}"><div class="ct">{e(m['t'])}</div>
<div class="cs">{'<br>'.join(e(s) for s in m['steps'])}</div>
<div class="cp"><s>{pf(m['barrato'])}</s> {pf(m['p'])} <small>a persona</small></div><div class="mk">{m['mk']}</div></div>''' for m in MENU)
    a4 = f'''<section class="anta scura fine" style="left:{sum(ANTE_F[:3])}mm;width:{ANTE_F[3]}mm">
  <h2 class="hm">I nostri menù</h2>{menu}
  <p class="legale">Per tutto il tavolo. Antipasto a scelta escluso Cestino Goloso e 30 CM. Bevande escluse dove non indicate. Servizio e coperto {pf(COPERTO)} a persona.</p>
</section>'''
    return f'<div class="blocco"><p class="etichetta">Fronte · aperto (interno)</p><div class="foglio" style="width:{sum(ANTE_F)}mm">{a1}{a2}{a3}{a4}</div></div>'


def retro():
    am = ''.join(f'<div class="am"><b>{e(n)}</b><span class="pz"> | {pf(p)}</span></div>' for n, p in AMARI)
    r1 = f'''<section class="anta r1" style="left:0;width:{ANTE_R[0]}mm">
  <h2>I Dolci</h2>{lista(DOLCI)}
  <h2 class="h2s">Prima di andare via</h2><div class="amari">{am}</div>
  <p class="caffe"><b>Caffè</b><span class="pz"> | 1,5</span></p>
  {legale()}
  {nota('Dolci a 6: fuori Cheesecake pistacchio, Pinacolada, Tozzette, Bomboncini. Amari dalla cassa.')}
</section>'''
    r2 = f'''<section class="anta terra" style="left:{ANTE_R[0]}mm;width:{ANTE_R[1]}mm">
  <p class="script">sorsi e mozzichi</p>
  <p class="big">Brace accesa<br>tutte le sere.</p>
  <div class="coll"><img class="c1" src="foto_vere/g_burger_ig.jpg" alt=""><img class="c2" src="foto_vere/g_ribs_ig.jpg" alt=""></div>
  <p class="small">Panini, griglia e birra alla spina dal 2009.</p>
</section>'''
    r3 = f'''<section class="anta r3" style="left:{sum(ANTE_R[:2])}mm;width:{ANTE_R[2]}mm">
  <div class="info">
    <div class="ir"><span class="k">Dove siamo</span><span class="v">Via Arnale Rosso 31, Fondi</span></div>
    <div class="ir"><span class="k">Per prenotare</span><span class="v">342 147 4739</span></div>
    <div class="ir"><span class="k">Seguiteci</span><span class="v">@giurges_</span></div>
    <div class="ir"><span class="k">Ogni sera</span><span class="v">la terrazza al secondo piano</span></div>
  </div>
  <img class="hero3" src="foto_vere/g_cucina_ig.jpg" alt="">
  <p class="legale">I prezzi sono in euro e comprendono l'IVA. {LEGALE}</p>
</section>'''
    r4 = f'''<section class="anta terra cop fine" style="left:{sum(ANTE_R[:3])}mm;width:{ANTE_R[3]}mm">
  <img class="logo" src="brand/logo_giurges_crema.png" alt="Giurgés">
</section>'''
    return f'<div class="blocco"><p class="etichetta">Retro · chiuso (esterno): a destra la copertina</p><div class="foglio" style="width:{sum(ANTE_R)}mm">{r1}{r2}{r3}{r4}</div></div>'


CSS = open(os.path.join(BASE, 'giurges.css'), encoding='utf-8').read()
FONTS = ('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wdth,wght@12..96,75..100,600;12..96,75..100,800'
         '&family=Oswald:wght@300;400;500&family=Caveat+Brush&display=swap')


def pagina():
    return f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Carta Giurgés 2026</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONTS}">
<style>{CSS}</style></head><body>
<div class="bar"><b>GIURGÉS</b><span>Carta 2026 · soffietto 580×297 · bozza di stampa RBR · serve il sì di Luca</span>
<div class="toggle"><button id="bCli" aria-pressed="true">Vista cliente</button><button id="bCon" aria-pressed="false">Vista consulente</button></div></div>
<div class="piano">{fronte()}{retro()}</div>
<script>(function(){{var b=document.body,c=document.getElementById('bCli'),r=document.getElementById('bCon');
function s(x){{b.classList.toggle('rbr',x);c.setAttribute('aria-pressed',!x);r.setAttribute('aria-pressed',x)}}
c.onclick=function(){{s(false)}};r.onclick=function(){{s(true)}}}})();</script>
</body></html>'''


def stampa(html_path, out):
    from weasyprint import HTML, CSS as WCSS
    W = sum(ANTE_F)
    css = f'''@page{{size:{W}mm 297mm;margin:0;bleed:{BLEED}mm;marks:crop}}
html,body{{background:#fff !important}} .bar,.etichetta,.nota,.mk,.rank,script{{display:none !important}}
.piano{{padding:0 !important}} .blocco{{margin:0 !important;page-break-after:always}} .blocco:last-child{{page-break-after:auto}}
.foglio{{box-shadow:none !important;zoom:1 !important;overflow:visible !important}}
.anta{{height:297mm !important}}
.anta.fine{{border-right:{BLEED}mm solid var(--bgfine) !important}}
.blocco:nth-of-type(1) .anta.fine{{width:{ANTE_F[3]+BLEED}mm !important}}
.blocco:nth-of-type(2) .anta.fine{{width:{ANTE_R[3]+BLEED}mm !important}}
'''
    doc = HTML(filename=html_path, base_url=BASE).render(stylesheets=[WCSS(string=css)])
    doc.write_pdf(out)
    return len(doc.pages)


if __name__ == '__main__':
    h = os.path.join(BASE, 'giurges.html')
    open(h, 'w', encoding='utf-8').write(pagina())
    n = stampa(h, os.path.join(BASE, 'Menu_Giurges_2026.pdf'))
    print('OK giurges.html · PDF', n, 'pagine', '(attese 2)' if n == 2 else '⚠️ ATTESE 2')

