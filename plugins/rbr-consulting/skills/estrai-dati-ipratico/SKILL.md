---
name: estrai-dati-ipratico
description: Estrae i numeri di un cliente da iPratico Cloud (incassi Z giornalieri, coperti, scontrino medio, prodotti venduti, margini, canali, fasce orarie) senza API key, usando il backend del portale con la sessione già loggata nel browser. Usala quando il consulente dice "tira giù gli incassi da iPratico", "estrai le chiusure di [cliente]", "quanto ha fatturato [cliente] a [mese] su iPratico", "prodotti venduti da iPratico per il menu engineering", "dati cassa iPratico nel CDG". Metodo verificato RBR (training=1, dedup per zNumber, cutoff 06:00).
---

# Estrarre i numeri da iPratico Cloud (metodo RBR verificato)

iPratico non dà API key, ma il portale web usa un backend interrogabile con la sessione del
cliente. Serve **Claude con accesso al browser** (Claude in Chrome o il browser tool della
sessione). Le credenziali dei clienti sono riservate: le inserisce il consulente, mai Claude.

## Prerequisiti (li fa il consulente)
1. Chrome loggato su `https://www.ipraticocloud.com` con l'account del cliente.
2. Aperta una pagina statistiche, es. *Chiusure alla cieca* (`/cloud-stats/blind-closure/eat`).
3. Chiedi in UN messaggio: cliente, periodo (dal → al, `YYYY-MM-DD`), e se ha più locali quale.

⚠️ **Una sola sessione iPratico per profilo Chrome, e cambia cliente da sola.** Se in un'altra
scheda si apre un altro cliente, l'utenza attiva cambia sotto i piedi senza alcun segnale nella
pagina su cui stai lavorando (due incidenti in tre giorni: una configurazione salvata sull'account
di un ALTRO cliente, un codice promo quasi creato nell'account sbagliato). Quindi:
1. Prima di OGNI scrittura (e prima di salvare un'estrazione) leggi l'utente attivo e fermati se
   non è quello atteso: `document.body.innerText.match(/Benvenuto\s+([^\n]+)\n([^\n]+)/)`.
2. Prima di sovrascrivere un valore leggi e annota quello precedente, così è ripristinabile.
3. Lavori su due account (es. confronto codici promo di due brand)? Non si tengono aperti
   insieme: metti in conto che il consulente cambi login a metà.
*(contributo di Luciano Purpi, 2026-09-03)*

## Passo 1 — shopId del locale
Nella pagina attiva leggi il menu a tendina del locale: `select#location-0`. Il `value`
dell'opzione selezionata è lo **shopId** (numero, es. `23179`). Più locali → chiedi quale o
ripeti per ciascuno.
⚠️ Il selettore **non è sempre `location-0`**: sulla pagina *Totalizzazioni* è `#location-1`, e
`.select-filter-location` letto con `querySelector` può restituire il nodo sbagliato. Leggi
sempre il **valore** (`$('#location-1').val()`), mai l'etichetta del bottone.
*(contributo di Luciano Purpi, 2026-09-03)*

## Passo 2 — Token di sessione
Nel contesto JS della pagina leggi `window.idUsr` (stringa alfanumerica ~40 caratteri): è il
token del backend. Se manca, apri prima `.../cloud-stats/blind-closure/eat` e rileggi.
Il token **scade**: se una chiamata torna 401, ricarica una pagina del portale e rileggilo.

## Passo 3 — Chiusure (incassi + Z fiscali)
```
GET https://apiportal.ipraticocloud.com/statistics/closures
    ?channel=lct_<SHOPID>&training=1
    &dateFrom=<DAL> 00:00:00&dateTo=<AL> 23:59:00
    &application=eat&includeDeleted=true
```
Header obbligatori:
- `Authorization: <window.idUsr>` (token nudo, NON "Bearer")
- `Origin: https://www.ipraticocloud.com`
- `Referer: https://www.ipraticocloud.com/`
- `Accept: application/json, text/javascript, */*; q=0.01`

⚠️ **`training=1` è regola RBR**: include anche l'"extra" nel fatturato. Mai `0`.

Come eseguire, in ordine di preferenza:
- **A)** `fetch()` nel contesto della pagina (stessa origine autorizzata) → JSON.
- **B)** Se bloccato: pagina **Chiusure di giornata** (`/it/cloud-stats/chiusure/eat`) → imposta
  periodo → **Aggiorna** → leggi le richieste di rete → corpo della risposta `statistics/closures`.
