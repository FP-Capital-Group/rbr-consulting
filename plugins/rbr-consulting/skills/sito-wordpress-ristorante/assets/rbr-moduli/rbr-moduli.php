<?php
/**
 * Plugin Name:       RBR – Moduli ristorante
 * Description:       Moduli del sito (prenotazione, evento, contatto, novità/club) che scrivono il contatto DIRETTAMENTE nel CRM GoHighLevel del ristorante, con tag e nota. Nessun server esterno: tutto gira su questo WordPress. Se il CRM non risponde arriva una email di riserva e l'invio resta salvato in bacheca (Moduli → Invii). Uso: blocco «Shortcode» con [rbr_modulo tipo="prenotazione"].
 * Version:           1.0.0
 * Requires at least: 6.5
 * Requires PHP:      7.4
 * Author:            Restaurant Business Revolution
 * License:           GPL-2.0-or-later
 * Text Domain:       rbr-moduli
 *
 * Configurazione in wp-config.php (MAI nel database, MAI in un repository):
 *   define( 'RBR_GHL_TOKEN', 'pit-…' );      Private Integration Token del sub-account GHL DEL CLIENTE (scope: contacts.write, contacts.readonly)
 *   define( 'RBR_GHL_LOCATION', '…' );       Location ID del sub-account del cliente
 * Senza queste due costanti i moduli funzionano lo stesso: arriva solo la mail + copia in bacheca.
 *
 * Tutto il resto (email notifiche, sedi, prefisso tag, link privacy) sta in Impostazioni → Moduli RBR.
 */

if ( ! defined( 'ABSPATH' ) ) {
	exit;
}

const RBR_MODULI_TIPI = array( 'prenotazione', 'evento', 'contatto', 'novita' );

/** Impostazioni con i valori predefiniti. */
function rbrm_opt( $k ) {
	$def = array(
		'email'     => get_option( 'admin_email' ),
		'sedi'      => '',
		'prefisso'  => 'lead-sito-' . sanitize_title( wp_parse_url( home_url(), PHP_URL_HOST ) ),
		'privacy'   => '/privacy/',
		'orari'     => "12:00\n12:30\n13:00\n13:30\n19:30\n20:00\n20:30\n21:00\n21:30",
		// campo del modulo = chiave del campo personalizzato GHL (SENZA «contact.»: con il prefisso GHL lo ignora in silenzio).
		// Nomi del modello base RBR (skill onboarding-cliente-ghl): se il campo non esiste nel sub-account viene ignorato.
		'campi'     => "sede_nome = pv\nlingua = lingua\ndata = giorno_prenotazione\nora = orario_prenotazione\npersone = numerodipersone\ncompleanno = compleanno_gg_mm",
	);
	$v = get_option( 'rbrm_' . $k, null );
	return null === $v || '' === $v ? $def[ $k ] : $v;
}

/** Sedi: una per riga nelle impostazioni → [ slug => nome ]. Vuoto = locale unico, nessuna tendina. */
function rbrm_sedi() {
	$out = array();
	foreach ( preg_split( '/\R/', (string) rbrm_opt( 'sedi' ) ) as $r ) {
		$r = trim( $r );
		if ( '' !== $r ) {
			$out[ sanitize_title( $r ) ] = $r;
		}
	}
	return $out;
}

/** Mappa campo del modulo → chiave GHL, dalle impostazioni («campo = chiave» una per riga). */
function rbrm_mappa_campi() {
	$m = array();
	foreach ( rbrm_righe( 'campi' ) as $r ) {
		$p = array_map( 'trim', explode( '=', $r, 2 ) );
		if ( 2 === count( $p ) && '' !== $p[0] && '' !== $p[1] ) {
			$m[ sanitize_key( $p[0] ) ] = preg_replace( '/^contact\./', '', sanitize_text_field( $p[1] ) );
		}
	}
	return $m;
}

function rbrm_righe( $k ) {
	return array_values( array_filter( array_map( 'trim', preg_split( '/\R/', (string) rbrm_opt( $k ) ) ) ) );
}

