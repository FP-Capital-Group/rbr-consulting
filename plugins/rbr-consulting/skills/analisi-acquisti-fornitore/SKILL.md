---
name: analisi-acquisti-fornitore
description: Legge le fatture elettroniche (XML FatturaPA, anche .p7m firmate) ricevute da uno o più fornitori di un ristorante cliente e produce un'analisi acquisti dettagliata in Excel — riepilogo, prezzi/quantità storico mensile, resi, dettaglio righe, confronto col prezzo di mercato e, con più fornitori, un confronto incrociato dei prodotti comprati da entrambi. Usa SEMPRE questa skill quando l'utente chiede di "analizzare le fatture di un fornitore", fare un "riepilogo acquisti/spesa" da un fornitore, capire "quanto sto pagando" un prodotto o se un fornitore "mi sta caricando i prezzi", confrontare più fornitori sugli stessi prodotti, o quando fornisce una cartella di fatture XML/p7m e chiede di "tirarne fuori un excel". Non usare per il File 02 Food Cost completo (ricette/margini per piatto — quello è `foodcost-cliente`) né per caricare i totali fattura nel CDG "Economico" (quello è `cdg-fatture`): questa skill guarda UN fornitore alla volta in profondità, articolo per articolo.
---

# Analisi acquisti fornitore

> Skill condivisa da Leo Franco il 2026-09-11.
> Nota dell'autore: legge fatture XML/p7m FatturaPA di uno o più fornitori e produce un'analisi acquisti dettagliata in Excel (riepilogo, storico prezzi/quantità mensile, resi, dettaglio righe, confronto col prezzo di mercato via ricerca web, confronto incrociato tra fornitori sugli stessi prodotti). Costruita e verificata in una sessione reale su 2 clienti (Resilienza con il fornitore Pregis; Lyevito con 5 fornitori: PGS Catering, PGS Prodotti Gastronomici, Rovagnati, Vera Food, Greci, Menù).

Un ristoratore o un consulente vuole sapere, per un fornitore specifico:
quanto ha speso, quali prodotti sono aumentati, quanti resi ha subito, e se
sta pagando un prezzo in linea col mercato. Le fatture elettroniche
contengono già tutto questo, riga per riga — questa skill lo estrae e lo
mette in un Excel leggibile, invece di lasciarlo sepolto in centinaia di XML.

## Prerequisiti

- Le fatture del cliente: cartella con file `.xml` e/o `.p7m` (FatturaPA).
  Chiedi dove sono se non è chiaro. Vanno bene sia export SDI grezzi che
  cartelle già organizzate dal consulente.
- Python con `openpyxl` (nessuna altra dipendenza; `.p7m` si decodifica con
  `openssl`, già presente su macOS/Linux).
- Tutti gli script sono in `scripts/` di questa skill; nel resto del
  documento `$SKILL` indica la cartella di questo SKILL.md.

## Procedura

### 1. Identifica il fornitore reale (mai dal nome del file)

```
python3 "$SKILL/scripts/estrai_fornitori.py" "<cartella fatture>" --json /tmp/fornitori.json
```

**Perché non fidarsi del nome del file**: il prefisso del filename FatturaPA è
di solito l'`IdentificativoTrasmittente` — l'intermediario SDI che ha
inoltrato la fattura — non il P.IVA del fornitore. In una cartella con
fatture di più fornitori, decine di mittenti completamente diversi possono
condividere lo stesso intermediario e quindi lo stesso prefisso file, mentre
un singolo fornitore può usare intermediari diversi in momenti diversi. Lo
script legge sempre `CedentePrestatore` dal CONTENUTO di ogni fattura.

Lo script stampa una tabella (P.IVA, denominazione, N. documenti, periodo)
ordinata per rilevanza. **Mostrala all'utente prima di proseguire.** Se:
- un nome compare due volte con P.IVA diverse (es. "PGS Catering & Service"
  e "PGS Prodotti Gastronomici" — sono capitati entrambi in una sessione
  reale, entità separate) → chiedi con AskUserQuestion quale intende, o se
  vuole entrambe;
- un fornitore atteso non compare, o compaiono nomi mai sentiti → segnalalo,
  non ignorarlo silenziosamente (`estrai_fornitori.py` elenca a parte anche i
  file che non è riuscito a leggere: controllali, spesso sono `.p7m`
  danneggiati o metadati).

