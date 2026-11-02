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
- Gli script e `MASTER_SHEET_URL.txt` vivono nella sottocartella `scripts/` di QUESTA skill; `credentials.json` è in `~/.claude/rbr/` (installata da /rbr-setup, gli script la trovano da soli) (distribuita col plugin `rbr-consulting`). All'inizio della sessione imposta `CDG_HOME` al percorso assoluto di quella cartella (es. `export CDG_HOME="<cartella di questo SKILL.md>/scripts"`) oppure sostituisci `$CDG_HOME` nei comandi con quel percorso.
  ⚠️ **Usa SOLO gli script in `scripts/` del plugin.** Se la shell esporta già una
  `CDG_HOME` verso una vecchia cartella `CDG_condiviso` (installazioni datate la
  mettevano nel profilo), quella cartella può essere rimasta indietro o contenere
  modifiche locali non portate nel plugin — non è detto che sia identica. Verifica
  sempre cosa punta `$CDG_HOME` prima di lanciare uno script, e se un collega la usa
  ancora, prima si portano nel plugin le modifiche che esistono solo lì, poi la
  cartella si archivia. (correzione di Andrea Chirivì, 2026-10-12)
- Il foglio Google del cliente deve essere condiviso in **Editor** con il service account (l'email è in `SETUP_COLLEGHI.md`). Lo stesso vale per il Google Sheet del master fornitori (vedi sotto). Come funziona tutto il modello di accessi Google (chi condivide cosa, SA vs connettore Drive, errori tipici): vedi `google-accessi.md` in questa cartella.
- Librerie Python: `pandas openpyxl gspread oauth2client` (vedi setup).

## Skill vs database condiviso — NON mischiare i due
Questa cartella skill (`cdg-fatture/`, quella che contiene questo SKILL.md) contiene solo
**istruzioni e logica**, stabili nel tempo. Il **database fornitori** invece cambia a ogni
caricamento (nuovi fornitori, correzioni di categoria) e vive **SEMPRE e SOLO** su questo Google
Sheet condiviso (dal 05/08/2026, non più un xlsx locale):
`https://docs.google.com/spreadsheets/d/1sxtE5X5Nf5O1XWCo3Kr72VcpRVwUhnhXUI7Eg_obMx4`
letto/scritto dagli script tramite il modulo `master_sheet.py` (usa `gspread`, stesso service
account dei fogli "Economico"). La fonte usata dagli script è `scripts/MASTER_SHEET_URL.txt`
**dentro il plugin** (non una copia in `CDG_condiviso`, vecchia e potenzialmente disallineata —
vedi i Prerequisiti).
- Ogni scrittura (nuovo fornitore aggiunto, correzione categoria) è una singola operazione
  API sulla riga giusta — non un salvataggio dell'intero file — quindi due colleghi che
  lavorano in parallelo su fornitori diversi non si sovrascrivono a vicenda (a differenza
  del vecchio xlsx locale sincronizzato via cloud, dove l'intero file veniva riscritto).
- La skill arriva a ogni collega tramite il **plugin `rbr-consulting`** (marketplace
  `rbr-suite`): niente più copie manuali in `~/.claude/skills/` — per gli aggiornamenti
  basta aggiornare il plugin. Script + `MASTER_SHEET_URL.txt` sono nel plugin, `credentials.json` in `~/.claude/rbr/`;
  inclusi in `scripts/` (i dati vivi del master restano sul Google Sheet).

## Quando ti chiedono come funziona (avvio del cliente)

Al primo incontro si fa partire il flusso in uno di due modi: si chiede la **delega
al cassetto fiscale**, oppure si scaricano le fatture **insieme al cliente durante
la call di onboarding** — e nella stessa call si configura Fatture in Cloud (o il
gestionale che usa), così i dati arrivano da soli ai caricamenti successivi. Se è il
titolare a dover scaricare le fatture su richiesta ogni volta, il CE resta fermo ad
aspettarle: va legato alla scadenza dei 60 giorni per i dati iniziali prevista dalle
condizioni contrattuali. (contributo di Andrea Chirivì, 2026-10-12)

⚠️ **Gli XML scadono sul portale AdE**: si scaricano da Fatture e Corrispettivi solo
fino al 31/12 del secondo anno dopo la ricezione (a settembre 2026 gli XML del 2023
non erano più scaricabili; dopo la scadenza restano solo gli ELENCHI CSV "Dati
fattura", senza le righe della fattura, che non bastano per analisi acquisti,
listino e food cost). **Il 31/12/2026 scadono gli XML del 2024 di tutti i clienti**:
al primo incontro scarica e archivia subito gli XML dei due anni precedenti. Questa
regola va riconfermata sulla pagina AdE (vale per chi ha aderito al servizio di
consultazione). (contributo di Andrea Chirivì, 2026-10-12)

## Procedura da seguire
1. **Individua i file** da elaborare.
   - **Caso standard**: CSV export Agenzia delle Entrate, separatore `;`, codifica utf-8, 17 colonne.
   - **Caso file già pronto**: a volte l'utente fornisce un file `.xlsx` già nel formato output (colonne: Data emissione, DenominazioneFornitore, NumeroDocumento, TipoDocumento, Imponibile, Iva, Lordo — senza Categoria). In questo caso NON passa da `genera_fatture.py`: si aggiunge solo la colonna Categoria leggendo dal master (le note di credito sono già negative in questi file). **La colonna Data emissione va scritta GG/MM/AAAA** (o come data vera di Excel), **mai come testo ISO AAAA-MM-GG**: il loader legge con `dayfirst=True`, e una data ISO può invertire giorno e mese per tutti i giorni fino al 12 (caso reale: totali annui giusti, fatture sparse nei mesi sbagliati, alcune in mesi futuri). Vale per ogni script che produce `FATTURE.xlsx`.
   - **Caso Fatture in Cloud**: due strade. (a) **API v2**: uno script dedicato può scaricare `/c/{company_id}/received_documents` a pagine, mettere le note di credito in negativo e unificare per P.IVA i fornitori scritti in modi diversi; filtro `--dal`/`--al`, categoria dal master, `--escludi` per le spese personali; produce `FATTURE.xlsx` direttamente. Il token è **manuale, in sola lettura** (`received_documents:r` + `entity.suppliers:r`) e **sta fuori dal repo**; un token dell'app può vedere più aziende, controlla in alto a sinistra sul web quale azienda è aperta prima di usarlo. ⚠️ Lo script non è ancora portato in questo plugin: se serve, va scritto o chiesto come contributo prima di affidarcisi. (b) **Export XLS dal web**: Acquisti → Spese → Seleziona tutto → XLS, un file per anno. Il `.xls` è malformato: va letto con `xlrd` e `ignore_workbook_corruption=True`, intestazione alla riga 5. Se il cliente usa categorie sue in FIC serve una **tabella di raccordo PER CLIENTE E PER ANNO** (i codici possono cambiare da un anno all'altro). Poi dry-run, righe vuote aggiunte dall'utente, backup, `--write`.
   - **Caso TeamSystem**: export "Fatture ricevute" (NON le altre viste: autofatture e integrazioni compaiono anche fra le inviate e si duplicherebbero). Le note di credito TD04 escono con segno incoerente: forzale tutte in negativo. Le date escono come numeri seriali di Excel: riscrivile GG/MM/AAAA. Più file si uniscono e si deduplicano sull'**ID SdI**. `--escludi` per le spese personali. ⚠️ Anche questo script non è ancora portato nel plugin.
   Se non è chiaro dove sono i file, chiedi all'utente la cartella.

   **Cosa il CSV AdE non contiene** (contributo di Andrea Chirivì, 2026-10-12): alcuni
   costi non sono fatture elettroniche e vanno chiesti al cliente e caricati a mano,
   ogni mese, prima di dire che il CE è chiuso. Esempi: bombole del gas pagate con
   scontrino, acqua dell'acquedotto (avvisi via PEC), ricevute e prestazioni
   occasionali dei collaboratori (es. chi gestisce i social, da cercare in Fatture in
   Cloud o chiedere), affitto pagato a un privato. Passa una checklist fissa col
   cliente a ogni chiusura del mese: senza, i costi risultano più bassi e l'EBITDA
   più alto di quello vero. (richiamo in `riconciliazione-dati-cliente/SKILL.md`)
2. **Unisci i CSV** (solo per il caso standard) in un unico file temporaneo. Escludi eventuali file di output (`_piano_scrittura*.csv`, `FATTURE.xlsx`).
   - **Controlla i duplicati prima di unire**: gli export trimestrali dell'Agenzia delle Entrate possono sovrapporsi (fatture del giorno di confine presenti in due file) o essere duplicati interi (cliente che esporta due volte lo stesso trimestre con nomi diversi, es. `2026-3.csv` identico a `2026-2.csv`). Dopo l'unione fai `drop_duplicates()` sulla riga intera e confronta i range di date dei singoli file — senza questo controllo gli importi raddoppiano nel CE (caso reale: ~65k€ doppi, cliente Zio Bibbi, ago 2026).
   - **Export mensili del cliente: depurare SEMPRE per numero fattura.** I CSV esportati per *data di ricezione* si portano dietro decine di fatture del mese prima (visti 26 doppioni per 38.284 € in un solo file) che `drop_duplicates()` sulla riga intera non vede, perché stanno in file di mesi diversi. Prima di elaborare incrocia **(fornitore + numero fattura + data emissione)** col file del mese precedente (o con FATTURE.xlsx già caricati) e scarta le già viste. ⚠️ Falsi doppioni: un canone mensile identico ha numeri fattura diversi → il match si fa sul numero, **mai sull'importo**. *(contributo di Andrea, 2026-09-10)*
   - **Controllo inverso sulle fatture scartate come doppioni**: cerca le fatture tolte come doppioni nel CE del mese giusto. Se nessuno le ha caricate, mancano — caricale su quel mese (caso reale: cinque fatture mancanti, una da 30.000 €). Le una tantum grosse (es. un percorso di consulenza) restano fuori dal CE ordinario. Quando è disponibile la colonna dell'identificativo **SdI** (`Sdi`/`file` nel CSV AdE, `ID SdI` negli altri export), deduplica su quella e non sulla riga intera: fra due export sovrapposti la stessa fattura può differire in un campo secondario (caso reale: 307 righe, 212 fatture vere dopo la dedup su SdI). (contributo di Andrea Chirivì, 2026-10-12)
3. **Genera FATTURE.xlsx**:
   `python3 "$CDG_HOME/genera_fatture.py" "<file_unito>.csv"`
   Lo script pulisce gli apostrofi, converte gli importi, mette in **negativo** le note di credito e assegna le categorie leggendo dal master (Google Sheet).
4. **Fornitori nuovi** — se lo script segnala fornitori non mappati (li aggiunge temporaneamente al master come "Altro"):
   - Prima di cercare online, **leggi le RIGHE delle fatture del fornitore negli XML**. Il personale in somministrazione o distacco (ribaltamento costi del personale) non è un fornitore: non è fra le 9 categorie, si toglie da FATTURE.xlsx e va nelle righe del personale (r24-80 del modello mono-store). Le utenze anticipate dalla banca con addebito mensile fisso vanno in Utenze. Un consulente precedente si riconosce dalle fatture di "analisi"/"assistenza" e va in Servizi. (contributo di Andrea Chirivì, 2026-10-12)
   - cerca **online** ogni fornitore residuo per ragione sociale e deduci una categoria proposta. Categorie valide: `FORNITORI` (SOLO food, bevande, o comunque costi variabili — MAI attrezzature/impianti/beni strumentali anche se destinati alla cucina: vedi la sezione **Investimenti** sotto), `Servizi`, `Utenze`, `Piattaforme Delivery`, `Pubblicità - Marketing`, `Provvigioni`, `Materiali di consumo`, `Viaggi e trasferte`.
   - **REGOLA FERREA: mai assegnare una categoria a un fornitore nuovo senza conferma dell'utente, nemmeno quando la ricerca online dà un risultato ad alta confidenza.** Un caso reale (fornitore "START SRL", utility energetica omonima ma in realtà un'azienda di servizi) ha dimostrato che la ricerca online può portare a una categoria plausibile ma sbagliata. Quindi per OGNI fornitore nuovo — trovato online o no — fermati, elenca fornitore + categoria proposta (o "non trovato/incerto" se non lo trovi) + importo, e **aspetta il via libera dell'utente prima di proseguire**. Mai lasciare un fornitore in "Altro" di default.
   - **I residui si portano al TITOLARE in call** come lista "chi è e cosa vi vende" (caso reale: un giro ne ha riconosciuti 24 su 33). Subito dopo la call si riclassifica il foglio, si corregge il master con `correggi_categoria_master.py` e si **ricalcola l'EBITDA**. Riclassificazioni tipiche fuori dal food: consulente social, manutenzione frigo e arredi, auto (assistenza, gomme, gasolio), defibrillatore (per il defibrillatore chiedi al titolare se ha incassato il contributo a fondo perduto o lo sgravio INAIL — è una domanda, non un dato del CE). (contributo di Andrea Chirivì, 2026-10-12)
   - Nomi da riconoscere: **Foodinho = Glovo** (Piattaforme Delivery, vedi `dati-delivery-portali/SKILL.md`). **Meta Platforms = Pubblicità - Marketing**; se da un anno all'altro va a zero, hanno smesso di fare ads.
   - **Costo del lavoro nascosto nelle fatture** (contributo di Andrea Chirivì, 2026-10-12, da allineare con la regola "persone fisiche → social" qui sopra): per ogni persona fisica che fattura **chiedi cosa fa**; se fa i social va in Pubblicità - Marketing, se lavora in sala/cucina/bar (collaboratori a ritenuta, extra pagati con ritenuta d'acconto) è **costo del lavoro**: si toglie da FATTURE.xlsx e si scrive a mano nelle righe del personale, perché il loader lì non scrive (caso reale: 6.507 € di tre collaboratori finiti nella voce Servizi). Agenzie per il lavoro (es. agenzie di somministrazione): la somministrazione vera va nel personale, la sola selezione/ricerca pay-per-use (annunci) può restare in Servizi ma va etichettata come costo del lavoro in una sotto-voce o con una nota, perché il totale misura il turnover — se il team decide di spostarla nel personale, si applica la stessa regola della lettera (a). Se la fonte è Fatture in Cloud con tabella di raccordo, una voce generica tipo "costo per servizi" va aperta fornitore per fornitore prima di mapparla tutta in Servizi: senza queste regole il personale del CE risulta più basso del vero e i Servizi più alti.
   - solo dopo la conferma, aggiorna il master (Google Sheet) con le categorie confermate e **rigenera** FATTURE.xlsx.
   - **Verifica finale prima di procedere**: controlla che FATTURE.xlsx non contenga righe con Categoria = "Altro". Se ce ne sono, sono da chiedere all'utente, non da ignorare.

### Cosa sta fuori dai costi di gestione — INVESTIMENTI (contributo di Nicola, 2026-10-07, e di Andrea Chirivì, 2026-10-12; decisione di Marco sugli investimenti fuori EBITDA)
Attrezzature, arredi, sedie e tavoli, opere e lavori, demolizioni, cappa, insegna,
piatti personalizzati sono **INVESTIMENTI**: vanno nella riga "Investimenti (fuori
gestione)" **sotto l'EBITDA**, mai in Servizi o Materiali di consumo come diceva la
vecchia regola. Riparazioni e manutenzioni restano in **Servizi**. I consumabili
(es. detergente del forno) restano in **Materiali di consumo**. Le spese personali
del titolare (occhiali, vestiti) **escono dal CE** (`--escludi` negli script FIC e
TeamSystem, o scarto diretto in FATTURE.xlsx). Le voci dubbie si chiudono col
cliente. Lo stesso fornitore può vendere sia beni da investimento sia consumi: per
spostare la singola fattura usa una colonna "Categoria forzata" in FATTURE.xlsx (se
presente) oppure scrivi a mano l'importo nella riga del fornitore nella sezione
**Investimenti** del foglio — `carica_google_sheet.py` **non gestisce** la sezione
Investimenti (in dry-run la segnala come "Categorie NON trovate"): escludi quelle
righe da FATTURE.xlsx prima del `--write`, scrivi a mano gli importi nella sezione
Investimenti (riga del fornitore, o una riga vuota con il nome in colonna A, colonna
del mese) e nella verifica finale sommali al totale caricato dallo script, perché
devono quadrare col totale di FATTURE.xlsx. *(vedi anche `crea-cdg-cliente:98` e
`cdg-gruppo-bilanci-commercialista:29-31`)*

