# Changelog plugin rbr-consulting

Ogni versione ha una sezione `## vX.Y.Z — data`. L'hook di sessione legge la sezione della
versione installata la PRIMA volta che gira e la mostra al consulente. La routine del lunedì
aggiunge la sezione della release che pubblica (3-6 righe, cosa cambia per chi lavora).

## v2.7.10 — 2026-09-02
- I repo GitHub sono passati dall'account personale di Marco all'organizzazione aziendale **FP Capital Group**: marketplace `https://github.com/FP-Capital-Group/rbr-consulting`, sorgente privato `FP-Capital-Group/rbr-suite`.
- Chi ha già installato il plugin non deve fare nulla: il vecchio indirizzo reindirizza al nuovo e gli aggiornamenti continuano ad arrivare. Nuove installazioni: usare il nuovo URL.

## v2.7.9 — 2026-09-02
- Contributi consulenti fusi: trabocchetti wizard nuovo account Google Ads, verifica pixel con ID reale post-deploy (blur-trick Resmio) in `adv-ristorante` e `sito-landing-ristorante`.
- Novità dal mondo: MCP ufficiale GHL multi-account (da validare) e Ask AI campagne Meta in bozza, WhatsApp Click-to-Chat come obiettivo Meta, Insight GBP per superficie (Maps AI/AI Overviews), tolleranza 5% sanzioni collegamento cassa-POS (D.Lgs 148/2026), terza tranche CCNL Pubblici Esercizi da giugno 2026, Claude nel provider AI nativo di Make.

## v2.7.8 — 2026-09-02
- Novità annunciate all'avvio: la prima sessione dopo un aggiornamento mostra questo changelog.
- Chiedi "cosa c'è di nuovo nel plugin" per il dettaglio di qualsiasi versione.

## v2.7.7 — 2026-09-02
- Pubblicazione sul marketplace via pull request + merge (unico trigger della sync in Cowork).

## v2.7.0 → v2.7.6 — 2026-09-02
- Distribuzione dal marketplace pubblico GitHub `FP-Capital-Group/rbr-consulting`, nessun
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