/** Lingua corrente (TranslatePress / Polylang / WPML scrivono la lingua in <html lang>). */
function rbrm_en() {
	return 0 === strpos( determine_locale(), 'en' );
}

function rbrm_t( $it, $en ) {
	return rbrm_en() ? $en : $it;
}

// ─── Gettone anti-bot: uguale per tutti i visitatori, regge la cache di pagina (vale 12-24 h) ─────────

function rbrm_token( $passo = 0 ) {
	return substr( wp_hash( 'rbr-modulo|' . ( (int) floor( time() / 43200 ) - $passo ), 'nonce' ), -12 );
}
function rbrm_token_ok( $t ) {
	return $t && ( hash_equals( rbrm_token( 0 ), $t ) || hash_equals( rbrm_token( 1 ), $t ) );
}

/** Ora di apertura del modulo firmata dal server («<secondi>.<firma>»): il bot non può falsificarla. */
function rbrm_t_firma( $ts ) {
	return $ts . '.' . substr( wp_hash( 'rbr-modulo-t|' . $ts, 'nonce' ), -10 );
}
function rbrm_t_secondi( $v ) {
	$p = explode( '.', (string) $v );
	return 2 === count( $p ) && hash_equals( rbrm_t_firma( (int) $p[0] ), (string) $v ) ? time() - (int) $p[0] : -1;
}

/** Massimo 5 invii ogni 10 minuti dallo stesso indirizzo IP. */
function rbrm_troppi() {
	$k = 'rbrm_ip_' . md5( (string) ( $_SERVER['REMOTE_ADDR'] ?? '' ) );
	$n = (int) get_transient( $k );
	set_transient( $k, $n + 1, 10 * MINUTE_IN_SECONDS );
	return $n >= 5;
}

// ─── Shortcode [rbr_modulo tipo="prenotazione|evento|contatto|novita" titolo="…"] ─────────────────────

