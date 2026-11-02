# -*- coding: utf-8 -*-
"""Genera carta_tennis.html e carta_club.html (libro A4, 10 facciate, doppia vista).
Uso: python3 build.py   → scrive i due HTML + riepilogo_leve.json
"""
import json, os, html
from dati import TENNIS, CLUB, FOTO_VERE

HERE = os.path.dirname(os.path.abspath(__file__))
KS = json.load(open(os.path.join(HERE, 'ks3.json')))
CARDS = json.load(open(os.path.join(HERE, 'cards.json')))
LIVE = json.load(open(os.path.join(HERE, 'prezzi_live.json')))['Prezzi RISTORANTI']   # python3 prezzi_live.py
E = html.escape
IVA = 1.1


# ---------------------------------------------------------------- lookup
def num(s):
    if isinstance(s, (int, float)):
        return float(s)
    s = (s or '').replace('€', '').replace(' ', '').strip()
    if not s or s.upper() == 'NO':
        return None
    try:
        return float(s.replace('.', '').replace(',', '.'))
    except ValueError:
        return None


def deciso(v):
    """numero, 'NO' o None (non deciso)."""
    if isinstance(v, str) and v.strip().upper() == 'NO':
        return 'NO'
    return num(v)


SHEET = {}   # (cat, prod) -> (oggi, prezzo FINALE o 'NO' o None, chi)
for r in LIVE:
    SHEET[(str(r['Categoria']).strip().lower(), str(r['Prodotto']).strip().lower())] = (
        num(r["Prezzo oggi"]), deciso(r['PREZZO FINALE']), 'foglio definitivo')
COPERTO = {str(r['Categoria']).split()[-1].upper(): num(r['PREZZO FINALE']) for r in LIVE if r['Prodotto'] == 'Coperto'}


def ks(cat, prod):
    for p in KS.get('R|' + cat, []):
        if p['prod'] == prod or p['prod'].startswith(prod):
            return p
    raise KeyError(f'ks3 non trovato: {cat} | {prod}')


def card(name, sigla):
    pref = 'TENNIS ·' if sigla == 'TENNIS' else 'CARTABIANCA ·'
    hits = [(k, v) for k, v in CARDS.items() if k.split('|', 1)[1] == name]
    hits.sort(key=lambda kv: not kv[0].startswith(pref))
    if not hits:
        raise KeyError(f'ricetta non trovata: {name}')
    return hits[0][1]


def r05(x):
    return round(x * 2) / 2


def nuovo_prezzo(p):
    if 'nuovo_prezzo' in p:
        return p['nuovo_prezzo'], 'proposta RBR'
    if not p['sheet']:
        return p['old'], None
    ks_ = [k for k in SHEET if k[0].startswith(p['sheet'][0].lower()) and k[1] == p['sheet'][1].lower()]
    if not ks_:
        raise KeyError(f'foglio prezzi: {p["sheet"]}')
    oggi, dec, chi = SHEET[ks_[0]]
    old = p['old']
    if dec is None:
        return old, 'prezzo non ancora deciso sul foglio'
    if dec == 'NO':
        return old, f'{chi} ha detto NO'
    if oggi and oggi < 0.7 * old:            # in cassa è un'altra unità (mezza porzione ecc.)
        return r05(old + max(0, dec - oggi)), f'in cassa {eur(oggi)}, deciso {eur(dec)} ({chi}): applico solo l\'aumento'
    if oggi and old < oggi:                   # carta stampata più bassa della cassa
        return dec, f'in carta {eur(old)} ma in cassa già {eur(oggi)}: stampo il prezzo deciso da {chi}'
    return dec, None


def eur(x, zero=True):
    s = f'{x:,.2f}'.replace(',', 'X').replace('.', ',').replace('X', '.')
    return s[:-3] if (s.endswith(',00') and not zero) else s


def prz(x):
    s = eur(x, zero=False)
    return s[:-1] if (',' in s and s.endswith('0')) else s


def attacca_prezzo(desc, prezzo, dopo=''):
    """ultima parola + «| prezzo» non si separano mai (niente prezzo da solo a capo). dopo = html da attaccare all'ultima parola (asterisco)."""
    testa, _, coda = desc.rpartition(' ')
    coda += dopo
    desc += dopo
    pr = f'<span class="prezzo">{prezzo}</span>'  # 06/10: prezzo discreto anche qui (più piccolo, mai bold)
    return f'{testa} <span style="white-space:nowrap;display:inline">{coda} | {pr}</span>' if testa else f'{desc} | {pr}'


def intero(x):
    return f'{x:,.0f}'.replace(',', '.')


# ---------------------------------------------------------------- calcolo piatto
def calcola(p, sigla):
    p = dict(p)
    if p.get('sale'):
        s = ks(*p['sale'])
        p['q6'] = p.get('q6', s['q'])
        p['cls'] = p.get('cls', s['k'])
        p['fc'] = p.get('fc_fisso', s['fc'])
    if p.get('card') and (p.get('fc_da') == 'card' or 'fc' not in p):
        p['fc'] = card(p['card'], sigla)
    if 'fc' not in p:
        raise KeyError(f'nessun food cost: {p["nome"]}')
    p['new'], p['nota_prezzo'] = nuovo_prezzo(p)
    p['m_old'] = p['old'] / IVA - p['fc']
    p['m_new'] = p['new'] / IVA - p['fc']
    p['fcp'] = p['fc'] / (p['new'] / IVA)
    p['qa'] = 2 * p['q6'] if p.get('q6') else 0
    p['cls'] = p.get('cls', 'NUOVO')
    p['leva_prezzo'] = round((p['new'] - p['old']) / IVA * p['qa'] * 0.98) if p['qa'] else 0
    return p


