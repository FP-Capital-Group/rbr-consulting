---
name: estrai-dati-ipratico
description: Estrae i numeri di un cliente da iPratico Cloud (incassi Z giornalieri, coperti, scontrino medio, prodotti venduti, margini, canali, fasce orarie, sconti, storni) senza API key, usando il backend del portale con la sessione già loggata nel browser, più l'API pubblica ufficiale dove serve. Usala quando il consulente dice "tira giù gli incassi da iPratico", "estrai le chiusure di [cliente]", "quanto ha fatturato [cliente] a [mese] su iPratico", "prodotti venduti da iPratico per il menu engineering", "dati cassa iPratico nel CDG", "food cost da iPratico", "fasce orarie da iPratico", "endpoint iPratico". Metodo verificato RBR (training=1, dedup per zNumber, cutoff 06:00). Gli archivi di `statistics/orders` durano solo ~3 giorni: salvali subito se servono.
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

**401 vs 403, cosa significano davvero**: `403 "Forbidden channel"` **non** è un token rotto —
il profilo Chrome è passato sull'account di un ALTRO cliente a metà lavoro (vedi sopra): prima
di dichiarare l'accesso rotto o fidarti dei numeri, rileggi `select#location-0` e fai rifare il
login sul cliente giusto. `401` = token scaduto: si rigenera **senza login** con
`fetch('/it/cloud-stats/blind-closure/eat')`, poi una regex su `window.idUsr = …` nel testo
restituito; se resta 401 serve il login vero, che fa il consulente. La durata del token varia
da cliente a cliente (ore, non minuti).
*(contributo di Andrea Chirivì, 2026-10-12)*

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

**Quadratura fiscale**: il controllo incrociato è `tot.fiscal` (solo `fiscal.bill`, con
`invoice` e `training.bill` tenuti a parte) che deve coincidere col `DGFETotal` della Z.
Eccezioni che **non** sono errori: `fiscal.bill` con `billNumber "??"` o `zNumber "0"`
(`receiptAmount 0`); più Z nello stesso giorno (confronta con la somma); scontrino revocato
(`hasBeenRevoked`, da togliere); buchi nella numerazione dei `billNumber` (scontrini fatti in
cassa ma non saliti nel cloud). `DGFETotal` è **solo** il fiscale: l'extra incluso da
`training=1` sta nei totali di `statistics/data` e nelle sessioni come `training.bill`, non
dentro `DGFETotal` stesso. Ogni confronto anno su anno va fatto **Z contro Z**, mai un totale
con l'extra contro una baseline di sole Z (confonde la lettura della crescita reale). ⚠️ Cosa
restituisce `closures` con `training=1` esattamente è da verificare con chi ha scritto la
procedura, prima di contarci sopra in automatico.
*(contributo di Andrea Chirivì, 2026-10-12)*

## Passo 5 — Pulizia (obbligatoria)
- **Deduplica per `zNumber`**: a volte arrivano 2 record con stesso `zNumber` e stesso
  `DGFETotal` (closureDate diverse, `deviceCode=null` o `isDGFETotalManual` diverso). Una sola
  entry per `zNumber`, altrimenti raddoppi il fatturato.
- **Escludi Z annullate**: `zNumber=null` o `DGFETotal<=0`.
- **Giorno di servizio**: NON usare `referenceDate` (le chiusure dopo mezzanotte finiscono sul
  giorno dopo). Cutoff alle **06:00 ora italiana** su `firstClosedPaymentSessionDate` (o
  `closureDate`).
- **Z mancanti**: numeri `zNumber` che saltano, o giorni senza Z né corrispettivo, sono
  chiusure saltate o giorni di chiusura reale — chiedi al cliente, non presumere. Un giorno con
  due Z diverse si somma. **Z non trasmessa** (incasso zero nel cloud ma gli ordini ci sono):
  manca la chiusura, non l'incasso. Procedura: 1) salva SUBITO `statistics/orders` (ritenzione
  ~3 giorni, ha le `paymentSessions` sull'ordine); 2) rifai `closures` su 4-5 giorni prima di
  dare la giornata per persa (la Z può arrivare il giorno dopo); 3) se la Z è fatta ma non
  salita, togli `referenceDate` e usa `D 00:00:00 → D+1 06:00:00` su `statistics/data` e sulle
  sessioni (portano lo `zNumber`), poi sottrai i `training.bill` della notte prima
  (`referenceDate < D`); 4) il recupero si fa **rifacendo** l'estrazione, mai ritoccando quella
  vecchia; 5) chiedi al locale di trasmettere la Z.
