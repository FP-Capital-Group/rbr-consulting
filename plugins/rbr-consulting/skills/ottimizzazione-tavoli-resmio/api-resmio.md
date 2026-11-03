# Come si legge e si scrive su Resmio

Resmio non ha un'API pubblica documentata per questo, ma il pannello gestore ne usa una
interna e completa. Due vie per chiamarla:

1. **Sessione browser** (sotto): cookie di sessione + token CSRF, serve Chrome loggato.
2. **Chiave API del locale** (vedi "Seconda via" più sotto, prima di "Scrivere"): header
   `Api-Key: <chiave>`, nessun CSRF, via curl/script, anche in parallelo. Disponibile solo sui
   piani con `api_key_enabled`.

Per leggere basta la sessione browser; per scrivere in automatico (import, bot, giri a
ciclo) la chiave API è la via giusta. Apri una pagina del gestionale del locale e da lì
esegui le chiamate, che ereditano i cookie di sessione.

```
https://app.resmio.com/<slug-locale>/bookings/timeline
```

Lo `<slug-locale>` è nell'URL del pannello ed è la chiave di tutto (per Dirigì Jesolo:
`dirigi-jesolo`). Da lì in poi ogni endpoint è `/v1/facility/<slug>/...`.

## Endpoint

Tutti in lettura con `GET` e `Accept: application/json`.

| Endpoint | Cosa dà |
|---|---|
| `/v1/facility/<slug>/` | configurazione: orari, durate, tetti, meal times |
| `/v1/facility/<slug>/resources` | i tavoli: nome, capienza, posizione, forma |
| `/v1/facility/<slug>/resource_groups` | le sale, con l'elenco dei tavoli che contengono |
| `/v1/facility/<slug>/resource_combinations` | gli accostamenti validati, con il `max` di persone |
| `/v1/facility/<slug>/resource_overrides` | blocchi a tempo su tavoli o intere sale |
| `/v1/facility/<slug>/booking_timespans` | **le durate per numero di coperti** |
| `/v1/facility/<slug>/bookings` | le prenotazioni |
| `/v1/facility/<slug>/availability` | quanto Resmio considera ancora vendibile |
| `/v1/facility/<slug>/waitlist` | lista d'attesa |

`booking_timespans` è la fonte autorevole delle durate: oggetti `{num, booking_timespan}` che
funzionano a scalini — per una tavolata usi la soglia `num` più grande che sia ≤ ai coperti.
Sono diverse per ogni locale e vanno rilette ogni volta: non assumere mai i valori di un altro
cliente. Usa queste durate sia per gli incastri sia come `booking_timespan` se crei
prenotazioni.

**`booking_timespan` si copia dalla tabella alla nascita della prenotazione, ma resta un
campo della SINGOLA prenotazione**, modificabile con `PATCH`. Due usi pratici:
- **Serate con musica/evento** (la gente resta più a lungo del turno standard): un tavolo = una
  prenotazione per tutta la sera. Resmio altrimenti rivende il tavolo allo scadere della
  durata standard e ricrea doppi turni. Rimedi: giro di correzione nel pomeriggio (allungare
  `booking_timespan` fino a fine serata sulle prenotazioni di quella sera) e sola lettura
  vicino al servizio; oppure un override sul tavolo. Negli altri giorni i doppi turni possono
  essere voluti.
- **Prenotazione "a tempo"**: `PATCH` con `status: unconfirmed` + `booking_timespan: 90` +
  un'etichetta tipo "Fino alle…". Il tavolo resta tenuto e poi torna in vendita da solo; si
  riconferma con `status: confirmed`. Non esiste un'impostazione per giorno o fascia: va fatto
  prenotazione per prenotazione.
*(contributo di Andrea Chirivì, 2026-10-12)*

