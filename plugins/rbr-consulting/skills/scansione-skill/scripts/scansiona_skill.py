#!/usr/bin/env python3
"""Inventario delle skill/comandi/agenti che il Claude di questo consulente conosce.

Uso: scansiona_skill.py [--json <file>] [--all] [--radici <dir1,dir2,...>]

Stampa un inventario Markdown (per Claude) e, se richiesto, un JSON con i dettagli.
NON legge il contenuto per intero: solo frontmatter (name/description), dimensioni,
elenco file e due flag: `segreti` (token/chiavi nel testo) e `percorsi_personali`
(path assoluti /Users/<nome>). NON invia nulla: la condivisione la fa `condividi_skill.py`
dopo la scelta del consulente.

Esclusi di default (già del team o pubblici): il plugin rbr-consulting stesso,
i plugin del marketplace ufficiale Anthropic, cowork-plugin-management, telegram.
`--all` li include comunque (solo elenco).
"""
import os, re, sys, json, glob, argparse, datetime

HOME = os.path.expanduser("~")
ESCLUSI_PLUGIN = {"rbr-consulting", "cowork-plugin-management", "telegram",
                  "anthropic-skills", "claude-plugins-official"}
RE_SECRET = re.compile(
    r"(sk-ant-[A-Za-z0-9_-]{10,}|pit-[0-9a-f-]{20,}|AIza[0-9A-Za-z_-]{20,}|"
    r"\b\d{9,10}:[A-Za-z0-9_-]{30,}\b|Bearer\s+[A-Za-z0-9._-]{20,}|"
    r"pk_[A-Za-z0-9]{20,}|xox[bap]-[A-Za-z0-9-]{10,}|"
    r"(?i:(api[_-]?key|secret|password|token)\s*[:=]\s*['\"]?[A-Za-z0-9_\-]{16,}))")
RE_USER_PATH = re.compile(r"/Users/[^/\s'\"]+/")
TEXT_EXT = {".md", ".py", ".js", ".ts", ".json", ".txt", ".yaml", ".yml", ".html",
            ".css", ".csv", ".sh", ".toml", ".jinja", ".j2", ".sql"}


def frontmatter(path):
    """name/description dal frontmatter YAML (best effort, senza dipendenze)."""
    out = {"name": "", "description": ""}
    try:
        with open(path, encoding="utf-8", errors="ignore") as f:
            head = f.read(6000)
    except OSError:
        return out
    if not head.startswith("---"):
        return out
    body = head.split("---", 2)
    if len(body) < 3:
        return out
    fm = body[1]
    m = re.search(r"^name:\s*(.+)$", fm, re.M)
    if m:
        out["name"] = m.group(1).strip().strip("'\"")
    m = re.search(r"^description:\s*(.*)$", fm, re.M)
    if m:
        desc = m.group(1).strip()
        if desc in (">-", ">", "|", "|-", ""):
            # descrizione multiriga: prendi le righe indentate successive
            lines, grab = [], False
            for ln in fm.splitlines():
                if ln.startswith("description:"):
                    grab = True
                    continue
                if grab:
                    if ln.startswith((" ", "\t")):
                        lines.append(ln.strip())
                    elif ln.strip():
                        break
            desc = " ".join(lines)
        out["description"] = desc.strip().strip("'\"")[:400]
    return out


def analizza_dir(d):
    """file testuali, dimensione totale, flag segreti/percorsi."""
    files, size, segreti, percorsi = [], 0, False, False
    for root, dirs, fnames in os.walk(d):
        dirs[:] = [x for x in dirs if x not in ("node_modules", "__pycache__", ".git", "dist")]
        for fn in fnames:
            p = os.path.join(root, fn)
            rel = os.path.relpath(p, d)
            try:
                sz = os.path.getsize(p)
            except OSError:
                continue
            size += sz
            files.append(rel)
            ext = os.path.splitext(fn)[1].lower()
            if fn in ("credentials.json", ".env") or fn.endswith((".pem", ".key")):
                segreti = True
                continue
            if ext in TEXT_EXT and sz < 400_000:
                try:
                    txt = open(p, encoding="utf-8", errors="ignore").read()
                except OSError:
                    continue
                if RE_SECRET.search(txt):
                    segreti = True
                if RE_USER_PATH.search(txt):
                    percorsi = True
    return files, size, segreti, percorsi


