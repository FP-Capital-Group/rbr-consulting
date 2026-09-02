# Changelog plugin rbr-consulting

Ogni versione ha una sezione `## vX.Y.Z — data`. L'hook di sessione legge la sezione della
versione installata la PRIMA volta che gira e la mostra al consulente. La routine del lunedì
aggiunge la sezione della release che pubblica (3-6 righe, cosa cambia per chi lavora).

## v2.7.8 — 2026-09-02
- Novità annunciate all'avvio: la prima sessione dopo un aggiornamento mostra questo changelog.
- Chiedi "cosa c'è di nuovo nel plugin" per il dettaglio di qualsiasi versione.

## v2.7.7 — 2026-09-02
- Pubblicazione sul marketplace via pull request + merge (unico trigger della sync in Cowork).

## v2.7.0 → v2.7.6 — 2026-09-02
- Distribuzione dal marketplace pubblico GitHub `marcocuccaro0309/rbr-consulting`, nessun
  segreto nel pacchetto: le chiavi (GHL, Google Ads, Make, service account, Telegram) le
  installa `/rbr-setup` da `rbr-chiavi.json` (Drive condiviso, letto da solo via connettore).
- `/rbr-setup` step 0 chiavi + check visibile Conoscenza live + scansione skill del consulente.
- Hook `auto_update.py` (aggiornamento locale per Claude Code CLI).
- Rimosso Playwright ovunque.

## v2.6.0 — 2026-09-02
- Skill `scansione-skill` + comando `/rbr-scansione`: inventario delle skill del consulente e
  condivisione col team di quelle utili.
- Conoscenza live iniettata automaticamente a ogni sessione (hook `conoscenza_live.py`).
- Report del lunedì a doppio canale (Sheet + Telegram).