def ordina(items):
    """n.1 per margine in SECONDA posizione, poi a scendere."""
    s = sorted(items, key=lambda p: -p['m_new'])
    for i, p in enumerate(s, 1):
        p['rank'] = i
    if len(s) >= 5:   # presentazione «5 step»: si ricordano l'inizio e la fine della lista → il n.3 va in fondo
        return [s[1], s[0]] + s[3:] + [s[2]]
    return [s[1], s[0]] + s[2:] if len(s) > 1 else s


def evidenzia(items, primo='asta'):
    if not items:
        return
    # regola Marco 03/10: si evidenzia solo il n.1 (in seconda posizione), sempre con lo stesso segno
    r1 = [p for p in items if p['rank'] == 1][0]
    r1['ev'] = 'asta'


# ---------------------------------------------------------------- html piatto
CLS_IT = {'STAR': 'STAR · da proteggere', 'PLOWHORSE': 'PLOWHORSE · da riprezzare',
          'PUZZLE': 'PUZZLE · da spingere', 'DOG': 'DOG', 'NUOVO': 'nuovo da settembre'}
# 08/10 Marco: calici tutti viola, boccali tutti gialli
VIOLA, GIALLO = '#6E2A6B', '#E3AE32'
W = dict.fromkeys(['bianco', 'bollicine', 'rosato', 'rosso'], VIOLA)
BE = dict.fromkeys(['bianca', 'chiara', 'ambrata', 'scura'], GIALLO)


def abb_html(a, inline=False):
    if not a:
        return ''
    t, tipo, c, n = a
    if inline:
        return abb_html(a).replace('class="vin"', 'class="vin in"').replace('class="birra"', 'class="birra in"')
    if t == 'v':
        return (f'<span class="vin"><svg width="11" height="16" style="--w:{W[tipo]}"><use href="#calice"/></svg>'
                f'<span><b>{E(c)}</b> {E(n)}</span></span>')
    return (f'<span class="birra"><svg width="15" height="16" style="--w:{BE[tipo]}"><use href="#boccale"/></svg>'
            f'<span><b>{E(n)}</b> · {tipo}</span></span>')


def mk_text(p):
    per = ''
    if p.get('per2'):
        per = ' · prezzo al kg, di solito 1,1-1,2 kg per 2'
    if p.get('proposta'):
        t = f'PROPOSTA RBR premium · margine {eur(p["m_new"])} € · FC {p["fcp"]*100:.1f}% · food cost: {p["conto"]} · da validare con la cucina'
    elif p['cls'] == 'NUOVO':
        t = f'nuovo da settembre · margine {eur(p["m_new"])} € · FC {p["fcp"]*100:.1f}%'
    else:
        mm = (f'margine {eur(p["m_old"])} → {eur(p["m_new"])} € a {prz(p["new"])}'
              if p['new'] != p['old'] else f'margine {eur(p["m_new"])} €')
        t = f'{mm} · FC {p["fcp"]*100:.1f}% · {intero(p["qa"])} pz/anno · {CLS_IT[p["cls"]]}'
    if p.get('era'):
        t += f' · in cassa era «{p["era"]}»'
    if p.get('nota_prezzo'):
        t += f' · {p["nota_prezzo"]}'
    if p.get('flag'):
        t += f' · {p["flag"]}'
    return t + per


FOTO = ('<div class="foto"><svg viewBox="0 0 120 70" class="ph"><ellipse cx="60" cy="38" rx="54" ry="24" fill="#fff" stroke="#E2D8CF" stroke-width=".8"/>'
        '<ellipse cx="60" cy="37" rx="36" ry="15" fill="#F7F2EC" stroke="#EDE4DA" stroke-width=".6"/>'
        '<text x="60" y="40" text-anchor="middle" font-size="6" letter-spacing="1.4" fill="#B9A99B">FOTO</text></svg></div>')


def foto_html(nome):
    """foto vera se c'è (FOTO_VERE), altrimenti il segnaposto."""
    f = FOTO_VERE.get(nome)
    return f'<div class="foto vera"><img src="{img64(f)}" alt=""></div>' if f else FOTO


def abb2_html(a):
    """pizze: un vino e una birra, piccoli, sotto la descrizione."""
    if not a:
        return ''
    (cant, vino), (tipo, birra) = a
    return (f'<span class="abb2"><svg width="9" height="13" style="--w:#6E2A6B"><use href="#calice"/></svg> {E(cant)} {E(vino)}'
            f'<span class="sep2">·</span><svg width="12" height="13" style="--w:#E3AE32"><use href="#boccale"/></svg> {E(birra)}</span>')


SENZA_CORNICE = set()
def AST(p):
    """09/10 Marco: asterisco sui piatti con prodotti congelati o abbattuti (dati.CONGELATI)"""
    import dati as _d
    return '<span style="font-size:.79em">*</span>' if p.get('nome') in getattr(_d, 'CONGELATI', ()) else ''   # 2 punti più piccolo del testo
FOTO_GRANDE = {'Battuta di scottona'}  # 08/10 Marco: cornice che racchiude la foto, foto più grande


