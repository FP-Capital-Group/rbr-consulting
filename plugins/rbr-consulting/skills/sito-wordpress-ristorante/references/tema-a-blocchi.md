# Tema a blocchi del ristorante — architettura e pezzi pronti

Modello: tema `cartabianca` (v0.3.3, ott 2026). Qui c'è quello che serve per rifarlo per un altro cliente.
Prefisso consigliato per funzioni/opzioni/classi: `<cliente>_` (es. `zio_`), mai `cartabianca_` copiato.

## Principi
- **Tema a blocchi (FSE), solo blocchi core** (+ WooCommerce solo se si vende online). Niente Elementor, Divi,
  WPBakery, temi premium: il cliente deve poter modificare tutto da *Aspetto → Editor* e nessuna licenza scade.
- **Tutti gli stili in `theme.json`** (palette, font, misure, bottoni, spaziature). Nei CSS extra solo
  `var(--wp--preset--color--<slug>)`, mai esadecimali sparsi: cambiare colore = una riga di `theme.json`.
- **Font locali** in `assets/fonts/*.woff2` dichiarati in `theme.json` (`fontFace`): niente Google Fonts dal
  browser (GDPR + velocità).
- **Niente stili inline né `<style>` nelle pagine.** Un audit su Cartabianca (v7) ha imposto: titoli in un solo
  font/peso, bottoni in 2 misure (50/40 px) × 3 varianti (pieno, contorno, bianco su foto), un solo beige.
- Nessun link scritto a mano nelle template part: menu modificabili (vedi sotto).

## File
```
<cliente>/
  style.css                 intestazione tema (Theme Name, Requires at least, Version, Text Domain)
  theme.json                palette, font, layout (contentSize 760, wideSize 1200), stili blocchi, templateParts
  functions.php             vedi sezioni sotto
  parts/header.html         logo a sinistra, nav, 2 CTA; hamburger sotto ~1100 px
  parts/footer.html         ragione sociale, P.IVA, indirizzi, social, privacy/cookie
  templates/                index, page, front-page, 404, pagina-piena (template custom senza titolo)
  patterns/*.php            sezioni pronte: copertina, griglia-locali, card-locale, info-locale, faq,
                            sezione-modulo, cta-beige, fascia-riconoscimenti, testata-locale
  styles/                   block style variations (bottone-bianco, gruppo-card …)
  assets/css/extra.css      carosello, pop-up, prenotatore a schede, pillole lingua
  assets/js/extra.js        carosello + pop-up
  assets/fonts/
```
Più locali con siti separati (es. bar + ristoranti) → **tema figlio** che ridefinisce solo header/footer.

### theme.json — palette tipo (nomi parlanti: il cliente li vede nell'editor)
```json
"palette": [
  {"slug":"bianco","name":"Bianco","color":"#FFFFFF"},
  {"slug":"beige","name":"Beige (sfondo sezioni)","color":"#F5EFE0"},
  {"slug":"primario","name":"Colore del marchio (pulsanti, link, etichette)","color":"#A6192E"},
  {"slug":"primario-scuro","name":"Pulsanti al passaggio del mouse","color":"#86121F"},
  {"slug":"scuro","name":"Piè di pagina","color":"#2E170D"},
  {"slug":"linea","name":"Linee e bordi","color":"#E8E2DA"},
  {"slug":"testo","name":"Testo","color":"#1E1A17"},
  {"slug":"grigio-caldo","name":"Testi secondari","color":"#5E544C"}
]
```
Con `"defaultPalette": false` (niente colori Gutenberg di serie). Misure Cartabianca: H1 36/40 mobile →
46/48 desktop, H2 28/32 → 32/40, corpo 16/24, etichette 14 px 600 maiuscolo, card r6, foto r16, sezioni 40/80 px.

## functions.php — i pezzi

