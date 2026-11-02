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

### Import dal gestionale per chi è venuto prima del tracciamento

(contributo di Luciano Purpi, 2026-10-12)

Per i clienti venuti prima che `ultima_visita` esistesse: export dal gestionale con stato in
(`finished`, `seated`) → dedup per telefono → CSV in Contatti → Importa, modalità "Crea e aggiorna",
con un tag di lotto `recupero-<data>` → filtro per tag → azione di massa. L'import riempie anche
`ultima_visita`. Per separare le lingue: filtro annidato "Etichetta è `recupero-<data>`" AND NON
`recensione-richiesta`, dopo aver accodato gli italiani. Dettagli import da pannello:
`sistema-tracciamento-locale/playbook.md`.

## I nove flussi standard

Nomi uguali su ogni cliente, convenzione `<nn> · <nome> — <canale>`. Mai lasciare "New Workflow: 1788…".

| # | Flusso | Note |
|---|---|---|
| 01 | Ponte prenotazioni — stato | Innesco su **Contact Changed del campo di stato** (es. `statoprenotazione` ∈ {seated, finished}), NON su "tag aggiunto" (vedi sotto). Scrive i campi di visita; matching sul telefono +39 con i duplicati spenti; il ramo che conferma non riscrive mai sul gestionale (anti-loop) |
| 02 | Stato cliente — ricalcolo giornaliero | Legge i campi, scrive UN solo tag `stato-*`, toglie il precedente |
| 03 | Smistamento lead in entrata | Normalizza, mette fonte e `pv`, se un dato manca mette `errore-<cosa>`. Due flussi separati se arrivano lead anche via API dal gestionale: dati diversi, e il fallimento di uno non ferma l'altro |
| 04 | Conferma prenotazione — WhatsApp | Utility. NON chiedere di confermare: un "confermo" non produce niente, un "annullo" rimette il tavolo in vendita |
| 05 | Promemoria 4 ore prima | Il flusso con più iscritti (2.135 su Noolas, 1.714 su Mister Pizza): ogni disdetta anticipata è un tavolo rivenduto — uscita e guardie: vedi sotto |
| 06 | Prenotazione cancellata | Niente promo dentro: una disdetta non è un momento di vendita — vedi sotto |
| 07 | L'orecchio — risposte in entrata | Customer Replied; le risposte-pulsante si chiudono da sole, il resto sveglia UNA persona su UN numero; dentro il ramo STOP. Su Noolas era ancora in bozza: il buco più caro dei tre conti |
| 08 | Recensione dopo la visita | Il motore è già dentro GHL, spesso configurato e MAI acceso — schema completo sotto |
| 09 | Benvenuto con riscatto | Consegna coupon → promemoria se non riscattato → RISCATTO IN SALA (modulo aperto dal QR, precompilato col contatto, due soli campi in cassa: coperti e scontrino). Il terzo pezzo è quello che salta sempre |

