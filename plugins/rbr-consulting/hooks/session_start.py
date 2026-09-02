#!/usr/bin/env python3
"""Hook SessionStart unico (Mac, Linux, Windows): stampa le Regole RBR, poi Conoscenza live e
auto-update. Ogni parte è indipendente: se una fallisce le altre girano comunque."""
import os, sys, runpy
try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass
ROOT = os.environ.get("CLAUDE_PLUGIN_ROOT") or os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
try:  # ambienti con HOME nuova a ogni chat (Cowork Windows/cloud): installa le chiavi dal file nella cartella di lavoro
    sys.path.insert(0, os.path.join(ROOT, "scripts"))
    import rbr_chiavi
    rbr_chiavi.installa_se_serve()
except Exception:
    pass
try:
    sys.stdout.write(open(os.path.join(ROOT, "hooks", "regole-rbr.md"), encoding="utf-8").read())
    sys.stdout.flush()
except Exception:
    pass
for script in ("conoscenza_live.py", "auto_update.py"):
    try:
        runpy.run_path(os.path.join(ROOT, "hooks", script), run_name="__main__")
    except SystemExit:
        pass
    except Exception:
        pass
