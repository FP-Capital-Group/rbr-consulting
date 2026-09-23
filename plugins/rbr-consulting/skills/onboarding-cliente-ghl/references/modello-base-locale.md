# Modello base di un sotto-account GHL per un locale: tre strati, nove flussi

(contributo di Luciano Purpi, 13/09/2026 — corretto dallo stesso il 14/09/2026 sul flusso 01;
regole su etichette e conti ereditati: contributo di Luciano Purpi, 13/09/2026)

Nasce dal confronto fatto il 13/09/2026 sui tre conti più avanti dell'agenzia: Mister Pizza
(`MF9NMKJn2givlRrTq3gw`), Barresi (`eFE9eUM30l0IVXim3xYn`), Noolas Pub (`KisUjQ6csrLVcYPIueLT`).
La struttura è UGUALE su ogni locale: cambia il contenuto (offerta, testi, tempi), non la struttura.
È la struttura target oltre lo Snapshot `RBR Blueprint v1` (che oggi porta 14 campi e 2 workflow):
usala per completare un conto nuovo o riordinarne uno ereditato.

## I tre strati, in quest'ordine

Saltarne uno per arrivare prima al terzo è il modo standard di bruciare un cliente.

1. **FONDAMENTA** — chi è la persona e cosa ha fatto: campi standard, consensi per canale, ponte
   gestionale → CRM. È quello che manca sempre ed è l'unico che non si improvvisa dopo: senza data
   ultima visita e numero visite nel contatto non esistono stati, freno, riaggancio.
2. **SERVIZIO** — quello che il cliente si aspetta: conferma, promemoria, disdetta, risposta a chi
   scrive, recensione. Va PRIMA del marketing: atteso, costa poco, non genera segnalazioni, riempie
   il canale di traffico legittimo e salva coperti veri.
3. **CRESCITA** — quello che vogliamo noi: benvenuto con riscatto misurato, racconto, premio, riaggancio.

## I nove flussi standard

Nomi uguali su ogni cliente, convenzione `<nn> · <nome> — <canale>`. Mai lasciare "New Workflow: 1788…".

| # | Flusso | Note |
|---|---|---|
| 01 | Ponte prenotazioni — stato | Innesco su **Contact Changed del campo di stato** (es. `statoprenotazione` ∈ {seated, finished}), NON su "tag aggiunto" (vedi sotto). Scrive i campi di visita; matching sul telefono +39 con i duplicati spenti; il ramo che conferma non riscrive mai sul gestionale (anti-loop) |
| 02 | Stato cliente — ricalcolo giornaliero | Legge i campi, scrive UN solo tag `stato-*`, toglie il precedente |
| 03 | Smistamento lead in entrata | Normalizza, mette fonte e `pv`, se un dato manca mette `errore-<cosa>`. Due flussi separati se arrivano lead anche via API dal gestionale: dati diversi, e il fallimento di uno non ferma l'altro |
| 04 | Conferma prenotazione — WhatsApp | Utility. NON chiedere di confermare: un "confermo" non produce niente, un "annullo" rimette il tavolo in vendita |
| 05 | Promemoria 4 ore prima | Il flusso con più iscritti (2.135 su Noolas, 1.714 su Mister Pizza): ogni disdetta anticipata è un tavolo rivenduto |
| 06 | Prenotazione cancellata | Niente promo dentro: una disdetta non è un momento di vendita |
| 07 | L'orecchio — risposte in entrata | Customer Replied; le risposte-pulsante si chiudono da sole, il resto sveglia UNA persona su UN numero; dentro il ramo STOP. Su Noolas era ancora in bozza: il buco più caro dei tre conti |
| 08 | Recensione dopo la visita | Il motore è già dentro GHL, spesso configurato e MAI acceso |
| 09 | Benvenuto con riscatto | Consegna coupon → promemoria se non riscattato → RISCATTO IN SALA (modulo aperto dal QR, precompilato col contatto, due soli campi in cassa: coperti e scontrino). Il terzo pezzo è quello che salta sempre |

**Avvisi allo staff** (07, disdette, modifiche): mai "Notifica interna" SMS se il sotto-account non
ha Sistema telefonico → vedi `suite/memory/gohighlevel.md`, sezione Notifica interna.

### Flusso 01: i tag del ponte si sommano, si innesca sul CAMPO (correzione 14/09/2026)

La regola "il tag che innesca un flusso va rimosso in coda al flusso" vale solo per i tag CHE
SCRIVIAMO NOI. I tag che arrivano dal ponte del gestionale (Make/M3R/integrazioni di terzi) di norma
SI SOMMANO e nessuno li toglie: su Barresi un contatto ha `status_confirmed` E `status_seated`,
un altro `status_confirmed` E `status_cancelled`.

- **Conseguenza:** "Etichetta aggiunta: status_seated" scatta SOLO alla prima visita e poi mai più.
  Il funnel sembra funzionare in collaudo (il primo giro parte) e muore in silenzio dal secondo.
- **Regola:** i TAG servono a SEGMENTARE, il CAMPO serve a INNESCARE. Il campo di stato viene
  sovrascritto a ogni evento dal ponte → l'innesco ripetibile è **Contact Changed** sul campo.
- **Verifica in 10 secondi:** apri 2-3 contatti che hanno prenotato più volte. Due `status_*` insieme
  sullo stesso contatto = i tag si sommano e ogni trigger "tag aggiunto" del conto è rotto dal secondo giro.
- **Calendario:** il calendario GHL alimentato dal ponte NON dice chi è venuto (Barresi: 32
  appuntamenti tutti "Confirmed", anche quelli passati e seated). O si chiede al ponte di aggiornare
  lo stato su BOOKING_UPDATED (seated/finished → Showed, noshow → No-Show, cancelled → Cancelled),
  o ci si basa solo sul campo di stato del contatto.
