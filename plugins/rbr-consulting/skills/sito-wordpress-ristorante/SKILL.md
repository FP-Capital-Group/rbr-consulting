---
name: sito-wordpress-ristorante
description: Costruisce DA ZERO il sito di un ristorante cliente su WordPress, sull'hosting e sul dominio comprati e intestati al CLIENTE — tutto il metodo RBR (modello Cartabianca): grafica e impaginazione pagina per pagina, prenotatore sempre in evidenza (TheFork senza commissione, Resmio o richiesta), CRM GoHighLevel del cliente (campi, tag, flussi con prompt pronti, plugin rbr-moduli incluso), normative (footer obbligatorio, privacy GDPR, cookie Garante, allergeni, recensioni, accessibilità), tema a blocchi solo core, IT/EN con TranslatePress, SEO local e JSON-LD, «sito in costruzione» con link di anteprima, collaudo e consegna. Usala quando il consulente dice "fai il sito a X", "rifacciamo il sito del ristorante", "sito nuovo su WordPress", "il cliente ha comprato dominio e hosting", "mettiamo online il sito su Aruba", "sito come quello di Cartabianca". MAI su server, domini, account o builder di Marco/RBR. Per un WordPress già esistente fatto da un'agenzia usa sito-wordpress-cliente-mcp; per SEO di un sito esistente seo-local-ristorante.
---

# Sito WordPress del ristorante — sull'hosting del cliente

> Modello di riferimento: **Cartabianca Ristoranti** (cartabiancaristoranti.it, Aruba, ott 2026) —
> tema a blocchi con solo blocchi core, prenotatore TheFork a schede, moduli → CRM, IT/EN, in costruzione
> con anteprima. Lezioni da Red Mike, Raíces, Osteria Ca' di Pieri, Trattoria Griss, Zio Bibi, Mister Pizza.

## La regola che viene prima di tutto
**Niente di RBR o di Marco dentro il sito.** Il cliente compra e intesta a sé dominio + hosting WordPress;
tutto vive lì. Vietati:
- server/VPS di Marco (Oracle, ex Contabo), sottodomini `*.ristoranteonline.ai`, il builder `/api/form-submit`,
  il generatore `siti-ristoranti`, Caddy, Telegram bot di Marco;
- email di Marco/RBR come destinatari dei moduli o in copia fissa nel codice;
- account Google/Meta/TheFork/GHL di RBR al posto di quelli del cliente (RBR entra come **utente/partner**
  negli account del cliente, mai il contrario);
- plugin o temi a pagamento intestati a RBR.

Perché: il sito è del cliente. Se domani il rapporto finisce, il sito continua a funzionare e nessuno deve
migrare niente. E un VPS da 1 GB condiviso fra tutti i clienti è già andato giù per 35 minuti (07/10/2026).
Se ti accorgi che serve qualcosa "che solo un server può fare" → c'è quasi sempre il modo nel WordPress
del cliente o nel suo GHL (workflow, notifiche interne). Chiedi a Marco prima di inventare infrastruttura.

## Mappa della skill (leggi il file giusto prima di ogni fase)
| File | Cosa contiene |
|---|---|
| `references/grafica-e-layout.md` | come deve essere fatto: colori, font, bottoni, foto, header/footer, ogni pagina sezione per sezione, cose vietate |
| `references/prenotatore.md` | il prenotatore sempre in evidenza: dove va (7 punti), TheFork/Resmio/richiesta, testi, tracciamento, collaudo |
| `references/crm-e-moduli.md` | sub-account GHL, campi standard, plugin moduli, tag, flussi con i prompt pronti, chat, collaudo CRM |
| `references/normative.md` | footer obbligatorio, privacy GDPR, cookie (Garante 2021), allergeni, recensioni, vendita online, accessibilità, fidelity/concorsi |
| `references/tema-a-blocchi.md` | il tema WordPress: file, theme.json, codice per in costruzione, carosello, pop-up, menu, lingue, plugin Avvio |
| `references/hosting-dominio.md` | cosa compra il cliente, Aruba e trappole, DNS, SMTP, plugin ammessi, manutenzione |
| `references/lezioni-siti-rbr.md` | tutte le regole nate dagli errori sui siti fatti finora |
| `assets/rbr-moduli.zip` | plugin moduli → GHL del cliente, pronto da caricare (sorgente in `assets/rbr-moduli/`) |
| `assets/blueprint.json` | WordPress Playground per lo sviluppo in locale |

## Quando usarla
- Sito nuovo o rifatto per un cliente RBR → sì.
- Il cliente ha già un WordPress fatto da un'agenzia e va solo "fatto prenotare" → `sito-wordpress-cliente-mcp`.
- Landing di una singola promo su un sito che c'è già → `sito-landing-ristorante` (percorso B) + `campagna-locale`.
- SEO di un sito esistente → `seo-local-ristorante`. Scheda Google → `google-business-ristorante`.