def a_capo(desc, prezzo, cap=112):
    """una riga se ci sta; altrimenti va a capo dopo una virgola o prima di « e », riempiendo la prima riga."""
    if '\n' in desc or len(desc) + len(prezzo) + 3 <= cap:
        return desc
    tagli = [i + 1 for i in range(len(desc)) if desc.startswith(', ', i)] + \
            [i for i in range(len(desc)) if desc.startswith(' e ', i)]
    ok = [t for t in tagli if t <= cap and len(desc) - t + len(prezzo) + 3 <= cap]
    if not ok:
        return desc
    t = max(ok)
    return desc[:t].rstrip() + '\n' + desc[t:].lstrip()


def piatto(p, foto=False, rank=True, inline=False):
    foto = foto and p['nome'] in FOTO_VERE   # 08/10 Marco: senza foto vera niente foto (mai segnaposto né foto finte)
    cls = 'p'
    if p.get('ev'):
        cls += ' ' + p['ev']
    if foto:
        cls += ' pfoto'
        if p['nome'] in FOTO_GRANDE:
            cls += ' fotogrande'
    if p['nome'] in SENZA_CORNICE:
        cls += ' grande'
    rk = f'<span class="rank">{p["rank"]}°</span>' if rank and p.get('rank') else ''
    desc = (E(p['desc']) + AST(p)).replace('\n', '<br>')   # 09/10 Marco: asterisco sull'ultima lettera della descrizione
    due = '<span class="due">, per 2 persone</span>' if p.get('per2') else ''
    pr = E(p['prezzo_txt']) if p.get('prezzo_txt') else prz(p['new'])
    corpo = (f'<span class="nome">{rk}{E(p["nome"]).replace("&quot;in nero&quot;", "“in nero”")}{abb2_html(p.get("abb2"))}</span>'
             f'<span class="desc">{desc}<span class="pz"><span class="sep">|</span><span class="prezzo">{pr}</span>{due}</span></span>'
             f'<span class="mk">{E(mk_text(p))}</span>')
    if foto:
        return f'<div class="{cls}"><div>{corpo}</div>{foto_html(p["nome"])}</div>'
    return f'<div class="{cls}">{corpo}</div>'


def cap(occ, tit, prem=False):
    return f'<div class="cap"><h2 class="cat{" prem" if prem else ""}">{tit}</h2></div>'


def lista(items, foto=False, inline=False, due=False, foto_su=None, rank=True):
    """foto di fianco: sul piatto foto_su se indicato, altrimenti sul n.1 (max 2 foto per pagina)."""
    out = []
    for p in items:
        f = (p['nome'] == foto_su) if foto_su else (foto and (p.get('rank') == 1 or (due and p.get('rank') == 2)))
        out.append(piatto(p, foto=f, inline=inline, rank=rank))
    return f'<div class="piatti{" inl" if inline else ""}">' + ''.join(out) + '</div>'


def premio(occ, tit, items, sotto=''):
    body = ''.join(piatto(p, rank=False) for p in items)
    return (f'<div class="premio"><p class="occhiello">{occ}</p><h2 class="cat prem">{tit}</h2>'
            f'{f"<p class=pre-sotto>{sotto}</p>" if sotto else ""}<div class="piatti">{body}</div></div>')


def nota(t):
    return f'<p class="nota">{t}</p>'


LEGALE = ('I piatti che presentano l’asterisco potrebbero essere preparati con prodotti congelati o abbattuti in base alla disponibilità.<br>'
          'L’elenco completo degli allergeni presenti nei nostri piatti è disponibile su richiesta. Consulta il personale o richiedi il documento dedicato.<br>'
          'Prezzi espressi in euro. Coperto e Servizio | {cop}')


def pag(inner, n, extra='', cop=None):
    leg = f'<p class="legale">{LEGALE.format(cop=prz(cop))}</p>' if cop and isinstance(n, int) and n % 2 == 0 else ''
    return f'<section class="pag{(" " + extra) if extra else ""}">{inner}{leg}<div class="num">— {n} —</div></section>'


def spread(label, *pagine):
    return f'<div class="spread"><p class="etichetta">{label}</p><div class="doppia">{"".join(pagine)}</div></div>'


F_ICON = {1: '#f1', 2: '#f2', 3: '#f3'}


