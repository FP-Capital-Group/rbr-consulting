#!/usr/bin/env python3
"""Recapita a Marco su Telegram i report del lunedì non ancora inviati.

La routine cloud scrive ogni report nel tab "Report lunedì" dello Sheet
"RBR - Contributi conoscenza" (colonne: Data, Testo, Inviato). Se dal cloud il curl a
api.telegram.org è bloccato, questo script (eseguito in locale, dove la rete è libera)
manda le righe con Inviato vuoto e le marca "sì <timestamp>".

Uso: invia_report_lunedi.py [--dry-run]
Token bot e chat: ~/.claude/rbr/config.json (installato da /rbr-setup) o env
TELEGRAM_RBR_BOT_TOKEN / TELEGRAM_RBR_CHAT_ID.
"""
import os, sys, json, datetime, urllib.request, urllib.parse

SHEET_NAME = "RBR - Contributi conoscenza"
TAB = "Report lunedì"
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
def _cfg():
    try:
        return json.load(open(os.path.expanduser("~/.claude/rbr/config.json"))).get("telegram", {})
    except Exception:
        return {}
TOKEN = os.environ.get("TELEGRAM_RBR_BOT_TOKEN") or _cfg().get("bot_token", "")
CHAT = os.environ.get("TELEGRAM_RBR_CHAT_ID") or _cfg().get("chat_id_marco", "")


def invia(testo):
    data = urllib.parse.urlencode({"chat_id": CHAT, "text": testo[:4000]}).encode()
    with urllib.request.urlopen(f"https://api.telegram.org/bot{TOKEN}/sendMessage", data, timeout=15) as r:
        return json.load(r).get("ok") is True


def main():
    dry = "--dry-run" in sys.argv
    if not TOKEN or not CHAT:
        sys.exit("❌ token/chat Telegram mancanti: esegui /rbr-setup (installa_chiavi.py)")
    import gspread
    from google.oauth2 import service_account
    creds = service_account.Credentials.from_service_account_file(
        CREDS, scopes=["https://www.googleapis.com/auth/spreadsheets",
                       "https://www.googleapis.com/auth/drive"])
    sh = gspread.authorize(creds).open(SHEET_NAME)
    try:
        ws = sh.worksheet(TAB)
    except gspread.WorksheetNotFound:
        print(f"tab '{TAB}' assente: nessun report in coda")
        return
    righe = ws.get_all_values()
    inviati = 0
    for i, r in enumerate(righe[1:], start=2):
        r = (r + ["", "", ""])[:3]
        if not r[1].strip() or r[2].strip():
            continue
        print(f"→ riga {i} ({r[0]}): {len(r[1])} caratteri")
        if dry:
            continue
        if invia(r[1]):
            ws.update_cell(i, 3, f"sì {datetime.datetime.now():%Y-%m-%d %H:%M}")
            inviati += 1
        else:
            print(f"❌ invio fallito riga {i}")
    print(f"✅ report inviati: {inviati}" if not dry else "(dry-run)")


if __name__ == "__main__":
    main()
