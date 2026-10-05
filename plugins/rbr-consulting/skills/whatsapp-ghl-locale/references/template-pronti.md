# Template WhatsApp pronti per un locale

> Contributo di Luciano Purpi (2026-09-04), con insieme minimo, nomi e pattern del
> consenso dal contributo del 2026-09-13. Prima ogni consulente li riscriveva da zero,
> moltiplicando il rischio di rifiuto: parti da qui e adatta solo nome del locale e tono.

Sono **bozze da mandare in approvazione**, non testi già approvati su ogni conto.
Prima di inviarle rileggi `trappole-template.md` (niente codici nei Marketing, niente
alcol, variabili dall'albero e non dalla ricerca, contenuto di esempio per ogni `{{n}}`).

## Regole comuni

- **Variabili numerate** `{{1}}`, `{{2}}`…: in tabella sotto ogni template c'è a cosa
  mapparle. Nome = `{{contact.first_name}}` scelto navigando l'albero (Contatto →
  Nome), MAI dalla ricerca (`paymentLink.contact.first_name` resta vuoto).
- Ogni `{{n}}` ha un **contenuto di esempio** (es. "Marco", "sabato 12 ottobre", "20:30").
- **Pulsanti** al posto delle domande aperte.
- **Marketing**: pulsante nativo **"Marketing opt-out"** sempre.
- **Link** con `source=whatsapp-<campagna>` per misurare (vedi `costi-limiti-misura.md`).
- Nome: `<funzione>_<lingua>` per il servizio, `<cliente>_<funzione>_<lingua>` per il
  marketing (lingua in coda).
- Non nominare mai bevande alcoliche; l'offerta nel dettaglio vive sulla landing.

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

## 7. Richiesta recensione — Marketing
Nome: `richiesta_recensione_it`

> Ciao {{1}}, grazie per essere stato da {{2}}. Ci lasci un parere? Ci aiuta tantissimo.

Pulsanti: **Lascia una recensione** (URL Google con `source=whatsapp-recensione`) ·
**Marketing opt-out**

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
