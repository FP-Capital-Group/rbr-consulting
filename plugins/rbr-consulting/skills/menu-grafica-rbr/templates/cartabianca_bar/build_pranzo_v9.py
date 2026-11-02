# -*- coding: utf-8 -*-
"""Carta ingegnerizzata del pranzo dei 7 bar Cartabianca — autunno 2026 (A4 fronte/retro, doppia vista).
Fissi: menu ottimale del modello di scelta v3 (../modello_scelta/menu_scelta.json).
Feedback Marco + Luciano 06/10: copertina della famiglia del «Menu del bar a libro» (niente «il PRANZO»); primo e secondo del giorno
FUORI carta (li dice il personale, resta una riga); contorni «Scegli il tuo contorno» 8/10/12 (proposta da confermare);
prezzo su una riga sua sotto ogni piatto; secondi in evidenza a destra con corpo più grande.
Prezzi: colonna PREZZO FINALE del tab «Prezzi BAR» del foglio «Prezzi definitivi - Cartabianca» (../prezzi_live.json,
scaricato da ../prezzi_live.py); se il piatto non è nel foglio, prezzo dei piatti simili (segnalato in vista consulente).
Regole RBR (Marco 03/10): in ogni sezione ordine per margine col n.1 al 2° posto, poi a scendere; evidenziato solo il n.1
con l'asticella rossa; foto solo sul n.1, al massimo una per pagina; niente riquadri pieni o col bordo; blocchi speciali
su fascia crema chiara.
06/10 sera (Marco): prezzo IN CODA alla descrizione (due righe, «… | 9,5»), piccolo, mai bold, colore tenue; n.1 per margine di
ogni sezione in riquadro con etichetta («la scelta dello chef» / «da provare») e foto vera o, se manca, illustrazione a tratto;
«il più amato» sul più venduto; copertina calda «A pranzo da noi»; misure di porzioni e contorni col prezzo sulla stessa riga.
Uscita: carta_pranzo_bar.html (artifact) → pdf_menu.py libro → Menu_Cartabianca_Pranzo_Bar_Autunno_2026.pdf
v9 (08/10/2026, feedback Emiliano 07/10): COPIA di build_pranzo.py (v8 resta rigenerabile). Unica differenza: una seconda
insalatona a base di tonno («Insalata tonno e fagioli», PROPOSTA prezzo 11 = come l'insalata al tonno, food cost STIMA RBR
dal listino «Prezzi ingredienti» del file 02). Uscita: carta_pranzo_bar_v9.html + leve_pranzo_v9.json."""
import base64, html, json, os

HERE = os.path.dirname(os.path.abspath(__file__))
UP = os.path.dirname(HERE)
E = html.escape
IVA = 1.1
def eur(x): return f"{x:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
def prz(x):
    """prezzo in carta senza zeri finali (Marco 05/10): 10 · 10,2 · 12,5"""
    return (f'{x:.2f}'.rstrip('0').rstrip('.')).replace('.', ',')
def intero(x): return f"{round(x):,}".replace(',', '.')

PL = {r['Prodotto'].strip().lower(): r for r in json.load(open(os.path.join(UP, 'prezzi_live.json'), encoding='utf-8'))['Prezzi BAR']}
def fin(prodotto, ripiego):
    """PREZZO FINALE del foglio per il prodotto di cassa; se manca, il prezzo dei simili (ripiego)."""
    r = PL.get(prodotto.strip().lower())
    v = r and r.get('PREZZO FINALE')
    return (float(v), True) if isinstance(v, (int, float)) and v > 0 else (ripiego, False)
def pf(prodotto, ripiego): return fin(prodotto, ripiego)[0]

MS = json.load(open(os.path.join(UP, 'modello_scelta', 'menu_scelta.json')))['menu']
MOD = {p['piatto']: p for c in ('primi', 'secondi', 'freddi') for p in MS[c]['fissi']}
CHEF_P = MS['primi']['chef_candidati']; CHEF_S = MS['secondi']['chef_candidati']

# ---- ipotesi di volume (venduto CIC 7 bar mar-ago 2026 ×2, modello v3)
BAR, GIORNI = 7, 250
PRIMI_ANNO = MS['primi']['pezzi_categoria_giorno'] * BAR * GIORNI          # ~47k primi
FREDDI_ANNO = MS['freddi']['pezzi_categoria_giorno'] * BAR * GIORNI        # ~12k piatti freddi
PRANZI_ANNO = 80_000                                                       # coperti pranzo stimati (92k piatti/anno)
GUAD_MIX = sum(MS[c]['guadagno_lo'] for c in ('primi', 'secondi', 'freddi')) * BAR * GIORNI

def piatto(nome, desc, prezzo, chiave=None, alg='', nota_prezzo='', mk=None, fc=None, pezzi=None):
    m = MOD.get(chiave) if chiave else None
    fc = m['fc'] if m else fc
    mn = prezzo / IVA - fc if fc is not None else None
    if mk is None and mn is not None:
        mk = f"margine {eur(mn)} € a {prz(prezzo)} · FC {fc / (prezzo / IVA) * 100:.0f}%"
        mk += f" · {m['x']:.1f} al giorno in un bar medio · {m['k']}" if m else (f" · {intero(pezzi)} pz/anno" if pezzi else '')
    if nota_prezzo: mk = (mk + ' · ' if mk else '') + nota_prezzo
    vend = m['x'] if m else (pezzi if isinstance(pezzi, (int, float)) else 0)
    return dict(nome=nome, desc=desc, new=prezzo, ev='', alg=alg, mk=mk or '', foto=False, m=mn, vend=vend)

def simile(chiave, ripiego, testo):
    """prezzo dal foglio se il piatto c'è; altrimenti il prezzo dei simili, con la nota per la vista consulente"""
    v, ok = fin(chiave, ripiego)
    return v, ('prezzo finale del foglio' if ok else testo)

_v, _n = simile('Penne Integrali Pomodori Secchi + Mandorle + Pecorino', 10.00, 'non nel foglio: come le paste di carne e verdure (10,00)')
PRIMI = [
    piatto('Penne integrali ai pomodori secchi', 'mandorle tostate e una spolverata di pecorino', _v,
           'Penne Integrali Pomodori Secchi + Mandorle + Spolverata di Pecorino', alg='1-7-8', nota_prezzo=_n),
    piatto('Spaghettone quadrato burro e bottarga', 'bottarga di muggine e scorza di limone', pf('Spaghettone Quadrato Burro + Bottarga + Limone', 10.20),
           'Spaghettone Quadrato Burro + Bottarga + Limone', alg='1-4-7', nota_prezzo='prezzo finale del foglio'),
    piatto("Tagliatelle all'uovo, zucca e salsiccia", 'crema di zucca gialla e salsiccia toscana', pf("Tagliatelle all'Uovo Crema di Zucca + Salsiccia", 10.00),
           "Tagliatelle all'Uovo Crema di Zucca Gialla + Salsiccia", alg='1-3', nota_prezzo='prezzo finale del foglio'),
    piatto('Pici al ragù bianco', 'pici freschi e ragù bianco di carne, cotto piano', pf('Pici Ragù Bianco', 10.00), 'Pici Ragù Bianco', alg='1-9',
           nota_prezzo='prezzo finale del foglio'),
    piatto("Gnocchetti all'ortolana", 'gnocchetti di patate e verdure di stagione', pf("Gnocchetti all'Ortolana", 9.90), "Gnocchetti all'Ortolana", alg='1-7',
           nota_prezzo='prezzo finale del foglio'),
]
PC = [pf('Pasta Corta Pomarola', 8.0), pf('Pasta Corta Pesto', 8.5), pf('Pasta Corta Cacio e Pepe', 8.5)]
PASTA_CORTA = dict(nome='Pasta corta come la vuoi', desc='la pasta corta di tutti i giorni', new=PC[1],
                   prz=f'al pomodoro <span class="sep">|</span> <span class="pz">{prz(PC[0])}</span> · al pesto <span class="sep">|</span> <span class="pz">{prz(PC[1])}</span>', ev='', alg='1-7-8',  # 08/10: 8 = frutta a guscio del pesto (pinoli/anacardi), per prudenza
                   mk='la base: resta fuori dalla classifica · prezzi finali del foglio', foto=False)
