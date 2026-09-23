---
name: whatsapp-ghl-locale
description: Metodo RBR per integrare WhatsApp Business ufficiale (via Meta) su GoHighLevel e raggiungere i clienti di un locale che NON hanno lasciato l'email, solo il telefono. Usala ogni volta che un consulente dice "il cliente non ha le mail dei suoi contatti", "come li raggiungiamo su WhatsApp", "attiviamo WhatsApp su GHL", "il template WhatsApp è stato rifiutato", "scrivimi i template WhatsApp", "la qualità del numero è scesa", "automatizziamo le conferme/promo su WhatsApp", "mandiamo un WhatsApp a tutta la lista", "invio di massa WhatsApp", "gestiamo gli STOP / le disiscrizioni", "ho una lista di numeri senza consenso", "quanto costa WhatsApp", "il bot risponde dopo il messaggio di benvenuto", o quando un workflow GHL deve avere un ramo WhatsApp per i contatti senza email. Copre: attivazione e struttura standard del canale, coexistence, qualità del numero e recupero, regola delle 24 ore, template pronti e trappole di approvazione, consenso e liste fredde, opt-out e STOP, invio di massa con drip, costi e limiti 2026, pattern di workflow, ponte col gestionale e anti-loop. Costruita sul caso Noolas (lug-ago 2026) e sui conti Barresi, Mister Pizza, Red Mike; replicabile su qualsiasi cliente.
---

# WhatsApp su GoHighLevel per un locale

> Skill condivisa da Andrea Chirivì (Andrew) il 2026-09-10 (pacchetto versione 08/09), nata sul caso Noolas lug-ago 2026.
> Nota dell'autore: per clienti con database di soli telefoni. Copre attivazione del canale WhatsApp ufficiale Meta su GHL, qualità e mantenimento, regola delle 24 ore, trappole di approvazione verificate, pattern workflow (ramo senza-email, Customer Replied come orecchio, anti-loop coi ponti esterni).
> Integrata con i contributi di Luciano Purpi (4, 8, 13 e 19 set 2026): template pronti, consenso e liste fredde, opt-out e STOP, costi e limiti 2026, invio di massa, coexistence, struttura standard del canale.

## Perché questa skill esiste

In un ristorante una fetta enorme del database entra **senza email**: chi scrive in
direct su WhatsApp/Instagram lascia solo il telefono, chi prenota a voce spesso pure.
Sul Noolas i numeri veri erano: 27.775 contatti, **97,6% col telefono, solo 80,5% con
un'email** — e la coda recente (messaggi diretti) era quasi tutta solo-telefono.
In più le email su GHL soffrono l'IP condiviso (Microsoft blocca hotmail/outlook):
**WhatsApp è l'unico canale che arriva a tutti, e arriva davvero.**

Il principio RBR resta quello di sempre: il canale serve a **far entrare persone nel
locale**, non a "mandare messaggi". Ogni automazione qui dentro deve finire in una
prenotazione, una conferma o un coperto salvato.

## File di riferimento (leggili quando servono)

| File | Quando |
|---|---|
| `references/trappole-template.md` | PRIMA di scrivere o mandare in approvazione un template |
| `references/template-pronti.md` | per partire da template già scritti invece che da zero |
| `references/consenso-e-liste.md` | prima di qualunque invio Marketing, e con liste importate senza consenso |
| `references/orecchio-e-stop.md` | per montare il workflow in entrata e la gestione STOP (workflow o Human Handover) |
| `references/invio-di-massa.md` | prima di mandare un template a una lista (Bulk WhatsApp, drip, pulizia rubrica) |
| `references/costi-limiti-misura.md` | preventivi al cliente, limiti di invio, misura dei risultati |

## Come funziona l'integrazione (l'architettura in breve)

GoHighLevel parla con **WhatsApp Business API ufficiale di Meta** — non è un
WhatsApp Web collegato, non è un bot di terze parti. Questo significa:

- I messaggi in entrata e in uscita vivono nelle **Conversazioni** di GHL
  (`TYPE_WHATSAPP`), quindi i workflow possono innescarsi e rispondere da soli.
- Meta governa le regole: template approvati, finestra delle 24 ore, punteggio
  qualità del numero. GHL è l'interfaccia, Meta è il giudice.
- Il canale va in **entrambe le direzioni**: i clienti scrivono, il sistema risponde
  e viceversa. L'errore classico è costruire solo l'uscita — vedi Pattern C.

## 1. Attivare il canale su un sub-account nuovo

Percorso: **Settings → WhatsApp** del sub-account.