*(contributo di Andrea Chirivì, 2026-10-12)*

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
| Coperti e scontrino medio | Day-end closing (colonne Customers amount, Cover average). ⚠️ Il campo **Coperti** dipende da chi apre il tavolo e resta spesso a `1` (campo non compilato). Controllo rapido: coperti del report ÷ tavoli vicino a 1 = campo non compilato — in quel caso prendi i coperti dal venduto (prodotto COPERTO o BATTUTA SINGOLA), confrontandoli con `nSittingPeople` di `statistics/data`. Va ricontrollato su ogni cliente nuovo e segnalato al cliente di far compilare i coperti a chi apre il tavolo |
| Fasce orarie | Report timeslot — `/cloud-stats/report-per-fascia-oraria/eat`, oppure `/statistics/data` → `timeChart` (vedi sotto) |
| Clienti / fidelity | Customer stats — `/cloud-stats/report-customer/1/eat` |
| Permanenza ai tavoli | Statistiche tavoli → "Permanenza ai tavoli" → Excel (vedi trappole sotto) |

Per queste: naviga → periodo → **Aggiorna** → *Mostra 100 righe* → leggi la tabella o **Excel**.
Stesse cautele: deduplica, escludi resi/storni, normalizza nomi prodotto (abbreviazioni, doppi spazi). **Cerca i prodotti per NOME, mai per categoria**: categorie miste (es. calici di vino dentro "Bevande" insieme ad acqua/bibite, mentre "Vini" contiene solo le bottiglie) fanno perdere pezzi e sballano i rapporti — filtra per nome del prodotto quando misuri una famiglia specifica.

### `/statistics/data`: prima scelta per i numeri di periodo (API-first)
Prima delle pagine report (tenute come controllo), prova `/statistics/data` con
`training=1&cashed=1&referenceDate=1&application=eat`. Campi: `totalSold`, `nSittingPeople`,
`docCount`, `avgCover`, `avgDoc`, `totalRowsDiscounts`, `dutchDiscount`, `customDiscounts`.
Grafici: `moneyTypeChart`, `categoryChart`, `productChart`, `businessMemberChart`,
`priceListChart`, `timeChart`. Accetta un mese intero (dal 1° all'ultimo giorno, `dateTo`
inclusivo). `timeChart` **non** è un grafico aggregato: è l'elenco dei singoli scontrini
(`{t: ISO UTC, y: importo}`) — raggruppandoli per ora locale ricostruisci le fasce orarie di
qualunque mese passato (ritenzione lunga, verificata su mesi passati). La stessa chiamata su
`D-7` dà il confronto con la settimana prima. Per i sospesi:
`closed-payment-sessions?isSuspendedPayment=1&documentTypes=invoice,fiscal.bill,customer.slip`.
*(contributo di Andrea Chirivì, 2026-10-12)*

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
- **Conti alla romana ("N Pasto")**: quando lo scontrino mostra "1 Pasto / 2 Pasto" al posto dei
  piatti, il dettaglio NON è in `closed-payment-sessions`. Il venduto vero sta in
  `/statistics/data` → `productChart` (`name, quantity, value`): conta i piatti ordinati con i
  Pasto già esplosi ("Pasto" stesso risulta a 0 nel `productChart`). Per consumo teorico e food
  cost usa `productChart` giorno per giorno, non le righe degli scontrini. Le varianti invece
  stanno solo nelle sessioni. Il dettaglio dei Pasto esiste anche in `statistics/orders`, ma solo
  per ~3 giorni (vedi ritenzione).
*(contributo di Andrea Chirivì, 2026-10-12)*

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

**Prima di ogni classifica per operatore**: `GET /business-members` (stesso token e channel)
restituisce operatori, nickname, `businessMemberGroupId`, `allowedApplications` e il PIN
personale in chiaro; `/business-member-groups` dà i gruppi permessi. **Se più operatori hanno
lo stesso PIN, l'attribuzione di storni e sconti per operatore non vale** finché i PIN non sono
personali — va scritto nel report **quanti** conti condividono un PIN, mai il valore del PIN.
Il tablet tiene gli operatori in copia locale: un PIN cambiato vale dal prossimo
login/sincronizzazione.

**Cosa significano davvero gli `eventTypes`** (non classificarli alla cieca):
- `loadCpsIntoCheckoutArea` e `switchedTabWhenOrderWasPopulated` = scontrino richiamato, conto
  diviso o conto spostato — **non sono storni**, vanno contati a parte come "divisioni e
  spostamenti di conto" (confondere i due può gonfiare di molto il totale storni apparente). Gli
  ordini senza tavolo da 0 minuti con lo stesso contenuto del tavolo diviso sono copie della
  divisione, non "ordini lampo".
