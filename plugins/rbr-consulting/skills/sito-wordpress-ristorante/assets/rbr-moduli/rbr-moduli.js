/* RBR Moduli: invio senza ricaricare la pagina + provenienza (utm_source o sito di provenienza). */
( function () {
	var C = window.rbrModuli || {};
	document.querySelectorAll( 'form[data-rbrm]' ).forEach( function ( f ) {
		var fonte = f.querySelector( '[name="fonte"]' );
		try {
			var q = new URLSearchParams( location.search );
			fonte.value = q.get( 'utm_source' ) || q.get( 'utm' ) || ( document.referrer && document.referrer.indexOf( location.host ) < 0 ? new URL( document.referrer ).hostname : 'diretto' );
		} catch ( e ) {}
		f.querySelector( '[name="pagina"]' ).value = location.pathname;
		var esito = f.querySelector( '.rbrm-esito' );
		var bott = f.querySelector( 'button[type="submit"]' );
		f.addEventListener( 'submit', function ( ev ) {
			ev.preventDefault();
			f.querySelectorAll( '.rbrm-errore' ).forEach( function ( x ) { x.classList.remove( 'rbrm-errore' ); } );
			if ( ! f.checkValidity() ) {
				f.querySelectorAll( ':invalid' ).forEach( function ( x ) { var p = x.closest( 'p' ); if ( p ) { p.classList.add( 'rbrm-errore' ); } } );
				esito.textContent = C.campi;
				return;
			}
			var dati = {};
			new FormData( f ).forEach( function ( v, k ) { dati[ k ] = v; } );
			bott.disabled = true;
			esito.textContent = C.attesa;
			fetch( C.url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify( dati ), credentials: 'omit' } )
				.then( function ( r ) { return r.json(); } )
				.then( function ( j ) {
					esito.textContent = j.messaggio || C.errore;
					( j.campi || [] ).forEach( function ( n ) { var x = f.querySelector( '[name="' + n + '"]' ); if ( x && x.closest( 'p' ) ) { x.closest( 'p' ).classList.add( 'rbrm-errore' ); } } );
					if ( j.ok ) {
						f.reset();
						f.querySelectorAll( 'p, .wp-block-button' ).forEach( function ( p ) { if ( ! p.classList.contains( 'rbrm-esito' ) ) { p.hidden = true; } } );
						window.dataLayer && window.dataLayer.push( { event: 'rbr_modulo_inviato', tipo: dati.tipo } );
						typeof window.fbq === 'function' && window.fbq( 'track', 'prenotazione' === dati.tipo ? 'Schedule' : 'Lead' );
					}
				} )
				.catch( function () { esito.textContent = C.errore; } )
				.then( function () { bott.disabled = false; } );
		} );
	} );
}() );