def voce(tipo, fonte, path, is_dir=True):
    fm = frontmatter(os.path.join(path, "SKILL.md") if is_dir else path)
    if is_dir:
        files, size, segreti, percorsi = analizza_dir(path)
    else:
        files, size = [os.path.basename(path)], os.path.getsize(path)
        txt = open(path, encoding="utf-8", errors="ignore").read()
        segreti, percorsi = bool(RE_SECRET.search(txt)), bool(RE_USER_PATH.search(txt))
    nome = os.path.basename(path.rstrip("/")).replace(".md", "")
    desc = fm["description"]
    if fm["name"] and fm["name"] != nome:
        desc = f"[{fm['name']}] {desc}"
    return {"tipo": tipo, "fonte": fonte, "nome": nome, "path": path,
            "descrizione": desc, "n_file": len(files), "kb": round(size / 1024, 1),
            "file": files[:40], "segreti": segreti, "percorsi_personali": percorsi}


def plugin_name(pdir):
    try:
        return json.load(open(os.path.join(pdir, ".claude-plugin", "plugin.json")))["name"]
    except Exception:
        return os.path.basename(pdir.rstrip("/"))


def scansiona(includi_tutto, radici_extra):
    voci, memorie, claude_md = [], [], []

    # 1. Skill personali Claude Code
    for d in sorted(glob.glob(f"{HOME}/.claude/skills/*/")):
        if os.path.exists(os.path.join(d, "SKILL.md")):
            voci.append(voce("skill", "utente (~/.claude/skills)", d))
    # 2. Comandi e agenti personali
    for p in sorted(glob.glob(f"{HOME}/.claude/commands/*.md")):
        voci.append(voce("comando", "utente (~/.claude/commands)", p, is_dir=False))
    for p in sorted(glob.glob(f"{HOME}/.claude/agents/*.md")):
        voci.append(voce("agente", "utente (~/.claude/agents)", p, is_dir=False))
    # 3. Plugin Claude Code installati (marketplace)
    for pdir in sorted(glob.glob(f"{HOME}/.claude/plugins/cache/*/*/*/")):
        mk = pdir.rstrip("/").split("/")[-3]
        pn = plugin_name(pdir)
        if not includi_tutto and (pn in ESCLUSI_PLUGIN or mk in ESCLUSI_PLUGIN):
            continue
        for d in sorted(glob.glob(os.path.join(pdir, "skills", "*/"))):
            voci.append(voce("skill", f"plugin {mk}/{pn}", d))
    # 4. Plugin caricati in Claude Cowork (desktop)
    cw = f"{HOME}/Library/Application Support/Claude/local-agent-mode-sessions"
    for pdir in sorted(glob.glob(f"{cw}/*/*/rpm/plugin_*/")):
        pn = plugin_name(pdir)
        if not includi_tutto and pn in ESCLUSI_PLUGIN:
            continue
        for d in sorted(glob.glob(os.path.join(pdir, "skills", "*/"))):
            voci.append(voce("skill", f"plugin Cowork/{pn}", d))
    # 5. Skill/comandi di progetto (cartelle di lavoro comuni, profondità limitata)
    radici = [f"{HOME}/Desktop", f"{HOME}/Documents", f"{HOME}/dev", f"{HOME}/Projects",
              f"{HOME}/code", f"{HOME}/Developer"] + radici_extra
    visti = set()
    for r in radici:
        if not os.path.isdir(r):
            continue
        for depth in ("", "*/", "*/*/", "*/*/*/"):
            for d in glob.glob(f"{r}/{depth}.claude/skills/*/"):
                rp = os.path.realpath(d)
                if rp in visti or "/rbr-consulting/" in rp:
                    continue
                visti.add(rp)
                proj = d.split("/.claude/")[0]
                voci.append(voce("skill", f"progetto {os.path.relpath(proj, HOME)}", d))
            for p in glob.glob(f"{r}/{depth}.claude/commands/*.md"):
                rp = os.path.realpath(p)
                if rp in visti:
                    continue
                visti.add(rp)
                proj = p.split("/.claude/")[0]
                voci.append(voce("comando", f"progetto {os.path.relpath(proj, HOME)}", p, is_dir=False))
            for p in glob.glob(f"{r}/{depth}CLAUDE.md"):
                claude_md.append(os.path.relpath(p, HOME))
    # 6. Istruzioni globali e memoria personale (solo segnalate, MAI condivise in blocco)
    g = f"{HOME}/.claude/CLAUDE.md"
    if os.path.exists(g):
        claude_md.insert(0, "~/.claude/CLAUDE.md (istruzioni globali)")
    for p in sorted(glob.glob(f"{HOME}/.claude/projects/*/memory/*.md")):
        if p.endswith("MEMORY.md"):
            continue
        fm = frontmatter(p)
        memorie.append({"file": os.path.relpath(p, HOME), "descrizione": fm["description"]})

    return voci, claude_md, memorie


