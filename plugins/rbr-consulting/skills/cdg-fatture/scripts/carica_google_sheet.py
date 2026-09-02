#!/usr/bin/env python3
"""
Carica i dati di FATTURE.xlsx nel foglio/i Google "Economico"
(supporta sia un unico foglio "Economico" con anni affiancati in colonna,
sia fogli separati per anno: "Economico 2025", "Economico 2026", ecc.,
sia clienti multi-punto-vendita con --sheet per puntare a una tab specifica
tipo "Economico Store 1" — l'eventuale tab di riepilogo aggregato, es.
"Economico Aggregato", non va mai passata: e' solo formule che pescano dagli
store, si aggiorna da sola).

Uso:
    python carica_google_sheet.py <FATTURE.xlsx> <URL_google_sheet> [--write] [--sheet "<nome tab>"]

Default: DRY-RUN. --write esegue la scrittura reale. --sheet forza una tab
specifica per nome (bypassa la ricerca automatica "Economico"/"Economico <anno>").

Strategia (deterministica, MAI inserimento automatico di righe):
  - Riga 1 di ogni foglio: blocchi "TOTALE <anno>" + 12 mesi (ogni mese = 2 colonne)
    -> mappa (anno,mese)->colonna. Un foglio puo' contenere uno o piu' blocchi-anno.
  - Le righe-totale di categoria hanno =SUM(<col><s>:<col><e>): s = inizio area fornitori.
    La regione utilizzabile arriva fino alla riga della categoria-totale successiva - 1
    (o del blocco di riepilogo "COMPARAZIONE", se presente prima).
  - Categorie "contenitore" (es. Servizi/Materiali di consumo con sotto-voci tipo
    Affitti/Software/Varie...): il fornitore viene cercato in TUTTE le sotto-voci
    insieme; se nuovo, va nella prima riga libera di TUTTA l'area del contenitore,
    a prescindere dalla sotto-voce. Le intestazioni di sotto-categoria non si toccano.
  - I fornitori vengono messi in righe libere della regione (match esistente o prima
    libera); le celle gia' valorizzate vengono SOMMATE.
  - Se una categoria non ha spazio fisico sufficiente: NESSUNA scrittura (ne' per
    quella categoria ne' per le altre), lo script si ferma e stampa un riepilogo
    di quante righe vuote servono e dove, cosi' l'utente puo' aggiungerle a mano.
  - A fine carica, per ogni categoria/sotto-voce toccata la formula SUM di ogni
    colonna-mese viene NORMALIZZATA a =SUM(<col><s>:<col><end>).
  - Categoria "Altro" assente nel foglio -> viene creata una sezione dedicata prima
    del blocco "COMPARAZIONE" (di norma non dovrebbe servire: i fornitori nuovi
    vanno categorizzati prima di generare FATTURE.xlsx, mai lasciati in "Altro").
"""
import os
import sys
import re
from collections import defaultdict

import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from gspread.utils import rowcol_to_a1

BASE = os.path.dirname(os.path.abspath(__file__))


def _resolve(name):
    """Cerca il file in: $CDG_HOME, ~/.claude/rbr (chiavi installate da /rbr-setup),
    cartella dello script, cartella corrente."""
    for d in (os.environ.get('CDG_HOME'), os.path.expanduser('~/.claude/rbr'), BASE, os.getcwd()):
        if d and os.path.exists(os.path.join(d, name)):
            return os.path.join(d, name)
    return os.path.join(os.environ.get('CDG_HOME') or BASE, name)


CREDENTIALS = _resolve("credentials.json")
CAT_START_ROW = 21

MESI = {'gennaio': 1, 'febbraio': 2, 'marzo': 3, 'aprile': 4, 'maggio': 5, 'giugno': 6,
        'luglio': 7, 'agosto': 8, 'settembre': 9, 'ottobre': 10, 'novembre': 11, 'dicembre': 12}
SUM_RE = re.compile(r'=\s*SUM\(\s*([A-Z]+)(\d+)\s*:\s*([A-Z]+)(\d+)\s*\)', re.I)


def cell(grid, r, c):
    if 1 <= r <= len(grid):
        row = grid[r - 1]
        if 1 <= c <= len(row):
            return row[c - 1]
    return ''


