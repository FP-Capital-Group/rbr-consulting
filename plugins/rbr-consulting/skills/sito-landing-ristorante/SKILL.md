---
name: sito-landing-ristorante
description: >-
  Landing page di una promo/campagna di un ristorante (offerta → modulo nel GHL
  del cliente → QR) e riferimento storico del vecchio metodo siti-ristoranti
  (generatore + server di Marco, DISMESSO per i clienti dal 12/10/2026). Usala
  per "serve una landing page", "pagina per la promo", "landing della gift
  card", "QR della promo". Per un SITO COMPLETO nuovo o rifatto usa
  sito-wordpress-ristorante (WordPress sull'hosting e dominio del cliente, mai
  sui server RBR); per un WordPress esistente sito-wordpress-cliente-mcp.
---

# Sito + landing page ristorante (percorso A: sito completo · percorso B: landing di campagna)

## Perché esiste
Un ristoratore non ha bisogno di "un sito": ha bisogno di una pagina che su mobile carichi subito, mostri il menu con foto giuste, faccia prenotare in 2 tap e mandi il lead nel CRM. RBR ha già un metodo collaudato (progetto **siti-ristoranti** di Marco, `~/Desktop/AI/siti-ristoranti/`): generatore AI + template con regole hard nate da errori reali + deploy standard. Questa skill codifica quel metodo e il suo gemello leggero, la **landing di campagna**. Se improvvisi uno stack diverso, perdi le regole hard e il tracciamento.

## Quando usarla
- Un cliente ha bisogno di un sito nuovo o di rifare quello vecchio → **NON questa skill**: `sito-wordpress-ristorante`.
- Manutenzione di un sito statico già online col vecchio metodo → Percorso A (solo riferimento).
- Serve la pagina di una singola offerta/promo (coupon, gift card, riapertura, evento) → **Percorso B**.
- Devi collegare form del sito → CRM GHL del cliente, o preparare il QR di una promo.
- NON usarla per: SEO on-page e pagine local per sede/città → skill `seo-local-ristorante`; catena completa offerta→coupon→cassa → skill `campagna-locale` (la landing è solo un anello di quella catena).

## Prerequisiti
- Dati reali del locale: nome, indirizzo, telefono, orari (NAP), menu con prezzi, foto (Google Places / Instagram / foto del cliente), USP e posizionamento.
- Per il percorso A: accesso al progetto `~/Desktop/AI/siti-ristoranti/` (leggi PRIMA il suo `CLAUDE.md` — contiene le regole hard del template) e al VPS di deploy.
- Per il collegamento CRM: sub-account GHL del cliente (Location ID + Private Integration Token con scope contacts) — operazioni GHL sempre via MCP `ghl2-<cliente>`.
- Prenotazioni: widget **Resmio** del locale (facility_id) se il cliente lo usa, altrimenti form nativo del template.
- Credenziali/token sempre dal `.env` — mai in chiaro (repo condivisa col team).

---

## Percorso A — Sito completo del ristorante (⚠️ METODO DISMESSO per i clienti)

> **Dal 12/10/2026 (decisione Marco) i siti dei clienti NON si fanno più così.** Niente generatore,
> niente server/VPS di Marco, niente sottodomini `ristoranteonline.ai`, niente builder `/api/form-submit`:
> il cliente compra dominio + hosting WordPress e il sito vive lì → skill **`sito-wordpress-ristorante`**.
> Questa sezione resta solo come riferimento per i siti statici già online (Red Mike, Griss, Ca' di Pieri,
> Zio Bibi) e per le regole di design/tracciamento, che valgono anche su WordPress.

Il metodo è quello del progetto **siti-ristoranti** (`ristoranteonline.ai`): sito statico generato via AI, non un CMS.

