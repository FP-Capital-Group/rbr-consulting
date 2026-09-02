#!/usr/bin/env python3
"""Trova il file chiavi `rbr-chiavi.json` e installa le chiavi in ~/.claude/rbr/ se mancano.

Perché: in Cowork su Windows (e nelle sessioni cloud) la HOME è un ambiente Linux NUOVO a ogni
chat: quello che /rbr-setup scrive in ~/.claude/rbr/ sparisce alla chat successiva. La cosa che
persiste è la cartella di lavoro del consulente, montata sotto ~/mnt/<cartella>. Quindi il file
chiavi vive lì (o dove indicato) e il plugin lo installa da solo a ogni avvio, in silenzio.

Ordine di ricerca del file chiavi:
  $RBR_CHIAVI · <cwd>/rbr-chiavi.json · <cwd>/.rbr/rbr-chiavi.json · ~/mnt/*/rbr-chiavi.json ·
  ~/mnt/*/.rbr/rbr-chiavi.json · ~/mnt/*/*/rbr-chiavi.json · ~/mnt/uploads/rbr-chiavi.json ·
  ~/Downloads/rbr-chiavi.json · ~/.claude/rbr/rbr-chiavi.json
"""
import os, sys, glob, json

HOME = os.path.expanduser("~")
RBR_DIR = os.path.join(HOME, ".claude", "rbr")
NOME = "rbr-chiavi.json"


def candidati():
    cwd = os.getcwd()
    c = [os.environ.get("RBR_CHIAVI"), os.path.join(cwd, NOME), os.path.join(cwd, ".rbr", NOME)]
    mnt = os.path.join(HOME, "mnt")
    for pat in (f"{mnt}/*/{NOME}", f"{mnt}/*/.rbr/{NOME}", f"{mnt}/*/*/{NOME}"):
        c += sorted(glob.glob(pat))
    c += [os.path.join(HOME, "Downloads", NOME), os.path.join(RBR_DIR, NOME)]
    return [p for p in c if p]


def trova_chiavi():
    for p in candidati():
        if os.path.isfile(p):
            try:
                d = json.load(open(p, encoding="utf-8"))
                if "service_account" in d and "mcp_servers" in d:
                    return p
            except Exception:
                continue
    return None


def installate():
    return os.path.exists(os.path.join(RBR_DIR, "credentials.json")) and os.path.exists(os.path.join(RBR_DIR, "mcp_servers.json"))


def installa_se_serve(forza=False):
    """Se le chiavi non sono in ~/.claude/rbr/ (o forza=True) e c'è un rbr-chiavi.json, le installa.
    Ritorna il percorso del file usato, oppure None. Silenzioso: mai eccezioni verso il chiamante."""
    try:
        if installate() and not forza:
            return None
        src = trova_chiavi()
        if not src:
            return None
        chiavi = json.load(open(src, encoding="utf-8"))
        os.makedirs(RBR_DIR, exist_ok=True)

        def scrivi(nome, dati):
            p = os.path.join(RBR_DIR, nome)
            with open(p, "w", encoding="utf-8") as f:
                json.dump(dati, f, indent=2, ensure_ascii=False)
            try:
                os.chmod(p, 0o600)
            except Exception:
                pass
        scrivi("credentials.json", chiavi["service_account"])
        cfg = {"telegram": chiavi.get("telegram", {}), "versione_chiavi": chiavi.get("versione", ""),
               "origine": src, "installato_auto": True}
        if chiavi.get("make_api_token"):
            cfg["make_api_token"] = chiavi["make_api_token"]
        scrivi("config.json", cfg)
        scrivi("mcp_servers.json", chiavi["mcp_servers"])
        return src
    except Exception:
        return None


if __name__ == "__main__":
    p = trova_chiavi()
    print("file chiavi:", p or "non trovato")
    if "--installa" in sys.argv:
        print("installato da:", installa_se_serve(forza=True) or "niente")
    print("chiavi in ~/.claude/rbr:", "sì" if installate() else "no")