add_shortcode(
	'rbr_modulo',
	function ( $a ) {
		$a    = shortcode_atts( array( 'tipo' => 'prenotazione', 'bottone' => '' ), $a );
		$tipo = in_array( $a['tipo'], RBR_MODULI_TIPI, true ) ? $a['tipo'] : 'contatto';
		wp_enqueue_script( 'rbr-moduli' );
		wp_enqueue_style( 'rbr-moduli' );

		$c = function ( $nome, $label, $html ) {
			return '<p class="rbrm-campo rbrm-' . esc_attr( $nome ) . '"><label>' . esc_html( $label ) . $html . '</label></p>';
		};
		$in = function ( $nome, $type, $req, $extra = '' ) {
			return '<input name="' . esc_attr( $nome ) . '" type="' . esc_attr( $type ) . '"' . ( $req ? ' required' : '' ) . ' ' . $extra . '>';
		};
		$f   = array();
		$f[] = $c( 'nome', rbrm_t( 'Nome e cognome', 'Full name' ), $in( 'nome', 'text', true, 'autocomplete="name"' ) );
		$tel_req = 'novita' !== $tipo;
		$f[] = $c( 'telefono', rbrm_t( 'Telefono', 'Phone' ) . ( $tel_req ? '' : rbrm_t( ' (facoltativo)', ' (optional)' ) ), $in( 'telefono', 'tel', $tel_req, 'autocomplete="tel" inputmode="tel"' ) );
		$f[] = $c( 'email', 'Email' . ( 'novita' === $tipo ? '' : rbrm_t( ' (facoltativa)', ' (optional)' ) ), $in( 'email', 'email', 'novita' === $tipo, 'autocomplete="email"' ) );

		$sedi = rbrm_sedi();
		if ( $sedi && 'novita' !== $tipo ) {
			$o = '<option value="">' . esc_html( rbrm_t( 'Scegli…', 'Choose…' ) ) . '</option>';
			foreach ( $sedi as $s => $n ) {
				$o .= '<option value="' . esc_attr( $s ) . '">' . esc_html( $n ) . '</option>';
			}
			$f[] = $c( 'sede', rbrm_t( 'Locale', 'Restaurant' ), '<select name="sede" required>' . $o . '</select>' );
		}
		if ( 'prenotazione' === $tipo || 'evento' === $tipo ) {
			$oggi = wp_date( 'Y-m-d' );
			$f[]  = $c( 'data', rbrm_t( 'Giorno', 'Date' ), $in( 'data', 'date', true, 'min="' . esc_attr( $oggi ) . '"' ) );
			if ( 'prenotazione' === $tipo ) {
				$o = '';
				foreach ( rbrm_righe( 'orari' ) as $h ) {
					$o .= '<option>' . esc_html( $h ) . '</option>';
				}
				$f[] = $c( 'ora', rbrm_t( 'Ora', 'Time' ), '<select name="ora" required>' . $o . '</select>' );
			}
			$f[] = $c( 'persone', rbrm_t( 'Persone', 'Guests' ), $in( 'persone', 'number', true, 'min="1" max="300" inputmode="numeric"' ) );
		}
		if ( 'novita' === $tipo ) {
			$f[] = $c( 'compleanno', rbrm_t( 'Compleanno (giorno e mese, facoltativo)', 'Birthday (day and month, optional)' ), $in( 'compleanno', 'text', false, 'placeholder="' . esc_attr( rbrm_t( 'gg/mm', 'dd/mm' ) ) . '" pattern="[0-3]?[0-9]/[01]?[0-9]" inputmode="numeric" maxlength="5"' ) );
		}
		if ( 'novita' !== $tipo ) {
			$f[] = $c( 'messaggio', 'evento' === $tipo ? rbrm_t( 'Raccontaci la festa', 'Tell us about the event' ) : rbrm_t( 'Note', 'Notes' ), '<textarea name="messaggio" rows="3"></textarea>' );
		}
		$priv = esc_url( home_url( rbrm_opt( 'privacy' ) ) );
		$f[]  = '<p class="rbrm-check"><label><input type="checkbox" name="privacy" value="1" required> ' . sprintf( rbrm_t( 'Ho letto l\'<a href="%s">informativa privacy</a>', 'I have read the <a href="%s">privacy policy</a>' ), $priv ) . '</label></p>';
		$f[]  = '<p class="rbrm-check"><label><input type="checkbox" name="marketing" value="1"> ' . esc_html( rbrm_t( 'Voglio ricevere novità e offerte via email, WhatsApp e SMS (facoltativo)', 'I want to receive news and offers by email, WhatsApp and SMS (optional)' ) ) . '</label></p>';
		// campo trappola per i bot (nascosto con CSS, non con type=hidden)
		$f[] = '<p class="rbrm-hp" aria-hidden="true"><label>Sito web<input name="sito_web" type="text" tabindex="-1" autocomplete="off"></label></p>';

		$bottone = $a['bottone'] ?: array(
			'prenotazione' => rbrm_t( 'Invia la richiesta', 'Send request' ),
			'evento'       => rbrm_t( 'Richiedi un preventivo', 'Request a quote' ),
			'contatto'     => rbrm_t( 'Invia', 'Send' ),
			'novita'       => rbrm_t( 'Iscrivimi', 'Sign me up' ),
		)[ $tipo ];

		return '<form class="rbrm-form" data-rbrm novalidate>'
			. '<input type="hidden" name="tipo" value="' . esc_attr( $tipo ) . '">'
			. '<input type="hidden" name="t" value="' . esc_attr( rbrm_t_firma( time() ) ) . '">'
			. '<input type="hidden" name="gettone" value="' . esc_attr( rbrm_token() ) . '">'
			. '<input type="hidden" name="lingua" value="' . ( rbrm_en() ? 'en' : 'it' ) . '">'
			. '<input type="hidden" name="fonte" value="">'
			. '<input type="hidden" name="pagina" value="">'
			. implode( '', $f )
			. '<div class="wp-block-button"><button type="submit" class="wp-block-button__link wp-element-button">' . esc_html( $bottone ) . '</button></div>'
			. '<p class="rbrm-esito" role="status" aria-live="polite"></p>'
			. '</form>';
	}
);

