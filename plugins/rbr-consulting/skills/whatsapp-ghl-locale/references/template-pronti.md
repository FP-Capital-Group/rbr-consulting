# Template WhatsApp pronti per un locale

> Contributo di Luciano Purpi (2026-09-04), con insieme minimo, nomi e pattern del
> consenso dal contributo del 2026-09-13. Prima ogni consulente li riscriveva da zero,
> moltiplicando il rischio di rifiuto: parti da qui e adatta solo nome del locale e tono.

Sono **bozze da mandare in approvazione**, non testi già approvati su ogni conto
(eccetto la sezione "Testi già approvati da Meta" in fondo al file). Prima di
inviarle rileggi `trappole-template.md` (niente codici nei Marketing, niente
alcol, variabili dall'albero e non dalla ricerca, contenuto di esempio per ogni `{{n}}`).

## Regole comuni

- **Variabili numerate** `{{1}}`, `{{2}}`…: in tabella sotto ogni template c'è a cosa
  mapparle. **Nome e campi standard dall'albero** (Contatto → Nome, mai la ricerca
  "first name"); **campi personalizzati con la ricerca sulla chiave interna esatta**
  (es. `orariodellaprenotazione`), poi si rilegge sempre il `value` (dettaglio
  completo in `trappole-template.md` §7). Non è provato che cercare per etichetta
  sbagli anche sui campi personalizzati: non trattarlo come regola finché non è
  verificato. (correzione di Andrea Chirivì e Luciano Purpi, 2026-10-12)
- Il corpo **non inizia né finisce con una variabile**: serve testo prima e dopo
  ("Ciao {{1}}, …", non "{{1}}, …").
- Ogni `{{n}}` ha un **contenuto di esempio** (es. "Marco", "sabato 12 ottobre", "20:30").
- **Pulsanti** al posto delle domande aperte.
- **Marketing**: pulsante nativo **"Marketing opt-out"** sempre (vedi SKILL.md
  Pattern D per il piè di pagina fisso in inglese che il pulsante aggiunge).
- **Link** con `source=whatsapp-<campagna>` per misurare (vedi `costi-limiti-misura.md`).
- Nome: `<funzione>_<lingua>` per il servizio, `<cliente>_<funzione>_<lingua>` per il
  marketing (lingua in coda).
- Non nominare mai bevande alcoliche; l'offerta nel dettaglio vive sulla landing.
- **Date e ora**: mai un campo DATA grezzo nel template (sui conti col ponte M3R
  esce in ISO, es. `2026-09-22T00:00:00.000Z`) — nel promemoria del giorno scrivi
  "oggi alle {{ora}}". L'ora va scritta dal ponte come testo `HH:MM`, **mai coi
  secondi** (verifica che nessun altro flusso legga i secondi prima di cambiare
  formato). Se lo stesso campo esce con formati diversi in momenti diversi, guarda
  l'Audit Log: può esserci un ramo di codice diverso o qualcosa in GHL che riscrive
  il campo. Prima di montare un template, fai un merge di prova su ogni campo.
  (contributo di Andrea Chirivì e Luciano Purpi, 2026-10-12)

## Insieme minimo (contributo di Luciano Purpi, 2026-09-13)

4 Utility fanno il servizio e tengono verde il numero, perché il cliente li aspetta:
`conferma_prenotazione_<lingua>`, `promemoria_prenotazione_<lingua>`,
`prenotazione_non_confermata`, `avviso_staff`. Poi il marketing, **un template per
gesto**: `richiesta_recensione_<lingua>`, `<cliente>_ritorno_<lingua>`,
`<cliente>_<offerta>_consenso`, `<cliente>_<offerta>_promemoria`,
`<cliente>_premio_<cosa>_<lingua>`.

---

## 1. Conferma prenotazione — Utility
Nome: `conferma_prenotazione_it`

> Ciao {{1}}, la tua prenotazione da {{2}} è confermata: {{3}} alle {{4}}, {{5}} persone.
> Se qualcosa cambia, puoi modificarla o annullarla da qui.