SECONDI = [
    piatto('Polpo con patate prezzemolate', 'polpo morbido, patate e prezzemolo', pf('Polpo + Patate Prezzemolate', 13.50), 'Polpo + Patate Prezzemolate', alg='14',
           nota_prezzo='prezzo finale del foglio'),
    piatto('Zuppetta di gamberetti', 'con i crostoni di pane tostato', pf('Zuppetta di Gamberetti + Crostoni', 13.50), 'Zuppetta di Gamberetti + Crostoni di pane', alg='1-2',
           nota_prezzo='prezzo finale del foglio · il margine più alto del pranzo ma la vedono in pochi: va spinta'),
    piatto('Bocconcini di pollo al curry', 'verdure e riso basmati', pf('Bocconcini pollo Curry con Verdure + Basmati', 13.50),
           'Bocconcini pollo Curry con Verdure + Basmati', alg='7', nota_prezzo='prezzo finale del foglio'),
    piatto('Scaloppine di maiale al vino bianco', 'con un contorno dal buffet', pf('Scaloppine di Maiale al Vino Bianco', 13.00),
           'Scaloppine di Maiale al Vino Bianco', alg='1-12', nota_prezzo='prezzo finale del foglio (13 deciso da Marco 05/10): secondo più venduto, +8k €/anno · da far approvare a Massimo'),
    # 07/10 Emiliano + Marco: un secondo «classico» tutti i giorni al posto del petto di pollo (roast-beef 1.390 pz/anno, arista 1.144, fesa/tacchino ~1.160);
    # food cost = media file 02 (roast-beef 4,16 · arista 3,01 · fesa 3,49)
    piatto('Il classico', 'roast-beef, arista al forno o fesa di tacchino, con un contorno dal buffet', 13.00, fc=3.55,
           nota_prezzo='nuovo 07/10 (Emiliano): sostituisce il petto di pollo · 13 deciso da Marco · da creare in cassa e nel foglio'),
]
# 07/10 Marco: 4 proposte, scelte per MARGINE TOTALE L'ANNO (margine a piatto × pezzi venduti), food cost e ingredienti dal file 02;
# via carpacci e crudo (vendono poco: 212-366 pz/anno), dentro le insalate che vendono (tonno 1.644, Design 904, greca 660) + la Caesar
FREDDI = [
    piatto('Insalata al tonno', 'insalata mista, filetto di tonno, pomodorini e olive', 11.00, fc=3.26, alg='4',
           nota_prezzo='11 deciso da Marco 07/10 (oggi 10): la più venduta dei freddi, 1.644 pz/anno, margine 6,74 → 11,1k €/anno · da aggiornare in cassa e nel foglio'),
    piatto('Insalata Design', 'insalata mista, pomodorini, scaglie di grana e noci', pf('INSALATA DESIGN', 10.00), fc=1.92, alg='7-8',
           nota_prezzo='904 pz/anno, margine 7,17 → 6,5k €/anno · prezzo finale del foglio'),
    piatto('Insalata greca', 'insalata mista, feta, pomodorini e olive', pf('INSALATA GRECA', 10.00), fc=2.62, alg='7',
           nota_prezzo='660 pz/anno, margine 6,47 → 4,3k €/anno · prezzo finale del foglio'),
    piatto('Insalata Caesar', 'pollo, crostini, grana e la nostra salsa Caesar', 13.00, 'Insalata Caesar', alg='1-3-4-7',
           nota_prezzo='voluta da Marco 07/10 · 13 = prezzo di cassa (foglio 12, Marco 07/10 sera: resta 13)'),
    # 08/10 sera (Marco): via l'insalata tonno e fagioli, torna il carpaccio di bresaola di prima (366 pz/anno)
    piatto('Carpaccio di bresaola', 'rucola e scaglie di grana', pf('Carpaccio di Bresaola + Rucola + Grana', 13.50),
           'Carpaccio di Bresaola + Rucola + Grana', alg='7', nota_prezzo='prezzo finale del foglio · rimesso da Marco 08/10 al posto di tonno e fagioli'),
]
for _p, _v in zip(FREDDI, (1644, 904, 660, 0, 366)): _p['vend_anno'] = _v
# dolci: food cost ingredienti dal file «02 - Food Cost Bar» (tab PASTE / COSTO PEZZO PASTICCERIA), prezzi finali del foglio
def dolce(nome, desc, prod, fc, alg='1-3-7'):
    r = PL.get(prod.lower(), {})
    return piatto(nome, desc, pf(prod, 3.20), alg=alg, fc=fc, pezzi=r.get("Pezzi l'anno"))
DOLCI = [
    dolce('Crostata mora e albicocca', 'la fetta, frolla al burro', 'Crostata Mora Albicocca', 0.54),
    dolce('Cannolo siciliano', "ricotta e scorza d'arancia", 'Cannolo Siciliano', 0.65, alg='1-7'),
    # 07/10 Emiliano + Marco: i mignon del banco al posto del tiramisù (2 mignon a prezzo pieno di cassa, 1,20 l'uno)
    piatto('Due mignon', 'due mignon a scelta dalla nostra pasticceria', 2.40, fc=0.38, alg='1-3-7', nota_prezzo='nuovo 07/10: sostituisce il tiramisù · 2 × 1,20 di cassa'),
    dolce('Crostatina alla frutta', 'crema pasticcera e frutta fresca', 'Crostatina frutta', 0.46),
    dolce('Millefoglie', 'sfoglia croccante e crema chantilly', 'Millefoglie Monoporzione', 0.21),
    dolce('Crostata pistacchio e nocciola', 'la fetta', 'Crostata Pistacchio e Nutella', 0.54, alg='1-3-7-8'),
    dolce('Bignè', 'alla crema o al cioccolato', 'Bignè', 0.30),
]
CHEF = (pf('Primo dello Chef', 9.70), pf('Secondo dello Chef', 13.50))
VERD = (pf('Piatto Verdure Piccolo', 5.90), pf('Piatto Verdure Grande', 9.50), pf('Macedonia', 4.80))
AMARO = pf('Amaro', 4.50)

def ordina(lst, foto=False):
    """regola RBR: n.2 per margine in cima, n.1 al 2° posto (asticella rossa, foto se è il piatto-foto della pagina), poi a scendere"""
    r = sorted([p for p in lst if p.get('m') is not None], key=lambda p: -p['m'])
    for i, p in enumerate(r): p['rank'] = i + 1
    r[0]['ev'] = 'asta'; r[0]['foto'] = foto
    if len(r) > 1: r[0], r[1] = r[1], r[0]
    return r

