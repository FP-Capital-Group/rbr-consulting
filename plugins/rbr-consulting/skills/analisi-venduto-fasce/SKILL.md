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

I parser relativi sono negli script di Leo (vedi sopra).

## Trappole documentate (tutte incontrate sul campo)

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

- **Tabacchi, sigarette e lotterie**: proponi sempre l'esclusione dal venduto. Sono
  rivendite a margine quasi nullo (a La Talpa Pergine il 30,2% della cassa) e
  falsano ogni indice di redditività. Restano in una colonna a parte per
  riconciliare col totale di cassa.
- **Percentuali delle categorie** sul venduto netto, non sul totale di cassa.
- **Scontrino medio ≠ venduto per coperto**: scontrino medio = venduto / documenti.
  In un bar un documento è un cliente, in un ristorante è un tavolo da 2-3 coperti.
  Non confonderli e dichiara quale stai usando.
- **Taglio di fascia a metà di una mezz'ora già aggregata**: riproporziona sul
  venduto di quella mezz'ora e dichiara l'approssimazione.

## Consegna

Excel + PDF al consulente, con in chiusura: quadratura mese per mese (e scostamenti
residui), voci escluse dal venduto (tabacchi, conto separato, eventi/rifornimenti)
con importi, e le assunzioni dichiarate (giorni di chiusura, addestramenti,
riproporzionamenti di fascia).
