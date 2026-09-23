---
name: riconciliazione-dati-cliente
description: Metodo RBR per validare i dati di un nuovo cliente PRIMA di scriverli nel controllo di gestione. Usala ogni volta che ricevi un dataset cliente (export gestionale, PDF fatture, email con incassi, cedolini, file Excel del commercialista) e devi caricarlo in un CDG o conto economico. Produce una panoramica dati con anomalie e decisioni di mapping aperte da discutere col cliente/consulente prima di compilare. NON iniziare mai a compilare un CDG senza aver prima riconciliato con questa skill.
---

# Riconciliazione dati cliente (panoramica prima di compilare)

## Perché esiste
In RBR i numeri finiscono in file che il ristoratore usa per decidere. Un caricamento frettoloso assorbe bug sistematici (es. finestre export Zucchetti che perdono sempre l'ultimo giorno del mese) e scelte di mapping sbagliate (IVA, categorie, sconti) che poi inquinano tutto il conto economico. La regola d'oro RBR: **prima si riconcilia e si discute, poi si compila.** Non saltare mai questo passaggio, nemmeno se il dataset sembra pulito.

## Quando usarla
- Ricevi dati di un cliente nuovo da caricare in un CDG / conto economico / KPI.
- Ricevi un nuovo periodo di dati per un cliente esistente.
- Un dato sembra "mancante" o "strano" e stai per dichiararlo assente.

## Procedura

### 1. Raccogli tutto
Metti insieme ogni fonte: export gestionale (iPratico, Zucchetti, TeamSystem…), PDF fatture SDI, email, allegati, Excel del commercialista. Non fermarti al primo file: un dato può essere nel **corpo di una email** e non in allegato.
- **Il file locale non è il file**: un file del cliente scaricato in cartella può essere una versione vecchia, mentre il compilato sta su Drive con lo stesso identico nome, modificato dopo (visto: food cost "vuoto" in locale e pieno su Drive). Prima di dichiarare un dato mancante controlla la versione su Drive (`modifiedTime`). *(contributo di Andrea, 2026-09-10)*
- **Allegati Gmail via MCP**: il connettore Gmail legge i messaggi ma non scarica gli allegati. Fai `get_message` con `messageFormat: "RAW"` e poi estrai il campo `raw` in modo **meccanico** dai file che Claude Code scrive da sé (transcript `~/.claude/projects/<progetto>/<sessione>.jsonl`, o il file in `tool-results/` se l'output era troppo grande). **Mai ricopiare a mano il base64** (due tentativi su due corrotti). Poi `base64.urlsafe_b64decode` → `email.message_from_bytes` → `get_payload(decode=True)`, e per xlsx/docx SEMPRE `zipfile.ZipFile(...).testzip()` prima di dichiarare il file buono. *(contributo di Andrea, 2026-09-10)*
- **Estrazioni dai gestionali del cliente** (con la sua sessione nel browser): iPratico → skill `estrai-dati-ipratico`; **Fatture in Cloud** (spese, note di credito, righe fattura) → `memory/fatture_in_cloud.md`; **Cassa in Cloud** (venduto per fascia, coperti per ora) → `memory/cassa_in_cloud.md` (repo rbr-suite).

### 2. Riconcilia contro totali indipendenti
Per ogni periodo, confronta la somma dei dati di dettaglio contro un totale che arriva da un'altra fonte (fatturato annuale dichiarato, YTD del commercialista, totale iPratico). **Quantifica ogni scarto** (in € e in %). Uno scarto non spiegato è un problema da capire, non da ignorare.

Controlli tipici che salvano da errori:
- **Finestre export**: molti gestionali tagliano il primo o l'ultimo giorno del periodo. Verifica che i giorni ci siano tutti.
- **IVA**: valori IVA inclusa o esclusa? Regola RBR: economici sempre IVA **esclusa** (÷1.1 ristorazione, ÷1.22 altro). Se non specificato → assumi esclusa e segnala con ⚠️.
- **Sconti / storni / resi**: capisci se sono già netti o vanno sottratti.
- **Canali**: sala / delivery / asporto / cerimonie mappati coerentemente.
- **Tre fonti, tre ricavi**: per lo stesso mese e sede CDG 195.763 € · contabilità 216.421 € · cassa POS 219.497 € lordi (caso reale). Lo scarto va spiegato PRIMA di mostrare un cruscotto al cliente. *(contributo di Luciano Purpi, 2026-09-03)*
- **Prima di dare la colpa alla cucina, riconcilia le Z**: uno scostamento di food cost di +7 punti su un locale era in buona parte un ricavo che nel CDG non c'era (5.651 € di Z fiscali non registrate a giugno); sui ricavi veri scendeva a +4,8 punti. *(contributo di Luciano Purpi, 2026-09-03)*
- **CDG ereditato** (non costruito da RBR): colonne-anno sfalsate, lordizzatori che raddoppiano il personale, sotto-totali persi, EBITDA di locale vs di gruppo → checklist nella skill `crea-cdg-cliente`.

### 3. Se un dato "manca", cercalo in più modi
Prima di scrivere "dato mancante": cerca per mittente, per testo nel corpo delle email, per periodo, in cartelle diverse, in formati diversi (testo vs PDF vs foto). Il 90% dei "dati mancanti" esistono ma sono in un formato che la prima ricerca non ha intercettato.

### 4. Produci la panoramica
Genera due file (condividili subito come Editor con il cliente/consulente):
- **Panoramica.md** — riepilogo leggibile: cosa hai ricevuto, coperture per periodo, riconciliazioni con scarti quantificati, **anomalie numerate**, **decisioni di mapping aperte numerate** (es. "1. La voce X va sotto Costi variabili o Personale?").
- **Panoramica.xlsx** — tabella periodo × fonte con totali, scarti e flag anomalie.

Usa le emoji di sistema RBR: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore.

### 5. Discuti, poi compila
Porta la panoramica alla persona giusta (Marco / il consulente / il cliente), chiudi le decisioni aperte, e **solo dopo** scrivi nel CDG. Per la compilazione vera e propria vedi la skill `crea-cdg-cliente`.

## Definition of Done
- [ ] Ogni periodo riconciliato contro un totale indipendente, scarti quantificati
- [ ] Nessun "dato mancante" dichiarato senza averlo cercato in ≥3 modi
- [ ] IVA esplicitata (inclusa/esclusa) per ogni fonte
- [ ] Panoramica.md + .xlsx prodotti e condivisi
- [ ] Decisioni di mapping numerate e discusse PRIMA di toccare il CDG
