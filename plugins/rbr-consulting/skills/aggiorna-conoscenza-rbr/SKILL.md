---
name: aggiorna-conoscenza-rbr
description: Routine di auto-aggiornamento della conoscenza RBR — ogni lunedì fonde nel plugin quello che i consulenti hanno imparato (contributi e skill condivise nello Sheet), cerca online le novità (suite GHL/Make/Resmio/iPratico/Pienissimo, Meta/Google Ads, AI e tool, business e formatori Hormozi/Merenda/Abraham, trend ristorazione), rilascia la versione sul marketplace pubblico, aggiorna Conoscenza live e manda il report Telegram a Marco. Usa quando l'utente chiede di aggiornare la conoscenza, "cosa c'è di nuovo", o come routine cloud settimanale.
---

# Aggiornamento conoscenza RBR (routine del lunedì)

Gira come routine cloud Claude Code (`Aggiornamento conoscenza RBR (settimanale)`,
lunedì 06:00 UTC, repo rbr-suite). Obiettivo: il cervello del team non invecchia e
cresce con quello che ognuno impara. Due fonti: **le persone** (Sheet contributi) e
**il mondo** (ricerca online).

## Fase 1 — Dalle persone: Sheet "RBR - Contributi conoscenza", tab Contributi
Service account: `~/.claude/rbr/credentials.json` (nel repo privato rbr-suite: `tools/rbr-chiavi.json`).
Colonne: Data, Autore, Area, Titolo, Contenuto, Stato. Lavora le righe `Stato = nuovo`:

**A. Contributi testuali** (Area = skill/tema): se valido → fondilo nella skill o memory
pertinente con provenienza `(contributo di <Autore>, <data>)`; se dubbio → non fondere,
Stato `da validare`, segnala nel report. Poi Stato → `integrato`.

**B. Skill condivise** (Area = `skill-nuova:<nome>`, prodotte da `scansione-skill`):
1. Raggruppa tutte le righe con la stessa Area. `Titolo` = percorso relativo del file
   (`SKILL.md`, `scripts/x.py`, …); le parti `(parte i/n)` si concatenano in ordine;
   la riga `_nota` è il contesto dell'autore.
2. Se esiste già `plugins/rbr-consulting/skills/<nome>/` o una skill equivalente →
   NON duplicare: integra le differenze utili nella skill esistente e segnala nel report.
3. Altrimenti ricrea i file in `plugins/rbr-consulting/skills/<nome>/`. Verifica che
   `SKILL.md` abbia frontmatter `name` (= nome cartella, kebab-case) e `description`
   senza caratteri `<` `>` (il validatore Cowork li rifiuta); riscrivi la description
   in italiano se serve, orientata ai trigger d'uso RBR. Aggiungi sotto il titolo:
   `> Skill condivisa da <Autore> il <data> (scansione skill).` e la `_nota`.
4. Sicurezza: grep di token/chiavi (`sk-`, `pit-`, `Bearer`, `AIza`, `token=`) → se
   ne trovi, sostituisci con segnaposto e segnala. Niente `credentials.json`/`.env`.
