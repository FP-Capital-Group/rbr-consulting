# Il prenotatore — sempre in evidenza, sempre funzionante

Il sito di un ristorante esiste per riempire tavoli. Il prenotatore è il pezzo più importante: si progetta per primo
e si collauda per ultimo.

## Dove va (tutti questi punti, su ogni sito)
1. **Header**: bottone pieno «Prenota» sempre visibile (sticky) → `/prenota/` o `#prenota` della pagina.
2. **Home, subito dopo la copertina**: sezione `#prenota` col widget vero (non solo un bottone). A schede se ci sono
   più locali (Cartabianca, Raíces).
3. **Barra fissa in basso su mobile**: «Chiama | Prenota».
4. **Ogni pagina locale**: prenotatore di quel locale nella testata (bottone) e in pagina (`#prenota`).
5. **Fine pagina menu, eventi, chi siamo**: «Ti è venuta fame? Prenota» con bottone.
6. **Pagina `/prenota/`** con tutti i locali e le ancore `#<locale>`; versioni `/prenota/<locale>/` se servono per
   le campagne (stessa pagina, URL parlante).
7. **Fuori dal sito**: scheda Google (link prenotazione preferito), Instagram/Facebook (bottone Prenota), firma mail,
   QR in sala → stesso widget.
Mai coprire il prenotatore con pop-up, chat o banner (il fumetto della chat su mobile copriva il widget Cartabianca:
spostarlo o nasconderlo sulle pagine prenota).

## Quale strumento
| Situazione | Prenotatore | Note |
|---|---|---|
| Il locale usa TheFork | **widget TheFork senza commissione** | TheFork Manager → Marketing → Widget → «Incorporalo nel sito» → URL `https://widget.thefork.com/<uuid>` (uno per locale). Le prenotazioni dal widget non pagano commissione; quelle da thefork.it sì |
| Il locale usa Resmio | iframe/widget Resmio | `https://app.resmio.com/<slug>/widget?source=sito`; `referrerpolicy="no-referrer-when-downgrade"` sull'iframe; pagine e link marcati `?utm=<pagina>-<canale>` (solo `utm` e `gclid` arrivano in `booking_request_parameters`) — dettagli `sito-landing-ristorante` A5-A6 |
| Altro gestionale (Plateform, Quandoo, CoverManager…) | il loro widget, stesse regole | verifica che funzioni con cookie rifiutati |
| Nessun gestionale, locale piccolo | modulo `[rbr_modulo tipo="prenotazione"]` = **richiesta** | il cliente riceve «ti richiamiamo per confermare», lo staff conferma a mano (workflow GHL). Mai scrivere «prenotazione confermata» se non lo è |
Non cambiare gestionale al cliente per fare il sito: si usa quello che usa la sala.

## Come si incorpora (WordPress)
- Blocco **HTML personalizzato** chiamato «Widget <gestionale> <locale> – non modificare» (è l'unico blocco HTML
  ammesso nel sito: il cliente sa che non va toccato):
  ```html
  <iframe src="https://widget.thefork.com/<uuid>" title="Prenota un tavolo da <Locale>" allow="payment *"
    style="width:100%;min-height:800px;border:none" loading="lazy"></iframe>
  ```
- Versione inglese: `https://widget.thefork.com/en/<uuid>` (il tema la sostituisce da solo in `/en/`, vedi
  `tema-a-blocchi.md`).
- Più locali in home: schede solo CSS (radio + label + iframe), la scheda attiva in colore di marca; sotto ogni scheda
  il nome e la via del locale.
- In home l'iframe può avere `loading="lazy"` solo se NON è nella prima schermata.
- «Offerto da TheFork» è dentro l'iframe: non si toglie, non perderci tempo.
- Locale stagionale chiuso: niente widget, riquadro «Riapre a <mese>» + modulo novità per avvisare alla riapertura.

## Testi intorno al prenotatore
- Titolo: «Prenota il tuo tavolo» (+ « · <Locale>» nelle pagine locale). EN «Book your table».
- Sopra: «Preferisci chiamare? <telefono cliccabile>».
- Sotto: «Siete più di <N> o organizzate una festa?» → `/eventi/`; «Preferisci essere richiamato?» → modulo `contatto`
  o `prenotazione` (richiesta) con il locale già scelto.
- Niente urgenze finte («ultimi 2 tavoli!»), niente codici sconto obbligatori per prenotare.

## Tracciamento del prenotatore
- Il clic dentro l'iframe NON è una prenotazione (il «blur-trick» conta il primo tocco): al massimo micro-conversione
  secondaria. Conversione primaria = prenotazione onorata importata dal gestionale (`google-ads-conversione-controllo`,
  `sistema-tracciamento-locale`).
- Eventi utili lato sito (dopo il consenso): clic su «Prenota» (bottoni verso il widget), clic `tel:`, invio modulo
  (il plugin manda `Schedule`/`Lead` al Pixel e `rbr_modulo_inviato` al dataLayer).
- Scheda Google: link prenotazione = **stesso URL del widget** come «preferito» (modificandolo il flag si perde:
  rimetterlo da *Prenotazioni → preferito*). Mai la pagina thefork.it (commissione) né il sito generico.

## Collaudo
- Apri ogni widget a mano UNA volta (desktop + telefono, IT + EN, con cookie rifiutati): si vede il nome giusto del
  locale, si arriva fino alla scelta dell'orario. Non completare prenotazioni finte su TheFork/Resmio senza
  accordo col locale (se serve una prova vera: avvisa la sala e cancellala subito).
- ⚠️ TheFork ha un antibot (DataDome): **niente test automatici sul widget** (Playwright, crawler, decine di
  ricariche): poi chiede «non sei un robot» anche ai clienti veri della stessa rete.
- Controlla che header, home, barra mobile e pagine locale portino tutti al widget giusto (crawl dei link `#prenota`
  e `/prenota/`).
