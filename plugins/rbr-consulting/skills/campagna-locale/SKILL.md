---
name: campagna-locale
description: >-
  Pipeline RBR per lanciare una campagna offerta di un locale, dall'idea al coupon in cassa. Usala ogni volta che devi far partire una promo di un ristorante — "lanciamo un'offerta per il locale", "creiamo una landing per la promo 10 euro", "genera il QR e il codice sconto", "campagna coupon per i turisti", "mandiamo la mail dell'offerta ai clienti". Copre tutto il flusso: offerta → landing WordPress parametrizzata → QR code → coupon sul POS iPratico → email nel CRM GHL. NON improvvisare landing o codici a mano: segui questa pipeline per non rompere il tracciamento e la cassa.
---

# Campagna locale (offerta → landing → QR → coupon → email)

## Perché esiste
In RBR un'offerta non è "un post con uno sconto": è una **catena tracciata** che parte dall'idea e arriva al coupon che lo staff scansiona in cassa. Ogni anello ha un codice univoco (`code`) che lega landing, QR, POS e CRM. Se salti un passaggio o inventi un codice a mano, il tracciamento si spezza: non sai più quanti clienti sono arrivati da quale canale, e la cassa non riconosce lo sconto. Questa skill fissa l'ordine giusto e gli strumenti giusti.

## Quando usarla
- Devi lanciare una promo di un locale (sconto €, %, prodotto gratis) su uno o più canali.
- Devi creare la landing di un'offerta e il relativo QR/coupon.
- Devi rigenerare o clonare un'offerta esistente per un nuovo target (es. turisti EN, riattivazione).
- Serve mandare ai clienti la mail con il codice/QR dell'offerta.

## Prerequisiti
- **Sheet master offerte/landing** del locale (sorgente di verità dei `code`, URL landing, URL QR). Per Mister Pizza: Sheet 1 "Modifiche sito" (mapping offerta→URL + source) e Sheet 2 "Descrizioni offerte + QR". Ogni locale ha i suoi.
- Accesso **WordPress** del sito (REST API + Application Password) per pubblicare/parametrizzare la landing.
- Accesso al **POS iPratico** del locale per creare il coupon (installazioni separate per brand — es. Mister Pizza e Dirigì sono account distinti).
- Istanza MCP CRM del cliente (`ghl2-<cliente>`) per l'email; token nel `.env`, mai in chiaro nel file.
- Tono email RBR (vedi Regole).

## Procedura

### 1. Definisci l'offerta e il `code`
Fissa: tipo sconto (€, %, prodotto gratis), target (italiani / turisti EN / riattivazione / hotel…), canale (facebook-adv, google-adv, instagram, riattivazione, hotel). Genera un `code` **parlante**: a vista deve dire offerta + target (es. `10euroturistaeng1`, `BRO10EU`, `10eurosett2`). Formato libero ma chiaro. Registra il `code` nello Sheet master — **è lui la chiave di tutta la catena**.

### 2. Landing page parametrizzata (WordPress)
Le landing sono già pubblicate e riusabili: cambia solo il querystring, non la pagina.
- Pattern URL: `https://<dominio>/<offerta>?code=<code>&source=<source>`
- Esempio: `https://www.misterpizza.it/10euro?code=10euroturistiita1&source=riattivazione`
- Mappa `offerta` → URL base dallo Sheet (es. 5euro, 10euro, 20euro, siciliana, calabrese). Se l'offerta è nuova, crea la landing base una volta sola, poi riusala parametrizzata.

### 3. QR code
Genera il QR che **contiene il `code` in chiaro** (lo staff lo scansiona in cassa, non serve che punti a un URL):
`https://quickchart.io/qr?size=800&captionFontSize=50&text=<code>`
Salva l'URL del QR nello Sheet 2 (Descrizioni offerte + QR), riga del `code`, con descrizione offerta nella lingua del target (turisti EN → inglese, italiani → italiano).

### 4. Coupon sul POS (iPratico)
Per ogni `code` creato va ricreato il coupon sul gestionale iPratico del locale.
- **Mapping 1:1 offerta→coupon**: `5euro`→€5 off, `10euro`→€10 off, `20euro`→€20 off, `siciliana`→pizza siciliana gratis, `calabrese`→pizza calabrese gratis. Offerta nuova = nuovo mapping da decidere col cliente.
- **Scadenza coupon**: durata lunga fissa `2025-01-01 → 2030-12-31`. Al pubblico non si comunica nessuna regola di scadenza.
- Se il locale ha più brand/installazioni, **replica il coupon su ciascuna** (stesso `code`, POS diversi).

### 5. Email nel CRM (GHL)
Manda ai clienti la mail con codice/QR via istanza MCP `ghl2-<cliente>` (segmenta per tag: città, target, riattivazione).
- **Tono asciutto, no marketing-speak**: al centro il codice e lo sconto, non gli aggettivi. "10€ di sconto da Mister Pizza. Mostra questo QR in cassa." Niente frasi da brochure.
- Rispetta eventuali frame di campagna (es. Glovo Firenze: mai nominare il vecchio partner, solo messaggio forward-looking).
- L'invio email a terzi è un'azione a conferma: prepara la bozza e il segmento, poi chiedi l'ok prima di spedire.

### 6. Registra e verifica
Scrivi tutto nello Sheet master (code, landing, source, QR) così resta la sorgente di verità. Verifica la catena end-to-end prima di dichiarare chiusa la campagna (vedi DoD).

## Regole RBR & trabocchetti
- ⚠️ **Il `code` è la chiave di tutto**: usa SEMPRE il `code` esatto dello Sheet, non normalizzarlo (i prefissi non sono uniformi, es. `turistiita1` vs `turistaita2`). Un code sbagliato = anello rotto.
- ⚠️ **Landing = riuso parametrizzato**, non pagina nuova ogni volta. Cambia il querystring `?code=&source=`, non duplicare la pagina.
- ⚠️ **iPratico è manuale e per-installazione**: quello che fai su un brand va replicato sull'altro. Non dare per scontato che il coupon esista già.
- ⚠️ **Mai token/API key nel repo** (condiviso col team): CRM via MCP `ghl2-<cliente>`, credenziali WordPress e POS dal `.env`.
- ⚠️ **WordPress dietro Cloudflare/WP Engine**: i fetch non-browser possono dare 403 → usa il client REST autenticato con User-Agent browser; dopo modifiche svuota la cache.
- 🟡 **Email**: sempre conferma prima dell'invio a clienti reali; tono asciutto codice/sconto.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] `code` parlante creato e scritto nello Sheet master (offerta + target riconoscibili)
- [ ] Landing raggiungibile con URL parametrizzato `?code=&source=` (verificata 200)
- [ ] QR generato con `text=<code>` e URL salvato nello Sheet 2 + descrizione nella lingua del target
- [ ] Coupon iPratico creato con mapping corretto e scadenza `2025-01-01 → 2030-12-31`, replicato su tutte le installazioni del locale
- [ ] Email preparata nel CRM con tono asciutto codice/sconto, segmento giusto, e **inviata solo dopo ok**
- [ ] Catena verificata end-to-end (scan QR → code leggibile → coupon riconosciuto in cassa)