# ---- leve €/anno (ipotesi dichiarate)
L_ABB = PRIMI_ANNO * 0.08 * (2.00 / IVA - 0.35)               # 8 primi su 100 «abbondante» +2 (+50 g pasta e sugo ≈ 0,35)
L_EXT = PRIMI_ANNO * 0.03 * (4.00 / IVA - 0.70)               # 3 primi su 100 «extra abbondante» +4 (+100 g ≈ 0,70)
L_DOL = PRANZI_ANNO * 0.05 * 1.50                              # 5 dolci in più ogni 100 pranzi, margine 1,50
L_AMA = PRANZI_ANNO * 0.03 * (AMARO / 1.22 - 0.50)              # 3 amari in più ogni 100 pranzi
LEVE = [
    ("Fissi d'autunno scelti dal modello (stessi clienti, scelgono piatti che rendono di più)", 'fronte', GUAD_MIX),
    ('Primi «abbondante» +2,00 (8 su 100)', 'fronte', L_ABB),
    ('Primi «extra abbondante» +4,00 (3 su 100)', 'fronte', L_EXT),
    ('Dolci in carta, in ordine di margine (5 in più ogni 100 pranzi)', 'retro', L_DOL),
    ('Amaro dopo pranzo (3 in più ogni 100 pranzi)', 'retro', L_AMA),
]
TOT = sum(x[2] for x in LEVE)

def img64(f):
    return 'data:image/' + ('png' if f.endswith('png') else 'jpeg') + ';base64,' + base64.b64encode(open(os.path.join(HERE, 'img', f), 'rb').read()).decode()
LOGO = img64('logo_hd_2400.png'); LOGO_T = LOGO  # logo ufficiale da PDF (img/Logo_Cartabianca.pdf), trasparente
# prezzi del pranzo già decisi sul foglio (contati a parte, nei prezzi del bar)
PRZ_PRANZO = sum(r["Margine in più l'anno FINALE"] or 0 for r in PL.values()
                 if r['Categoria'].startswith('Pranzo') and isinstance(r["Margine in più l'anno FINALE"], (int, float)))

FOTO = '<div class="foto"><span>FOTO</span></div>'
# foto vere (ritoccate con ChatGPT, prompt in bar/prompt_foto_pranzo.md): se il file c'è in img/foto/ entra da solo
FOTO_FILE = {'Spaghettone quadrato burro e bottarga': 'spaghettone_bottarga', 'Gran piatto di crudo e bufala': 'crudo_bufala',
             'Zuppetta di gamberetti': 'zuppetta_gamberetti', 'Millefoglie': 'millefoglie',
             'Insalata Caesar': 'insalata_caesar'}  # 07/10 Caesar (ChatGPT, su bianco: la pagina è bianca)
def foto_di(nome):
    base = FOTO_FILE.get(nome)
    for ext in ('webp', 'png', 'jpg'):
        f = os.path.join(HERE, 'img', 'foto', f'{base}.{ext}') if base else ''
        if f and os.path.exists(f):
            mime = 'jpeg' if ext == 'jpg' else ext
            return f'<div class="foto vera"><img src="data:image/{mime};base64,' + base64.b64encode(open(f, 'rb').read()).decode() + '" alt=""></div>'
    return FOTO

# ---- 06/10 sera (Marco): carta più ingegnerizzata e meno formale ----
# etichette di menu engineering: il n.1 per margine di ogni sezione sta in un riquadro con la sua etichetta;
# «il più amato» sul più venduto (modello di scelta: unità al giorno; dolci: pezzi l'anno del foglio) se è un altro piatto
ETICHETTA_N1 = {'Spaghettone quadrato burro e bottarga': 'la scelta dello chef', 'Zuppetta di gamberetti': 'la scelta dello chef', 'Insalata Caesar': 'da provare',
                'Gran piatto di crudo e bufala': 'da provare', 'Millefoglie': 'da provare'}
def segna_amato(lst, vendite):
    """vendite: nome → pezzi; mette «il più amato» sul più venduto se non è già il n.1 per margine"""
    top = max(lst, key=lambda p: vendite.get(p['nome'], 0))
    if top.get('ev') != 'asta' and vendite.get(top['nome'], 0) > 0:
        top['amato'] = True
    return top['nome']

# illustrazioni a tratto (stesso marrone della carta): stanno nel riquadro del n.1 finché non arriva la foto vera
_S = 'fill="none" stroke="#4A2617" stroke-width="1.1" stroke-linecap="round" stroke-linejoin="round"'
ILLU = {
 'Spaghettone quadrato burro e bottarga': f"""<svg viewBox="0 0 120 84"><ellipse cx="58" cy="50" rx="50" ry="27" {_S}/><ellipse cx="58" cy="48" rx="34" ry="17" {_S} opacity=".45"/>
  <path d="M38 47c4-9 30-11 38-2 6 7-6 14-20 13s-24-6-18-13 24-8 30-2-2 10-12 10-15-4-11-8 14-4 16 0" {_S}/>
  <path d="M42 50c2 5 14 8 24 6M46 43c6-4 18-4 24 0" {_S} opacity=".6"/>
  <g fill="#C9772B"><circle cx="50" cy="44" r="1"/><circle cx="58" cy="41" r=".9"/><circle cx="64" cy="47" r="1"/><circle cx="54" cy="50" r=".9"/><circle cx="61" cy="52" r=".8"/></g>
  <path d="M66 40c2-1 4-1 5 1M47 52c1 1 3 1 4 0" fill="none" stroke="#D9B13B" stroke-width="1.1" stroke-linecap="round"/>
  <path d="M110 18v42M106 18v10c0 3 2 4 4 4s4-1 4-4V18M110 18v10" {_S}/></svg>""",
 'Gran piatto di crudo e bufala': f"""<svg viewBox="0 0 120 84"><ellipse cx="60" cy="50" rx="52" ry="27" {_S}/><ellipse cx="60" cy="48" rx="38" ry="18" {_S} opacity=".45"/>
  <circle cx="71" cy="45" r="11" fill="#FFFDF9" {_S}/><path d="M65 41c2-2 6-3 9-1" {_S} opacity=".5"/>
  <path d="M30 50c5-6 10 4 15-2s9 4 13-1M28 43c6-5 10 4 16-1s8 3 12-1M34 56c5-4 9 3 14 0s7 2 10 0" fill="none" stroke="#B8545E" stroke-width="1.2" stroke-linecap="round"/>
  <path d="M82 56c4-3 9-3 12 0-4 2-9 2-12 0zM86 35c3-3 7-3 9-1-3 2-6 2-9 1zM52 36c3-2 6-2 8 0-3 2-6 2-8 0z" fill="none" stroke="#6E7F3A" stroke-width="1" stroke-linejoin="round"/></svg>""",
 'Zuppetta di gamberetti': f"""<svg viewBox="0 0 120 84"><path d="M22 40c2 22 18 32 38 32s36-10 38-32" {_S}/><ellipse cx="60" cy="40" rx="38" ry="10" {_S}/>
  <ellipse cx="60" cy="41" rx="31" ry="6.5" fill="#F1D3C4" stroke="none"/>
  <path d="M44 41c0-3 4-4 6-2M58 43c0-3 4-4 6-2M70 39c0-3 4-4 6-2" fill="none" stroke="#C8643F" stroke-width="1.3" stroke-linecap="round"/>
  <path d="M82 16l16 4-6 24-16-4z" fill="#EBD3A8" {_S}/><path d="M92 12l14 6-9 22-14-6z" fill="#F2DDB6" {_S}/>
  <path d="M86 24l6 1.5M88 31l5 1.3M97 20l5 2" {_S} opacity=".5"/><path d="M50 37c2-1 3 0 4-1" fill="none" stroke="#6E7F3A" stroke-width="1"/></svg>""",
 'Millefoglie': f"""<svg viewBox="0 0 120 84"><ellipse cx="60" cy="70" rx="44" ry="8" {_S} opacity=".45"/>
  <path d="M30 60h60v6H30zM30 46h60v6H30zM30 32h60v6H30z" fill="#E7C48C" {_S}/>
  <path d="M30 52h60v8H30zM30 38h60v8H30z" fill="#FBF1D9" {_S}/>
  <path d="M32 55c4 2 8-2 12 0s8-2 12 0 8-2 12 0 8-2 12 0 6-1 8 0M32 41c4 2 8-2 12 0s8-2 12 0 8-2 12 0 8-2 12 0 6-1 8 0" fill="none" stroke="#E3CFA0" stroke-width="1"/>
  <g fill="#FFFFFF" stroke="#C9B48F" stroke-width=".5"><circle cx="38" cy="29" r="1.2"/><circle cx="47" cy="28" r="1"/><circle cx="56" cy="29.5" r="1.2"/><circle cx="66" cy="28" r="1"/><circle cx="75" cy="29" r="1.2"/><circle cx="84" cy="28.4" r="1"/></g></svg>""",
}
# copertina: tavola apparecchiata a tratto
COP_ILLU = f"""<svg viewBox="0 0 220 120" class="c-illu"><ellipse cx="110" cy="66" rx="70" ry="38" {_S}/><ellipse cx="110" cy="64" rx="50" ry="25" {_S} opacity=".45"/>
  <path d="M82 62c6-13 42-16 54-3 9 10-9 20-29 19s-35-9-26-19 35-11 43-3-3 14-17 14-22-6-16-11 20-6 23 0" {_S}/>
  <g fill="#C9772B"><circle cx="98" cy="56" r="1.3"/><circle cx="110" cy="52" r="1.2"/><circle cx="119" cy="60" r="1.3"/><circle cx="104" cy="66" r="1.2"/></g>
  <path d="M110 47c3-6 9-7 12-4" fill="none" stroke="#6E7F3A" stroke-width="1.2" stroke-linecap="round"/>
  <path d="M24 28v74M19 28v14c0 4 2 6 5 6s5-2 5-6V28M24 28v14" {_S}/><path d="M196 28c6 6 6 26 0 32v42" {_S}/>
  <path d="M196 30c-4 6-4 24 0 30" {_S} opacity=".5"/></svg>"""

