# -*- coding: utf-8 -*-
"""Listino prezzo finale per locale, pronto per Cassa in Cloud (07/10/2026).

Fonti (snapshot in questa cartella, sola lettura):
- sheet.json        foglio «Prezzi definitivi - Cartabianca» 1CMhwMHH…FjDE (colonna PREZZO FINALE)
- products.json.gz  catalogo prodotti Cassa in Cloud (GET /products, 2.609 prodotti, 06/10/2026)
- sold12m.json.gz   venduto per locale ott-2025 → set-2026 (GET /reports/sold/products)

Regole:
- BAR = 7 bar (Panciatichi, Novoli, Calenzano, Osmannoro, Prato, Ingromarket, Soffiano);
  RISTORANTI = Club San Mauro + Tennis. Coperto 2,50 solo Club e Tennis.
- Abbinamento categoria+prodotto (senza accenti/punteggiatura) sul catalogo di cassa.
- Prezzo di oggi = prezzo del locale in cassa (se c'è) altrimenti prezzo generale.
- Si carica SOLO se il prezzo sale e il prezzo di cassa è fisso (non a peso, non 0).
  Ribassi, salti oltre +35% (tranne coperto), prezzi liberi e prodotti a peso → «Da verificare».
- Effetto €/anno = (nuovo − oggi) / 1,1 × pezzi 12 mesi × 0,98 (stessa formula del foglio).
Uso: python3 build_listino.py  → Cartabianca_Listino_Cassa_2026-10-07.xlsx + payload_cassa.json
"""
import json, gzip, collections, unicodedata, re, os, datetime as dt
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '..', '..', '..', 'consegne', '2026-10-07')
P = json.load(gzip.open(os.path.join(HERE, 'products.json.gz')))
S = json.load(open(os.path.join(HERE, 'sheet.json')))
SOLD = json.load(gzip.open(os.path.join(HERE, 'sold12m.json.gz')))

SPN = {13785: 'Panciatichi', 13788: 'Novoli', 13782: 'Calenzano', 13786: 'Osmannoro', 13783: 'Prato',
       25818: 'Ingromarket', 38512: 'Soffiano', 13784: 'Club San Mauro', 27029: 'Tennis'}
BAR = [13785, 13788, 13782, 13786, 13783, 25818, 38512]
RIST = [13784, 27029]
# nomi del foglio diversi dal nome in cassa (piatti nuovi della carta pranzo, righe 241-250 del tab BAR)
ALIAS = {'penne integrali pomodori secchi mandorle pecorino': 'Penne Integrali Pomodori Secchi + Mandorle + Spolverata di Pecorino',
         'tagliatelle all uovo crema di zucca salsiccia': "Tagliatelle all'Uovo Crema di Zucca Gialla + Salsiccia",
         'carpaccio salmone arance finocchi': 'Carpaccio Salmone + Insalatina di Arance + Finocchi',
         'zuppetta di gamberetti crostoni': 'Zuppetta di Gamberetti + Crostoni di pane'}
COPERTO = {'Coperto Club': ('93d6ce48-8cae-4a42-8537-9f805b347dfd', 13784),
           'Coperto Tennis': ('b6852583-d272-40f8-86e8-25e2457e9901', 27029)}


def N(s):
    s = unicodedata.normalize('NFKD', str(s)).encode('ascii', 'ignore').decode().lower()
    return re.sub(r'[^a-z0-9]+', ' ', s).strip()


byid = {p['id']: p for p in P}
idx = collections.defaultdict(list)
for p in P:
    idx[(N(p['category']['description']), N(p['description']))].append(p)
qty = collections.defaultdict(collections.Counter)
prof = collections.defaultdict(collections.Counter)
soldkeys = set()
for sp, rows in SOLD.items():
    for r in rows:
        qty[r['idProduct']][int(sp)] += r.get('quantity', 0)
        prof[r['idProduct']][int(sp)] += r.get('profit', 0)
        soldkeys.add((N(r['product'].get('category', {}).get('description', '')), N(r['product']['description'])))