1. **Add-on WhatsApp**: 15 $/mese per sub-account, più il consumo Meta a messaggio
   template consegnato (dettagli e cifre in `references/costi-limiti-misura.md`).
   Si vede in Settings → Billing → Wallet & Transactions.
2. **Requisiti Meta** (senza questi non si parte):
   - Business Manager del cliente con **verifica aziendale completata** (Verified);
   - account WhatsApp Business **Approved**;
   - **messaggi marketing Enabled** (altrimenti solo Utility).
3. **Il numero**: la scelta chiave è la modalità **Coexistence** — lo stesso numero
   resta utilizzabile dall'app WhatsApp Business sul telefono dello staff mentre le
   automazioni girano su GHL. Vantaggi: nessun numero nuovo da comunicare, lo staff
   continua a lavorare come sempre. Rovesci da gestire:
   - se lo staff risponde dal telefono, in GHL quei messaggi risultano "non letti":
     quando misuri l'arretrato tienine conto prima di dichiarare il disastro;
   - **il messaggio di benvenuto configurato nell'app parte PRIMA del bot** (vedi
     sotto "Coexistence: spegnere i messaggi automatici dell'app");
   - la connessione cade se nessuno apre l'app per 14 giorni (vedi `diagnosi-suite`).
4. **Verifica finale**: stato **Connected**, qualità **Green** (vedi sotto). Fai uno
   screenshot di questa schermata per la checklist di avvio del cliente.

### Coexistence: spegnere i messaggi automatici dell'app (contributo di Luciano Purpi, 2026-09-08)
Il **messaggio di benvenuto** impostato dentro l'app WhatsApp Business resta attivo
e parte prima della risposta dell'agente: il cliente riceve due messaggi, prima
quello vecchio del titolare, poi quello del bot. Caso Red Mike (8 set 2026): alle
11:17 il cliente riceve emoji a raffica, "Buonasera" alle undici del mattino e link
misti — testo scritto mesi prima, contro tutte le regole di tono del prompt.
- **Come riconoscerlo** nel thread GHL: esce dal nostro numero ma **senza l'icona ✨**
  dell'agente, lo stile è diverso dal prompt; per escludere un'automazione GHL, apri
  la lista Workflow e controlla che i "Total enrolled" non siano saliti.
- **Perché è critico**: in una campagna di massa rovina l'esperienza proprio sui
  contatti più caldi, quelli che rispondono.
- **Come si spegne**: solo dal telefono del titolare → WhatsApp Business →
  Impostazioni → Strumenti per l'azienda → Messaggio di benvenuto → disattiva. Nella
  stessa schermata controlla anche **Messaggio di assenza** e **Risposte rapide**.

### La struttura standard del canale (contributo di Luciano Purpi, 2026-09-13)
Rilevata su tre conti (Barresi, Mister Pizza, Noolas). Schema:
**1 numero in coexistence → 4 template Utility → 2 flussi di servizio; N template
Marketing → 1 flusso per campagna; 1 flusso in entrata (orecchio + STOP).**

Le 5 schede di **Impostazioni → WhatsApp**:
- **Numeri**: stato account, verifica Meta, marketing abilitato, QUALITÀ per numero;
- **Modelli**: categoria, lingua, stato Attiva/Rifiutato;
- **Flussi**: i flow nativi Meta, di norma vuoti (i rami si fanno nei workflow);
- **Limiti di messaggistica**: il gradino attuale (vedi `costi-limiti-misura.md`);
- **Chiamata in corso**: inutile per un locale.

**Guarda quale numero è "predefinito".** Su Mister Pizza, sotto la stessa WABA, ci
sono due numeri e il predefinito è un numero americano con qualità "Nessuno", mentre
l'italiano vero è Verde. Un'azione che non sceglie il numero esplicitamente parte da
quello sbagliato: controllalo su ogni conto con più di un numero e scegli sempre il
mittente a mano (workflow, Bulk WhatsApp).

## 2. Lo "stato verde": il punteggio qualità di Meta

Accanto al numero GHL mostra la **Quality** che Meta assegna: **Green / Yellow / Red**.
Verde = nessuna limitazione, i messaggi partono e i limiti di invio crescono.
Giallo/rosso = Meta sta ricevendo segnalazioni/blocchi dai destinatari e **riduce i
limiti in silenzio** — i workflow sembrano girare ma i messaggi non arrivano.
Un numero nuovo in coexistence ha qualità **vuota**: nessuna reputazione, va scaldato
(vedi `invio-di-massa.md`).

Il verde non "si attiva": **si merita e si mantiene**. Le regole che lo tengono verde:

