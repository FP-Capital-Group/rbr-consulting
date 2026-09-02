#!/usr/bin/env python3
"""Installa le chiavi RBR sul Mac del consulente (una volta sola, da /rbr-setup).

Il plugin pubblico NON contiene segreti. Le chiavi arrivano in un file `rbr-chiavi.json`
che Marco condivide in privato (cartella Drive "RBR - Chiavi consulenti"). Questo script:
  1. salva il service account Google in   ~/.claude/rbr/credentials.json
  2. salva token Telegram e altre config in ~/.claude/rbr/config.json
  3. salva URL+chiavi dei server MCP (GHL clienti, Google Ads, Make) in ~/.claude/rbr/mcp_servers.json:
     li legge il ponte scripts/mcp_bridge.py dichiarato nel .mcp.json del plugin, quindi i tool
     compaiono sia in Cowork (sessione locale) sia in Claude Code, senza Terminale
  4. aggiunge i domini necessari all'allowlist di rete del sandbox (~/.claude/settings.json)
  5. registra il marketplace pubblico con auto-update attivo (~/.claude/settings.json)

Uso: installa_chiavi.py <percorso rbr-chiavi.json> [--dry-run]
Idempotente: rieseguirlo aggiorna senza duplicare. Fa backup dei file toccati (.bak-<ts>).
"""
import os, sys, json, time, shutil

HOME = os.path.expanduser("~")
RBR_DIR = os.path.join(HOME, ".claude", "rbr")
SETTINGS = os.path.join(HOME, ".claude", "settings.json")
DOMINI = ["oauth2.googleapis.com", "www.googleapis.com", "sheets.googleapis.com",
          "drive.googleapis.com", "api.telegram.org", "services.leadconnectorhq.com",
          "eu1.make.com", "google-ads.mcp.pipeboard.co", "mcp.facebook.com",
          "raw.githubusercontent.com", "github.com"]


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
    if chiavi.get("make_api_token"):
        cfg["make_api_token"] = chiavi["make_api_token"]  # usato da sync_contributi_datastore.py (lato Marco)
    salva_json(os.path.join(RBR_DIR, "config.json"), cfg, dry)

    print("3. Server MCP con chiave (per il ponte del plugin)")
    for nome in chiavi["mcp_servers"]:
        print(f"  + {nome}")
    salva_json(os.path.join(RBR_DIR, "mcp_servers.json"), chiavi["mcp_servers"], dry)

    print("4. Rete sandbox + 5. marketplace auto-update")
    st = carica_json(SETTINGS)
    net = st.setdefault("sandbox", {}).setdefault("network", {})
    dom = net.setdefault("allowedDomains", [])
    for d in DOMINI:
        if d not in dom:
            dom.append(d)
    # formato documentato: oggetto {nome: {source: {source: github, repo}, autoUpdate}}
    mk = st.get("extraKnownMarketplaces")
    if not isinstance(mk, dict):
        mk = {}  # migra/scarta la vecchia forma a lista
    mk["rbr-consulting"] = {"source": {"source": "github", "repo": "FP-Capital-Group/rbr-consulting"},
                            "autoUpdate": True}
    st["extraKnownMarketplaces"] = mk
    salva_json(SETTINGS, st, dry)
    # registro marketplace (se il plugin è già stato installato dal marketplace)
    km_path = os.path.join(HOME, ".claude", "plugins", "known_marketplaces.json")
    km = carica_json(km_path)
    if "rbr-consulting" in km:
        km["rbr-consulting"]["autoUpdate"] = True
        salva_json(km_path, km, dry)

    print("\n✅ Chiavi installate. Apri una chat NUOVA: i tool GHL/Google Ads/Make e la rete si attivano lì.")
    print("   Puoi cancellare il file rbr-chiavi.json scaricato (le chiavi ora sono in ~/.claude/rbr/).")


if __name__ == "__main__":
    main()
