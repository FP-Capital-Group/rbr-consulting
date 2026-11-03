# iPratico — stato ordini, blu preconto, magazzino/food cost e trappole aggiuntive

> Integrato dalla skill proposta "dati-ipratico" di Andrea Chirivì (2026-10-12, scansione
> skill) nella skill `estrai-dati-ipratico` — l'autore stesso la proponeva come pezzi da
> fondere qui, non come skill a sé. Copre ciò che il metodo base (chiusure Z) non tocca:
> stato ordini/preconto, anagrafiche/magazzino per il food cost, e alcune trappole di
> lettura trovate sul campo (Noolas shopId 18300, Osteria Carmelo shopId 23698, 05-09/09/2026).

## Accesso via browser (riassunto)
Stesso login/token del metodo base (`window.idUsr`, header `Authorization: <token>` nudo,
NON Bearer; `channel=lct_<SHOPID>`; base `https://apiportal.ipraticocloud.com`, solo GET).
⚠️ Il profilo Chrome può cambiare account fra una sessione e l'altra: rileggere sempre
`select#location-0` anche a metà lavoro. Un canale non proprio risponde `403 Forbidden
channel`; un `401` è il token scaduto (ricaricare e rileggere `window.idUsr`).

## La trappola delle date è doppia e non dà errore
| Tipo | Endpoint | Formato |
|---|---|---|
| Giorno-based | `statistics/data`, `closed-payment-sessions` | `dateFrom=D&dateTo=D` — **dateTo INCLUSIVO** |
| Con orario | `closures`, `business-member-operations`, **`statistics/orders`** | serve data **e ora** |

- Passare `D → D+1` su un endpoint giorno-based **somma due giornate** (esempio reale:
  D→D = 1.327,94 € · D→D+1 = 6.776,47 €).
- `statistics/orders` con date **senza orario** torna **0 record e status 200**: sembra
  "nessun ordine", invece è la query sbagliata. Usare `D 00:00:00` → `D+1 04:00:00`.
- Operazioni (`business-member-operations`): finestra UTC con cutoff 06:00 locali,
  `D 04:00Z → D+1 04:00Z`.
- Il controllo che smaschera ogni errore di periodo: `tot.fiscal` deve coincidere col
  `DGFETotal` della Z (vedi skill base, Passo 4).

## Gli archivi non durano uguale
| Endpoint | Ritenzione |
|---|---|
| `closed-payment-sessions`, `statistics/data`, `closures`, `business-member-operations` | **lunga**, verificata fino a dic 2025 |
| **`statistics/orders`** | **~3 giorni** completi, ~7 per gli ordini mai chiusi |

Tutto ciò che richiede lo **stato dell'ordine** (blu preconto compreso) **va letto ogni
giorno o è perso per sempre**: è il motivo per cui il controllo giornaliero non è
rimandabile (vedi anche skill `foodcost-cliente/references/caccia-allo-spreco-teorico-vs-reale.md`
per come questo impatta la caccia allo spreco).

## Stato ordini e blu preconto (`/statistics/orders`)
Campi utili: `hasBeenPrintedPreBill`, `lastPrebillNumber`, `paymentSessions[]`, `total`,
`table.name`, `log.*`. Nome prodotto qui è **`name`** (diverso da `printedOrderItemName`
degli altri endpoint — vedi tabella nomi campo più sotto).

Il **blu preconto** è un concetto del cliente, non un difetto: quando il responsabile di
sala stampa il preconto, quel conto è **incassato, solo per un'altra via**. Non è un
ammanco e non deve generare allarme. Il bersaglio sono i tavoli inseriti che spariscono
**senza** passare né dallo scontrino né dal blu:

```
paymentSessions > 0 (o stesso tavolo ribattuto)  -> chiuso e scontrinato   NORMALE
0 sessioni + hasBeenPrintedPreBill == true       -> blu preconto           NORMALE
0 sessioni + niente preconto + total > 0         -> LIBERATO SENZA INCASSO  segnale
```

Dentro gli orfani, la **durata** (`modifiedDate − createdDate`) separa due cose diverse:
- **> 3 minuti con un tavolo vero** = gente che ha consumato e il conto è sparito (caso grave).
- **0-1 minuto senza tavolo** = "ordini lampo" (pasto personale o asporto annullato):
  non è furto, ma è food che esce e va misurato, non ignorato.