- Le comunicazioni di servizio (conferma, promemoria, attesa conferma) viaggiano su
  template **Utility**: costano meno, passano l'approvazione facilmente e nessuno le
  segnala, perché il cliente le sta aspettando. Sono loro che tengono verde il numero.
- Il marketing va **solo a chi ha il consenso** (tag `consenso-marketing`, vedi
  `consenso-e-liste.md`) e ogni template Marketing ha l'**opt-out**.
- **Mai raffiche massive su liste fredde.** Un database importato non è una lista di
  persone che hanno chiesto tue notizie: si scalda a blocchi, partendo dai clienti
  recenti/attivi, e si guarda la qualità dopo ogni invio.

**Recupero qualità** (contributo di Luciano Purpi, 2026-09-04) — se il numero va
giallo/rosso:
1. fermare subito i massivi;
2. lasciar correre solo le Utility legate a prenotazioni vere;
3. mettere in pausa i template che hanno generato blocchi (WhatsApp Manager,
   colonna qualità);
4. 7 giorni di traffico pulito, poi riprendere il marketing a piccoli blocchi.
Se resta rossa, il problema è la lista, non il testo.

## 3. La regola delle 24 ore (il cuore del canale)

È la regola che decide tutto il disegno:

- **Entro 24 ore** dall'ultimo messaggio del cliente puoi scrivere **testo libero**
  (risposte, follow-up, quello che vuoi).
- **Oltre le 24 ore** — quindi verso qualunque contatto "freddo" che ha solo il
  telefono — puoi mandare **SOLO template approvati da Meta**.

Conseguenza pratica per il caso tipico ("tanti contatti senza email da raggiungere"):
**prima si fanno approvare i template, poi si costruiscono i workflow.** Senza
template approvati il canale verso i contatti freddi non esiste, per quanti workflow
tu monti. Il pattern "consenso prima dell'offerta" (`consenso-e-liste.md`) sfrutta la
regola: il template chiede, la risposta del cliente riapre le 24 ore e il seguito è
testo libero.

## 4. Template: categorie, forma e trappole

Leggi **`references/trappole-template.md`** PRIMA di scrivere o inviare in
approvazione qualunque template (tre rifiuti in un giorno sul Noolas; variabile
`paymentLink` che genera il «Ciao ,»). Parti dai testi di
**`references/template-pronti.md`** invece che da zero.

Le regole di sintesi:

- **Utility** per conferme/promemoria/attesa, **Marketing** per promo (con opt-out),
  **Authentication** solo per codici di verifica. Un codice personale dentro un
  template Marketing ("Ecco il tuo codice: XXX") somiglia a un OTP e viene
  **rifiutato automaticamente in pochi secondi**.
- **Pulsanti, non domande aperte.** "Rispondi a questo messaggio per confermare"
  produce risposte libere che nessun workflow sa smistare; tre bottoni
  (Confermo · Disdico · Voglio modificare) restituiscono un dato pulito e gratuito.
- Un template rifiutato **non si ripara**: si crea da zero con nome nuovo — e il
  rifiutato si toglie dall'elenco (vedi trappole).
- Il motivo del rifiuto GHL non lo mostra e Meta lo scrive generico: non perdere ore
  a indovinare — cambia la **struttura** (codici, pulsanti, lunghezza), non solo le
  parole.
- L'header immagine di un template è **uguale per tutti**: niente QR o contenuti
  personalizzati dentro WhatsApp. Si manda il **link** alla pagina personale
  (coupon, conferma) e il QR vive lì.
- Ogni modifica a un template approvato **riparte da zero con l'approvazione**: i
  template che funzionano non si toccano, se ne crea uno nuovo accanto e si sostituisce
  a cose pronte.
- **Nomi** (contributo di Luciano Purpi, 2026-09-13): `<funzione>_<lingua>` per il
  servizio, `<cliente>_<funzione>_<lingua>` per il marketing; lingua sempre in coda
  così le due versioni dello stesso messaggio stanno vicine in elenco.

## 5. Workflow autonomi: i pattern che funzionano

I workflow GHL **si montano a mano nell'editor** (non esistono via API, e l'editor
gira in un iframe che l'automazione del browser non riesce a pilotare — vedi
`invio-di-massa.md`).

**Cosa si può fare via API/MCP e cosa no** (contributo di Andrea, 2026-09-10):
- L'API pubblica GHL **NON invia template WhatsApp**: `POST /conversations/messages`
  con `templateId` risponde "Template not found" (gli id dei template WA vivono in un
  servizio interno non esposto).
