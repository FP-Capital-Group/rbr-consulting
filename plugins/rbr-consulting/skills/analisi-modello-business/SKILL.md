---
name: analisi-modello-business
description: Il "File 03" RBR — analisi del modello di business del ristorante con conto economico per fasce orarie e per reparto, per scoprire fasce/reparti in perdita e ridimensionare i turni. Usala quando un consulente dice "facciamo l'analisi modello di business", "il pranzo perde?", "conto economico per fasce orarie", "quanto rende il delivery/la sala", "ottimizziamo i turni sul venduto", "compila il file 03". Metodo: fatturato e ore per fascia → CE per fascia (ATTUALE vs OTTIMIZZATO) → KPI di produttività → proposta turni e saving annuo.
---

# Analisi modello di business (File 03)

## Perché esiste
Un conto economico annuale dice SE il ristorante guadagna; il File 03 dice **QUANDO e DOVE**: quale fascia oraria e quale reparto genera margine e quale lo brucia. Nei casi reali RBR il pattern ricorrente è che **il pranzo infrasettimanale è strutturalmente in perdita** (Dirigì: da −113 a −253 €/giorno) mentre la cena salva il conto — ma senza spaccare il CE per fasce non si vede. L'output è una proposta di turni ridimensionata sui volumi reali, con saving quantificato (Dirigì: €117k/anno stimati; Cartabianca: €578k/anno di rete).

## Quando usarla
- Il cliente "fattura ma non resta niente" e serve capire dove perde.
- Bisogna dimensionare/tagliare i turni sul venduto reale.
- Valutare una decisione strutturale per fascia: chiudere il pranzo, aprire il pomeriggio, introdurre la cucina, chiudere una saletta.

## Prerequisiti
- **Dati riconciliati** con la skill `riconciliazione-dati-cliente` (venduto, ore, costo personale — con scarti quantificati). MAI costruire il File 03 su dati non riconciliati.
- **Venduto per fascia oraria** (scontrini/coperti/fatturato per slot 30 min o per fascia) dal POS del cliente (es. Cassa in Cloud, iPratico, Zucchetti).
- **Ore lavorate per fascia e reparto** — ⚠️ baseline = **cedolini/ore reali**, non i turni teorici (lezione Cartabianca: la griglia dai cedolini è il dato vero).
- **Costo orario del personale**: costo pieno annuo ÷ ore. Multi-locale: usare il **costo orario medio ponderato di rete** per TUTTI i locali, per uniformità (Cartabianca: €18,09/h; indiretti ufficio/jolly esclusi).
- Template File 03: `03 Analisi Modello` in `_TEMPLATE`, ID `1WoxoChHbGjbF9irVkQWZhoaLiyztsc_g2WC11HrorSo`. Riferimento metodologico completo: template "Da Tito" `17uFEGIVldVtodMO-mpW7PbinEo5sgvS80BS_43Fum2s` e file "Analisi modello di business - Dirigì" `18cHQIYZp2kwzn_0mQVbkZkn3BEDmIxVNUqlhpVv9bqE`.
- Foglio condiviso Editor con `fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com`; scritture sempre con anteprima/dry-run prima.

## Procedura

### 1. Definisci fasce e periodi
- Fasce orarie standard File 03: **11-16 / 16-19 / 19-24** (pranzo / pomeriggio-aperitivo / cena). Variante Dirigì: 11:30-15:30 / 15:30-18:30 / 18:30-23:30. ⛔ Regola RBR: **non modificare la struttura fasce/reparti del template — solo i valori**.
- Reparti standard: **Pizzeria / Cucina / Sala** (adattare le etichette al locale: nei ristoranti Sala può includere bar/lavaggio come colonna separata).
- Se il business è stagionale, dividi l'anno in **blocchi di ricavo omogeneo** e costruisci un CE per blocco (metodo Jacopo su Dirigì: bassa stagione a 2 fasce · spalla estate a 3 fasce · alta estate a 3 fasce con volumi 2×): turni stabili per blocco, senza assumere/licenziare di continuo.

### 2. Costruisci il CE per fascia (blocco ATTUALE)
Per ogni blocco/periodo × fascia calcola: **fatturato, coperti, ore, operatori per reparto, costo personale, food cost (parametro 30% nel modello Dirigì), utenze, BEP, EBITDA di fascia**. Il margine netto per fascia (pranzo settimana / pranzo weekend / cena) è la tabella-verità dell'analisi: mostra subito quale fascia perde.