def foto_o_illu(nome):
    """foto vera se il file c'è (img/foto/), altrimenti l'illustrazione a tratto del piatto (mai una foto di un altro piatto)"""
    f = foto_di(nome)
    if f != FOTO:
        return f.replace('class="foto vera"', 'class="ft"')
    return f'<div class="illu">{ILLU[nome]}</div>' if nome in ILLU else ''

def due_righe(desc):
    """descrizione su due righe (Marco 06/10): a capo dopo una virgola o prima di « e »/« con », il più vicino a metà"""
    n = len(desc)
    tagli = [(k + 2, k + 1) for k in range(n) if desc.startswith(', ', k)]
    tagli += [(k + 1, k) for k in range(n) if desc.startswith(' e ', k) or desc.startswith(' con ', k)]
    tagli = [t for t in tagli if 12 < t[1] < n - 8]
    if not tagli:
        sp = [k for k in range(n) if desc[k] == ' ' and 12 < k < n - 8]
        if not sp: return E(desc), ''
        k = min(sp, key=lambda k: abs(k - n / 2)); return E(desc[:k]), E(desc[k + 1:])
    a, b = min(tagli, key=lambda t: abs(t[1] - n / 2))
    return E(desc[:b]), E(desc[a:].lstrip())

def coda_prezzo(testo, prezzo):
    """l'ultima parola e «| prezzo» non si separano mai; prezzo piccolo, mai bold, colore tenue"""
    testa, _, ult = testo.rpartition(' ')
    return f'{testa} <span class="nb">{ult} <span class="sep">|</span> <span class="pz">{prezzo}</span></span>' if testa else f'<span class="nb">{ult} <span class="sep">|</span> <span class="pz">{prezzo}</span></span>'

def html_p(p):
    """nome sopra; descrizione su due righe con il prezzo in coda alla seconda (mai in colonna, mai da solo).
    n.1 per margine: riquadro + etichetta + foto vera o illustrazione; «il più amato» sul più venduto."""
    uno = p.get('ev') == 'asta'
    cls = 'p' + (' uno bx' if uno else '') + (' amato' if p.get('amato') else '')
    rk = f'<span class="rank">{p["rank"]}°</span>' if p.get('rank') else ''
    et = ''
    if uno and ETICHETTA_N1.get(p['nome']): et = f'<p class="et">{ETICHETTA_N1[p["nome"]]}</p>'
    elif p.get('amato'): et = '<p class="et am">il più amato</p>'
    alg = f'<span class="alg">{p["alg"]}</span>' if p.get('alg') else ''
    riga1 = f'<p class="vn">{rk}{E(p["nome"])}{alg}</p>'
    if p.get('prz'):  # pasta corta: tre condimenti, i prezzi in coda a ogni condimento
        riga2 = f'<p class="vd">{E(p["desc"])}, {p["prz"]}</p>'
    else:
        riga2 = f'<p class="vd">{coda_prezzo(E(p.get("desc") or ""), prz(p["new"]))}</p>'   # una riga sola (Marco 07/10 sera)
    corpo = et + riga1 + riga2 + (f'<span class="mk">{E(p["mk"])}</span>' if p.get('mk') else '')
    if uno:
        return f'<div class="{cls}"><div class="tx">{corpo}</div>{foto_o_illu(p["nome"])}</div>'
    return f'<div class="{cls}">{corpo}</div>'

def lista(lst): return '<div class="piatti">' + ''.join(html_p(p) for p in lst) + '</div>'
def cap(occ, tit): return f'<div class="cap"><h2 class="cat">{tit}</h2></div>'  # niente occhiello sopra (Marco 05/10)
def nota(t): return f'<p class="nota">{t}</p>'
def sotto(t): return f'<p class="sotto">{t}</p>'

# piatti del giorno (Luciano 06/10): li dice il personale a voce → fuori dalla carta, resta una riga discreta
DEL_GIORNO = ('<div class="giorno-bx"><p class="et">oggi in cucina</p><p class="giorno">Ogni giorno prepariamo anche un primo e un secondo del giorno:<br>'
              'chiedeteli al nostro personale.</p></div>')
# contorni dal buffet a formato fisso, tipo pokè (proposta Luciano 06/10, DA CONFERMARE col cliente: non sono nel foglio prezzi)
CONT = (8.0, 10.0, 12.0)
MACEDONIA = dict(nome='Macedonia o frutta di stagione', desc='frutta fresca di stagione, tagliata al momento', new=VERD[2],
                 mk='fuori classifica · prezzo finale del foglio (Macedonia)')

