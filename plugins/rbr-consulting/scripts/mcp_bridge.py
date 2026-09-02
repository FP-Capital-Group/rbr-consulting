#!/usr/bin/env python3
"""Ponte stdio ↔ MCP Streamable HTTP per i server RBR con chiave (GHL clienti, Google Ads, Make).

Il plugin pubblico non contiene segreti: il `.mcp.json` dichiara ogni server come
`python3 mcp_bridge.py <nome>` e questo script, all'avvio della sessione, legge URL e header
(con le chiavi) da ~/.claude/rbr/mcp_servers.json, scritto da /rbr-setup (installa_chiavi.py).
Funziona ovunque il plugin giri sul Mac del consulente: Cowork (sessione locale) e Claude Code.
Solo libreria standard: niente Node, niente pacchetti da installare.

Protocollo: ogni messaggio JSON-RPC letto da stdin viene inviato in POST all'endpoint; la
risposta (JSON o flusso SSE) viene riscritta su stdout una riga per messaggio. L'header
Mcp-Session-Id restituito dall'initialize viene riusato nelle richieste successive.
"""
import os, sys, json, threading, urllib.request, urllib.error

NOME = sys.argv[1] if len(sys.argv) > 1 else ""
CFG = os.environ.get("RBR_MCP_SERVERS") or os.path.expanduser("~/.claude/rbr/mcp_servers.json")
_lock = threading.Lock()
_sessione = {"id": None}


def log(msg):
    sys.stderr.write(f"[mcp_bridge {NOME}] {msg}\n"); sys.stderr.flush()


def invia(obj):
    with _lock:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n"); sys.stdout.flush()


def emetti(obj):
    for o in (obj if isinstance(obj, list) else [obj]):
        if isinstance(o, dict):
            invia(o)


def leggi_sse(resp):
    dati = []
    for raw in resp:
        line = raw.decode("utf-8", "replace").rstrip("\r\n")
        if line.startswith("data:"):
            dati.append(line[5:].lstrip())
        elif line == "" and dati:
            try:
                emetti(json.loads("\n".join(dati)))
            except ValueError:
                pass
            dati = []
    if dati:
        try:
            emetti(json.loads("\n".join(dati)))
        except ValueError:
            pass


def post(url, headers, msg):
    body = json.dumps(msg).encode()
    # User-Agent esplicito: Cloudflare (GHL, Make) blocca quello di default di urllib (errore 1010)
    h = {"Content-Type": "application/json", "Accept": "application/json, text/event-stream",
         "User-Agent": "rbr-mcp-bridge/1.0 (Claude plugin rbr-consulting)", **headers}
    if _sessione["id"]:
        h["Mcp-Session-Id"] = _sessione["id"]
    req = urllib.request.Request(url, body, h, method="POST")
    ha_id = isinstance(msg, dict) and msg.get("id") is not None
    try:
        with urllib.request.urlopen(req, timeout=180) as r:
            sid = r.headers.get("Mcp-Session-Id")
            if sid:
                _sessione["id"] = sid
            ct = (r.headers.get("Content-Type") or "").lower()
            if r.status == 202:
                return
            if "text/event-stream" in ct:
                leggi_sse(r)
            else:
                raw = r.read()
                if raw.strip():
                    emetti(json.loads(raw))
    except urllib.error.HTTPError as e:
        dettaglio = e.read()[:400].decode("utf-8", "replace")
        log(f"HTTP {e.code}: {dettaglio}")
        if ha_id:
            invia({"jsonrpc": "2.0", "id": msg["id"],
                   "error": {"code": -32000, "message": f"{NOME}: HTTP {e.code} — {dettaglio}"}})
    except Exception as e:
        log(f"errore: {e}")
        if ha_id:
            invia({"jsonrpc": "2.0", "id": msg["id"], "error": {"code": -32000, "message": f"{NOME}: {e}"}})


def main():
    if not NOME:
        sys.exit("uso: mcp_bridge.py <nome-server>")
    if not os.path.exists(CFG):
        sys.exit(f"chiavi RBR non installate ({CFG}): lancia /rbr-setup e riapri la chat")
    conf = json.load(open(CFG)).get(NOME)
    if not conf or not conf.get("url"):
        sys.exit(f"server '{NOME}' assente da {CFG}: rilancia /rbr-setup (chiavi aggiornate)")
    url, headers = conf["url"], dict(conf.get("headers") or {})
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            continue
        threading.Thread(target=post, args=(url, headers, msg), daemon=True).start()


if __name__ == "__main__":
    main()
