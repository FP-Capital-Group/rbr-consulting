# Modalità 2: controllo ricorrente contro listino concordato

Richiamato da SKILL.md, sezione "Modalità 2: controllo ricorrente contro listino concordato". Soglie ed esempi qui sotto sono **proposte** da un solo cliente (Noolas): vanno ritarate su un secondo caso prima di darle per definitive, e serve l'ok di Leo Franco (autore della skill) prima di considerarle regola del plugin.

## 1. Prerequisiti e buchi da dichiarare
Prima di iniziare, mappa: fornitori che fatturano senza righe (solo totali DDT — vedi SKILL.md, sezione finale), data dell'ultima fattura registrata per fornitore, fatture registrate dopo lo scarico (righe tardive). Dichiarali, non ignorarli.

## 2. Costruire il listino concordato in casa
Catalogo costruito dalle righe fattura. Prezzo concordato = moda del periodo. Categoria e reparto a menu a tendina. Scorta minima e tetto dal consumo medio. Il file è il **master**: una rigenerazione non deve sovrascrivere le modifiche manuali già fatte.

## 3. Pulizia dei nomi e delle categorie
Stessa logica della pulizia nomi in SKILL.md, con due aggiunte specifiche:
- regex di categoria con **confini di parola** (es. "BOVINO" contiene "VINO": senza `\b` la carne finisce nelle bevande);
- P.IVA normalizzata con zero-padding a 11 cifre per confrontarla in modo affidabile tra fonti diverse.

## 4. Tolleranze
Unica (~2%) su secco e confezionato; ~15% su ortofrutta e fresco, **come proposta da ritarare dopo un mese** di controllo reale. Il fresco del fornitore abituale, se la sua fattura non ha righe, si prende dal food cost. Gli acquisti di ripiego (fornitore abituale chiuso/in ferie) vanno a reparto "NO", mai cancellati dal confronto.

## 5. Sforamento vero
`valore netto ÷ quantità netta` per fornitore+prodotto, nettando note di credito, omaggi (es. un cartone omaggio ogni N) e resi — mai da una singola riga. Ordina per €/anno, non per %: una % alta su un prodotto marginale pesa meno di una % piccola su un prodotto ad alto volume. Confronta sempre lo stesso prodotto, non la stessa famiglia (vedi SKILL.md, "stessa merce"), sempre per unità.

## 6. Controllo settimanale automatico
Finestra di 8 giorni. Mail al titolare **solo se** ci sono sforamenti, prodotti nuovi o casi speciali — niente rumore se è tutto in regola. Zero segnalazioni non vuol dire tutto in regola: prima guarda sempre la data dell'ultimo dato disponibile. Ordine dei filtri: prima i casi speciali (trasporti, rettifiche), poi il rumore, con un test di non regressione sui numeri chiave a ogni modifica. Non ripetere uno sforamento già segnalato dalle bolle della settimana precedente.

## 7. Trend
Incidenza sforamento/spesa merce mese per mese. Soglie **proposte**, non confermate su più clienti: 0,25% avviso, 0,35% non tollerabile. Conta anche quanti prodotti scivolano sopra il concordato nel tempo. Due avvertenze da dire sempre: la moda è costruita sul periodo osservato (quindi nei primi mesi ci sono pochi sforamenti per come è costruito il riferimento, non perché vada tutto bene) e le note di credito cadono nel mese in cui arrivano, non in quello della fattura originale.

## 8. Liste ordini per reparto dal listino
Raggruppate per fornitore attuale, **senza prezzi**, con giacenza e colonna "ordina" da compilare. I prodotti in comune fra reparti, poco usati, vanno in fondo (assenti da più di 60 giorni e da più del doppio dell'intervallo abituale, contati fino all'ultima fattura registrata). Agganciale all'inventario dei reparti (vedi `foodcost-cliente`). Una copia **riservata** al titolare porta prezzi e "dove conviene". Le liste ordini non cambiano mai fornitore da sole: ci possono essere premi contrattuali che la fattura non mostra (vedi SKILL.md, "Premi contrattuali e accordi").

## 9. Bolle settimanali quando le fatture arrivano in ritardo
Trascrizione delle scansioni: poche per volta, mezze pagine ad alta risoluzione, ogni documento controllato col suo totale. Filtra per data documento (le scansioni spesso contengono anche la settimana prima). "Documento omesso" = scansione mancante da chiedere. Un file per settimana (se esiste già, si aggiunge) con fornitore e numeri scritti **identici** fra una settimana e l'altra — altrimenti la deduplica raddoppia le righe. Omaggi e resi vanno come righe negative.

## 10. Limiti di lettura
Le bolle sono un **minimo** degli acquisti, mai il totale. Non calcolare mai un food cost % settimanale dalle sole bolle: il consuntivo si fa solo sul mese, con gli inventari (vedi `foodcost-cliente`).

## 11. Fonti dati
XML FatturaPA dal cassetto fiscale (vedi SKILL.md, "Come procurarsi gli XML"), API Fatture in Cloud (il token manuale non si riattiva col login web, c'è una quota oraria, ordina con `sort=-date`), bolle da gestionale del cliente. Cadenza tipica: bolle la domenica, controllo prezzi il lunedì.

## 12. Esempio e Definition of Done
- [ ] Listino concordato costruito e non sovrascritto da rigenerazioni successive
- [ ] Sforamento calcolato su valore netto ÷ quantità netta, mai su una riga sola
- [ ] Controllo settimanale eseguito con verifica della data dell'ultimo dato (non solo "zero segnalazioni")
- [ ] Mail al fornitore sempre in bozza, mandata dal consulente
- [ ] Liste ordini per reparto senza prezzi; copia con prezzi solo per titolare/consulente
- [ ] Bolle filtrate per data documento, mai usate per un food cost % settimanale

(contributo di Andrea Chirivì, Noolas, 07/09–12/10/2026. Soglie e tolleranze sono proposte da ritarare: serve un secondo cliente di riferimento e l'ok di Leo Franco, autore della skill ospite, prima di considerarle definitive.)