# descrizioni valorizzate (Marco 05/10): ingredienti veri, niente marche, un tono che fa venire fame
DESC = {
    'Penne integrali ai pomodori secchi': 'penne integrali, pomodori secchi, mandorle tostate e pecorino grattugiato al momento',
    'Spaghettone quadrato burro e bottarga': 'trafilato al bronzo, burro, bottarga di muggine e scorza di limone',
    "Tagliatelle all'uovo, zucca e salsiccia": "tagliatelle all'uovo tirate sottili, crema di zucca gialla e salsiccia toscana rosolata",
    'Pici al ragù bianco': 'pici tirati a mano e ragù bianco di carne cotto piano per ore, come si faceva una volta',
    "Gnocchetti all'ortolana": 'gnocchetti di patate morbidi, con le verdure di stagione saltate in padella al momento',
    'Carpaccio di bresaola': 'bresaola tagliata sottile, rucola fresca e scaglie di grana',
    'Gran piatto di crudo e bufala': 'prosciutto crudo, mozzarella di bufala campana dop e rucola',
    'Insalata Caesar': 'lattuga romana, pollo alla griglia, crostini dorati, grana e salsa Caesar',
    'Insalata al tonno': 'insalata mista fresca e croccante, filetto di tonno, pomodorini dolci e olive',
    'Insalata Design': 'lattughe miste croccanti, pomodorini dolci, noci e scaglie di grana padano',
    'Insalata greca': 'insalata mista fresca e croccante, feta a cubetti, pomodorini dolci e olive',
    'Insalata tonno e fagioli': 'il classico toscano: tonno, fagioli, cipolla rossa di Tropea e pomodorini',
    'Carpaccio di salmone': "salmone marinato con un'insalatina di arance e finocchi",
    'Polpo con patate prezzemolate': 'polpo cotto piano finché diventa morbidissimo, con patate lesse al prezzemolo',
    'Zuppetta di gamberetti': 'gamberetti in un brodetto leggero di pomodoro e crostoni di pane',
    'Bocconcini di pollo al curry': 'bocconcini di pollo in un curry dolce e cremoso, verdure saltate e riso basmati',
    'Scaloppine di maiale al vino bianco': 'scaloppine di maiale sfumate al vino bianco, con un contorno a scelta dal buffet',
    'Petto di pollo alla griglia': 'petto di pollo alla griglia con le verdure del nostro buffet',
    'Crostata mora e albicocca': 'frolla al burro del nostro laboratorio, confettura di more e di albicocche',
    'Millefoglie': 'sfoglia croccante a strati e crema chantilly del nostro laboratorio',
    'Crostatina alla frutta': 'frolla al burro, crema pasticcera e frutta fresca di stagione tagliata al momento',
    'Crostata pistacchio e nocciola': 'frolla al burro, una crema al pistacchio e una crema di nocciole',
    'Cannolo siciliano': "cialda croccante riempita di ricotta dolce, con scorza d'arancia candita",
    'Due mignon': 'due mignon a scelta dal banco della nostra pasticceria, perfetti con il caffè',
    'Il classico': 'roast-beef, arista al forno o fesa di tacchino, con un contorno a scelta dal buffet',
    'Bignè': 'bignè ripieni di crema pasticcera o di cioccolato',
}
def valorizza(*liste):
    for lst in liste:
        for p in lst: p['desc'] = DESC.get(p['nome'], p['desc'])

def foto_cop():
    """foto di copertina se un giorno c'è il file (img/foto/copertina_pranzo.*); altrimenti copertina solo tipografica"""
    for ext in ('webp', 'png', 'jpg'):
        f = os.path.join(HERE, 'img', 'foto', f'copertina_pranzo.{ext}')
        if os.path.exists(f):
            mime = 'jpeg' if ext == 'jpg' else ext
            return f'<img class="c-ft" src="data:image/{mime};base64,' + base64.b64encode(open(f, 'rb').read()).decode() + '" alt="">'
    return '<div class="c-filo"></div>'

def facciate():
    P, S, F, D = ordina(PRIMI, foto=True), ordina(SECONDI, foto=True), ordina(FREDDI, foto=True), ordina(DOLCI, foto=True)  # foto sul n.1 di ogni sezione
    valorizza(P, S, F, D)
    # vendite per «il più amato»: unità al giorno del modello di scelta (primi, freddi, secondi), pezzi l'anno del foglio (dolci)
    vend = {p['nome']: p.get('vend') or 0 for p in P + S + F + D}
    vend.update({p['nome']: p['vend_anno'] for p in F if p.get('vend_anno') is not None})  # freddi 07/10: pezzi l'anno di cassa
    AMATI = [segna_amato(l, vend) for l in (P, F, S, D)]
    cerchio = lambda r: (f'<svg width="{2*r+4}" height="{2*r+4}" viewBox="0 0 {2*r+4} {2*r+4}"><circle cx="{r+2}" cy="{r+2}" r="{r}" fill="none" stroke="#4A2617" stroke-width="1.3"/>'
                         f'<circle cx="{r+2}" cy="{r+2}" r="{r*0.6:.1f}" fill="none" stroke="#4A2617" stroke-width=".8" opacity=".5"/></svg>')
    def tre(tit, sotto, opz):
        # prezzo in coda alla misura, sulla stessa riga (Marco 06/10)
        s = f'<p class="fame-sub">{sotto}</p>' if sotto else ''
        return (f'<p class="fame-tit">{tit}</p>{s}<div class="fame-opz">'
                + ''.join(f'<div><span class="ic">{cerchio(r)}</span><span class="fn">{n} <span class="sep">|</span> <span class="pz">{p}</span></span></div>' for r, n, p in opz)
                + '</div>')
    porz = '<div class="fame">' + tre('Che fame hai? · vale per tutti i primi', '',
                                      [(6, 'giusta', 'inclusa'), (9, 'abbondante', '+ 2'), (12, 'extra abbondante', '+ 4')]) + '</div>'
    contorni = '<div class="fame contorni">' + tre('Scegli il tuo contorno', 'le verdure di stagione del nostro buffet, nel piatto che vuoi',
                                                   [(6, 'piccolo', prz(CONT[0])), (9, 'medio', prz(CONT[1])), (12, 'grande', prz(CONT[2]))]) + '</div>'
    # copertina della stessa famiglia del «Menu del bar a libro» (build_libro_bar.py): scritta Cartabianca in Cormorant, niente «il PRANZO» (Marco 06/10)
    # copertina meno formale (Marco 06/10 sera): calda, invitante, famiglia Eataly del menu del bar a libro
    # copertina classica (Marco 06/10 notte): stessa impostazione del «Menu del bar a libro», niente disegni né foto, «il pranzo» discreto
    cop = ('<div class="cop4"><h1 class="c4-tit">Cartabianca</h1><p class="c4-cafe">cafè</p>'
           '<div class="c4-filo"></div><p class="c4-pranzo">il pranzo</p>'
           '<p class="c4-sotto">la pasta · le insalate · i secondi · i dolci</p></div>')
    f2 = (cap('Primi', 'la pasta') + lista(P + [PASTA_CORTA]) + porz
          + cap('Freschi', 'insalate e freddi') + lista(F)
          + nota(f"<b>Fissi d'autunno: +{intero(GUAD_MIX)} €/anno</b> (modello di scelta, valore basso). In ogni sezione il n.1 per margine sta al secondo posto "
                 f"in un riquadro con etichetta e illustrazione (foto quando arriva): {E(P[1]['nome'])} e {E(F[1]['nome'])}. «Il più amato» sul più venduto: {E(AMATI[0])}, {E(AMATI[1])}. Tolto il carpaccio di tonno (food cost 39%). "
                 f"<b>Porzioni: +{intero(L_ABB + L_EXT)} €/anno</b> (abbondante +2 su 8 primi su 100: +1,47 € di margine; extra +4 su 3 su 100: +2,94 €). "
                 'Primo del giorno tolto dalla carta: lo dice il personale a voce (Luciano 06/10). Prezzo in coda alla descrizione, piccolo e tenue (Marco 06/10). Porzioni abbondante/extra: in cassa non ci sono ancora, vanno create come varianti (+2 / +4).'))
    f3 = (cap('Secondi', 'i secondi') + lista(S) + contorni + DEL_GIORNO
          + nota(f'<b>Secondi in evidenza</b> (Luciano 06/10): pagina di destra, dove cade l\'occhio a libro aperto, corpo più grande. '
                 f'<b>{E(S[1]["nome"])}</b>: margine più alto del pranzo ({eur(S[1]["m"])} €), la sceglie poca gente: riquadro «la scelta dello chef» al 2° posto; «il più amato» su {E(AMATI[2])}. '
                 f'<b>Contorni a formato fisso {prz(CONT[0])} / {prz(CONT[1])} / {prz(CONT[2])}</b>: proposta di Luciano, NON nel foglio prezzi, da confermare con Cartabianca '
                 f'(foglio: verdure piccolo {prz(VERD[0])} e grande {prz(VERD[1])}; in cassa oggi 5 e 9, il MEDIO non esiste: va creato). Secondo del giorno fuori carta, a voce. '
                 'Verifica cassa 07/10: tutti i piatti di questa carta esistono in Cassa in Cloud (categoria PRANZO.); petto di pollo, Caesar e carpaccio di salmone '
                 'in cassa sono a 13: in carta il PREZZO FINALE del foglio, da allineare in cassa con il sì di Massimo.'))
    f4 = (cap('Prima di tornare al lavoro', 'per finire') + lista(D + [MACEDONIA])
          + '<div class="fascia"><p class="fame-tit">Col caffè</p>'
          + '<p class="opz">' + ''.join(f'<span>{n} <span class="sep">|</span> <span class="pz">{v}</span></span>' for n, v in
                                       (('Caffè e un mignon', '2,5'), ('Un amaro', prz(AMARO)), ('Limoncello', '4'), ('Grappa', '4,5'))) + '</p></div>'
          + nota(f'<b>Dolci: +{intero(L_DOL)} €/anno</b> (margine sul food cost ingredienti del file 02 Bar: {E(D[1]["nome"])} n.1). Macedonia spostata qui dai contorni, in fondo e fuori classifica. '
                 f'<b>Amaro: +{intero(L_AMA)} €/anno</b>. Caffè e mignon 2,50 = prezzi pieni di cassa (caffè 1,30 + mignon 1,20, 07/10).')
          + ('<div class="chiudi"><p class="legenda"><b>Allergeni:</b> 1 Glutine · 2 Crostacei · 3 Uova · 4 Pesce · 5 Arachidi · 6 Soia · 7 Latte · 8 Frutta a guscio · 9 Sedano · 10 Senape · 11 Sesamo · 12 Anidride solforosa · 13 Lupini · 14 Molluschi. '
             'Alcuni prodotti sono sottoposti in loco ad abbattimento come descritto nelle procedure HACCP ai sensi del reg. CE 852/04.</p>'
             f'<img class="logo-retro" src="{LOGO}" alt="Cartabianca Cafè"></div>')
          + nota('Allergeni stimati dalle ricette: da far confermare alla cucina prima della stampa.'))
    sp = lambda et, *pp: (f'<div class="spread"><p class="etichetta">{et}</p><div class="doppia">' + ''.join(pp) + '</div></div>')
    return (sp('Copertina', f'<section class="pag copertina">{cop}</section>')
            + sp('Interno · A4', f'<section class="pag">{f2}<div class="num">— 2 —</div></section>', f'<section class="pag secondi">{f3}<div class="num">— 3 —</div></section>')
            + sp('Copertina dietro', f'<section class="pag retro">{f4}</section>'))

