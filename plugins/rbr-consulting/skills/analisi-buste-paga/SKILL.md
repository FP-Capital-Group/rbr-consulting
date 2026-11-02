---
name: analisi-buste-paga
description: >-
  Metodo RBR per trasformare i PDF dei cedolini/buste paga di un ristorante in un Excel strutturato per l'analisi del costo del lavoro. Usala ogni volta che devi "analizzare le buste paga di un ristorante", "capire quanto costa un dipendente", "trasformare i cedolini in Excel", "calcolare il costo orario del personale" o "aggregare le buste paga di più società in un unico file". Estrae ~21 campi da qualsiasi software paghe (Zucchetti, TeamSystem, Paghe GB…) e produce un Excel a sezioni con formule di costo. È la logica dell'agente Tony resa skill: usala PRIMA di dare numeri sul costo del personale a un cliente.
---

# Analisi buste paga (cedolini PDF → Excel costo del lavoro)

## Perché esiste
Il costo del personale è la voce più pesante del conto economico di un ristorante e la più difficile da leggere: ratei, TFR, contributi datore e IRAP restano nascosti nel cedolino. Il ristoratore vede solo il netto pagato e sottostima il costo vero. Questa skill estrae dal PDF tutti i pezzi del **costo pieno annuo** (non solo la retribuzione del mese) e li mette in un Excel con formule, così il consulente può ragionare su costo orario reale, incidenza sul fatturato e confronto tra società. È la stessa logica dell'agente Telegram **Tony**, portabile fuori dal bot.

## Quando usarla
- Un ristoratore ti manda i cedolini (PDF, un file o uno per dipendente) e vuole capire il costo del lavoro.
- Devi caricare il costo del personale in un CDG / conto economico (dopo aver riconciliato con la skill `riconciliazione-dati-cliente`).
- Il cliente ha più società (es. Panino Genuino, Al Re, Amate) e vuole i costi aggregati o separati per società.
- Vuoi individuare anomalie nei cedolini prodotti dal consulente del lavoro.
- Il titolare paga parte del personale fuori busta (extra, tariffa a giornata) e vuoi il costo reale, non solo quello dichiarato.
- Serve uno scadenzario dei contratti a termine o un controllo del turnover.

## Prerequisiti
- PDF **testuali** (non scansioni-immagine): servono per l'estrazione. Se il PDF è una foto/scansione → passa da OCR prima (skill `pdf`).
- PDF **cifrati da password**: terzo caso oltre a testuale/scansione. Si apre con `pikepdf` (`password=...`) e si salva la copia decrittata nella cartella privata del cliente, mai in file condivisi. Password da provare in sequenza: codice ditta (cifre dopo "PG" nel nome file TeamSystem) → CF/P.IVA della società datrice → altre varianti note al cliente. **Non è una regola unica**: dipende dallo studio paghe, varia da cliente a cliente. Se nessuna apre, si chiede UNA volta al consulente del lavoro o al cliente. Dettagli per software paghe in `references/formati-cedolini.md`.
- Chiedi sempre allo studio paghe la versione **COMPLETA** del PDF del mese (non solo i cedolini): contiene anche riepilogo, F24 e prospetto "costo a consuntivo" per dipendente, cioè il costo azienda vero (vedi §1 e Regole).
- Se il cliente usa un portale paghe/presenze (es. Dipendenti in Cloud): chiedi subito un accesso con ruolo amministratore, così cedolini e timbrature si scaricano senza aspettare il cliente. Dettagli in `references/formati-cedolini.md`.
- `ANTHROPIC_API_KEY` disponibile (vedi `.env` del progetto Tony — mai scrivere la chiave nei file).
- Librerie Python: `pdfplumber` (estrazione testo), `pikepdf` (PDF cifrati), `anthropic` (estrazione JSON), `openpyxl` (Excel).
- Codice di riferimento riusabile: `RBR AI/agents/tony/core/extractor.py`, `core/excel_generator.py`, `prompts/system_prompt.py` — non obbligatorio: la lettura posizionale con `pdfplumber` (vedi `references/formati-cedolini.md`) non richiede né API key né quel repo.