### Competenza: conguagli, arretrati, canoni e note di credito premio (contributo di Andrea Chirivì, 2026-10-12)
Nuovo controllo **prima del dry-run**, dopo aver gestito i fornitori nuovi. Il
loader mette ogni fattura nel mese della sua data di emissione: prima di caricare
cerca le fatture che coprono più mesi. Una fattura di arretrati si ripartisce sui
mesi di competenza o si scrive a mano sulla sua riga (caso reale: affitto 19.800 €
per 11 mesi in una fattura sola). Le utenze fatturate in ritardo vanno sul mese di
consumo, e le bollette a consumi stimati si segnalano. I canoni fatturati per più
mesi (auto, telefonia, abbonamenti annuali) si riducono al canone del mese e si
spalmano. Gli arretrati di un servizio fisso (es. commercialista) si normalizzano al
canone; la parte arretrata va nel Finanziario, che **non si tocca**: si segnala
soltanto. Per individuarle: importo molto sopra la media del fornitore, o
descrizione con "conguaglio", "arretrati", "periodo dal… al…".

⚠️ **Note di credito di premio** (premi contrattuali, a ettolitri, tipicamente
fornitori di bevande): vanno spalmate sui mesi in cui il premio è **maturato**, non
sul mese dell'accredito — un premio annuale azzera altrimenti il costo merce di un
mese solo (caso reale: NC di premio di 21.819,93 € netti ha quasi azzerato i costi
variabili di un mese). Si riconoscono da TD04 con causale/righe che parlano di
premio, bonus, obiettivi, ettolitri, importo molto più alto delle NC di reso
normali. Si chiede al titolare o al fornitore su quale periodo di acquisti è
maturato il premio (decisione da prendere col cliente o col consulente, soprattutto
se tocca mesi già presentati), poi si ripartisce sui mesi di maturazione: **da
decidere col team** se in proporzione agli acquisti del fornitore mese per mese
(regola usata nel CDG di gruppo, vedi `cdg-gruppo-bilanci-commercialista/SKILL.md`)
o a quote uguali. Il codice non va toccato: si aggiungono righe di rettifica in
FATTURE.xlsx intestate allo stesso fornitore con TipoDocumento "SPALMATURA PREMI"
(una riga positiva pari alla NC nel mese dell'accredito, una riga negativa per ogni
mese di competenza). Effetto collaterale da sapere: dopo la spalmatura la riga del
fornitore sul foglio non coincide più col mensile della fonte originale — tieni le
righe di rettifica nel confronto fatture-celle quando aggiorni un periodo già
caricato (vedi sotto), altrimenti il confronto segnala una differenza ogni mese. La
stessa NC va tenuta separata dai resi anche nell'analisi fornitori.