def prezzo_cassa(p, sp):
    g = None
    for x in p['prices']:
        if x.get('idSalesMode'):
            continue
        if x.get('idSalesPoint') == sp:
            return x['value']
        if 'idSalesPoint' not in x:
            g = x['value']
    return g


righe, nuovi, spariti = [], [], []
for tab, stores in (('Prezzi BAR', BAR), ('Prezzi RISTORANTI', RIST)):
    v = S[tab]; H = v[1]
    for r in v[3:]:
        if len(r) < 2 or not r[1]:
            continue
        d = dict(zip(H, r + [''] * 12))
        cat, prod, new = str(d['Categoria']).strip(), str(d['Prodotto']).strip(), d['PREZZO FINALE']
        if cat in COPERTO:
            pid, sp = COPERTO[cat]; cands = [byid[pid]]; st = [sp]
        else:
            cands = idx.get((N(cat), N(prod)), []); st = stores
            if not cands and N(prod) in ALIAS:
                cands = idx.get((N(cat), N(ALIAS[N(prod)])), [])
        if not cands:
            rec = dict(tab=tab, cat=cat, prod=prod, nuovo=new, oggi=d['Prezzo oggi'], pezzi=d["Pezzi l'anno"])
            (spariti if (N(cat), N(prod)) in soldkeys else nuovi).append(rec)
            continue
        # doppioni in cassa (es. Spremuta, RedBull): si usa quello davvero battuto nei locali del tab
        p = sorted(cands, key=lambda c: -sum(qty[c['id']][s] for s in st))[0]
        mai_venduto = sum(qty[p['id']][s] for s in st) == 0  # piatto del pranzo a rotazione: vale per tutti i locali del tab
        for s in st:
            if p.get('idSalesPoint') and p['idSalesPoint'] != s:
                continue
            q = qty[p['id']][s]
            if q == 0 and p.get('idSalesPoint') != s and not mai_venduto:
                continue  # il locale non lo vende
            c = prezzo_cassa(p, s)
            medio = round(prof[p['id']][s] / q, 2) if q else None
            if p['description'] in ('Piatto Verdure Piccolo', 'Piatto Verdure Grande'):
                stato, nota = 'verifica', 'la carta pranzo nuova propone verdure piccolo/medio/grande 8/10/12: si carica con il sì di Massimo (e si crea il medio)'
            elif p['soldByWeight']:
                stato, nota = 'verifica', 'venduto a peso in cassa: il prezzo del foglio non è al kg'
            elif not c:
                stato, nota = 'verifica', 'in cassa è a prezzo libero (0): il prezzo lo batte il banco'
            elif new == c:
                stato, nota = 'uguale', ''
            elif new < c:
                stato, nota = 'verifica', 'il foglio è SOTTO la cassa: resta il prezzo di oggi finché Massimo non conferma'
            elif new / c > 1.35 and cat not in COPERTO:
                stato, nota = 'verifica', f'salto di +{round((new / c - 1) * 100)}%: prezzo di cassa diverso da quello del foglio ({d["Prezzo oggi"]})'
            else:
                stato, nota = 'carica', ''
            base = medio if (stato == 'verifica' and not c) else c
            eff = round((new - base) / 1.1 * q * 0.98) if (base is not None and q and isinstance(new, (int, float))) else 0
            righe.append(dict(sp=s, locale=SPN[s], tab=tab, id=p['id'], cat=p['category']['description'],
                              prod=p['description'], iva=p['department']['tax']['rate'], oggi=c, medio=medio,
                              nuovo=new, pezzi=q, eff=eff, stato=stato, nota=nota,
                              solo_locale=bool(p.get('idSalesPoint'))))

carica = [x for x in righe if x['stato'] == 'carica']
verifica = [x for x in righe if x['stato'] == 'verifica']
uguali = [x for x in righe if x['stato'] == 'uguale']

