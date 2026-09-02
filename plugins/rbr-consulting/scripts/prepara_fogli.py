#!/usr/bin/env python3
"""Prepara e verifica l'accesso ai fogli Google dei clienti (il cuore del lavoro RBR: CDG, fatture, KPI).

Uso: prepara_fogli.py [--test-url <url o id di un foglio cliente>]
Fa, in ordine, senza chiedere nulla:
  1. installa le librerie Python che mancano (gspread, google-auth, oauth2client, pandas, openpyxl)
     con `python -m pip install --user` (Mac e Windows)
  2. verifica che ~/.claude/rbr/credentials.json esista (la installa /rbr-setup dal file chiavi)
  3. prova reale: apre lo Sheet "RBR - Contributi conoscenza" con il service account e legge il tab Contributi
  4. (--test-url) apre anche il foglio del cliente indicato: se fallisce con 403 stampa l'email del
     service account da aggiungere come Editor
Esce con 0 se tutto ok, 1 se qualcosa manca (dice cosa).
"""
import os, sys, json, subprocess, importlib

LIBS = {"gspread": "gspread", "google.oauth2": "google-auth", "oauth2client": "oauth2client",
        "pandas": "pandas", "openpyxl": "openpyxl"}
CREDS = os.environ.get("RBR_CREDENTIALS") or os.path.expanduser("~/.claude/rbr/credentials.json")
SHEET_ID = "1uyeGR-epzvb7JDkomc_XrkaTvoW7gAZFHbGv7JtqdQU"


def passo(n, msg):
    print(f"{n}. {msg}")


def main():
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import rbr_chiavi
        rbr_chiavi.installa_se_serve()
    except Exception:
        pass
    ok = True
    mancanti = []
    for mod, pkg in LIBS.items():
        try:
            importlib.import_module(mod)
        except Exception:
            mancanti.append(pkg)
    if mancanti:
        passo(1, f"installo librerie mancanti: {', '.join(mancanti)}")
        r = subprocess.run([sys.executable, "-m", "pip", "install", "--user", "--quiet", "--disable-pip-version-check", *mancanti],
                           capture_output=True, text=True)
        if r.returncode != 0:
            r = subprocess.run([sys.executable, "-m", "pip", "install", "--quiet", "--disable-pip-version-check", *mancanti],
                               capture_output=True, text=True)
        if r.returncode != 0:
            print("   ❌ pip non è riuscito:", (r.stderr or r.stdout).strip()[-400:])
            print("   → prova a mano: python3 -m pip install --user " + " ".join(mancanti))
            ok = False
        else:
            print("   ✅ installate")
    else:
        passo(1, "✅ librerie Python presenti (gspread, google-auth, pandas, openpyxl)")

    if not os.path.exists(CREDS):
        passo(2, f"❌ manca {CREDS}: le chiavi non sono installate → /rbr-setup punto 0 (file rbr-chiavi.json dal Drive)")
        return 1
    sa = json.load(open(CREDS))
    passo(2, f"✅ service account: {sa.get('client_email')}")
    if not ok:
        return 1

    try:
        import gspread
        from google.oauth2 import service_account
        creds = service_account.Credentials.from_service_account_file(
            CREDS, scopes=["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"])
        gc = gspread.authorize(creds)
        sh = gc.open_by_key(SHEET_ID)
        n = len(sh.worksheet("Contributi").get_all_values())
        passo(3, f"✅ lettura reale ok: «{sh.title}», tab Contributi, {n} righe")
    except Exception as e:
        passo(3, f"❌ accesso ai fogli fallito: {type(e).__name__}: {str(e)[:200]}")
        print("   → se è un errore di rete/403 sul sandbox: chat nuova dopo il setup; se è di chiavi: rifai il punto 0")
        return 1

    if "--test-url" in sys.argv:
        url = sys.argv[sys.argv.index("--test-url") + 1]
        try:
            shc = gc.open_by_url(url) if url.startswith("http") else gc.open_by_key(url)
            passo(4, f"✅ foglio cliente «{shc.title}»: {len(shc.worksheets())} tab")
        except Exception as e:
            passo(4, f"❌ foglio cliente non accessibile ({type(e).__name__}). Condividilo come Editor con: {sa.get('client_email')}")
            return 1
    print(f"\n✅ Fogli Google pronti. Regola: ogni foglio cliente va condiviso come Editor con {sa.get('client_email')}")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    sys.exit(main())
