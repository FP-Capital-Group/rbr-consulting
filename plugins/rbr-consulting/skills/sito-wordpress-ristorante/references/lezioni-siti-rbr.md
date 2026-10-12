# Lezioni dai siti fatti (2026) — regole nate da errori veri

Siti di riferimento: Cartabianca bar + Ristoranti (WordPress Aruba, modello di questa skill), Raíces (WordPress
di un'agenzia, via MCP), Red Mike, Osteria Ca' di Pieri, Trattoria Griss, Zio Bibi (siti statici del vecchio
metodo su server di Marco — **metodo dismesso per i clienti**), Mister Pizza / Dirigì / Barresi (WordPress esistenti).

## Design e UX
- Colori dal brand reale, contrasto ≥ 4,5:1. Senza identità: toni caldi; vietati rosa pallido, blu, azzurro,
  viola, grigio freddo. Beige = crema/sabbia (`#F5EFE0`).
- Hero: foto vera e calda dell'ambiente/piatto. Foto Google mediocre (mani, primi piani, sfocata) → meglio un
  blocco a tinta unita col nome o un gradiente del brand. Stock solo come atmosfera, mai «il nostro piatto»
  (errore: bistecca stock sulla landing carne di Red Mike).
- Foto originali ≥ 1600 px, caricate in webp; card ≥ 400 px; testata solo con foto ≥ 1200 px.
- Menu: foto di categoria coerente (sotto «Primi» un primo) o nessuna; prezzi piccoli nel font della
  descrizione, mai in rosso, senza «€» e «,00»; ordine del menu stampato; nota allergeni (Reg. UE 1169/2011)
  + coperto.
- Header: una sola nav, max 2 bottoni (con 3 si rompe tra 1024 e 1280 px); in flusso, hamburger < 1100 px.
- Niente emoji nei bottoni né bandiere (su Windows diventano «IT», «GB»): icone SVG e sigle.
- Sezione prenota su sfondo liscio, mai una foto dietro al modulo.
- Mobile: campi ≥ 48 px, input data sistemati per iOS, niente `loading=lazy` sopra la piega, niente animazioni
  d'ingresso, barra fissa «Chiama | Prenota».

## Contenuti e copy
- **Mai recensioni inventate** (29 siti su 39 del vecchio generatore ne avevano: tutte tolte). Solo «4,6 su 261
  recensioni Google» con link. Recensioni citate devono parlare del locale di oggi (tolta quella «paninoteca»).
- H1 = prodotto + città («Torte, pasticceria e caffè a Firenze e Prato»), non lo slogan; niente cucina
  regionale dedotta da «trattoria/osteria» (un sito di Lodi titolava «cucina romana»).
- Claim solo se confermati: «griglia» non «brace», mai «forno a legna» o «fatto in casa» senza conferma.
- Da far confermare per iscritto: prezzi, orari (quelli di Google spesso sono vecchi: usa cassa/cliente),
  volumi di vendita pubblici, premi (verifica la fonte: il premio Repubblica era del 2017, non del 2025), date
  stagionali, gruppi di locali, premi fidelity.
- Fidelity/club: premi = regali, mai sconti. Niente leve «prezzo basso / porzioni XL / consegna gratis».
- Niente disclaimer «sito dimostrativo», niente dati interni o numeri che il cliente non vuole pubblici.

## Prenotazioni
- TheFork: widget **senza commissione** (TheFork Manager → Marketing → Widget → «Incorporalo nel sito»); le
  prenotazioni da thefork.it la pagano. Un widget per locale. Lo stesso URL va come link «preferito» nella
  scheda Google (modificandolo il flag preferito si perde: rimetterlo).
- TheFork ha l'antibot DataDome: niente test automatici sul widget.
- Resmio: `source` nell'URL dell'iframe e `?utm=` (solo le chiavi `utm` e `gclid` arrivano in
  `booking_request_parameters`), `referrerpolicy="no-referrer-when-downgrade"` sull'iframe, skeleton trasparente.
- Sempre il piano B sotto il widget: «Chiama» + «Preferisci essere richiamato?».
- Locali stagionali: fuori stagione avviso e niente prenotazione.
- Locale piccolo senza gestionale: modulo `prenotazione` come «richiesta», conferma a mano dallo staff (workflow GHL).

## CRM e moduli
- Lead sempre nel sub-account GHL del cliente, con tag `form-<tipo>` e fonte; consenso marketing mai pre-spuntato.
- Token del cliente solo in `wp-config.php`. Mai in database, repository, chat.
- Workflow: avvisi allo staff = *Internal Notification*; niente SMS se il sub-account non ha il numero; test con
  `@rbr-test.local` e cancellazione.
- Sul sito solo chat testuale (Conversation AI) se presidiata; niente assistente vocale sul sito.

## Tracciamento e cookie
- Placeholder dimenticato: Red Mike ha avuto `PIXEL_ID` letterale online per 2 mesi, zero eventi. Verifica sempre
  con l'ID reale.
- Tag sotto il banner cookie (bloccati fino al consenso); privacy/cookie policy aggiornate quando aggiungi
  pixel, statistiche o mappe; banner e testi cookie tradotti anche in `/en/`.
- Blur-trick sul widget = primo clic, non prenotazione: solo micro-conversione.
- Script rifiutati dal connettore MCP di un WordPress → `wp.apiFetch` sulla template-part del footer dalla
  sessione admin (dettagli in `sito-wordpress-cliente-mcp`).

## SEO
- Pagina per ogni locale + pagina del piatto firma; title ≤ 60 caratteri (col suffisso!), una H1, FAQ.
- JSON-LD Organization + Restaurant (o Bakery/Cafe) per locale.
- Noindex durante la costruzione e tolto al go-live: un noindex dimenticato ha tenuto fuori da Google la home di
  Red Mike per mesi. Landing promo/QR restano noindex.
- Inglese scritto (TranslatePress), mai Google Translate.

## Costi
- Places/Maps chiamate dal browser: addebiti a ogni visita (tolte da 42 siti il 01/09/2026). Mappa con iframe
  embed gratuito; stelle/recensioni scritte statiche e aggiornate a mano.
- Prima di ogni spesa (plugin, API, dominio, crediti AI) stima € e ok.

## Hosting
- Mai sul server di Marco: un `dnf` sul VPS condiviso ha bloccato tutti i siti clienti per 35 minuti (07/10/2026).
- Dopo la consegna si modifica solo da wp-admin, non da pannelli paralleli o copie locali.
- Prima di sovrascrivere qualcosa sul sito vivo: backup (l'hosting lo fa; altrimenti esporta).