add_action(
	'wp_enqueue_scripts',
	function () {
		wp_register_script( 'rbr-moduli', false, array(), '1.0.0', array( 'in_footer' => true ) );
		wp_add_inline_script(
			'rbr-moduli',
			'window.rbrModuli=' . wp_json_encode(
				array(
					'url'    => esc_url_raw( rest_url( 'rbr-moduli/v1/invia' ) ),
					'attesa' => rbrm_t( 'Invio in corso…', 'Sending…' ),
					'errore' => rbrm_t( 'Non siamo riusciti a inviare. Riprova o chiamaci.', 'We could not send it. Please try again or call us.' ),
					'campi'  => rbrm_t( 'Controlla i campi evidenziati.', 'Please check the highlighted fields.' ),
				)
			) . ';' . file_get_contents( __DIR__ . '/rbr-moduli.js' ) // phpcs:ignore WordPress.WP.AlternativeFunctions
		);
		wp_register_style( 'rbr-moduli', false, array(), '1.0.0' );
		wp_add_inline_style(
			'rbr-moduli',
			'.rbrm-form{display:grid;gap:12px;max-width:640px}.rbrm-campo{margin:0}.rbrm-campo label{display:grid;gap:6px;font-weight:600}'
			. '.rbrm-form input:not([type=checkbox]),.rbrm-form select,.rbrm-form textarea{min-height:48px;line-height:1.4;padding:10px 12px;font:inherit;font-weight:400;border:1px solid currentColor;border-radius:6px;background:#fff;color:inherit;width:100%;box-sizing:border-box}'
			. '.rbrm-form input::-webkit-date-and-time-value{text-align:left}.rbrm-check{margin:0;font-size:.9em}.rbrm-check input{width:20px;height:20px;vertical-align:middle;margin-right:6px}'
			. '.rbrm-hp{position:absolute!important;left:-9999px!important}.rbrm-errore input,.rbrm-errore select,.rbrm-errore textarea{outline:2px solid #B3261E}.rbrm-esito:empty{display:none}.rbrm-esito{font-weight:600}'
		);
	}
);

// ─── Invio: REST rbr-moduli/v1/invia ─────────────────────────────────────────────────────────────────

add_action(
	'rest_api_init',
	function () {
		register_rest_route(
			'rbr-moduli/v1',
			'/invia',
			array(
				'methods'             => 'POST',
				'callback'            => 'rbrm_invia',
				'permission_callback' => '__return_true', // modulo pubblico: protetto da gettone, trappola e tempo minimo
			)
		);
	}
);

