# Changelog plugin rbr-consulting

Ogni versione ha una sezione `## v2.10.0 — 2026-09-02
- Windows: Cowork lavora in un ambiente Linux con Python già pronto, ma nuovo a ogni chat. Le chiavi RBR ora vivono nella tua cartella di lavoro Cowork (file rbr-chiavi.json, ce lo mette /rbr-setup) e il plugin le carica da solo a ogni avvio. Su Mac non cambia nulla.
- Dai a Cowork una cartella di lavoro (icona cartella) prima di /rbr-setup: è lì che finiscono file e chiavi.

## v2.9.5 — 2026-09-02
- Fogli Google dei clienti: in /rbr-setup rispondi 'fogli' e Claude installa le librerie, prende le chiavi e fa una prova di lettura reale prima di dirti che sei pronto. Ogni foglio cliente va condiviso come Editor con il service account RBR.

## v2.9.4 — 2026-09-02
- /rbr-setup ora prepara il computer da solo: su Windows installa Python 3 se manca (o crea l'alias python3 se hai quello di python.org), su Mac attiva gli strumenti Apple. Poi chiede se vuoi collegare anche GHL, Google Ads, Make e fogli: puoi dire 'non ora'.

## v2.9.3 — 2026-09-02
- Condividere quello che impari funziona appena installato il plugin, senza setup e senza chiavi (anche su Windows): 'condividi quello che ho imparato' → arriva a Marco, che decide cosa entra nel plugin di tutti.

## v2.9.2 — 2026-09-02
- Supporto Windows completo: Regole RBR e Conoscenza live si caricano anche su PC (nessuna dipendenza da openssl o comandi Unix), tool GHL/Google Ads/Make funzionano con Python 3 del Microsoft Store.
- Su Windows installa Python 3 dal Microsoft Store: serve per le skill che producono file (Excel, PDF) e per /rbr-setup.

## v2.9.1 — 2026-09-02
- Consegna al team (3/9/2026): il plugin funziona appena installato; /rbr-setup serve solo a chi usa GoHighLevel, Google Ads, Make o i fogli Google dei clienti.
- Quello che impari lo dici a Claude ('condividi quello che ho imparato'): arriva a Marco, che decide cosa entra nel plugin di tutti.

## v2.9.0 — 2026-09-02
- Nuova skill estrai-dati-ipratico: incassi Z, coperti, prodotti, margini e canali di un cliente da iPratico Cloud senza API key (sessione del portale nel browser). Chiedi 'tira giù gli incassi di [cliente] da iPratico'.
- Windows: le Regole RBR e la Conoscenza live ora si caricano anche su PC (hook di sessione unificato).
- Installazione senza setup: i server GHL/Google Ads/Make non mostrano più errori finché non fai /rbr-setup.

## v2.8.1 — 2026-09-02
- Nuovo comando /rbr-pubblica (per Marco): pubblica subito una versione a tutti i consulenti in un colpo (pull, versione, changelog, PR, merge, Conoscenza live, Telegram).
- Ogni lunedì esce SEMPRE una versione nuova, anche solo per allineare tutti: se non vedi novità nelle skill, le novità del team sono in Conoscenza live.

## vX.Y.Z — data`. L'hook di sessione legge la sezione della
versione installata la PRIMA volta che gira e la mostra al consulente. La routine del lunedì
aggiunge la sezione della release che pubblica (3-6 righe, cosa cambia per chi lavora).

## v2.8.0 — 2026-09-02
- **Setup tutto in Cowork, niente Terminale.** I tool GoHighLevel (7 clienti), Google Ads e Make sono dichiarati nel plugin e prendono le chiavi dal tuo Mac (`~/.claude/rbr/`) tramite un ponte: dopo `/rbr-setup` e una chat nuova funzionano sia in Cowork sia in Claude Code, senza configurare nulla a mano.
- Chi ha già fatto il setup con una versione precedente: rilancia `/rbr-setup` una volta (scrive il nuovo file chiavi), poi apri una chat nuova. Al primo avvio Cowork chiede di consentire i server MCP del plugin: sì.
- Nuovo cliente GHL: ora richiede anche una riga nel plugin (release del lunedì o immediata da Marco), oltre alle chiavi.

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
