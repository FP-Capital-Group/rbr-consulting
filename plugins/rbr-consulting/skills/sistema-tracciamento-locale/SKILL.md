---
name: sistema-tracciamento-locale
description: Replica su un cliente nuovo l'architettura di misurazione di un locale — CRM al centro, prenotazioni con la fonte parlante, coupon con QR riscattabile in cassa che registra coperti e scontrino. Usa questa skill quando si parla di montare il tracciamento, l'attribuzione o la misura del ritorno di un ristorante/pizzeria/pub, di collegare Resmio o un gestionale prenotazioni a GoHighLevel, di creare un coupon con QR o un modulo di riscatto, di capire quali campagne portano gente vera in sala, oppure quando si nomina un locale cliente insieme a parole come tracciamento, attribuzione, conversioni, coupon, QR, funnel di acquisizione. Vale anche quando la richiesta è solo "replichiamo il sistema del Noolas su questo cliente".
---

# Il sistema di misurazione di un locale

> Skill condivisa da Luciano Purpi il 2026-09-03, corretta da Andrea l'08/09/2026 (v. 2: un modulo di riscatto per offerta, QR con `phone_raw`, Outlook, email ASCII, finestra oraria del workflow, test end-to-end).
> Pacchetto migliorie di Andrea Chirivì (contributi anche di Luciano Purpi), verifica completa del 2026-10-12 su clienti veri (Noolas e altri): integrato qui, in `playbook.md` e in `trappole.md`.
> Nota dell'autore: replica su un cliente nuovo l'architettura di misurazione di un locale — CRM al centro, prenotazioni con la fonte parlante, coupon con QR riscattabile in cassa che registra coperti e scontrino. È il metodo dietro l'anello che manca quasi sempre, cioè il RISCATTO (caso reale: 138 scaricati e 2 riscatti all'11/08, saliti a 252 scaricati e 11 riscatti al 17/08 col sollecito corretto — la misura funzionava, il problema era la resa dell'offerta). 4 fasi a cancello A-B-C-D con regole dure in `trappole.md`. `campagna-locale` arriva fino al coupon, questa chiude il cerchio in cassa.

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
| **È entrato?** | la sala, che marca l'arrivo | tag su `arrived` + `seated` + `finished` (si sommano i coperti con `num`, non le prenotazioni — vedi playbook A3) |
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

⚠️ Il punto 6 copre il tracciamento web (banner cookie). **Caricare email e telefono
presi dalle prenotazioni su Google/Meta** (conversioni offline, Customer Match, pubblici
personalizzati) è un trattamento diverso: serve una base giuridica e un'informativa
attiva che citi *anche* la comunicazione dei dati di contatto alle piattaforme per la
misurazione. Il caricamento si accende solo dopo aver raccolto il consenso marketing
anche sulle prenotazioni telefoniche (Resmio non lo scrive da solo).

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
  sempre subordinati al consenso. ⚠️ **Il banner cookie è il rubinetto del tracciamento:
  va controllato ogni settimana.** Se il banner si spegne (es. piano del servizio cookie
  scaduto o sforato) il sito diventa cieco senza nessun errore — spariscono `_ga`, `_fbp`,
  `_gcl_au` — mentre le campagne continuano a spendere. Controllo in 10 secondi:
  `curl -s "https://cs.iubenda.com/cookie-solution/confs/js/<cookiePolicyId>.js" | grep csEnabled`
  (`true` = tracciamento vivo). La carta di pagamento del banner va tenuta valida
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

- **D1** Il front end resta **dentro la piattaforma** dove la gente già sta — vale
  soprattutto per **Meta** (traffico senza intenzione). Su **Google** chi cerca ha già
  intenzione: va mandato alla prenotazione, meglio sul proprio dominio (regola 3), perché
  è lì che il tag vede il `gclid`. Con `gclid` dentro `booking_request_parameters`, le
  prenotazioni onorate si caricano come conversioni offline per gclid senza bisogno di
  match su email/telefono — le conversioni avanzate per i lead restano a 0 se la
  prenotazione avviene fuori dal dominio del locale
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
3. **Mai l'embed Resmio lasciato così com'è: il widget costruisce l'iframe con `source =
   hostname`.** Due strade buone. (a) Link diretto `app.resmio.com/<slug>/widget?source=…`:
   la source arriva, ma gclid/utm NON entrano in `booking_request_parameters` (li legge
   solo da `document.referrer`, solo dentro un iframe). (b) Consigliata con Google Ads:
   pagina di prenotazione sul dominio del locale (`/prenota/`) col widget, pulsanti con
   `?source=pagina.canale`; uno snippet riscrive l'attributo `src` dell'iframe dopo il
   rendering (polling ~300ms) per iniettare la source giusta — col consenso l'iframe usa
   `referrerpolicy="no-referrer-when-downgrade"` e si ricarica (non si ricarica se la
   persona ha già toccato il modulo); gbraid/wbraid viaggiano come `utm=gbraid_<valore>`.
   Regola d'oro: **la sorgente si aggiunge, la destinazione non si tocca.** La data della
   serata nell'iframe funziona con `date=YYYY-MM-DD`, non con `nextAvailability=true`.
   ⚠️ Da confermare ancora su prenotazioni vere: il caso «gclid solo in memoria» e
   Safari/iPhone.
4. **Quando cambi il percorso di un clic, controlla subito quale misura ci stava sopra, e
   tienila sotto controllo settimanale finché 7 giorni interi di dati non danno il
   verdetto** (vedi trappole.md, «Una correzione non è chiusa il giorno in cui la fai»).
5. **Non accendere una campagna prima che la macchina del coupon sia viva e provata**,
   o raccogli nomi a cui non arriva niente.

## Cosa consegnare al cliente

- Lo **schema** del suo sistema (i due diagrammi del manuale, adattati)
- La **frase per la sala**: «inquadri il QR, scrivi quante persone e quanto hanno pagato,
  conferma»
- L'elenco onesto di **cosa il sistema non misura** — tipicamente l'80% di chi entra, che
  arriva da telefono, walk-in, mappe e passaparola
- La domanda **«come ci avete trovati?»**, fatta in sala e al telefono e registrata sul
  gestionale con un vocabolario fisso. Non è un'altra correzione tecnica: oltre l'80% di
  chi entra non passa da un pixel, e questi clienti si riconoscono anche dall'email finta
  di appoggio che Resmio genera (`appoggiokeap+<telefono>@gmail.com`). Per il telefono non
  basta far scrivere `source=telefono`: manca il motivo della chiamata

**Il documento da consegnare al cliente è già dentro questa skill:**
`references/manuale-da-consegnare-al-cliente.pdf` — 8 pagine, con i due schemi, le quattro fasi e il
capitolo su cosa il sistema non misura. Si manda così com'è, oppure si usa come traccia
per la riunione di partenza.

## Cosa questa skill NON contiene

Nessuna credenziale, nessun accesso, nessun dato di clienti. Gli strumenti per operare
(connettore del CRM, accessi al sito, gestore inserzioni) vanno collegati da chi la usa,
sul proprio account e su quello del proprio cliente.