Il JSON salvato (`piva -> lista file`) è l'input dello step successivo.

### 2. Costruisci l'analisi per ciascun fornitore confermato

```
python3 "$SKILL/scripts/costruisci_analisi.py" "<cartella>" --lista-file /tmp/file_fornitore_X.txt \
    --fornitore "RAGIONE SOCIALE" --piva 01234567890 --cliente "NOME CLIENTE" \
    --out Analisi_Acquisti_<FORNITORE>.xlsx
```
(estrai la lista file per il fornitore scelto dal JSON di `estrai_fornitori.py`
e salvala come .txt, una riga per file — oppure passa i nomi file
direttamente come argomenti posizionali se sono pochi).

Un file per fornitore è quasi sempre la scelta giusta (il consulente li apre
uno alla volta, e ogni foglio "Confronto Mercato" ha una lista di prodotti
diversa) — usa un solo workbook multi-fornitore solo se l'utente lo chiede
esplicitamente.

Lo script produce 6 fogli — **Riepilogo Fornitore, Articoli, Storico Prezzi,
Storico Quantità, Resi - Note di credito, Dettaglio Righe** — e stampa un
riepilogo a schermo. Se segnala documenti con scostamento tra imponibile
dichiarato e somma delle righe (di solito <1%, spesso uno sconto finanziario
di fattura tipo "pagamento anticipato" non legato a un prodotto specifico),
è normale: lo script lo esclude correttamente dal dettaglio articoli ma lo
riporta come nota di trasparenza nel foglio Riepilogo — non un bug da
correggere, ma spiegalo al consulente se chiede perché i totali non tornano
al centesimo con il totale fattura.

Come lo script tratta i dati (non serve rileggerlo, ma utile per rispondere
a domande): righe di fattura (TD01/TD24) alimentano Storico Prezzi/Quantità e
la parte "acquisti" di Articoli; note di credito (TD04) alimentano il foglio
Resi e la parte "netta" di Articoli, mai mescolate alle medie mensili.
Prezzi presi da `PrezzoTotale` (già scontato, sconti a cascata inclusi), mai
da `PrezzoUnitario` grezzo. Descrizioni ripulite da entità XML doppiamente
escappate e da duplicazioni/troncamenti del campo `<Descrizione>` (visti su
più fornitori — gestiti automaticamente, non serve intervenire).