function rbrm_invia( WP_REST_Request $req ) {
	$in = $req->get_params();
	$en = 'en' === ( $in['lingua'] ?? '' );
	$ok = $en ? 'Thank you! We have received your request and will get back to you soon.' : 'Grazie! Abbiamo ricevuto la tua richiesta, ti ricontattiamo al più presto.';
	// bot: campo trappola compilato o invio in meno di 3 secondi → «ok» e scarto
	$secondi = rbrm_t_secondi( $in['t'] ?? '' );
	if ( ! empty( $in['sito_web'] ) || ( $secondi >= 0 && $secondi < 3 ) ) {
		return new WP_REST_Response( array( 'ok' => true, 'messaggio' => $ok ), 200 );
	}
	if ( $secondi < 0 || ! rbrm_token_ok( (string) ( $in['gettone'] ?? '' ) ) ) {
		return new WP_REST_Response( array( 'ok' => false, 'messaggio' => $en ? 'Page expired: reload it and try again.' : 'Pagina scaduta: ricaricala e riprova.' ), 403 );
	}
	if ( rbrm_troppi() ) {
		return new WP_REST_Response( array( 'ok' => false, 'messaggio' => $en ? 'Too many requests: please call us.' : 'Troppi invii: chiamaci per favore.' ), 429 );
	}
	$tipo = in_array( $in['tipo'] ?? '', RBR_MODULI_TIPI, true ) ? $in['tipo'] : '';
	$sedi = rbrm_sedi();
	$d    = array(
		'nome'      => sanitize_text_field( $in['nome'] ?? '' ),
		'telefono'  => preg_replace( '/[^+0-9]/', '', (string) ( $in['telefono'] ?? '' ) ),
		'email'     => sanitize_email( $in['email'] ?? '' ),
		'sede'      => sanitize_title( $in['sede'] ?? '' ),
		'data'      => sanitize_text_field( $in['data'] ?? '' ),
		'ora'       => sanitize_text_field( $in['ora'] ?? '' ),
		'persone'   => absint( $in['persone'] ?? 0 ),
		'messaggio' => sanitize_textarea_field( $in['messaggio'] ?? '' ),
		'compleanno' => sanitize_text_field( $in['compleanno'] ?? '' ),
		'marketing' => ! empty( $in['marketing'] ),
		'privacy'   => ! empty( $in['privacy'] ),
		'fonte'     => sanitize_text_field( $in['fonte'] ?? '' ),
		'pagina'    => esc_url_raw( (string) ( $in['pagina'] ?? '' ) ),
		'lingua'    => $en ? 'en' : 'it',
	);
	$err = array();
	if ( ! $tipo ) {
		$err[] = 'tipo';
	}
	if ( '' === $d['nome'] ) {
		$err[] = 'nome';
	}
	$d['telefono'] = rbrm_tel( $d['telefono'] );
	$tel_ok        = (bool) preg_match( '/^\+[0-9]{8,15}$/', $d['telefono'] );
	if ( 'novita' === $tipo ? ( '' !== $d['telefono'] && ! $tel_ok ) : ! $tel_ok ) {
		$err[] = 'telefono';
	}
	if ( 'novita' === $tipo ? ! is_email( $d['email'] ) : ( '' !== $d['email'] && ! is_email( $d['email'] ) ) ) {
		$err[] = 'email';
	}
	if ( $sedi && 'novita' !== $tipo && ! isset( $sedi[ $d['sede'] ] ) ) {
		$err[] = 'sede';
	}
	if ( in_array( $tipo, array( 'prenotazione', 'evento' ), true ) ) {
		if ( ! preg_match( '/^\d{4}-\d{2}-\d{2}$/', $d['data'] ) || $d['data'] < wp_date( 'Y-m-d' ) ) {
			$err[] = 'data';
		}
		if ( $d['persone'] < 1 || $d['persone'] > 300 ) {
			$err[] = 'persone';
		}
		if ( 'prenotazione' === $tipo && ! in_array( $d['ora'], rbrm_righe( 'orari' ), true ) ) {
			$err[] = 'ora';
		}
	}
	if ( '' !== $d['compleanno'] ) {
		if ( preg_match( '#^([0-3]?[0-9])/([01]?[0-9])$#', $d['compleanno'], $m ) && checkdate( (int) $m[2], (int) $m[1], 2024 ) ) {
			$d['compleanno'] = sprintf( '%02d/%02d', $m[1], $m[2] ); // giorno e mese, senza anno
		} else {
			$err[] = 'compleanno';
		}
	}
	if ( ! $d['privacy'] ) {
		$err[] = 'privacy';
	}
	if ( $err ) {
		return new WP_REST_Response( array( 'ok' => false, 'campi' => $err, 'messaggio' => $en ? 'Please check the highlighted fields.' : 'Controlla i campi evidenziati.' ), 422 );
	}
	$d['sede_nome'] = $sedi[ $d['sede'] ] ?? '';

	$crm = rbrm_ghl( $tipo, $d );
	rbrm_mail( $tipo, $d, $crm );
	if ( ! $crm['ok'] ) {
		rbrm_riserva( $tipo, $d, $crm['motivo'] );
	}
	return new WP_REST_Response( array( 'ok' => true, 'messaggio' => $ok ), 200 );
}

