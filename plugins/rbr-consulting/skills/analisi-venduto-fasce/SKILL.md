---
name: analisi-venduto-fasce
description: Analisi del venduto di un locale per giorno della settimana, fascia oraria, mese e categoria merceologica, partendo da qualunque export del gestionale di cassa (CSV, xls, report aggregati, chiusure mensili). Produce un Excel a 4 schede e una relazione PDF brandizzata RBR, con quadratura mese per mese contro il totale interno dell'export. Usala quando il consulente dice "analizza il venduto per fasce", "quanto incassa a pranzo e a cena", "venduto per giorno della settimana", "scontrino medio per fascia", "venduto per categoria", "prepara i dati per il File 03", "ho gli export della cassa, tirane fuori un Excel", o quando deve interrogare al tavolo col cliente un periodo o un giorno specifico.
---

# Analisi del venduto per fasce orarie

> Skill condivisa da Leo Franco il 2026-09-06.
> Nota dell'autore: trasforma gli export del venduto di un locale — qualunque sia il gestionale — in un Excel a 4 schede e una relazione PDF brandizzata RBR. Prepara i dati per il File 03 (analisi-modello-business) e per il conto economico, e serve al tavolo col cliente per interrogare un periodo o un giorno specifico. Verificata sul campo su Osteria, Pinocchio, La Talpa Trento, La Talpa Pergine, Da Giorgio.

## Cosa produce

1. **Excel a 4 schede**
   - **Riepilogo** per giorno della settimana, con blocchi mensili;
   - **Dettaglio fasce** (venduto, documenti, scontrino medio per fascia oraria);
   - **Fasce per mese**;
   - **Venduto per categorie merceologiche**, con quantità.
   - *(opzionale, se l'export ha l'ora di seduta per tavolo, es. iPratico)* **Rotazione
     tavoli**: per fascia di partenza, quanti tavoli vengono rivenduti nella stessa sera
     e quanto vale un tavolo a uno o due giri — utile per decidere quali fasce spingere.
     Accanto, leggi la permanenza media al tavolo insieme alle categorie "del tempo"
     (spina, cocktail, amari, dolci): il legame permanenza→secondo giro è un'ipotesi da
     verificare caso per caso, non una causa dimostrata. Rimando a
     `ottimizzazione-tavoli-resmio` per l'uso in sala. *(contributo di Andrea Chirivì,
     2026-10-12)*
   Si creano solo le schede per cui ci sono dati.
2. **Relazione PDF RBR** (header col logo, footer con numerazione pagine) —
   stile e regole di impaginazione come `relazione-rbr`.

A valle: i numeri per fascia alimentano il **File 03** (`analisi-modello-business`)
e la parte ricavi del **conto economico** (`crea-cdg-cliente`).

## Script (da chiedere a Leo)

Il contributo descrive tre script che **non sono arrivati nel pacchetto**:
`costruisci_excel.py` (costruttore Excel generico dal JSON normalizzato, crea solo
le schede che hanno dati), `relazione.py` + `rbr_relazione.py` (motore della
relazione PDF RBR via Chrome headless in DevTools Protocol: header col logo,
footer con numerazione, senza LibreOffice). Anche i **parser dei 4 formati già
risolti** (vedi sotto) stanno nella versione originale di Leo.
Vanno chiesti a Leo Franco e aggiunti in `scripts/`. Finché mancano: si segue il
metodo a mano (Python + openpyxl per l'Excel; per il PDF il motore di
`relazione-rbr`). Non inventare script con quei nomi.

Il costruttore di Leo è stato validato su La Talpa Pergine: ricostruendo il file
dal JSON normalizzato, le righe TOTALE di tutte e quattro le schede sono risultate
identiche a quelle del file costruito a mano.

## Metodo

1. **Chiedi al consulente** (in un solo messaggio): cliente, periodo, file o
   cartella, fasce orarie volute.
2. **Sfoglia TUTTI i file**, non solo quelli che sembrano utili. Attenzione: alcuni
   `.xml` sono definizioni di interrogazione del gestionale, non dati.
3. **Trova il riferimento di quadratura interno all'export**: chiusura mensile del
   registratore, riga TOTALI in fondo al CSV, "Totale Generale" del report.
   Confronta **mese per mese** e dichiara in nota ogni scostamento residuo.
4. **Normalizza tutto in un JSON comune**: da lì Excel e relazione escono sempre
   uguali, qualunque fosse il gestionale.
5. **Costruisci Excel e relazione** dal JSON.

**Regola d'oro: mai inventare un dato.** Se manca si chiede, e si propone sempre
la scelta fra file parziale subito o attesa dei dati completi.

Se il cliente usa iPratico, i dati si possono estrarre direttamente con
`estrai-dati-ipratico` (fasce orarie, prodotti, canali) invece di lavorare sugli
export.

## Formati già risolti (playbook)

