# iPratico — API pubblica ufficiale (chiave, host, percorsi, limiti)

Alternativa al backend del portale (Passi 1-6 di `SKILL.md`): serve una **chiave API pubblica**
per punto vendita (richiesta a `webdevelopers@ipratico.it`, doc
`https://ipratico.readme.io/reference/general`). Confermato sul campo (06-09/10/2026), salvo
dove indicato.

## Autenticazione e host
- Header `x-api-key` con la stringa **INTERA**, prefisso incluso: `<shopId>:<secret>`. Il solo
  uuid/secret senza prefisso dà `401`.
- La chiave di **staging** vale solo su `apicbdev` (locale demo, nessun dato vero).
- **Produzione**: `api.ipraticocloud.com/api/public` (risponde anche `apicb`).

## Percorsi
- **Chiusure**: `/closure` (singolare), date `YYYY-MM-DD`, massimo **365 giorni** per chiamata.
- **`/closed-payment-sessions`**: massimo **7 giorni** per chiamata, date **ISO col fuso**
  (con date a solo giorno risponde 0).
- **`/orders`** con date ISO dà gli stessi ordini di `statistics/orders` del portale, con
  differenze: nome riga in `value.orderItemName`; niente `isProduct` (usa `itemType: product` +
  `saleItem.productId`, che il Coperto non ha); niente categoria (si risale da `productId` col
  catalogo `/products`/`/product-categories`); attributi in
  `attributeName`/`attributeValue`/`attributeNote`; figli in `orderItemsChildren`; `table` è
  `null`, il nome si risale da `value.tableId` via `/tables`.

## Limiti e polling
Il limite di **60 richieste/minuto per chiave è CONDIVISO** con altri integratori dello stesso
locale: leggi `X-RateLimit-Remaining`. Schema di polling collaudato: 2 chiamate (`/orders` +
`/closed-payment-sessions`) al massimo ogni 8 secondi (≤15/minuto), più 3 chiamate pesanti ogni
30 minuti (categorie, prodotti, tavoli) che rinnovano le cache `productId→categoria` e
`tableId→nome`. Su `401`/`403`/`429` torna al token del portale come fallback. Collaudo:
la stessa serata letta con le due fonti (API pubblica e portale) deve dare comande, righe,
varianti, tavoli e storni identici.

Niente webhook: si legge solo a intervalli.

## Sicurezza
Chi ha la chiave di un locale può **creare ordini in cassa**: caso reale, asporti di prova
creati da terzi con righe inviate in cucina. Si riconoscono in `/orders` da `source.app:
api-public` e `value.log.createdBy`. Quando la chiave è condivisa con altri fornitori, questi
ordini vanno controllati periodicamente.

## ⚠️ Da verificare (letto sulla documentazione, non ancora provato sul campo)
`GET /orders` con gli stati completi (da `PARSED` a `CLOSED`/`CANCELED`, `sourceTypes`),
`GET /tables` (status `TAKEN`/`AVAILABLE`/`PAYING`, `orderId`, `roomId`, `currentSittings`,
`numberOfGuests`, `openDate`), `GET /rooms`, `POST /reservations` (la prenotazione arriva
nell'app Eat), fidelity, magazzino, operazioni. Non promettere al cliente queste funzioni finché
non sono testate.

(contributo di Andrea Chirivì, 2026-10-12 — sopra la base di Luciano Purpi, 2026-09-08)