EXTRA = """
/* stile sito Cartabianca — regole RBR: NOME | prezzo, un solo segno (asticella rossa), una foto per pagina, fascia crema */
:root{--carta:#FFFDF8;--panna:#F5EFE0;--marrone:#4A2617;--rosso:#A6192E;--inchiostro:#4A2617;--soft:#7A6A5E;--linea:#E3D9C6;
  --display:'Lora',Georgia,serif;--wide:'DM Sans','Helvetica Neue',Arial,sans-serif;--body:'DM Sans','Helvetica Neue',Arial,sans-serif}
body{color:#1E1A17}
.pag{background:var(--carta);padding:16mm 16mm 14mm}
.pag::before,.pag::after{content:none !important;display:none}
.testa{text-align:center;margin-bottom:8mm}
.testa .logo{height:12mm;width:auto;margin:0 auto 3mm;display:block}
.testa .tit{margin:0 0 1.5mm;font-family:var(--wide);font-weight:700;font-size:32pt;color:var(--marrone);letter-spacing:.01em}
.testa .tit em{font-family:var(--display);font-style:italic;font-weight:400;color:#1E1A17;font-size:.8em}
.cap{text-align:center;margin:0 0 4mm}
.cols>div>.cap~.cap{margin-top:9mm}
h2.cat{font-family:var(--display);font-style:italic;font-weight:400;font-size:28pt;color:var(--marrone);margin:.5mm 0 0;line-height:1.1}
.occhiello{font-family:var(--wide);color:var(--rosso);font-weight:700;letter-spacing:.2em;text-transform:uppercase;font-size:7.4pt;margin:0}

.piatti{display:block}
.piatti+.piatti{margin-top:5mm;padding-top:4mm;border-top:.5pt solid var(--linea)}
.p{margin:0 0 4.6mm;padding-left:3.6mm;border-left:2pt solid transparent}
.p.asta{border-left-color:var(--rosso)}
.vr{margin:0;font-family:var(--wide);font-size:11.4pt;line-height:1.3;text-transform:uppercase;letter-spacing:.03em;color:var(--marrone)}
.vn{font-weight:600}
.pz{white-space:nowrap}
.nobr{white-space:nowrap}
h2.cat{font-style:italic !important}
.sbar{color:var(--soft);font-weight:400;margin:0 .6mm}

.prezzo{font-weight:600;white-space:nowrap;font-variant-numeric:tabular-nums}
.alg{font-family:var(--display);font-style:italic;text-transform:none;font-size:7pt;color:var(--soft);margin-left:1.6mm;letter-spacing:0}
.vd{display:block;margin:.8mm 0 0;font-family:var(--display);font-style:italic;font-size:10.4pt;line-height:1.4;color:var(--soft)}
.p.pfoto{display:grid;grid-template-columns:1fr 24mm;gap:4mm;align-items:start}
.foto{aspect-ratio:1;border:.6pt dashed #D9CDBD;border-radius:1.5mm;display:grid;place-items:end center;padding-bottom:1.2mm}
.foto span{font-family:var(--wide);font-size:5pt;letter-spacing:.2em;color:var(--soft)}
.fascia{background:var(--panna);padding:3.4mm 4mm;text-align:center;margin:0 0 6mm}
.fascia .opz{margin:1.8mm 0 0;display:flex;flex-wrap:wrap;justify-content:center;gap:1.4mm 7mm;font-family:var(--wide);font-size:9pt;text-transform:uppercase;letter-spacing:.03em;color:var(--marrone)}
.fascia .opz b{font-weight:600;margin-left:1mm}
.pag>.fascia{margin-top:auto}
.chiudi{margin-top:auto;padding-top:3mm;border-top:.7pt solid var(--linea)}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:12mm;align-items:start}
/* categorie in orizzontale (Marco 05/10): ogni categoria tutta larghezza, piatti su 2 colonne */
.piatti.c2{column-count:2;column-gap:12mm;margin-bottom:9mm}
.piatti.c2>.p{break-inside:avoid;display:inline-block;width:100%}
.pag>.cap{margin:0 0 6mm}
.pag>.fascia{margin:0 0 9mm}
/* copertina */
.pag.copertina{background:var(--panna)}
.cop{position:absolute;top:0;left:0;right:0;bottom:0;padding:30mm 20mm;text-align:center}
.logo-cop{display:block;height:20mm;width:auto;margin:0 auto}
.cop-centro{position:absolute;left:0;right:0;top:112mm}
.cop-tit{margin:4mm 0;font-family:var(--wide);font-weight:700;font-size:64pt;color:var(--marrone);line-height:1}
.cop-tit em{font-family:var(--display);font-style:italic;font-weight:400;color:#1E1A17;font-size:.7em}
.cop-sotto{font-family:var(--display);font-style:italic;font-size:15pt;color:var(--soft);margin:0}
.cop-piede{position:absolute;left:0;right:0;bottom:26mm;font-family:var(--wide);font-size:8pt;letter-spacing:.3em;text-transform:uppercase;color:var(--marrone);margin:0}
.pag.retro .chiudi{position:absolute;left:16mm;right:16mm;bottom:14mm;text-align:center}
.logo-retro{display:block;height:9mm;width:auto;margin:5mm auto 0}
.doppia .pag{position:relative}
/* ===== una colonna (Marco 05/10) con lo stile di sempre: DM Sans maiuscolo + Lora corsivo, marrone su crema, asticella rossa sul n.1 ===== */
.pag:not(.copertina){padding:16mm 20mm 14mm}
.cap{text-align:center;margin:0 0 5mm}
h2.cat{font-family:var(--display) !important;font-style:italic !important;font-weight:400 !important;font-size:26pt !important;color:var(--marrone) !important;margin:.5mm 0 0}
.cap .occhiello{font-family:var(--wide);color:var(--rosso);font-weight:700;letter-spacing:.2em;text-transform:uppercase;font-size:7.4pt;margin:0}
.piatti{display:block}
.piatti .p{margin:0 0 5mm;padding-left:3.6mm;border-left:2pt solid transparent}
.p.uno{border-left-color:var(--rosso) !important}
.p.uno.pfoto{border-left-color:transparent !important;padding-left:0 !important;border-left-width:0 !important}
.p.uno.pfoto>div:first-child{border-left:2pt solid var(--rosso);padding-left:3.6mm}
.vn{margin:0;font-family:var(--wide);font-weight:600;font-size:10.8pt;color:var(--marrone);text-transform:uppercase;letter-spacing:.03em;line-height:1.3}
.vd{display:block;margin:.6mm 0 0;font-family:var(--display);font-style:italic;font-size:10.2pt;line-height:1.45;color:var(--soft)}
.vd.in{display:inline;margin:0}
.pz{font-family:var(--display);font-style:italic;font-weight:400;color:var(--soft)}
.sbar{margin:0 .8mm 0 .4mm;color:var(--linea);font-style:normal;font-weight:400}
.alg{font-family:var(--display);font-style:italic;text-transform:none;font-weight:400;font-size:7pt;color:var(--soft);margin-left:1.6mm;letter-spacing:0}
.p.pfoto{display:grid;grid-template-columns:1fr 34mm;gap:6mm;align-items:center}
.foto.vera{border:0 !important;background:none !important;padding:0}
.foto.vera img{width:100%;height:100%;object-fit:contain}
.fame{background:var(--panna);text-align:center;margin:2mm 0 7mm;padding:3.5mm 4mm}
.fame-tit{margin:0 0 2mm;font-family:var(--wide);font-weight:700;letter-spacing:.2em;text-transform:uppercase;font-size:7.4pt;color:var(--rosso)}
.fame-opz{display:flex;justify-content:space-around;align-items:flex-end}
.fame-opz>div{display:flex;flex-direction:column;align-items:center;gap:.6mm}
.fame .fn{font-family:var(--wide);font-weight:600;text-transform:uppercase;letter-spacing:.03em;font-size:9pt;color:var(--marrone)}
.fame .fp{font-family:var(--wide);font-size:9pt;color:var(--marrone)}
.pag>.cap~.cap{margin-top:7mm}
.fascia .occhiello{font-family:var(--wide);color:var(--rosso);font-weight:700;letter-spacing:.2em;text-transform:uppercase;font-size:7.4pt}
.fascia .opz{font-family:var(--wide);text-transform:uppercase;letter-spacing:.03em;font-size:9pt;color:var(--marrone)}
.pag>.fascia.contorni{margin:7mm 0 0}

/* ===== 06/10 (call Marco + Luciano) ===== */
/* cornice sottile come il menu del bar a libro, stessa famiglia */
.pag{background:#FFFDF9}
.pag::before{content:"" !important;display:block !important;position:absolute;top:6mm;left:6mm;right:6mm;bottom:6mm;border:.5pt solid #E7DCCB;pointer-events:none}
/* copertina: Cormorant come build_libro_bar.py, niente «il PRANZO» */
.pag.copertina{background:#FFFDF9}
.cop2{position:absolute;top:0;left:0;right:0;bottom:0;text-align:center;padding:0 20mm}
.c-occ{margin:96mm 0 0;font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-weight:500;font-size:19pt;color:#4A2617}
.c-tit{margin:2mm 0 0;font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:52pt;letter-spacing:.12em;text-transform:uppercase;color:#4A2617;line-height:1}
.c-cafe{margin:2mm 0 0;font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-size:17pt;color:#8A5A2B}
.c-filo{width:18mm;height:0;border-top:1pt solid #A6192E;margin:14mm auto 0}
.c-ft{display:block;width:118mm;height:auto;margin:16mm auto 0}
.c-sotto{position:absolute;left:0;right:0;bottom:30mm;margin:0;font-family:'Cormorant Garamond',Georgia,serif;font-size:11.5pt;letter-spacing:.26em;text-transform:uppercase;color:#8A5A2B}
/* prezzo su una riga sua sotto il piatto, discreto */
.vp{margin:.5mm 0 0;font-family:var(--wide);font-size:9.6pt;font-weight:500;letter-spacing:.04em;color:var(--soft);font-variant-numeric:tabular-nums}
/* fasce a tre misure (porzioni e contorni) */
.fame-sub{margin:-1mm 0 2.4mm;font-family:var(--display);font-style:italic;font-size:9.6pt;color:var(--soft)}
.fame.contorni{margin:5mm 0 0}
/* piatti del giorno: una riga discreta */
.giorno{margin:6mm 0 0;text-align:center;font-family:var(--display);font-style:italic;font-size:10.2pt;color:var(--soft)}
/* secondi in evidenza: pagina di destra, corpo più grande, più aria */
.pag.secondi{padding-top:24mm !important}
.secondi h2.cat{font-size:32pt !important}
.secondi .cap{margin-bottom:7mm !important}
.secondi .piatti .p{margin-bottom:8.5mm !important}
.secondi .vn{font-size:13.4pt !important}
.secondi .vd{font-size:11.6pt !important}
.secondi .vp{font-size:11pt}
.secondi .alg{font-size:8pt}

/* ===== 06/10 sera (Marco): prezzo in coda alla descrizione, discreto; riquadri ed etichette; copertina calda ===== */
.vp{display:none}
.nb{white-space:nowrap}
.vd .sep,.fame .sep,.fascia .sep{color:#D6C8B4;font-style:normal;font-weight:400;margin:0 .5mm}
.pz{font-family:var(--wide) !important;font-style:normal !important;font-weight:400 !important;font-size:8.2pt !important;letter-spacing:.02em;color:#9C8C7E !important;font-variant-numeric:normal}
.secondi .pz{font-size:9pt !important}
.p.uno{border-left-color:transparent !important}
.p.bx{display:flex;align-items:center;gap:5mm;border:1pt dotted #A6192E !important;padding:3mm 4mm 3mm 4.4mm !important;margin-left:-4.4mm;margin-right:-4mm}
.p.bx .tx{flex:1 1 auto;min-width:0}
.illu,.ft{flex:0 0 34mm;width:34mm;height:24mm}
.illu svg{display:block;width:100%;height:100%}
.ft img{display:block;width:100%;height:100%;object-fit:contain}
.et{margin:0 0 .8mm;font-family:var(--wide);font-weight:700;font-size:6.6pt;letter-spacing:.2em;text-transform:uppercase;color:#A6192E}
.et.am{color:#8A5A2B}
.fame .fn{white-space:nowrap}
.fame .fn .pz{text-transform:none}
.fascia .opz .pz{font-size:8pt !important}
.giorno-bx{margin:7mm auto 0;padding:3.2mm 5mm;border:1pt dotted #A6192E;text-align:center;max-width:132mm}
.giorno-bx .giorno{margin:0}
/* copertina meno formale */
.pag.copertina{background:#F6EFE3 !important}
.pag.copertina::before{border-color:#E2D3BC !important}
.cop3{position:absolute;top:0;left:0;right:0;bottom:0;text-align:center;padding:0 22mm}
.c-marca{margin:34mm 0 0;font-family:'Cormorant Garamond',Georgia,serif;font-weight:600;font-size:12pt;letter-spacing:.32em;text-transform:uppercase;color:#8A5A2B}
.c-marca i{text-transform:none;letter-spacing:.02em;font-weight:500}
.c-big{margin:9mm 0 0;font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:66pt;line-height:.92;color:#4A2617}
.c-big i{font-size:.82em;color:#8A5A2B}
.c-invito{margin:7mm 0 0;font-family:'Lora',Georgia,serif;font-style:italic;font-size:13pt;line-height:1.5;color:#6E5A4A}
.c-illu{display:block;width:128mm;height:auto;margin:12mm auto 0}
.cop3 .c-ft{display:block;width:128mm;height:auto;margin:12mm auto 0}
.c-oggi{position:absolute;left:44mm;right:44mm;bottom:26mm;border:1pt dotted #A6192E;padding:3mm 4mm}
.c-oggi-t{margin:0;font-family:var(--wide);font-weight:700;font-size:7pt;letter-spacing:.22em;text-transform:uppercase;color:#A6192E}
.c-oggi-d{margin:1mm 0 0;font-family:'Lora',Georgia,serif;font-style:italic;font-size:11pt;color:#4A2617}
/* copertina classica (Marco 06/10 notte): famiglia del menu del bar a libro, niente disegni */
.pag.copertina{background:#FFFDF9 !important}
.pag.copertina::before{border-color:#E7DCCB !important}
.cop4{position:absolute;top:0;left:0;right:0;bottom:0;text-align:center;padding:0 20mm}
.c4-tit{margin:112mm 0 0;font-family:'Cormorant Garamond',Georgia,serif;font-weight:500;font-size:52pt;letter-spacing:.12em;text-transform:uppercase;color:#4A2617;line-height:1}
.c4-cafe{margin:2mm 0 0;font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-size:17pt;color:#8A5A2B}
.c4-filo{width:16mm;height:0;border-top:.8pt solid #A6192E;margin:13mm auto 0}
.c4-pranzo{margin:9mm 0 0;font-family:'Cormorant Garamond',Georgia,serif;font-style:italic;font-weight:500;font-size:21pt;color:#4A2617}
.c4-sotto{position:absolute;left:0;right:0;bottom:30mm;margin:0;font-family:'Cormorant Garamond',Georgia,serif;font-size:11.5pt;letter-spacing:.26em;text-transform:uppercase;color:#8A5A2B}
"""