/** Telefono in formato internazionale: 00… → +…; numero italiano (3… o 0…, 9-11 cifre) → +39…; il resto com'è. */
function rbrm_tel( $t ) {
	if ( 0 === strpos( $t, '00' ) ) {
		return '+' . substr( $t, 2 );
	}
	if ( '' !== $t && '+' !== $t[0] && preg_match( '/^[03][0-9]{8,10}$/', $t ) ) {
		return '+39' . $t;
	}
	return $t;
}

/** Riepilogo leggibile (nota GHL, mail, copia di riserva). */
function rbrm_riepilogo( $tipo, $d ) {
	$r = array( 'Modulo: ' . $tipo );
	foreach ( array( 'nome' => 'Nome', 'telefono' => 'Telefono', 'email' => 'Email', 'sede_nome' => 'Locale', 'compleanno' => 'Compleanno', 'data' => 'Giorno', 'ora' => 'Ora', 'persone' => 'Persone', 'messaggio' => 'Messaggio', 'fonte' => 'Provenienza', 'pagina' => 'Pagina', 'lingua' => 'Lingua' ) as $k => $l ) {
		if ( '' !== (string) $d[ $k ] && 0 !== $d[ $k ] ) {
			$r[] = $l . ': ' . $d[ $k ];
		}
	}
	$r[] = 'Consenso marketing: ' . ( $d['marketing'] ? 'sì' : 'no' );
	$r[] = 'Privacy accettata: ' . gmdate( 'c' );
	return implode( "\n", $r );
}

/** Tag uguali su tutti i siti RBR: <prefisso>, form-<tipo>, pv-<locale>, consenso-marketing, lingua-en. */
function rbrm_tag( $tipo, $d ) {
	$p = sanitize_title( rbrm_opt( 'prefisso' ) );
	$t = array( $p, 'form-' . $tipo );
	if ( $d['sede'] ) {
		$t[] = 'pv-' . $d['sede']; // famiglia pv-<locale> del modello base GHL
	}
	if ( $d['marketing'] ) {
		$t[] = 'consenso-marketing';
	}
	if ( 'en' === $d['lingua'] ) {
		$t[] = 'lingua-en';
	}
	return $t;
}

function rbrm_ghl_call( $metodo, $path, $body ) {
	$base = defined( 'RBR_GHL_API' ) ? RBR_GHL_API : 'https://services.leadconnectorhq.com';
	$r    = wp_remote_request(
		$base . $path,
		array(
			'method'  => $metodo,
			'timeout' => 10,
			'headers' => array(
				'Authorization' => 'Bearer ' . RBR_GHL_TOKEN,
				'Version'       => '2021-07-28',
				'Content-Type'  => 'application/json',
				'Accept'        => 'application/json',
			),
			'body'    => wp_json_encode( $body, JSON_UNESCAPED_UNICODE ),
		)
	);
	if ( is_wp_error( $r ) ) {
		return array( 0, $r->get_error_message() );
	}
	return array( (int) wp_remote_retrieve_response_code( $r ), json_decode( wp_remote_retrieve_body( $r ), true ) );
}

/**
 * Scrive nel CRM del cliente: upsert del contatto (dedup su email/telefono), poi tag (aggiunti, mai sostituiti)
 * e una nota col riepilogo. I workflow GHL partono dal tag form-<tipo>.
 */