| Formato | Caso di riferimento |
|---|---|
| Giorni × fascia | Osteria, Pinocchio |
| Righe di vendita | La Talpa Trento |
| Chiusure di cassa `.xls` con 3 layout diversi | Da Giorgio |
| Report già aggregati senza date | La Talpa Pergine |
| `.xls` che in realtà è HTML (iPratico Totalizzazioni e altri gestionali) | si legge con `pandas.read_html` (serve `html5lib`); per un `.htm` con la cartella `.fld` accanto, leggi `<nome>.fld/sheet001.htm`, non il file principale |

I parser relativi sono negli script di Leo (vedi sopra).

## Trappole documentate (tutte incontrate sul campo)

- **L'ora di cassa è quella di CHIUSURA del conto, non quella del lavoro**: verificato su
  Cassa in Cloud, dove sold-by-hour coincide riga per riga con le chiusure conto. Usata
  così com'è sposta la cena avanti di 1-1,5 ore e gonfia il "dopo le 23" coi conti pagati
  tardi (un caso: il post-23 passava dall'11,7% per chiusura al 2,9% per apertura).
  Prima di ogni analisi chiedi se l'orario è di apertura tavolo o di chiusura conto —
  su iPratico e altri gestionali la domanda va rifatta ogni volta, non si assume.
- **Acconti e buoni regalo**: righe con pochi pezzi e importi tondi non sono servizio, si
  tolgono dal venduto di fascia e si elencano fra le voci escluse.
- **Eventi chiusi in cassa la mattina dopo**: finiscono nel pranzo se non riportati alla
  sera dell'evento vero (un evento da 6.500€ chiuso alle 10 di domenica era la cena del
  sabato sera).
- **Giorni a locale chiuso o di sola cena**: restano fuori dal denominatore del pranzo.
- **Cassa in Cloud — filtro sold-trend-by-hour**: il filtro dashboard di default
  (idSharedBillReasonIsNull:true) esclude i conti divisi (anche ~13% del venduto, quasi
  tutto a cena): usa il filtro {document:true, refund:false, idSalesPoint:[id],
  referenceDatetimeFrom/To}, che quadra al centesimo col totale giornaliero. Per i
  coperti per ora, idDepartment va passato come array (come stringa dà errore 500).
- **Tasti fuori reparto ed errori di catalogo**: scorri reparti e categorie cercando
  articoli chiaramente fuori posto (es. pasta in "Aperitivi", salame in "Bibite"): finché
  restano lì ogni percentuale per reparto o categoria è falsata. Segnala al titolare e
  correggi in cassa; nel frattempo riclassifica nel JSON normalizzato e dichiaralo. I
  tasti di tracciamento dei menu fissi non si toccano.
- **Coperto non battuto e incasso senza nome prodotto**: confronta i pezzi del reparto
  COPERTO coi coperti veri del pannello e misura, per fascia, la % di scontrini senza
  coperto e quella di incasso senza nome prodotto (spesso concentrata a fine cena). I
  coperti per ora dal reparto COPERTO sottostimano: usali solo come distribuzione fra le
  fasce e riscalali sul totale ufficiale dei coperti. Nella scheda categorie dichiara la
  quota di incasso senza nome. In consegna riporta il valore del coperto non battuto
  (coperti non battuti × prezzo del coperto) e le due mosse operative: coperto sempre
  battuto, piatto sempre selezionato.