Parametri utili: `?disable_total_count=true&limit=1000`, e per le prenotazioni
`&date__gte=<ISO>&date__lt=<ISO>` in UTC. Per una serata italiana con l'**ora legale** la
giornata va da `T22:00:00.000Z` del giorno prima a `T22:00:00.000Z` del giorno stesso; con
l'**ora solare** (dal 25/10/2026) lo scarto cambia a `T23:00:00.000Z` → `T23:00:00.000Z`. Un
offset fisso (es. sempre +2) sbaglia di un'ora tutte le date appena cambia l'ora legale: va
calcolato col fuso **Europe/Rome**, non con un offset hardcoded. Vale anche per gli override
a finestra e per l'inizio dei blocchi ricorrenti in UTC. Il `mealDate` del GraphQL TheFork è
già in UTC e si passa così com'è. *(contributo di Andrea Chirivì, 2026-10-12 — urgente per il
cambio d'ora del 25/10/2026; corregge un'indicazione di Luciano Purpi)*

Se non ricordi la forma esatta di una chiamata, aprila dal pannello e leggi
`performance.getEntriesByType('resource')`: le richieste vere dell'app sono lì con i loro
parametri.

## I campi che contano

**Prenotazione** (`bookings`)

| Campo | Nota |
|---|---|
| `date` | inizio, in UTC |
| `booking_timespan` | durata **in minuti** — non secondi, ci si casca |
| `num` | numero di persone |
| `facility_resources` | array di URI dei tavoli assegnati; vuoto = senza tavolo |
| `status` | `confirmed`, `seated`, `finished`, `cancelled`, `noshow`, `arrived`, **`unconfirmed`** (nasce così dal widget pubblico o dalle prenotazioni a tempo) |
| `walk_in` | booleano, la chiave per misurare il passaggio |
| `source` | canale; spesso vuoto per quelle inserite a mano o via sync |
| `comment` | nota dell'**OSPITE** (quella visibile in lista): passeggini, seggioloni, intolleranze |
| `notes` | nota dello **STAFF** — campo diverso da `comment`, non la stessa cosa |
| `last_reply_sent` | quando è stata mandata l'ultima mail all'ospite |

Escludi sempre `cancelled` e `noshow` dai calcoli di occupazione.