# ---------------------------------------------------------------- costruzione carta
def costruisci(L):
    sg = L['sigla']
    C = {k: [calcola(p, sg) for p in L[k]] for k in
         ['premium_antipasti', 'antipasti', 'premium_primi', 'primi', 'premium_secondi', 'secondi', 'contorni',
          'classiche', 'saporite', 'tartufate', 'gourmet', 'speciali', 'calzoni', 'dolci']}
    fuori = {k: [calcola(p, sg) for p in L.get(k, [])] for k in
             ['fuori_antipasti', 'fuori_primi', 'fuori_contorni', 'fuori_pizze', 'fuori_dolci']}
    sorb = calcola(L['sorbetto'], sg)
    for k in ['antipasti', 'primi', 'secondi', 'classiche', 'saporite', 'gourmet', 'speciali', 'calzoni', 'dolci',
              'premium_primi', 'premium_secondi', 'contorni']:
        C[k] = ordina(C[k])
    evidenzia(C['antipasti'])
    for k in ['primi', 'secondi', 'gourmet', 'speciali']:   # le classiche restano sobrie, senza evidenze
        evidenzia(C[k])
    evidenzia(C['dolci'])
    for k in ['premium_antipasti', 'premium_primi', 'premium_secondi', 'tartufate']:
        for p in C[k]:
            p['ev'] = None
    # dolci con foto in cima: i primi tre in ordine di pagina
    tutti = [p for v in C.values() for p in v] + [sorb]

    # ---- volumi di base (6 mesi → anno)
    cats = [k for k in KS if (('TENNIS' in k.upper()) == (sg == 'TENNIS'))
            and 'PRANZO' not in k.upper() and 'TAGLIERI' not in k.upper()]
    princ = sum(p['q'] for k in cats for p in KS[k]
                if any(w in k.upper() for w in ['PIZZE', 'CALZONI', 'PRIMI', 'SECONDI'])
                and 'Nutella' not in p['prod'])
    marg_cibo = sum(p['mc'] * p['q'] for k in cats for p in KS[k] if 'Concordato' not in p['prod'])
    dolci_q = sum(p['q'] for k in cats for p in KS[k] if 'DESSERT' in k.upper())
    coperti_a = 2 * princ
    m_coperto = marg_cibo / princ
    amari_q = sum(L['amari_q6'].values())

    leve = []
    def leva(nome, euro, dove):
        leve.append(dict(leva=nome, euro=round(euro), dove=dove))
        return round(euro)

    # prezzi (solo piatti con storico di vendita)
    lp = sum(p['leva_prezzo'] for p in tutti)
    leva('Prezzi definitivi (colonna PREZZO FINALE del foglio)', lp, 'tutte le pagine')

    # uscite: i clienti del piatto tolto scelgono un piatto della stessa pagina (margine medio)
    def uscita(lst, ref):
        med = sum(p['m_new'] for p in ref) / len(ref)
        return sum(max(0, med - p['m_old']) * p['qa'] * 0.8 for p in lst if p['qa'])
    lu = (uscita(fuori['fuori_antipasti'], C['antipasti'])
          + uscita(fuori['fuori_primi'], C['primi'] + C['premium_primi'])
          + uscita(fuori['fuori_contorni'], C['contorni'])
          + uscita(fuori['fuori_pizze'], C['classiche'] + C['saporite'] + C['gourmet'] + C['speciali'])
          + uscita(fuori['fuori_dolci'], C['dolci']))
    e_usc = leva('Piatti tolti: chi li ordinava sceglie tra quelli che restano', lu, 'tutte le pagine')

    # formati pasta
    primi_all = C['primi'] + C['premium_primi']
    fc_primo = sum(p['fc'] for p in primi_all) / len(primi_all)
    q_primi = sum(ks(*p['sale'])['q'] * 2 if p.get('sale') else p.get('q6', 0) * 2 for p in primi_all)
    if q_primi == 0:  # Tennis: carta primi nuova, uso il venduto primi dei 6 mesi
        q_primi = 2 * sum(p['q'] for k in cats if 'PRIMI' in k.upper() for p in KS[k])
    else:
        q_primi = 2 * sum(p['q'] for k in cats if 'PRIMI' in k.upper() for p in KS[k])
    guad_r = 4 / IVA - 0.45 * fc_primo
    guad_p = 6 / IVA - 1.1 * fc_primo
    e_form = leva('Formati della pasta (8% abbastanza +4, 3% tanta +6)',
                  q_primi * (0.08 * guad_r + 0.03 * guad_p), 'pag. 4')

    # impasti pizza
    q_pizze = 2 * sum(p['q'] for k in cats if 'PIZZE' in k.upper() or 'CALZONI' in k.upper() for p in KS[k]
                      if 'Nutella' not in p['prod'])
    # aggiunte sulla pizza (prezzo, costo IVA esclusa da listino file 02 con scarto)
    AGG = [('Tartufo nero', 6, 0.87, 'agg_tartufo.png', 'a lamelle, sopra ogni pizza'),
           ('Burrata', 3.5, 1.40, 'agg_burrata.png', 'di Puglia, aggiunta a crudo'),
           ('Crudo di Parma', 3, 0.82, 'agg_crudo.png', '18 mesi, a fette sottili')]
    m_agg = sum(p / IVA - c for _, p, c, *r in AGG) / len(AGG)
    e_imp = leva(f'Aggiunte sulla pizza (10 pizze su 100, margine medio {m_agg:.2f} €)'.replace('.', ','), q_pizze * 0.10 * m_agg, 'pag. 7')

    # Cartabianca Experience (08/10, Emiliano + Marco): PER DUE = un antipasto da dividere, un primo o un secondo a testa
    # (scelti dallo chef tra quelli della carta, non i piatti della casa) e un dolce da dividere; coperto e bevande esclusi
    av = lambda ks, f: sum(p[f] for k in ks for p in C[k]) / sum(len(C[k]) for k in ks)
    deg = [p for p in C['dolci'] if 'Degustazione' in p['nome']]
    perc_prezzo = L.get('percorso', {}).get('prezzo', 49)
    perc_costo = av(['antipasti'], 'fc') + 2 * av(['primi', 'secondi'], 'fc') + av(['dolci'], 'fc')   # per due
    perc_m = perc_prezzo / IVA - perc_costo                                                        # per due
    alla_carta = int(av(['antipasti'], 'new') + 2 * av(['primi', 'secondi'], 'new') + av(['dolci'], 'new'))   # 08/10 Marco: coperto ESCLUSO
    guad_perc = perc_m / 2 - m_coperto        # a coperto, bevande escluse: confronto col margine cibo di un coperto medio
    e_perc = leva(f'«{L.get("percorso",{}).get("nome","Experience")}» a {perc_prezzo // 2} € a persona, 2 persone (3 coperti su 100)', coperti_a * 0.03 * guad_perc, 'pag. 3')

    # dolci
    m_dolce = sum(p['m_new'] for p in C['dolci']) / len(C['dolci'])
    att = dolci_q / princ
    e_dol = leva(f'Carta dei dolci A5 a parte, con le foto: da {att*100:.0f} a {att*100+5:.0f} dolci ogni 100 coperti',
                 coperti_a * 0.05 * m_dolce, 'carta dei dolci A5')
    # amari
    att_a = amari_q / princ
    e_ama = leva(f'Amari con la loro sezione: da {att_a*100:.1f} a {att_a*100+4:.1f} ogni 100 coperti',
                 coperti_a * 0.04 * 3.4, 'pag. 8')
    tot = sum(l['euro'] for l in leve)

    m_prem_p = sum(p['m_new'] for p in C['premium_primi']) / max(1, len(C['premium_primi']))
    m_prem_s = sum((p['m_new'] * 1.15 if p.get('per2') else p['m_new']) for p in C['premium_secondi']) / max(1, len(C['premium_secondi']))
    ctx = dict(m_prem_p=m_prem_p, m_prem_s=m_prem_s, L=L, C=C, fuori=fuori, sorb=sorb, leve=leve, tot=tot, princ=princ, coperti_a=coperti_a,
               m_coperto=m_coperto, att=att, att_a=att_a, perc=dict(prezzo=perc_prezzo, m=perc_m, costo=perc_costo,
               guad=guad_perc), e=dict(usc=e_usc, form=e_form, imp=e_imp, perc=e_perc, dol=e_dol, ama=e_ama, prezzi=lp),
               guad_r=guad_r, guad_p=guad_p, alla_carta=alla_carta, AGG=AGG, m_agg=m_agg)
    return ctx


