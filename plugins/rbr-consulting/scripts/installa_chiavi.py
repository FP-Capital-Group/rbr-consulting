#!/usr/bin/env python3
"""Installa le chiavi RBR sul Mac del consulente (una volta sola, da /rbr-setup).

Il plugin pubblico NON contiene segreti. Le chiavi arrivano in un file `rbr-chiavi.json`
che Marco condivide in privato (cartella Drive "RBR - Chiavi consulenti"). Questo script:
  1. salva il service account Google in   ~/.claude/rbr/credentials.json
  2. salva token Telegram e altre config in ~/.claude/rbr/config.json
  3. registra i server MCP con chiave (GHL clienti, Google Ads, Make) in ~/.claude.json
     (scope utente: valgono in Claude Code e nelle sessioni locali Cowork)
  4. aggiunge i domini necessari all'allowlist di rete del sandbox (~/.claude/settings.json)
  5. registra il marketplace pubblico con auto-update attivo (~/.claude/settings.json)

Uso: installa_chiavi.py <percorso rbr-chiavi.json> [--dry-run]
Idempotente: rieseguirlo aggiorna senza duplicare. Fa backup dei file toccati (.bak-<ts>).
"""
import os, sys, json, time, shutil

HOME = os.path.expanduser("~")
RBR_DIR = os.path.join(HOME, ".claude", "rbr")
CLAUDE_JSON = os.path.join(HOME, ".claude.json")
SETTINGS = os.path.join(HOME, ".claude", "settings.json")
MARKETPLACE_URL = "https://github.com/marcocuccaro0309/rbr-consulting"
DOMINI = ["oauth2.googleapis.com", "www.googleapis.com", "sheets.googleapis.com",
          "drive.googleapis.com", "api.telegram.org", "services.leadconnectorhq.com",
          "eu1.make.com", "raw.githubusercontent.com", "github.com"]


def carica_json(p):
    if os.path.exists(p):
        with open(p, encoding="utf-8") as f:
            return json.load(f)
    return {}


def salva_json(p, data, dry):
    if dry:
        print(f"  [dry-run] scriverei {p}")
        return
    os.makedirs(os.path.dirname(p), exist_ok=True)
    if os.path.exists(p):
        shutil.copy2(p, f"{p}.bak-{int(time.time())}")
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    os.chmod(p, 0o600)
    print(f"  ✅ {p}")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    dry = "--dry-run" in sys.argv
    if not args:
        sys.exit(__doc__)
    src = os.path.expanduser(args[0])
    if not os.path.exists(src):
        sys.exit(f"❌ file chiavi non trovato: {src}")
    chiavi = carica_json(src)
    for k in ("service_account", "telegram", "mcp_servers"):
        if k not in chiavi:
            sys.exit(f"❌ file chiavi incompleto: manca '{k}'")

    print("1. Service account Google")
    salva_json(os.path.join(RBR_DIR, "credentials.json"), chiavi["service_account"], dry)

    print("2. Config (Telegram, ecc.)")
    cfg = {"telegram": chiavi["telegram"], "installato": time.strftime("%Y-%m-%d %H:%M"),
           "versione_chiavi": chiavi.get("versione", "")}
    salva_json(os.path.join(RBR_DIR, "config.json"), cfg, dry)

    print("3. Server MCP con chiave (scope utente)")
    cj = carica_json(CLAUDE_JSON)
    cj.setdefault("mcpServers", {})
    for nome, conf in chiavi["mcp_servers"].items():
        cj["mcpServers"][nome] = conf
        print(f"  + {nome}")
    salva_json(CLAUDE_JSON, cj, dry)

    print("4. Rete sandbox + 5. marketplace auto-update")
    st = carica_json(SETTINGS)
    net = st.setdefault("sandbox", {}).setdefault("network", {})
    dom = net.setdefault("allowedDomains", [])
    for d in DOMINI:
        if d not in dom:
            dom.append(d)
    mk = st.setdefault("extraKnownMarketplaces", [])
    if not any(isinstance(m, dict) and m.get("url") == MARKETPLACE_URL for m in mk):
        mk.append({"url": MARKETPLACE_URL, "autoUpdate": True})
    else:
        for m in mk:
            if isinstance(m, dict) and m.get("url") == MARKETPLACE_URL:
                m["autoUpdate"] = True
    salva_json(SETTINGS, st, dry)
    # registro marketplace (se il plugin è già stato installato dal marketplace)
    km_path = os.path.join(HOME, ".claude", "plugins", "known_marketplaces.json")
    km = carica_json(km_path)
    if "rbr-consulting" in km:
        km["rbr-consulting"]["autoUpdate"] = True
        salva_json(km_path, km, dry)

    print("\n✅ Chiavi installate. Apri una chat NUOVA perché MCP e rete si ricarichino.")
    print("   Puoi cancellare il file rbr-chiavi.json scaricato (le chiavi ora sono in ~/.claude/rbr/).")


if __name__ == "__main__":
    main()