- **Incassi non battuti (comande cancellate)**: se il titolare segna a parte vendite non
  battute e in cassa cancella le comande, quegli incassi mancano dalle statistiche.
  Chiedili mese per mese (anche per l'anno precedente), sommali al venduto di cassa e
  ripartiscili per fascia/reparto in proporzione al battuto, dichiarandolo fra le
  assunzioni. Per il futuro consiglia al cliente "Archivia" invece di "Cancella"
  (gestionale GC5/GC Cloud) così la statistica resta. Gli extra pagati ai dipendenti si
  chiedono a parte: vanno nel personale, non nel venduto.
- **Righe cumulate salvate col nome di un giorno** (valore fuori scala rispetto
  agli altri) → ricostruisci il valore vero per differenza dalla chiusura mensile.
- **File "semplice" che duplica** la somma di pranzo+cena dello stesso giorno. Se
  invece affianca solo una "cena", quel file è il pranzo.
- **Colonne stampate senza funzione di aggregazione**: sulle righe di gruppo
  mostrano il valore di un singolo record, non un totale. Si riconoscono perché
  assurde (un giovedì da 8.827 documenti che "vale 1,00 euro"). Usa solo le colonne
  che sommano davvero.
- **Categoria "CONTO SEPARATO"** nei report per categoria: sono i conti divisi, già
  compresi nelle altre voci, e gonfiano il totale (a Pergine 76.754 euro su 460.469).
  Va esclusa.
- **Copie della stessa chiusura mensile in cartelle di altri mesi**, con dati
  diversi: vale solo quella nella cartella del proprio mese.
- **Export dei documenti troncato di un giorno** rispetto a quello del venduto
  (quasi sempre): controllalo e segnalalo.
- **Addestramenti / battute a nero**: se il loro importo è già dentro il totale
  giornaliero, il loro numero va sommato ai documenti, altrimenti lo scontrino medio
  esce gonfiato (convenzione confermata dal cliente Da Giorgio; su un cliente nuovo
  chiedere).
- **Giorni di chiusura**: se i dati hanno le date, i giorni assenti dal calendario
  vanno esclusi dai denominatori; se le date non ci sono, si usano i giorni di
  calendario e lo si dichiara.
- **Giorno "aperto" con pochissimi documenti e scontrino medio altissimo**: non è
  servizio, sono rifornimenti o eventi → classificali fuori dal venduto.

## Convenzioni

- **Le fasce seguono l'apertura del tavolo** (presa comanda), non la chiusura conto. Se
  il gestionale non la espone, riporta indietro le chiusure della durata media del
  servizio (circa 1h-1h30, da pannello Tavoli se disponibile) con una mappa
  chiusura→fascia dichiarata. Le battute tardive CON coperto sono cena, quelle SENZA
  coperto sono bar dopo-cena per ora di emissione. Conti ed eventi chiusi dopo
  mezzanotte (anche al mattino dopo) vanno al servizio della sera prima.
- **Tabacchi, sigarette e lotterie**: proponi sempre l'esclusione dal venduto. Sono
  rivendite a margine quasi nullo (a La Talpa Pergine il 30,2% della cassa) e
  falsano ogni indice di redditività. Restano in una colonna a parte per
  riconciliare col totale di cassa.
- **Percentuali delle categorie** sul venduto netto, non sul totale di cassa.
- **Scontrino medio ≠ venduto per coperto**: scontrino medio = venduto / documenti.
  In un bar un documento è un cliente, in un ristorante è un tavolo da 2-3 coperti.
  Non confonderli e dichiara quale stai usando.
- **Coperto medio = venduto ristorazione con coperti ÷ coperti del pannello ufficiale
  del gestionale**, letto mese per mese (è il numero che il cliente riconcilia da solo).
  MAI calcolarlo sui soli conti-tavolo col coperto battuto: è un campione parziale e
  sovrastima. Il coperto medio PER FASCIA non si mostra (il fatturato senza coperti lo
  falsa): resta solo sulla riga del totale. "Incasso/coperto" (fatturato totale ÷
  coperti) è un numero diverso: se serve nel CE si chiama così, al cliente si porta un
  numero solo. Non mischiare fonti nello stesso confronto (su Cassa in Cloud "Analisi di
  Periodo" ≠ "Venduto per Reparto") e cita sempre quella usata; su periodi lunghi
  global-stats va in timeout senza dare errore — leggi mese per mese e somma. Se i
  coperti si stimano come incasso ÷ spesa a coperto, usa la spesa dello STESSO periodo
  (mai di un'altra stagione) e dichiaralo.
- **Taglio di fascia a metà di una mezz'ora già aggregata**: riproporziona sul
  venduto di quella mezz'ora e dichiara l'approssimazione.

## Confronti fra periodi

Prima di commentare un calo o una crescita, quattro passaggi *(contributo di Andrea
Chirivì, 2026-10-12)*:
1. **Normalizza per calendario**: confronta solo mesi interi in entrambi gli anni e
   conta i giorni della settimana (due venerdì contro uno può spiegare da solo un calo a
   doppia cifra). Escludi i mesi incompleti.
2. **Scomponi per fascia oraria** e controlla se è cambiato l'orario di apertura/chiusura
   del locale: un calo annuo può stare tutto in una fascia che ha smesso di esistere.
3. **Scomponi la spesa a coperto in cucina e bere**, e leggi il mix per categoria: le due
   voci possono muoversi in direzioni opposte e nascondersi a vicenda nella media.
4. **Chiedi se nel frattempo sono cambiati gestione, staff, menu o orari**: in quel caso
   si stanno confrontando due aziende diverse, non due periodi dello stesso locale.

## Come si leggono i risultati

*(contributo di Andrea Chirivì, 2026-10-12)* La skill produce già scontrino medio per
fascia e per giorno, ma vanno letti coi pattern visti sul campo:
- **Due locali nello stesso locale**: pranzo = volume (tanti scontrini piccoli), sera =
  valore (pochi scontrini alti, soprattutto fra le 21 e le 23). Decidi cosa spingere in
  base a questo, fascia per fascia.
- **Fasce morte**: vanno portate al File 03 (`analisi-modello-business`).
- **Giri = coperti al giorno ÷ posti**, con controllo di quali sale compaiono davvero in
  cassa (una sala può non comparire mai separata dalle altre).
- **Settimana piatta = locale di vacanzieri**: se i coperti non calano nei giorni
  "deboli" tipici, non proporre promozioni per "riempire l'infrasettimanale" — è già
  pieno come il weekend.
- **Le serate con evento sono un altro locale**: escludile dalle medie degli altri giorni
  e analizzale a parte (anche il giorno critico dove servono più coperti).

## Consegna

Excel + PDF al consulente, con in chiusura: quadratura mese per mese (e scostamenti
residui), voci escluse dal venduto (tabacchi, conto separato, eventi/rifornimenti,
**acconti e buoni regalo**) con importi, il **valore del coperto non battuto**, e le
assunzioni dichiarate (giorni di chiusura, addestramenti, incassi non battuti sommati,
riproporzionamenti di fascia). *(contributo di Andrea Chirivì, 2026-10-12)*
