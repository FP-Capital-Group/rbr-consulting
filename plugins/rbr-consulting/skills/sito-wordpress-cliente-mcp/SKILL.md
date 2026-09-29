---
name: sito-wordpress-cliente-mcp
description: Lavora sul sito WordPress GIÀ ESISTENTE di un ristorante cliente collegandolo a Claude come connettore MCP (niente Chrome, niente password applicative) — sezione Prenota con widget TheFork senza commissioni, tasti Ordina asporto/domicilio, pagine SEO per sede e per il piatto firma, traduzioni EN/ES, dati strutturati JSON-LD Restaurant, pulizia di link e fornitori vecchi. Include il trucco per inserire script (JSON-LD, tag Google Ads) quando il connettore li rifiuta. Usala quando il consulente dice "sistema il sito di X", "metti il tasto prenota sul sito", "aggiungi il widget TheFork", "fai le pagine SEO dei locali", "il sito non ha lo schema Restaurant", "collega il sito a Claude", "togli Quandoo dal sito". Per un sito o una landing DA ZERO usa sito-landing-ristorante.
---

# Sito WordPress del cliente via MCP

> Metodo nato su Raíces (Firenze, 24/09/2026): in un giorno home rifatta, pagina /prenota/,
> 3 pagine SEO in 3 lingue, JSON-LD e tag Google Ads online, tutto senza toccare il tema a mano.

## Perché esiste
Molti clienti hanno già un sito fatto da un'agenzia: non va rifatto, va fatto **prenotare**.
Lavorarci dal browser è lento e fragile (login nascosti, reCAPTCHA, editor a blocchi). Se il sito
espone un server MCP (plugin tipo «Conector de IA» / MCP Adapter), Claude lo usa come un'API:
legge i blocchi, modifica, traduce e verifica.

## Prerequisiti
1. **Connettore**: claude.ai → Impostazioni → Connettori → personalizzato → `https://<dominio>/mcp`,
   OAuth fatto dal consulente con un utente **administrator** del sito.
2. Chiedi chi altro lavora sul sito (sviluppatore dell'agenzia): modifiche grosse al tema vanno coordinate.
3. Link prenotazione e delivery del cliente per ogni locale (TheFork, Deliveroo, Glovo, telefono).

## Procedura
1. **Leggi prima di scrivere**: design system del tema, pagine esistenti, template di header/footer,
   pattern già pronti (galleria, fisarmonica, card) — usare quelli invece di scrivere HTML nuovo.
2. **Prenotazione senza commissioni**: in TheFork Manager → Marketing → Widget → «Incorporalo nel sito»
   si prende l'URL `widget.thefork.com/<uuid>` di ogni locale. Le prenotazioni dal widget non pagano
   commissione (quelle da thefork.it sì). Pagina `/prenota/` con un widget per locale (ancore `#locale`)
   + sezione `#prenota` in home subito dopo l'hero, con tab CSS-only fra i locali.
3. **Ordina**: due tasti semplici — «Ordina da asporto» (scegli locale → telefono) e «Ordina a domicilio»
   (scegli locale → Deliveroo/Glovo). Con `<details name="gruppo">` se ne apre uno solo alla volta.
   Header: «Ordina» (outline) + «Prenota» (pieno). Via carrello/account/preferiti se il sito non vende online.
4. **Pagine SEO**: una per sede (`/locali/<via>/`: H1, info, mappa, foto, FAQ, link incrociati) + una per
   il piatto firma (`/tacos-de-birria-firenze/`), tutte tradotte EN/ES. Title della home con la
   categoria + il piatto («Ristorante messicano a Firenze: tacos de birria»). Link interni dalla home.
5. **SEO tecnica**: title/description mancanti, alt delle immagini in uso, sitemap, http→https.
6. **JSON-LD**: Organization + un `Restaurant` per sede (address, orari, servesCuisine, hasMenu,
   acceptsReservations = URL del widget), nel footer.
7. **Pulizia**: fornitori dismessi (es. Quandoo) da banner cookie, Cookie Policy, Termini, footer.
8. **Verifica**: crawl di tutti i link (403 di Deliveroo = anti-bot, non rotto), mobile 375 px senza
   overflow, widget funzionante anche con cookie RIFIUTATI, ogni lingua.

## Quando il connettore rifiuta gli script
I connettori MCP di WordPress rifiutano `<script>` («requires additional permissions») anche da admin,
sia nei contenuti sia nei template. Soluzione verificata:
- Apri wp-admin nel Chrome del consulente **già loggato** (spesso `/wp-admin` dà 404 apposta: il login è
  su un URL nascosto dell'agenzia).
- Dalla console della pagina admin usa `wp.apiFetch` (porta da solo il nonce) sul template part:
  `GET/POST /wp/v2/template-parts/<tema>//footer` → aggiungi in coda un blocco `wp:html` con un
  **marker** (`<!-- cliente-gads-v1 -->`) così la modifica è idempotente e si ritrova.
- Rileggi il footer dopo il salvataggio e controlla la pagina pubblica.

## Regole RBR & trabocchetti
- Nomi dei locali SEMPRE quelli ufficiali (mai i soprannomi di quartiere), uguali su sito, GBP, TheFork.
- Niente WhatsApp se il cliente non lo presidia: un canale non risposto costa prenotazioni.
- «Offerto da TheFork» sta dentro l'iframe cross-origin: non si toglie via CSS, non perderci tempo.
- Glovo/Deliveroo: i nomi degli store possono essere invertiti rispetto all'intuito → verifica dall'ID nel sorgente.
- Foto condivise fra le schede TheFork di più locali: chiedi al cliente di quale locale è l'interno prima di usarla in una pagina sede.
- I tag di tracciamento vanno sotto il banner cookie (vedi `google-ads-conversione-controllo`).

## Definition of Done
- [ ] Prenota (widget senza commissione) raggiungibile dall'header e dalla home in ≤1 clic
- [ ] Ordina asporto/domicilio per ogni locale
- [ ] Pagine sede + piatto firma online in tutte le lingue del sito, linkate dalla home
- [ ] JSON-LD Restaurant per sede presente nel sorgente pubblico
- [ ] Crawl link 0 rotti, mobile ok, widget ok con cookie rifiutati
- [ ] Memoria cliente aggiornata con id pagine, URL widget e cosa resta allo sviluppatore
