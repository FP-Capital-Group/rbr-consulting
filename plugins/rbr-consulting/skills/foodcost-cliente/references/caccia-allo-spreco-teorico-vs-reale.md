# Caccia allo spreco: consumo teorico vs reale

> Integrato dalla skill proposta "foodcost-rbr" di Andrea Chirivì (2026-10-12, scansione
> skill) nella skill `foodcost-cliente` — l'autore stesso la proponeva come pezzi da
> fondere qui, non come skill a sé. Copre il secondo prodotto del food cost RBR, che il
> File 02 (margine per piatto) non fa da solo: la caccia allo spreco per differenza fra
> consumo teorico e consumo reale. Costruito e validato sul Noolas (set 2026).
>
> ⚠️ **Da allineare con Marco**: la formula dello sfrido usata qui per il costo riga
> (`peso/1000 × prezzo/(1−sfrido%)`) va verificata contro quella del template RBR
> (`D = s/(1−s)`) prima di usarla come standard — non riconciliata in questo merge.

## Quando si usa
Dopo il File 02 (margine per piatto), quando il cliente chiede "dove sto sprecando" o
"se qualcuno ruba". Richiede, in più rispetto al File 02: **due inventari** agli estremi
del periodo (per reparto: pizzeria/cucina/sala/bar) e il **venduto POS con le varianti**
(aggiunte/rimozioni). Periodo minimo sensato: 1 mese; ideale 3-5 mesi al primo giro, poi
mensile.

## Il metodo
Per gruppi di ingredienti confrontabili (15-20: farina, mozzarella, patatine, macinato,
buns, birra per spina…):
```
teorico = Σ venduto × grammatura (± varianti, + tavoli cancellati)
reale   = inventario iniziale + acquisti − inventario finale
```
- **Convalida del metodo prima di fidarsi del risultato**: 3-4 gruppi devono chiudere
  entro ±5-6% (esempio di gruppi "ancora"sul Noolas: bistecca, bacon, stracciatella,
  pelato). Se nessuno chiude, è sbagliata una grammatura o un inventario, non il locale.
- **Lettura dei residui**: sui **PEZZI** (burger, buns) e sui **LITRI** (birra) "porzioni
  abbondanti" non esiste — un pezzo è un pezzo, quindi un residuo è merce uscita senza
  comanda. Sui **KG** decidono le pesate a campione.
- **Residui negativi** = serviti più poveri della ricetta (es. cheddar −50% = metà fette)
  oppure omaggi fuori inventario (es. fusti regalo): sono un finding anche loro, non un
  errore di calcolo da scartare.

## I 4 canali del POS da chiudere PRIMA di parlare di furto (iPratico: skill `dati-ipratico`
integrata in `estrai-dati-ipratico`, vedi `references/ordini-preconto-magazzino.md`)
1. Venduto + **varianti** (`printedOrderItems[].variations`, `quantityVariation<0` = rimozione).
2. **Tavoli cancellati/svuotati** (`business-member-operations`, `table-emptied` ecc.): le
   righe con `dateSend` sono state CUCINATE → vanno DENTRO il teorico. Attenti al
   ribattuto (stesso tavolo, `orderId` nuovo): incrociare per nome tavolo o si conta doppio.
3. **Storni di riga** (`row-removed`/`change-quantity`/`row-blocked`): `dateSend` distingue
   prodotto-e-tolto (nel teorico) da tolto-prima-della-comanda (nessun impatto).
   Ritenzione lunga: recuperabili all'indietro.
4. **Blu preconto e ordini orfani** (`statistics/orders`): il blu è incasso per altra via,
   NON ammanco; gli orfani (0 sessioni, 0 preconto, tavolo vero, >3 min) sono IL segnale.
   Ritenzione ~3 giorni: all'indietro NON si ricostruisce — dirlo, mai spacciare il totale
   per ammanco.

Solo ciò che resta DOPO tutti e quattro è "mai passato dalla cassa".

