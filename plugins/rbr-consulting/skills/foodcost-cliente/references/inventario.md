# Inventario: progetto del foglio, lettura di quello del cliente, controlli

Richiamato dai Prerequisiti di SKILL.md come input della caccia allo spreco (`references/caccia-allo-spreco-teorico-vs-reale.md`) e del FC consuntivo. Serve per il valore di magazzino (righe r8/r10 del CDG, vedi `crea-cdg-cliente` e `cdg-gruppo-bilanci-commercialista`) e per il consumo reale = inventario iniziale + acquisti dal 1° del mese − inventario finale, letto solo sul mese, mai sulla settimana. Inventario sempre al 1° del mese (la Mastermind RBR indica anche il 15 come secondo giro).

## 1. Progettare il foglio da zero
- Un foglio per reparto, righe fisse, **nomi di fattura** (così i pattern degli acquisti valgono anche per le giacenze) e una colonna per ogni data di conta.
- Una sola quantità nell'unità dichiarata: niente terne conf/pz/g che si prestano a errori di lettura.
- Colonna posizione, con le righe dello stesso prodotto sommate.
- Prezzo per unità (vuoto se l'unità di conta è diversa da quella di fattura, da completare dal catalogo).
- Riga 2 = valore totale calcolato (SUMPRODUCT prezzo × quantità).
- Colonne anagrafiche protette da modifica accidentale.
- Un LEGGIMI per i responsabili del conteggio: come trattare le confezioni aperte (decimali, es. mezzo sacco = 0,5), 0 è diverso da vuoto.
- Schede di carta per i reparti, **senza la colonna prezzo**, col numero di riga vero del foglio come prima colonna (per una trascrizione 1:1) — da rigenerare ogni volta che si aggiungono o tolgono righe.

## 2. Generare il file dal listino fatture
Una riga per prodotto col nome di fattura, l'unità d'acquisto e il prezzo per quell'unità preso dal catalogo del listino (vedi SKILL.md step 1). Un foglio per reparto, una colonna per ogni data.

## 3. Leggere un inventario già esistente del cliente
Gli inventari che arrivano dal cliente spesso hanno terne conf/pz/"grammi" dove i "grammi" sono in realtà kg, la data su una colonna centrale invece che in testata, colonne etichettate male o colonne spurie (es. una data ripetuta). Mappa foglio per foglio quale colonna corrisponde a quale data, e chiedi al titolare quali inventari considera validi prima di usarli.

## 4. Righe gemelle: il doppione vero e il doppione legittimo
Il doppione vero ha lo stesso nome **solo dopo la pulizia** (coda tipo "RIF. DDT", numero di lotto, unità scritta in due modi diversi come CF/CAR o PZ/PZ./pz.). Riconoscilo senza indovinare: stesso fornitore + stesso ultimo prezzo + stesso codice nel catalogo → allinealo a una sola riga e una sola unità. Una riga gemella **senza prezzo** vale 0 € nel valore di magazzino in silenzio: è uno degli errori più insidiosi, controllalo sempre (vedi punto 6).

### Più posizioni dello stesso prodotto: due disegni, da NON mischiare
- **(a) Riga sola con somma nella casella** (es. "5+15+20") e colonna TOTALE calcolata e protetta — disegno scelto come standard operativo.
- **(b) Sezioni per posizione**, dove il foglio somma i nomi identici — utile solo se si vuole seguire il giro fisico del locale.
Mischiare i due disegni nello stesso foglio è l'errore principale da evitare: con il disegno (a) la regola di conta è "conta tutto sulla riga N", non sparpagliare per posizione.

## 5. Valore di magazzino: le sue trappole
- SUMPRODUCT prezzo × quantità totale, non una somma manuale.
- Una riga senza prezzo vale 0 € **in silenzio** — va sempre controllata prima di consegnare.
- Un range di formula che si ferma all'ultimo prodotto storico lascia fuori le righe aggiunte in fondo dai reparti: verifica che il range copra anche le righe nuove.
- Unità diverse non si sommano: controlla che ogni riga sia nella sua unità dichiarata.

## 6. Due controlli da fare sempre prima di consegnare ai reparti
1. Nomi uguali dopo la normalizzazione, da classificare come al punto 4 (doppione vero o legittimo).
2. Prezzi vuoti: da riempire dal catalogo, oppure da dichiarare esplicitamente (es. prodotti che non si comprano più e restano solo a scaffale).

## 7. Regola di conta da dare al cliente
- Un prodotto, una sola unità: quella con cui lo si compra.
- Confezioni aperte coi decimali (es. mezzo sacco = 0,5).
- 0 non è "vuoto": vanno distinti.
- Più posizioni fisiche dello stesso prodotto si sommano in un'unica casella (vedi disegno (a) al punto 4).

## 8. Dopo la conta
- **Conta fatta dopo la data di riferimento**: corregila col venduto e le consegne del giorno di mezzo, in colonne separate (grezzo, rettifica, valore alla data).
- **Reparti che contano sul vecchio file**: riporta il conteggio convertendo le unità al nuovo foglio.
- **Test di completezza**: se dopo la data di conta si vende di un articolo più di (contato + comprato), la conta era incompleta — va rifatta, non accettata come scarto reale.

## 9. Locale stagionale
Inventario il giorno della chiusura, che diventa l'iniziale alla riapertura. Nell'ultima settimana i cartoni chiusi non si aprono e si rendono con nota di credito. ⚠️ Questo pattern è confermato su un solo caso cliente: trattalo come esempio operativo, non come regola valida per ogni locale stagionale senza riverificarlo.

## 10. Magazzino teorico infra-mese (fra due inventari) — metodo da verificare
Un magazzino teorico giorno per giorno fra due inventari (inventario validato del 1° + acquisti − consumo teorico per gruppo) è un'idea interessante ma **non ancora validata a regime** su un caso reale: non proporlo come metodo pronto, va prima provato. Quello che invece È confermato: i **moduli di magazzino dei gestionali vivono solo se qualcuno li alimenta davvero**. Si sono viste giacenze negative e personale allo 0% su un software di margine, e un modulo che scarica l'articolo di vendita anziché la materia prima comprata. **Non replicare mai un magazzino teorico giornaliero se il locale non fa inventari veri**: il dato uscirebbe fuori scala in modo silenzioso.

## Definition of Done
- [ ] Controlli del punto 6 fatti (nomi normalizzati, prezzi vuoti risolti)
- [ ] Valore per reparto riletto con le trappole del punto 5 verificate
- [ ] Colonna della data successiva pronta sul foglio
- [ ] Schede per i reparti rigenerate se sono cambiate le righe

(contributo di Andrea Chirivì, 2026-10-12 — Noolas 17/09/2026 e test di completezza su 7 Ponti 29/09/2026; cadenza 1°/15 del mese dalla Mastermind RBR)
