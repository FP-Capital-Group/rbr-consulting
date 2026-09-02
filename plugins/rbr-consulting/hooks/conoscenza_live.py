#!/usr/bin/env python3
"""Hook SessionStart: inietta le ultime novità del cervello condiviso RBR.

Legge il tab "Conoscenza live" dello Sheet "RBR - Contributi conoscenza" via service
account (solo stdlib + openssl: nessuna libreria da installare), con cache locale di
12 ore in ~/.claude/rbr-cache/. Stampa le ultime 12 novità e avvisa se esiste una
versione del plugin più recente di quella installata. Qualsiasi errore → silenzio
(o cache vecchia): la sessione non deve mai rompersi per questo hook.
"""
import os, re, sys, json, time, base64, urllib.request, urllib.parse
try:
    sys.stdout.reconfigure(encoding="utf-8")  # Windows: console cp1252 romperebbe accenti/emoji
except Exception:
    pass

SHEET_ID = os.environ.get("RBR_SHEET_ID", "1uyeGR-epzvb7JDkomc_XrkaTvoW7gAZFHbGv7JtqdQU")
TAB = "Conoscenza live"
N_RIGHE = 12
TTL = 12 * 3600
ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
def _creds_path():
    """Chiave service account: $RBR_CREDENTIALS → ~/.claude/rbr/credentials.json (installata
    da /rbr-setup) → copia nel plugin (solo installazioni private/legacy)."""
    for p in (os.environ.get("RBR_CREDENTIALS"),
              os.path.expanduser("~/.claude/rbr/credentials.json"),
              os.path.join(ROOT, "skills", "cdg-fatture", "scripts", "credentials.json")):
        if p and os.path.exists(p):
            return p
    return os.path.expanduser("~/.claude/rbr/credentials.json")


CREDS = _creds_path()
CACHE_DIR = os.path.join(os.path.expanduser("~"), ".claude", "rbr-cache")
CACHE = os.path.join(CACHE_DIR, "conoscenza_live.md")


def b64(b):
    return base64.urlsafe_b64encode(b).rstrip(b"=").decode()


def token():
    sa = json.load(open(CREDS))
    now = int(time.time())
    header = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    claim = b64(json.dumps({
        "iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/spreadsheets.readonly",
        "aud": "https://oauth2.googleapis.com/token", "iat": now, "exp": now + 600}).encode())
    msg = f"{header}.{claim}".encode()
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    from rsa_sign import sign  # openssl se c'è, altrimenti RSA in puro Python (Windows)
    sig = sign(sa["private_key"], msg)
    jwt = f"{header}.{claim}.{b64(sig)}"
    data = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer",
                                   "assertion": jwt}).encode()
    with urllib.request.urlopen("https://oauth2.googleapis.com/token", data, timeout=8) as r:
        return json.load(r)["access_token"]


def righe():
    rng = urllib.parse.quote(f"'{TAB}'!A:E", safe="")
    url = f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{rng}"
    req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token()}"})
    with urllib.request.urlopen(req, timeout=8) as r:
        return json.load(r).get("values", [])


def versione_installata():
    try:
        return json.load(open(os.path.join(ROOT, ".claude-plugin", "plugin.json")))["version"]
    except Exception:
        return None


def semver(v):
    try:
        return tuple(int(x) for x in str(v).strip().lstrip("v").split("."))
    except Exception:
        return (0,)


def componi(vals):
    dati = [r for r in vals[1:] if r and any(c.strip() for c in r)] if vals else []
    ultime = dati[-N_RIGHE:][::-1]
    out = [f"# Conoscenza live RBR — ultime novità del team (aggiornato {time.strftime('%Y-%m-%d %H:%M')})",
           "Novità e procedure fuse nel cervello condiviso dopo la tua versione del plugin. "
           "Applicale come se fossero nelle skill."]
    for r in ultime:
        r = (r + [""] * 5)[:5]
        data, area, testo, rif, ver = (c.strip() for c in r)
        riga = f"- {data} [{area}] {testo}"
        if rif:
            riga += f" → {rif}"
        if ver:
            riga += f" (v{ver.lstrip('v')})"
        out.append(riga)
    inst = versione_installata()
    ultima = max((semver(r[4]) for r in dati if len(r) > 4 and r[4].strip()), default=None)
    if inst and ultima and ultima > semver(inst):
        out.append(f"\n⚠️ Plugin installato v{inst}, disponibile v{'.'.join(map(str, ultima))}: "
                   "l'auto-update del plugin la installa da solo: sarà attiva dalla prossima chat. "
                   "Prima esporta ciò che hai imparato (skill contribuisci-conoscenza).")
    return "\n".join(out) + "\n"


def novita_versione():
    """Alla PRIMA sessione di una versione nuova stampa la sezione del CHANGELOG."""
    try:
        inst = versione_installata()
        if not inst:
            return ""
        marker = os.path.join(CACHE_DIR, "ultima_versione_vista")
        vista = open(marker).read().strip() if os.path.exists(marker) else ""
        if vista == inst:
            return ""
        os.makedirs(CACHE_DIR, exist_ok=True)
        open(marker, "w").write(inst)
        if not vista:
            return ""  # prima installazione: niente annuncio
        ch = os.path.join(ROOT, "CHANGELOG.md")
        sez = ""
        if os.path.exists(ch):
            txt = open(ch, encoding="utf-8").read()
            m = re.search(r"^## v" + re.escape(inst) + r"[^\n]*\n(.*?)(?=^## |\Z)", txt, re.M | re.S)
            sez = m.group(1).strip() if m else ""
        out = [f"\n🆕 Plugin RBR aggiornato: v{vista} → v{inst}. Novità di questa versione:"]
        out.append(sez or "- (vedi CHANGELOG.md del plugin)")
        out.append("Di' al consulente, all'inizio della chat, in 2 righe cosa è cambiato e che può "
                   "chiedere «cosa c'è di nuovo nel plugin» per il dettaglio.")
        return "\n".join(out) + "\n"
    except Exception:
        return ""


def main():
    try:
        sys.stdout.write(novita_versione())
        if os.path.exists(CACHE) and time.time() - os.path.getmtime(CACHE) < TTL:
            sys.stdout.write(open(CACHE, encoding="utf-8").read())
            return
        testo = componi(righe())
        os.makedirs(CACHE_DIR, exist_ok=True)
        with open(CACHE, "w", encoding="utf-8") as f:
            f.write(testo)
        sys.stdout.write(testo)
    except Exception:
        if os.path.exists(CACHE):
            try:
                sys.stdout.write(open(CACHE, encoding="utf-8").read())
            except Exception:
                pass


if __name__ == "__main__":
    main()