## Procedura

### 1. Raccogli e ordina i cedolini
Metti insieme tutti i PDF. Annota per ognuno: dipendente, società, mese/anno. Se un dipendente ha più cedolini (mesi diversi) trattali come righe distinte — il costo si legge mese per mese, poi si annualizza.
- **Regola generale: si contano i NOMI, non i fogli.** Fanno fogli in più i doppi fogli dello stesso mese (vedi `references/formati-cedolini.md`), gli ingressi a metà mese e il foglio TFR di chi esce — un caso reale aveva 18 cedolini per 14 nomi.
- Il PDF del mese spesso è il **libro paga intero** (tutti i dipendenti in un unico file), non una busta singola: va spezzato per nome prima di procedere.
- **Da dove arrivano i cedolini**: cartella mandata dal cliente/consulente, oppure — se il cliente usa un portale paghe (Dipendenti in Cloud e simili) — download diretto con accesso amministratore. Dettaglio completo (percorso export, trappole: export che prende solo gli attivi, tredicesime che non escono nell'export) in `references/formati-cedolini.md`.
- Chiedi sempre, oltre ai cedolini, il **PDF completo del mese** (riepilogo + F24 + costo a consuntivo): è l'unica fonte solida del costo azienda vero (vedi Regole RBR e §3 compilazione).

### 2. Estrai il testo grezzo da ogni PDF
Usa `pdfplumber`: estrai sia il testo (`extract_text`, con `x_tolerance=2, y_tolerance=2`) sia le tabelle (`extract_tables`). I cedolini sono spesso tabellari: senza le tabelle perdi mezze colonne. Se non esce testo → il PDF è scansionato, fermati e fai OCR. Se il PDF è cifrato, decrittalo prima con `pikepdf` (vedi Prerequisiti).
- Per il **netto in busta**, la lettura posizionale per coordinate (`extract_words`) è più sicura dell'estrazione via LLM sul testo appiattito, che rischia di prendere la colonna sbagliata (es. ROL invece di netto). Coordinate per software paghe in `references/formati-cedolini.md` — sono tarate sui clienti visti finora e vanno **verificate a mano su una busta** prima di un'estrazione in blocco, confrontando il totale dei netti col riepilogo del PDF.

### 3. Estrai i ~21 campi via Claude (PDF → JSON)
Passa il testo grezzo a Claude con un system prompt da **consulente del lavoro italiano** (usa `prompts/system_prompt.py` di Tony come base). Chiedi SOLO un JSON valido, un oggetto per cedolino, con questi blocchi:
1. **dipendente** — cognome, nome, matricola, codice fiscale, data assunzione, qualifica, livello, CCNL, tipo contratto (FT/PT), % part-time, tempo determinato, **data fine contratto** (i cedolini la riportano quando il contratto è a termine — serve per lo scadenzario, vedi §4)
2. **azienda** — ragione sociale, P.IVA, sede, posizione INPS, posizione INAIL
3. **periodo** — mese, anno
4. **retribuzioni** — importo, contributi INPS datore, altri contributi datore, INAIL, totale
5. **tredicesima** e **6. quattordicesima** — rateo del mese + contributi + INAIL + totale
7. **altri_ratei** — ferie, ROL/permessi, ex festività (importo + contributi + INAIL)
8. **tfr** — quota del mese + totale maturato progressivo
9. **contributi_lavoratore** — INPS IVS, esonero contributivo, totale
10. **fiscale** — imponibile IRPEF, IRPEF lorda/netta, detrazioni, addizionali regionale/comunale, trattamento integrativo
11. **ore** — lavorabili, lavorate, straordinarie, assenze (malattia/altra), ferie/permessi goduti, festività
    più netto pagato, costo orario, note.

Regola ferrea del prompt: **se un campo non c'è → 0.0 / "" ; non inventare mai un valore. Se incerto → scrivilo in `note`.** Decodifica il JSON robustamente (trova il primo `{` e usa `raw_decode`).

### 4. Genera l'Excel a sezioni con openpyxl
Costruisci un foglio "Costo del Personale" con intestazioni raggruppate su due righe (riga 1 = gruppi, riga 2 = sottocolonne) e sezioni:
**Anagrafica** (matricola, cognome/nome, TD, periodo) · **Retribuzione** · **Contributi** (INPS, altri, INAIL mese, TFR maturato, totale) · **Ratei** (ferie, permessi, rateo 13ª, rateo 14ª, contributi sui ratei, INAIL su ratei, TFR sui ratei, totale) · **Costi Indiretti** · **Costo IRAP** · **Altri Costi** · **Totale mese** · **Ore Lavorate** · **Costo Orario**. Per l'analisi annua espandi con le colonne 13ª/14ª/Altri Ratei/TFR/Costo Annuo come richiesto dal cliente (~52 colonne complete).
Metti come **formule** (non valori) i totali e i derivati, così restano vivi:
- Totale contributi = `SUM(F:I)` · Totale ratei = `SUM(K:Q)`
- IRAP = `(Retribuzione + Tot.contributi + Tot.ratei) * 4.57%`
- Totale mese = `Retribuzione + Contributi + Ratei + Costi Indiretti + IRAP + Altri Costi`
- Costo orario = `Totale mese / Ore lavorate`
Aggiungi una **riga TOTALI** in fondo (SUM per colonna, costo orario = tot/tot). Formatta: `freeze_panes` sotto le intestazioni, `number_format="#,##0.00"`, righe alternate.
- Se nei cedolini compaiono contratti a tempo determinato, aggiungi un tab **"Scadenze contratti"**, ordinato per data di scadenza, con avviso a 30 giorni: il gestionale presenze del cliente spesso avvisa solo il giorno stesso, quindi questo tab è il preavviso utile. La decisione su rinnovo/proroga resta al titolare e al consulente del lavoro — la skill segnala, non decide.

### 5. Aggrega o separa per società (linguaggio naturale)
Il cliente parla, tu interpreti: "fai un unico Excel", "separali per azienda", "aggrega Al Re e Amate come Gruppo Z srl". Raggruppa i cedolini per `ragione_sociale` e genera un file per gruppo. Default se non dice nulla: un unico Excel con tutte le buste.

**Perimetro del locale quando la stessa società ha più sedi**: se la ragione sociale copre più locali, il PDF contiene i cedolini di tutti. Attribuisci ogni dipendente alla **sede stampata sul cedolino** (es. codice sede 0001 = locale A). Chi è stato assunto da poco può non averla ancora: in quel caso attribuiscilo con l'appello turni del locale (vedi `personale-oggi-domani` §1 per l'abbinamento soprannome↔cognome). Il perimetro — chi compare nei turni del locale — si fissa **una volta** e vale per ogni mese successivo: non si richiede al cliente "di chi è" ogni cedolino ogni volta. Chi lavora su due sedi va su due righe, ciascuna con la sua quota (es. ½). Senza questo filtro il costo del personale può risultare gonfiato da persone fuori dal perimetro del locale in analisi.

