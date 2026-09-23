---
name: sistema-tracciamento-locale
description: Replica su un cliente nuovo l'architettura di misurazione di un locale — CRM al centro, prenotazioni con la fonte parlante, coupon con QR riscattabile in cassa che registra coperti e scontrino. Usa questa skill quando si parla di montare il tracciamento, l'attribuzione o la misura del ritorno di un ristorante/pizzeria/pub, di collegare Resmio o un gestionale prenotazioni a GoHighLevel, di creare un coupon con QR o un modulo di riscatto, di capire quali campagne portano gente vera in sala, oppure quando si nomina un locale cliente insieme a parole come tracciamento, attribuzione, conversioni, coupon, QR, funnel di acquisizione. Vale anche quando la richiesta è solo "replichiamo il sistema del Noolas su questo cliente".
---

# Il sistema di misurazione di un locale

> Skill condivisa da Luciano Purpi il 2026-09-03, corretta da Andrea l'08/09/2026 (v. 2: un modulo di riscatto per offerta, QR con `phone_raw`, Outlook, email ASCII, finestra oraria del workflow, test end-to-end).
> Nota dell'autore: replica su un cliente nuovo l'architettura di misurazione di un locale — CRM al centro, prenotazioni con la fonte parlante, coupon con QR riscattabile in cassa che registra coperti e scontrino. È il metodo dietro l'anello che manca quasi sempre, cioè il RISCATTO (su un cliente: migliaia di coupon scaricati contro 4 riscatti tracciati). 4 fasi a cancello A-B-C-D con regole dure in `trappole.md`. `campagna-locale` arriva fino al coupon, questa chiude il cerchio in cassa.

Monta, su un cliente nuovo, la catena che collega **l'euro speso in pubblicità** alla
**persona seduta al tavolo** e a **quanto ha lasciato in cassa**.

Non è un lavoro di analytics. È un lavoro di cucitura: ogni pezzo del sistema esiste per
portare il suo dato dentro il CRM, dove le quattro domande stanno sulla stessa riga.

**Prima di toccare qualsiasi cosa leggi `playbook.md`** (come si monta ogni pezzo, con gli
schemi esatti) e **`trappole.md`** (le lezioni già pagate: ognuna è costata giorni o soldi
veri su un cliente vero).

## Il criterio che decide ogni scelta

Le quattro domande, per la stessa persona, sulla stessa riga:

| | Chi risponde | Il dato |
|---|---|---|
| **Chi è?** | modulo, prenotazione, coupon | nome · email · telefono |
| **Da dove viene?** | la stringa `source` nei link, l'attribuzione della piattaforma | fonte nominativa |
| **È entrato?** | la sala, che marca l'arrivo | tag `status_arrived` |
| **Quanto ha lasciato?** | il collaboratore, al riscatto | scontrino · coperti |

**Fra due soluzioni tecniche vince sempre quella che finisce nel CRM con un nome attaccato.**

⛔ **Una metrica che vive solo dentro Meta o Google — costo per clic, tasso di atterraggio,
copertura — non è un risultato.** È una misura di piattaforma. Non presentarla mai come
rendimento: il rendimento è gente entrata ed euro incassati.

## Prima di iniziare: 6 dati dal cliente

Senza questi il lavoro si blocca a metà. Chiedili tutti insieme, in un messaggio solo.

1. **Che CRM usa** e se ha accesso da amministratore (di norma GoHighLevel)
2. **Che gestionale prenotazioni usa** (Resmio, TheFork, Plateform, telefono e basta…)
   e se è già collegato al CRM
3. **Se ha un sito**, su cosa è fatto, e se ha accesso a FTP/pannello
4. **Se ha un'anagrafica clienti da importare** — e con quale consenso marketing
5. **Chi sta in cassa la sera** e se può fare un gesto in più su un telefono
6. **L'informativa privacy: esiste, è attiva, cita la misurazione?**

Il punto 6 non è burocrazia ed è il primo a bloccare tutto: verificalo aprendo davvero
l'URL, non fidandoti che risponda 200. Una policy disattivata risponde 200 e dice
«non è più attiva».

## Le quattro fasi — l'ordine è il contenuto

Ogni fase è un cancello: **non si passa alla successiva finché la precedente non è
verificata su un dato vero.** Ogni volta che quest'ordine è stato invertito si è pagato.

### Fase A — Le fondamenta (nessun euro di pubblicità)