# ---------------------------------------------------------------- pagine
def sez_leva(ctx, chiavi):
    return sum(p['leva_prezzo'] for k in chiavi for p in ctx['C'][k])


def fuori_txt(lst):
    if not lst:
        return ''
    return 'Escono: ' + '; '.join(f'<b>{E(p["nome"])}</b> ({p["motivo"]})' for p in lst) + '.'


def fotorow(items, n=2, hero=False):
    """foto grandi scontornate in fondo alla sezione (stile Eataly): i primi due piatti in pagina = n.2 e n.1."""
    out = []
    for p in items[:n]:
        src = p.get('img')
        img = (f'<img src="{src}" alt="">' if src else
               '<svg viewBox="0 0 120 50" class="ph"><ellipse cx="60" cy="24" rx="54" ry="17" fill="#fff" stroke="#E2D8CF" stroke-width=".8"/>'
               '<ellipse cx="60" cy="23" rx="36" ry="10.5" fill="#F7F2EC" stroke="#EDE4DA" stroke-width=".6"/>'
               '<text x="60" y="26" text-anchor="middle" font-size="5" letter-spacing="1.4" fill="#B9A99B">FOTO</text></svg>')
        out.append(f'<figure class="ft"><div class="ftimg">{img}</div><figcaption>{E(p["nome"])}</figcaption></figure>')
    return f'<div class="fotorow{" hero" if hero else ""}">' + ''.join(out) + '</div>'


def premio2(occ, tit, items, var, sotto=''):
    """i blocchi «della casa» cambiano forma da una pagina all'altra: cornice / linee / eroe / tinta."""
    body = ''.join(piatto(p, rank=False) for p in items)
    return (f'<div class="premio2 {var}"><h2 class="cat prem">{tit}</h2>'
            f'{f"<p class=pre-sotto>{sotto}</p>" if sotto else ""}<div class="pgrid n{len(items)}">{body}</div></div>')


def blocco(tit, items, var, sotto='', foto=None):
    """blocchi «della casa», ognuno con una forma sua: rosso pieno / crema / brace / cornice con foto che esce."""
    body = ''.join(piatto(p, rank=False) for p in items)
    vere = [p['nome'] for p in items if p['nome'] in FOTO_VERE]
    ft = f'<div class="fotoesce">{foto_html(vere[0] if vere else "")}</div>' if foto else ''
    return (f'<div class="blocco-casa {var}">{ft}{f"<h3>{tit}</h3>" if tit else ""}'
            f'{f"<p class=sotto>{sotto}</p>" if sotto else ""}<div class="bc-piatti n{len(items)}">{body}</div></div>')


def titolo(t, sotto='', liv=1):
    return f'<div class="tit l{liv}"><h2>{t}</h2>{f"<p>{sotto}</p>" if sotto else ""}</div>'


ICONE = {
  'agg_tartufo.png': '<svg class="ico-agg" viewBox="0 0 64 64"><path d="M14 36c-3-9 2-19 11-22 4-6 14-6 19-1 8 1 12 9 10 17 3 7-2 15-10 16-5 5-14 5-19 1-7 1-13-4-11-11z" fill="none" stroke="currentColor" stroke-width="1.6"/><g fill="currentColor"><circle cx="24" cy="26" r="1.3"/><circle cx="33" cy="22" r="1.3"/><circle cx="41" cy="29" r="1.3"/><circle cx="29" cy="34" r="1.3"/><circle cx="38" cy="39" r="1.3"/><circle cx="22" cy="40" r="1.3"/><circle cx="46" cy="22" r="1"/><circle cx="18" cy="31" r="1"/></g><path d="M46 52l8-6M50 55l6-5" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>',
  'agg_burrata.png': '<svg class="ico-agg" viewBox="0 0 64 64"><path d="M32 18c-2-5 2-9 4-9 0 4-1 6-4 9z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M32 18c-13 0-21 9-21 19 0 10 9 16 21 16s21-6 21-16c0-10-8-19-21-19z" fill="none" stroke="currentColor" stroke-width="1.6"/><path d="M24 26c3-2 6-3 8-3" stroke="currentColor" stroke-width="1.1" stroke-linecap="round" fill="none"/><path d="M8 54h48" stroke="currentColor" stroke-width="1.2" stroke-linecap="round"/></svg>',
  'agg_crudo.png': '<svg class="ico-agg" viewBox="0 0 64 64"><path d="M50 12c3 3 3 7 0 10L40 32c-4 12-14 22-24 20-6-1-8-7-5-13 4-9 14-14 25-17l10-10c1-1 3-1 4 0z" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"/><path d="M18 44c4-6 10-10 16-12" stroke="currentColor" stroke-width="1.1" fill="none" stroke-linecap="round"/><circle cx="48" cy="16" r="2.4" fill="none" stroke="currentColor" stroke-width="1.2"/></svg>',
}