# ---------- Excel ----------
ROSSO = 'A6192E'; CREMA = 'F5EFE0'
hf = Font(bold=True, color='FFFFFF'); hfill = PatternFill('solid', fgColor=ROSSO)
thin = Side(style='thin', color='DDDDDD')
wb = Workbook(); ws = wb.active; ws.title = 'Riepilogo'


def header(sh, cols, widths):
    sh.append(cols)
    for i, w in enumerate(widths, 1):
        c = sh.cell(row=sh.max_row, column=i); c.font = hf; c.fill = hfill
        c.alignment = Alignment(wrap_text=True, vertical='center')
        sh.column_dimensions[get_column_letter(i)].width = w
    sh.freeze_panes = sh.cell(row=sh.max_row + 1, column=1)


ws.append(['Cartabianca — listino prezzo finale per Cassa in Cloud'])
ws['A1'].font = Font(bold=True, size=14, color=ROSSO)
ws.append(['Fonte prezzi: foglio «Prezzi definitivi - Cartabianca» (03/10), colonna PREZZO FINALE. Prezzi di cassa letti il 06/10/2026. Pezzi = venduto ott-2025 → set-2026.'])
ws.append(['Effetto €/anno = (nuovo − oggi) / 1,1 × pezzi × 0,98, netto IVA. NON ancora caricato in cassa: si carica il giorno concordato con Massimo.'])
ws.append(['Come si carica: un tab per locale con l\'ID del prodotto in Cassa in Cloud (colonna A) e il PREZZO NUOVO. Il prezzo va messo come prezzo DEL LOCALE (non generale), così bar e ristoranti restano separati.'])
ws.append(['Il caricamento lo fa RBR via API il giorno concordato (file payload_cassa.json, stessi dati). In alternativa dal back office: Prodotti › cerca per nome › Prezzi › punto vendita.'])
ws.append([])
header(ws, ['Locale', 'Prezzi da cambiare', 'Effetto €/anno', 'Effetto €/mese', 'Già al prezzo nuovo', 'Da verificare'], [22, 18, 16, 16, 18, 16])
tot = [0, 0, 0, 0]
for sp in BAR + RIST:
    L = SPN[sp]
    n = sum(1 for x in carica if x['sp'] == sp); e = sum(x['eff'] for x in carica if x['sp'] == sp)
    u = sum(1 for x in uguali if x['sp'] == sp); vv = sum(1 for x in verifica if x['sp'] == sp)
    ws.append([L, n, e, round(e / 12), u, vv]); tot = [tot[0] + n, tot[1] + e, tot[2] + u, tot[3] + vv]
ws.append(['TOTALE', tot[0], tot[1], round(tot[1] / 12), tot[2], tot[3]])
for c in ws[ws.max_row]:
    c.font = Font(bold=True)
for row in ws.iter_rows(min_row=8, min_col=3, max_col=4):
    for c in row:
        c.number_format = '#,##0'

cols = ['ID prodotto Cassa in Cloud', 'Categoria in cassa', 'Prodotto', 'IVA %', 'Prezzo oggi in cassa', 'PREZZO NUOVO', 'Differenza', 'Pezzi 12 mesi', 'Effetto €/anno', 'Prezzo valido']
wid = [38, 26, 42, 7, 12, 12, 11, 11, 13, 22]
for sp in BAR + RIST:
    sh = wb.create_sheet(SPN[sp][:31])
    header(sh, cols, wid)
    for x in sorted([x for x in carica if x['sp'] == sp], key=lambda x: (x['cat'], x['prod'])):
        sh.append([x['id'], x['cat'], x['prod'], x['iva'], x['oggi'], x['nuovo'], round(x['nuovo'] - x['oggi'], 2),
                   x['pezzi'], x['eff'], 'solo questo locale' if x['solo_locale'] else 'prezzo del locale'])
        sh.cell(row=sh.max_row, column=6).font = Font(bold=True)
    for row in sh.iter_rows(min_row=2, min_col=5, max_col=7):
        for c in row:
            c.number_format = '0.00'
    for row in sh.iter_rows(min_row=2, min_col=8, max_col=9):
        for c in row:
            c.number_format = '#,##0'

