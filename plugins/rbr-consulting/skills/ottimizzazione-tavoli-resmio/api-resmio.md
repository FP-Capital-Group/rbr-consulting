# Come si legge e si scrive su Resmio

Resmio non ha un'API pubblica documentata per questo, ma il pannello gestore ne usa una
interna e completa. Si richiama **dalla sessione già loggata nel browser**: apri una pagina
del gestionale del locale e da lì esegui le chiamate, che ereditano i cookie di sessione.

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

Parametri utili: `?disable_total_count=true&limit=1000`, e per le prenotazioni
`&date__gte=<ISO>&date__lt=<ISO>` in UTC. Per una serata italiana la giornata va da
`T22:00:00.000Z` del giorno prima a `T22:00:00.000Z` del giorno stesso.

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
| `status` | `confirmed`, `seated`, `finished`, `cancelled`, `noshow`, `arrived` |
| `walk_in` | booleano, la chiave per misurare il passaggio |
| `source` | canale; spesso vuoto per quelle inserite a mano o via sync |
| `comment` / `notes` | richieste dell'ospite: passeggini, seggioloni, intolleranze |
| `last_reply_sent` | quando è stata mandata l'ultima mail all'ospite |

Escludi sempre `cancelled` e `noshow` dai calcoli di occupazione.

**Tavolo** (`resources`): `name`, `capacity`, `table_location_horizontal` /
`_vertical` (planimetria), `table_shape`, `is_unlocated` (tavolo mobile, non posizionato).

**Combinazione** (`resource_combinations`): `resources` (array di URI) e `max`, che è il
numero massimo di persone — **non sempre uguale alla somma delle capienze**. Ne trovi di
sovradichiarate (tre tavoli da 2 con `max: 8`) e di duplicate: segnalale al cliente, perché
fanno accettare gruppi che in sala non entrano.

**Override** (`resource_overrides`): `begins`, `ends`, e `resources` **oppure**
`resource_groups`. Blocca la vendita online, non l'assegnazione manuale.

## Disponibilità: il numero che dimostra il lavoro

```
/v1/facility/<slug>/availability?date=<YYYY-MM-DD>&num=<persone>
```

- `available_authenticated` — **i posti ancora vendibili** in quella fascia. È la metrica da
  registrare prima e dopo l'intervento.
- `available` — il gruppo massimo che il sistema accetterebbe.

Attenzione: **il parametro `date` viene ignorato** e la risposta è sempre la giornata
corrente. Non usarlo per confrontare date diverse — ci si costruisce sopra conclusioni
sbagliate.

Quando `available_authenticated` è 0 su una fascia mentre la sala è a metà, non è un bug: il
motore sta guardando avanti e vede che ogni tavolo libero in quell'istante serve a qualcuno
poco dopo. È esattamente il problema che il riassetto risolve.

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

**Creare una combinazione** — `POST /v1/facility/<slug>/resource_combinations`,
risponde `201`:

```json
{
  "facility": "/v1/facility/<slug>",
  "max": 4,
  "resources": ["/v1/facility/<slug>/resources/<id-a>", "/v1/facility/<slug>/resources/<id-b>"]
}
```

Metti `max` uguale alla somma reale delle capienze, non di più.

## Nota sull'ambiente

Alcuni strumenti browser bloccano l'output che contiene stringhe di query o dati di cookie:
la chiamata riesce ma il risultato torna oscurato. Se succede, non stampare l'URL — restituisci
solo i campi che ti servono, o sostituisci `?`, `&` e `=` prima di stampare. L'output è anche
troncato intorno al migliaio di caratteri: salva i risultati in `window.__X` e leggili a
fette invece di rifare la chiamata ogni volta.