### A1. Stack reale (non cambiarlo)
- **Node.js (ESM)** — script del generatore. Niente Python (legacy archiviato), niente WordPress per i siti nuovi.
- **Generazione AI**: `step2_generazione/generatore.js` — Gemini (vision per classificare foto e menu) con fallback Groq (`lib/llm.js`). Legge i dati del lead da GHL.
- **Acquisizione dati**: `step1_scraping/scraper.js` — lookup Google Places (placeId, stelle, recensioni, foto, indirizzo) → push lead su GHL.
- **Output**: sito statico in `output/siti/<slug>/` (HTML+CSS+JS vanilla, foto ottimizzate).
- **Deploy**: `step3_deploy/deploy_vps.js --slug <slug>` → live su `https://<slug>.ristoranteonline.ai` (HTTPS Let's Encrypt). ⚠️ I siti già migrati stanno su **Oracle** (web server **Caddy**, builder systemd su :3100): per quelli il deploy è rsync su `/var/www/sites/<slug>/` + eventuale blocco Caddyfile — e Caddy Oracle ha admin API off → **sempre `systemctl restart caddy`, mai `reload`**. `deploy_vps.js` punta al vecchio Contabo, obsoleto per i siti migrati. 🟡 **Da validare con Marco**: percorso di deploy standard per un sito NUOVO oggi (il business ristoranteonline.ai è in pausa dal 2026-06-23; per un cliente consulenza va deciso host e dominio caso per caso).

### A2. Avvio progetto nuovo (workflow "crea il sito per X")
1. **Lookup Google Places** → placeId, stelle, recensioni, indirizzo, foto.
2. **Push lead su GHL** (idempotente: se esiste, riusa l'id).
3. **Genera**: `node step2_generazione/generatore.js --contact-id <id> --city <città>`.
4. **Deploy** (mai fermarsi al locale, salvo richiesta esplicita "solo preview").
5. **Verifica visiva post-generazione** (obbligatoria, Marco l'ha chiesta esplicitamente): screenshot + lettura di OGNI foto categoria menu — la foto sotto "Primi" deve essere un primo. Mai saltarla.

Se il ristorante non ha sito/foto buone: foto Instagram scaricate con `gallery-dl` al posto delle `gp_*.jpg`, poi rigenera con `--force`. Personalizzazioni per singolo sito (palette, font, hero) → `brand-override.json` nella cartella del sito, mai a mano nel template.

**Sito di riferimento indicato dal titolare** (contributo di Andrea Chirivì, 2026-10-12): se il titolare indica un sito che gli piace, separa cosa **prendere** (impaginazione, pulsanti in alto, scorrimento fluido, home lunga con più contenuto, barra bloccata in alto) da cosa **non prendere** (delivery, ordini online, multi-sede, posizionamento "per tutti" di una catena: il locale è una destinazione). Barra fissa con il logo sopra e i quattro pulsanti sotto (Prenota, Chiama, Ordina, Menu), tutto nello stesso blocco sticky. Sui temi WordPress con sticky "slide" la barra ricompare solo quando si risale: per averla sempre visibile cambia il comportamento nel tema.

### A3. Struttura pagine tipo
- **Home** — hero con foto ambiente calda + posizionamento (attenzione: "trattoria" NON implica cucina romana — il claim segue la regione/cucina reale), card piatti cliccabili verso il menu, sezione **prenota** (form o widget Resmio) su sfondo beige liscio (mai foto di sfondo sul form), contatti/orari nel footer.
  **Checklist del sito che converte** (Piano Marketing RBR v1.0 di Roberto Falcon, Mossa 10, 2026-10-12): `<title>` nel formato "Nome — zona | promessa" con una `description` vera (caso reale: title "home" e Google che mostrava il nome del file del logo); prima schermata con **la promessa in una riga e sotto le tre prove**, mai "benvenuti nel nostro ristorante"; pulsante **PRENOTA fisso in alto**, visibile da telefono, e telefono cliccabile (già in regola, vedi sotto); **menu in testo sulla pagina**, non solo PDF o immagine; responsive sul serio — se il fornitore del sito non lo fa, si rifà ("costa meno di due serate piene"); pop-up con **un regalo concreto** (fidelity o lead magnet), mai "iscriviti alla newsletter" — sotto il 2% di conversione si riscrive (vedi A7); Pixel, tag Google e conversioni su prenotazione/chiamata/form **testati prima di avviare le Ads**.
- **Menu** — categorie con foto matchate semanticamente ai piatti (mai per indice cieco; nessun match → nessuna foto). **Ordine di abbinamento** (contributo di Andrea Chirivì, 2026-10-12 — l'abbinamento per sola somiglianza del nome sbaglia, es. "crispy chicken.jpg" finito sull'insalata Chicken invece che sul burger Crispy Chicken): (1) corrispondenze esatte su TUTTI i piatti; (2) parziali solo sui piatti rimasti; (3) a mano i file con nomi diversi dal piatto (es. "tris crocchettoni" → Triplo Crocchettone). Le foto vengono solo dalla cartella ufficiale del cliente, mai da cartelle temporanee tipo l'archivio WhatsApp personale. Si caricano in WebP a 900px.
- **Storia/Chi siamo** — la narrazione del locale, foto ambiente.
- **Contatti** — NAP completo, mappa, orari, telefono cliccabile (`tel:`). **Cucina e locale scritti separati, su tutte le pagine** (contributo di Andrea Chirivì, 2026-10-12): "cucina" va con l'ultima ordinazione, "aperti/si esce" con la chiusura del locale (es. cucina fino a mezzanotte, locale fino alle 02) — controlla anche il compilato del page builder e le description SEO; lo schema `opens`/`closes` parla del locale e resta così; nei testi si scrive per esteso ("cucina fino a mezzanotte, locale aperto fino alle 02"). Rimando alla scheda cliente di `checklist-marketing-rbr`, che separa già i tre orari.
- Opzionale: **Galleria** con lightbox (pattern esistente su Trattoria Griss).
- Opzionale: **Pagina feste e gruppi** ⚠️ (struttura confermata, risultato non ancora misurato — contributo di Andrea Chirivì, 2026-10-12): un elenco di menù senza prezzi, CTA o motivo per scegliere non vende. Struttura: cosa si festeggia (le occasioni), come si organizza in tre passi, i menù come schede in scala, cosa succede se la data cade la sera di un evento, chiamata come CTA. **"Prezzi a testa in pagina sì/no" e "torta da fuori sì/no" sono domande da fare al titolare ogni volta**, non regole fisse.
- Opzionale: **Cartellone eventi** (contributo di Andrea Chirivì, 2026-10-12): gli eventi stanno in un solo `eventi.json`; uno script genera sia la landing sia la pagina del sito, perché due copie scritte a mano divergono sempre. Una pagina generata una volta filtra le date future SOLO quando lo script gira (caso reale: la pagina eventi mostrava una serata passata col tasto "Prenota il 7"): o la pagina legge un file JS dei dati a ogni visita, o si rilancia lo script dopo ogni serata. Se non restano eventi esce un messaggio di attesa col pulsante di prenotazione. I link di prenotazione dell'evento nascono interni, con data e coperti nell'indirizzo.

### A4. Regole HARD del template (nate da errori reali — non ridiscuterle)
- ❌ Mai widget di auto-traduzione dentro il template (per i turisti → GTranslate come da skill `seo-local-ristorante`).
- ❌ Mai **FormSubmit** (formsubmit.co): bandito da Marco.
- ❌ Mai palette fredda (rosa pallido, blu, azzurro, viola, grigio): **sempre toni caldi** — rosso, arancione, ocra, terracotta, oro, bordeaux; beige = crema/sabbia.
- ✅ **Colori del brand si LEGGONO, non si scelgono a occhio** (contributo di Luciano Purpi, 2026-09-08): dal sito (colori calcolati con `getComputedStyle`, scartando la tavolozza di default di Gutenberg e i widget di terzi) e dal logo (PIL, scartando i pixel neutri); poi **contrasto WCAG ≥ 4,5:1 su ogni accostamento testo/sfondo PRIMA di applicare** — un giallo/arancio di marca su bianco sta a 2-3:1: si tiene la tinta e la si scurisce per il testo (es. #FFA600 → #9C6200), lasciando il colore pieno ai pulsanti con testo scuro. Su 10 clienti 6 palette non passavano al primo giro. Vale per sito, landing, mail, widget, coupon → metodo e snippet in `references/colori-brand.md`.
- ❌ Mai `loading="lazy"` sulle foto above-the-fold (card piatti, foto categorie).
- ✅ Mobile-first sul serio: input form min-height 48px, hamburger menu funzionante, hero leggibile su schermo piccolo.
- ✅ Se le foto Google Places sono mediocri (mani, close-up, sfocate) → hero con foto stock via `brand-override.json`.
- ✅ **Schema.org `Restaurant`** JSON-LD in ogni sito: NAP reale, geo, orari, telefono, `aggregateRating` da Places (i dettagli SEO delle pagine local → skill `seo-local-ristorante`, non duplicare qui).

### A5. Form, prenotazioni e CRM
- **Form nativo** → `POST /api/form-submit` del builder (payload `{slug, type, data}`), con fallback WhatsApp se la fetch fallisce. Il builder notifica via **email + Telegram** (token per-sito in `site-config.json`) e fa **push nel GHL del cliente** (multi-tenant): config per slug in `site-config.json` (`locationId` + `tokenEnv`), PIT nel `.env` del builder. Tag automatici: `lead-sito-<slug>`, `form-<type>`, `consenso-marketing`; upsert su email+telefono, niente duplicati.
  ⚠️ **ATTENZIONE: il campo `tags` nell'upsert SOVRASCRIVE i tag esistenti del contatto** (contributo di Andrea Chirivì, 2026-10-12). `POST services.leadconnectorhq.com/contacts/upsert` (header `Version 2021-07-28`) con `tags` sostituisce la lista intera: un cliente fedele che compila il form perde tag di stato, coupon e benvenuto, e le automazioni che li ascoltano saltano in silenzio. **Sequenza collaudata: upsert SENZA `tags`, poi `POST /contacts/{id}/tags` (additiva), poi l'eventuale nota.** Verifica con Marco se il builder `/api/form-submit` passa i tag nell'upsert (stessa trappola riportata in `diagnosi-suite/references/trappole-strumenti.md`, sezione GoHighLevel).
- **Compleanno**: va nel campo personalizzato `compleanno_gg_mm` (giorno e mese senza anno) — è quello letto dal cron dei compleanni, non il campo standard `dateOfBirth` (il cron non lo legge). (correzione di Andrea Chirivì, 2026-10-12)
- **Ponte modulo → GHL senza Make, per siti non generati dal builder** (WordPress o pagine statiche sull'hosting del cliente): un endpoint `.php` sullo stesso dominio fa l'upsert. Il token Private Integration vive **solo sul server**, mai nel JS del browser. L'endpoint scrive una `source` dedicata, aggiunge il tag con la chiamata additiva (vedi sopra), mette il compleanno nel campo `compleanno_gg_mm`, registra il consenso marketing con la data e lascia una nota con l'esito. Lato pagina: telefono obbligatorio e normalizzato a `+39`, honeypot invisibile anti-bot, riga privacy col link alla policy, invio con `fetch keepalive` fire-and-forget così la pagina non aspetta. Collaudo end-to-end, poi si cancellano i contatti di prova (nome riconoscibile tipo "Collaudo …" o email `@rbr-test.local`; si cancellano anche eventuali registri di prova lato server). (contributo di Andrea Chirivì, 2026-10-12)
- ⚠️ **Safari su iPhone riempie i campi senza avvisare la pagina**: dopo un ricaricamento, Safari iOS rimette i valori nei campi ma non genera gli eventi che la pagina ascolta — i campi sembrano pieni ma un calcolo/pulsante che si accende in JS sugli eventi dei campi resta spento e la richiesta non parte. Riguarda ogni modulo il cui pulsante o calcolo dipende da eventi JS sui campi. Rimedio: la pagina ricontrolla i valori dei campi una volta al secondo e, se il calcolo non riesce, lo scrive a schermo invece di restare muta. Verificato su una pagina cassa interna usata da staff su iPhone; su un modulo per i clienti la regola arriva per analogia, non è ancora stata osservata direttamente. (contributo di Andrea Chirivì, 2026-10-12)
- **Resmio**: se il locale lo usa, widget iframe (`app.resmio.com/<facility_id>/widget`) nella sezione prenota, con `referrerpolicy="no-referrer-when-downgrade"` sull'iframe e le pagine marcate `?utm=` (vedi A6 Tracciamento). Nota: gli iframe esterni non vengono tradotti da GTranslate (limite noto).
- Confine di responsabilità: sito/landing/deploy/Pixel front-end = questa skill; workflow CRM, catenarie, CAPI e campagne Meta = lato RBR AI (webhook router universale Make come interfaccia).

### A6. Tracciamento
- **Meta Pixel**: snippet nel template (nei siti campagna il Pixel ID reale arriva da chi gestisce le Ads — non inventarlo).
- **GA4**: eventi che contano per un ristorante = click su `tel:`, click prenota / submit form, click indicazioni stradali, view menu. 🟡 **Da validare con Marco**: il template siti-ristoranti documenta il Pixel ma NON un setup GA4 standard — prima di installare GA4 su un sito generato concordare misurazione (GA4 vs solo Pixel) e Measurement ID. Sui siti WordPress dei locali diretti (Mister Pizza/Dirigì) il tracciamento conversioni esiste già (vedi `mister-pizza/memory/google_ads_tracciamento.md`): non aggiungere container doppi.
- ⚠️ **Verifica SEMPRE con l'ID reale dopo ogni deploy, mai col nome della funzione** (contributo di Marco (RBR AI), 2026-09-01): un grep su `fbq(` o `connect.facebook.net` dà esito positivo anche se è rimasto il placeholder letterale `fbq('init','PIXEL_ID')` — caso reale redmike.it, live 2 mesi senza un solo evento raccolto. Verifica corretta:
  - `curl -sL https://sito.it | grep -c '<pixel_id_reale>'` → deve dare **>0**; `grep -c PIXEL_ID` (il placeholder) → deve dare **0**. Stessa cosa per GA4 (`G-XXXX`) e Google Ads (`AW-XXXX`).
  - In browser: `window.fbq.getState().pixels` deve elencare l'ID giusto ed esistere il cookie `_fbp`.
  - Per iniettare pixel/eventi su siti statici senza duplicare ad ogni riesecuzione: script idempotente con marker in commento (`RBR-PIXEL` / `RBR-SCHEDULE` / `RBR-LEAD`) che cerca il marker prima di scrivere.
- ⚠️ **Prenotazioni Resmio: il blur-trick NON è una conversione** (correzione, contributo di Luciano Purpi, 2026-09-03). Ascoltare `window.blur` + `document.activeElement === iframe` conta il PRIMO CLIC dentro il widget, non la prenotazione. Caso Barresi (21/08/2026): 42 "conversioni" Google Ads in 14 giorni contro 39 prenotazioni TOTALI dal sito, tutte le fonti sommate — "Massimizza le conversioni" ottimizzava su tocchi di iframe; stessa malattia sul Pixel Meta. Dove è già installato resta **solo micro-conversione secondaria**, MAI primaria di bidding.
- ✅ **Metodo corretto: canale nel `booking_request_parameters` + conversioni offline** (contributo di Luciano Purpi, 2026-09-03):
  1. Resmio salva nel campo invisibile `booking_request_parameters` SOLO le chiavi il cui nome è esattamente `gclid` o `utm` (letto nel bundle del widget): `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` vengono **buttati**. Marca le pagine/link con un parametro che si chiama `utm` e basta: `?utm=<landing>-<canale>` (GA4 lo ignora, non sporca l'organico). Il `gclid` di Google passa da solo. ⚠️ **Correzione importante** (contributo di Andrea Chirivì, 2026-10-12, verificata sul bundle 4.24.0 del widget, funzione `getBookingRequestParams`): il widget prende `gclid`/`utm` **SOLO da `document.referrer`**, cioè dall'indirizzo della pagina che lo ospita, **e SOLO se gira dentro un iframe** (`parent !== window`). Il suo stesso indirizzo non lo guarda: scrivere `&gclid=`/`&utm=` sull'URL `app.resmio.com/<slug>/widget` (link diretto o `src` dell'iframe) **non salva niente** (caso reale: 23 prenotazioni da clic Google e 0 con `booking_request_parameters` popolato, 0 su 900 in tutto). La frase "non serve se il widget è servito dallo stesso dominio" al punto 2 vale **solo se il widget resta comunque dentro un iframe**. **Mai il click id nel parametro `comment`**: Resmio lo tratta come codice sconto (finisce in `codicesconto`/`active_coupon_code` sul contatto GHL) ed è visibile all'ospite nella mail di conferma.
  2. Il widget legge il `document.referrer`: di default il browser manda solo l'origine e taglia la query → sull'**iframe del widget** metti `referrerpolicy="no-referrer-when-downgrade"` (solo lì: il `<meta name="referrer">` di pagina regalerebbe l'URL completo anche a Pixel, Analytics e chat). Non serve se il widget è servito dallo stesso dominio del sito **e resta comunque in iframe**.
  3. Le prenotazioni col `gclid`/`utm` si caricano come **conversioni offline SOLO se onorate** (escluse cancellate e no-show, che valgono il 17-20%): segnale più pulito di qualsiasi evento front-end. Caricamento e KPI → skill `adv-ristorante` punto 4.
  4. Il parametro `source` scritto nell'embed classico (`widget.js`) NON arriva: Resmio lo riscrive con l'hostname. Passa intero solo col proxy PHP o col link diretto `app.resmio.com/<slug>/widget?source=` (dettagli → skill `campagna-locale`). ⚠️ **Il link diretto conserva il `source` ma NON porterà mai il `gclid`** (va bene per mail, WhatsApp, QR e bio): il traffico Google Ads deve atterrare su una **pagina propria con l'iframe** (ricetta al punto 5 sotto). Il GTM nativo di Resmio è solo nel piano Ultimate (non nell'add-on Marketing): non serve comprarlo per questo (`suite/memory/resmio.md`).
  5. ⚠️ **Ricetta per far entrare il gclid senza cambiare i pulsanti** (contributo di Andrea Chirivì, 2026-10-12 — confermata per il gclid già nell'indirizzo della pagina, DA VERIFICARE il caso del gclid solo in memoria/consenso cookie, Safari/iPhone e le prime prenotazioni `.google` vere). Sulla pagina propria di prenotazione con l'iframe Resmio, e solo DOPO il consenso cookie: (a) `referrerpolicy="no-referrer-when-downgrade"` sull'iframe; (b) il gclid deve stare nell'indirizzo della PAGINA quando l'iframe carica — se è solo in memoria (conservato 30 giorni col consenso) si aggiunge con `history.replaceState` e si toglie al load dell'iframe (timeout di sicurezza, es. 8s); (c) si riassegna il `src` dell'iframe per ricaricarlo, togliendo l'eventuale `gclid=` residuo e scrivendo `source=<pagina>.<canale>` così il source resta intatto; (d) `gbraid`/`wbraid` viaggiano come `utm=gbraid_<valore>`, perché Resmio tiene solo `gclid` e `utm`, e un `utm` già scritto da altri non si tocca; (e) non ricaricare se la persona ha già toccato il modulo (blur sull'iframe); (f) **trappola**: i tag di misurazione ascoltano i cambi di indirizzo e un `replaceState` può contare una page view in più — usa la funzione nativa presa da un iframe vuoto (`fr.contentWindow.History.prototype.replaceState.call(window.history, state, '', url)`); (g) dopo ogni modifica svuota la cache del sito (es. WP-Optimize). Verifica sempre via **API Resmio su una prenotazione di prova** (`booking_request_parameters` non vuoto), mai dal solo codice installato.
  6. **Widget aperto sempre su "Oggi"** (contributo di Luciano Purpi, 2026-10-12): di domenica o a tarda sera chi arriva da una campagna vede "Spiacenti, siamo chiusi". Inietta `date=YYYY-MM-DD` col prossimo giorno di apertura, calcolato nel fuso locale (Europe/Rome); `nextAvailability=true` **non funziona** (dà "Invalid date"). I link di prenotazione interni (es. dal cartellone eventi) devono conservare `date` e `people` nell'indirizzo, senza redirect che li perdono.

### A7. Pop-up di cattura (contributo di Andrea Chirivì, 2026-10-12)
**Regole**: compare dopo 12 secondi o all'uscita del mouse; non riappare per 60 giorni a chi l'ha chiuso; non compare sulla pagina di prenotazione né sulle landing; si spegne con `?nopopup=1`. Non si accende finché il modulo GHL dentro ha ancora i segnaposto e il pulsante in inglese di serie ("Enter your first name", "Submit"). Prima di accenderlo verifica che il modulo non mandi `X-Frame-Options`.

**Difetto noto di `form_embed.js`**: mette l'iframe in `position:absolute` dentro wrapper alti zero (`.ep-wrapper`, `.ep-iFrameContainer`). Il riquadro non conosce l'altezza, non scorre, e il pulsante di invio diventa irraggiungibile. Correzione: altezza esplicita e `position:relative` su `#inline-<formId>-wrapper`, `#inline-<formId>-div` e sull'iframe, più `max-height:92vh` e `overflow-y:auto` sul contenitore VERO del pop-up (su FireBox è `#dialogNNNN`, non `.fbox-content`). Verifica misurando le altezze, non guardando a occhio. Nei primi 1-2 secondi il modulo appare come un rettangolo bianco (lazy + `data-initial-iframe-hidden`): non è un guasto. Obiettivo: tutto in una schermata (osservato 470px, 500px su mobile, dopo aver tolto il regolamento dal modulo — vedi B2 punto 6).

Il salvataggio del form builder GHL si controlla dall'**esterno**, con un `curl` sull'URL pubblico del modulo. Quando si sostituisce un pop-up, cerca e togli TUTTE le regole CSS del vecchio, anche quelle solo mobile. Poi fai il giro completo da cliente su un telefono vero (modulo, email, QR, riscatto): trova difetti che il collaudo tecnico non vede.

---

## Percorso B — Landing di campagna (pagina singola per un'offerta)

La landing è **un anello della catena** della skill `campagna-locale` (code → landing → QR → coupon iPratico → email GHL): leggi quella skill per la catena completa. Qui c'è solo come si COSTRUISCE la pagina.

### B1. Scegli il contenitore (non crearne uno nuovo)
- **Locale con sito WordPress** (es. Mister Pizza, Dirigì): le landing base esistono già e si **riusano parametrizzate** via querystring `?code=<code>&source=<source>` — non duplicare la pagina (regola di `campagna-locale`). ⚠️ Se la landing contiene l'embed classico Resmio, `source` non arriva alla prenotazione (vedi A6): aggiungi `utm=<landing>-<canale>` e verifica l'URL dell'iframe generato.
- **Cliente con WordPress fatto con `sito-wordpress-ristorante`**: pagina WordPress (template pagina piena, noindex) con il modulo `[rbr_modulo tipo="novita"]` del plugin rbr-moduli → contatto nel GHL del cliente con tag `form-novita` → workflow della promo. Una pagina riusata via querystring, non una per campagna.
- **Locale con sito statico GIÀ online col vecchio metodo** (es. Red Mike — solo manutenzione, nessun sito/landing nuovo così): pagina HTML dedicata dentro la cartella del sito (`output/siti/<slug>/<promo>.html`), deployata sullo stesso host. Su Caddy Oracle: `try_files` per URL puliti (`/riapertura` → `riapertura.html`) e `systemctl restart caddy` (mai reload).
- **Sito sull'hosting del cliente (Plesk/MisterDomain/FTP, non Oracle/Caddy)** (contributo di Andrea Chirivì, 2026-10-12): prima di dire che un locale non ha sito, controlla i domini nello stesso account del registrar e leggi i DNS (caso reale: dominio e hosting pagati e vuoti, A record su Vercel senza deploy). Correzione standard: A record sull'IP dell'hosting, CNAME `www`, certificato Let's Encrypt da Plesk per dominio, `www` e webmail. I DNS li digita il titolare: Claude legge e prepara. Plesk serve gli `.html` statici con `Cache-Control max-age=31536000` (un anno): ogni pagina statica va in una cartella sua con `.htaccess` (`Header always set Cache-Control "no-cache, must-revalidate"` + `ExpiresActive Off`), oppure si mette la versione nel nome del file — chi ha già aperto la pagina vecchia deve fare un refresh a mano. Per strumenti PHP già in servizio: carica una copia di prova (`api-nuovo.php`/`index-nuovo.html`), collauda con `&prova=`, sostituisci fuori servizio dopo l'ok del titolare e cancella le copie; `curl` via FTP tronca i file oltre ~16KB, quindi serve uno script Python di caricamento; l'host FTP si indica col nome di dominio, mai con l'IP (dopo un cambio DNS risponde "530 Login incorrect"); i file interni sono sempre `.php` con guardia 403.
- **Landing su funnel GHL** (dominio `offerta.<dominio>`, vedi `onboarding-cliente-ghl` Step 7) (contributo di Andrea Chirivì, 2026-10-12, completa i punti sotto): il page builder GHL è un iframe cross-origin (`page-builder.leadconnectorhq.com`) **che non si pilota**, e l'MCP gohighlevel non ha operazioni sui funnel. Funnel, step e path si creano; il contenuto lo incolla una persona **una volta**.
  - **L'HTML del blocco custom code** carica un file JS sul server del cliente (es. `/dati/eventi.js`), e da lì arrivano contenuti, tracciamento (pixel, banner cookie) e correzioni di testo. Nell'HTML resta una copia statica di scorta. Il contenuto si consegna come un **unico HTML autoconsistente**, CSS in un `<style>` dentro un `<div>` con id proprio, senza fogli esterni: si mette negli appunti e si incolla in un elemento Custom JS/HTML del builder; dopo l'incolla si toglie il padding della Section che lo contiene, altrimenti resta una striscia bianca in cima (⚠️ la correzione esatta non è ancora verificata su un conto in produzione). I dati che cambiano (eventi, offerte) stanno in un file `.js` sul server del cliente caricato con `<script src>`: con `fetch` dal dominio della landing verso quello del cliente si incappa nel CORS, quindi all'indirizzo si aggiunge `?t=` con un valore che cambia ogni 5 minuti, così la cache non serve dati vecchi.
  - L'URL `page-builder.leadconnectorhq.com` aperto da solo resta in caricamento infinito: gli serve l'handshake `postMessage` con la pagina madre, non provare ad aprirlo a parte né a pilotarlo.
  - **Verifica SEMPRE nel browser, mai con `curl`**: un `curl` sulla landing restituisce solo la copia statica di scorta. Nota: il form builder GHL invece SI pilota (il blocco custom code/page builder no).
  - **Canva** per le immagini della landing, **mai per fare la landing come immagine esportata** (niente form, non responsive, non tracciabile): la pagina si costruisce in HTML. Nel sub-account GHL, Canva non sta in Settings → Integrations (pagina bianca) ma in **App Marketplace → Canva → External Connection**; si usa da Media Storage → menu delle sorgenti in alto a sinistra → Canva ("Edit in Canva" / "Import to media library" sul singolo file). Prima di mettere sulla landing una locandina dall'archivio Canva, **leggi la data stampata dentro l'immagine**: un archivio può avere locandine di edizioni passate con date vecchie. Le regole grafiche delle locandine (non qui): tema candidato "locandine-eventi-canva", destinazione `adv-ristorante/references/creativita-eventi-offerte.md`.

### B2. Struttura della pagina (dall'alto in basso)
1. **Headline con l'offerta** — il beneficio concreto subito: "Gift Card da 10€", "Pizza siciliana in omaggio". Niente giri di parole: tono asciutto RBR, al centro il codice e lo sconto.
2. **Posizionamento** — 1-2 righe su chi è il locale e perché (stesse regole palette/foto del template: toni caldi, foto ambiente vera).
3. **Prova sociale** — stelle + recensioni Google Places reali (se serve, filtrate client-side quando citano cose non più in menu — caso reale Red Mike/pizza).
4. **Form / CTA coupon** — nome, telefono e/o email (almeno uno), consenso marketing. Submit → plugin `rbr-moduli` o form GHL nativo sul WordPress del cliente (`/api/form-submit` solo sui vecchi siti statici già online) → contatto in GHL con tag campagna → parte la **catenaria** (email/WhatsApp col codice) lato CRM. La consegna del codice avviene DOPO il form, non in chiaro in pagina, se l'offerta va tracciata.
5. **Urgenza** — scadenza o quantità limitata SOLO se vera; ricorda che il coupon iPratico ha scadenza tecnica lunga e al pubblico non si comunicano regole di scadenza diverse dal frame di campagna.
6. **T&C in piccolo** — spesa minima, non cumulabile, una per tavolo: sempre esplicitati (caso reale Red Mike: minimo €45, no domicilio).

### B3. QR e distribuzione
- **QR verso la landing** (locandine, tavoli, vetrina): `https://quickchart.io/qr?size=800&text=<URL landing parametrizzato>` — l'URL DEVE portare `?code=&source=` così il canale resta tracciato.
- Non confonderlo col **QR da cassa** di `campagna-locale` (quello contiene il `code` in chiaro per lo staff): sono due QR con due scopi.
- Registra URL landing, code e QR nello Sheet master offerte del locale — è la sorgente di verità.
- **QR del menu al tavolo** (contributo di Andrea Chirivì, 2026-10-12, distinto dal QR della landing): menu HTML statico sull'hosting del dominio del locale. QR con correzione d'errore **H** che punta al dominio, non a una pagina specifica. Ogni piatto ha un `data-id` parlante; in fondo a `index.html` una lista JS `NASCOSTI = []` dove si aggiunge il `data-id` per oscurare un piatto finito senza ristampare — le sezioni svuotate spariscono da sole e il QR non cambia. Il vecchio URL va in redirect 301. Stampa: cartoncini A6 per i tavoli + cartello A4.

### B4. Test velocità e mobile (prima di pubblicare)
- **Lighthouse mobile** sulla landing: le foto sono la causa n.1 di lentezza — comprimi/ridimensiona, no lazy sull'hero.
- Test da smartphone vero (o browser tool): form compilabile, tastiera che non copre i campi, CTA raggiungibile senza zoom.
- **Test form end-to-end**: submit di prova → contatto appare in GHL col tag giusto (via MCP `ghl2-<cliente>`) → catenaria parte → poi CANCELLA il contatto di test.

---

## Regole RBR & trabocchetti
- ⚠️ **Siti e landing nuovi dei clienti: solo sul WordPress/hosting del cliente** (skill `sito-wordpress-ristorante`), mai sui server di Marco. Le regole hard del template (palette, foto menu, FormSubmit, lazy) valgono uguale.
- ⚠️ **Il progetto siti-ristoranti è un business SEPARATO** da RBR consulenza e non si usa per i clienti (né generatore né server).
- ⚠️ **Solo per i vecchi siti statici già online — Deploy Oracle**: Caddy con admin off → `restart`, mai `reload`; `deploy_vps.js` punta a Contabo (obsoleto per i siti migrati).
- ⚠️ **FormSubmit bandito**, palette fredda vietata, foto menu mai per indice cieco: regole hard, non preferenze.
- ⚠️ **Verifica visiva menu post-generazione obbligatoria** — mai dichiarare finito senza.
- ⚠️ **Landing WordPress = riuso parametrizzato**, mai pagina duplicata per ogni campagna.
- ⚠️ **Mai token/PIT in chiaro** nel repo condiviso: `.env` + MCP `ghl2-<cliente>` per ogni operazione GHL.
- ⚠️ **Prima di spendere** (API Gemini/Places, hosting, domini): avvisare Marco con stima costi e attendere ok.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done (checklist di pubblicazione)
- [ ] Sito/landing **live in HTTPS** e raggiungibile (200) all'URL definitivo — non solo in locale
- [ ] **Mobile ok**: Lighthouse mobile decente (foto ottimizzate, no lazy sull'above-the-fold), form usabile da smartphone, hamburger/nav funzionanti
- [ ] **Schema.org `Restaurant` valido** (test con validator.schema.org) con NAP reale — solo percorso A
- [ ] **Form testato end-to-end**: submit di prova → email/Telegram ricevuti → contatto in GHL col tag giusto → catenaria partita → contatto di test cancellato
- [ ] **Link prenotazione funzionante**: form nativo o widget Resmio caricato e prenotabile; `tel:` cliccabile
- [ ] **Tracciamento attivo**: Pixel con ID reale (no placeholder); eventi GA4 concordati e verificati in DebugView (🟡 se GA4 non concordato con Marco, segnalarlo esplicitamente, non installare alla cieca); widget Resmio con `referrerpolicy` sull'iframe e `?utm=`/`gclid` verificati **via API Resmio su una prenotazione di prova** (`booking_request_parameters` non vuoto) — **mai dal solo codice installato**, perché il widget legge solo `document.referrer` dentro un iframe; nessun blur-trick come conversione primaria
- [ ] **Palette** letta da sito/logo e contrasto ≥ 4,5:1 verificato su ogni coppia testo/sfondo
- [ ] **Verifica visiva** fatta: foto-categoria menu coerenti, palette calda, hero degno (percorso A); recensioni pertinenti e T&C presenti (percorso B)
- [ ] Landing di campagna: URL parametrizzato `?code=&source=`, QR generato, tutto registrato nello Sheet master (il resto della catena → skill `campagna-locale`)
- [ ] **Checklist Mossa 10**: title con promessa + description vera, prima schermata promessa+prove, pulsante Prenota fisso in alto, menu in testo (non solo PDF/immagine), soglia 2% di conversione sul pop-up (vedi A3/A7)
- [ ] **Pop-up di cattura** (se presente): tutto in una schermata su desktop e mobile, nessuna regola CSS del pop-up vecchio rimasta, salvataggio del modulo GHL verificato con `curl` esterno (vedi A7)
- [ ] **Modulo testato anche da iPhone con Safari**: compilato, pagina ricaricata a campi pieni, pulsante/calcolo si accende davvero e la richiesta arriva nei log del server (vedi A5)
- [ ] **GHL: upsert del contatto verificato senza `tags`**, tag aggiunti con chiamata additiva separata (vedi A5)
