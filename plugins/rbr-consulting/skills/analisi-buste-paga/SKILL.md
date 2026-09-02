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

## Prerequisiti
- PDF **testuali** (non scansioni-immagine): servono per l'estrazione. Se il PDF è una foto/scansione → passa da OCR prima (skill `pdf`).
- `ANTHROPIC_API_KEY` disponibile (vedi `.env` del progetto Tony — mai scrivere la chiave nei file).
- Librerie Python: `pdfplumber` (estrazione testo), `anthropic` (estrazione JSON), `openpyxl` (Excel).
- Codice di riferimento riusabile: `RBR AI/agents/tony/core/extractor.py`, `core/excel_generator.py`, `prompts/system_prompt.py`.

## Procedura

### 1. Raccogli e ordina i cedolini
Metti insieme tutti i PDF. Annota per ognuno: dipendente, società, mese/anno. Se un dipendente ha più cedolini (mesi diversi) trattali come righe distinte — il costo si legge mese per mese, poi si annualizza.

### 2. Estrai il testo grezzo da ogni PDF
Usa `pdfplumber`: estrai sia il testo (`extract_text`, con `x_tolerance=2, y_tolerance=2`) sia le tabelle (`extract_tables`). I cedolini sono spesso tabellari: senza le tabelle perdi mezze colonne. Se non esce testo → il PDF è scansionato, fermati e fai OCR.

### 3. Estrai i ~21 campi via Claude (PDF → JSON)
Passa il testo grezzo a Claude con un system prompt da **consulente del lavoro italiano** (usa `prompts/system_prompt.py` di Tony come base). Chiedi SOLO un JSON valido, un oggetto per cedolino, con questi blocchi:
1. **dipendente** — cognome, nome, matricola, codice fiscale, data assunzione, qualifica, livello, CCNL, tipo contratto (FT/PT), % part-time, tempo determinato
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

### 5. Aggrega o separa per società (linguaggio naturale)
Il cliente parla, tu interpreti: "fai un unico Excel", "separali per azienda", "aggrega Al Re e Amate come Gruppo Z srl". Raggruppa i cedolini per `ragione_sociale` e genera un file per gruppo. Default se non dice nulla: un unico Excel con tutte le buste.

### 6. Controllo anomalie
Prima di consegnare, rileggi i numeri con occhio da consulente e segnala con ⚠️: costo orario fuori scala (< 8 €/h o > 40 €/h), contributi datore non ~29-32% della retribuzione, TFR ≈ retribuzione annua / 13,5 rispettato?, livello CCNL coerente con la qualifica, esonero contributivo applicato solo su imponibile mensile (non su ratei/TFR/arretrati).

## Regole RBR & trabocchetti
- **CCNL principale = Turismo/Ristorazione (FIPE)**; livelli 3°=cuoco/barman, 4°=aiuto cuoco/barista, 5°=lavapiatti/fattorino; 14ª erogata a luglio. Ma la skill deve gestire QUALSIASI CCNL e QUALSIASI software paghe.
- 🟡 **Aggiornamento contrattuale (segnalato agosto 2026)**: dal 1° giugno 2026 è scattata la terza tranche di aumento CCNL Confcommercio-FIPE (+40€ lordi al 4° livello, proporzionale sugli altri); per la ristorazione collettiva l'aumento previsto a giugno slitta a settembre 2026. Dal luglio 2026 parte inoltre la previdenza complementare di settore ospitalità. Se un cedolino di un cliente su questo CCNL non riflette l'aumento dal mese corretto, segnalalo come possibile errore payroll invece di darlo per scontato — verificare sempre col consulente del lavoro del cliente prima di correggere numeri.
- **Costo pieno ≠ retribuzione lorda**: includi sempre contributi datore + INAIL + ratei + TFR + IRAP. È l'errore più comune del ristoratore.
- **PDF scansionati**: `pdfplumber` non estrae nulla → riconoscilo subito, non consegnare un Excel di zeri.
- **Mai la API key nei file** (repo condivisa col team): riferisci `.env` / `ANTHROPIC_API_KEY`.
- **Non è consulenza fiscale personalizzata**: è analisi di costo. Per obblighi/adempimenti rimanda al consulente del lavoro del cliente.
- Prima di caricare in un CDG, passa da `riconciliazione-dati-cliente`: i numeri vanno riconciliati e discussi, non compilati al volo.
- Emoji di sistema RBR: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Un oggetto JSON estratto per ogni cedolino, con i ~21 campi (0.0/"" dove assente, niente valori inventati)
- [ ] PDF scansionati riconosciuti e gestiti (OCR o segnalati), non consegnati come zeri
- [ ] Excel a sezioni generato con totali/IRAP/costo orario come FORMULE + riga TOTALI
- [ ] Aggregazione/separazione per società fatta secondo la richiesta del cliente
- [ ] Controllo anomalie eseguito e anomalie segnalate con ⚠️
- [ ] Nessuna API key/segreto scritto nel file
- [ ] Se destinato a un CDG: riconciliazione fatta PRIMA della compilazione