### 6. Controllo anomalie
Prima di consegnare, rileggi i numeri con occhio da consulente e segnala con ⚠️: costo orario fuori scala (< 8 €/h o > 40 €/h), contributi datore non ~29-32% della retribuzione, TFR ≈ retribuzione annua / 13,5 rispettato?, livello CCNL coerente con la qualifica, esonero contributivo applicato solo su imponibile mensile (non su ratei/TFR/arretrati).

**Casi che sembrano anomalie e non lo sono** — leggi la voce prima di segnalare, soprattutto per il controllo "costo orario < 8 €/h":
- un cessato che "incassa" un importo alto può essere un acconto TFR a rate dopo la cessazione: il costo azienda del mese resta minimo;
- chi è in malattia tutto il mese ha un netto pagato ma il costo è a carico INPS, non dell'azienda;
- una cessazione nel mese gonfia il netto con TFR e residui di ferie/permessi;
- pignoramenti (voce 3511, anche più di uno sullo stesso cedolino) e TFR pagato a rate sono trattenute/rateazioni, da separare dal costo del mese.

Per l'incidenza sul fatturato usa sempre il **costo azienda del prospetto a consuntivo**, mai la somma dei netti (vedi Regole, "Costo pieno ≠ retribuzione lorda").

**Il netto è stato pagato davvero? Quadratura cedolino ↔ bonifico.** Quando gli stipendi passano da banca, abbina ogni netto in busta al suo bonifico (stesso mese, stessa persona, importo al centesimo). Buchi tipici: 13ª/14ª senza bonifico corrispondente, mesi pagati solo con acconti, TFR finale pagato in parte. Un netto non pagato è un debito latente verso il dipendente (rischio di vertenza) — se nel CDG si scrivono i netti da cedolino, il costo del mese è pieno ma la cassa no: segnalalo al consulente, mai per iscritto al cliente. Stessa logica per gli F24: se sul conto non risultano gli addebiti delle deleghe, i contributi sono un debito, non un costo già pagato. Per gli aspetti legali rimanda sempre al consulente del lavoro. Non scrivere mai nomi di dipendenti in esempi o report su questo controllo.

