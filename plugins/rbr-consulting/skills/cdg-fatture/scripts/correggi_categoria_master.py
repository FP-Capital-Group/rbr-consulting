#!/usr/bin/env python3
"""
Corregge la Categoria di un fornitore nel master condiviso (Google Sheet).

Uso:
  python3 correggi_categoria_master.py "<Denominazione Fornitore>" "<Nuova Categoria>"

Esempio:
  python3 correggi_categoria_master.py "START SRL" "Servizi"

Il match sul nome fornitore è normalizzato (case-insensitive, spazi multipli collassati),
quindi non serve scrivere la ragione sociale esattamente come appare nel foglio.
"""
import os
import sys

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get('CDG_HOME') or BASE)
import master_sheet as ms


def main():
    if len(sys.argv) != 3:
        print('Uso: python3 correggi_categoria_master.py "<Denominazione Fornitore>" "<Nuova Categoria>"')
        sys.exit(1)

    fornitore, nuova_categoria = sys.argv[1], sys.argv[2].strip()

    if ms.norm(nuova_categoria) not in ms.CATEGORIE_VALIDE:
        print(f"!! Attenzione: '{nuova_categoria}' non è una delle categorie standard "
              f"(FORNITORI, Servizi, Utenze, Piattaforme Delivery, Pubblicità - Marketing, "
              f"Provvigioni, Materiali di consumo, Viaggi e trasferte). Procedo comunque, "
              f"ma verifica che non sia un refuso.")

    esito = ms.update_categoria(fornitore, nuova_categoria)

    if not esito['aggiornati']:
        print(f"!! Nessun fornitore trovato nel master corrispondente a '{fornitore}'.")
        if esito['simili']:
            print("   Nomi simili presenti nel master:")
            for s in esito['simili']:
                print(f"   - {s}")
        sys.exit(1)

    vecchie_categorie = sorted({c for _, c in esito['aggiornati']})
    print(f"Aggiornato: {len(esito['aggiornati'])} riga/righe -> '{nuova_categoria}' "
          f"(prima: {', '.join(vecchie_categorie)})")
    for nome, _ in esito['aggiornati']:
        print(f"   - {nome}")


if __name__ == "__main__":
    main()