def to_num(v):
    if isinstance(v, (int, float)):
        return float(v)
    s = str(v).replace('€', '').replace('\xa0', '').strip()
    if not s or s in ('-', '—', '–'):
        return 0.0
    neg = s.lstrip().startswith('-')
    s = s.replace('-', '').strip().replace('.', '').replace(' ', '').replace(',', '.')
    try:
        return (-1 if neg else 1) * float(s)
    except ValueError:
        return 0.0


def norm(s):
    return re.sub(r'\s+', ' ', str(s)).strip().lower()


def col_letter(c):
    return re.sub(r'\d', '', rowcol_to_a1(1, c))


def build_col_map(row1):
    colmap, year = {}, None
    for c, v in enumerate(row1):
        v = str(v if v is not None else '').strip()
        m = re.search(r'TOTALE\s*(\d{4})', v.upper())
        if m:
            year = int(m.group(1)); continue
        if v.lower() in MESI and year is not None:
            colmap[(year, MESI[v.lower()])] = c + 1
    return colmap


def resolve_worksheets(ss, years_needed):
    """Ritorna {worksheet_key: (worksheet, set_anni)}.
    Se esiste un unico foglio 'Economico', tutti gli anni ci finiscono dentro.
    Altrimenti cerca 'Economico <anno>' per ciascun anno servito."""
    titles = [w.title for w in ss.worksheets()]
    if 'Economico' in titles:
        ws = ss.worksheet('Economico')
        return {ws.id: (ws, set(years_needed))}, []

    by_ws = {}
    mancanti = []
    for y in sorted(years_needed):
        title = f'Economico {y}'
        if title in titles:
            ws = ss.worksheet(title)
            if ws.id not in by_ws:
                by_ws[ws.id] = (ws, set())
            by_ws[ws.id][1].add(y)
        else:
            mancanti.append(y)
    return by_ws, mancanti


