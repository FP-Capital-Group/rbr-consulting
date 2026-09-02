---
name: sito-landing-ristorante
description: >-
  Metodo RBR per costruire il sito completo di un ristorante o la landing page di
  una promo. Usala quando devi mettere online la presenza web di un locale —
  "fai il sito al ristorante", "rifacciamo il sito", "serve una landing page",
  "pagina per la promo", "il cliente non ha un sito decente". Due percorsi:
  (A) sito completo col metodo siti-ristoranti di Marco (generatore AI Node.js,
  template mobile-first, form → email+GHL, deploy VPS); (B) landing singola di
  campagna collegata a campagna-locale (offerta → form GHL → QR). NON inventare
  stack alternativi (WordPress nuovo, Wix, site builder a caso): il metodo e il
  template esistono già — segui questa skill.
---

# Sito + landing page ristorante (percorso A: sito completo · percorso B: landing di campagna)

## Perché esiste
Un ristoratore non ha bisogno di "un sito": ha bisogno di una pagina che su mobile carichi subito, mostri il menu con foto giuste, faccia prenotare in 2 tap e mandi il lead nel CRM. RBR ha già un metodo collaudato (progetto **siti-ristoranti** di Marco, `~/Desktop/AI/siti-ristoranti/`): generatore AI + template con regole hard nate da errori reali + deploy standard. Questa skill codifica quel metodo e il suo gemello leggero, la **landing di campagna**. Se improvvisi uno stack diverso, perdi le regole hard e il tracciamento.

## Quando usarla
- Un cliente (o un locale diretto) ha bisogno di un sito nuovo o di rifare quello vecchio → **Percorso A**.
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

## Percorso A — Sito completo del ristorante

Il metodo è quello del progetto **siti-ristoranti** (`ristoranteonline.ai`): sito statico generato via AI, non un CMS.

