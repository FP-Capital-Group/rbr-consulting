# CRM e moduli — dal sito al GoHighLevel del cliente, e cosa succede dopo

Il sito non è finito quando il modulo «invia»: è finito quando il contatto arriva nel CRM del cliente con i dati
giusti e parte la cosa giusta (avviso allo staff, risposta al cliente, poi marketing solo a chi ha detto sì).
Quadro completo delle fonti e dei flussi → `checklist-marketing-rbr`; setup del sub-account → `onboarding-cliente-ghl`.

## 0. Prima del sito: il sub-account del cliente
- Sub-account GHL **del cliente** (creato dall'agenzia RBR, pagato secondo accordo), snapshot RBR applicato, modello
  base a tre strati (fondamenta → servizio → crescita) da `onboarding-cliente-ghl/references/modello-base-locale.md`.
- Impostazioni: «Allow duplicate contact» **spento** (dedup su email/telefono), fuso Europe/Rome, mittente email dal
  dominio del cliente verificato (SPF/DKIM/DMARC).
- Campi personalizzati del modello base che il sito usa (crea quelli che mancano, tipo giusto):
  | Chiave GHL | Tipo | Dal sito |
  |---|---|---|
  | `pv` | testo/tendina | locale scelto (nome uguale alle opzioni del campo) |
  | `lingua` | testo | `it` / `en` |
  | `giorno_prenotazione` | data | AAAA-MM-GG |
  | `orario_prenotazione` | testo/tendina | `20:30` |
  | `numerodipersone` | numero | persone |
  | `compleanno_gg_mm` | testo | `05/03` (giorno/mese, senza anno) |
  | `gdpr_email`, `gdpr_whatsapp`, `marketing_consent`, `privacy_policy` | consensi | li scrive il passo «Consensi» dei flussi S1-S4 quando c'è il tag `consenso-marketing` (la casella del sito elenca i canali: email, WhatsApp, SMS) |
- Valori delle tendine **identici carattere per carattere** alle opzioni del sito (accenti, «·», maiuscole).
- Private Integration Token **del sub-account** (non dell'agenzia) per il sito: scope `contacts.write`,
  `contacts.readonly`. Nome «Sito web <dominio>», così si riconosce e si revoca.

## 1. Moduli: due strade (una per sito)
| | A. Plugin `rbr-moduli` (consigliata) | B. Modulo/sondaggio nativo GHL incorporato |
|---|---|---|
| Aspetto | stili del tema, bilingue IT/EN | iframe GHL, stile limitato, traduzione a parte |
| Dove gira | WordPress del cliente | GHL del cliente |
| Setup | zip + 2 costanti in wp-config | codice embed → blocco HTML |
| Se GHL non risponde | mail + copia in bacheca | perso |
| Cookie | nessuno di terzi | iframe di terzi (nel banner) |

Mai: FormSubmit, Make/Google Sheet come destinazione, il builder `/api/form-submit` o altri server RBR, la pipeline di
vendita `ristoranteonline.ai`. Il lead nasce nel sub-account del cliente.

### Plugin rbr-moduli (`assets/rbr-moduli.zip`)
Collaudato in WordPress Playground il 12/10/2026 con un GHL finto: upsert con campi personalizzati → tag → nota ok;
campi errati → 422; gettone o ora falsificati → 403; oltre 5 invii in 10 minuti dallo stesso IP → 429; GHL spento →
mail + copia in *Moduli → Invii* (cancellata da sola dopo 90 giorni: scriverlo nell'informativa).
⚠️ Al primo sito vero: prova su GHL reale e annota qui l'esito.

Installazione:
1. *Plugin → Aggiungi → Carica* `rbr-moduli.zip` → Attiva.
2. `wp-config.php` (file manager dell'hosting), sopra «That's all, stop editing»:
   `define( 'RBR_GHL_TOKEN', 'pit-…' ); define( 'RBR_GHL_LOCATION', '<location id>' );`
3. Menu *Moduli*: email notifiche (casella del ristorante; più indirizzi separati da virgola), locali (uno per riga,
   uguali alle opzioni di `pv`; vuoto = locale unico), orari prenotabili, tag fonte (default `lead-sito-<dominio>`),
   pagina privacy, mappa campi («campo del modulo = chiave GHL», già precompilata col modello base).
4. Nelle pagine: blocco **Shortcode** — `[rbr_modulo tipo="prenotazione"]`, `tipo="evento"`, `tipo="contatto"`,
   `tipo="novita"` (con compleanno facoltativo); `bottone="Testo"` cambia il pulsante.

Per ogni invio:
- `POST /contacts/upsert` con nome, email, telefono (`00…`→`+…`, italiani →`+39…`) e campi personalizzati (chiave
  SENZA `contact.`: con il prefisso GHL li ignora in silenzio); `source = Sito <dominio>` solo sui contatti nuovi
  (non si cancella l'attribuzione Meta/coupon dei vecchi).
- `POST /contacts/{id}/tags`: `lead-sito-<dominio>`, `form-<tipo>`, `pv-<locale>`, `consenso-marketing` (solo se
  spuntato), `lingua-en`.
- `POST /contacts/{id}/notes`: riepilogo con provenienza (utm/referrer), pagina, lingua, consenso e ora della privacy.
- Mail al ristorante (Reply-To = cliente). Se il CRM fallisce la mail lo dice.
Il token resta in PHP sul server del cliente, mai nel browser. (La regola «GHL sempre via MCP» riguarda il lavoro di
Claude, non il codice del sito.)

Varianti: ordini (torte, asporto) → tipo nuovo con righe e totale nella nota, pagamento al ritiro; campi in più →
aggiungili al modulo e alla mappa campi.

## 2. Tag: regole
- Tag = stato o fonte che si accende/spegne; dato con tanti valori = campo (mai anno di nascita o piatto preferito in tag).
- Minuscolo, trattini. Famiglie del sito (da aggiungere a quelle ammesse del modello base): `lead-sito-<dominio>` (fonte), `form-<tipo>` (innesco, si TOGLIE in coda al flusso), `pv-<locale>` (come il modello base), `consenso-marketing`, `lingua-en`.
- Non usare tag che fanno partire funnel vecchi dello snapshot (es. `locale`, `turista` facevano partire 9 mail
  generiche su Raíces): prima di scegliere un tag controlla quali workflow lo usano come innesco.
- I flussi del sito partono su **tag aggiunto** `form-<tipo>` e **lo tolgono come ultimo passo**: «Tag aggiunto» scatta
  solo se il tag non c'era, quindi senza la rimozione il secondo invio dello stesso cliente non avvisa più la sala.
  I flussi delle prenotazioni del gestionale partono invece sul **campo di stato** (Contact Changed), perché i tag del
  ponte si sommano.

## 3. Flussi GHL da creare per il sito (in bozza → test → attivi)
Nomi `<nn> · <nome> — <canale>` come nel modello base. Regole per tutti:
- Avvisi allo staff = **Internal Notification di tipo EMAIL** a un utente/indirizzo preciso. Mai «Send Email» (scrive al
  cliente!) e mai Notifica interna SMS se il sub-account non ha il Sistema telefonico (risulta «eseguito» ma non parte).
- Nessuna firma personale del consulente; mittente e firma del locale.
- Messaggi promozionali solo con `consenso-marketing` (o consenso del canale).
- Ogni flusso finisce con **Remove tag `form-<tipo>`** (così riparte al prossimo invio) e, se il contatto ha
  `consenso-marketing`, un passo **Consensi**: Update contact fields `marketing_consent`, `gdpr_email`, `gdpr_whatsapp`
  = sì (valori come definiti nel sub-account).

Prompt per *Automation → Workflows → Build using AI* (adatta nomi, indirizzi, campi; poi apri ogni passo e controlla):

**S1 · Richiesta di prenotazione dal sito — email**
```
Create a workflow named "S1 · Richiesta prenotazione sito — email".
Trigger: Contact Tag Added, tag = form-prenotazione.
Actions:
1. Internal Notification, type Email (NOT Send Email), to <email del locale>. Subject: "Nuova richiesta di prenotazione - {{contact.pv}}". Body: name, phone, email, pv, giorno_prenotazione, orario_prenotazione, numerodipersone and the latest note. Add the line "DA RICHIAMARE: la prenotazione NON è ancora confermata".
2. Send email to the contact: "Abbiamo ricevuto la tua richiesta per {{contact.pv}} il {{contact.giorno_prenotazione}} alle {{contact.orario_prenotazione}} per {{contact.numerodipersone}} persone. Ti richiamiamo a breve per confermare." (English version if contact has tag lingua-en.)
3. If the contact has tag consenso-marketing: update contact fields marketing_consent, gdpr_email, gdpr_whatsapp to yes.
4. Remove tag form-prenotazione (last step, so the workflow starts again at the next request).
Keep the workflow in draft.
```
(Se le prenotazioni vere passano dal widget TheFork/Resmio, questo modulo è il «richiamami»: il testo resta «ti
richiamiamo», mai «prenotazione confermata».)

**S2 · Richiesta evento — email + pipeline** (crea prima la pipeline «Eventi e feste»: il modello base non ha pipeline per i tavoli, ma per gli eventi con preventivo sì)
```
Create a workflow named "S2 · Richiesta evento sito — email".
Trigger: Contact Tag Added, tag = form-evento.
Actions:
1. Create an opportunity in pipeline "Eventi e feste", stage "Richiesta ricevuta", name = "{{contact.name}} - {{contact.pv}} - {{contact.giorno_prenotazione}}".
2. Internal Notification, type Email (NOT Send Email), to <email eventi>. Subject: "Nuova richiesta evento - rispondere entro 2 ore". Body: name, phone, email, pv, giorno_prenotazione, numerodipersone and the latest note.
3. Send email to the contact: "Grazie, abbiamo ricevuto la tua richiesta. Ti contattiamo entro poche ore con una proposta."
4. If the contact has tag consenso-marketing: update contact fields marketing_consent, gdpr_email, gdpr_whatsapp to yes.
5. Remove tag form-evento.
6. Wait 2 days. If the opportunity is still in stage "Richiesta ricevuta", send the same internal email again with subject prefix "PROMEMORIA:".
Keep the workflow in draft.
```

**S3 · Contatto dal sito — email**: trigger `form-contatto` → Internal Notification email allo staff con nota +
risposta automatica breve al cliente → passo Consensi → Remove tag `form-contatto`.

**S4 · Iscrizione novità / club — benvenuto**
```
Create a workflow named "S4 · Iscrizione dal sito — benvenuto email".
Trigger: Contact Tag Added, tag = form-novita.
Condition: continue only if the contact has tag consenso-marketing.
Actions:
1. Send email "Benvenuto!" with what the subscriber gets (the welcome gift, how to redeem it in the restaurant, birthday treat). No discount codes as main lever: a gift.
2. Internal Notification, type Email (NOT Send Email), to <email del locale>: "Nuovo iscritto: {{contact.name}} {{contact.phone}} - {{contact.pv}}".
3. Update contact fields marketing_consent, gdpr_email, gdpr_whatsapp to yes.
4. Remove tag form-novita (also when the condition is not met).
Keep the workflow in draft.
```
Poi il resto della crescita (compleanno, riaggancio, recensione dopo la visita) è nel modello base GHL e nelle skill
`mail-funnel-ghl`, `whatsapp-ghl-locale`, `risposte-recensioni-ai-ghl`.

## 4. Chat sul sito (facoltativa)
- Solo se qualcuno la presidia o se c'è la Conversation AI configurata (`onboarding-cliente-ghl/references/conversation-ai.md`).
  Solo chat testuale, niente assistente vocale sul sito.
- Widget chat GHL: è uno script di terzi → sotto il banner cookie; colore di marca; lingua EN su `/en/`; il fumetto
  **non deve coprire il prenotatore** su mobile (nascondilo sulle pagine prenota o spostalo). L'icona del bottone va
  verificata (su Cartabianca era rotta).
- La chat che raccoglie una prenotazione mette gli stessi tag (`form-prenotazione`) così parte lo stesso flusso S1.

## 5. Notifiche senza server
Le notifiche Telegram dei vecchi siti passavano dal server di Marco: sui siti cliente si usano l'app LeadConnector
(push sul telefono del titolare) e le Internal Notification email. Niente bot da ospitare.

## 6. Collaudo CRM (per ogni tipo di modulo usato)
1. Invio reale dal sito (telefono + desktop, IT ed EN) con email `nome@rbr-test.local` e un telefono di prova.
2. GHL: contatto creato una volta sola, campi personalizzati pieni, tag giusti, nota completa, `source` giusto.
3. Mail di notifica arrivata alla casella del ristorante (non in spam).
4. Flusso S1-S4 partito (registro del workflow) e il passo «Internal Notification» è di tipo Email.
5. Invia due volte con lo stesso telefono: nessun doppione E il flusso riparte la seconda volta (tag `form-<tipo>`
   tolto in coda al primo giro).
6. Cancella i contatti di prova.
