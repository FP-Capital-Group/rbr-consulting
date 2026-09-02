#!/usr/bin/env python3
"""Hook SessionStart: auto-aggiornamento del plugin rbr-consulting dal marketplace pubblico.

Replica ciò che fa Claude Code per i plugin da marketplace, ma in modo deterministico a ogni
avvio (l'app desktop non sempre lo fa da sola):
  1. `git pull` del clone del marketplace (~/.claude/plugins/marketplaces/rbr-consulting)
  2. legge la versione pubblicata (marketplace.json) e quella installata (installed_plugins.json)
  3. se la pubblicata è più nuova: copia il plugin in ~/.claude/plugins/cache/rbr-consulting/
     rbr-consulting/<versione>/ e aggiorna installed_plugins.json (backup .bak). La nuova
     versione è attiva dalla PROSSIMA sessione.
Tutto silenzioso in caso di errore (rete, permessi): la sessione non deve mai rompersi.
Timeout totale ~20s. Stampa una riga solo se ha aggiornato.
"""
import os, sys, json, time, shutil, subprocess

HOME = os.path.expanduser("~")
PLUGIN = "rbr-consulting"
KEY = f"{PLUGIN}@{PLUGIN}"
MK = os.path.join(HOME, ".claude", "plugins", "marketplaces", PLUGIN)
IP = os.path.join(HOME, ".claude", "plugins", "installed_plugins.json")
CACHE = os.path.join(HOME, ".claude", "plugins", "cache", PLUGIN, PLUGIN)


def semver(v):
    try:
        return tuple(int(x) for x in str(v).strip().lstrip("v").split("."))
    except Exception:
        return (0,)


def main():
    if not os.path.isdir(os.path.join(MK, ".git")) or not os.path.exists(IP):
        return  # installato da zip o non da marketplace: niente da fare
    try:
        subprocess.run(["git", "-C", MK, "pull", "--ff-only", "-q"], timeout=15,
                       capture_output=True)
    except Exception:
        pass  # offline: usa quello che c'è
    mk = json.load(open(os.path.join(MK, ".claude-plugin", "marketplace.json")))
    nuova = mk.get("metadata", {}).get("version") or mk["plugins"][0].get("version")
    ip = json.load(open(IP))
    voci = ip.get("plugins", {}).get(KEY)
    if not voci:
        return
    attuale = voci[0].get("version", "0")
    if semver(nuova) <= semver(attuale):
        return
    src = os.path.join(MK, "plugins", PLUGIN)
    if not os.path.exists(os.path.join(src, ".claude-plugin", "plugin.json")):
        return
    dest = os.path.join(CACHE, nuova)
    if os.path.isdir(dest):
        shutil.rmtree(dest)
    shutil.copytree(src, dest, ignore=shutil.ignore_patterns("__pycache__", ".DS_Store"))
    try:
        sha = subprocess.run(["git", "-C", MK, "rev-parse", "HEAD"], capture_output=True,
                             text=True, timeout=5).stdout.strip()
    except Exception:
        sha = voci[0].get("gitCommitSha", "")
    now = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time.gmtime())
    voci[0].update({"version": nuova, "installPath": dest, "lastUpdated": now,
                    "gitCommitSha": sha})
    shutil.copy2(IP, IP + ".bak")
    with open(IP, "w", encoding="utf-8") as f:
        json.dump(ip, f, indent=2)
    print(f"🔄 Plugin RBR aggiornato v{attuale} → v{nuova} (auto-update dal marketplace): "
          "attivo dalla prossima chat.")


if __name__ == "__main__":
    try:
        main()
    except Exception:
        pass