- **C)** Fallback sempre valido: stessa pagina, *Mostra 100 righe*, leggi la tabella (o **Excel**).

## Passo 4 — Campi utili di ogni chiusura
| Campo | Significato |
|---|---|
| `DGFETotal` | **Incasso lordo Z** del giorno: è IL fatturato. Valorizzato anche per le manuali |
| `zNumber` | Numero Z progressivo (stringa). `null` = Z annullata |
| `referenceDate` | Data di competenza `YYYY-MM-DD` (trappola: vedi Passo 5) |
| `closureDate` | Momento della chiusura (UTC) |
| `firstClosedPaymentSessionDate` | Prima sessione: miglior proxy del giorno di servizio |
| `isDGFETotalManual` | `true` = totale inserito a mano (cassa giù). Da tenere |
| `nDocuments` | Numero documenti fiscali |

## Passo 5 — Pulizia (obbligatoria)
- **Deduplica per `zNumber`**: a volte arrivano 2 record con stesso `zNumber` e stesso
  `DGFETotal` (closureDate diverse, `deviceCode=null` o `isDGFETotalManual` diverso). Una sola
  entry per `zNumber`, altrimenti raddoppi il fatturato.
- **Escludi Z annullate**: `zNumber=null` o `DGFETotal<=0`.
- **Giorno di servizio**: NON usare `referenceDate` (le chiusure dopo mezzanotte finiscono sul
  giorno dopo). Cutoff alle **06:00 ora italiana** su `firstClosedPaymentSessionDate` (o
  `closureDate`).

## Passo 6 — Output
Tabella per giorno di servizio: data, incasso (`DGFETotal`), n. Z, n. documenti; **totale del
periodo**. Segnala giorni con chiusure manuali e duplicati risolti. Se il dato va nel CDG:
prima la skill `riconciliazione-dati-cliente`, poi `cdg-fatture` / `crea-cdg-cliente`.

## Altri numeri (stesso login, pagine report: menu Statistics — iPratico eat)
| Numero | Pagina |
|---|---|
| Prodotti venduti (mix, per `menu-engineering`) | **Totalizzazioni** → tabella *DETTAGLIO CATEGORIA PER QUANTITÀ* (vedi sotto). *Venduto e sconti* (`/cloud-stats/report-prodotti-operatore/eat`) solo come controllo |
| Margini / food cost per prodotto | ⚠️ *Products profit margin* (`/cloud-stats/stats-products-profit-margin/eat`) è **parziale**: poche decine di prodotti su centinaia. Mai usarla come fonte del mix; il costo va dal File 02 (`foodcost-cliente`) |
| Sala / asporto / delivery, reparti, varianti | Totalizzazioni — `/cloud-stats/totalizzazioni/eat` |
| Storni, sconti, omaggi, aperture cassetto | endpoint `business-member-operations` (vedi sotto) |
| Coperti e scontrino medio | Day-end closing (colonne Customers amount, Cover average) |
| Fasce orarie | Report timeslot — `/cloud-stats/report-per-fascia-oraria/eat` |
| Clienti / fidelity | Customer stats — `/cloud-stats/report-customer/1/eat` |

Per queste: naviga → periodo → **Aggiorna** → *Mostra 100 righe* → leggi la tabella o **Excel**.
Stesse cautele: deduplica, escludi resi/storni, normalizza nomi prodotto (abbreviazioni, doppi spazi).

## Pagina Totalizzazioni: quattro trappole che falsano il dato senza errore
*(contributo di Luciano Purpi, 2026-09-03)*
1. **Locale**: `#location-1`, leggere il valore (vedi Passo 1).
2. **"Interrogazione per" = *Data di emissione*** (dentro *Mostra filtri*). Il default è *Data di
   competenza* e alza il dato. Si resetta a ogni reload: rimetterlo a ogni giro. In JS:
   `$('.select-filter-reference-date').val('createdDate').multiselect('refresh').trigger('change')`,
   poi verificare che il bottone visibile dica "Data di emissione" prima di premere Aggiorna.