## Consumi interni da togliere dal teorico PRIMA di parlare di spreco
⚠️ Confermato il principio, non ancora generalizzato ogni singolo numero: verificare i parametri specifici su ogni cliente, non riusarli come costanti.
- **Personale**: se battere i pasti dello staff ogni sera non regge nella pratica, stimali dai turni (chi ha lavorato, quante sere, moltiplicato per la regola di consumo del locale — es. una bibita a fine turno + acqua + un piatto a cena è un parametro visto su un cliente, **non una costante da riusare**: va scritto come parametro del locale specifico, verificato con lui). Valorizzali a food cost e ttogli il risultato dal teorico dei clienti paganti: senza questa voce, lo scarto sembra spreco o ammanco quando è solo personale non battuto.
- **Vino dei menu evento**: quando è compreso nel prezzo del menu, non passa dai tasti vino in cassa — togli le bottiglie degli eventi dal confronto per etichetta prima di parlare di eventuali furti.
- **Omaggi e fusti regalati fuori inventario**: spiegano residui negativi altrimenti incomprensibili (vedi sopra).

## Cerimonie / menù forfait
Se il locale ribatte menù fissi cancellando il tavolo vero: abbinare cancellazioni↔menù
**per valore, tavolo per tavolo** (non per somma giorno). I menù forfait senza ricetta
bucano il teorico: farsi dare la composizione standard (i personalizzati sono pochi, si
trascurano al primo giro). Stessa logica dei menù cerimonia: stesso nome a prezzi diversi
= composizioni diverse → chiedere la composizione PER FASCIA DI PREZZO.

## Trappole verificate (costate ore)
- Google Sheets locale IT: scrivere **float**, mai stringhe "28.29" (diventano ORE);
  formule con `;`; pattern numberFormat in sintassi EN (`#,##0.00 €`); `clear()` NON pulisce
  i formati.
- Il service account **non ha storage Drive**: il file lo crea il connettore Drive del
  consulente (mimeType spreadsheet), poi si condivide in scrittura al service account e si
  compila con gspread.
- Ingredienti omonimi con pesi diversi (es. HAMBURGER 150 vs 300 g): chiavi distinte per peso.
- Regex categorie: attenzione ai confini di parola (es. `BOVINO` contiene `VINO`).
- P.IVA da Excel perde lo zero iniziale: `zfill(11)` da entrambi i lati.
- Fogli dei clienti: aspettarsi blocchi doppi, tab copiati da ALTRI locali, totali rotti —
  il costo piatto nel file pulito è SEMPRE la somma delle righe, mai il totale ereditato.
- iPratico non dà il food cost da solo: ingredienti e `productionCost` in anagrafica sono
  quasi sempre vuoti. Le grammature si raccolgono dalla cucina, non dalla cassa.

## Altri innesti utili non ancora nel file principale
- **Food e drink SEPARATI, coperto fuori da entrambi**: il coperto è ricavo senza costo e
  le bevande devono FINANZIARE il margine. Se il drink cost supera il food cost (caso
  reale: 37,8% vs 29,4%) si parte da lì.
- **Il canale cambia il margine**: delivery al 32% di commissione può rendere il 48% in
  meno a scontrino pari rispetto alla sala — se il locale ha delivery/asporto rilevante,
  margini e break-even vanno calcolati PER CANALE, mai aggregati. Commissione = pagato
  reale ÷ ricavi canale, mai stimata.
- **Quadratura del venduto prima di usarlo**: prima di usare un estratto POS per il
  teorico, quadrarlo col riferimento interno (Z/DGFETotal per iPratico, riga TOTALI per
  gli export) mese per mese, dichiarando gli scostamenti residui.

## Output e ritmo
- File pulito consegnato + **riepilogo al cliente in €/anno** (mai solo %), coi 5
  piatti/prodotti peggiori.
- Controllo prezzi fatture settimanale (alert solo su violazioni) + giro sprechi
  **mensile a ogni inventario**.
- Contromisure standard da proporre: motivo obbligatorio sui tavoli cancellati,
  omaggi/staff battuti a 0 €, pesate a campione sui kg, conta pezzi serale sui pezzi,
  inventario mensile puntuale.