def img64(f):
    import base64
    mime = 'jpeg' if f.lower().endswith(('.jpg', '.jpeg')) else ('webp' if f.endswith('.webp') else 'png')
    return f'data:image/{mime};base64,' + base64.b64encode(open(os.path.join(HERE, 'img', f), 'rb').read()).decode()


def upsell(tit, sotto, voci):
    """upsell su una riga, senza riquadro: titolo + voci separate da un filetto verticale."""
    vv = ''.join(f'<div class="uv">{ico}<b>{n}</b><span>{d}</span><i>{p}</i></div>' for ico, n, d, p in voci)
    return f'<div class="upsell2"><p class="ut2"><b>{tit}</b> {sotto}</p><div class="uvs">{vv}</div></div>'


SOMM = ('<p class="somm"><svg width="11" height="16" style="--w:#6E2A6B"><use href="#calice"/></svg>'
           '<svg width="15" height="16" style="--w:#E3AE32"><use href="#boccale"/></svg> '
           'Il calice e il boccale accanto ai piatti sono gli abbinamenti scelti dal nostro <b>beer &amp; wine sommelier</b>: '
           'il vino o la birra che esaltano quel piatto. Chiedete al personale, ve lo serviamo al calice.</p>')


def render(ctx):
    L, C, F = ctx['L'], ctx['C'], ctx['fuori']
    sg = L['sigla']
    pom = L['pomodoro']
    cop = COPERTO.get(sg, 2.5)
    P = []
    luogo = L['nome_cop'].replace('Cartabianca ', '')

    # 1 copertina
    P.append(spread('Copertina', pag(f'''
      <div class="cop2">
        <div class="cb">CARTABIANCA</div>
        <div class="cop-linee"><em>{E(luogo)}</em></div>
        <p class="cop-sotto">ristorante · pizzeria</p>
      </div>
      <p class="cop-ind">{E(L["indirizzo"])}</p>''', 1, 'copertina')))

    # 2 antipasti | 3 carta bianca allo chef
    tA = sez_leva(ctx, ['antipasti', 'premium_antipasti'])
    p2 = titolo('Antipasti')
    p2 += lista(C['antipasti'], foto=True)
    ILLU = False  # 05/10: illustrazione sospesa da Marco, si rimette con True
    if ILLU:
        p2 += f'<img class="illu" src="{img64("illustrazione_antipasti.png")}" alt="">'
    if C['premium_antipasti']:
        p2 += titolo('Le selezioni Cartabianca', liv=3) + lista(C['premium_antipasti'], rank=False)
    p2 += nota(f'<b>Per margine: n.2 in cima, n.1 in seconda posizione in cornice, n.3 in fondo; le due foto grandi in fondo riempiono la pagina.</b> Prezzi: '
               f'<b>+{intero(tA)} €/anno</b>. {fuori_txt(F["fuori_antipasti"])}')
    pc = ctx['perc']
    per = L['percorso']
    alla_carta = ctx['alla_carta']
    p3 = f'''
      <div class="exp">
        <div class="cb small">CARTABIANCA</div>
        <h2 class="exp-t">Experience</h2>
        <p class="exp-intro">Un percorso per vivere al massimo la nostra cucina.<br>Scegliete il vostro viaggio: <b>tra Terra e Mare</b>.</p>
        <div class="exp-p"><h3>Un antipasto da dividere</h3><p>al centro del tavolo</p></div>
        <div class="exp-p"><h3>Una portata a testa</h3><p>a scelta tra <span class="exp-cat">La pasta</span> e <span class="exp-cat">I secondi</span></p></div>
        <div class="exp-p"><h3>e un dolce da dividere</h3><p>dalla nostra pasticceria, per chiudere il viaggio</p></div>
        <p class="exp-note"><span class="pz"><s>{per.get("barrato", round(alla_carta / 2))}</s> <span class="prezzo">{per["prezzo"] // 2} pp</span></span></p>
        <p class="exp-legal">La portata a testa si sceglie solo tra i piatti delle sezioni «La pasta» e «I secondi» della carta. Coperto e bevande esclusi.</p>
      </div>
      {nota(f'<b>+{intero(ctx["e"]["perc"])} €/anno se la sceglie 3 coperti su 100.</b> Formula di Emiliano (08/10): per due, antipasto e dolce da dividere, un primo o secondo a testa. Barrato {per.get("barrato")} pp scelto da Marco; media alla carta vera (antipasto + 2 tra pasta/secondi + dolce, coperto escluso) = {alla_carta} € per due, cioè {round(alla_carta / 2)} pp. '
            f'Costo medio {eur(pc["costo"])} € per due, margine {eur(pc["m"])} € per due ({eur(pc["m"] / 2)} € a testa) contro {eur(ctx["m_coperto"])} € di un coperto medio (solo cibo).')}'''
    P.append(spread('Si apre · antipasti e Cartabianca Experience', pag(p2, 2, cop=cop), pag(p3, 3, 'rossa centrata')))

    # 4 primi | 5 secondi
    ICO = lambda i, w, h: f'<svg width="{w}" height="{h}" viewBox="0 0 32 24"><use href="#f{i}"/></svg>'
    form = ('<div class="fame"><p class="fame-t">Che fame hai?</p><div class="fame-row">'
            f'<div class="fm1"><span class="ic">{ICO(1, 26, 20)}</span><em>normale</em><b>100 g</b><i>&#160;</i></div>'
            f'<div class="fm1"><span class="ic">{ICO(2, 34, 26)}</span><em>abbastanza</em><b>150 g</b><i>+ 4</i></div>'
            f'<div class="fm1"><span class="ic">{ICO(3, 42, 32)}</span><em>tanta</em><b>220 g</b><i>+ 6</i></div>'
            '</div></div>')
    tP = sez_leva(ctx, ['primi', 'premium_primi'])
    p4 = (titolo('I primi d’autore') + blocco('', C['premium_primi'], 'cornice senza-tit', foto=True)
          + form + titolo('La pasta', liv=2) + lista(C['primi'])
          + nota(f'<b>Primi d’autore 22-23 € (margine medio {eur(sum(p["m_new"] for p in C["premium_primi"])/3)} €): cornice con foto.</b> '
                 f'I grandi secondi rendono di più per ordine e prendono il blocco rosso. Formati +4/+6: <b>+{intero(ctx["e"]["form"])} €/anno</b>. '
                 f'Prezzi: <b>+{intero(tP)} €/anno</b>. {fuori_txt(F["fuori_primi"])}'))
    tS = sez_leva(ctx, ['secondi', 'premium_secondi', 'contorni'])
    cont = ''.join(f'<div class="ct"><b>{E(p["nome"])}</b><span>{attacca_prezzo(E(p.get("desc") or ""), prz(p["new"]), AST(p)).replace(chr(10), "<br>")}</span></div>' for p in C['contorni'])
    p5 = (titolo('I grandi secondi', liv=2) + blocco('', C['premium_secondi'], 'rosso tartufo senza-tit', foto=True)
          + titolo('I secondi', liv=2) + lista(C['secondi'])
          + titolo('Contorni', liv=3) + f'<div class="contorni">{cont}</div>'
          + nota(f'<b>I grandi secondi prendono il blocco rosso</b>: margine per ordine ~{eur(ctx["m_prem_s"])} € contro ~{eur(ctx["m_prem_p"])} € dei primi d’autore (fiorentina contata 1,15 kg). '
                 f'Prezzi: <b>+{intero(tS)} €/anno</b>. {fuori_txt(F["fuori_contorni"])}'))
    P.append(spread('Si apre · i primi e i secondi', pag(p4, 4, 'stretta primi', cop=cop), pag(p5, 5, 'stretta', cop=cop)))

    # 6 speciali + nota birra + classiche (sinistra) | 7 tartufate + eccellenze + aggiunte (destra)
    birra = ('<div class="somm3"><p class="fame-t">Vino o birra?</p><div class="fame-row">'
             '<div class="fm1"><span class="ic"><svg width="22" height="32" viewBox="0 0 16 24" style="--w:#6E2A6B"><use href="#calice"/></svg></span>'
             '<em>un calice</em><b>il vino giusto per ogni pizza</b></div>'
             '<div class="fm1"><span class="ic"><svg width="30" height="32" viewBox="0 0 22 24" style="--w:#E3AE32"><use href="#boccale"/></svg></span>'
             '<em>una birra</em><b>chiara, ambrata, bianca o scura</b></div></div>'
             '<p class="somm3-n">Accanto a ogni pizza trovi l’abbinamento scelto dal nostro beer &amp; wine sommelier</p></div>')
    agg = ('<div class="cta"><p class="cta-t">La vuoi ancora più buona?</p><div class="cta-row">'
           + ''.join(f'<div class="cta-i">{foto_html(n)}<b>{E(n)}</b><span>{attacca_prezzo(E(d), '+&#8239;' + prz(p))}</span></div>'
                     for n, p, c, f, d in ctx['AGG']) + '</div></div>')
    tPz = sez_leva(ctx, ['speciali', 'classiche'])
    for _p in C['speciali'] + C['classiche']:
        _p['desc'] = a_capo(_p['desc'], prz(_p['new']))
    p6 = (titolo('Le pizze speciali') + lista(C['speciali'], inline=True)
          + birra + titolo('Le pizze classiche', liv=2) + f'<div class="sobria">{lista(C["classiche"], inline=True)}</div>'
          + nota(f'<b>Sinistra: speciali in alto, nota del beer sommelier, classiche sobrie in basso.</b> Prezzi: <b>+{intero(tPz)} €/anno</b>.'))
    tT = sez_leva(ctx, ['tartufate', 'gourmet'])
    p7 = (titolo('Le pizze tartufate') + blocco('', C['tartufate'], 'rosso tartufo senza-tit', foto=True)
          + titolo('Le eccellenze di Cartabianca') + lista(C['gourmet'], foto=True, inline=True) + agg
          + nota(f'<b>Tartufate nel blocco rosso, in alto a destra (17/15, proposta RBR).</b> Aggiunte al posto degli impasti (che non hanno): '
                 f'<b>+{intero(ctx["e"]["imp"])} €/anno</b> se le prende 1 pizza su 10, margine medio {eur(ctx["m_agg"])} €. '
                 f'Prezzi: <b>+{intero(tT)} €/anno</b>. Pizze tolte: {fuori_txt(F["fuori_pizze"])[8:]}'))
    P.append(spread('Si apre · le pizze', pag(p6, 6, 'stretta pz6', cop=cop), pag(p7, 7, 'larga', cop=cop)))

    # 8 retro copertina
    p8 = f'''<div class="retro">
        <div class="cb small">CARTABIANCA</div>
        <p class="r-luogo">{E(L["nome_cop"])}</p>
        <p class="r-ind">{E(L["indirizzo"])}</p>
        <p class="r-grazie">Grazie di essere stati nostri ospiti.<br>Chiedete la carta dei dolci e quella dei vini e delle birre.</p>
      </div>''' + nota(f'Amari, caffè e sorbetto sono sul retro della carta dei dolci A5. Amari: <b>+{intero(ctx["e"]["ama"])} €/anno</b>.')
    P.append(spread('Retro copertina', pag(p8, 8, 'copertina retro')))
    return ''.join(P)