- **A1** CRM scelto e acceso, anagrafica esistente importata con presenze, data ultima
  visita e **consenso marketing**
- **A2** Gestionale prenotazioni collegato al CRM: devono arrivare giorno, ora, coperti,
  stato e **fonte**. Verificalo su una prenotazione vera — e **aspetta 20 minuti prima di
  dichiararlo rotto**, la catena è lenta
- **A3** La sala marca chi si presenta davvero. È una procedura umana ed è il dato più
  prezioso di tutto il sistema
- **A4** Informativa privacy attiva e che citi la misurazione

**Cancello:** una prenotazione vera che arriva nel CRM con la sua fonte e il suo stato.

### Fase B — Il sito strumentato

- **B1** Analytics e pixel **a livello di sito**, mai dentro il contenuto di una pagina,
  sempre subordinati al consenso
- **B2** La **sorgente parlante** nei link di prenotazione: ogni pulsante porta con sé da
  quale pagina e da quale canale arriva la persona
- **B3** L'evento di prenotazione dichiarato conversione e importato nella piattaforma
  pubblicitaria — **e verificato che arrivi alla singola campagna, non solo all'account**

**Cancello:** una prenotazione vera in cui la fonte nel CRM dice pagina + canale.

### Fase C — La macchina dell'offerta

- **C1** Modulo di cattura: nome, email, telefono. Niente altro
- **C2** **Un modulo di riscatto per offerta**, tutti duplicati dallo stesso originale
  (stessi campi, stesso aspetto): campi anagrafici precompilabili più **coperti** e
  **scontrino** obbligatori. In cassa il gesto resta uno — è il QR a sapere di quale
  offerta è
- **C3** Due automazioni: consegna (tag + email col QR + solleciti) e riscatto (bivio sul
  tag). La seconda deve permettere il rientro
- **C4** Prova end-to-end dal telefono su un contatto vero, e **rilettura del dato arrivato**

**Cancello:** un QR inquadrato davvero, un modulo che si apre precompilato, i valori
riletti nel CRM.

### Fase D — Solo adesso la pubblicità

- **D1** Il front end resta **dentro la piattaforma** dove la gente già sta
- **D2** L'offerta ha una **scadenza** e dei **giorni validi** scelti dove c'è posto, non
  dove c'è già coda
- **D3** L'anagrafica esistente si **esclude** dal pubblico
- **D4** Si giudica su persone entrate ed euro incassati

## Regole che non si violano

1. **Un modulo di riscatto PER OFFERTA, duplicato sempre dallo stesso originale.**
   Mai un modulo condiviso fra due offerte: ogni automazione di riscatto ascolta il
   proprio modulo, e se due offerte ascoltano lo stesso, un solo invio marca *utilizzati*
   entrambi i coupon di chi li ha tutti e due (successo davvero: provato sui dati).
   In cassa il gesto resta comunque uno — si inquadra il QR e basta, è il QR a sapere
   di quale offerta è.
2. **I campi che scrive l'uomo sono obbligatori.** Un campo facoltativo in cassa, dopo tre
   sere, è vuoto.
3. **Link diretti al gestionale, mai widget incorporati.** Il widget sovrascrive la fonte.
4. **Quando cambi il percorso di un clic, controlla subito quale misura ci stava sopra.**
5. **Non accendere una campagna prima che la macchina del coupon sia viva e provata**,
   o raccogli nomi a cui non arriva niente.

## Cosa consegnare al cliente

- Lo **schema** del suo sistema (i due diagrammi del manuale, adattati)
- La **frase per la sala**: «inquadri il QR, scrivi quante persone e quanto hanno pagato,
  conferma»
- L'elenco onesto di **cosa il sistema non misura** — tipicamente l'80% di chi entra, che
  arriva da telefono, walk-in, mappe e passaparola

**Il documento da consegnare al cliente è già dentro questa skill:**
`references/manuale-da-consegnare-al-cliente.pdf` — 8 pagine, con i due schemi, le quattro fasi e il
capitolo su cosa il sistema non misura. Si manda così com'è, oppure si usa come traccia
per la riunione di partenza.

## Cosa questa skill NON contiene

Nessuna credenziale, nessun accesso, nessun dato di clienti. Gli strumenti per operare
(connettore del CRM, accessi al sito, gestore inserzioni) vanno collegati da chi la usa,
sul proprio account e su quello del proprio cliente.