def process_worksheet(ws, df, do_write):
    """Elabora un singolo worksheet con le fatture di df (gia' filtrate per gli anni
    pertinenti a questo foglio). Ritorna un dict di riepilogo per il report finale."""

    vals = ws.get_values(value_render_option='UNFORMATTED_VALUE')
    forms = ws.get_values(value_render_option='FORMULA')
    row1 = forms[0] if forms else []
    colmap = build_col_map(row1)
    year_total_col, year_pct_col = {}, {}
    for c, v in enumerate(row1):
        m = re.search(r'TOTALE\s*(\d{4})', str(v).upper())
        if m:
            y = int(m.group(1)); year_total_col[y] = c + 1; year_pct_col[y] = c + 2

    # Fallback posizionale: alcuni fogli "Economico <anno>" hanno l'intestazione riga 1
    # inaffidabile (es. "TOTALE" senza anno, mesi come numeri seriali di date residue di
    # un vecchio template, non testo "gennaio"/"febbraio"). Se non troviamo nulla di
    # testuale ma il titolo della tab contiene un anno, assumiamo il layout POSIZIONALE
    # standard confermato in tutti i fogli finora: TOTALE=col B(2), %=col C(3),
    # mese1..12 = colonne D,F,H,...,Z (4,6,8,...,26).
    if not colmap:
        m = re.search(r'(\d{4})', ws.title)
        if m:
            y = int(m.group(1))
            colmap = {(y, mese): 4 + 2 * (mese - 1) for mese in range(1, 13)}
            if y not in year_total_col:
                year_total_col[y], year_pct_col[y] = 2, 3

    month_cols = sorted(set(colmap.values()))
    n_rows = len(vals)
    colA = [cell(vals, r, 1) for r in range(1, n_rows + 1)]
    colA_norm = [norm(x) for x in colA]
    cat_total = {}
    for r in range(1, len(forms) + 1):
        for c in month_cols:
            m = SUM_RE.match(str(cell(forms, r, c)).strip())
            if m:
                cat_total[r] = (int(m.group(2)), int(m.group(4)))
                break
    total_rows_sorted = sorted(cat_total)

    # Limite invalicabile: la riga del blocco di riepilogo "COMPARAZIONE ..." (se presente).
    # Le sue righe (RICAVI, EBITDA, ...) usano formule tipo =D2+F2+H2 (non SUM), quindi NON
    # vengono rilevate come categoria da cat_total: senza questo limite, una categoria che
    # risulta l'ULTIMA con SUM nel foglio avrebbe end=n_rows e scriverebbe fornitori dentro
    # il blocco di riepilogo, corrompendolo.
    hard_stop_row = next(
        (i + 1 for i, a in enumerate(colA_norm) if 'comparazione' in a),
        n_rows + 1,
    )

    def region(cat_row):
        s = cat_total[cat_row][0]
        nxt = [r for r in total_rows_sorted if r > cat_row]
        end = (nxt[0] - 1) if nxt else n_rows
        end = min(end, hard_stop_row - 1)
        return s, end

    # ---- aggrega fatture (per nome NORMALIZZATO: varianti di spazi/maiuscole si fondono) ----
    agg = defaultdict(float)
    disp = {}
    for _, row in df.iterrows():
        try:
            d = pd.to_datetime(row['Data emissione'], dayfirst=True)
            cat = str(row['Categoria']).strip()
            sup_raw = str(row['DenominazioneFornitore']).strip()
            nsup = norm(sup_raw)
            agg[(cat, nsup, d.year, d.month)] += float(row['Imponibile'])
            disp.setdefault((cat, nsup), sup_raw)
        except Exception:
            continue
    per_fornitore = defaultdict(dict)
    for (cat, nsup, anno, mese), tot in agg.items():
        per_fornitore[(cat, nsup)][(anno, mese)] = tot

    # ---- trova riga categoria (gestisce anche categorie "contenitore" con sotto-voci) ----
    container_cache = {}

    def find_cat_row(cat):
        t = norm(cat)
        for i in range(CAT_START_ROW - 1, len(colA_norm)):
            if colA_norm[i] == t and (i + 1) in cat_total:
                return i + 1
        parent = next((i + 1 for i in range(CAT_START_ROW - 1, len(colA_norm)) if colA_norm[i] == t), None)
        if parent is None:
            return None
        if parent in container_cache:
            return parent if container_cache[parent] else None
        subs = []
        for c in month_cols:
            f = str(cell(forms, parent, c)).strip()
            if f.startswith('=') and 'SUM' not in f.upper() and '+' in f:
                subs = [int(x) for x in re.findall(r'[A-Za-z]+(\d+)', f)]
                break
        subs = sorted(r for r in subs if r in cat_total)
        container_cache[parent] = subs
        return parent if subs else None

    def get_span(cat_row):
        if cat_row in container_cache:
            subs = container_cache[cat_row]
            s = subs[0]
            _, end = region(subs[-1])
            return s, end
        return region(cat_row)

    def governing_sub(cat_row, landed_row):
        if cat_row in container_cache:
            subs = container_cache[cat_row]
            candidates = [sr for sr in subs if sr <= landed_row]
            return candidates[-1] if candidates else subs[0]
        return cat_row

    # ---- controllo capienza PRIMA di qualunque scrittura: mai inserimento automatico ----
    targets = defaultdict(list)
    cat_names = {}
    cat_non_trovate = defaultdict(list)
    altro_data = {}
    for (cat, nsup), mesi_val in per_fornitore.items():
        r = find_cat_row(cat)
        if r is None:
            if norm(cat) == 'altro':
                altro_data[nsup] = (disp[(cat, nsup)], mesi_val)
            else:
                cat_non_trovate[cat].append(disp[(cat, nsup)])
            continue
        targets[r].append(nsup)
        cat_names.setdefault(r, cat)

    shortfall = {}
    for r, nsups in targets.items():
        s, end = get_span(r)
        existing, empties = set(), 0
        for rr in range(s, end + 1):
            nm = colA_norm[rr - 1] if rr - 1 < len(colA_norm) else ''
            if nm:
                existing.add(nm)
            else:
                empties += 1
        need = max(0, sum(1 for n in nsups if n not in existing) - empties)
        if need:
            shortfall[r] = {'cat': cat_names[r], 'need': need, 'after_row': end}

    if shortfall:
        return {
            'sheet': ws.title, 'shortfall': shortfall, 'blocked': True,
            'fatture': len(df),
        }

    # ---- placement (spazio verificato sufficiente per tutti) ----
    batch = []
    writes_report = []
    nuovi_report = []
    anni_mancanti = set()
    touched = {}
    ptr = {}
    existing_cache = {}

    def cat_existing(cat_row, s, end):
        if cat_row not in existing_cache:
            ex = {}
            for r in range(s, end + 1):
                nm = colA_norm[r - 1] if r - 1 < len(colA_norm) else ''
                if nm:
                    ex[nm] = r
            existing_cache[cat_row] = ex
            ptr[cat_row] = s
        return existing_cache[cat_row]

    def place(cat_row, s, end, sup):
        ex = cat_existing(cat_row, s, end)
        if norm(sup) in ex:
            return ex[norm(sup)], False
        r = ptr[cat_row]
        while r <= end and colA_norm[r - 1]:
            r += 1
        if r > end:
            return None, False   # non dovrebbe accadere: shortfall gia' verificato a monte
        colA_norm[r - 1] = norm(sup)
        ex[norm(sup)] = r
        ptr[cat_row] = r + 1
        return r, True

    for (cat, nsup), mesi_val in sorted(per_fornitore.items()):
        cat_row = find_cat_row(cat)
        if cat_row is None:
            continue  # gia' in altro_data / cat_non_trovate
        sup = disp[(cat, nsup)]
        s, end = get_span(cat_row)
        row, is_new = place(cat_row, s, end, sup)
        if row is None:
            continue
        if is_new:
            nuovi_report.append((cat, sup, row))
            batch.append({'range': rowcol_to_a1(row, 1), 'values': [[sup]]})
        gov = governing_sub(cat_row, row)
        gov_s = cat_total[gov][0]
        tu = touched.get(gov, (gov_s, gov_s))
        touched[gov] = (gov_s, max(tu[1], row))
        for (anno, mese), tot in sorted(mesi_val.items()):
            col = colmap.get((anno, mese))
            if col is None:
                anni_mancanti.add(anno); continue
            vecchio = to_num(cell(vals, row, col))
            nuovo = round(vecchio + tot, 2)
            batch.append({'range': rowcol_to_a1(row, col), 'values': [[nuovo]]})
            writes_report.append((rowcol_to_a1(row, col), sup, anno, mese, vecchio, round(tot, 2), nuovo))

    formula_fixes = 0
    for cat_row, (s, last_used) in touched.items():
        orig_s, orig_e = cat_total[cat_row]
        new_end = max(orig_e, last_used)
        for c in month_cols:
            cl = col_letter(c)
            desired = f"=SUM({cl}{orig_s}:{cl}{new_end})"
            current = str(cell(forms, cat_row, c)).strip()
            if current != desired:
                batch.append({'range': rowcol_to_a1(cat_row, c), 'values': [[desired]]})
                formula_fixes += 1

    if do_write and batch:
        ws.batch_update(batch, value_input_option='USER_ENTERED')

    altro_info = None
    if altro_data:
        N = len(altro_data)
        BUF = 5
        if do_write:
            g = ws.get_values(value_render_option='UNFORMATTED_VALUE')
            cA = [r[0] if r else '' for r in g]
            ins = next((i + 1 for i, a in enumerate(cA) if 'comparazione' in norm(a)), len(cA) + 1)
            header, s, e = ins, ins + 1, ins + N + BUF
            ws.insert_rows([[''] for _ in range(1 + N + BUF)], row=ins)

            ab = [{'range': rowcol_to_a1(header, 1), 'values': [['Altro']]}]
            for y, tcol in year_total_col.items():
                months = [colmap[(y, m)] for m in range(1, 13) if (y, m) in colmap]
                tl = col_letter(tcol)
                ab.append({'range': rowcol_to_a1(header, tcol),
                           'values': [["=" + "+".join(f"{col_letter(mc)}{header}" for mc in months)]]})
                ab.append({'range': rowcol_to_a1(header, year_pct_col[y]),
                           'values': [[f"={tl}{header}/${tl}$2"]]})
                for mc in months:
                    cl = col_letter(mc)
                    ab.append({'range': rowcol_to_a1(header, mc), 'values': [[f"=SUM({cl}{s}:{cl}{e})"]]})
            for i, (nsup, (dsp, mesi)) in enumerate(sorted(altro_data.items())):
                rr = header + 1 + i
                ab.append({'range': rowcol_to_a1(rr, 1), 'values': [[dsp]]})
                for (yy, mm), tot in mesi.items():
                    if (yy, mm) in colmap:
                        ab.append({'range': rowcol_to_a1(rr, colmap[(yy, mm)]), 'values': [[round(tot, 2)]]})
            ws.batch_update(ab, value_input_option='USER_ENTERED')
            altro_info = header
        else:
            altro_info = 'dry-run'

    if writes_report:
        pd.DataFrame(writes_report, columns=['Cella', 'Fornitore', 'Anno', 'Mese',
                     'Valore_attuale', 'Aggiunto', 'Nuovo']).to_csv(
            f'_piano_scrittura_{re.sub(r"[^A-Za-z0-9]+", "_", ws.title)}.csv', index=False)

    return {
        'sheet': ws.title, 'blocked': False, 'fatture': len(df),
        'celle': len(writes_report), 'nuovi': len(nuovi_report),
        'formula_fixes': formula_fixes, 'altro': (len(altro_data), altro_info),
        'cat_non_trovate': dict(cat_non_trovate), 'anni_mancanti': sorted(anni_mancanti),
        'writes_report': writes_report[:15],
    }