sh = wb.create_sheet('Da verificare')
header(sh, ['Locale', 'Categoria in cassa', 'Prodotto', 'Prezzo oggi in cassa', 'Prezzo medio battuto', 'Prezzo foglio', 'Pezzi 12 mesi', 'Effetto €/anno se si applica', 'Perché non è nel listino', 'ID prodotto'],
       [16, 24, 38, 12, 12, 12, 11, 14, 60, 38])
for x in sorted(verifica, key=lambda x: (x['nota'][:12], x['prod'], x['locale'])):
    sh.append([x['locale'], x['cat'], x['prod'], x['oggi'], x['medio'], x['nuovo'], x['pezzi'], x['eff'], x['nota'], x['id']])

sh = wb.create_sheet('Nuovi da creare')
header(sh, ['Foglio', 'Categoria', 'Prodotto', 'PREZZO NUOVO', 'Nota'], [18, 22, 52, 12, 60])
for x in nuovi:
    pranzo = x['cat'].lower().startswith('pranzo')
    sh.append([x['tab'], x['cat'], x['prod'], x['nuovo'],
               'piatto nuovo della carta pranzo dei 7 bar: da creare in cassa (categoria PRANZO.)' if pranzo
               else ('prezzo da controllare: sembra al kg' if x['nuovo'] and isinstance(x['nuovo'], (int, float)) and x['nuovo'] > 12 and x['cat'] == 'Pane' else 'non c\'è in cassa e non è stato battuto negli ultimi 12 mesi: si crea solo se torna in carta')])

sh = wb.create_sheet('Non più in cassa')
header(sh, ['Foglio', 'Categoria', 'Prodotto', 'Prezzo foglio', 'Nota'], [18, 26, 48, 12, 60])
for x in spariti:
    sh.append([x['tab'], x['cat'], x['prod'], x['nuovo'], 'battuto negli ultimi 12 mesi ma oggi cancellato dal catalogo: niente da caricare (se è stato rinominato, applicare il prezzo al nome nuovo)'])

fn = os.path.join(OUT, 'Cartabianca_Listino_Cassa_2026-10-07.xlsx')
wb.save(fn)

# ---------- payload per il caricamento (NON eseguito) ----------
payload = collections.defaultdict(list)
for x in carica:
    payload[x['id']].append({'idSalesPoint': x['sp'], 'value': x['nuovo']})
json.dump({'generato': dt.datetime.now().isoformat(timespec='seconds'), 'nota': 'prezzi per locale da applicare il giorno concordato; NON eseguito. Al caricamento aggiornare/aggiungere SOLO la riga prezzo del locale (idSalesPoint): le altre righe prezzo del prodotto (prezzo generale, altri locali, Renai) restano come sono',
           'prodotti': payload}, open(os.path.join(HERE, 'payload_cassa.json'), 'w'), ensure_ascii=False, indent=1)

json.dump(dict(righe=righe, nuovi=nuovi, spariti=spariti), open(os.path.join(HERE, 'listino.json'), 'w'), ensure_ascii=False)
print('salvato', fn)
print('da caricare', len(carica), 'righe su', len({x['id'] for x in carica}), 'prodotti · effetto', sum(x['eff'] for x in carica))
print('già uguali', len(uguali), '· da verificare', len(verifica), '· nuovi', len(nuovi), '· spariti', len(spariti))
ver = collections.Counter(x['nota'].split(':')[0][:40] for x in verifica)
print(ver)
for sp in BAR + RIST:
    print(SPN[sp], sum(1 for x in carica if x['sp'] == sp), sum(x['eff'] for x in carica if x['sp'] == sp))

