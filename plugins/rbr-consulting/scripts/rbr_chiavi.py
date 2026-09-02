#!/usr/bin/env python3
"""Trova il file chiavi `rbr-chiavi.json` e installa le chiavi in ~/.claude/rbr/ se mancano.

Perché: in Cowork su Windows (e nelle sessioni cloud) la HOME è un ambiente Linux NUOVO a ogni
chat: quello che /rbr-setup scrive in ~/.claude/rbr/ sparisce alla chat successiva. La cosa che
persiste è la cartella di lavoro del consulente, montata sotto ~/mnt/<cartella>. Quindi il file
chiavi vive lì (o dove indicato) e il plugin lo installa da solo a ogni avvio, in silenzio.

Due sorgenti, in ordine: (1) un `rbr-chiavi.json` in chiaro; (2) la cassaforte `rbr-chiavi.enc` dentro il
plugin pubblico, decifrata con la passphrase `rbr-passphrase.txt` della Competenza personale «rbr-chiavi»
(il modo standard dal v2.12.0: la passphrase non cambia mai, le chiavi arrivano con gli aggiornamenti).
Ordine di ricerca del file chiavi in chiaro:
  $RBR_CHIAVI · <plugin>/rbr-chiavi.json · <cwd>/rbr-chiavi.json · <cwd>/.rbr/rbr-chiavi.json ·
  ~/.claude/skills/*/rbr-chiavi.json e ~/mnt/.claude/skills/*/rbr-chiavi.json (Competenza personale
  "rbr-chiavi", il modo consigliato) · ~/mnt/*/rbr-chiavi.json ·
  ~/mnt/*/.rbr/rbr-chiavi.json · ~/mnt/*/*/rbr-chiavi.json · ~/mnt/uploads/rbr-chiavi.json ·
  ~/Downloads/rbr-chiavi.json · ~/.claude/rbr/rbr-chiavi.json
"""
import os, sys, glob, json

HOME = os.path.expanduser("~")
RBR_DIR = os.path.join(HOME, ".claude", "rbr")
NOME = "rbr-chiavi.json"


def candidati():
    cwd = os.getcwd()
    qui = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # radice del plugin
    # pacchetto TEAM (repo privato): il file chiavi è dentro il plugin stesso
    c = [os.environ.get("RBR_CHIAVI"), os.path.join(qui, NOME),
         os.path.join(cwd, NOME), os.path.join(cwd, ".rbr", NOME)]
    mnt = os.path.join(HOME, "mnt")
    # Competenza personale "rbr-chiavi" caricata dal consulente (Personalizza → Competenze): persiste ovunque
    for pat in (f"{HOME}/.claude/skills/*/{NOME}", f"{mnt}/.claude/skills/*/{NOME}",
                f"{mnt}/*/{NOME}", f"{mnt}/*/.rbr/{NOME}", f"{mnt}/*/*/{NOME}"):
        c += sorted(glob.glob(pat))
    # Cowork Windows/cloud: ~/mnt/.claude è montato dal sistema (se persistente, è il posto ideale)
    c += [os.path.join(mnt, ".claude", "rbr", NOME), os.path.join(mnt, ".claude", NOME),
          os.path.join(mnt, "uploads", NOME),
          os.path.join(HOME, "Downloads", NOME), os.path.join(RBR_DIR, NOME)]
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


PASS_NOME = "rbr-passphrase.txt"


def trova_passphrase():
    """Passphrase della cassaforte: $RBR_PASSPHRASE → file rbr-passphrase.txt nella Competenza personale
    «rbr-chiavi» (~/.claude/skills/*/ o ~/mnt/.claude/skills/*/), in ~/.claude/rbr/, nella cartella di lavoro."""
    if os.environ.get("RBR_PASSPHRASE"):
        return os.environ["RBR_PASSPHRASE"].strip()
    mnt = os.path.join(HOME, "mnt")
    cands = [os.path.join(RBR_DIR, PASS_NOME), os.path.join(os.getcwd(), PASS_NOME)]
    for pat in (f"{HOME}/.claude/skills/*/{PASS_NOME}", f"{mnt}/.claude/skills/*/{PASS_NOME}",
                f"{mnt}/*/{PASS_NOME}", f"{mnt}/uploads/{PASS_NOME}", f"{HOME}/Downloads/{PASS_NOME}"):
        cands += sorted(glob.glob(pat))
    for c in cands:
        try:
            if os.path.isfile(c):
                v = open(c, encoding="utf-8").read().strip()
                if len(v) >= 12:
                    return v
        except Exception:
            pass
    return None


def chiavi_da_enc():
    """Decifra <plugin>/rbr-chiavi.enc con la passphrase. Ritorna (dict, descrizione) o (None, None)."""
    enc = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rbr-chiavi.enc")
    if not os.path.isfile(enc):
        return None, None
    pw = trova_passphrase()
    if not pw:
        return None, None
    try:
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import rbr_crypto
        d = json.loads(rbr_crypto.decrypt(open(enc, "rb").read(), pw).decode("utf-8"))
        if "service_account" in d and "mcp_servers" in d:
            return d, f"{enc} (decifrato con la passphrase della Competenza rbr-chiavi)"
    except Exception:
        return None, None
    return None, None


def installate():
    return os.path.exists(os.path.join(RBR_DIR, "credentials.json")) and os.path.exists(os.path.join(RBR_DIR, "mcp_servers.json"))


def installa_se_serve(forza=False):
    """Se le chiavi non sono in ~/.claude/rbr/ (o forza=True) e c'è un rbr-chiavi.json, le installa.
    Ritorna il percorso del file usato, oppure None. Silenzioso: mai eccezioni verso il chiamante."""
    try:
        if installate() and not forza:
            return None
        src = trova_chiavi()
        if src:
            chiavi = json.load(open(src, encoding="utf-8"))
        else:
            chiavi, src = chiavi_da_enc()
            if not chiavi:
                return None
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
    if "--passphrase" in sys.argv:  # salva la passphrase in ~/.claude/rbr (persiste su Mac; nel sandbox solo per la chat)
        os.makedirs(RBR_DIR, exist_ok=True)
        open(os.path.join(RBR_DIR, PASS_NOME), "w").write(sys.argv[sys.argv.index("--passphrase") + 1].strip() + "\n")
        print("passphrase salvata in", os.path.join(RBR_DIR, PASS_NOME))
    p = trova_chiavi()
    print("file chiavi in chiaro:", p or "non trovato")
    print("passphrase cassaforte:", "trovata" if trova_passphrase() else "non trovata")
    enc = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "rbr-chiavi.enc")
    print("cassaforte nel plugin (rbr-chiavi.enc):", "presente" if os.path.isfile(enc) else "assente")
    if "--installa" in sys.argv:
        print("installato da:", installa_se_serve(forza=True) or "niente")
    print("chiavi in ~/.claude/rbr:", "sì" if installate() else "no")
