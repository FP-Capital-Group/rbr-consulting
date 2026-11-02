---
name: sito-wordpress-cliente-mcp
description: Lavora sul sito WordPress GIÀ ESISTENTE di un ristorante cliente — via connettore MCP quando il sito lo espone; altrimenti REST con password per applicazioni, console di wp-admin col nonce, FTP — sezione Prenota con widget TheFork senza commissioni, tasti Ordina asporto/domicilio, pagine SEO per sede e per il piatto firma, traduzioni EN/ES, dati strutturati JSON-LD Restaurant, pulizia di link e fornitori vecchi. Include il trucco per inserire script (JSON-LD, tag Google Ads) quando il connettore li rifiuta. Usala quando il consulente dice "sistema il sito di X", "metti il tasto prenota sul sito", "aggiungi il widget TheFork", "fai le pagine SEO dei locali", "il sito non ha lo schema Restaurant", "collega il sito a Claude", "togli Quandoo dal sito". Per un sito DA ZERO usa sito-wordpress-ristorante (WordPress sull'hosting del cliente); per una landing di promo sito-landing-ristorante.
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
2. **Strada senza MCP** (se il sito non espone il connettore): password per applicazioni WordPress,
   console di wp-admin, FTP. La password per applicazioni va salvata **tra virgolette** nel file delle
   credenziali perché contiene spazi: senza virgolette `source` la spezza e `curl -u` autentica come
   anonimo **senza dare errore** (l'API risponde come a un visitatore). Leggila con
   `grep '^PASSWORD=' <file> | cut -d= -f2-` e non stamparla mai.
3. Chiedi chi altro lavora sul sito (sviluppatore dell'agenzia): modifiche grosse al tema vanno
   coordinate. **Chi controlla cosa**: con `whois` verifica intestatario e scadenza del dominio — se è
   intestato alla società del titolare, l'accesso si pretende, non si chiede come favore. La zona DNS
   può stare dal registrar e non nel pannello di hosting (sottodomini/CNAME li fa chi ha quel pannello;
   col solo FTP non si promette di crearli); la propagazione si controlla con `dig`. L'hosting può
   migrare il sito senza avviso (per questo come host FTP usa sempre il **dominio**, non un IP). Gli
   utenti WordPress e le loro date di creazione dicono chi ha messo le mani sul sito.
4. Link prenotazione e delivery del cliente per ogni locale (TheFork, Deliveroo, Glovo, telefono).

(contributo di Andrea Chirivì, 12/10/2026)

## Procedura
1. **Leggi prima di scrivere**: design system del tema, pagine esistenti, template di header/footer,
   pattern già pronti (galleria, fisarmonica, card) — usare quelli invece di scrivere HTML nuovo. Prima
   di creare pop-up, snippet o pagine nuove, tre chiamate obbligatorie: snippet attivi
   (`GET /wp-json/code-snippets/v1/snippets`), plugin attivi (`/wp-json/wp/v2/plugins`), tipi di
   contenuto (`GET /wp-json/wp/v2/types`, compaiono anche tipi come `firebox`, `elementor_snippet`). Per
   ogni pezzo trovato leggi le sue regole di visualizzazione prima di dichiararlo rotto o mancante — è
   già capitato di rifare da zero un pop-up che esisteva già e non usciva solo per una regola sbagliata.
   Se la pagina è fatta con un page builder (Brizy, Elementor) **non riscriverla via REST**: vedi
   `references/trappole-wordpress.md`, sezione «Page builder».
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
   Se più pagine condividono un foglio sorgente e nascono da script (es. pagine ricorrenti, `/eventi/`
   da un file dati): vedi `references/trappole-wordpress.md`, sezione «Pagine generate da script».
   Il lato tecnico del blog (copertine, autore, paginazione) è nella stessa reference, sezione «Blog»
   — cosa scrivere resta in `seo-local-ristorante`.
5. **SEO tecnica**: title/description mancanti, alt delle immagini in uso, sitemap, http→https.
   **Se cambi la home**: salva prima `page_on_front`/`page_for_posts` per poter tornare indietro — la
   pagina nuova NON eredita title/description SEO, vanno riscritti subito o Google si costruisce da
   solo lo snippet (perdita di clic sulla query di marca). Ricontrolla anche: regole dei pop-up che
   puntavano all'ID della vecchia home, codice di tracciamento dentro il contenuto, voci di menu verso
   la vecchia home, doppio H1. La vecchia home va in bozza con un 301 verso `/`.
6. **JSON-LD**: Organization + un `Restaurant` per sede (address, orari, servesCuisine, hasMenu,
   acceptsReservations = URL del widget), nel footer.
7. **Pulizia**: fornitori dismessi (es. Quandoo) da banner cookie, Cookie Policy, Termini, footer.
   **Redirect**: prima di aggiungerne uno controlla TUTTI i posti dove possono vivere (plugin 301
   Redirects, mu-plugin con mappa, `.htaccess`) — una regola resta attiva anche con la pagina in bozza
   e può nascondere in silenzio un widget o una sezione nuova. Le URL in redirect si tolgono dalla
   sitemap. **Voci di menu**: controllale una per una (una voce verso una bozza dà 404), cerca pagine
   orfane e menu_order duplicati (rinumerare). **Telefono**: `callto:` è morto, sostituisci con
   `tel:+39…` ovunque, dati del page builder compresi.
8. **Verifica**: crawl di tutti i link (403 di Deliveroo = anti-bot, non rotto), mobile 375 px senza
   overflow, widget funzionante anche con cookie RIFIUTATI, ogni lingua. **Cache di pagina**: una
   verifica con `?cb=<casuale>` salta la cache e mostra l'HTML giusto anche se il visitatore reale vede
   quello vecchio — controlla l'header `wpo-cache-status` su una richiesta SENZA query string, e dopo
   ogni modifica lato server (menu, pagine, snippet, head, PHP) svuota la cache prima di concludere.
   Dettagli trappole in `references/trappole-wordpress.md`.

(contributo di Andrea Chirivì, 12/10/2026)

## Quando il connettore rifiuta gli script
I connettori MCP di WordPress rifiutano `<script>` («requires additional permissions») anche da admin,
sia nei contenuti sia nei template. Soluzione verificata:
- Apri wp-admin nel Chrome del consulente **già loggato** (spesso `/wp-admin` dà 404 apposta: il login è
  su un URL nascosto dell'agenzia).
- Dalla console della pagina admin usa `wp.apiFetch` (porta da solo il nonce) sul template part:
  `GET/POST /wp/v2/template-parts/<tema>//footer` → aggiungi in coda un blocco `wp:html` con un
  **marker** (`<!-- cliente-gads-v1 -->`) così la modifica è idempotente e si ritrova.
- In alternativa, dalla console di wp-admin usa `fetch` con header `X-WP-Nonce` =
  `wpApiSettings.nonce` su `/wp/v2/pages/<id>` o `/wp/v2/widgets/<id>`, aggirando Gutenberg e i campi
  React (Gutenberg si blocca da solo su un blocco HTML sopra i ~10 KB, la REST no; su un widget
  ripassa sempre anche `title` nel payload, altrimenti si azzera).
- Rileggi il footer/pagina dopo il salvataggio e controlla la pagina pubblica.
- WordPress **riscrive** quello che scrivi (wpautop, wptexturize, entità HTML) e il CSS non accetta
  caratteri non-ASCII in `content:`; un mu-plugin non collaudato può far cadere l'intero sito; per il
  codice globale (CSS/JS/PHP) ci sono strade diverse secondo lo strumento del tema — tutti i dettagli e
  le trappole in `references/trappole-wordpress.md`.

## Regole RBR & trabocchetti
- Nomi dei locali SEMPRE quelli ufficiali (mai i soprannomi di quartiere), uguali su sito, GBP, TheFork.
- Niente WhatsApp se il cliente non lo presidia: un canale non risposto costa prenotazioni.
- «Offerto da TheFork» sta dentro l'iframe cross-origin: non si toglie via CSS, non perderci tempo.
- Glovo/Deliveroo: i nomi degli store possono essere invertiti rispetto all'intuito → verifica dall'ID nel sorgente.
- Foto condivise fra le schede TheFork di più locali: chiedi al cliente di quale locale è l'interno prima di usarla in una pagina sede.
- I tag di tracciamento vanno sotto il banner cookie (vedi `google-ads-conversione-controllo`).
- **Una pagina "non si aggiorna"? Primo controllo (Plesk): una cartella fisica in `httpdocs` con lo
  stesso nome dello slug** (es. `httpdocs/cassa/index.html`) serve il suo contenuto mentre la pagina WP
  resta pubblicata e invisibile — il sito non corrisponde al database e le revisioni sembrano sparite.
  Ordine di diagnosi: 1) FTP, cartella omonima in `httpdocs`; 2) cache di pagina (sopra); 3) solo dopo,
  il database. Togliendo la cartella la pagina WP torna a rispondere. Dettagli in
  `references/trappole-wordpress.md`.
- **Moduli del sito che scrivono nel CRM (GHL)**: un endpoint pubblico (mu-plugin) va collaudato SOLO
  compilando dalla pagina vera fino al contatto creato nel CRM, mai solo con `curl` sull'endpoint — un
  mismatch fra l'id HTML (es. `ca-nome`, con trattino) e il JS che legge `ca_nome` fa fallire il modulo
  in silenzio anche se l'endpoint risponde bene. Dettagli in `references/trappole-wordpress.md`.

## Definition of Done
- [ ] Prenota (widget senza commissione) raggiungibile dall'header e dalla home in ≤1 clic
- [ ] Ordina asporto/domicilio per ogni locale
- [ ] Pagine sede + piatto firma online in tutte le lingue del sito, linkate dalla home
- [ ] JSON-LD Restaurant per sede presente nel sorgente pubblico
- [ ] Crawl link 0 rotti (voci di menu, redirect e `tel:` controllati), mobile ok, widget ok con cookie rifiutati
- [ ] Cache di pagina svuotata dopo ogni modifica lato server e verificata senza query string
- [ ] Ogni modulo che scrive nel CRM collaudato dalla pagina vera fino al contatto creato in GHL
- [ ] Memoria cliente aggiornata con id pagine, URL widget e cosa resta allo sviluppatore