def pagina():
    css = open(os.path.join(HERE, 'stile_pranzo.css'), encoding='utf-8').read() + EXTRA  # copia ferma del CSS base: lo stile.css delle carte ristoranti cambia
    sym = open(os.path.join(UP, 'simboli.svg'), encoding='utf-8').read()
    righe = ''.join(f'<tr><td>{E(a)}</td><td class="dove">{b}</td><td class="n">+{intero(c)} €</td></tr>' for a, b, c in LEVE)
    riep = f'''<div class="riepilogo"><p class="etichetta">Vist
a consulente · potenziale della carta</p>
      <div class="rbox"><h3>Pranzo dei 7 bar: <b>+{intero(TOT)} €/anno</b> di margine</h3><table>{righe}</table>
      <p class="rnote">Modello di scelta (venduto giornaliero Cassa in Cloud × menu del sito × meteo, due autunni) · food cost dalle distinte del file 02 ·
      prezzi = colonna PREZZO FINALE del tab «Prezzi BAR» (foglio «Prezzi definitivi»); i prezzi finali del pranzo (+{intero(PRZ_PRANZO)} €/anno) sono contati a parte, nei prezzi del bar ·
      volumi: ~{intero(PRIMI_ANNO)} primi, ~{intero(FREDDI_ANNO)} piatti freddi e ~{intero(PRANZI_ANNO)} pranzi l'anno.</p></div></div>'''
    return f'''<title>Carta Cartabianca Pranzo Bar</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=Lora:ital,wght@0,400;0,600;1,400&family=DM+Sans:wght@400;500;600;700&display=swap">
<style>{css}</style>
{sym}
<div class="bar">
  <div class="id"><b>CARTABIANCA</b><span>Pranzo dei 7 bar · libro A4, 4 facciate · proposta RBR</span></div>
  <div class="toggle" role="group" aria-label="Vista">
    <button id="bCli" aria-pressed="true">Vista cliente</button>
    <button id="bCon" aria-pressed="false">Vista consulente</button>
  </div>
  <p class="hint" id="hint">Il menu come lo vede chi si siede al tavolo.</p>
</div>
<div class="piano">
{riep}
{facciate()}
</div>
<script>
(function(){{
  var b=document.body,cli=document.getElementById('bCli'),con=document.getElementById('bCon'),hint=document.getElementById('hint');
  function set(rbr){{
    b.classList.toggle('rbr',rbr);
    cli.setAttribute('aria-pressed',String(!rbr));con.setAttribute('aria-pressed',String(rbr));
    hint.textContent=rbr?'Margini sui prezzi finali, unità al giorno dal modello d\\'autunno. Il numero nel cerchietto è il posto per margine nella sezione.':'Il menu come lo vede chi si siede al tavolo.';
  }}
  cli.addEventListener('click',function(){{set(false)}});con.addEventListener('click',function(){{set(true)}});
}})();
</script>'''

if __name__ == '__main__':
    open(os.path.join(HERE, 'carta_pranzo_bar_v9.html'), 'w', encoding='utf-8').write(pagina())
    json.dump(dict(tot=TOT, leve=[dict(leva=a, dove=b, euro=round(c)) for a, b, c in LEVE]),
              open(os.path.join(HERE, 'leve_pranzo_v9.json'), 'w'), ensure_ascii=False, indent=1)
    print('TOT', round(TOT)); [print(f'  {round(c):>7}  {a}') for a, b, c in LEVE]