function rbrm_ghl( $tipo, $d ) {
	if ( ! defined( 'RBR_GHL_TOKEN' ) || ! defined( 'RBR_GHL_LOCATION' ) || ! RBR_GHL_TOKEN || ! RBR_GHL_LOCATION ) {
		return array( 'ok' => false, 'motivo' => 'RBR_GHL_TOKEN / RBR_GHL_LOCATION assenti in wp-config.php' );
	}
	$parti = explode( ' ', $d['nome'], 2 );
	$c     = array(
		'locationId' => RBR_GHL_LOCATION,
		'firstName'  => $parti[0],
		'lastName'   => $parti[1] ?? '',
	);
	if ( $d['email'] ) {
		$c['email'] = $d['email'];
	}
	if ( $d['telefono'] ) {
		$c['phone'] = $d['telefono'];
	}
	$cf = array();
	foreach ( rbrm_mappa_campi() as $campo => $chiave ) {
		if ( isset( $d[ $campo ] ) && '' !== (string) $d[ $campo ] && 0 !== $d[ $campo ] ) {
			$cf[] = array( 'key' => $chiave, 'field_value' => (string) $d[ $campo ] );
		}
	}
	if ( $cf ) {
		$c['customFields'] = $cf;
	}
	list( $code, $res ) = rbrm_ghl_call( 'POST', '/contacts/upsert', $c );
	$id = is_array( $res ) ? ( $res['contact']['id'] ?? '' ) : '';
	if ( ( 200 !== $code && 201 !== $code ) || ! $id ) {
		return array( 'ok' => false, 'motivo' => 'GHL upsert HTTP ' . $code . ' ' . ( is_array( $res ) ? wp_json_encode( $res ) : (string) $res ) );
	}
	if ( ! empty( $res['new'] ) ) { // origine solo sui contatti nuovi: non si cancella l'attribuzione (Meta, coupon…) dei vecchi
		rbrm_ghl_call( 'PUT', '/contacts/' . rawurlencode( $id ), array( 'source' => 'Sito ' . wp_parse_url( home_url(), PHP_URL_HOST ) ) );
	}
	list( $ct ) = rbrm_ghl_call( 'POST', '/contacts/' . rawurlencode( $id ) . '/tags', array( 'tags' => rbrm_tag( $tipo, $d ) ) );
	list( $cn ) = rbrm_ghl_call( 'POST', '/contacts/' . rawurlencode( $id ) . '/notes', array( 'body' => rbrm_riepilogo( $tipo, $d ) ) );
	if ( ! in_array( $ct, array( 200, 201 ), true ) ) {
		return array( 'ok' => false, 'motivo' => 'contatto ' . $id . ' creato ma tag non messi (HTTP ' . $ct . ')' );
	}
	if ( ! in_array( $cn, array( 200, 201 ), true ) ) {
		return array( 'ok' => false, 'motivo' => 'contatto ' . $id . ' creato con i tag ma nota non salvata (HTTP ' . $cn . ')' );
	}
	return array( 'ok' => true, 'id' => $id );
}

/** Mail al ristorante per ogni invio (rispondendo si scrive al cliente). */
function rbrm_mail( $tipo, $d, $crm ) {
	$h = array();
	if ( $d['email'] ) {
		$h[] = 'Reply-To: ' . $d['email']; // solo l'indirizzo: un nome con la virgola creerebbe destinatari in più
	}
	$oggetto = sprintf( '[%s] %s – %s%s', wp_parse_url( home_url(), PHP_URL_HOST ), $tipo, $d['nome'], $d['data'] ? ' – ' . $d['data'] . ' ' . $d['ora'] : '' );
	$testo   = rbrm_riepilogo( $tipo, $d ) . "\n\nCRM: " . ( $crm['ok'] ? 'contatto salvato' : 'NON salvato (' . $crm['motivo'] . ') – copia in Moduli → Invii' );
	foreach ( array_filter( array_map( 'trim', explode( ',', (string) rbrm_opt( 'email' ) ) ) ) as $a ) {
		wp_mail( $a, $oggetto, $testo, $h );
	}
}