### A1. Stack reale (non cambiarlo)
- **Node.js (ESM)** — script del generatore. Niente Python (legacy archiviato), niente WordPress per i siti nuovi.
- **Generazione AI**: `step2_generazione/generatore.js` — Gemini (vision per classificare foto e menu) con fallback Groq (`lib/llm.js`). Legge i dati del lead da GHL.
- **Acquisizione dati**: `step1_scraping/scraper.js` — lookup Google Places (placeId, stelle, recensioni, foto, indirizzo) → push lead su GHL.
- **Output**: sito statico in `output/siti/<slug>/` (HTML+CSS+JS vanilla, foto ottimizzate).
- **Deploy**: `step3_deploy/deploy_vps.js --slug <slug>` → live su `https://<slug>.ristoranteonline.ai` (HTTPS Let's Encrypt). ⚠️ I siti già migrati stanno su **Oracle** (130.110.2.70, web server **Caddy**, builder systemd su :3100): per quelli il deploy è rsync su `/var/www/sites/<slug>/` + eventuale blocco Caddyfile — e Caddy Oracle ha admin API off → **sempre `systemctl restart caddy`, mai `reload`**. `deploy_vps.js` punta al vecchio Contabo, obsoleto per i siti migrati. 🟡 **Da validare con Marco**: percorso di deploy standard per un sito NUOVO oggi (il business ristoranteonline.ai è in pausa dal 2026-06-23; per un cliente consulenza va deciso host e dominio caso per caso).

### A2. Avvio progetto nuovo (workflow "crea il sito per X")
1. **Lookup Google Places** → placeId, stelle, recensioni, indirizzo, foto.
2. **Push lead su GHL** (idempotente: se esiste, riusa l'id).
3. **Genera**: `node step2_generazione/generatore.js --contact-id <id> --city <città>`.
4. **Deploy** (mai fermarsi al locale, salvo richiesta esplicita "solo preview").
5. **Verifica visiva post-generazione** (obbligatoria, Marco l'ha chiesta esplicitamente): screenshot + lettura di OGNI foto categoria menu — la foto sotto "Primi" deve essere un primo. Mai saltarla.

Se il ristorante non ha sito/foto buone: foto Instagram scaricate con `gallery-dl` al posto delle `gp_*.jpg`, poi rigenera con `--force`. Personalizzazioni per singolo sito (palette, font, hero) → `brand-override.json` nella cartella del sito, mai a mano nel template.

### A3. Struttura pagine tipo
- **Home** — hero con foto ambiente calda + posizionamento (attenzione: "trattoria" NON implica cucina romana — il claim segue la regione/cucina reale), card piatti cliccabili verso il menu, sezione **prenota** (form o widget Resmio) su sfondo beige liscio (mai foto di sfondo sul form), contatti/orari nel footer.
- **Menu** — categorie con foto matchate semanticamente ai piatti (mai per indice cieco; nessun match → nessuna foto).
- **Storia/Chi siamo** — la narrazione del locale, foto ambiente.
- **Contatti** — NAP completo, mappa, orari, telefono cliccabile (`tel:`).
- Opzionale: **Galleria** con lightbox (pattern esistente su Trattoria Griss).

### A4. Regole HARD del template (nate da errori reali — non ridiscuterle)
- ❌ Mai widget di auto-traduzione dentro il template (per i turisti → GTranslate come da skill `seo-local-ristorante`).
- ❌ Mai **FormSubmit** (formsubmit.co): bandito da Marco.
- ❌ Mai palette fredda (rosa pallido, blu, azzurro, viola, grigio): **sempre toni caldi** — rosso, arancione, ocra, terracotta, oro, bordeaux; beige = crema/sabbia.
- ❌ Mai `loading="lazy"` sulle foto above-the-fold (card piatti, foto categorie).
- ✅ Mobile-first sul serio: input form min-height 48px, hamburger menu funzionante, hero leggibile su schermo piccolo.
- ✅ Se le foto Google Places sono mediocri (mani, close-up, sfocate) → hero con foto stock via `brand-override.json`.
- ✅ **Schema.org `Restaurant`** JSON-LD in ogni sito: NAP reale, geo, orari, telefono, `aggregateRating` da Places (i dettagli SEO delle pagine local → skill `seo-local-ristorante`, non duplicare qui).

### A5. Form, prenotazioni e CRM
- **Form nativo** → `POST /api/form-submit` del builder (payload `{slug, type, data}`), con fallback WhatsApp se la fetch fallisce. Il builder notifica via **email + Telegram** (token per-sito in `site-config.json`) e fa **push nel GHL del cliente** (multi-tenant): config per slug in `site-config.json` (`locationId` + `tokenEnv`), PIT nel `.env` del builder. Tag automatici: `lead-sito-<slug>`, `form-<type>`, `consenso-marketing`; upsert su email+telefono, niente duplicati.
- **Resmio**: se il locale lo usa, widget iframe (`app.resmio.com/<facility_id>/widget`) nella sezione prenota. Nota: gli iframe esterni non vengono tradotti da GTranslate (limite noto).
- Confine di responsabilità: sito/landing/deploy/Pixel front-end = questa skill; workflow CRM, catenarie, CAPI e campagne Meta = lato RBR AI (webhook router universale Make come interfaccia).

### A6. Tracciamento
- **Meta Pixel**: snippet nel template (nei siti campagna il Pixel ID reale arriva da chi gestisce le Ads — non inventarlo).
- **GA4**: eventi che contano per un ristorante = click su `tel:`, click prenota / submit form, click indicazioni stradali, view menu. 🟡 **Da validare con Marco**: il template siti-ristoranti documenta il Pixel ma NON un setup GA4 standard — prima di installare GA4 su un sito generato concordare misurazione (GA4 vs solo Pixel) e Measurement ID. Sui siti WordPress dei locali diretti (Mister Pizza/Dirigì) il tracciamento conversioni esiste già (vedi `mister-pizza/memory/google_ads_tracciamento.md`): non aggiungere container doppi.

---

## Percorso B — Landing di campagna (pagina singola per un'offerta)

La landing è **un anello della catena** della skill `campagna-locale` (code → landing → QR → coupon iPratico → email GHL): leggi quella skill per la catena completa. Qui c'è solo come si COSTRUISCE la pagina.

### B1. Scegli il contenitore (non crearne uno nuovo)
- **Locale con sito WordPress** (es. Mister Pizza, Dirigì): le landing base esistono già e si **riusano parametrizzate** via querystring `?code=<code>&source=<source>` — non duplicare la pagina (regola di `campagna-locale`).
- **Locale con sito generato/statico** (es. Red Mike): pagina HTML dedicata dentro la cartella del sito (`output/siti/<slug>/<promo>.html`), deployata sullo stesso host. Su Caddy Oracle: `try_files` per URL puliti (`/riapertura` → `riapertura.html`) e `systemctl restart caddy` (mai reload).

### B2. Struttura della pagina (dall'alto in basso)
1. **Headline con l'offerta** — il beneficio concreto subito: "Gift Card da 10€", "Pizza siciliana in omaggio". Niente giri di parole: tono asciutto RBR, al centro il codice e lo sconto.
2. **Posizionamento** — 1-2 righe su chi è il locale e perché (stesse regole palette/foto del template: toni caldi, foto ambiente vera).
3. **Prova sociale** — stelle + recensioni Google Places reali (se serve, filtrate client-side quando citano cose non più in menu — caso reale Red Mike/pizza).
4. **Form / CTA coupon** — nome, telefono e/o email (almeno uno), consenso marketing. Submit → `/api/form-submit` (siti statici) o form GHL nativo (WordPress) → contatto in GHL con tag campagna → parte la **catenaria** (email/WhatsApp col codice) lato CRM. La consegna del codice avviene DOPO il form, non in chiaro in pagina, se l'offerta va tracciata.
5. **Urgenza** — scadenza o quantità limitata SOLO se vera; ricorda che il coupon iPratico ha scadenza tecnica lunga e al pubblico non si comunicano regole di scadenza diverse dal frame di campagna.
6. **T&C in piccolo** — spesa minima, non cumulabile, una per tavolo: sempre esplicitati (caso reale Red Mike: minimo €45, no domicilio).

### B3. QR e distribuzione
- **QR verso la landing** (locandine, tavoli, vetrina): `https://quickchart.io/qr?size=800&text=<URL landing parametrizzato>` — l'URL DEVE portare `?code=&source=` così il canale resta tracciato.
- Non confonderlo col **QR da cassa** di `campagna-locale` (quello contiene il `code` in chiaro per lo staff): sono due QR con due scopi.
- Registra URL landing, code e QR nello Sheet master offerte del locale — è la sorgente di verità.

### B4. Test velocità e mobile (prima di pubblicare)
- **Lighthouse mobile** sulla landing: le foto sono la causa n.1 di lentezza — comprimi/ridimensiona, no lazy sull'hero.
- Test da smartphone vero (o browser tool): form compilabile, tastiera che non copre i campi, CTA raggiungibile senza zoom.
- **Test form end-to-end**: submit di prova → contatto appare in GHL col tag giusto (via MCP `ghl2-<cliente>`) → catenaria parte → poi CANCELLA il contatto di test.

---

## Regole RBR & trabocchetti
- ⚠️ **Non inventare stack**: il metodo siti-ristoranti esiste — generatore + template + regole hard. Un sito "fatto a mano diverso" perde tutti i fix accumulati.
- ⚠️ **Il progetto siti-ristoranti è un business SEPARATO** da RBR consulenza: usane il metodo e il template, ma per un cliente consulenza dominio/hosting/pricing si decidono con Marco (🟡 l'offerta storica era €1000 una tantum su `ristoranteonline.ai` — da validare per il contesto consulenza).
- ⚠️ **Deploy Oracle**: Caddy con admin off → `restart`, mai `reload`; `deploy_vps.js` punta a Contabo (obsoleto per i siti migrati).
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
- [ ] **Tracciamento attivo**: Pixel con ID reale (no placeholder); eventi GA4 concordati e verificati in DebugView (🟡 se GA4 non concordato con Marco, segnalarlo esplicitamente, non installare alla cieca)
- [ ] **Verifica visiva** fatta: foto-categoria menu coerenti, palette calda, hero degno (percorso A); recensioni pertinenti e T&C presenti (percorso B)
- [ ] Landing di campagna: URL parametrizzato `?code=&source=`, QR generato, tutto registrato nello Sheet master (il resto della catena → skill `campagna-locale`)