### Ricostruire il passato quando `statistics/orders` non c'è più
Sessioni ed eventi portano entrambi `orderId`, e le sessioni portano `table.name`. Per un
giorno passato: incrociare eventi `table-emptied` con sessioni dello stesso giorno per
`orderId` **e** nome tavolo. Dà "fiscalizzato sì/no" ma **non** distingue il blu preconto:
oltre i 7 giorni quella distinzione non è ricostruibile — va **detto**, mai spacciare il
totale per ammanco.

## Tre errori di lettura da non rifare
1. **`table-emptied` da solo NON significa ammanco.** Un tavolo da 105,50 € con un
   `table-emptied` aveva **sei** `fiscal.bill`: gruppo da 5 che ha pagato alla romana.
2. **Un tavolo svuotato e poi RIBATTUTO prende un `orderId` nuovo**: incrociare **anche
   per nome tavolo**, o risulta falsamente sparito (caso reale: un tavolo da 596,80 €
   riapparso come conto da 529 € con id diverso).
3. **La riga `no_name` con `isSubtotal:true` è il SUBTOTALE, non un prodotto**: va
   scartata dai `printedOrderItems` o si raddoppia lo sconto del conto.

## Anagrafiche, prodotti e magazzino (per il food cost)
| Cosa | Endpoint |
|---|---|
| Prodotti | `/products` |
| Categorie | `/product-categories` |
| Tutto insieme (ingredienti, listini, categorie, tag, IVA) | `/products/dependencies` |
| Magazzino a unità | `/warehouse-items?isIngredient=false&isModular=false` |
| Inventario / distinta base (pagine portale) | `/it/wharehouse/warehouse-unit-inventory` · `/it/wharehouse/warehouse-bill-of-materials-advice` |

⚠️ **Prima di promettere un food cost da iPratico, verifica che i costi ci siano.**
Riscontro reale: `/warehouse-items` vuoto, 0 ingredienti su 119 con un costo, 0 prodotti
su 613 con `productionCost`, e gli `articleComponents` dei prodotti "con distinta base"
spesso sono in realtà gruppi di upsell (`initialQuantity: 0`), non ricette con
grammature. La struttura esiste ma è vuota finché il cliente non popola ingredienti e
grammature: in quel caso il food cost va costruito fuori da iPratico (skill
`foodcost-cliente`). Controllo rapido in console:
```js
const P=(await g('/products',{})).map(x=>x.value||x);
P.filter(p=>p.isIngredient).length;                      // ingredienti in anagrafica
P.filter(p=>(p.pricesArray||[]).some(x=>x.productionCost>0)).length;  // con costo: se 0, niente food cost
```

## Nomi campo che fanno perdere tempo
| Dove | Campo |
|---|---|
| Nome prodotto in `closed-payment-sessions` | `printedOrderItemName` → `orderItemName` → `product.name` |
| Nome prodotto in **`statistics/orders`** | **`name`** (diverso!) |
| Mezzo di pagamento | `payments[].transactionDetail.moneyTypeId` |
| Operatore di un evento | `value.log.createdBy` |
| Operatore di un ordine | `log.createdBy` (apre) / `log.modifiedBy` (chiude) |
| `fiscal` = solo i `fiscal.bill` | esistono anche `invoice` e `training.bill`: sommarli rompe la quadratura con la Z |

## Portare fuori output grossi dal browser
Chrome blocca i download in serie e il tool JS tronca a ~1.000 caratteri. Scrivere il
JSON nel DOM (`document.body.innerHTML='<pre id="d"></pre>'` + `textContent`) e leggerlo
col tool di lettura pagina: regge ~50.000 caratteri in una chiamata. Le query lunghe
(30+ giorni) vanno spezzate in blocchi da ~10 giorni accumulando su `window`, o il CDP
va in timeout a 45 s.

## Mappa delle pagine del portale (per capire cosa esiste)
Venduto e sconti · Turni di lavoro · Statistiche costi variabili · Statistiche tavoli ·
Report per fascia oraria · Quadrature di cassa · Totalizzazioni · Comparazioni ·
Corrispettivi · Fatture · Sospesi · Storni e operazioni di cassa · Operazioni tavoli e
takeaway · Conferma stampe · Eliminazione Addebiti · Ingredienti/semilavorati ·
Prodotti · Magazzino semplice a unità · Distinta base · Operatori · Sale · Tavoli ·
Listini. Per scoprire l'endpoint di una pagina: aprirla e leggere le richieste di rete
filtrando `apiportal`.

## Strumenti già pronti (Noolas)
`~/noolas-strumenti/controllo-ipratico/`: `RUNBOOK.md` (procedura completa e datata),
`render_controllo.py` (PDF giornaliero, **non modificare senza chiedere**),
`fix_doctot.py`, `storico/` (memoria per operatore, **non cancellare**).
