# Come si estraggono le recensioni, fonte per fonte

Ordine di preferenza: **backoffice del locale** → scheda pubblica → niente. I backoffice
danno l'ordinamento per data nativo, il testo integrale e i voti analitici; le schede
pubbliche danno testi troncati e ordinamenti che non controlli.

---

## TheFork — la fonte migliore, quando c'è

Il backoffice `manager.thefork.com/reviews` espone un GraphQL interno richiamabile
**dall'interno della pagina loggata** (stessa origine, usa i cookie di sessione).

Serve il `restaurantUuid`. Lo trovi installando un intercettore su `window.fetch` e
cliccando "LOAD MORE REVIEWS": la richiesta catturata contiene `operationName:
getPaginatedOnlineRestaurantReviews` con l'uuid nelle variabili.

Poi interroghi direttamente con una query ridotta ai campi che servono:

```js
const Q = `query R($u:String!,$f:RestaurantReviewFilters,$s:SortInput,$p:ReviewsPaginationInput!){
  restaurant(restaurantUuid:$u){ id paginatedOnlineReviews(filters:$f,sort:$s,pagination:$p){
    nextPage reviews{ id mealDate
      dinerRating{ globalRating ambienceRating foodQualityRating serviceRating
                   waitingTimeEvaluation noiseLevelEvaluation }
      comment{ content } } } }`;

const r = await fetch('/api/graphql', {
  method:'POST', credentials:'include', headers:{'content-type':'application/json'},
  body: JSON.stringify({ operationName:'R', variables:{
    u:'<restaurantUuid>',
    f:{ withCommentOnly:false },              // false = TUTTE, anche i voti senza testo
    s:{ sortBy:'mealDate', sortOrder:'desc' }, // ordine per data del pasto
    p:{ size:50, page:1 }                      // 50 per pagina, cicla su nextPage
  }, query:Q })
});
```

Note che contano:

- **`withCommentOnly:false`.** Con `true` perdi i voti senza testo, che sono ~30% del totale
  e fanno parte della media. La prima volta che ho fatto questa analisi ho usato `true` e
  ho sottostimato sia il totale sia il numero di negative.
- **`mealDate` è la data del pasto**, non della recensione. È quella giusta per il trend.
- Cicla finché `nextPage` esiste **o** finché la data più vecchia scende sotto la finestra.
- I locali stagionali hanno buchi enormi: dopo l'ultima recensione di stagione la serie
  salta all'anno prima. Non è un bug, è la chiusura invernale.
- Il campo `waitingTimeEvaluation` (`VERY_FAST`…`VERY_SLOW`) è oro: è l'unica misura
  strutturata della percezione dei tempi.

---

## Google — dal pannello del Profilo dell'attività

**La via che funziona.** Se l'utente gestisce il profilo, dalla pagina di ricerca del
locale compare il riquadro *"La tua attività su Google"* → **"Leggi recensioni"**. Quel
pannello ha l'ordinamento **"Più recente" nativo**.

Meccanica:

- Il pannello si apre in un **iframe same-origin**: leggilo con `iframe.contentDocument`
  (prendi l'iframe con `clientHeight` grande, sono presenti anche iframe da 0px).
- Contenitore scrollabile: cercalo come l'unico elemento con `scrollHeight` molto maggiore
  di `clientHeight`.
- Paginazione col bottone **"Altre recensioni"**, circa 100 recensioni per click, con un
  **tetto duro a 200**. Oltre quello serve l'esportazione dal Profilo dell'attività o
  l'API Google Business Profile.
- **Le stelle si leggono da `[aria-label="N su 5 stelle"]`**, mai dal testo: `innerText`
  rende cinque volte la parola "star" a prescindere dal voto. Il primo aria-label della
  pagina è la media del locale, va scartato.
- Il click sul bottone deve essere **reale** (mouse), non `element.click()`: le pagine
  Google ignorano i click sintetici. Lo scroll via JS invece funziona per posizionare.

**Vie che sembrano funzionare e non funzionano** (verificate, non riprovarle da zero):

| Tentativo | Esito |
|---|---|
| Menu "Ordina → Più recenti" su Maps pubblico | Il menu non viene proprio generato in un browser pilotato — né click reale, né tastiera |
| Scorrere la lista pubblica di Maps | Si interrompe intorno alle 40 recensioni |
| Pannello `tbm=lcl` / `#lkt=LocalPoiReviews` | Nessun controllo di ordinamento |
| `maps/rpc/listugcposts` | 403 senza un session token valido |
| `listentitiesreviews`, `/async/reviewDialog` | 404, endpoint dismessi |
| `business.google.com/locations` per verificare la proprietà | **Inaffidabile**: può non trovare un profilo che l'account gestisce davvero. Verifica dalla SERP del locale, dove compare "Il profilo di questa attività è gestito da te" |

Dalla scheda pubblica di Maps i testi sono **troncati intorno ai 240 caratteri** e
l'espansione ("Altro") richiede click reali uno per uno. Per l'analisi dei temi bastano;
per citare una recensione negativa per intero, no.

---

## Yelp e TripAdvisor — verifica di presenza

In Italia pesano poco per volume ma vanno controllati, perché un'assenza è un buco
colmabile a costo zero e un concorrente presente dove tu non ci sei è un'informazione.

Cerca il locale su `yelp.com` **e** su `yelp.it` (sono indici diversi). Se non c'è,
verifica che i concorrenti diretti della stessa via ci siano: è quello che rende
l'assenza significativa invece che irrilevante.

Su TripAdvisor spesso basta il dato aggregato (media e numero) che compare già nei
risultati di ricerca Google della scheda del locale, insieme a quello di TheFork pubblico.

---

## Regole comuni

**Fissa e dichiara la finestra.** "Ultimi tre mesi" va tradotto in due date esplicite, e la
data di riferimento va scritta nel documento: fra un mese quel PDF verrà riletto.

**Le date relative vanno convertite.** "1 mese fa" di Google è un'approssimazione grossa —
copre diverse settimane. Se la usi per un trend mensile, dichiara che è un'approssimazione.

**Deduplica per id.** Sia Maps sia il pannello Google rendono lo stesso blocco più volte
nel DOM. Conta gli id univoci (`data-review-id`, o il numero di autori distinti), non le
occorrenze.

**Salva l'estratto grezzo** in un file prima di analizzarlo. La sessione del browser scade,
la pagina si ricarica, e rifare l'estrazione costa molto più che rileggere un JSON.
