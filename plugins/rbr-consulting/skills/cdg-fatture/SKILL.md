---
name: cdg-fatture
description: Elabora i CSV delle fatture esportati dall'Agenzia delle Entrate e li carica nel foglio Google "Economico" del cliente. Usa anche quando l'utente vuole correggere la categoria di un fornitore nel database master condiviso, o quando chiede come funziona questa skill / cosa deve fare per usarla. Trigger tipici - "carica le fatture", "elabora i CSV dell'agenzia delle entrate", "aggiorna l'economico", "genera fatture.xlsx", "carica i dati sul foglio del cliente", "[fornitore] è categoria X non Y", "correggi il master fornitori", "sposta [fornitore] in un'altra categoria", "come funziona questa skill", "come devo fare", "cosa ti devo mandare", "come inizio un caricamento".
---

# CDG — Elaborazione e caricamento fatture

Pipeline: **CSV Agenzia delle Entrate → FATTURE.xlsx → foglio/i Google "Economico"**.

## Quando ti chiedono "come funziona" o "come devo fare"
Se qualcuno (nuovo o già utente della skill) chiede come funziona, cosa deve mandarti, o come
iniziare un caricamento, rispondi SEMPRE con queste istruzioni (puoi adattare il tono ma non il
contenuto):

1. Condividimi il file CSV (export Agenzia delle Entrate) oppure gli XML delle fatture.
2. Condividi il Google Sheet "Economico" del cliente da compilare con questo indirizzo, così posso leggerlo e scriverci: **fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com** (Condividi → Editor).
3. Copia e incolla qui l'URL del foglio.

Poi procedo io: genero FATTURE.xlsx, ti chiedo conferma solo per i fornitori nuovi o non
riconosciuti, e carico i dati sul foglio.

Il CSV grezzo dell'Agenzia delle Entrate è sempre nello stesso formato: le operazioni di
pulizia/generazione (step 1-3) non cambiano mai. È il layout del foglio Google che può
variare da cliente a cliente (vedi sotto) — le CATEGORIE restano sempre le stesse 9
(FORNITORI, Servizi, Utenze, Piattaforme Delivery, Pubblicità - Marketing, Provvigioni,
Materiali di consumo, Viaggi e trasferte, più eventuale "Altro").

