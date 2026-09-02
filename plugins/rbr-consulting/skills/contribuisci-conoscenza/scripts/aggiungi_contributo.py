#!/usr/bin/env python3
"""Aggiunge un contributo al cervello condiviso RBR.

Uso: aggiungi_contributo.py "<autore>" "<area>" "<titolo>" "<contenuto>"

Trova lo Sheet "RBR - Contributi conoscenza" su Drive (service account) e aggiunge
una riga: Data | Autore | Area | Titolo | Contenuto | Stato(=nuovo).
La chiave del service account è in ../../cdg-fatture/scripts/credentials.json.
"""
import os, sys, datetime

try:
    import gspread
    from google.oauth2 import service_account
except ImportError:
    sys.exit("Librerie mancanti: pip3 install gspread google-auth")

SHEET_NAME = "RBR - Contributi conoscenza"
HEADER = ["Data", "Autore", "Area", "Titolo", "Contenuto", "Stato"]
def _creds_path():
    """Chiave service account: $RBR_CREDENTIALS → ~/.claude/rbr/credentials.json (installata
    da /rbr-setup) → copia nel plugin (solo installazioni private/legacy)."""
    for p in (os.environ.get("RBR_CREDENTIALS"),
              os.path.expanduser("~/.claude/rbr/credentials.json"),
              os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "cdg-fatture", "scripts", "credentials.json")):
        if p and os.path.exists(p):
            return p
    return os.path.expanduser("~/.claude/rbr/credentials.json")

CREDS = _creds_path()

def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    autore, area, titolo, contenuto = sys.argv[1:5]
    creds = service_account.Credentials.from_service_account_file(
        CREDS, scopes=["https://www.googleapis.com/auth/spreadsheets",
                       "https://www.googleapis.com/auth/drive"])
    gc = gspread.authorize(creds)
    try:
        sh = gc.open(SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        sys.exit(f"⚠️ Sheet '{SHEET_NAME}' non trovato: chiedi a Marco di crearlo "
                 "nella cartella Drive 'Cervello condiviso - Contributi' e condividerlo "
                 "col service account (di solito eredita dalla cartella).")
    ws = sh.sheet1
    if not ws.get_values("A1:F1"):
        ws.update("A1:F1", [HEADER])
    ws.append_row([datetime.date.today().isoformat(), autore, area, titolo,
                   contenuto, "nuovo"], value_input_option="RAW")
    print("✅ contributo inviato al cervello condiviso")

if __name__ == "__main__":
    main()