def markdown(voci, claude_md, memorie):
    out = [f"# Inventario skill locali — {datetime.date.today().isoformat()}", ""]
    out.append(f"Trovate **{len(voci)}** voci (skill/comandi/agenti) fuori dal plugin RBR.")
    out.append("")
    out.append("| # | Tipo | Nome | Fonte | Descrizione | File | KB | ⚠️ |")
    out.append("|---|---|---|---|---|---|---|---|")
    for i, v in enumerate(voci, 1):
        flag = []
        if v["segreti"]:
            flag.append("segreti")
        if v["percorsi_personali"]:
            flag.append("path personali")
        desc = (v["descrizione"] or "—").replace("|", "/")
        if len(desc) > 140:
            desc = desc[:137] + "…"
        out.append(f"| {i} | {v['tipo']} | `{v['nome']}` | {v['fonte']} | {desc} | "
                   f"{v['n_file']} | {v['kb']} | {', '.join(flag) or ''} |")
    out.append("")
    out.append("## Path (per condividi_skill.py)")
    for i, v in enumerate(voci, 1):
        out.append(f"{i}. `{v['path']}`")
    out.append("")
    if claude_md:
        out.append("## File CLAUDE.md trovati (istruzioni: da cui ESTRARRE regole riutilizzabili, non copiare il file)")
        out += [f"- {c}" for c in claude_md[:30]]
        out.append("")
    if memorie:
        out.append(f"## Memoria personale auto-memory ({len(memorie)} file) — PERSONALE: non condividere in blocco")
        out.append("Solo se una voce è chiaramente una procedura di team, proporla come contributo testuale.")
        for m in memorie[:60]:
            out.append(f"- {m['file']}: {m['descrizione'] or '—'}")
        out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", help="salva anche il JSON completo qui")
    ap.add_argument("--all", action="store_true", help="includi anche plugin pubblici/RBR")
    ap.add_argument("--radici", default="", help="cartelle extra da scandire, separate da virgola")
    a = ap.parse_args()
    radici = [os.path.expanduser(x) for x in a.radici.split(",") if x.strip()]
    voci, claude_md, memorie = scansiona(a.all, radici)
    print(markdown(voci, claude_md, memorie))
    if a.json:
        with open(a.json, "w", encoding="utf-8") as f:
            json.dump({"data": datetime.date.today().isoformat(), "voci": voci,
                       "claude_md": claude_md, "memorie": memorie}, f, ensure_ascii=False, indent=1)
        print(f"\nJSON: {a.json}")


if __name__ == "__main__":
    main()