## Prerequisiti (chiedili tutti insieme, in un solo messaggio numerato)
1. **Dominio + hosting WordPress comprati dal cliente, intestati alla sua società** (vedi
   `references/hosting-dominio.md`: cosa comprare, quanto costa, cosa NON comprare). Accesso: il cliente ti
   crea un utente **amministratore** WordPress col tuo nome (o ti passa il pannello hosting per installarlo).
   Mai farsi dare la sua password personale: utente tuo, revocabile.
2. **Casella email del dominio** (es. `info@dominio.it`) per mandare le mail del sito via SMTP.
3. **Prenotazioni**: TheFork (UUID del widget senza commissione, uno per locale) o Resmio (facility id) o
   modulo a richiesta.
4. **Sub-account GHL del cliente** + un Private Integration Token creato DENTRO quel sub-account
   (scope `contacts.write`, `contacts.readonly`). Se il sub-account non c'è → `onboarding-cliente-ghl` prima.
5. **Contenuti veri**: logo (vettoriale o PNG grande), foto originali ≥1600 px, menu con prezzi confermati,
   orari per locale, telefoni, indirizzi, social, ragione sociale + P.IVA (footer), cosa deve fare il visitatore
   (prenotare? ordinare? chiamare?).
6. **Account di tracciamento DEL CLIENTE** se si fanno ads: Pixel Meta, Google Ads/GA4 (ID reali).

Manca qualcosa → si parte lo stesso con i blocchi beige al posto delle foto e i testi marcati DA CONFERMARE,
in costruzione. Mai inventare foto, recensioni, premi, prezzi o orari.

## Procedura

### 1. Raccolta e strategia (prima di toccare WordPress)
- Leggi `strategia-marketing-rbr` (tono, posizionamento) e, se non c'è, fai la `market-discovery-ristorante`.
- **Colori e font si leggono dal brand** (logo, insegna, sito vecchio, menu stampato) e si verificano col
  contrasto ≥ 4,5:1 → metodo in `sito-landing-ristorante/references/colori-brand.md`. Senza identità chiara:
  toni caldi (mai blu/rosa/grigio freddo), beige crema `#F5EFE0`.
- Mappa pagine e un solo obiettivo per pagina. Struttura standard (sezione per sezione in
  `references/grafica-e-layout.md` §7):
  - **Home**: hero/carosello con foto vera del locale → **prenota subito dopo l'hero** (widget a schede se
    più locali) → perché sceglierci (3 punti concreti) → menu in evidenza → locali → eventi/feste → dove siamo.
  - **Pagina per locale** `/locali/<nome>/` (H1 «Ristorante X a Città», orari, mappa, foto, prenota, FAQ).
  - **Menu** (HTML vero, non PDF; prezzi piccoli, senza «€» e «,00», ordine del menu stampato).
  - **Prenota** `/prenota/` (un widget per locale, ancore `#locale`).
  - **Eventi e feste** (modulo `evento`), **Contatti**, **Privacy** + **Cookie**.
  - Facoltative: fidelity/club (premi = regali, mai sconti), pagina del piatto firma per la SEO, blog.
- Una sola nav, uguale su tutte le pagine, con al massimo 2 bottoni (es. «Prenota» pieno + «Chiama»/«Ordina»).
- **Il prenotatore si progetta per primo**: deve essere raggiungibile da header, home subito dopo la copertina, barra
  fissa mobile, ogni pagina locale, fine di menu/eventi, pagina `/prenota/` → `references/prenotatore.md`.
- **Normative da preparare subito** (servono dati dal cliente): ragione sociale, sede, P.IVA, REA e capitale per il
  footer; fornitori reali per l'informativa; allergeni del menu → `references/normative.md`.
- **CRM pronto prima del sito**: sub-account, campi standard, token del sito, flussi S1-S4 in bozza →
  `references/crm-e-moduli.md`.

### 2. Sviluppo: in locale o direttamente sull'hosting in costruzione
Niente server intermedi. Due modi:
- **Con Node sul computer (Mac)**: WordPress Playground in locale, blueprint pronto in `assets/blueprint.json`
  (metti il nome della cartella del tema):
  ```bash
  npx @wp-playground/cli@latest server --port=9450 \
    --mount=./tema-<cliente>:/wordpress/wp-content/themes/<cliente> \
    --mount=<skill>/assets/rbr-moduli:/wordpress/wp-content/plugins/rbr-moduli \
    --blueprint=<skill>/assets/blueprint.json
  ```