Pulsante (URL, suffisso dinamico): **Modifica o annulla** → link di gestione della
prenotazione su Resmio. **Un solo pulsante, nessun «Confermo»**: il pulsante serve a chi
disdice. Mai link di annullamento GHL (annullano in GHL, il tavolo su Resmio resta).

**Il link di gestione Resmio** (contributo di Andrea Chirivì e Luciano Purpi,
2026-10-12): ogni prenotazione Resmio porta un `user_cancel_authentication_code`;
`https://app.resmio.com/external/<codice>` apre la pagina dove il cliente modifica o
annulla da solo. Il PONTE scrive il codice in un campo del contatto (es.
`contact.<campo_codice_gestione>`), prendendolo dalla **prossima prenotazione
attiva** del contatto. ⚠️ Versione superata da NON usare: uno scenario Make che
ricopia il codice ogni 5 minuti, perché sovrascrive il campo coi codici di
prenotazioni annullate (chi annulla e riprenota). **Ordine obbligato**: prima il
campo popolato, poi il template — altrimenti il pulsante arriva rotto davanti al
cliente. L'URL dinamico è base fissa + variabile IN CODA, con solo il codice nella
variabile; Meta vuole un esempio anche per la variabile del pulsante. Testo
consigliato: "fallo dal pulsante qui sotto: si aggiorna subito".

| Var | Mappa | Esempio |
|---|---|---|
| {{1}} | Contatto → Nome | Marco |
| {{2}} | nome locale (custom value) | Trattoria Esempio |
| {{3}} | data prenotazione (custom field booking) | sabato 12 ottobre |
| {{4}} | ora prenotazione | 20:30 |
| {{5}} | coperti | 4 |

## 2. Promemoria del giorno — Utility
Nome: `promemoria_prenotazione_it`

> Ciao {{1}}, ti aspettiamo oggi alle {{2}} da {{3}}. Se hai un imprevisto, puoi
> modificare o annullare da qui: il tavolo torna libero per qualcun altro.

Pulsante (URL): **Modifica o annulla** → link di gestione Resmio. Invio **4 ore prima**:
è il flusso che ripaga il canale (ogni disdetta anticipata è un tavolo rivenduto).
Mai chiedere conferma.

| Var | Mappa | Esempio |
|---|---|---|
| {{1}} | Contatto → Nome | Marco |
| {{2}} | ora prenotazione | 20:30 |
| {{3}} | nome locale | Trattoria Esempio |

## 3. Attesa conferma (prenotazione non ancora confermata) — Utility
Nome: `prenotazione_non_confermata`

> Ciao {{1}}, abbiamo ricevuto la tua richiesta per {{2}} alle {{3}}. Stiamo verificando
> la disponibilità e ti scriviamo qui appena confermata.

Nessun pulsante obbligatorio (eventuale: **Annulla richiesta**).

## 4. Richiesta di consenso — Marketing
Nome: `<cliente>_<offerta>_consenso`

Il template che apre la relazione **non manda l'offerta: chiede se la vuole**
(pattern Barresi, funziona). Fa tre cose insieme: dichiara perché hai il numero,
raccoglie un consenso esplicito e tracciabile, e sposta il seguito dentro le 24 ore,
dove il testo è libero e non serve più nessun template.

> Ciao {{1}}, sono {{2}} di {{3}}. Ho il tuo numero perché sei stato nostro cliente.
> Vorrei regalarti {{4}}. Vuoi riceverlo qui su WhatsApp?
> Se non ti interessa non fare niente: non ti scrivo più.

Pulsanti: **Sì, lo voglio** · pulsante nativo **Marketing opt-out**

| Var | Mappa | Esempio |
|---|---|---|
| {{1}} | Contatto → Nome | Marco |
| {{2}} | nome del titolare | Francesco |
| {{3}} | nome locale | Trattoria Esempio |
| {{4}} | il regalo, senza codici | una Gift Card da 20 euro |