### Menu modificabili dall'editor
Nelle template part il blocco Navigazione porta la classe `<pfx>-rif-<slug>`; il tema la risolve nel post
`wp_navigation` con quello slug. Così il cliente modifica il menu da *Aspetto → Editor → Navigazione* e nessun
link è cablato nel tema.
```php
function pfx_menu_id( $slug ) {
	static $c = array();
	if ( ! isset( $c[ $slug ] ) ) {
		$ids = get_posts( array( 'post_type' => 'wp_navigation', 'name' => $slug, 'post_status' => 'publish',
			'posts_per_page' => 1, 'fields' => 'ids', 'no_found_rows' => true ) );
		$c[ $slug ] = $ids ? (int) $ids[0] : 0;
	}
	return $c[ $slug ];
}
add_filter( 'render_block_data', function ( $b ) {
	if ( 'core/navigation' === $b['blockName'] && empty( $b['attrs']['ref'] )
		&& preg_match( '/(?:^|\s)pfx-rif-([a-z0-9-]+)/', $b['attrs']['className'] ?? '', $m ) ) {
		$id = pfx_menu_id( $m[1] );
		if ( $id ) { $b['attrs']['ref'] = $id; }
	}
	return $b;
} );
```
(Cartabianca applica la stessa sostituzione anche ai filtri `get_block_template(s)` / `get_block_file_template`
così nell'Editor del sito le parti arrivano già collegate.)

### «Sito in costruzione» + link di anteprima (OBBLIGATORIO finché non si pubblica)
Visitatori non collegati → pagina di cortesia 503 + noindex; chi è collegato vede il sito; chi ha il link
`/?anteprima=<codice>` lo vede per 30 giorni senza account (cliente, consulente, controlli). In bozza
`no-store`: sennò la cache dell'hosting (Aruba HiSpeed Cache) serve a tutti le pagine viste in anteprima.
```php
add_action( 'template_redirect', function () {
	if ( 'yes' !== get_option( 'pfx_in_costruzione' ) ) { return; }
	nocache_headers();
	header( 'Cache-Control: no-cache, no-store, must-revalidate, max-age=0, private' );
	header( 'X-Robots-Tag: noindex, nofollow' );
	if ( is_user_logged_in() ) { return; }
	$codice = (string) get_option( 'pfx_anteprima_codice', '' );
	if ( '' === $codice ) { $codice = wp_generate_password( 10, false ); update_option( 'pfx_anteprima_codice', $codice, false ); }
	$firma = hash_hmac( 'sha256', $codice, wp_salt() );
	if ( isset( $_GET['anteprima'] ) && hash_equals( $codice, (string) wp_unslash( $_GET['anteprima'] ) ) ) {
		setcookie( 'pfx_anteprima', $firma, time() + 30 * DAY_IN_SECONDS, COOKIEPATH, COOKIE_DOMAIN, is_ssl(), true );
		return;
	}
	if ( isset( $_COOKIE['pfx_anteprima'] ) && hash_equals( $firma, (string) $_COOKIE['pfx_anteprima'] ) ) { return; }
	status_header( 503 ); header( 'Retry-After: 86400' );
	echo '<!doctype html><html lang="it"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>'
		. esc_html( get_bloginfo( 'name' ) ) . '</title></head><body style="display:grid;place-items:center;min-height:100vh;font-family:system-ui;text-align:center">'
		. '<main><h1>Il nuovo sito arriva presto</h1><p lang="en">Our new website is coming soon.</p></main></body></html>';
	exit;
}, 1 );
```
Più una casella in *Impostazioni → Lettura* (`register_setting( 'reading', 'pfx_in_costruzione' )` +
`add_settings_field`) che mostra anche il link di anteprima: il cliente/consulente la spegne al go-live.

### Carosello (in testa alla home)
Un blocco **Gruppo** con classe `pfx-carosello` che contiene una **Copertina** per foto: nell'editor si
vedono una sotto l'altra e si modificano come copertine normali; sul sito scorrono (scroll-snap + frecce +
pallini + autoplay 6 s, fermo con `prefers-reduced-motion`, pausa al passaggio del mouse/tocco).
CSS chiave: `.pfx-carosello{display:flex!important;overflow-x:auto;scroll-snap-type:x mandatory}`
`.pfx-carosello>*{flex:0 0 100%;scroll-snap-align:start}`. JS ~50 righe: scrivilo nel tema (`assets/js/extra.js`) con questa logica — frecce `‹ ›` con aria-label, pallini `aria-current`, `setInterval` 6 s che si ferma su hover/focus/touch e se `document.hidden`, `scrollTo({left: slide.offsetLeft})`.
Copertine: disattiva `srcset` sulle immagini di sfondo delle copertine (filtro
`wp_img_tag_add_srcset_and_sizes_attr` se contiene `wp-block-cover__image-background`), altrimenti WP sceglie la
miniatura da 768 px e la sgrana.