3. **Finestra 08:00 → 08:00 del giorno dopo** per i locali che chiudono dopo mezzanotte: un mese
   si prende `01/MM 08:00 → 01/MM+1 08:00`, non `01 00:00 → 30 23:59`.
4. **Rendering con un giro di ritardo**: dopo Aggiorna i filtri mostrano già i valori nuovi ma i
   numeri sono ancora della query precedente, e un reload asincrono può riportare indietro il
   contenuto (dati della sede o del mese sbagliato salvati tre volte). Regola: attendere ~20 s e
   pretendere che **locale + intervallo + incassato restino identici per 6 letture consecutive a
   1 s** prima di salvare.

**Dove sta il venduto vero** (tabelle DataTables, lettura `$(tb).DataTable().rows().data().toArray()`):
- **Venduto per prodotto** → *DETTAGLIO CATEGORIA PER QUANTITÀ*: ogni riga categoria ha un array
  `children[]` con i prodotti (`{name, quantity, value}`). Non esiste una pagina dedicata al mix.
- **Aggiunte** → *DETTAGLIO VARIANTI* (130-415 righe per locale/mese). ⚠️ La maggior parte NON
  sono aggiunte: sono istruzioni di cucina ("ben cotta", "ghiaccio", "non fare") e marcatori di
  portata `1 <NOME PRODOTTO>`, che hanno un importo ma sono già contati nelle categorie →
  sommarli è doppio conteggio. Eccezione: nei menù a formula/Experience i piatti scelti compaiono
  proprio come varianti `N <NOME PRODOTTO>` → usarli AL POSTO del forfait della formula, mai in
  aggiunta.
- **Imponibile** → *DETTAGLIO REPARTI*.

## Storni, sconti, omaggi, cassetto — `business-member-operations`
*(contributo di Andrea, 2026-09-10, validato sul campo)*
`GET https://apiportal.ipraticocloud.com/business-member-operations`, `Authorization: <window.idUsr>`
(stessi header del Passo 3). Filtro `eventTypes=`:
- righe/quantità/cassetto: `change-quantity,row-removed,row-blocked,rowBlockedLastProduct,loadCpsIntoCheckoutArea,switchedTabWhenOrderWasPopulated,didOpenDrawer`
- tavoli: `table-emptied,loadOrderIntoTable,ignoredTableOpenedInPayment,ignoredTableOpenedInTakeOrder,deleteClosedPaymentSession,takeawayOrderDeleted,changeServiceCharge`

Trappole: `dateTo` è **esclusivo** e a giorno (per il giorno D: `dateFrom=D&dateTo=D+1`); scontrini
e Z compaiono nel cloud solo **dopo la chiusura Z**, gli storni invece in tempo reale; sconto riga
= `discountsTotal` dell'item, prezzo pieno = `discountsTotal + finalPrice`; omaggio = `finalPrice == 0`.
Dettagli: `memory/ipratico_portal_api.md` (repo rbr-suite).

## Note
- Per queste estrazioni non serve API key: si usa il backend del portale con la sessione del
  cliente (è l'unica via che vede le Z manuali e l'extra con `training=1`).
- iPratico ha **anche un'API pubblica ufficiale** (header `x-api-key`, una chiave segreta per
  punto vendita, rilasciata una sola volta su richiesta a `webdevelopers@ipratico.it`; doc
  `https://ipratico.readme.io/reference/general`). Serve per anagrafiche clienti, codici promo,
  ordini e sessioni chiuse: in particolare `promo-codes-movements` è il **registro dei riscatti
  dei codici promo** (con `orderId` → scontrino e `businessActorId` → cliente), cioè il
  tracciamento delle campagne QR senza scaricare report a mano. Host di produzione, endpoint e
  trappole: `memory/ipratico_api.md` (repo rbr-suite). *(contributo di Luciano Purpi, 2026-09-08)*
- Vale per qualunque cliente su iPratico Cloud: cambia solo lo `shopId`.
- Se il consulente ha `mcp__claude-in-chrome__*` o il browser tool, è la via A/B; senza browser
  fai fare l'export Excel al consulente e leggi il file (via C).

(Procedura di Marco Cuccaro, 2026-09-02.)
