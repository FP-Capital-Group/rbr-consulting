#!/usr/bin/env python3
"""
Step 1 della skill analisi-acquisti-fornitore.

Scansiona una cartella di fatture elettroniche (.xml e/o .p7m, esclude i
*_metaDato.xml) e raggruppa i documenti per fornitore REALE, leggendo
CedentePrestatore/IdCodice + Denominazione dal contenuto di OGNI file — mai
dal nome del file (il prefisso del filename è spesso l'IdentificativoTrasmittente
di un intermediario SDI condiviso da fornitori completamente diversi, non il
fornitore stesso: in cartelle con più mittenti raggruppare per nome file dà
risultati sbagliati).

Uso:
    python3 estrai_fornitori.py "<cartella fatture>" [--json output.json]

Stampa una tabella ordinata per numero di documenti (i fornitori più
rilevanti in alto) con P.IVA, denominazione, conteggio documenti e periodo
coperto. Mostra questa tabella all'utente PRIMA di procedere: se compaiono
nomi simili/ambigui (es. due entità che sembrano lo stesso fornitore, o un
nome generico che potrebbe indicare più aziende), chiedi conferma con
AskUserQuestion su quali P.IVA includere — non indovinare.
"""
import argparse
import json
import os
import sys
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from fatture_lib import parse_invoice, mese_label  # noqa: E402


def scan_folder(folder):
    files = [
        f for f in os.listdir(folder)
        if not f.endswith('_metaDato.xml') and (f.endswith('.xml') or f.endswith('.p7m'))
    ]
    gruppi = defaultdict(lambda: {'denominazioni': defaultdict(int), 'documenti': []})
    errori = []
    for f in files:
        path = os.path.join(folder, f)
        d = parse_invoice(path)
        if not d or not d['piva_cedente']:
            errori.append(f)
            continue
        key = d['piva_cedente']
        gruppi[key]['denominazioni'][d['denominazione_cedente']] += 1
        gruppi[key]['documenti'].append({
            'file': f, 'data': d['data'], 'tipo_doc': d['tipo_doc'], 'numero': d['numero'],
        })
    return gruppi, errori


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cartella')
    ap.add_argument('--json', help='Salva anche un JSON dettagliato (piva -> lista file) in questo path')
    args = ap.parse_args()

    gruppi, errori = scan_folder(args.cartella)

    righe = []
    for piva, info in gruppi.items():
        denom = max(info['denominazioni'].items(), key=lambda kv: kv[1])[0] or '(denominazione non letta)'
        docs = info['documenti']
        date = sorted(d['data'] for d in docs if d['data'])
        righe.append({
            'piva': piva,
            'denominazione': denom,
            'n_documenti': len(docs),
            'periodo': f"{mese_label(date[0])} — {mese_label(date[-1])}" if date else '?',
            'tipi_doc': sorted(set(d['tipo_doc'] for d in docs if d['tipo_doc'])),
        })
    righe.sort(key=lambda r: -r['n_documenti'])

    print(f"\n{len(righe)} fornitori distinti trovati in {args.cartella}\n")
    print(f"{'N.doc':>6}  {'P.IVA':<13}  {'Periodo':<20}  Denominazione")
    print('-' * 90)
    for r in righe:
        print(f"{r['n_documenti']:>6}  {r['piva']:<13}  {r['periodo']:<20}  {r['denominazione']}")

    if errori:
        print(f"\n⚠️  {len(errori)} file non leggibili (P.IVA non estratto) — controllali a mano:")
        for e in errori[:20]:
            print(f"   {e}")
        if len(errori) > 20:
            print(f"   ... e altri {len(errori) - 20}")

    if args.json:
        out = {}
        for piva, info in gruppi.items():
            out[piva] = [d['file'] for d in info['documenti']]
        with open(args.json, 'w') as fh:
            json.dump(out, fh, indent=2, ensure_ascii=False)
        print(f"\nDettaglio file per P.IVA salvato in {args.json}")


if __name__ == '__main__':
    main()