/** Copia di riserva in bacheca quando il CRM non risponde. */
add_action(
	'init',
	function () {
		register_post_type(
			'rbr_invio',
			array(
				'label'           => 'Invii moduli',
				'public'          => false,
				'show_ui'         => true,
				'show_in_menu'    => 'rbr-moduli',
				'capability_type' => 'post',
				'capabilities'    => array( 'create_posts' => 'do_not_allow' ),
				'map_meta_cap'    => true,
				'supports'        => array( 'title', 'editor' ),
			)
		);
	}
);
/** Le copie di riserva contengono dati personali: si cancellano da sole dopo 90 giorni (una volta al giorno). */
add_action(
	'admin_init',
	function () {
		if ( get_transient( 'rbrm_pulizia' ) ) {
			return;
		}
		set_transient( 'rbrm_pulizia', 1, DAY_IN_SECONDS );
		foreach ( get_posts( array( 'post_type' => 'rbr_invio', 'post_status' => 'any', 'numberposts' => 200, 'fields' => 'ids', 'date_query' => array( array( 'before' => '90 days ago' ) ) ) ) as $id ) {
			wp_delete_post( $id, true );
		}
	}
);
function rbrm_riserva( $tipo, $d, $motivo ) {
	wp_insert_post(
		array(
			'post_type'    => 'rbr_invio',
			'post_status'  => 'private',
			'post_title'   => $tipo . ' – ' . $d['nome'] . ' – ' . wp_date( 'd/m/Y H:i' ),
			'post_content' => '<pre>' . esc_html( rbrm_riepilogo( $tipo, $d ) . "\n\nMotivo: " . $motivo ) . '</pre>',
		)
	);
}

// ─── Impostazioni → Moduli RBR ───────────────────────────────────────────────────────────────────────

add_action(
	'admin_menu',
	function () {
		add_menu_page( 'Moduli RBR', 'Moduli', 'manage_options', 'rbr-moduli', 'rbrm_pagina', 'dashicons-feedback', 58 );
	}
);
add_action(
	'admin_init',
	function () {
		foreach ( array( 'email', 'sedi', 'prefisso', 'privacy', 'orari', 'campi' ) as $k ) {
			register_setting( 'rbr-moduli', 'rbrm_' . $k, array( 'sanitize_callback' => 'sanitize_textarea_field' ) );
		}
	}
);
function rbrm_pagina() {
	$crm = defined( 'RBR_GHL_TOKEN' ) && RBR_GHL_TOKEN && defined( 'RBR_GHL_LOCATION' ) && RBR_GHL_LOCATION;
	echo '<div class="wrap"><h1>Moduli del sito</h1>';
	echo $crm
		? '<p>✅ Collegato al CRM (sub-account <code>' . esc_html( RBR_GHL_LOCATION ) . '</code>).</p>'
		: '<div class="notice notice-warning"><p>CRM non collegato: aggiungi <code>RBR_GHL_TOKEN</code> e <code>RBR_GHL_LOCATION</code> in wp-config.php. Fino ad allora arrivano solo le mail.</p></div>';
	echo '<p>Per inserire un modulo: blocco «Shortcode» con <code>[rbr_modulo tipo="prenotazione"]</code> (tipi: prenotazione, evento, contatto, novita).</p>';
	echo '<form method="post" action="options.php">';
	settings_fields( 'rbr-moduli' );
	$campi = array(
		'email'    => array( 'Email notifiche (separate da virgola)', 'input' ),
		'sedi'     => array( 'Locali (uno per riga; vuoto = locale unico)', 'textarea' ),
		'orari'    => array( 'Orari prenotabili (uno per riga)', 'textarea' ),
		'prefisso' => array( 'Tag fonte nel CRM (default lead-sito-<dominio>)', 'input' ),
		'campi'    => array( 'Campi personalizzati GHL («campo del modulo = chiave GHL», una per riga; campi disponibili: sede_nome, data, ora, persone, compleanno, lingua, pagina, fonte, messaggio)', 'textarea' ),
		'privacy'  => array( 'Indirizzo pagina privacy', 'input' ),
	);
	echo '<table class="form-table">';
	foreach ( $campi as $k => $c ) {
		$v = esc_textarea( (string) rbrm_opt( $k ) );
		echo '<tr><th>' . esc_html( $c[0] ) . '</th><td>' . ( 'textarea' === $c[1]
			? '<textarea name="rbrm_' . esc_attr( $k ) . '" rows="6" class="large-text">' . $v . '</textarea>' // phpcs:ignore
			: '<input name="rbrm_' . esc_attr( $k ) . '" value="' . $v . '" class="regular-text">' ) . '</td></tr>'; // phpcs:ignore
	}
	echo '</table>';
	submit_button();
	echo '</form></div>';
}