**Righe di rettifica non-prodotto** (es. "ABBUONO COMMERCIALE", "SCONTO
STRIKE" con importo negativo, viste su fornitori di salumi) compaiono come
articoli a sé nel foglio Articoli, perché raggruppare per codice+descrizione
le tiene naturalmente separate dai prodotti veri. È corretto: segnalalo al
consulente ("il fornitore applica sconti a riga separata, già dentro il
totale netto"), non filtrarle via silenziosamente.

### 3. Confronto con il mercato (foglio "Confronto Mercato")

**Questo step non ha uno script che fa la ricerca**: la ricerca dei prezzi di
mercato è il passo "manuale" della skill, fatto da Claude con agenti di
ricerca web (punti 1-2). Lo script `integra_mercato.py` arriva solo dopo
(punto 3) e si limita a leggere il JSON prodotto dalla ricerca e a scrivere i
fogli "Confronto Mercato" e "Fonti e Metodo".

Salta questo step se l'utente vuole solo i dati interni (più veloce). Se lo
vuole:

1. Apri il foglio "Articoli" appena creato, prendi i prodotti a maggiore
   spesa nel periodo (colonna "Importo acquisti €"), escludendo righe di
   servizio (trasporto, bolli, abbuoni). 8-12 articoli per fornitore è un
   buon compromesso.
2. Per ogni fornitore del batch, lancia UN Task/agente di ricerca in
   **parallelo** (non in sequenza — con più fornitori il tempo si
   moltiplica) seguendo il template in
   `references/prompt_ricerca_mercato.md`: elenca i prodotti con
   descrizione/unità/prezzo pagato, chiedi un JSON con schema fisso
   (descrizione, prezzo_attuale, unita, prezzo_mercato o null, valutazione,
   fonte, tipo_fonte, url, data_rilevazione, affidabilita, note). Mai
   inventare prezzi: un `prezzo_mercato: null` con nota è un risultato
   valido, un numero a caso no.
3. Salva l'output di ogni agente in un file JSON, poi:
   ```
   python3 "$SKILL/scripts/integra_mercato.py" Analisi_Acquisti_X.xlsx mercato_X.json --mese-rif Giu-26
   ```
   Lo script fa da solo il match fuzzy tra le descrizioni scritte
   dall'agente e quelle del foglio Articoli (non sono mai identiche
   carattere per carattere), recupera quantità/spesa del periodo, calcola
   Diff €/%, Impatto sul periodo e Valutazione (soglia ±8%: sopra/in
   linea/sotto mercato), e scrive anche il foglio "Fonti e Metodo" con le
   fonti deduplicate. Se un batch di ricerca copriva più fornitori insieme,
   lo script scarta da solo le righe che non appartengono a QUESTO
   fornitore (stampa un avviso, verifica che abbia senso).
4. **Leggi le note prima di riportare le valutazioni al consulente**: molti
   benchmark trovati online sono prezzi al dettaglio o di un altro
   marchio/formato, non un vero listino ingrosso HORECA per lo stesso
   prodotto — un "SOTTO MERCATO" ottenuto così è quasi sempre atteso (l'
   ingrosso costa meno del dettaglio) e non un vero risparmio da segnalare
   con enfasi; un "SOPRA MERCATO" con affidabilità Alta/Media, invece, è un
   segnale concreto da portare al consulente.

### 4. Con più fornitori: confronto incrociato

Se il batch ha più fornitori, cerca prodotti uguali o comparabili comprati
da più di uno:
```
python3 "$SKILL/scripts/candidati_incrocio.py" Analisi_Acquisti_A.xlsx Analisi_Acquisti_B.xlsx [...]
```
Ti dà CANDIDATI (match testuale), non certezze: uno score alto tra due
descrizioni che condividono solo parole generiche ("olio", "pomodoro") è
spesso un falso positivo, mentre un match anche solo discreto tra nomi
prodotto specifici è spesso vero. Guarda ogni candidato a occhio prima di
metterlo nel confronto finale, e **normalizza sempre alla stessa unità** se
le confezioni differiscono (es. prodotto A venduto a 500g e prodotto B a
660g: confronta €/kg, non €/pezzo — altrimenti si rischia di dire che A è
più economico solo perché la confezione è più piccola). Presenta i match
confermati in un foglio o file a parte "Confronto Fornitori", evidenziando
il prezzo più conveniente per ciascun prodotto.

### 5. Consegna

Manda i file Excel all'utente (un file per fornitore + l'eventuale
"Confronto Fornitori"). Nel messaggio di chiusura riassumi: spesa totale nel
periodo, punti "sopra mercato" con affidabilità Alta/Media da verificare col
fornitore, ed eventuali anomalie di dati segnalate durante la costruzione
(scostamenti imponibile, righe di rettifica, documenti non leggibili).

## Rapporto con le altre skill

- **`cdg-fatture`**: anche lei legge XML/p7m FatturaPA (`estrai_fatture_xml.py`,
  per dividere i totali fattura fra punti vendita), ma lavora a livello di
  **documento** (imponibile/IVA per fornitore e categoria → foglio Economico
  del CDG). Questa skill lavora a livello di **riga articolo** di un singolo
  fornitore. Stessi file in ingresso, output diversi: non usarle una al posto
  dell'altra. Il parsing XML/p7m è duplicato nei due script (`fatture_lib.py`
  qui, `estrai_fatture_xml.py` lì): se si corregge un bug di lettura FatturaPA
  in uno, controllare anche l'altro.
- **`foodcost-cliente`**: i prezzi puliti per articolo usciti da qui (foglio
  Articoli / Storico Prezzi) sono un buon ingresso per aggiornare i costi
  materie prime del File 02.



Se il cliente fornisce le fatture solo come PDF (scansioni o export senza
XML/p7m allegato — capita con alcuni fornitori grandi) e non hai il file
elettronico originale, il parsing riga per riga automatico non è possibile:
serve estrarre il testo del PDF e riconoscere le righe a mano (più lento, più
soggetto a errori di lettura numerica — controlla sempre i totali per
documento contro l'imponibile dichiarato nel PDF). Preferisci sempre chiedere
se esistono gli XML originali (spesso sì, anche quando il consulente ha solo
i PDF a portata di mano) prima di imboccare questa strada più lenta.