"Se non ti interessa non fare niente" è l'opt-out più gentile che esista. Chi preme
**Sì** → tag `consenso-marketing` + campi consenso (vedi `consenso-e-liste.md`) e, dentro
le 24 ore, testo libero col link al regalo.

## 5. Riattivazione (cliente che non torna da tempo) — Marketing
Nome: `<cliente>_ritorno_it` — solo a chi ha il consenso.

> Ciao {{1}}, è da un po' che non ti vediamo da {{2}}. Abbiamo {{3}}: ti teniamo un tavolo?

Pulsanti: **Prenota** (URL con `source=whatsapp-ritorno`) · **Marketing opt-out**

## 6. Offerta / Gift card — Marketing
Nome: `<cliente>_<offerta>_promemoria` oppure `<cliente>_premio_<cosa>_it`

> Ciao {{1}}, il tuo regalo da {{2}} ti aspetta: {{3}}. Lo trovi qui, mostralo al tavolo.

Pulsanti: **Apri il regalo** (URL alla pagina personale del contatto, dove vive
l'eventuale QR/codice) · **Marketing opt-out**

⚠️ Niente codice personale nel corpo (forma di OTP → rifiuto automatico): il codice
sta sulla pagina linkata.

**Promemoria gift card a 7 e 17 giorni** (contributo di Luciano Purpi, 2026-10-12),
con due template diversi, pulsante "Prenoto un tavolo" su entrambi: al giorno 7
"ha una scadenza" senza indicare il numero di giorni; al giorno 17 "scade fra pochi
giorni e sarebbe un peccato sprecarla" (pensati per una validità di 21 giorni: se
cambia la durata, ricalcolare i giorni). Finestra lun-sab 11:00-19:00, guardia (non
prenotata, non `whatsapp-stop`), rientro OFF, "Interrompi alla risposta" ON. Una
coda di invii programmati su questi template non va in revisione.

## 7. Richiesta recensione — Marketing
Nome: `richiesta_recensione_it`

> Ciao {{1}}, com'è andata da noi? Trenta secondi, non di più.

Pulsanti: **Lascia una recensione** · **Marketing opt-out**

⚠️ Flusso, apertura, link e misura (contributo di Andrea Chirivì e Luciano Purpi,
2026-10-12 — struttura e misura confermate, risultati specifici da verificare su
ogni cliente):
- **Flusso anti-ripetizione**: trigger campo stato → `arrived`; guardia in testa
  (tag `recensione-richiesta` → fine); tag; attesa 12 ore; invio del template;
  attesa 60 giorni; rimozione tag; finestra di invio 10:00-20:00; rientro ON; ramo
  inglese solo se serve davvero.
- **Apertura**: evita un'anteprima che non dà un motivo per aprire (il nome del
  locale è già il mittente, non ripeterlo in apertura).
- **Link**: il **pulsante URL** apre il browser interno di WhatsApp, dove Google
  può chiedere un accesso che molti non fanno (tasso di clic basso osservato). Il
  **link scritto nel corpo del messaggio** apre invece il browser di sistema e
  converte meglio: usa un template Marketing col link nel testo e
  `{{contact.id}}` in coda per tracciare la singola persona. Mai un redirect lento
  del sito del cliente: se serve una pagina-redirect propria, deve essere veloce
  (es. `/recensione/` → 301/302 verso `search.google.com/local/writereview?placeid=…`).
  Altri canali: QR al tavolo, sondaggio di gradimento su pagina propria col
  pulsante Google mostrato a **tutti** (mai filtrare chi recensisce).
- **Misura**: clic totali = URL statico verso il redirect proprio; clic per persona
  = URL dinamico con `{{contact.id}}` + pagina che registra; nodo WhatsApp →
  Statistiche (Total, Pending, Sent, Delivered, Read, Failed). **"Read" è un
  pavimento** (chi ha spento le conferme di lettura non conta): mai dire "l'80% non
  apre" basandosi solo su Read.