**Avvisi allo staff** (07, disdette, modifiche): mai "Notifica interna" SMS se il sotto-account non
ha Sistema telefonico — i nodi SMS risultano "Eseguito" ma non partono (vale anche per SMS verso il
numero del locale stesso, senza sistema telefonico). Usa **Notifica interna → Email → Utente
specifico**, con un corpo che dice cosa fare: DISDETTA → "sul gestionale è ancora attiva, va tolta a
mano"; MODIFICA → "c'è ancora quella vecchia, sentilo e aggiornala"; NON RECAPITATA → "probabilmente
non ha WhatsApp: chiamalo". Prima di credere a un log "Eseguito", guarda il tipo di notifica.
*(contributo di Luciano Purpi, 2026-10-12)*

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
  - ⚠️ **Cambio di ponte gestionale→GHL**: gli appuntamenti creati dal ponte vecchio non stanno nella
    mappa di quello nuovo. All'annullo restano `confirmed` e il promemoria 4 ore parte lo stesso
    (caso reale: due clienti che avevano disdetto hanno ricevuto "ti aspettiamo oggi"). "Remove from
    Workflow" non basta. Rimedio: se il ponte nuovo non trova l'appuntamento nella sua mappa, lo
    cerca sul contatto con `GET /contacts/{id}/appointments` (±20 minuti dall'ora, in ora locale) e
    lo adotta; poi fa lo sweep dei fantasmi e li annulla in silenzio con `toNotify:false`. Ripeti il
    controllo dopo ogni cambio o correzione del ponte: gli appuntamenti `confirmed` futuri senza
    prenotazione attiva sul gestionale (stesso telefono o email, ora ±20 min) devono essere zero, e a
    ogni prenotazione attiva corrisponde un solo appuntamento — utile anche a regime, perché i
    webhook del gestionale possono perdersi. *(contributo di Andrea Chirivì, 2026-10-12, confermato:
    37 prenotazioni attive = 37 appuntamenti, zero fantasmi)*
  - Con certi ponti gestionale→GHL **ogni modifica della prenotazione può arrivare come "New
    appointment created"**, non come aggiornamento — vale anche per uno spostamento tavolo via API o
    pannello (caso reale: una sola cena ha generato 7 appuntamenti, 10-35 secondi dopo ogni
    modifica). Quindi mai un workflow su "appuntamento creato" con rientro aperto: ogni spostamento
    diventerebbe un messaggio al cliente già a tavola. Innesca sul campo di stato (vedi sopra), non
    sul calendario. Prima di montare un flusso sul calendario, prova una modifica e conta gli
    appuntamenti: con un ponte proprio le modifiche a stato invariato di solito non duplicano.
    *(contributo di Andrea Chirivì, 2026-10-12, confermato per il ponte di terzi; col ponte proprio
    non si è ripresentato)*
- **Effetto buono:** con il campo che si aggiorna da solo, i quattro dati di visita (data ultima
  visita, numero visite, media coperti, esito) si costruiscono DENTRO GHL su Contact Changed, senza
  chiederli al fornitore del ponte (su Barresi ha sbloccato il freno del funnel tre settimane prima).

### Promemoria (05) e cancellato (06): uscita quando il cliente annulla

(contributo di Andrea Chirivì, 2026-10-12 — supera una versione precedente del 18-19/09 basata su
Data Store + solo "Remove from Workflow")

Prima di costruire, fai la diagnosi dei buchi sul campo e l'inventario di cosa manda già il ponte
terzo. Casi reali di buchi trovati spegnendo l'accettazione automatica: nessun messaggio definitivo
dopo un'accettazione o un annullo manuale, promemoria mandato a chi aveva già annullato, ponte terzo
che perdeva gli UPDATE, promemoria doppio.

- **Il promemoria 4 ore deve avere un'uscita.** Prima dell'invio, una guardia rilegge il campo di
  stato della prenotazione. All'annullo: **"Remove from Workflow"** del promemoria E POI il WhatsApp
  Utility di annullo. Per riconoscere l'annullo basta filtrare `status=cancelled`: niente Data Store
  Make per confrontare lo stato precedente, si blocca.
- Se il promemoria vive su un appuntamento del calendario GHL, **"Remove from Workflow" non basta**:
  va annullato anche l'appuntamento.
- ⚠️ **Resmio NON manda il webhook quando è il CLIENTE ad annullare dal link** (verificato: 0 su 10
  arrivati, circa 1 annullo su 4-5). Serve un giro di recupero ogni 5 minuti sulle prenotazioni
  modificate nell'ultima ora, **fuori sessione**, che riconcilia lo stato.

### ⚠️ Flusso "Visita registrata": montaggio, campo Numero, ponte che non riscrive gli stati

(contributo di Luciano Purpi — montaggio — e Andrea Chirivì — Math su campo testo, ponte
finished→arrived —, 2026-10-12; da verificare solo che l'operazione Math non scriva su un campo
vuoto)

Due trigger **"Contatto aggiornato"**: `statoprenotazione` "è stato modificato in" `seated`, e un
altro per `finished` — i filtri nello stesso trigger vanno in AND, quindi servono due trigger
separati.
- `ultima_visita` = Current Date (campo **Selettore di data**).
- `visite_totali` con "Operazione matematica" `Add 1`. **Il Math NON accetta un campo testo**: serve
  un campo **Numero** — se il contatore esiste già come Linea singola, crea un campo Numero nuovo e
  travasa via API il valore del vecchio.
- Se usi `{{right_now.date}}` in un campo testo, verifica il formato alla prima esecuzione.
- Il contatto si toglie dal Timer 90 giorni **PRIMA** di rimettergli il tag attivo: toglie
  `stato-abituale-fermo` e `stato-attivo`, poi rimette `stato-attivo`. Re-entry ON.
- **Attesa finale di 20 ore come guardia contro il doppio conteggio** `seated → finished`:
  `visite_totali` parte da zero all'accensione (dirlo al titolare prima che lo chieda). I flussi
  Visita registrata e Richiesta recensione ripartirebbero per i `seated` e per chi ha un'altra
  prenotazione, contando le presenze due volte.
- **Regola del ponte**: un solo stato vuol dire "è venuto". Non tradurre `finished` in `arrived` né in
  un altro stato che innesca. Due strade: o si ignora `finished` (innesco su `arrived`) o si usa la
  guardia di 20 ore.
- Per correggere contatti toccati male rimetti solo il tag, **mai il campo di stato**, che farebbe
  ripartire il workflow.

### Regole dei flussi: tag del risultato, tag che fanno da trigger

(contributo di Luciano Purpi, 2026-10-12)

- Prima di ogni invio la guardia legge il **campo di stato** della prenotazione: il tag del ponte è
  uno stato, non un evento.
- Le condizioni di uscita guardano il tag del **RISULTATO**, non quello della richiesta.
  `giftcard-richiesta` viene RIMOSSA dall'ultimo nodo per permettere un secondo giro: una guardia
  "non ha `giftcard-richiesta`" lascia quindi passare chi è già stato servito, e il regalo parte
  doppio. La guardia giusta è `giftcard-consegnata` (o `coupon-utilizzato`). Prima di fidarsi di una
  guardia, apri il flusso a valle e guarda cosa fa l'ultimo nodo.
- Un tag che fa da trigger non si usa come marcatore. Caso reale: un nodo "Aggiungi tag" nel flusso
  del sondaggio metteva anche `giftcard-richiesta`, cioè il trigger della consegna WhatsApp —
  risultato: persone con due email e un WhatsApp free form fallito (fuori dalle 24 ore). Prima di
  aggiungere un tag in un nodo, cerca chi lo ascolta.

### Flusso 08 — messaggio dopo la visita (recensione o sondaggio)

*(schema nodo per nodo: contributo di Luciano Purpi; sondaggio e regole d'invio: contributo di
Andrea Chirivì — 2026-10-12. In onda su un cliente dall'8/10; lo schema dei nodi è confermato su un
altro cliente. Il trigger va scelto sul valore che il ponte del locale scrive davvero —
seated/finished oppure arrived.)*

**Costruzione** (variante: sondaggio di gradimento nativo GHL invece della richiesta diretta di
recensione). Survey nativo GHL (non una pagina sul sito) con 9 voti da 1 a 10 — Servizio (gentilezza,
attenzione, velocità), Cucina (qualità, quantità, presentazione, varietà), Atmosfera (comfort),
Esperienza complessiva — più la domanda aperta "Cosa possiamo fare per rendere la tua esperienza un
10?". Le risposte vanno in campi `gradimento_*` del contatto, con tag `gradimento-risposto`. Voto
basso (complessiva ≤6 o una voce ≤4) → tag `gradimento-basso` + nota coi voti. Link personale:
`?contact_id={{contact.id}}`, non il telefono — risponde sul contatto giusto anche senza telefono,
non crea doppioni e non mette dati personali nell'URL.

**Regole d'invio**: un solo messaggio — il sondaggio sostituisce la richiesta diretta di recensione,
non si aggiunge. Solo a chi è "arrivato" sul gestionale, il giorno dopo fra le 10 e le 20, al massimo
una volta ogni 60 giorni, mai a chi ha dato STOP. Blocco su due livelli: "Skipped: contact is already
part of this workflow" + If/Else sul tag `recensione-richiesta`.

**Schema nodi** (valido come scheletro per qualunque messaggio dopo la visita):
- Trigger: due "Contatto aggiornato" sul campo `statoprenotazione`, uno per `seated` e uno per
  `finished` (nello stesso trigger i filtri vanno in AND). Se il ponte del locale scrive `arrived`,
  basta un trigger su `arrived`.
- Guardia in testa: Tags NON include `recensione-richiesta`, altrimenti fine. Poi si mette il tag
  `recensione-richiesta`.
- Attesa 12 ore con finestra 10-20 su 7 giorni: il messaggio cade la mattina dopo.
- Condizione lingua in OR: Phone contiene "+39" OPPURE Phone non contiene "+" (sul canvas il nodo
  mostra "contiene 39" senza il +: è solo l'etichetta, apri il nodo).
- Template con rami attivi e timeout di 2 giorni. Undelivered → tag "non su whatsapp" → fine. Stop →
  DND WhatsApp → fine. Time Out → attesa 60 giorni → toglie `recensione-richiesta` (lo sblocco sta
  SOLO sul Time Out).
- Rientro ON: la guardia contro il doppio è la condizione in testa, e GHL salta comunque chi è ancora
  dentro.

**Flusso "risposta a parole"** (gemello, risposta testuale del cliente al messaggio dopo la visita):
trigger "Risposta del cliente" su WhatsApp con filtro "corpo non contiene <testo del pulsante
opt-out>" (GHL conta il tap su una quick reply come risposta, serve escluderlo). If/Else: tag
`recensione-richiesta` E non `recensione-feedback` → tag `recensione-feedback` + email al titolare.
Rientro ON. Le regole su COSA rispondere (tono, quando mettere il link, quando passare allo staff)
sono nel bot: vedi `references/conversation-ai.md` §2, "Dopo la visita, risposta a parole del
cliente".

**Recuperi una tantum** (IT/EN): senza trigger, si lanciano da Contatti → Attiva automazione. Guardia
sul tag, stessi rami, ma Time Out → fine (sono una tantum). Rientro OFF. Fai due gemelli invece di
cambiare il template di un flusso con contatti in volo.

### ⚠️ Compleanni: mail A (giorno e mese) e mail B (solo mese) senza doppio invio

(contributo di Andrea Chirivì, 2026-10-12 — metodo scritto come riferimento: il primo giro
end-to-end non è ancora verificato, vedi sotto)

- **Mail A**: a chi ha giorno e mese, 15 giorni prima, col trigger nativo **Birthday Reminder** di
  GHL, che legge `dateOfBirth` del contatto (per la migrazione vedi sopra, "compleanno_gg_mm").
- **Mail B**: a chi ha solo il mese (tag `gennaio`…`dicembre`), 10 giorni prima che il mese cominci.
  GHL non ha questo trigger: il tag `compleanno-mese-in-arrivo` lo mette un cron esterno, e il
  workflow B parte dal tag. Condizione di B: tag del mese E `compleanno_gg_mm` vuoto (evita i doppi
  invii a chi ha già entrambi i dati). Nel B il **Remove Contact Tag finale è obbligatorio**,
  altrimenti l'anno dopo non riscatta; il cron toglie e rimette il tag come salvaguardia. B chiede il
  giorno esatto con un link all'iscrizione, così la lista "solo mese" si svuota e l'anno dopo quei
  contatti passano ad A.
- Si misura in tavoli arrivati con `src=compleanno` e `src=compleanno-mese`, non in aperture. Prima
  di accendere, conta i destinatari su domini Microsoft (possono essere una quota rilevante della
  lista).
- ⚠️ **Non ancora verificato end-to-end**: il cron che mette il tag funziona, ma i workflow A e B
  possono risultare non montati — verifica sempre che siano pubblicati e attivi prima di darli per
  scontati, e segna la data del primo invio reale.

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

⚠️ Nei contatti importati il compleanno c'è spesso già nel campo standard `dateOfBirth`, salvato
come timestamp in millisecondi (es. `676252800000` = 07/06/1991), non in un campo personalizzato —
un campione di soli contatti recenti lo dà per vuoto: campiona anche gli importati. Si migra in
`compleanno_gg_mm` con uno script (caso reale: 28.449 contatti letti, 3.925 con data valida migrati
in 35 minuti, 0 errori). Sui moduli controlla che giorno e mese non escano invertiti in `dateOfBirth`.
*(contributo di Andrea Chirivì, 2026-10-12)*

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

Altri segnali *(contributo di Luciano Purpi, 2026-10-12)*:
- ⚠️ **Gli iscritti non sono il fenomeno**: un trigger largo li gonfia (caso reale: flusso STOP, 262
  iscritti e solo 6 opt-out veri, perché il trigger era "qualunque risposta" e la condizione filtrava
  dopo). Conta i tag veri (es. `whatsapp-stop`, `giftcard-consegnata`, `giftcard-prenotata`): ogni
  conteggio letto è un pavimento, non il totale.
- **Varianti in bozza**: una variante alternativa di un flusso resta in bozza, col perché scritto nel
  nome (es. consegna immediata vs consegna dopo la prenotazione). Pubblicarle entrambe manda due
  gift card.
- **Filtri "contiene" troppo larghi**: nello Smistamento Lead una condizione tipo "Phone contiene 39"
  mette fra i locali anche un numero estero che contiene quella sequenza — serve "inizia con +39". La
  riga sotto il riquadro può essere troncata: apri il nodo prima di giudicare. Controlla anche lo
  Smistamento Lead del blueprint.
- I workflow **cancellati restano recuperabili 30 giorni** nella scheda Eliminato, anche se GHL fa
  digitare "Elimina" e scrive "definitivamente" — aggiungilo al punto 5 del riordino sotto.
- Un **webhook che punta a un flusso in bozza** cade nel vuoto (0 iscritti anche dopo mesi).

## Riordino di un conto ereditato, in quest'ordine

1. Conta le etichette (oltre ~150 su un locale c'è un archivio travestito: porta le famiglie in
   campi, ma non cancellare finché non sai chi le legge).
2. Leggi iscritti totali/attivi di ogni flusso.
3. Guarda l'anello del riscatto.
4. Collauda i link delle email PRIMA di riaccendere qualsiasi cosa (skill `mail-funnel-ghl`,
   `references/collaudo-catenaria.md`).
5. Rinomina o cancella i New Workflow senza nome e i "test"/"migrazionecampo".
6. Solo adesso aggiungi.