- **Effetto buono:** con il campo che si aggiorna da solo, i quattro dati di visita (data ultima
  visita, numero visite, media coperti, esito) si costruiscono DENTRO GHL su Contact Changed, senza
  chiederli al fornitore del ponte (su Barresi ha sbloccato il freno del funnel tre settimane prima).

## Cosa NON mettere nel modello base

- Pipeline/opportunità: servono a chi vende preventivi, non a chi riempie tavoli.
- Matrice RFM a 125 celle: i campi `rfm_recenza/frequenza/monetario` esistono su tutti e tre i conti
  e su tutti e tre sono VUOTI.
- Ramo lingua se non c'è davvero turismo.

## Campi standard (stessi nomi ovunque, i flussi si copiano senza rimappare)

- **Visita:** `nprenotazionicliente`, `ncancellazionicliente`, `nnoshowscliente`, `data_ultima_presenza`,
  `numerodipersone`, giorno/orario prenotazione, `statoprenotazione`, `fonteresmio`
- **Riscatto:** `coperti_riscatto`, `scontrino_riscatto`, `codicesconto`, `linkqr_offerta`
- **Consenso:** `gdpr_email`, `gdpr_whatsapp`, `marketing_consent`, `privacy_policy`
- **Persona:** `compleanno_gg_mm` (giorno e mese SENZA anno: l'anno quasi nessuno lo dà), `lingua`, `area`, `pv`
- **Calcolato:** `stato_cliente`

Tipi: contatori = **Numero**, date = **Data** (su Mister Pizza i contatori sono Linea singola, quindi
"più di 3 visite" non si filtra). Scontrino = **Numero in euro interi, MAI Monetario**: il Monetario
di GHL è a virgola italiana e in cassa 27,80 diventa 2780 senza avviso.

## Valori personalizzati

Mister Pizza e Noolas ne hanno ZERO: ogni frase variabile è murata nelle email. Barresi ha
`novita_del_mese`, una riga che il titolare aggiorna in un punto solo: tiene viva un'automazione
per anni invece che per due mesi, e costa dieci minuti.

## Etichetta = stato, campo = dato

Contati il 13/09/2026: Mister Pizza 61 etichette, Barresi 1.244, Noolas 1.093. Barresi e Noolas
vengono dallo stesso stampo: risposte dei sondaggi e anno di nascita finiti IN ETICHETTA (anno 1942,
18-25, 20-30, abbondanza…), con duplicati esatti creati a due ore di distanza. Mille etichette non
sono un patrimonio, sono un archivio che nessuno può interrogare.

- **Regola:** se la risposta può essere una fra tante (anno, fascia d'età, piatto preferito) è un
  CAMPO. Se è una condizione che si accende e si spegne (`status_confirmed`, `coupon-riscattato`,
  `stato-abituale`) è un'ETICHETTA.
- **Famiglie ammesse:** `status_<stato>` (prenotazione) · `stato-<nome>` (cliente) ·
  `<campagna>-<stato>` (ciclo coupon) · `<n>-invio-<catenaria>` (passo) · `pv-<nome>` (con `pv-unknown`
  che esiste, così si conta) · `turista`/`locale` + `-ita`/`-eng` solo dove serve · `errore-<cosa>` ·
  igiene (`email-non-valida`, `whatsapp-stop`). Minuscolo, trattini, niente spazi. Un contatto sta in
  UNO stato per famiglia: il nuovo tag sostituisce, non si somma (per i tag nostri).
- **Etichette di errore (da Mister Pizza, da mettere su ogni conto):** `errore funnel`,
  `errore funnel turista o locale`, `errore-qr`. Quando un dato manca il flusso lo DICHIARA invece di
  proseguire zoppo: è l'unico modo di accorgersi che qualcosa non gira prima che lo dica il cliente.
- **I quattro stati del coupon come cruscotto:** inviato → scaricato → riscattato → scaduto.
  Inviati ≫ scaricati = il messaggio non convince. Scaricati ≫ riscattati = MANCA IL MECCANISMO IN
  SALA, non è il coupon sbagliato (Noolas: 646 consegnati, 60 riscattati). Riscattati alti ma coperti
  bassi = l'offerta attira chi viene da solo.

## Due segnali da leggere nella lista flussi (prima di aprire qualunque cosa)

Le colonne "Iscritti totali" e "Iscritti attivi" dicono in dieci secondi cosa gira davvero:
- **pubblicato con 0 iscritti** = non è mai partito, o l'innesco è sbagliato;
- **bozza con iscritti attivi** = gente ferma dentro un flusso spento da mesi (Funnel RBR su Noolas:
  93 attivi in bozza). La cosa più facile da non vedere e la più sgradevole da spiegare;
- **due flussi con innesco quasi uguale** = uno ruba i contatti all'altro.

Altro segnale (contributo di Luciano Purpi, 10/09/2026): dashboard con "conversion rate 0%" su
centinaia di opportunità aperte = il cliente non chiude le opportunità nel CRM e tiene le vendite
in un foglio.

## Riordino di un conto ereditato, in quest'ordine

1. Conta le etichette (oltre ~150 su un locale c'è un archivio travestito: porta le famiglie in
   campi, ma non cancellare finché non sai chi le legge).
2. Leggi iscritti totali/attivi di ogni flusso.
3. Guarda l'anello del riscatto.
4. Collauda i link delle email PRIMA di riaccendere qualsiasi cosa (skill `mail-funnel-ghl`,
   `references/collaudo-catenaria.md`).
5. Rinomina o cancella i New Workflow senza nome e i "test"/"migrazionecampo".
6. Solo adesso aggiungi.
