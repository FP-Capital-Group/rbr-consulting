#!/usr/bin/env python3
"""Condivide una skill/comando locale col team RBR (cervello condiviso).

Uso: condividi_skill.py "<autore>" <path skill (cartella con SKILL.md) o file .md> [--nota "..."] [--dry-run]

Esporta i file testuali della skill come righe nello Sheet "RBR - Contributi conoscenza"
(tab Contributi): Area = `skill-nuova:<nome>`, Titolo = percorso relativo del file,
Contenuto = testo. La routine del lunedì ricostruisce la skill in
`plugins/rbr-consulting/skills/<nome>/` e la distribuisce a tutti.

Sicurezza: salta credentials.json/.env/chiavi e i binari; oscura token/chiavi nel testo
(<REDATTO>); sostituisce i path /Users/<nome>/ con ~/. File > 45.000 caratteri divisi
in parti. Con --dry-run mostra cosa verrebbe inviato senza scrivere.
"""
import os, re, sys, datetime, argparse

SHEET_NAME = "RBR - Contributi conoscenza"
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
TEXT_EXT = {".md", ".py", ".js", ".ts", ".json", ".txt", ".yaml", ".yml", ".html",
            ".css", ".csv", ".sh", ".toml", ".jinja", ".j2", ".sql"}
SKIP_FILES = {"credentials.json", ".env", "token.json", "package-lock.json"}
MAX_CELL = 45_000
RE_SECRET = re.compile(
    r"(sk-ant-[A-Za-z0-9_-]{10,}|pit-[0-9a-f-]{20,}|AIza[0-9A-Za-z_-]{20,}|"
    r"\b\d{9,10}:[A-Za-z0-9_-]{30,}\b|(?<=Bearer\s)[A-Za-z0-9._-]{20,}|"
    r"pk_[A-Za-z0-9]{20,}|xox[bap]-[A-Za-z0-9-]{10,})")
RE_KV_SECRET = re.compile(r"(?i)((?:api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?)([A-Za-z0-9_\-]{16,})")


def pulisci(txt):
    txt = RE_SECRET.sub("<REDATTO>", txt)
    txt = RE_KV_SECRET.sub(lambda m: m.group(1) + "<REDATTO>", txt)
    txt = re.sub(r"/Users/[^/\s'\"]+/", "~/", txt)
    return txt


def raccogli(path):
    """[(titolo, contenuto)] dei file testuali della skill."""
    voci = []
    if os.path.isfile(path):
        voci.append((os.path.basename(path), open(path, encoding="utf-8", errors="ignore").read()))
        return voci
    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ("node_modules", "__pycache__", ".git", "dist")]
        for fn in sorted(files):
            if fn in SKIP_FILES or fn.endswith((".pem", ".key", ".DS_Store")):
                continue
            if os.path.splitext(fn)[1].lower() not in TEXT_EXT:
                continue
            p = os.path.join(root, fn)
            if os.path.getsize(p) > 400_000:
                continue
            voci.append((os.path.relpath(p, path), open(p, encoding="utf-8", errors="ignore").read()))
    # SKILL.md sempre per primo
    voci.sort(key=lambda v: (v[0] != "SKILL.md", v[0]))
    return voci


def spezza(titolo, testo):
    if len(testo) <= MAX_CELL:
        return [(titolo, testo)]
    parti = [testo[i:i + MAX_CELL] for i in range(0, len(testo), MAX_CELL)]
    return [(f"{titolo} (parte {i}/{len(parti)})", p) for i, p in enumerate(parti, 1)]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("autore")
    ap.add_argument("path")
    ap.add_argument("--nota", default="", help="contesto per il team (quando usarla, perché è utile)")
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()
    path = os.path.abspath(os.path.expanduser(a.path.rstrip("/")))
    if not os.path.exists(path):
        sys.exit(f"❌ path non trovato: {path}")
    nome = os.path.basename(path).replace(".md", "")
    nome = re.sub(r"[^a-z0-9-]", "-", nome.lower()).strip("-")
    voci = raccogli(path)
    if not voci:
        sys.exit("❌ nessun file testuale da condividere")
    righe = []
    oggi = datetime.date.today().isoformat()
    area = f"skill-nuova:{nome}"
    if a.nota:
        righe.append([oggi, a.autore, area, "_nota", a.nota, "nuovo"])
    for titolo, testo in voci:
        for t, parte in spezza(titolo, pulisci(testo)):
            righe.append([oggi, a.autore, area, t, parte, "nuovo"])
    tot = sum(len(r[4]) for r in righe)
    print(f"Skill `{nome}` → {len(righe)} righe, {tot:,} caratteri:")
    for r in righe:
        print(f"  - {r[3]} ({len(r[4]):,} car.)")
    if a.dry_run:
        print("(dry-run: nulla inviato)")
        return
    try:
        import gspread
        from google.oauth2 import service_account
    except ImportError:
        sys.exit("Librerie mancanti: pip3 install gspread google-auth")
    creds = service_account.Credentials.from_service_account_file(
        CREDS, scopes=["https://www.googleapis.com/auth/spreadsheets",
                       "https://www.googleapis.com/auth/drive"])
    gc = gspread.authorize(creds)
    try:
        sh = gc.open(SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        sys.exit(f"⚠️ Sheet '{SHEET_NAME}' non trovato: avvisa Marco.")
    ws = sh.sheet1
    ws.append_rows(righe, value_input_option="RAW")
    print(f"✅ skill `{nome}` condivisa col team ({len(righe)} righe). "
          "Sarà nel plugin di tutti dal prossimo aggiornamento del lunedì.")


if __name__ == "__main__":
    main()