- **Senza Terminale (Cowork/Windows)**: si lavora direttamente sul WordPress del cliente con «in costruzione»
  attivo (il pubblico vede solo «arriva presto»), caricando zip di tema e plugin da wp-admin.
- **Tema**: tema a blocchi (FSE) con SOLO blocchi core, stili tutti in `theme.json` → il cliente cambia
  testi, foto, colori e menu da *Aspetto → Editor* senza codice. Architettura, file e snippet pronti in
  `references/tema-a-blocchi.md` (carosello, pop-up, «in costruzione» + anteprima, menu collegati, pillole
  lingua, prenotatore a schede).
- **Moduli**: plugin incluso `assets/rbr-moduli/` (testato) → blocco Shortcode `[rbr_modulo tipo="prenotazione"]`
  (tipi: `prenotazione`, `evento`, `contatto`, `novita`). Scrive DIRETTAMENTE nel GHL del cliente:
  upsert contatto (niente doppioni) → tag `lead-sito-<dominio>`, `form-<tipo>`, `pv-<locale>`, `consenso-marketing`,
  `lingua-en` → nota con il riepilogo. Mail al ristorante a ogni invio; se il CRM non risponde, copia in
  *Moduli → Invii*. Campi personalizzati del modello base GHL (`pv`, `giorno_prenotazione`, `orario_prenotazione`,
  `numerodipersone`, `compleanno_gg_mm`, `lingua`). Antibot: gettone firmato, ora firmata, campo trappola, max 5
  invii/10 min per IP. Dettagli, flussi e prompt GHL in `references/crm-e-moduli.md`.
- **Prenotazioni**: iframe del widget TheFork senza commissione (`widget.thefork.com/<uuid>`, `/en/<uuid>`
  in inglese) in un blocco HTML marcato «non modificare»; Resmio con `referrerpolicy` e `?utm=` (vedi
  `sito-landing-ristorante` A5-A6). Sotto il widget sempre il piano B: «Chiama» + modulo `contatto`.
- **Lingue**: TranslatePress gratuito, `/en/`, traduzioni SCRITTE (mai traduzione automatica, mai widget
  Google Translate, mai emoji bandiera). Testi EN del menu copiati da quelli del cliente se esistono.
- Se ti serve generare molte pagine uguali (es. 10 locali), scrivi un plugin «Avvio» idempotente
  (`references/tema-a-blocchi.md` §Avvio) invece di copiare a mano.

### 3. Messa online sull'hosting del cliente
Ordine: installa WordPress (dal pannello hosting) → utente admin tuo → **subito «in costruzione» + Scoraggia
i motori di ricerca** → carica tema (zip) → plugin `rbr-moduli` (zip) → TranslatePress → foto → pagine
(plugin Avvio o import) → menu → impostazioni (permalink `/%postname%/`, fuso Europe/Rome, lingua it_IT,
commenti chiusi, contenuti demo cancellati) → SMTP → costanti in `wp-config.php`.
Trappole per hosting (Aruba in testa) in `references/hosting-dominio.md`.