**Tavolo** (`resources`): `name`, `capacity`, `priority` (più alta = scelta prima
dall'assegnazione automatica, ma conta solo a parità di capienza — vedi `trappole.md`),
`table_location_horizontal` / `_vertical` (planimetria), `table_shape`, `is_unlocated`
(tavolo mobile, non posizionato).

**Combinazione** (`resource_combinations`): `resources` (array di URI) e `max`, che è il
numero massimo di persone. Il default prudente resta la somma delle capienze, ma **calcolata
sui minimi** — Resmio ha un solo campo `capacity` col massimo del tavolo, quindi sommando i
massimi la catena arriva a tavolate sovradimensionate. **Il valore finale lo decide il
cliente** (es. somma + 2 posti per l'accostamento, posti veri dove richiesto): non è un dato
che si calcola da solo. Ne trovi anche di sovradichiarate (tre tavoli da 2 con `max: 8`) e di
duplicate: segnalale al cliente, perché fanno accettare gruppi che in sala non entrano.
*(sezione comment/notes e priority: contributo di Andrea Chirivì, 2026-10-12; max delle
combinazioni corregge un'indicazione precedente di Luciano Purpi)*

### Trappole di campo

- `num` = coperti e `facility_resources` = tavoli nelle prenotazioni; negli override il campo
  è `resources`; la capienza è `capacity` (niente min/max seats).
- Gli id delle risorse arrivano **interi**, quelli estratti dagli URI **stringhe**: confrontali
  sempre come stringhe, altrimenti la piantina sembra vuota.
- `facility_resource_names` nella lista è sempre `[]` e il `PATCH` risponde `202` senza nomi:
  verifica con una `GET`.
- Nomi di tavolo **duplicati fra sale** (es. "1-20" in due sale diverse): il nome si risolve
  **dentro la sala** (`resource_groups`), mai con un dizionario nome→uri su tutti i `resources`.
- Fila = `Math.floor(table_location_horizontal)`, posizione = `Math.floor(vertical)`: con
  `round` i `.5` finiscono nella colonna sbagliata.
- `table_shape` è inaffidabile (marca "round" quasi tutto): quali tavoli sono tondi e non si
  accostano lo dice il titolare, non il campo.
- La piantina è su `<canvas>`: si legge dall'API, non dallo screenshot.
- Dopo una scrittura via API l'interfaccia mostra i valori vecchi finché non si fa un
  `location.reload()` vero — non vuol dire che la scrittura sia fallita. L'interfaccia
  riordina i tavoli a ogni clic: i lotti si fanno via API.
- Nel `POST` di un override `resource_groups` va passato **anche vuoto**, altrimenti `400`.
*(contributo di Andrea Chirivì, 2026-10-12)*

**Override** (`resource_overrides`): `begins`, `ends`, e `resources` **oppure**
`resource_groups`. Blocca la vendita online, non l'assegnazione manuale.

## Disponibilità: il numero che dimostra il lavoro

La chiamata che usa il widget è:

```
/v1/facility/<slug>/availability?num=<persone>&date__gte=<AAAA-M-G>&resource_group=&end_of_acceptance_enabled=true
```

(mese e giorno **senza zero iniziale**). Restituisce `objects[]` per quarto d'ora, con data in
UTC. Il parametro `date` resta ignorato — per una data futura diversa da oggi l'unica via
affidabile è `date__gte` di questa chiamata widget, non una `date` sulla vecchia forma.

- `available_authenticated` — **i posti residui veri**. È la metrica da registrare prima e
  dopo l'intervento.
- `available` — ciò che vede il **widget pubblico**: `0` = pieno, **mai sopra `max_num`**,
  tiene conto di tetto per fascia e abbinamenti configurati. Non è "il gruppo massimo
  accettato": è un numero di posti, calcolato dal motore di vendita online.
- `max_num` (per locale, es. 20), `booking_interval` e la capacità per fascia stanno in
  `GET /v1/facility/<slug>/`. Un abbinamento oltre `max_num` **non si vende mai online**: si
  prende solo a mano.

**Occhio all'overbooking silenzioso**: col turno unico, `availability` può dichiarare posti
disponibili anche con **tutti i tavoli fisicamente occupati** (caso reale: 51 tavoli su 51
occupati e ancora 26 coperti "disponibili" 23:00-23:45). Il pieno vero si conta a parte:
tavoli distinti occupati da prenotazioni attive contro i tavoli vendibili (totale meno
override attivi) — mai fidarsi solo di `available`/`available_authenticated` per dire "la
sala è piena".
*(contributo di Andrea Chirivì, 2026-10-12 — corregge e completa un'indicazione precedente di
Luciano Purpi)*

## Seconda via di accesso: la chiave API del locale

Sui piani con `api_key_enabled` si legge e scrive su `api.resmio.com` con la chiave del
locale, senza sessione browser né CSRF:

```
Api-Key: <chiave>
```

- Con `Token`, `Bearer` o la chiave come parametro in query si ottiene **401**.
- Con `Authorization:` le liste rispondono **200 ma vuote**: sembra funzionare e non funziona.
- Il nome esatto dell'header, se serve riconfermarlo, si legge da `access-control-allow-headers`
  della risposta 401.

Con questa chiave `POST`/`PATCH` di `bookings`, `resources` e `resource_overrides` danno
`201`/`202` **senza cookie né `X-CSRFToken`**: niente Chrome, giri automatici possibili e
anche in parallelo (8 thread testati senza errori). Si usa per import da altri canali, bot,
scritture di configurazione in blocco (vedi fondo pagina). La chiave si legge da file al
momento dell'uso e **non si stampa mai** in chat o nei log. Da script si usa **curl**: Python
`urllib` resta appeso senza errore sui `POST` Resmio (vedi anche `diagnosi-suite` sui timeout).
*(contributo di Andrea Chirivì, 2026-10-12)*

### Parametri utili (liste, storico, giorno di servizio)

- **Liste vuote sospette**: con la sessione scaduta o l'header sbagliato le liste rispondono
  `200` con `total_count: 0`, mentre le risorse singole danno `401`. Prima di dichiarare
  riuscito un giro, o prima di reimportare, sonda una prenotazione nota per id: una lista
  vuota inattesa è sospetta (rischio di reimport in doppio).
- **Storico**: `bookings` senza filtri restituisce circa 1 mese indietro più il futuro. Anche
  con `date__gte` e Api-Key lo storico oltre ~30 giorni indietro **non è garantito** —
  controlla sempre la data minima del set restituito prima di fidartene.
- Campi utili per lo storico cliente: `customer_bookings` e `customer_noshows`.
- **Giorno di servizio**: il taglio è alle **06:00 ora di Roma** (non mezzanotte).

## Scrivere

Serve il token CSRF dal cookie di sessione:

```js
const csrf = document.cookie.split('; ')
  .find(c => c.startsWith('csrftoken='))?.split('=')[1];
```

e va passato come header `X-CSRFToken` con `credentials: 'same-origin'`.

**Spostare una prenotazione** — `PATCH /v1/facility/<slug>/bookings/<id>`, risponde `202`:

```json
{ "facility_resources": ["/v1/facility/<slug>/resources/<id>", "..."] }
```

Per una tavolata su due tavoli uniti si passano entrambi gli URI. Fra un PATCH e l'altro
lascia un attimo di respiro (~200 ms) e rileggi la serata alla fine per verificare davvero.

### Annullare una prenotazione via API: a differenza dello spostamento, può mandare una mail

`PATCH {"status":"cancelled"}` **fa partire la mail di annullamento di Resmio se la
prenotazione ha l'`email`**. A differenza del `PATCH` sui tavoli (che non manda mail, vedi
`trappole.md`), annullare NON è sempre silenzioso. Prima di ogni annullo via API (doppioni,
disdette da altri canali da riportare su Resmio, prenotazioni di prova) **leggi `email`**: se
c'è e il cliente non deve ricevere nulla, fermati e chiedi, oppure usa il metodo silenzioso
sotto. Dopo il primo annullo di un giro rileggi `last_reply_sent`, come per gli spostamenti.
*(contributo di Andrea Chirivì, 2026-10-12 — nessuna PATCH sui tavoli copriva questo caso)*

**Annullare un doppione senza avvisare il cliente** — solo su un doppione vero (stesso
telefono e stessa data, create a pochi minuti l'una dall'altra; mai su una tavolata grande
divisa su due tavoli con lo stesso nome) e mai oltre l'ora limite concordata col locale salvo
richiesta esplicita del titolare:
1. Rileggi il doppione e guarda `email`. Se c'è, Resmio manderà comunque la sua mail di
   annullamento: fermati e chiedi prima di procedere.
2. `PATCH /bookings/<id>` con `{"phone":""}` più una nota sul doppione (campo `comment` o
   `notes` secondo il caso, vedi sopra).
3. `PATCH {"status":"cancelled"}`.
4. Rileggi: la prenotazione tenuta è ancora `confirmed` col telefono, non è partito nessun
   WhatsApp verso l'ospite.
Funziona perché i ponti verso il CRM cercano il contatto per telefono: togliendolo, l'avviso
di annullo non trova a chi mandarlo. **Confermato su un solo cliente**: su un locale nuovo si
prova prima su una prenotazione di test e si controlla ogni ponte attivo verso il CRM, perché
un ponte di terzi può comportarsi diversamente. Togliere anche `email` (`PATCH {"email":""}`)
per bloccare anche la mail di Resmio non è mai stato provato: finché non è verificato, con
l'email presente ci si ferma e si chiede.
*(contributo di Andrea Chirivì, 2026-10-12, un solo caso verificato)*

### Inserire prenotazioni nuove: due vie diverse, non intercambiabili

- **POST con Api-Key su `api.resmio.com/.../bookings`**: dà `201`, **non** manda mail
  all'ospite. **Non** assegna il tavolo e **non** controlla tetto né tavoli (una fascia da 36
  è arrivata a 37 senza errore). È la via giusta per gli **import da altri canali**: `status`,
  `tags`, `facility_resources` e `comment` li scegliamo noi.
- **POST pubblico del widget su `app.resmio.com/.../bookings`**, senza chiave: serve telefono
  in formato E.164 valido (altrimenti 400) e `User-Agent` da browser. Dà `201` e assegna il
  tavolo in automatico. Però non controlla la disponibilità (accetta anche fuori orario), crea
  la prenotazione **`unconfirmed`** (va confermata con `PATCH status:confirmed` e Api-Key), non
  prende i `tags`, può mandare in una sala non voluta e **notifica il locale a ogni
  inserimento**. Va bene per un bot guidato dal cliente (flusso: `availability` → slot con
  `available>0` → POST pubblico). **Mai per gli import**, che devono usare la via con Api-Key.

**Scelta del tavolo quando lo decidiamo noi** (import, assegnazione manuale): il più piccolo
con `capacity ≥ coperti`, senza override attivi e senza sovrapposizioni nella finestra di
`booking_timespan` (almeno 90'). Si ordina per capienza e poi per numero — **non** per
`priority`, che manda su tavoli lontani. Si rispetta l'ordine delle sale voluto dal cliente. I
tavoli già scelti nello stesso lotto si segnano (altrimenti due import della stessa sera
prendono lo stesso tavolo). I tavoli bloccati o dismessi si escludono a mano. I gruppi molto
grandi restano senza tavolo e li assegna la sala.
*(contributo di Andrea Chirivì, 2026-10-12)*

**Creare una combinazione** — `POST /v1/facility/<slug>/resource_combinations`,
risponde `201`:

```json
{
  "facility": "/v1/facility/<slug>",
  "max": 4,
  "resources": ["/v1/facility/<slug>/resources/<id-a>", "/v1/facility/<slug>/resources/<id-b>"]
}
```

Il `max` lo decide il cliente (vedi sopra, "I campi che contano" → Combinazione): la somma
reale delle capienze minime resta il default prudente, non un tetto fisso da non superare.
Con una regola del cliente (es. "solo tavoli sulla stessa fila con numeri consecutivi") ogni
sequenza continua è un abbinamento (1+2, 1+2+3, 2+3…). Quando cambiano capienze o formazione
della sala, gli abbinamenti vanno ricalcolati prima che l'online riapra.
*(contributo di Andrea Chirivì, 2026-10-12)*

## Chiudere l'online: una fascia, una serata, una stagione

Sempre su decisione del titolare, mai di iniziativa propria.

- **Una fascia** (es. le 22:00 sature): override sui gruppi-sala vendibili con finestra di 15
  minuti sull'inizio della fascia, in UTC (20:00Z-20:15Z = le 22:00 con l'ora legale, vedi
  sopra per l'ora solare). `/availability` va a 0 solo lì, le fasce dopo restano aperte. Scade
  da sola, non tocca tavoli né prenotazioni esistenti.
- **Una serata intera**: non esiste un endpoint per il tetto coperti (`capacities` e
  `booking_limits` danno 404). Si fa un `PATCH` del facility su `min_book_in_advance_minutes`
  (es. 300 = 5 ore di anticipo), da rimettere a 0 la mattina dopo. **Mai** un override
  sull'intera sala per questo scopo.
- **Una stagione**: non si usa `booking_enabled` (comportamento non chiaro: una fonte dice che
  spegne tutti i giorni, un'altra che è di sola lettura — da verificare, nel dubbio non
  usarlo). Si va in Impostazioni › Prenotazioni › Eccezioni e promozioni › Vacanze ed eccezioni
  › Aggiungi eccezione (Chiuso, tutto il giorno, intervallo date, testo per il widget). Riapre
  da sola a fine intervallo. Verifica sempre sul widget una data dentro e una dopo l'intervallo,
  e che le prenotazioni future in quelle date siano zero.
*(contributo di Andrea Chirivì, 2026-10-12)*

## Nota sull'ambiente

Alcuni strumenti browser bloccano l'output che contiene stringhe di query o dati di cookie:
la chiamata riesce ma il risultato torna oscurato. Se succede, non stampare l'URL — restituisci
solo i campi che ti servono, o sostituisci `?`, `&` e `=` prima di stampare. L'output è anche
troncato intorno al migliaio di caratteri: salva i risultati in `window.__X` e leggili a
fette invece di rifare la chiamata ogni volta.

## Scritture di configurazione in blocco (override, abbinamenti, risorse)

La regola delle ~200 ms fra un `PATCH` e l'altro vale per le prenotazioni vere. Per decine di
scritture di configurazione cambia: dalla console del browser, in sequenza, il tab va in
timeout dopo ~45 s e lascia il lavoro a metà. Si lanciano in parallelo con `Promise.all`,
oppure dal server con la chiave Api-Key (8 thread testati senza problemi). Prima si fa il
backup JSON delle definizioni che si stanno per toccare (es. gli override da cancellare).
*(contributo di Andrea Chirivì, 2026-10-12)*