## Prerequisiti
- Gli script e `MASTER_SHEET_URL.txt` vivono nella sottocartella `scripts/` di QUESTA skill; `credentials.json` è in `~/.claude/rbr/` (installata da /rbr-setup, gli script la trovano da soli) (distribuita col plugin `rbr-consulting`). All'inizio della sessione imposta `CDG_HOME` al percorso assoluto di quella cartella (es. `export CDG_HOME="<cartella di questo SKILL.md>/scripts"`) oppure sostituisci `$CDG_HOME` nei comandi con quel percorso. Se l'utente ha ancora la vecchia cartella condivisa `CDG_condiviso` e la preferisce, va bene lo stesso: è identica.
- Il foglio Google del cliente deve essere condiviso in **Editor** con il service account (l'email è in `SETUP_COLLEGHI.md`). Lo stesso vale per il Google Sheet del master fornitori (vedi sotto). Come funziona tutto il modello di accessi Google (chi condivide cosa, SA vs connettore Drive, errori tipici): vedi `google-accessi.md` in questa cartella.
- Librerie Python: `pandas openpyxl gspread oauth2client` (vedi setup).

## Skill vs database condiviso — NON mischiare i due
Questa cartella skill (`cdg-fatture/`, quella che contiene questo SKILL.md) contiene solo
**istruzioni e logica**, stabili nel tempo. Il **database fornitori** invece cambia a ogni
caricamento (nuovi fornitori, correzioni di categoria) e vive **SEMPRE e SOLO** su questo Google
Sheet condiviso (dal 05/08/2026, non più un xlsx locale):
`https://docs.google.com/spreadsheets/d/1sxtE5X5Nf5O1XWCo3Kr72VcpRVwUhnhXUI7Eg_obMx4`
letto/scritto dagli script tramite il modulo `master_sheet.py` (usa `gspread`, stesso service
account dei fogli "Economico"). Questo stesso URL è anche in `CDG_condiviso/MASTER_SHEET_URL.txt`
(fonte usata dagli script): se mai divergessero, quel file è quello autoritativo per gli script,
ma non dovrebbero mai cambiare — è lo stesso identico foglio.
- Ogni scrittura (nuovo fornitore aggiunto, correzione categoria) è una singola operazione
  API sulla riga giusta — non un salvataggio dell'intero file — quindi due colleghi che
  lavorano in parallelo su fornitori diversi non si sovrascrivono a vicenda (a differenza
  del vecchio xlsx locale sincronizzato via cloud, dove l'intero file veniva riscritto).
- La skill arriva a ogni collega tramite il **plugin `rbr-consulting`** (marketplace
  `rbr-suite`): niente più copie manuali in `~/.claude/skills/` — per gli aggiornamenti
  basta aggiornare il plugin. Script + `MASTER_SHEET_URL.txt` sono nel plugin, `credentials.json` in `~/.claude/rbr/`;
  inclusi in `scripts/` (i dati vivi del master restano sul Google Sheet).

## Procedura da seguire
1. **Individua i file** da elaborare.
   - **Caso standard**: CSV export Agenzia delle Entrate, separatore `;`, codifica utf-8, 17 colonne.
   - **Caso file già pronto**: a volte l'utente fornisce un file `.xlsx` già nel formato output (colonne: Data emissione, DenominazioneFornitore, NumeroDocumento, TipoDocumento, Imponibile, Iva, Lordo — senza Categoria). In questo caso NON passa da `genera_fatture.py`: si aggiunge solo la colonna Categoria leggendo dal master (le note di credito sono già negative in questi file).
   Se non è chiaro dove sono i file, chiedi all'utente la cartella.
2. **Unisci i CSV** (solo per il caso standard) in un unico file temporaneo. Escludi eventuali file di output (`_piano_scrittura*.csv`, `FATTURE.xlsx`).
   - **Controlla i duplicati prima di unire**: gli export trimestrali dell'Agenzia delle Entrate possono sovrapporsi (fatture del giorno di confine presenti in due file) o essere duplicati interi (cliente che esporta due volte lo stesso trimestre con nomi diversi, es. `2026-3.csv` identico a `2026-2.csv`). Dopo l'unione fai `drop_duplicates()` sulla riga intera e confronta i range di date dei singoli file — senza questo controllo gli importi raddoppiano nel CE (caso reale: ~65k€ doppi, cliente Zio Bibbi, ago 2026).
3. **Genera FATTURE.xlsx**:
   `python3 "$CDG_HOME/genera_fatture.py" "<file_unito>.csv"`
   Lo script pulisce gli apostrofi, converte gli importi, mette in **negativo** le note di credito e assegna le categorie leggendo dal master (Google Sheet).
4. **Fornitori nuovi** — se lo script segnala fornitori non mappati (li aggiunge temporaneamente al master come "Altro"):
   - cerca **online** ogni fornitore per ragione sociale e deduci una categoria proposta. Categorie valide: `FORNITORI` (SOLO food, bevande, o comunque costi variabili — MAI attrezzature/impianti/beni strumentali anche se destinati alla cucina, quelli vanno in Servizi o Materiali di consumo), `Servizi`, `Utenze`, `Piattaforme Delivery`, `Pubblicità - Marketing`, `Provvigioni`, `Materiali di consumo`, `Viaggi e trasferte`.
   - **REGOLA FERREA: mai assegnare una categoria a un fornitore nuovo senza conferma dell'utente, nemmeno quando la ricerca online dà un risultato ad alta confidenza.** Un caso reale (fornitore "START SRL", utility energetica omonima ma in realtà un'azienda di servizi) ha dimostrato che la ricerca online può portare a una categoria plausibile ma sbagliata. Quindi per OGNI fornitore nuovo — trovato online o no — fermati, elenca fornitore + categoria proposta (o "non trovato/incerto" se non lo trovi) + importo, e **aspetta il via libera dell'utente prima di proseguire**. Mai lasciare un fornitore in "Altro" di default.
   - solo dopo la conferma, aggiorna il master (Google Sheet) con le categorie confermate e **rigenera** FATTURE.xlsx.
   - **Verifica finale prima di procedere**: controlla che FATTURE.xlsx non contenga righe con Categoria = "Altro". Se ce ne sono, sono da chiedere all'utente, non da ignorare.
5. **Chiedi all'utente l'URL del foglio Google** del cliente.
6. **Dry-run** (nessuna scrittura):
   `python3 "$CDG_HOME/carica_google_sheet.py" FATTURE.xlsx "<url>"`
   Lo script rileva da solo il layout del foglio (vedi sotto) e mostra il riepilogo per ciascun foglio coinvolto.
   - **Se lo script segnala spazio insufficiente in una categoria**: NON esiste inserimento automatico di righe (rimosso deliberatamente — instabile). Lo script si ferma e stampa un riepilogo (categoria + quante righe servono + dopo quale riga inserirle). Riporta questo riepilogo all'utente **testuale, chiaro**, e chiedi di aggiungere lui le righe vuote nel punto indicato. Rilancia il dry-run dopo la sua conferma.
7. **Su conferma esplicita dell'utente, scrivi davvero**:
   `python3 "$CDG_HOME/carica_google_sheet.py" FATTURE.xlsx "<url>" --write`
8. **Verifica**: confronta i totali del foglio (colonne `TOTALE <anno>`) con i totali per categoria/anno calcolati da FATTURE.xlsx e riporta se quadra al centesimo. Su un foglio già popolato, verifica invece che le celle scritte fossero vuote prima (nessun raddoppio) e che la somma "Aggiunto" combaci col totale di FATTURE.xlsx.

## Layout del foglio Google — può variare, lo script si adatta da solo
- **Foglio unico "Economico"**: tutti gli anni affiancati in colonna (TOTALE 2025=B, gennaio=D…; TOTALE 2026=AB, gennaio=AD…), categorie in colonna A dalla riga 21. (Layout più comune.)
- **Fogli separati per anno**: tab distinte "Economico 2025", "Economico 2026", ecc., ciascuna con il proprio blocco anno. Lo script rileva automaticamente quale caso si applica (`resolve_worksheets`) e instrada ogni fattura al foglio giusto in base all'anno.
- **Categorie "contenitore" con sotto-voci**: a volte una categoria (es. "Servizi", "Materiali di consumo") non ha una riga-totale propria con `SUM`, ma è la somma di sotto-voci (Affitti, Software, Commercialista, Varie...). Il loader lo rileva da solo. In questo caso il fornitore viene cercato in TUTTE le sotto-voci insieme; se nuovo, va nella **prima riga libera di tutta l'area della categoria** (a prescindere da quale sotto-voce), SENZA mai toccare le intestazioni di sotto-categoria.
- **Cliente multi-punto-vendita**: il workbook ha una tab **per ogni punto vendita** (es. "Economico Store 1", "Economico Store 2", i nomi reali possono usare il nome del locale al posto di "Store N") + una tab di **riepilogo aggregato** (es. "Economico Aggregato") che è SOLO formule (pesca dagli store, es. `='Economico Store 1'!B2`) e NON va MAI passata come target di scrittura.
  - Individua tutte le tab del workbook (`ss.worksheets()`), riconosci quali sono i punti vendita.
  - Origine dati — due sotto-casi: (a) **P.IVA diverse per punto vendita** → ogni CSV Agenzia Entrate è già specifico di un punto vendita, stesso flusso di sempre, un CSV = un FATTURE.xlsx = una tab; (b) **stessa P.IVA per tutti i punti vendita** → il CSV unico non basta, servono gli **XML delle singole fatture elettroniche** (anche .p7m), usa `python3 "$CDG_HOME/estrai_fatture_xml.py" "<cartella>" --store "PAROLA1,PAROLA2=FATTURE_Store1.xlsx" --store "PAROLA3=FATTURE_Store2.xlsx"`.
    - **La destinazione NON è quasi mai (solo) nell'intestazione**: l'intestazione (CessionarioCommittente/Sede) spesso riporta un'unica sede legale fissa uguale per tutti i punti vendita — usarla come UNICA fonte assegna quasi tutto a un solo store (successo realmente: differenza di ~155k€ su un cliente, scoperta solo confrontando con un partitario del fornitore). Lo script cerca la destinazione vera in ordine di priorità: 1) riga per riga in `DettaglioLinee` (Descrizione o AltriDatiGestionali, qualunque etichetta usi il fornitore — "DEST MERCI", "Dest.Merce", ecc. — con "eredità" sulle righe successive fino al prossimo cambio); 2) nella Causale del documento; 3) nel testo di un eventuale PDF allegato alla fattura (bollette utenze/gas spesso hanno l'indirizzo SOLO lì); 4) l'intestazione, come ULTIMA istanza (per la maggior parte dei fornitori la varia correttamente, quindi va comunque usata quando non c'è nient'altro — solo NON come prima/unica fonte).
    - Per evitare falsi positivi (alcuni fornitori scrivono nomi di città che sono un proprio riferimento interno — es. il proprio punto vendita di ritiro o il proprio magazzino di spedizione, non la destinazione del cliente), un match riga/causale è accettato solo se il testo nomina anche il cliente/locale o usa un'etichetta esplicita inequivocabile (vedi `MARCATORI_CLIENTE`/`ETICHETTE_FORTI` in cima allo script — da adattare al nome del cliente specifico).
    - Se al termine restano fatture non classificate, lo script le segnala in `FATTURE_NON_CLASSIFICATE.xlsx` — copiane gli XML originali in una cartella dedicata e chiedi all'utente di controllarle (spesso lui trova il campo giusto guardando la fattura in un lettore, più veloce che indovinare altri pattern XML).
  - Per il caricamento, usa `python3 "$CDG_HOME/carica_google_sheet.py" FATTURE_storeN.xlsx "<url>" --sheet "Economico Store N" [--write]`: il flag `--sheet` forza la tab esatta per nome, bypassando la ricerca automatica "Economico"/"Economico <anno>". Ripeti dry-run→write→verifica per ogni punto vendita separatamente, mai sulla tab aggregata.