### Pop-up del sito
Pattern sincronizzato (`wp_block`) con slug `popup-del-sito`, modificabile da *Aspetto → Editor → Pattern*,
acceso/spento da una casella in *Impostazioni → Lettura*. Il tema lo stampa nel footer dentro un `<dialog>`;
il JS lo apre a metà pagina o dopo 20 s, max una volta ogni 7 giorni (localStorage), mai su privacy, carrello,
cassa e sulla pagina che ha già lo stesso modulo; chi si iscrive non lo rivede; un link che finisce in
`#popup` lo apre. Dentro: modulo `[rbr_modulo tipo="novita"]` con un regalo (mai uno sconto come leva
principale: `strategia-marketing-rbr`).

### Prenotatore a schede (più locali, solo CSS)
```html
<!-- wp:html --><!-- Widget TheFork – non modificare -->
<div class="pfx-rb">
  <input type="radio" name="pfx-rb" id="rb1" checked><input type="radio" name="pfx-rb" id="rb2">
  <div class="pfx-rb-schede"><label for="rb1">Locale 1<small>Via …</small></label><label for="rb2">Locale 2<small>Via …</small></label></div>
  <iframe src="https://widget.thefork.com/<uuid1>" title="Prenota Locale 1" loading="lazy"></iframe>
  <iframe src="https://widget.thefork.com/<uuid2>" title="Prenota Locale 2" loading="lazy"></iframe>
</div><!-- /wp:html -->
```
CSS: radio nascosti; `input:nth-of-type(n):checked ~ iframe:nth-of-type(n){display:block}`; iframe
`min-height:760px` (820 su mobile). In `/en/` sostituisci l'URL con `widget.thefork.com/en/<uuid>`
(filtro `render_block` sul blocco html quando la lingua è EN). «Offerto da TheFork» sta dentro l'iframe: non
si toglie.

### Lingue (TranslatePress gratuito)
- Lingue IT + EN, URL `/en/`, selettore senza bandiere: pillole «IT | EN» (filtro `render_block` sul blocco
  `trp/language-switcher` che usa `url_converter->get_url_for_language()`), niente riquadro fluttuante.
- Gli slug delle pagine restano italiani (gli slug tradotti sono a pagamento: non servono).
- Traduci anche: alt delle immagini, banner cookie, testi dei moduli (il plugin rbr-moduli è già bilingue),
  messaggi del pop-up. La quota di traduzione automatica di TranslatePress finisce subito: si scrive.

### Altro utile (Cartabianca)
- Barra fissa in basso su mobile «Chiama | Prenota» del locale della pagina.
- Meta description / Open Graph di riserva se non c'è un plugin SEO.
- Header in flusso (mai `position:absolute` centrato: col logo largo si sovrappone), hamburger sotto 1100 px.
- Niente animazioni d'ingresso o elementi che si spostano al passaggio del mouse.

## Plugin «Avvio» (quando le pagine sono tante)
Per siti con molti locali/pagine, un plugin che alla prima attivazione crea tutto, idempotente:
- `pfx_upsert( $slug, $titolo, $contenuto_blocchi )` salva un hash md5 in meta: rilanciato non tocca le pagine
  modificate a mano (salvo «forza»);
- foto con `media_handle_sideload` + meta della sorgente (non ricarica due volte) + alt IT/EN;
- menu come post `wp_navigation` con lo slug usato dalle classi `pfx-rif-*`;
- impostazioni base (titolo, motto, Europe/Rome, permalink, it_IT, commenti chiusi, demo cancellati,
  `pfx_in_costruzione=yes` se l'host non è localhost, `blog_public=0`);
- pagina *Strumenti → Avvio* con «Rilancia» (sugli hosting senza WP-CLI il build può andare in timeout: si rilancia).
Dati del cliente (locali, orari, UUID TheFork, testi) in un JSON dentro il plugin, non sparsi nel codice.
Il sito va installato **nella radice del dominio** (link interni relativi).

## Bozza locale → hosting
1. Playground con tema + plugin montati (comando in SKILL.md) e `assets/blueprint.json` (installa
   TranslatePress, attiva tema e plugin; aggiungi uno step `runPHP` per lanciare l'Avvio).
2. Zip: `cd tema && zip -r ../<cliente>.zip .` (la cartella dentro lo zip = slug del tema).
3. wp-admin del cliente: *Aspetto → Temi → Aggiungi → Carica*; *Plugin → Aggiungi → Carica*.
   Aggiornare un tema già installato = ricaricare lo zip e confermare «Sostituisci la versione attuale».
4. Mai lavorare in parallelo sul sito vivo e sulla bozza: dopo la consegna le modifiche si fanno SOLO da
   wp-admin (decisione Marco 08/10/2026), la bozza locale non è più la verità.