# ---------------------------------------------------------------- pagina html
CSS = open(os.path.join(HERE, 'stile.css'), encoding='utf-8').read()
SYM = open(os.path.join(HERE, 'simboli.svg'), encoding='utf-8').read()


def pagina(ctx):
    L = ctx['L']
    righe = ''.join(f'<tr><td>{E(l["leva"])}</td><td class="dove">{l["dove"]}</td><td class="n">+{intero(l["euro"])} €</td></tr>'
                    for l in ctx['leve'])
    riep = f'''<div class="riepilogo"><p class="etichetta">Vista consulente · potenziale della carta</p>
      <div class="rbox"><h3>{E(L["nome"])}: <b>+{intero(ctx["tot"])} €/anno</b> di margine</h3>
      <table>{righe}</table>
      <p class="rnote">Venduto Cassa in Cloud 1 marzo – 31 agosto 2026 ×2 per l'anno · food cost dal file 02 (IVA esclusa, prezzi ÷1,1) ·
      prezzi = foglio «Prezzi definitivi - Cartabianca», colonna PREZZO FINALE · ipotesi di adozione dichiarate in ogni nota.</p></div></div>'''
    return f'''<title>Carta Cartabianca {"Tennis" if L["sigla"]=="TENNIS" else "Club"}</title>
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;1,400;1,600&family=DM+Sans:wght@400;500;600;700&display=swap">
<style>{CSS}</style>
{SYM}
<div class="bar">
  <div class="id"><b>CARTABIANCA</b><span>{E(L["nome"])} · libro A4 · proposta RBR</span></div>
  <div class="toggle" role="group" aria-label="Vista">
    <button id="bCli" aria-pressed="true">Vista cliente</button>
    <button id="bCon" aria-pressed="false">Vista consulente</button>
  </div>
  <p class="hint" id="hint">Il menu come lo vede chi si siede al tavolo.</p>
</div>
<div class="piano">
{riep}
{render(ctx)}
</div>
<script>
(function(){{
  var b=document.body,cli=document.getElementById('bCli'),con=document.getElementById('bCon'),hint=document.getElementById('hint');
  function set(rbr){{
    b.classList.toggle('rbr',rbr);
    cli.setAttribute('aria-pressed',String(!rbr));con.setAttribute('aria-pressed',String(rbr));
    hint.textContent=rbr?'Food cost dal file 02, venduto marzo-agosto 2026. Il numero nel cerchietto è il posto per margine nella sezione.':'Il menu come lo vede chi si siede al tavolo.';
  }}
  cli.addEventListener('click',function(){{set(false)}});con.addEventListener('click',function(){{set(true)}});
}})();
</script>'''