def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    file_excel, url = sys.argv[1], sys.argv[2]
    do_write = '--write' in sys.argv
    sheet_override = None
    if '--sheet' in sys.argv:
        idx = sys.argv.index('--sheet')
        if idx + 1 < len(sys.argv):
            sheet_override = sys.argv[idx + 1]

    df = pd.read_excel(file_excel)
    df['_anno'] = df['Data emissione'].apply(lambda d: pd.to_datetime(d, dayfirst=True).year)
    anni_serviti = set(df['_anno'].unique())

    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS, scope)
    client = gspread.authorize(creds)
    ss = client.open_by_url(url)

    if sheet_override:
        # Cliente multi-punto-vendita: forza una tab specifica (es. "Economico Store 1"),
        # bypassando la ricerca automatica di "Economico"/"Economico <anno>".
        try:
            ws = ss.worksheet(sheet_override)
        except gspread.exceptions.WorksheetNotFound:
            titoli = [w.title for w in ss.worksheets()]
            print(f"!! Foglio '{sheet_override}' non trovato. Fogli disponibili: {titoli}")
            return
        by_ws, mancanti = {ws.id: (ws, anni_serviti)}, []
    else:
        by_ws, mancanti = resolve_worksheets(ss, anni_serviti)

    print("=" * 66)
    print("SCRITTURA REALE" if do_write else "DRY-RUN (nessuna modifica)")
    print("=" * 66)
    if mancanti:
        print(f"!! ATTENZIONE: nessun foglio 'Economico' ne' 'Economico <anno>' per gli anni {mancanti}")
    if not by_ws:
        print("Nessun foglio Economico trovato. Interrotto.")
        return

    any_blocked = False
    results = []
    for ws_id, (ws, anni) in sorted(by_ws.items(), key=lambda kv: sorted(kv[1][1])):
        sub = df[df['_anno'].isin(anni)].drop(columns='_anno')
        res = process_worksheet(ws, sub, do_write)
        results.append(res)
        if res['blocked']:
            any_blocked = True

    for res in results:
        print(f"\n--- Foglio: {res['sheet']} ({res['fatture']} fatture) ---")
        if res['blocked']:
            print("!! SPAZIO INSUFFICIENTE — nessuna scrittura effettuata su questo foglio.")
            print("   Righe vuote da aggiungere:")
            for r, info in sorted(res['shortfall'].items()):
                print(f"     - {info['cat']}: +{info['need']} righe (inseriscile subito dopo la riga {info['after_row']})")
            continue
        print(f"Celle valore        : {res['celle']}")
        print(f"Nuovi fornitori     : {res['nuovi']}")
        print(f"Formule SUM corrette: {res['formula_fixes']}")
        n_altro, altro_info = res['altro']
        if n_altro:
            if altro_info == 'dry-run':
                print(f"Categoria 'Altro'   : {n_altro} fornitori -> sezione DA CREARE (prima di COMPARAZIONE)")
            else:
                print(f"Categoria 'Altro'   : {n_altro} fornitori -> sezione CREATA a riga {altro_info}")
        if res['cat_non_trovate']:
            print(f"Categorie NON trovate: {res['cat_non_trovate']}")
        if res['anni_mancanti']:
            print(f"!! Anni assenti dal foglio: {res['anni_mancanti']}")
        if res['writes_report']:
            print("--- Esempio celle (prime 15) ---")
            for c_, sup, a, m, vec, ag, nu in res['writes_report']:
                print(f"  {c_:>6} {a}-{m:02d} {sup[:30]:30s} {vec:>9.2f} + {ag:>8.2f} = {nu:>9.2f}")

    print()
    if any_blocked:
        print(">>> BLOCCATO: aggiungi le righe vuote indicate sopra e rilancia.")
    elif do_write:
        print(">>> SCRITTURA COMPLETATA.")
    else:
        print(">>> DRY-RUN. Usa --write per scrivere.")


if __name__ == "__main__":
    main()