### 7. Paghe miste: busta + extra fuori busta + pignoramenti
Si attiva quando il titolare paga parte del personale fuori busta o dice che le buste "non sono reali".
1. Il cedolino non basta: **costo del mese = netti in busta + extra fuori busta + pignoramenti trattenuti**.
2. Per ogni persona scrivi la regola dell'extra e falla confermare dal titolare. Possono essere: un fisso mensile, un importo per ogni giornata oltre un tetto settimanale, un importo per giorno della settimana, chiamate a tariffa differenziata per turno, un turno fisso. Questi extra sono **ADDITIVI**: si sommano alla busta.
3. La tariffa a giornata onnicomprensiva è invece un extra **SOTTRATTIVO**: maturato = giorni × tariffa + giornate doppie × extra + quota forfettaria 13ª/14ª; si tolgono netto in busta e pignoramento, e quello che resta è l'extra in contanti. Tieni additivi e sottrattivi in colonne distinte.
4. Il pignoramento si legge ogni mese dal cedolino (voce 3511, possono essere due su uno stesso cedolino) e **mai come rata fissa**.
5. Prima di contare il foglio presenze chiarisci la notazione col cliente: può essere "1 = giornata normale, 2 = giornata doppia con extra" per i contrattualizzati, mentre per extra/chiamate il numero può essere direttamente l'importo. Leggere tutto con una regola sola porta a errori di conto. **Senza il foglio presenze del mese non si calcolano extra né tariffa giornaliera: si segnala il buco, non si stima.**
6. Le regole si riconfermano quando cambiano le aperture del locale (es. apertura di un nuovo giorno della settimana cambia cosa si intende per "oltre il tetto settimanale").
7. Se la busta copre solo una piccola parte del cash, ricostruisci il costo dalle figure dettate dal titolare (es. figura a giornata × giorni + fisso in busta + extra a servizio). Gli F24 restano l'ancora della parte dichiarata.
8. Nel CDG gli extra vanno nella riga "Extra stipendi", mai sommati sotto la formula dei contributi.

Negli esempi scritti nel plugin: niente nomi di dipendenti, niente pignoramenti abbinati a una persona.