- Il **testo libero** via API funziona solo **dentro la finestra delle 24 ore**; fuori
  fallisce con errore esplicito.
- Quindi i template WhatsApp partono **SOLO da UI e da workflow GHL**. Via API/MCP
  (`conversations_send-a-new-message`) i merge field del contatto
  (`{{contact.first_name}}`, `{{contact.id}}`…) si risolvono (verificato sul canale
  email), i **trigger link NO** (stringa vuota): non usarli mai nei messaggi via API.
- **Pattern-ponte** per mandare un template da Make/API (es. avvisare un numero
  fisso): Make rileva l'evento e **aggiunge un tag** al contatto destinatario →
  workflow GHL "Tag Added → Send WhatsApp template → Remove tag". Trappola Make: nel
  modulo `http:ActionSendData` il campo `timeout` dev'essere un numero, non una
  stringa.

Un vantaggio strutturale per un database di soli-telefono: con
`allowDuplicateContact` disattivato GHL riconosce il contatto **dal numero di
telefono** (identificatori unici: email E telefono). Chi scrive in direct o riscatta
un coupon viene agganciato al contatto esistente senza creare doppioni — è la base
che rende affidabili tag e conteggi su questo pubblico.

### Pattern A — Uscita su evento (conferme, promemoria) e ponte col gestionale
Architettura (contributo di Luciano Purpi, 2026-09-04): **gestionale → ponte
(Make/webhook) che cerca il contatto in GHL PER NUMERO DI TELEFONO → tag di stato
(es. `status_confirmed`) → workflow** che formatta data/ora, ramifica per stato,
manda il **template WhatsApp** e **rimuove il tag alla fine**.
Tre errori da evitare:
1. **Non rimuovere il tag**: la seconda prenotazione non innesca più (rimuoverlo è
   ciò che fa ripartire la conferma a ogni modifica della prenotazione).
2. **Numero non normalizzato in +39**: matching fallito e contatti doppi.
3. **Ramo che conferma e scrive anche sul gestionale**: loop (vedi Anti-loop).

### Pattern B — Il ramo "senza email" (il caso di questa skill)
Dentro qualunque workflow di comunicazione, condizione If/Else:

- **Email presente e valida** → ramo email.
- **Email vuota O tag `email-non-valida`, e telefono presente** → ramo WhatsApp
  (template approvato).

⚠️ Trappola verificata: certi ponti (es. Resmio) inventano **email di appoggio finte**
(tipo `appoggiokeap+numero@gmail.com`) per i contatti senza email. Se non le tagghi
`email-non-valida`, il contatto sembra raggiungibile via email e non lo è: il ramo
WhatsApp non scatta mai e il cliente non riceve niente. Prima di costruire il ramo,
**conta e tagga le email finte** del sub-account.

### Pattern C — L'orecchio (entrata)
Trigger: **Customer Replied → canale WhatsApp**. Senza questo il sistema parla ma non
ascolta: sul Noolas il 43% delle conversazioni finiva col cliente che scrive e nessuno
che risponde — disdette perse, tavoli bloccati, clienti arrabbiati. Il ramo minimo:
le risposte-pulsante si chiudono da sole (tag + risposta automatica), tutto il resto
**avvisa una persona precisa su un numero preciso**. Se non decidi CHI riceve la
sveglia, hai ricostruito il silenzio un piano più in alto.
Forma minima montata su Noolas e dettagli che costano un'ora (connettore AND→OR,
campo "Replied message", notifica interna): `references/orecchio-e-stop.md`.

### Pattern D — STOP e opt-out (obbligatorio prima di qualunque Marketing)
Chi chiede di non ricevere più messaggi deve uscire **da solo e subito** da ogni
flusso Marketing. Due strade, da usare entrambe (contributi di Luciano Purpi,
2026-09-04 / 08 / 13):
1. **Pulsante nativo "Marketing opt-out"** nel template Marketing: Meta compila da sé
   piè di pagina ed etichetta, tradotti in automatico (nessuna riga aggiunta al
   corpo, quindi nessuna nuova approvazione).
2. **Chi scrive la parola** (STOP, BASTA, CANCELLAMI…) → tag di esclusione + DND
   **solo sul canale WhatsApp** + conferma breve e gentile. Si monta:
   - nel ramo STOP dell'orecchio (workflow), se sul numero non c'è un agente AI;
   - in uno **scenario di Human Handover "Disiscrizione"** del Conversation AI, se
     sul numero risponde un agente: senza scenario dedicato lo STOP cade in "Human
     Requested" e il cliente si sente rispondere "Ti metto in contatto con un
     collega".