## Correggere la categoria di un fornitore nel master

L'utente conosce il business dei suoi clienti meglio di qualsiasi ricerca online, quindi
quando corregge la categoria di un fornitore la correzione è definitiva e va applicata subito,
senza chiedere conferma (rientra nell'autonomia già concessa per questa pipeline). Trigger
tipici: *"START SRL è servizi non utenze, correggi il master"*, *"sposta X in FORNITORI"*,
*"NOVE NOVE è servizi"*.

1. Esegui: `python3 "$CDG_HOME/correggi_categoria_master.py" "<Denominazione Fornitore>" "<Nuova Categoria>"`
   Fa match sul nome normalizzato (case/spazi insensibile), aggiorna la Categoria e salva. Se
   il fornitore non viene trovato, lo script elenca i nomi più simili presenti nel master:
   usa quello giusto e ripeti, non indovinare/creare una riga nuova.
2. Conferma all'utente in una riga cosa è stato cambiato (fornitore, categoria vecchia → nuova).
3. **Non fermarti qui se il fornitore ha già fatture caricate nel periodo corrente**: se nella
   stessa conversazione hai appena caricato o stai per caricare dati che includono questo
   fornitore, la correzione del master vale solo per i **prossimi** caricamenti — non sposta
   automaticamente celle già scritte su un foglio Google. Segnala all'utente se sospetti che
   ci siano importi già scritti nella categoria vecchia (sbagliata) sul foglio del cliente, e
   chiedi se vuole che tu sposti anche quella cella, invece di assumerlo silenziosamente.

## Note importanti
- Il master fornitori è un **Google Sheet condiviso**: ogni categorizzazione fatta da un collega (in tempo reale) vale per tutti i prossimi caricamenti, anche in corso da un altro collega in parallelo.
- Lo script **SOMMA** sui valori già presenti nelle celle: **non ricaricare due volte lo stesso periodo** (raddoppia gli importi).
- **Mai inserimento automatico di righe**: se manca spazio, lo script si ferma SEMPRE e chiede conferma prima di qualunque scrittura (anche parziale). Non bypassare mai questa regola.
- La sezione "Altro" sul foglio (diversa dal campo Categoria nel master), se creata, registra i dati ma **non** è collegata ai totali generali/EBITDA del foglio. Con la nuova regola "mai Altro nel master", questa sezione dovrebbe servire sempre più raramente.
- **Bug storico colonna Lordo (fix 2026-08-27, scoperto su Zio Bibbi):** prima di questa data `genera_fatture.py` riempiva la colonna Lordo con l'identificativo SDI del file invece che con Imponibile+Iva (totali in trilioni, errore evidente). Se hai FATTURE.xlsx generati prima del 27/8/2026 e li usi ancora, la colonna Lordo di quei file è sbagliata: rigenerali o ricalcola Lordo a mano come Imponibile+Iva.