### 3. Calcola i KPI di produttività e fissa il target
- KPI cardine cucina/pizzeria: **piatti per operatore in 30 minuti**. Il valore migliore osservato nel locale stesso (Dirigì: 26 piatti/op/30min in cucina il sabato sera; 17 coperti/cameriere per 3 slot da 30min in sala) diventa il **target** per tutti gli altri turni.
- Variante heat-map per slot da 30 min (Cartabianca, bar e ristoranti): righe = scontrini, fatturato, operatori per reparto ATTUALI/OTTIMIZZATI/differenza, scontrini per operatore, costo, margine. **Criterio di taglio**: se uno slot ha ≥2 operatori E <5 scontrini a testa → −1 operatore (min 1). **Protezioni**: mai il primo slot attivo (apertura/prep) né gli ultimi 2 (chiusura); prima delle 07:00 nessun taglio; prima delle 15:00 mai sotto 2 operatori totali.
- ⚠️ **Ristoranti ≠ bar**: non dimensionare la preparazione sull'incasso orario. Le persone in cucina alle 16-19 con incasso ~0 sono la brigata in prep per la cena (lezione Tennis Cartabianca: taglio da €90k fasullo). I tagli in fasce a incasso ~0 vanno **flaggati PREP e validati col cliente**, non applicati. Confrontare il €/ora-uomo solo tra locali della **stessa tipologia** (bar con bar, ristoranti con ristoranti).

### 4. Costruisci il blocco OTTIMIZZATO
- Stessa struttura del blocco ATTUALE, con operatori ridimensionati al target. Pattern ricorrenti (Dirigì): cucina infrasettimanale da 2-3 → 1; sala compattata su 2-4 risorse tagliando i runner; sabato/domenica cena NON si toccano (sono il picco).
- Traduci i fabbisogni in **turni veri** (entrata-uscita, FT/PT): turni contigui, max 8h, min 3-4h, senza coprire ore a domanda zero. Le ore-costo si contano sui turni veri, non sulla somma teorica dei fabbisogni.
- **Saving = Δ EBITDA settimanale per fascia × settimane del blocco** (oppure turni tagliati/settimana × costo turno medio × settimane — Dirigì usava €85,35/turno). Le due strade devono tornare.

### 5. Decisioni strutturali per fascia
Con il CE per fascia si valutano a numeri le decisioni tipo:
- **Pranzo in perdita** → chiusura, riduzione organico minimo, o spinta asporto/convenzioni.
- **Introduzione cucina / nuovo reparto** → CE dedicato: costi extra (operatori, lavapiatti, alloggi…), BEP, scenari per crescita coperti. Dirigì: la cucina paga solo con **almeno +5% coperti**; sotto, è una perdita.
- **Saletta/area marginale** → peso % sul giro + MDC perso se si chiude.

### 6. Consegna e iterazione col cliente
- Compila il File 03 del cliente (copia del template, `03 Analisi Modello di Business - <CLIENTE>`) **solo nei valori**, con anteprima dei numeri prima di scrivere sul foglio. Registra l'ID nel Registry Clienti (`file_03_analisi_id`).
- Il file va reso **dinamico**: righe OTTIMIZZATO editabili dal cliente/consulente, totali e saving a formule (costo orario parametrico in una cella) — così il cliente può "mitigare" i tagli e i numeri si ricalcolano.
- ⚠️ Dopo la consegna **il file vive**: il cliente/Marco corregge a mano i valori OTTIMIZZATO. Ogni ricalcolo successivo deve partire dal **file live**, mai rigenerare da script sovrascrivendo le sue modifiche.
- Proponi sempre un **pilot di 2-3 settimane** sul taglio più grosso prima del rollout.

## Regole RBR & trabocchetti
- ⛔ MAI compilare senza riconciliazione (skill `riconciliazione-dati-cliente`); economici IVA esclusa (÷1,1).
- ⛔ Non modificare struttura fasce orarie/reparti del template — solo valori (regola File 03 nel master brain).
- ⚠️ I saving sono **indicativi** finché l'"attuale" non è payroll reale: dichiararlo nel deliverable.
- ⚠️ Non estrapolare l'estate (o il picco) a 12 mesi linearmente: analisi per stagione/blocco.
- ⚠️ Anomalie di €/h su singoli mesi (es. fine stagione con TFR/14ª accantonati) vanno isolate prima di usarle nella media.

## Lacune note (da completare con Marco)
- La **struttura interna del template** `03 Analisi Modello` (`1Wox…`: righe, colonne, formule) non è documentata nelle memory — solo le regole ("fasce 11-16/16-19/19-24, reparti Pizzeria/Cucina/Sala, non toccare la struttura") e i file applicati (Dirigì, Da Tito/Cartabianca). Prima del primo uso su un cliente nuovo, aprire il template con Marco e mappare i blocchi.
- I parametri standard (food cost 30%, costo turno €85,35, soglia 5 scontrini/operatore, turnover pranzo 1,5×/cena 2,5×) vengono dai casi Dirigì/Cartabianca: confermare con Marco se sono i default RBR o vanno tarati cliente per cliente.

## Definition of Done
- [ ] Fasce/blocchi/reparti definiti come da template, struttura non modificata
- [ ] CE ATTUALE per fascia con dati riconciliati (baseline = ore/cedolini reali)
- [ ] KPI target dal best interno del locale; tagli con protezioni (apertura/chiusura/prep/min organico)
- [ ] Tagli PREP flaggati e validati, non applicati d'ufficio
- [ ] Blocco OTTIMIZZATO a turni veri FT/PT + saving = Δ EBITDA × settimane (quadratura verificata)
- [ ] File 03 dinamico consegnato, ID nel Registry Clienti, pilot proposto
