#!/usr/bin/env python3
"""Aggiunge un contributo allo Sheet "RBR - Contributi conoscenza" (Marco lo legge ogni settimana).

Uso: aggiungi_contributo.py "<autore>" "<area>" "<titolo>" "<contenuto>"

Canale 1 (default, nessuna chiave sul Mac): webhook Make → riga nello Sheet. Funziona appena
installato il plugin, anche senza /rbr-setup, su Mac e Windows (solo libreria standard).
Canale 2 (fallback): service account in ~/.claude/rbr/credentials.json + gspread.
Canale 3 (fallback): file locale ~/.claude/rbr-cache/contributi_da_inviare.jsonl da mandare a Marco.
Riga scritta: Data | Autore | Area | Titolo | Contenuto | Stato(=nuovo).
"""
import os, sys, json, datetime, urllib.request

WEBHOOK = os.environ.get("RBR_CONTRIBUTI_WEBHOOK", "https://hook.eu1.make.com/2nbvlxprrsfkmgt5g43y1wxkn6hktxet")
SHEET_NAME = "RBR - Contributi conoscenza"
HEADER = ["Data", "Autore", "Area", "Titolo", "Contenuto", "Stato"]


def via_webhook(riga):
    body = json.dumps(dict(zip(["data", "autore", "area", "titolo", "contenuto", "stato"], riga)),
                      ensure_ascii=False).encode("utf-8")
    req = urllib.request.Request(WEBHOOK, body, {"Content-Type": "application/json",
                                                 "User-Agent": "rbr-plugin/contribuisci-conoscenza"})
    with urllib.request.urlopen(req, timeout=20) as r:
        risposta = r.read().decode("utf-8", "replace")
    if r.status != 200 or "Accepted" not in risposta and "ok" not in risposta.lower():
        raise RuntimeError(f"webhook: {r.status} {risposta[:120]}")


def via_service_account(riga):
    import gspread
    from google.oauth2 import service_account
    for p in (os.environ.get("RBR_CREDENTIALS"), os.path.expanduser("~/.claude/rbr/credentials.json")):
        if p and os.path.exists(p):
            creds_path = p; break
    else:
        raise FileNotFoundError("nessuna chiave service account (serve /rbr-setup)")
    creds = service_account.Credentials.from_service_account_file(
        creds_path, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
    sh = gspread.authorize(creds).open(SHEET_NAME)
    ws = sh.sheet1
    if not ws.get_values("A1:F1"):
        ws.update("A1:F1", [HEADER])
    ws.append_row(riga, value_input_option="RAW")


def backup_locale(riga):
    d = os.path.expanduser("~/.claude/rbr-cache"); os.makedirs(d, exist_ok=True)
    p = os.path.join(d, "contributi_da_inviare.jsonl")
    with open(p, "a", encoding="utf-8") as f:
        f.write(json.dumps(dict(zip(HEADER, riga)), ensure_ascii=False) + "\n")
    return p


def main():
    if len(sys.argv) != 5:
        sys.exit(__doc__)
    autore, area, titolo, contenuto = sys.argv[1:5]
    riga = [datetime.date.today().isoformat(), autore, area, titolo, contenuto, "nuovo"]
    errori = []
    try:
        via_webhook(riga); print("✅ contributo inviato (Marco lo legge nel digest settimanale)"); return
    except Exception as e:
        errori.append(f"webhook: {e}")
    try:
        via_service_account(riga); print("✅ contributo inviato via service account"); return
    except Exception as e:
        errori.append(f"service account: {e}")
    p = backup_locale(riga)
    print("⚠️ contributo NON inviato (" + "; ".join(errori) + f").\n   Salvato in {p}: mandalo a Marco o riprova più tardi.")
    sys.exit(1)


if __name__ == "__main__":
    main()
