# Hosting e dominio — cosa compra il cliente e come si lavora sopra

## Cosa compra il cliente (intestato alla SUA società, con la SUA carta)
- **Dominio** `.it` (o `.com` se lavora con turisti esteri), solo registrazione: poche decine di €/anno.
  Se esiste già un dominio intestato a terzi (agenzia, cugino, ex socio) → segnalarlo: va trasferito al
  cliente prima del go-live (caso Raíces: dominio su un account IONOS non del titolare).
- **Hosting WordPress** gestito con: PHP 8.2/8.3, HTTPS Let's Encrypt incluso, almeno 1 casella email sul
  dominio, backup automatici, cache. Va bene Aruba Hosting WordPress/Easy (il più usato dai clienti italiani),
  SiteGround, Hostinger, IONOS. Mai un VPS da gestire.
- Prezzi: verifica il listino del momento e mandalo al cliente prima che compri (regola: stima € prima di
  ogni spesa). Niente servizi aggiuntivi inutili (SEO pack, site builder, «sicurezza premium», email extra).
- Il cliente ti dà accesso così: (1) crea un utente WordPress amministratore col TUO nome/email; oppure
  (2) ti delega l'accesso al pannello hosting. Le credenziali non passano in chat né nei file: canale sicuro
  del team. A fine lavoro l'utente si può revocare senza toccare quello del cliente.

## Aruba (Hosting Easy / WordPress) — trappole vere (Cartabianca, ott 2026)
- Installazione WordPress dal pannello con **Softaculous** (sceglie DB e prefisso). «Accedi come
  amministratore» da Softaculous → Installazioni entra senza password.
- **Niente SSH né WP-CLI**: tutto da wp-admin (zip di tema/plugin, plugin «Avvio» per creare le pagine).
- Su alcuni wp-admin Aruba i POST dei form (caricamento tema/plugin, «Rilancia») rimandano a `about.php` senza
  fare nulla: rifai l'invio dalla console della pagina con `fetch` + `FormData` del form (stessi campi,
  nonce compreso). Aggiornare un tema caricato = link con `overwrite=update-theme`.
- **Aruba HiSpeed Cache** (Impostazioni): attivare cache di pagina + object cache + cache browser → TTFB da
  2-3 s a 0,3 s. Dopo ogni modifica: «Cancella cache». In bozza il tema deve mandare `no-store` (sennò la
  cache serve a tutti le pagine viste in anteprima).
- Cache di pagina con durata < 12 h (il gettone dei moduli vale 12-24 h).
- Pannello admin lento: se una pagina wp-admin non finisce di caricare, `window.stop()` e procedi.
- Email: SMTP `smtps.aruba.it` porta 465 SSL con la casella del dominio (plugin gratuito tipo WP Mail SMTP).
  Senza SMTP le mail di WordPress finiscono in spam o non partono.
- Il pannello hosting si usa solo per installare, DNS, email e cache; **le modifiche al sito si fanno solo da
  wp-admin**.

## DNS e go-live
- Dominio e hosting dallo stesso fornitore: DNS già puntati. Fornitori diversi: record A `@` e `www` →
  IP dell'hosting (o i nameserver dell'hosting) dal pannello del registrar del cliente.
- HTTPS attivo prima di togliere «in costruzione»; *Impostazioni → Generali* con `https://`.
- Redirect 301 da vecchio sito/sottodominio alle pagine nuove equivalenti (non tutto sulla home).
- Mail del dominio: SPF/DKIM/DMARC configurati dal pannello (le mail dei moduli escono dal dominio del cliente).

## Plugin ammessi (gratuiti, del cliente)
TranslatePress (lingue) · un plugin SMTP · un banner cookie (Complianz / CookieYes free o quello dell'hosting) ·
un plugin SEO solo se serve (Yoast/Rank Math free) · cache dell'hosting · WooCommerce solo se vende online ·
`rbr-moduli` (della skill, codice aperto, nessuna licenza). Niente page builder, niente plugin «nulled», niente
abbonamenti a nome RBR. Ogni plugin in più è una cosa che il cliente deve aggiornare.

## Manutenzione dopo la consegna
Aggiornamenti automatici minori di WordPress attivi; backup dell'hosting attivo; il cliente (o il consulente
con l'utente suo) aggiorna plugin una volta al mese. Annotare nella memoria cliente: hosting, versione del
tema, plugin installati, utenti, pendenze.