- `changeServiceCharge` "da N a 0" = **coperti tolti dal tavolo** (azzeramento), non si vede da
  nessun'altra parte: l'evento ha righe vuote e totale nullo, il delta sta nel testo
  dell'evento. "N × Coperto in N × Coperto Live" è un cambio di voce, non un azzeramento: si
  ignora.
- Un acconto seguito da `loadOrderIntoTable` col conto pieno = conto scontrinato due volte.
- `ignoredTableOpenedInTakeOrder` = l'avviso "tavolo già aperto altrove" ignorato dall'operatore:
  ci sono due ordini aperti sullo stesso tavolo e un conto può sparire dal master (vedi
  `diagnosi-suite` §6 per il meccanismo completo).
- Le motivazioni di storno sono testo libero, spesso scritto a caso: **non vanno usate per
  classificare**.
- Prima di dire che un'operazione "non c'è", interroga `business-member-operations` **senza**
  filtro `eventTypes` su qualche giorno: escono i tipi davvero usati da quel locale (zero eventi
  nei gruppi sopra spesso vuol dire solo che ci sono altri eventi non filtrati, non che
  l'endpoint sia rotto). Con la lettura del preconto attiva, il portale espone anche
  `deletePrebill`, `billPrintedSuccessFull`, `billReprint`, `billReprintDismiss`: non tutti i
  locali li hanno.

**Sconti — in quali campi stanno, come non contarli due volte**: `totalRowsDiscounts` (sconti
di riga, es. da TheFork) e `customDiscounts` (sconti % manuali) sono campi **diversi** — non
confrontare mai due periodi letti su campi diversi. Le promo (`scontiCustom`) sono **già**
dentro lo sconto di fine conto delle sessioni: totale sconti = righe + fine conto, **senza**
aggiungere le promo a parte (altrimenti raddoppi). Nei `printedOrderItems` la riga `no_name` con
`isSubtotal:true` (`itemType: subtotal`) ripete lo sconto di fine conto e ha come `finalPrice`
il totale del conto: va scartata (`!i.isSubtotal && i.itemType!=='subtotal'`), altrimenti lo
sconto raddoppia. `discountsTotal` e `finalPrice` sono totali di **riga**, non si moltiplicano
per la quantità. I valori per categoria/prodotto delle statistiche sono già al netto degli
sconti di riga: gli sconti si leggono a parte e non si sottraggono una seconda volta. Da dove
vengono: i bottoni sconto del tastierino scrivono una riga unica sul subtotale con
`variation.name` = nome del bottone; un promo code con categorie selezionate sconta riga per
riga; un 2x1 senza tasto dedicato è una riga `no_name` con `priceVariation` negativo pari al
piatto meno caro.

**Storni di riga, `dateSend` dice se il piatto era già in cucina**: negli eventi
`row-removed`, `change-quantity`, `row-blocked`, `rowBlockedLastProduct` e nelle righe dei
tavoli svuotati, la riga d'ordine porta `dateSend`. Se **valorizzato**, la comanda era partita:
il piatto è stato prodotto e poi tolto dal conto (impatta il food cost reale). Se **vuoto**, il
piatto è stato tolto prima della comanda. Su `statistics/orders` la firma è diversa: uno storno
prima dell'invio ha `dateCancelled` senza `dateSend`, uno dopo l'invio ha `dateCancelled` e un
`dateSend` nuovo. ⚠️ Il percorso esatto del campo dentro l'evento va riletto su un evento vero
prima di scriverlo in automazioni: non risulta documentato altrove nel plugin.
*(contributo di Andrea Chirivì, 2026-10-12)*

## Stato ordini, blu preconto, anagrafiche/magazzino
Per lo **stato degli ordini** (preconto, tavoli spariti/orfani — endpoint `statistics/orders`,
ritenzione ~3 giorni), per le **anagrafiche prodotti/ingredienti/magazzino** (endpoint
`products`, `product-categories`, `warehouse-items`, utili a capire se il food cost è
compilabile da iPratico) e per altre trappole di lettura verificate sul campo (tavoli
ribattuti, riga subtotale, nomi campo che cambiano da un endpoint all'altro): vedi
`references/ordini-preconto-magazzino.md`. Per chi legge gli ordini **in diretta** (monitor
reparti/pass, non estrazione storica): `references/statistics-orders-live.md`.

## closed-payment-sessions, /rooms, /tables, permanenza ai tavoli

- **closed-payment-sessions**: gli scontrini stanno sotto la chiave `paymentSessions`. Varianti
  in `printedOrderItems[].variations` (`quantityVariation < 0` = rimozione). Per verificare un
  conto usa `originalOrderItems`/`printedOrderItems` con `discountsTotal` per riga; il tavolo si
  aggancia al numero tavolo del gestionale prenotazioni e all'ora. Più sessioni sullo stesso
  tavolo = conto alla romana. `closesOrder` è vero solo sulla quota che chiude il conto (distingue
  un pagamento parziale da un tavolo pagato); `orderId` combacia con l'id dell'ordine. Per mesi
  interi di venduto per prodotto, aggrega in pagina via JS spezzando a blocchi di ~10 giorni (vedi
  `diagnosi-suite/references/trappole-strumenti.md` per portare fuori output grossi dal browser).
  Per il giorno corrente, `statistics/data` dà 0 finché la Z non è entrata: ricostruisci da
  `statistics/orders`.
- **`/rooms` e `/tables`**: i nomi tavolo si **duplicano** fra sale diverse e anche nella stessa
  sala con formati diversi ("T 31", "T31", "Tav 31"). Ogni incrocio per nome tavolo (sessioni con
  eventi, controlli, import da Resmio o TheFork) deve portarsi dietro la **sala** e normalizzare
  il formato — altrimenti due tavoli con lo stesso nome in sale diverse si confondono.
- **Report "Permanenza ai tavoli" (Statistiche tavoli → Excel)**: una riga per conto con data/ora
  di chiusura, sala, tavolo, coperti, totale in centesimi, permanenza e comanda riga per riga.
  Trappole: (1) gli `.xls` di iPratico sono **HTML travestiti** — leggili con `pandas.read_html`
  (html5lib) o lxml, non come xls binario. (2) Imposta le date e premi **Aggiorna** prima di
  scaricare. (3) Ora di seduta = ora di chiusura − permanenza; la permanenza ha formati diversi
  ("52 mins", "01 hr, 01 min", "02 hrs") — serve un parser con ore/minuti opzionali e un controllo
  righe lette = righe totali. (4) Giorno di servizio = data − 7 ore (confine 07:00 dell'export).
  (5) Asporto e banco sono esclusi dal report: la quadratura al centesimo va fatta con le Z
  (`DGFETotal`) contro i corrispettivi, non con questo export. (6) Non contiene cliente né
  prenotazione: niente statistiche di no-show da qui.
- **Filtro date del portale**: senza premere **Aggiorna**, anche il file scaricato può essere del
  periodo precedente (un export richiesto per un intervallo può contenere solo una parte di
  quell'intervallo). I KPI a schermo possono restare vecchi mentre il file è già corretto:
  verifica sempre il range contando i giorni distinti **dentro** il file scaricato, non fidarti
  dell'intervallo impostato nei filtri. Il campo ora spesso non viene applicato: per i confronti
  anno su anno usa giorni interi identici su entrambi i periodi.
*(contributo di Andrea Chirivì, 2026-10-12)*

## Note
- Per queste estrazioni non serve API key: si usa il backend del portale con la sessione del
  cliente (è l'unica via che vede le Z manuali e l'extra con `training=1`).
- iPratico ha **anche un'API pubblica ufficiale** (header `x-api-key`, una chiave segreta per
  punto vendita, rilasciata una sola volta su richiesta a `webdevelopers@ipratico.it`; doc
  `https://ipratico.readme.io/reference/general`). Serve per anagrafiche clienti, codici promo,
  ordini e sessioni chiuse: in particolare `promo-codes-movements` è il **registro dei riscatti
  dei codici promo** (con `orderId` → scontrino e `businessActorId` → cliente), cioè il
  tracciamento delle campagne QR senza scaricare report a mano. Host di produzione, endpoint,
  limiti di rate e trappole: `references/api-ufficiale.md` in questa skill (dettagli ulteriori in
  `memory/ipratico_api.md` del repo rbr-suite). *(contributo di Luciano Purpi, 2026-09-08; chiave,
  host, percorsi e limiti completati da Andrea Chirivì, 2026-10-12)*
- Vale per qualunque cliente su iPratico Cloud: cambia solo lo `shopId`.
- Se il consulente ha `mcp__claude-in-chrome__*` o il browser tool, è la via A/B; senza browser
  fai fare l'export Excel al consulente e leggi il file (via C).

(Procedura di Marco Cuccaro, 2026-09-02.)
