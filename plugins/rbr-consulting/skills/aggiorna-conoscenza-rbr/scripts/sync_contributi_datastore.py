#!/usr/bin/env python3
"""Copia nello Sheet "RBR - Contributi conoscenza" (tab Contributi) i contributi arrivati dal
webhook del plugin e parcheggiati nel Data Store Make "RBR contributi conoscenza" (id 178400).

Perché: i consulenti inviano i contributi senza chiavi (webhook Make); Make non ha ancora una
connessione Google Sheets, quindi il Data Store fa da buffer. Questo script (lato Marco: task
locale del lunedì o routine cloud) sposta le righe nel foglio e marca su_sheet=true.

Token Make API: $MAKE_API_TOKEN → ~/.claude/rbr/config.json (make_api_token) → tools/rbr-chiavi.json (make_api_token).
Service account: ~/.claude/rbr/credentials.json (o $RBR_CREDENTIALS, o tools/rbr-chiavi.json → service_account).
Solo libreria standard. Uso: sync_contributi_datastore.py [--dry-run]
"""
import os, sys, json, time, base64, urllib.request, urllib.parse

DS_ID = os.environ.get("RBR_DATASTORE_ID", "178400")
MAKE = "https://eu1.make.com/api/v2"
SHEET_ID = "1uyeGR-epzvb7JDkomc_XrkaTvoW7gAZFHbGv7JtqdQU"
QUI = os.path.dirname(os.path.abspath(__file__))
PLUGIN = os.path.abspath(os.path.join(QUI, "..", "..", ".."))
SUITE_CHIAVI = os.path.abspath(os.path.join(PLUGIN, "..", "..", "tools", "rbr-chiavi.json"))


def _chiavi():
    try:
        return json.load(open(SUITE_CHIAVI))
    except Exception:
        return {}


def make_token():
    t = os.environ.get("MAKE_API_TOKEN")
    if t:
        return t
    for p in (os.path.expanduser("~/.claude/rbr/config.json"),):
        try:
            t = json.load(open(p)).get("make_api_token")
            if t:
                return t
        except Exception:
            pass
    return _chiavi().get("make_api_token") or sys.exit("❌ token Make API non trovato (MAKE_API_TOKEN / config.json / rbr-chiavi.json)")


def service_account():
    for p in (os.environ.get("RBR_CREDENTIALS"), os.path.expanduser("~/.claude/rbr/credentials.json")):
        if p and os.path.exists(p):
            return json.load(open(p))
    sa = _chiavi().get("service_account")
    return sa or sys.exit("❌ service account non trovato")


def google_token(sa):
    sys.path.insert(0, os.path.join(PLUGIN, "hooks"))
    from rsa_sign import sign
    b64 = lambda b: base64.urlsafe_b64encode(b).rstrip(b"=").decode()
    now = int(time.time())
    h = b64(json.dumps({"alg": "RS256", "typ": "JWT"}).encode())
    c = b64(json.dumps({"iss": sa["client_email"], "scope": "https://www.googleapis.com/auth/spreadsheets",
                        "aud": "https://oauth2.googleapis.com/token", "iat": now, "exp": now + 600}).encode())
    jwt = f"{h}.{c}.{b64(sign(sa['private_key'], f'{h}.{c}'.encode()))}"
    d = urllib.parse.urlencode({"grant_type": "urn:ietf:params:oauth:grant-type:jwt-bearer", "assertion": jwt}).encode()
    return json.load(urllib.request.urlopen("https://oauth2.googleapis.com/token", d, timeout=20))["access_token"]


def make_req(path, method="GET", body=None):
    h = {"Authorization": f"Token {make_token()}", "User-Agent": "rbr-plugin/sync-contributi"}  # UA esplicito: Cloudflare blocca urllib
    if body is not None:
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{MAKE}{path}", json.dumps(body).encode() if body is not None else None, h, method=method)
    with urllib.request.urlopen(req, timeout=30) as r:
        raw = r.read()
        return json.loads(raw) if raw.strip() else {}


def main():
    dry = "--dry-run" in sys.argv
    recs = make_req(f"/data-stores/{DS_ID}/data?pg%5Blimit%5D=100").get("records", [])
    nuovi = [r for r in recs if not (r.get("data") or {}).get("su_sheet")]
    print(f"record nel Data Store: {len(recs)}, da copiare: {len(nuovi)}")
    if not nuovi:
        return
    righe = [[(r["data"].get("data") or ""), r["data"].get("autore", ""), r["data"].get("area", ""),
              r["data"].get("titolo", ""), r["data"].get("contenuto", ""), r["data"].get("stato") or "nuovo"] for r in nuovi]
    if dry:
        for x in righe: print("  [dry-run]", x[:4])
        return
    tok = google_token(service_account())
    rng = urllib.parse.quote("'Contributi'!A:F", safe="")
    req = urllib.request.Request(f"https://sheets.googleapis.com/v4/spreadsheets/{SHEET_ID}/values/{rng}:append?valueInputOption=RAW",
                                 json.dumps({"values": righe}).encode(), {"Authorization": f"Bearer {tok}", "Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=30).read()
    for r in nuovi:
        make_req(f"/data-stores/{DS_ID}/data/{urllib.parse.quote(r['key'], safe='')}", "PATCH", {"su_sheet": True})
    print(f"✅ copiati nello Sheet {len(righe)} contributi: " + "; ".join(f"{x[1]} → {x[3][:40]}" for x in righe))


if __name__ == "__main__":
    main()