## Regole RBR & trabocchetti
- **CCNL principale = Turismo/Ristorazione (FIPE)**; livelli 3°=cuoco/barman, 4°=aiuto cuoco/barista, 5°=lavapiatti/fattorino; 14ª erogata a luglio. Ma la skill deve gestire QUALSIASI CCNL e QUALSIASI software paghe.
- 🟡 **Aggiornamento contrattuale (segnalato agosto 2026)**: dal 1° giugno 2026 è scattata la terza tranche di aumento CCNL Confcommercio-FIPE (+40€ lordi al 4° livello, proporzionale sugli altri); per la ristorazione collettiva l'aumento previsto a giugno slitta a settembre 2026. Dal luglio 2026 parte inoltre la previdenza complementare di settore ospitalità. Se un cedolino di un cliente su questo CCNL non riflette l'aumento dal mese corretto, segnalalo come possibile errore payroll invece di darlo per scontato — verificare sempre col consulente del lavoro del cliente prima di correggere numeri.
- **Costo pieno ≠ retribuzione lorda**: includi sempre contributi datore + INAIL + ratei + TFR + IRAP. È l'errore più comune del ristoratore. Per il **costo azienda vero** segui questa gerarchia delle fonti, in ordine: 1) prospetto "costo a consuntivo" per dipendente (nel PDF completo del mese); 2) F24 del mese, ancora della parte dichiarata; 3) solo in mancanza dei primi due, una stima scritta ESPLICITAMENTE come stima (es. imponibile×1,30 o lordo×1,60 o formula del CE sui netti), da sostituire appena arrivano gli F24. Nessun moltiplicatore unico è affidabile: le stime possono divergere anche del 10-15% l'una dall'altra e dal dato reale — non scrivere un costo azienda definitivo basato solo su una stima.
- **Confronti tra anni**: il costo dichiarato in busta può crescere da un anno all'altro per pura ricomposizione (es. una persona passata a tempo pieno, un collaboratore uscito dalla busta), senza un euro di costo cash in più. Nei confronti anno su anno — soprattutto quando il compenso RBR dipende dallo sviluppo del margine — usa lo **stesso criterio di costo del personale nei due anni** (es. costo cash pieno in entrambi): col solo costo dichiarato lo sviluppo può uscire negativo per costruzione. Rimando incrociato: `riconciliazione-dati-cliente` §2 e `cdg-gruppo-bilanci-commercialista` per i confronti "a parità di locali".
- **PDF scansionati**: `pdfplumber` non estrae nulla → riconoscilo subito, non consegnare un Excel di zeri.
- **Mai la API key nei file** (repo condivisa col team): riferisci `.env` / `ANTHROPIC_API_KEY`. Stessa regola per le **password dei PDF cifrati**: non si scrivono mai nei file condivisi, nel plugin o nei report, solo nella memoria privata del cliente.
- **Non è consulenza fiscale personalizzata**: è analisi di costo. Per obblighi/adempimenti rimanda al consulente del lavoro del cliente.
- Prima di caricare in un CDG, passa da `riconciliazione-dati-cliente`: i numeri vanno riconciliati e discussi, non compilati al volo.
- **Turnover e costo del lavoro fuori dai cedolini**: le fatture pay-per-use di ricerca personale (agenzie/portali annunci) misurano il turnover anche senza dati HR — affiancale alle cessazioni del prospetto a consuntivo (fonte: `cdg-fatture`). I collaboratori a ritenuta finiti nel "costo per servizi" sono costo del lavoro: segnalali e sommali al personale invece di lasciarli nascosti in un'altra voce.
- Emoji di sistema RBR: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Fonti/contributi
(contributo di Andrea Chirivì, 2026-10-12)

## Definition of Done
- [ ] Un oggetto JSON estratto per ogni cedolino, con i ~21 campi (0.0/"" dove assente, niente valori inventati)
- [ ] PDF scansionati riconosciuti e gestiti (OCR o segnalati), non consegnati come zeri
- [ ] PDF cifrati riconosciuti e aperti
- [ ] Cedolini completi, cessati compresi, e 13ª/14ª presenti (lette dall'export o dal pannello del portale paghe) prima di annualizzare
- [ ] Excel a sezioni generato con totali/IRAP/costo orario come FORMULE + riga TOTALI
- [ ] Aggregazione/separazione per società fatta secondo la richiesta del cliente, col perimetro per sede verificato se il cliente ha più locali
- [ ] Controllo anomalie eseguito (incluse le casistiche che sembrano anomale e non lo sono) e anomalie segnalate con ⚠️
- [ ] Se ci sono contratti a termine: scadenzario aggiornato
- [ ] Nessuna API key/password/segreto scritto nel file
- [ ] Se destinato a un CDG: riconciliazione fatta PRIMA della compilazione