def allinea_prezzi():
    """menu unico: stesso prezzo nei due locali = il più alto dei due prezzi finali (fiorentina esclusa, al kg e carne diversa)."""
    from dati import UNICO
    cT, cC = costruisci(TENNIS)['C'], costruisci(CLUB)['C']
    diff = []
    for k in UNICO:
        pt = {p['nome']: p['new'] for p in cT[k]}
        pc = {p['nome']: p['new'] for p in cC[k]}
        for L in (TENNIS, CLUB):
            for p in L[k]:
                n = p['nome']
                if 'fiorentina' in n or pt.get(n) == pc.get(n):
                    continue
                m = max(pt[n], pc[n])
                p['nuovo_prezzo'] = m
                if L is TENNIS:
                    diff.append(f'{n}: Tennis {prz(pt[n])} / Club {prz(pc[n])} → {prz(m)}')
    return diff


if __name__ == '__main__':
    out = {}
    for r in allinea_prezzi():
        print('  prezzo allineato ·', r)
    for L, f in [(TENNIS, 'carta_tennis.html'), (CLUB, 'carta_club.html')]:
        ctx = costruisci(L)
        open(os.path.join(HERE, f), 'w', encoding='utf-8').write(pagina(ctx))
        out[L['sigla']] = dict(tot=ctx['tot'], leve=ctx['leve'], coperti_anno=ctx['coperti_a'],
                               m_coperto=round(ctx['m_coperto'], 2))
        print(f, 'TOTALE', ctx['tot'])
        for l in ctx['leve']:
            print(f'   {l["euro"]:>8}  {l["leva"]}')
    json.dump(out, open(os.path.join(HERE, 'riepilogo_leve.json'), 'w'), ensure_ascii=False, indent=1)