5. **Chiedi all'utente l'URL del foglio Google** del cliente.
6. **Dry-run** (nessuna scrittura):
   `python3 "$CDG_HOME/carica_google_sheet.py" FATTURE.xlsx "<url>"`
   Lo script rileva da solo il layout del foglio (vedi sotto) e mostra il riepilogo per ciascun foglio coinvolto.
   - **Se lo script segnala spazio insufficiente in una categoria**: NON esiste inserimento automatico di righe (rimosso deliberatamente — instabile). Lo script si ferma e stampa un riepilogo (categoria + quante righe servono + dopo quale riga inserirle). Riporta questo riepilogo all'utente **testuale, chiaro**, e chiedi di aggiungere lui le righe vuote nel punto indicato. Rilancia il dry-run dopo la sua conferma.
7. **Su conferma esplicita dell'utente, scrivi davvero**:
   `python3 "$CDG_HOME/carica_google_sheet.py" FATTURE.xlsx "<url>" --write`
8. **Verifica**: confronta i totali del foglio (colonne `TOTALE <anno>`) con i totali per categoria/anno calcolati da FATTURE.xlsx e riporta se quadra al centesimo. Su un foglio già popolato, verifica invece che le celle scritte fossero vuote prima (nessun raddoppio) e che la somma "Aggiunto" combaci col totale di FATTURE.xlsx. Il foglio Economico riceve l'**IMPONIBILE**: confronta sempre la colonna Imponibile di FATTURE.xlsx, mai il Lordo, altrimenti sembra che non quadri. La verifica si fa **MESE PER MESE e categoria per categoria**, non solo sul totale dell'anno: è l'unico controllo che vede uno sfasamento di date che a fine anno si compensa (vedi il caso ISO/dayfirst allo step 1). (contributo di Andrea Chirivì, 2026-10-12)

