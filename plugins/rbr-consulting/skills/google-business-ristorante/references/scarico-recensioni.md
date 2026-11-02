# Scaricare TUTTE le recensioni Google con data e voto veri (oltre il tetto di 200)

(contributo di Luciano Purpi, 2026-09-03) Serve per misurare cosa dicono davvero i clienti
(quota di testi che citano la promessa di marca, andamento nel tempo, segnali di filtro
anti-sollecitazione). L'analisi completa della reputazione sta nella skill
`analisi-reputazione-locale`: qui c'è solo come si prende il dato.

**Prerequisito**: accesso da gestore alla scheda del cliente (identità team), sessione loggata
nel browser. Si lavora sul profilo del cliente, non su schede di terzi.

## Il problema
Il pannello "Leggi recensioni" del Profilo dell'attività si ferma a 100-200 schede e nel DOM
NON c'è la data assoluta (solo "3 giorni fa", "un mese fa").

## Il metodo (rpc `kAyvCf`)
1. SERP del profilo → pannello "La tua attività su Google" → "Leggi recensioni"
   (`#mpd=~<idProfilo>/customers/reviews`). Il pannello vive in un **iframe same-origin**: si
   legge con `iframe.contentDocument`.
2. Dentro, il bottone "Altre recensioni" fa una POST a
   `/local/business/_/GeoMerchantFrontendEmbeddedUi/data/batchexecute`, rpc **`kAyvCf`**.
3. Agganciare `XMLHttpRequest.prototype.send` nel `contentWindow` dell'iframe, cliccare
   "Altre recensioni" UNA volta per catturare URL + body (contiene il token `at`).
4. Rigiocare la stessa POST cambiando solo il payload interno di `f.req`:
   `[null, 100, "updatetimedesc", <pageToken>, null, null, null, "<idProfilo>", 1]`
   - token della pagina successiva = `payload[1]`; recensioni = `payload[0]`.
5. Indici dell'array recensione: `[0]` id · `[5]` testo · `[8]` timestamp in ms (ordinamento
   monotono decrescente, verificato) · `[19]` voto 1-5. L'autore è il sotto-array che inizia
   con l'id numerico a 21 cifre.

Risultato misurato: 800 recensioni in 8 pagine, fino a due mesi indietro, in circa un minuto.

## Attenzione
- La console del browser pilotato tronca/blocca output con URL o id lunghi → fare tutta
  l'aggregazione DENTRO la pagina e restituire solo numeri; per esportare, generare un Blob
  CSV e scaricarlo (metodo in `diagnosi-suite` → `references/trappole-strumenti.md`, B.2).
- Nomi degli autori = dati personali: servono solo per contare profili ripetuti/nuovi, non
  vanno nei report al cliente.

## Vie che NON funzionano (verificate, non riprovare)
Menu "Ordina → Più recenti" della scheda Maps pubblica; pannello `tbm=lcl`; Maps pubblica
(si ferma a ~40 recensioni); `maps/rpc/listugcposts` (403 senza session token);
`listentitiesreviews` e `/async/reviewDialog` (404).

## Metodo veloce senza login, per verificare l'esito di segnalazioni/risposte
Per un controllo rapido senza accedere al Profilo:
- Su Maps pubblico, le barre del riepilogo voti hanno il conteggio esatto per stella
  nell'`aria-label` (es. "5 stelle, 775 recensioni").
- Su **GHL Reputation** si fa un hook XHR su `/reputation/reviews` e poi un pull completo.
  Parametri: `pageNumber` e `pageSize=100` — **non** `page`/`limit`. Si tolgono i filtri
  `starRating`; `filterParams[deleted][0][value]=true` mostra anche le cancellate. Il mirror
  GHL può contare 1-2 recensioni Google in più del pubblico, tiene Facebook a parte e non
  anticipa Google: va trattato come una stima vicina, non come il dato esatto.
- **Il confronto va fatto PER STELLA, mai sul totale**: solo così si vede se è sparita una
  negativa o una positiva dopo una segnalazione.
- Le risposte non cambiano i voti in modo prevedibile: su un caso, dopo oltre 1.000 risposte,
  a 2 giorni non si era mosso nulla, a 7 giorni un voto senza testo era già cambiato. Si
  ricontrolla **a 48 ore** chi ha cambiato voto — la vecchia risposta resta appesa sotto il
  voto nuovo e va aggiornata.
*(contributo di Andrea Chirivì, con il controllo a 48 ore di Luciano Purpi, 2026-10-12)*