5. Skill nuova = bump **MINOR** della versione (arriva a tutti con l'auto-update).
   Aggiorna il conteggio skill in `README.md` e `plugin.json` (description).
6. Stato di tutte le righe del gruppo → `integrato`.

## Fase 2 — Dal mondo: ricerca online (WebSearch/WebFetch, ultimi 7-30 giorni)
Per ogni fronte: se non c'è niente di rilevante scrivi "nessuna novità" e passa oltre.
1. **Piattaforme suite** (impattano le skill operative): GoHighLevel (API, email,
   workflow, limiti), Make (API/MCP, moduli), Resmio, iPratico, Pienissimo Pro.
2. **Advertising & presenza locale**: Meta Ads per local business (formati, targeting,
   policy, CAPI, lead form), Google Ads local/PMax, Google Business Profile, GA4/GSC.
3. **AI e strumenti**: novità Claude/Claude Code/Cowork/MCP che cambiano il modo di
   lavorare dei consulenti; nuovi MCP/tool utili (segnalare, mai installare).
4. **Business e formatori**: nuovi contenuti/framework di Alex Hormozi, Frank Merenda
   (Metodo Merenda, Pienissimo), Jay Abraham; altri formatori di riferimento per
   ristorazione e marketing a risposta diretta (Dan Kennedy, Russell Brunson, formatori
   italiani di ristorazione). Solo idee applicabili ai clienti RBR, riscritte in parole
   nostre come framework operativi — mai copiare testi.
5. **Trend ristorazione Italia**: report di settore, normative (scontrini, lavoro,
   TFR/CCNL), consumi, delivery. Solo ciò che tocca CDG, marketing o HR dei clienti.
6. **Circolo degli Imprenditori** (mensile): con i tool Drive cerca il PDF più recente
   "Circolo degli Imprenditori - Gold - <Mese Anno>"; se è un numero non ancora in
   `strategia-marketing-rbr/circolo-imprenditori.md`, aggiungi in cima la sezione
   (Temi / Concetti in parole nostre / Applicazione RBR). Zero citazioni.

## Fase 3 — Filtro rilevanza
Per ogni novità: cambia qualcosa in come lavoriamo? Dove?
- Procedura operativa → `memory/` o skill del plugin
- Framework strategico → skill `strategia-marketing-rbr`
- Nuovo tool → segnalazione a Marco (nome + cosa fa + 2-3 casi d'uso RBR + costo)
Scarta il rumore. Mai modificare procedure con API/script su una news non verificata:
in dubbio, segnala nel report invece di modificare.

## Fase 4 — Aggiornamento e release
1. Aggiorna i file (stile breve, operativo, italiano, con data).
2. Voce in `memory/aggiornamenti_log.md` (sezione `## Settimana YYYY-MM-DD` in cima):
   novità, contributi con autore, skill nuove, tool, release, esito Telegram.
3. Se hai toccato `plugins/rbr-consulting/`: aggiungi in cima a `CHANGELOG.md` la sezione
   `## vX.Y.Z — data` (3-6 righe: cosa cambia per chi lavora), poi bump versione **semver numerico**
   (patch: `2.7.0 → 2.7.1`, MAI zero-padded; minor per skill nuove). MAI chiavi/token nel
   plugin: il pacchetto viene pubblicato. Poi **pubblica sul marketplace pubblico**
   `FP-Capital-Group/rbr-consulting` (da cui i plugin dei consulenti si auto-aggiornano):
   `python3 tools/build_public_plugin.py --push` (clona/aggiorna il repo pubblico, rimuove
   credentials.json e gli MCP con chiave, scansione anti-segreti — se abortisce NON forzare —,
   scrive marketplace.json, push). Se il push fallisce per permessi, lo fa la task locale sul
   Mac di Marco il lunedì. Lo zip su Drive non serve più.
4. **Conoscenza live** (tab dello stesso Sheet: Data, Area, Novità/procedura,
   Skill/file di riferimento, Versione plugin): una riga per ogni novità/contributo/skill
   della settimana. È quello che l'hook inietta nelle sessioni di tutti. Max 100 righe.
5. Commit `knowledge: aggiornamento settimanale YYYY-MM-DD` + push su main.

## Fase 5 — Report a Marco (SEMPRE, anche con zero novità)
Testo semplice, max 15 righe: `📚 Conoscenza RBR — settimana YYYY-MM-DD`, poi
**Dalle persone** (autore → cosa → dove; skill nuove), **Dal mondo** (fonte → cosa cambia
→ file), tool da valutare, release (`Plugin vX.Y.Z sul marketplace: si aggiorna da solo al prossimo riavvio; già live via Conoscenza live`), chiusura `Storico: memory/aggiornamenti_log.md (rbr-suite)`.
Invio in DUE canali, sempre entrambi:
1. Riga nel tab `Report lunedì` dello Sheet (colonne Data, Testo, Inviato; crea il tab
   se manca). Inviato = vuoto.
2. Telegram: `curl -s -X POST https://api.telegram.org/bot<token>/sendMessage -d chat_id=<chat> --data-urlencode text="…"`
   (token e chat in `~/.claude/rbr/config.json`, chiave `telegram`). Se `"ok":true` → aggiorna Inviato = `sì`.
   Se la rete lo blocca (proxy 403), lascia Inviato vuoto: lo recapita la task locale
   sul Mac di Marco (`scripts/invia_report_lunedi.py`, lunedì 09:00).