## Aggiornare un foglio già caricato (fatture arrivate dopo)

Non ricaricare due volte lo stesso periodo con lo script normale: gli importi si
SOMMANO. Per inserire fatture arrivate in ritardo in un periodo già caricato
(contributo di Andrea Chirivì, 2026-10-12 — la vecchia regola del 09/09 "i delta si
calcolano da FATTURE.xlsx" è SUPERATA):
1. Riscarica l'export **completo e fresco** del periodo, non solo le fatture nuove.
2. Confronta il totale fornitore×mese delle fatture con le **CELLE del foglio**, non
   con un FATTURE.xlsx vecchio: dopo scritture dirette sulle celle quel file non è
   più allineato.
3. Dove c'è differenza, scrivi nella cella il **TOTALE ricalcolato**, non sommare il
   delta al valore presente — così le fatture arrivate in ritardo entrano senza
   doppioni. (Oggi il loader standard SOMMA sempre: finché non esiste un'opzione
   dedicata, l'aggiornamento di celle già scritte va fatto a mano o con uno script
   ad hoc sul modello di `master_sheet.py`.)
4. Prima di scrivere, salva il piano e i valori di partenza (cella, prima, dopo) in
   un JSON di backup, per poter tornare indietro: il `_piano_scrittura_*.csv`
   attuale salva solo le celle-valore, non le formule `SUM`.
5. I fornitori nuovi si fermano comunque al dry-run e passano dalla regola ferrea
   del punto 4 della procedura.

## Layout del foglio Google — può variare, lo script si adatta da solo
- **Foglio unico "Economico"**: tutti gli anni affiancati in colonna (TOTALE 2025=B, gennaio=D…; TOTALE 2026=AB, gennaio=AD…), categorie in colonna A dalla riga 21. (Layout più comune.)
- **Modelli con più anni affiancati nello stesso blocco**: dal secondo blocco i mesi
  si chiamano "gennaio 2", "febbraio 3". ⚠️ **Bug noto (ancora presente)**: lo script
  può non riconoscere questi mesi e segnalare "Anni assenti dal foglio" — è un
  **errore che blocca**, non un semplice avviso, anche se oggi lo script lo stampa e
  prosegue comunque. Se lo vedi, fermati e verifica a mano le colonne mese prima di
  fidarti del caricamento. Stessa cautela se una **categoria risulta "NON trovata"**
  pur esistendo sul foglio con un nome leggermente diverso (alias) o se una riga è
  stata **rinominata a mano** dal cliente (es. "Axpo Italia S.p.A. (luce)"): in
  questi casi non creare una riga nuova, verifica prima col dry-run se è la stessa
  riga rinominata, e aggiungi l'alias nel master invece di rinominare la riga del
  cliente. Il match dei fornitori resta sul nome esatto in colonna A. (segnalato da
  Andrea Chirivì, 2026-10-12 — correzione nel codice ancora da portare nel plugin)
- **Fogli separati per anno**: tab distinte "Economico 2025", "Economico 2026", ecc., ciascuna con il proprio blocco anno. Lo script rileva automaticamente quale caso si applica (`resolve_worksheets`) e instrada ogni fattura al foglio giusto in base all'anno.
- **Categorie "contenitore" con sotto-voci**: a volte una categoria (es. "Servizi", "Materiali di consumo") non ha una riga-totale propria con `SUM`, ma è la somma di sotto-voci (Affitti, Software, Commercialista, Varie...). Il loader lo rileva da solo. In questo caso il fornitore viene cercato in TUTTE le sotto-voci insieme; se nuovo, va nella **prima riga libera di tutta l'area della categoria** (a prescindere da quale sotto-voce), SENZA mai toccare le intestazioni di sotto-categoria.
- **Cliente multi-punto-vendita**: il workbook ha una tab **per ogni punto vendita** (es. "Economico Store 1", "Economico Store 2", i nomi reali possono usare il nome del locale al posto di "Store N") + una tab di **riepilogo aggregato** (es. "Economico Aggregato") che è SOLO formule (pesca dagli store, es. `='Economico Store 1'!B2`) e NON va MAI passata come target di scrittura.
  - Individua tutte le tab del workbook (`ss.worksheets()`), riconosci quali sono i punti vendita.
  - Origine dati — due sotto-casi: (a) **P.IVA diverse per punto vendita** → ogni CSV Agenzia Entrate è già specifico di un punto vendita, stesso flusso di sempre, un CSV = un FATTURE.xlsx = una tab; (b) **stessa P.IVA per tutti i punti vendita** → il CSV unico non basta, servono gli **XML delle singole fatture elettroniche** (anche .p7m), usa `python3 "$CDG_HOME/estrai_fatture_xml.py" "<cartella>" --store "PAROLA1,PAROLA2=FATTURE_Store1.xlsx" --store "PAROLA3=FATTURE_Store2.xlsx"`.
    - **La destinazione NON è quasi mai (solo) nell'intestazione**: l'intestazione (CessionarioCommittente/Sede) spesso riporta un'unica sede legale fissa uguale per tutti i punti vendita — usarla come UNICA fonte assegna quasi tutto a un solo store (successo realmente: differenza di ~155k€ su un cliente, scoperta solo confrontando con un partitario del fornitore). Lo script cerca la destinazione vera in ordine di priorità: 1) riga per riga in `DettaglioLinee` (Descrizione o AltriDatiGestionali, qualunque etichetta usi il fornitore — "DEST MERCI", "Dest.Merce", ecc. — con "eredità" sulle righe successive fino al prossimo cambio); 2) nella Causale del documento; 3) nel testo di un eventuale PDF allegato alla fattura (bollette utenze/gas spesso hanno l'indirizzo SOLO lì); 4) l'intestazione, come ULTIMA istanza (per la maggior parte dei fornitori la varia correttamente, quindi va comunque usata quando non c'è nient'altro — solo NON come prima/unica fonte).
    - Per evitare falsi positivi (alcuni fornitori scrivono nomi di città che sono un proprio riferimento interno — es. il proprio punto vendita di ritiro o il proprio magazzino di spedizione, non la destinazione del cliente), un match riga/causale è accettato solo se il testo nomina anche il cliente/locale o usa un'etichetta esplicita inequivocabile (vedi `MARCATORI_CLIENTE`/`ETICHETTE_FORTI` in cima allo script — da adattare al nome del cliente specifico).
    - Se al termine restano fatture non classificate, lo script le segnala in `FATTURE_NON_CLASSIFICATE.xlsx` — copiane gli XML originali in una cartella dedicata e chiedi all'utente di controllarle (spesso lui trova il campo giusto guardando la fattura in un lettore, più veloce che indovinare altri pattern XML).
  - Per il caricamento, usa `python3 "$CDG_HOME/carica_google_sheet.py" FATTURE_storeN.xlsx "<url>" --sheet "Economico Store N" [--write]`: il flag `--sheet` forza la tab esatta per nome, bypassando la ricerca automatica "Economico"/"Economico <anno>". Ripeti dry-run→write→verifica per ogni punto vendita separatamente, mai sulla tab aggregata.
  - **(c) Stessa P.IVA, fatture che non dicono la destinazione, ma il locale tiene un registro bolle** (contributo di Andrea Chirivì, 2026-10-12): se il locale ha un registro giornaliero della merce arrivata con bolla (fornitore, numero documento, imponibile — anche se vive in un gruppo WhatsApp "spese"), i FORNITORI del CE si compilano **dal registro**. La differenza fra fatture e registro è la quota dell'altro locale: fai prima una controprova al centesimo su un mese. Se un fornitore serve solo quel locale, usa direttamente la fattura. Serve una tab "suddivisione" con registro, percentuale e fatture per fornitore, confrontata con la media storica. **Regola**: se si registra la merce con bolla settimana per settimana, NON si carica anche la fattura riepilogativa di fine mese, altrimenti la spesa raddoppia. Il registro dà anche i prezzi d'acquisto per il food cost (vedi `foodcost-cliente`).

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
- Lo script **SOMMA** sui valori già presenti nelle celle: **non ricaricare due volte lo stesso periodo** (raddoppia gli importi); per aggiornare un periodo con fatture arrivate dopo, usa la procedura in "Aggiornare un foglio già caricato" sopra, non un secondo caricamento.
- **Mai inserimento automatico di righe**: se manca spazio, lo script si ferma SEMPRE e chiede conferma prima di qualunque scrittura (anche parziale). Non bypassare mai questa regola.
- La sezione "Altro" sul foglio (diversa dal campo Categoria nel master), se creata, registra i dati ma **non** è collegata ai totali generali/EBITDA del foglio. Con la nuova regola "mai Altro nel master", questa sezione dovrebbe servire sempre più raramente.
- **Bug storico colonna Lordo (fix 2026-08-27, scoperto su Zio Bibbi):** prima di questa data `genera_fatture.py` riempiva la colonna Lordo con l'identificativo SDI del file invece che con Imponibile+Iva (totali in trilioni, errore evidente). Se hai FATTURE.xlsx generati prima del 27/8/2026 e li usi ancora, la colonna Lordo di quei file è sbagliata: rigenerali o ricalcola Lordo a mano come Imponibile+Iva.
