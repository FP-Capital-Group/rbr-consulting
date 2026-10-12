# Moduli del sito → CRM GoHighLevel del cliente

## Due strade (scegli una per sito, non mescolarle)
| | A. Plugin `rbr-moduli` (consigliata) | B. Modulo/sondaggio nativo GHL incorporato |
|---|---|---|
| Aspetto | stili del tema, bilingue IT/EN | iframe GHL, stile limitato, va tradotto in GHL |
| Dove gira | sul WordPress del cliente | sul GHL del cliente |
| Setup | zip + 2 costanti in wp-config | copia codice embed da GHL → blocco HTML |
| Se GHL non risponde | mail + copia in bacheca | perso |
| Cookie | nessun cookie di terzi | iframe di terzi (va nel banner) |

Mai: FormSubmit, Make/Sheet come destinazione dei lead, il builder `/api/form-submit` di Marco, la pipeline di
vendita `ristoranteonline.ai`. Il lead nasce nel sub-account del cliente.

## Plugin rbr-moduli (cartella `assets/rbr-moduli/` della skill)
Collaudato in WordPress Playground il 12/10/2026 con un finto GHL: upsert → tag → nota corretti; campi errati
→ 422 con l'elenco; gettone/ora falsificati → 403; più di 5 invii in 10 minuti dallo stesso IP → 429; GHL spento →
mail + copia in *Moduli → Invii* (cancellata dopo 90 giorni: scriverlo nell'informativa). ⚠️ Al primo sito vero:
prova su GHL reale e annota l'esito qui.

Installazione:
1. Carica `assets/rbr-moduli.zip` (già pronto) da *Plugin → Aggiungi → Carica* → Attiva. Se modifichi il plugin, rifai lo zip della cartella `rbr-moduli/`.
2. GHL del cliente → *Impostazioni → Private Integrations* → nuovo token «Sito web», scope
   `contacts.write` + `contacts.readonly` (solo quelli). Location ID da *Impostazioni → Business Profile*.
3. `wp-config.php` (file manager dell'hosting), sopra «That's all, stop editing»:
   `define( 'RBR_GHL_TOKEN', 'pit-…' ); define( 'RBR_GHL_LOCATION', '…' );`
4. *Moduli* (menu admin): email notifiche (casella del ristorante, più indirizzi separati da virgola), locali
   (uno per riga; vuoto = locale unico), orari prenotabili, tag fonte (default `lead-sito-<dominio>`), pagina privacy.
5. Nelle pagine: blocco **Shortcode** `[rbr_modulo tipo="prenotazione"]` — tipi `prenotazione`, `evento`,
   `contatto`, `novita`; `bottone="Testo"` per cambiare il pulsante.

Cosa scrive in GHL per ogni invio:
- `POST /contacts/upsert` (dedup su email/telefono secondo l'impostazione «Allow duplicate contact» del sub-account: tenerla SPENTA); telefono: `00…` → `+…`, numeri italiani → `+39…`; `source = Sito <dominio>` solo se il contatto è nuovo (non si sovrascrive l'attribuzione Meta/coupon dei vecchi)
- `POST /contacts/{id}/tags` → `lead-sito-<dominio>` (tag fonte, come da DoD WEB-5; cambiabile in *Moduli*), `form-<tipo>`, `sede-<locale>`, `consenso-marketing`
  (solo se spuntato: la casella non è mai pre-spuntata), `lingua-en`
- `POST /contacts/{id}/notes` → riepilogo (locale, giorno, ora, persone, messaggio, provenienza utm/referrer,
  pagina, lingua, consenso, data/ora accettazione privacy)
- mail al ristorante con Reply-To = cliente

Il token resta sul server del cliente (PHP), mai nel browser. È il sito del cliente che parla col CRM del
cliente: la regola «GHL sempre via MCP» riguarda il lavoro di Claude, non il codice del sito.

Varianti frequenti (modifica il plugin, mantieni i nomi dei tag):
- campi custom GHL (es. `Locale preferito`, data di nascita per il club) → aggiungi a `customFields`
  nell'upsert con l'**id** del campo letto via MCP `ghl2-<cliente>`; valori delle tendine identici
  carattere per carattere a quelli del campo GHL;
- ordine torte/asporto → tipo nuovo con righe e totale nella nota; pagamento al ritiro (gateway solo se il
  cliente lo chiede, col SUO Stripe/SumUp/Satispay).

## Workflow GHL da creare nel sub-account (in bozza, poi attivi dopo il test)
- **Trigger: tag aggiunto `form-prenotazione`** → *Internal Notification* allo staff (mail/app/SMS al
  responsabile) + mail/WhatsApp al cliente «abbiamo ricevuto la richiesta». Se le prenotazioni vere passano
  da TheFork/Resmio, il modulo è solo «richiamami»: niente conferme automatiche di un tavolo che non esiste.
- `form-evento` → opportunità in pipeline «Eventi» + avviso al responsabile eventi.
- `form-novita` + `consenso-marketing` → benvenuto / club (→ `mail-funnel-ghl`, `whatsapp-ghl-locale`).
- ⚠️ Il «Build using AI» di GHL mette gli avvisi allo staff come *Send Email* al CLIENTE: cambiali sempre in
  *Internal Notification*. Non riusare tag che fanno partire funnel dello snapshot (es. `locale`, `turista`).
- Test: contatto `nome@rbr-test.local`, verifica tag/nota/workflow, poi cancellalo.

## Notifiche senza server
Le notifiche Telegram dei vecchi siti passavano dal server di Marco: sui siti cliente si usa l'app GHL
(LeadConnector) o una *Internal Notification* via SMS/email. Niente bot da ospitare.