Procedura passo passo di entrambe: `references/orecchio-e-stop.md`.
**La condizione "ha il tag di esclusione → esci" va IN TESTA a ogni flusso di
marketing**, non solo come filtro nel CRM.

### Anti-loop (quando c'è un ponte esterno)
Se un ponte terzo spinge gli eventi del gestionale dentro GHL (webhook
BOOKING_CREATED/UPDATED/…), ogni scrittura di ritorno sul gestionale fa ripartire il
giro: modifichi la prenotazione → il ponte rimanda il tag → riparte la conferma → il
cliente risponde → riparte il tuo workflow. **La regola che spezza il giro: il ramo
che si limita a confermare non deve mai scrivere sul gestionale.** E quando modifichi
qualcosa, lascia che la conferma aggiornata la mandi la macchina già esistente: niente
doppioni.

## 6. Consenso e buon senso

- Conferme e promemoria di un servizio richiesto (la prenotazione) sono legittimi di suo.
- Le promo no: **solo consenso marketing esplicito**, registrato in GHL, e l'opt-out
  sempre presente. Liste importate senza consenso: procedura in 5 passi in
  `references/consenso-e-liste.md` (primo messaggio = richiesta di consenso, MAI
  l'offerta).
- Il criterio del ritorno vale anche qui: si misura in **persone che entrano**
  (prenotazioni, coupon riscattati), non in messaggi consegnati.

## 7. Invio di massa

Per mandare un template a una lista **non serve un workflow**: Contatti → seleziona →
More → **Send WhatsApp**, con modalità **drip** per rilasciare a lotti (contributo di
Luciano Purpi, 2026-09-08). Prima di premere invio: rubrica ripulita da fornitori e
contatti di prova, numero nuovo scaldato con un lotto sonda, messaggi automatici
dell'app spenti, STOP attivo. Tutto in `references/invio-di-massa.md`.

## Checklist di consegna (prima di dire "fatto" al cliente)

1. ☐ Canale Connected, business Verified, marketing Enabled, qualità **Green**
2. ☐ Numero **predefinito** corretto (se il conto ha più numeri) e messaggi automatici
   dell'app (benvenuto, assenza, risposte rapide) spenti in coexistence
3. ☐ Template necessari **approvati** (non "inviati": approvati), variabili verificate
   (nessun `paymentLink.*`), rifiutati tolti dall'elenco
4. ☐ Email finte di appoggio contate e taggate `email-non-valida`
5. ☐ Ramo senza-email presente nei workflow di comunicazione
6. ☐ **Ponte gestionale attivo**: contatto trovato per telefono in +39, tag rimosso a
   fine workflow, nessuna scrittura di ritorno dal ramo di conferma
7. ☐ Workflow in entrata (Customer Replied) attivo, con UN nome e UN numero per la sveglia
8. ☐ **STOP testato**: un contatto di prova scrive STOP → tag di esclusione + DND
   WhatsApp + conferma; condizione di uscita in testa ai flussi marketing
9. ☐ **Consenso popolato**: tag `consenso-marketing` + campi `consenso_data` e
   `consenso_origine` sui contatti che ricevono Marketing
10. ☐ **Link tracciati** nei template: `source=whatsapp-<campagna>`
11. ☐ Test end-to-end con un contatto di prova: messaggio partito, risposta smistata
12. ☐ Costi spiegati al cliente: 15 $/mese + consumo a messaggio template consegnato

(Punti 6, 8, 9, 10 aggiunti da Luciano Purpi il 2026-09-04; punto 2 dai contributi
dell'8 e 13 set 2026.)

## Trappole d'ambiente (perdono ore)

- **La traduzione automatica di Chrome su GHL riscrive il DOM**: anteprime template
  sbagliate, campi che si sganciano, menu che cambiano lingua tra un clic e l'altro.
  Disattivarla SEMPRE prima di lavorare nel pannello (clic destro → Mostra originale).
- Le schermate GHL caricano lente (**30-60 secondi**): non trarre conclusioni da una
  pagina che non ha finito di caricare — "lista vuota" spesso significa "lista non
  ancora caricata". Se una vista resta bianca all'infinito, apri una scheda nuova e
  chiudi la vecchia.
- **Le tendine GHL non selezionano al clic**: clic sulla voce (la evidenzia) POI
  Invio. Con le frecce attenzione allo sfasamento: dopo un clic la prima voce è già
  evidenziata, quindi Giù porta alla SECONDA (contributo di Luciano Purpi, 2026-09-19).
- In coexistence i "non letti" di GHL possono essere stati gestiti dal telefono dello
  staff: verificare prima di allarmare il cliente.
