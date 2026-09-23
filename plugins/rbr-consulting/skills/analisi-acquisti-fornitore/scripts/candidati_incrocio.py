#!/usr/bin/env python3
"""
Step 5 della skill analisi-acquisti-fornitore (solo con più fornitori nello
stesso batch).

Confronta i fogli "Articoli" di più workbook già costruiti e segnala
CANDIDATI prodotti uguali/comparabili acquistati da più di un fornitore.
È solo un aiuto per non doverli cercare a occhio in centinaia di righe: le
uscite sono candidati da verificare, non certezze — un match testuale alto
tra "OLIO DI OLIVA" e "FILETTI ACCIUGHE...OLIO OLIVA" è quasi sempre un falso
positivo (parole in comune ma prodotti diversi), mentre un match più basso
tra "Zucchine a fette grigliate" e "GIAS ZUCCHINE FETTE GRIGLIATE" è quasi
sempre vero. Guarda SEMPRE la descrizione intera e il buonsenso, non solo lo
score, prima di includere una coppia nel foglio "Confronto Fornitori" finale.

Uso:
    python3 candidati_incrocio.py Analisi_Acquisti_A.xlsx Analisi_Acquisti_B.xlsx [...]
"""
import argparse
import re
import sys
from difflib import SequenceMatcher

from openpyxl import load_workbook


def norm(s):
    s = s.upper()
    s = re.sub(r'[^A-Z0-9 ]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def read_articoli(path):
    wb = load_workbook(path, data_only=True)
    ws = wb['Articoli']
    # il nome fornitore è nella riga 3 del foglio Riepilogo Fornitore
    riepilogo = wb['Riepilogo Fornitore']
    fornitore = None
    for row in riepilogo.iter_rows(min_row=1, max_row=6, values_only=True):
        for v in row:
            if v and '—' in str(v) and 'P.IVA' in str(v):
                fornitore = str(v).split('—')[0].strip()
    headers = [c.value for c in ws[1]]
    idx = {h: i for i, h in enumerate(headers)}
    out = []
    for row in ws.iter_rows(min_row=2, values_only=True):
        if row[idx['Descrizione articolo']] is None:
            continue
        out.append({
            'fornitore': fornitore or path, 'codice': row[idx['Codice']],
            'descrizione': row[idx['Descrizione articolo']], 'um': row[idx['UM']],
            'prezzo': row[idx['PREZZO MEDIO NETTO']], 'importo': row[idx['Importo acquisti €']],
        })
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('xlsx', nargs='+')
    ap.add_argument('--soglia', type=float, default=0.55)
    args = ap.parse_args()

    if len(args.xlsx) < 2:
        print("Servono almeno 2 file per cercare incroci tra fornitori", file=sys.stderr)
        sys.exit(1)

    tutti = []
    for path in args.xlsx:
        tutti.extend(read_articoli(path))
    print(f"Articoli totali tra {len(args.xlsx)} fornitori: {len(tutti)}\n")

    trovati = []
    for i in range(len(tutti)):
        for j in range(i + 1, len(tutti)):
            a, b = tutti[i], tutti[j]
            if a['fornitore'] == b['fornitore']:
                continue
            na, nb = norm(a['descrizione']), norm(b['descrizione'])
            ratio = SequenceMatcher(None, na, nb).ratio()
            set_a = {w for w in na.split() if len(w) > 3}
            set_b = {w for w in nb.split() if len(w) > 3}
            common = set_a & set_b
            if ratio > args.soglia or len(common) >= 2:
                trovati.append((ratio, a, b))

    trovati.sort(key=lambda x: -x[0])
    seen = set()
    for ratio, a, b in trovati:
        key = tuple(sorted([a['fornitore'] + a['descrizione'], b['fornitore'] + b['descrizione']]))
        if key in seen:
            continue
        seen.add(key)
        print(f"{ratio:.2f} | {a['fornitore'][:22]:22s} {a['descrizione'][:42]:42s} {a['prezzo']:>8} {a['um'] or '':3s} | "
              f"{b['fornitore'][:22]:22s} {b['descrizione'][:42]:42s} {b['prezzo']:>8} {b['um'] or '':3s}")

    if not trovati:
        print("Nessun candidato trovato — nessun prodotto sembra in comune tra i fornitori analizzati.")


if __name__ == '__main__':
    main()
