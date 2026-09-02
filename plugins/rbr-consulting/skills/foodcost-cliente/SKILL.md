---
name: foodcost-cliente
description: Il "File 02" RBR — analisi Food Cost del cliente per categoria e per piatto, versione Attuale vs Nuovo, con margine unitario e food cost %. Usala quando un consulente dice "facciamo il food cost di X", "compila il file 02", "quanto margina questo piatto", "food cost attuale vs nuovo", "aggiorna il listino ingredienti", "confronta i prezzi ingredienti con le fatture". Costruisce listino ingredienti → ricette/distinte base → costo porzione → margine per piatto → incrocio col venduto, e prepara la classificazione per il menu engineering.
---

# Food Cost cliente (File 02)

## Perché esiste
Il food cost è il costo variabile più grande e più manipolabile del ristorante, e quasi sempre il ristoratore lo conosce "a sensazione". Il File 02 mette in fila **quanto costa davvero ogni piatto e quanto margina**, in doppia versione **Attuale vs Nuovo** (ricetta/prezzo di oggi vs proposta). Trabocchetto reale: i listini ingredienti invecchiano in fretta — su Raices i prezzi in scheda erano sotto del 37-63% rispetto alle fatture reali (petto pollo +46%, edamer +63%, farina 2×) → food cost dei piatti sottostimato e decisioni sballate. Il confronto con le fatture vere è parte del metodo, non un extra.

## Quando usarla
- Onboarding cliente: serve il File 02 Food Cost compilato.
- Revisione prezzi/ricette ("il commercialista mi chiede il food cost").
- Prima di un menu engineering (il food cost per piatto è input obbligatorio della skill `menu-engineering`).
- Verifica periodica listino ingredienti vs prezzi reali di acquisto.

## Prerequisiti
- **Dati riconciliati** con la skill `riconciliazione-dati-cliente` (fatture acquisti, venduto per articolo). MAI compilare il CDG o il File 02 con dati non riconciliati.
- Dal cliente: **ricette con grammature** (distinta base per piatto: ingrediente, quantità, sfrido). Se mancano → file "grammature da compilare" per i responsabili (pattern Cartabianca: 1 blocco per prodotto, colonne Categoria · Prodotto · Ingrediente · Grammatura stimata · Unità · Grammatura reale da compilare · Note; coprire i prodotti ≥300 pz/anno = ~98% dei pezzi venduti).
- **Venduto per articolo** (unità e prezzi) dal POS, per la parte Attuale e per pesare i margini.
- **Fatture di acquisto** (XML AdE con righe di dettaglio) per il listino reale — estrazione righe prodotto dagli XML/p7m (pattern Raices: 1.137 fatture food → 18.085 righe prodotto → €/kg reale per ingrediente).
- Template: `02 Food Cost` in `_TEMPLATE`, ID `1bjB4ifLTxDClaa7GV0HsMwTq0schxmoX`. Fogli del cliente condivisi Editor con `fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com`; ogni scrittura preceduta da anteprima/dry-run.

## Struttura del File 02 (dal template e dai casi reali)
- **Tab "Food Cost"**: listino ingredienti (blocchi in colonne A/D/G/J/M nel file Raices) + **ricette** con costo porzione calcolato dalle grammature.
- **Tab per categoria** (Categoria 1-6; esempi dal master brain: Panini, Pizzette, Fainè, Patate, Dolci, Bibite): per ogni piatto la doppia versione **Attuale e Nuovo** con colonne chiave **Prezzo IVA inclusa · Food Cost € · Food Cost % · Margine Unitario · Unità vendute**.
- **Tab "Listino Fatture"** (aggiunta RBR, pattern Raices): confronto ingrediente per ingrediente tra prezzo in scheda e **€/kg reale dalle fatture**, con Δ>25% evidenziato in rosso.

## Procedura

### 1. Listino ingredienti reale
Estrai le righe prodotto dalle fatture XML del cliente e calcola il **€/kg (o €/unità) reale** per ingrediente. Compila la tab "Listino Fatture" con il confronto scheda vs reale (Δ>25% in rosso). Aggiorna il listino della tab "Food Cost" con i prezzi reali confermati — segnala al consulente ogni scostamento grosso prima di aggiornarlo.