`wp-config.php` (dal file manager dell'hosting, mai nel database né in chat):
```php
define( 'RBR_GHL_TOKEN', 'pit-…' );     // PIT del sub-account DEL CLIENTE
define( 'RBR_GHL_LOCATION', '…' );      // location id del cliente
```

### 4. SEO e dati strutturati
- Title ≤ 60 caratteri con categoria + città («Ristorante messicano a Firenze | Raíces»), una sola H1 per
  pagina = prodotto + città, mai lo slogan. Meta description, alt delle foto, sitemap (core WP o un plugin SEO).
- JSON-LD `Organization` + un `Restaurant` (o `Bakery`, `CafeOrCoffeeShop`…) per locale con NAP reale, orari,
  `servesCuisine`, `hasMenu`, `acceptsReservations` = URL del widget. Nel tema (functions.php) o nel footer.
- Dopo il go-live: link sito + menu + prenotazione (widget TheFork) nella scheda Google → `google-business-ristorante`.
  Vecchio sito/sottodominio → redirect 301 sulle nuove pagine.

### 5. Tracciamento e cookie
- Banner cookie a norma Garante (Accetta/Rifiuta uguali, X = rifiuto; plugin gratuito tipo Complianz/CookieYes
  free o quello dell'hosting): Pixel, Google Ads, GA4, mappe incorporate partono SOLO dopo il consenso; Consent Mode
  v2 se c'è Google. Privacy e cookie policy coi fornitori reali → checklist in `references/normative.md` §9.
- Pixel/tag con gli **ID del cliente**; verifica col numero reale (`curl -sL dominio | grep -c <ID>` > 0 e
  `grep -c PIXEL_ID` = 0) e a runtime dopo «Accetta» (`fbq.getState().pixels`, cookie `_fbp`). Il plugin
  moduli manda già `Schedule`/`Lead` a Pixel e `rbr_modulo_inviato` al dataLayer.
- Il clic nel widget NON è una prenotazione: conversioni primarie e offline → `google-ads-conversione-controllo`,
  `sistema-tracciamento-locale`.

### 6. Collaudo (prima di dire «pronto»)
Vedi la Definition of Done qui sotto. Strumenti: browser integrato o Playwright a 360/390/768/1280 px su ogni
pagina, IT ed EN. **Non far aprire i widget TheFork ai test automatici** (antibot DataDome: poi il widget chiede
«non sei un robot» ai clienti veri): controllali a mano, una volta.

### 7. Go-live e consegna
- Togli «in costruzione» e «Scoraggia i motori di ricerca» SOLO con l'ok di Marco/consulente responsabile.
- Svuota la cache dell'hosting, ricontrolla da finestra anonima.
- Consegna al cliente: link sito, utente WordPress (credenziali solo nel canale sicuro del team, mai in chat
  o nei file), 5 righe «come cambio una foto / un orario / il menu / il pop-up», cosa resta da lui (foto,
  conferme). Lezioni riusabili → `contribuisci-conoscenza`.

## Regole RBR & trabocchetti (sintesi — l'elenco completo con i casi in `references/lezioni-siti-rbr.md`)
- ❌ Mai recensioni inventate né «Recensione Google» finte (AGCM/Omnibus): solo stelle e numero reali con link alla scheda.
- ❌ Mai foto di repertorio spacciate per piatti del locale; senza foto vera → blocco beige col nome. Foto
  categoria menu coerente con la categoria, o nessuna foto.
- ❌ Mai Maps/Places API chiamate dal browser (costano a ogni visita): mappa con iframe embed gratuito.
- ❌ Mai FormSubmit o servizi form esterni: i moduli scrivono nel GHL del cliente.
- ❌ WhatsApp sul sito solo se il locale lo presidia davvero.
- ❌ Mai il disclaimer «sito dimostrativo» su un sito cliente; mai claim non confermati («forno a legna», «fatto da noi»).
- ✅ Numeri pubblici (prezzi, orari, volumi, premi, date stagionali) → conferma scritta del cliente.
- ✅ Valori delle tendine identici a quelli dei campi GHL (lettere accentate comprese).
- ✅ Ai giri di correzione cambia solo quello che è stato chiesto.
- ✅ Prima di qualsiasi spesa (plugin premium, API, crediti, dominio extra) → stima € e ok.

## Definition of Done
- [ ] Dominio + hosting + WordPress **intestati al cliente**; nessun riferimento a server, domini, email o
      account RBR/Marco nel sito (`grep` su tema e plugin: `ristoranteonline`, `marco`, IP)
- [ ] HTTPS sul dominio definitivo, `www` e senza `www` → stessa versione, permalink puliti
- [ ] Mobile 360/390 senza scroll orizzontale, nav/hamburger ok, campi ≥ 48 px, zero errori in console
- [ ] Contrasto ≥ 4,5:1 su ogni coppia testo/sfondo; palette dal brand; grafica conforme a `grafica-e-layout.md` §9
- [ ] Checklist normativa `normative.md` §9 tutta spuntata (footer obbligatorio, privacy, cookie, allergeni)
- [ ] Prenotatore nei 7 punti di `prenotatore.md`, ≤ 1 clic da ogni pagina, mai coperto da pop-up/chat; widget ok
      anche con cookie RIFIUTATI; piano B «Chiama» + richiamami; link preferito nella scheda Google
- [ ] Collaudo CRM di `crm-e-moduli.md` §6 per ogni tipo di modulo: contatto unico con campi, tag e nota, mail
      arrivata, flusso S partito con avviso di tipo Email → contatti di prova cancellati (`@rbr-test.local`)
- [ ] IT/EN completi (menu, moduli, banner cookie, alt), nessuna stringa italiana su `/en/`
- [ ] Title/description/H1/alt, JSON-LD validato (validator.schema.org), sitemap
- [ ] Pixel/tag con ID reale verificati dopo il consenso; privacy e cookie policy aggiornate
- [ ] Velocità: cache dell'hosting attiva, foto webp ≤ 1600 px, niente `loading=lazy` sopra la piega
- [ ] Cliente sa modificare testi/foto/orari dall'editor; credenziali consegnate nel canale sicuro
- [ ] «In costruzione» e noindex tolti solo dopo l'ok; memoria cliente aggiornata (URL, versioni, pendenze)