## 8. Compleanno — Marketing
Nome: `<cliente>_compleanno_it`

> Ciao {{1}}, buon compleanno da tutti noi di {{2}}! Per festeggiarlo ti abbiamo
> preparato {{3}}. Ti aspettiamo.

Pulsanti: **Prenota** · **Marketing opt-out**

## 9. Avviso staff (alert interno) — Utility
Nome: `avviso_staff`

Arriva al numero di una persona del locale (non al cliente) quando serve un umano:
disdetta, richiesta di modifica, messaggio non smistato. Ce l'ha solo Noolas e
servirebbe a tutti (contributo di Luciano Purpi, 2026-09-13). Si innesca col
pattern-ponte "tag al contatto dello staff → workflow → template → rimuovi tag".

> Avviso {{1}}: {{2}} ha scritto su WhatsApp e serve una risposta. Motivo: {{3}}.

| Var | Mappa | Esempio |
|---|---|---|
| {{1}} | nome locale | Trattoria Esempio |
| {{2}} | nome cliente | Marco Rossi |
| {{3}} | motivo | disdetta di stasera |

## Schema vincente e testi già approvati da Meta (contributo di Luciano Purpi, 2026-10-12)

Schema approvato al primo colpo su più locali: si scrive col nome proprio del
titolare + locale e città, si spiega perché si ha il numero, **una sola cosa alla
volta** senza codici, un pulsante che è la risposta, opt-out morbido in chiusura.

Testi che sono passati l'approvazione (adattare solo nome locale/importi, non la
struttura): consenso con regalo ("Ho {{importo}} euro in regalo per te… rispondi
Sì e ti arrivano… Se non ti interessa non fare niente e non ti scrivo più :)",
pulsante "Sì, mandami i {{importo}} euro"); raccolta consenso pura dopo una
riapertura di conversazione; richiesta recensione IT/EN con opt-out testuale "Non
scrivermi piu"; premio al cliente affezionato col pulsante "Prenoto e te lo dico →".
I testi integrali completi stanno nella skill locale dell'autore: da chiedere come
contributo futuro.

**Catena completa collaudata** (contributo di Andrea Chirivì e Luciano Purpi,
2026-10-12): contatto del responsabile con tag `staff-interno`; template Utility
`avviso_staff_<cliente>` corto, **senza variabili né header** (si approva in
minuti); scenario Make `RBR-Handover-Alert-<Cliente>` ogni 10 minuti che cerca
`contacts/search` coi tag `human handover` → se trovati, tag `avvisa-<responsabile>`
sul contatto del responsabile → iterator sui clienti → tag `handover-avvisato` +
rimozione del tag `human handover`; Private Integration dedicata (contatti e
conversazioni r/w); workflow di 3 blocchi: Tag added → template (Enable branches
OFF) → Remove tag (per riarmare). È un **campanello**, non il registro: più
handover ravvicinati danno un solo avviso ed è normale, le richieste vere restano
in GHL (conversazione assegnata + task). Latenza massima = intervallo della
vedetta (circa 6 minuti dall'handover al messaggio letto).

**Limiti della notifica interna**: il nodo WhatsApp del workflow non accetta un
numero libero (solo "Utente specifico" o "Titolari assegnati"); solo l'SMS ha un
campo libero, e funziona solo col sistema telefonico GHL attivo; l'**email** è
quella che arriva sempre, come riserva. "Success" nel log vuol dire **spedito**, non
arrivato: si verifica chiedendo al destinatario. Meta vede male le utility non
dirette al cliente finale.

⚠️ Variante con dati (da verificare prima di adottarla): con l'avviso generico lo
staff annullava la disdetta sul gestionale solo in circa l'80% dei casi; proposta
non ancora validata: template con nome, motivo, data, coperti + "se è una disdetta
annulla sul gestionale", con lo scenario Make che scrive 4 campi sul contatto del
responsabile prima di mettere il tag.