### 2. Costo porzione (versione Attuale)
Per ogni piatto: somma `grammatura × €/kg` degli ingredienti della distinta base = **Food Cost €**. Esempio di calcolo validato (Mister Pizza, Margherita): panetto 300g×1,90 + pomodoro 90g×1,31 + mozzarella 100g×5,63 + olio 10g×5,42 + basilico 3g×19,30 = **€1,36**.
- **Prezzo netto = Prezzo menu IVA inclusa ÷ 1,1** (ristorazione).
- **Margine unitario € = prezzo netto − food cost €** · **Food Cost % = food cost ÷ prezzo netto** (Margherita: 8,70 → netto 7,91, margine 6,55, FC 17,24%).
- Grammature: dove possibile confrontare **peso reale verificato in cucina vs scheda** (pattern Cartabianca "Scheda Pezzature": porzioni fuori controllo fino a +67% vs sistema = food cost reale ben oltre la ricetta).

### 3. Incrocio col venduto
Compila le tab Categoria con le **unità vendute** per piatto dal POS. Ora ogni piatto ha popolarità e margine: è la base della **matrice Kasavana-Smith** (Star / Plowhorse / Puzzle / Dog — alto/basso margine × alta/bassa popolarità) e dei 5 pilastri RBR del menu engineering. Per la classificazione e il redesign del menu passa alla skill `menu-engineering` (regola RBR: prima si classificano i piatti, poi si decide il layout).
- Controllo di coerenza top-down: FC% teorico dal mix venduto vs **FC% di bilancio dal CDG (Acquisti/Ricavi)**. Se il bilancio è molto sopra il teorico, il problema non è il menu ma le **operations** (sfridi, porzioni, acquisti, ammanchi) — finding chiave Cartabianca: FC teorico piatto 23-27% su tutti gli store, bilancio da 21,6% a 42,4%.

### 4. Versione "Nuovo"
Per ogni categoria compila il blocco Nuovo con le proposte: ricetta rivista (grammature/sfridi), prezzo ritoccato, piatto sostituito. Stesse colonne (Prezzo IVA inclusa, FC €, FC %, Margine unitario) così il confronto Attuale vs Nuovo è cella a cella. Ogni proposta va motivata dai numeri dello step 3 (es. Plowhorse: porzione ridotta o prezzo +2-3%).

### 5. Consegna
- Anteprima dei valori al consulente/cliente prima di scrivere sul foglio; poi scrittura e verifica.
- Registra l'ID nel **Registry Clienti** (`file_02_food_cost_id`).
- Ricontrollo periodico: il listino ingredienti va riallineato alle fatture (step 1) a ogni aggiornamento di stagione/listino fornitori.

## Regole RBR & trabocchetti
- ⛔ MAI compilare senza riconciliazione (skill `riconciliazione-dati-cliente`).
- ⚠️ Economici sempre IVA esclusa: margini calcolati sul **prezzo netto** (÷1,1), il prezzo IVA inclusa resta solo come colonna di listino.
- ⚠️ Listini ingredienti in scheda quasi sempre vecchi → mai fidarsi senza il confronto fatture (step 1).
- ⚠️ Le "lavorazioni" (es. panetto pizza) sono a loro volta ricette: il costo va risolto a cascata sul listino, non lasciato a zero.
- ⚠️ Menu composti/menu fissi (Experience, convenzioni): il POS spesso non ha il costo per il prodotto composto → costo da compilare a mano dalla distinta.
- ⚠️ Non sovrascrivere tab/valori compilati a mano dal cliente; se il File 02 è un xlsx su Drive, export per ID + modifica openpyxl preservando le formule + update in place.
- Benchmark FC% di settore per categoria: utilizzabili come stima iniziale quando mancano le ricette (metodo Cartabianca), da dichiarare come stima e raffinare coi costi reali.

## Lacune note (da completare con Marco)
- La **struttura interna del template** `02 Food Cost` (`1bjB…`: layout esatto delle tab Categoria, formule Attuale vs Nuovo) non è mappata nelle memory — documentate le colonne chiave (master brain) e la struttura del file Raices (tab Food Cost + Categoria 1-6 + Listino Fatture). Prima del primo uso, aprire il template e mappare i blocchi.
- Il **target FC%** RBR per tipologia di locale non è documentato (nel File 03 di Dirigì si usa un parametro F.C. 30%): confermare con Marco i target standard.
- Gestione **sfridi** nelle distinte: citata nei fogli Shohreh (Mister Pizza) ma senza regola documentata di calcolo — chiedere il metodo.

## Definition of Done
- [ ] Listino ingredienti confrontato con €/kg reale da fatture (tab Listino Fatture, Δ>25% flaggati)
- [ ] Costo porzione da distinta base per ogni piatto; prezzi netti ÷1,1
- [ ] Tab Categoria con Attuale completo (FC €, FC %, margine, unità vendute)
- [ ] Coerenza FC teorico vs FC di bilancio dal CDG verificata e commentata
- [ ] Blocco Nuovo compilato con proposte motivate dai numeri
- [ ] Anteprima prima di ogni scrittura; ID nel Registry Clienti
