---
name: analisi-acquisti-fornitore
description: Legge le fatture elettroniche (XML FatturaPA, anche .p7m firmate) ricevute da uno o più fornitori di un ristorante cliente e produce un'analisi acquisti dettagliata in Excel — riepilogo, prezzi/quantità storico mensile, resi, dettaglio righe, confronto col prezzo di mercato e, con più fornitori, un confronto incrociato dei prodotti comprati da entrambi. Usa SEMPRE questa skill quando l'utente chiede di "analizzare le fatture di un fornitore", fare un "riepilogo acquisti/spesa" da un fornitore, capire "quanto sto pagando" un prodotto o se un fornitore "mi sta caricando i prezzi", confrontare più fornitori sugli stessi prodotti, "controllo prezzi settimanale", "prezzi concordati", "il fornitore ha alzato", "listino fornitori", "liste ordini per lo staff", "trascrivi le bolle", o quando fornisce una cartella di fatture XML/p7m e chiede di "tirarne fuori un excel". Non usare per il File 02 Food Cost completo (ricette/margini per piatto — quello è `foodcost-cliente`) né per caricare i totali fattura nel CDG "Economico" (quello è `cdg-fatture`): questa skill guarda UN fornitore alla volta in profondità, articolo per articolo — tranne nella Modalità 2 (controllo ricorrente), che segue più fornitori insieme.
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

### Come procurarsi gli XML riga per riga
- **Cassetto fiscale AdE**: Fatture e Corrispettivi → Consultazioni e download massivi → ricerca **ESTESA** per periodo → fatture ricevute → file fattura. Esce uno zip misto (XML in chiaro, `.xml.p7m`, un `_metaDato.xml` per fattura) da scompattare e passare a `estrai_fornitori.py`, che scarta da solo i metadati e apre i p7m. La ricerca "puntuale" serve solo con gli id SdI già noti. È la via standard per un cliente senza gestionale fatture. Login del consulente o del cliente.
- **Aruba Fatturazione Elettronica**: login del consulente. Dalla console della pagina, `POST /services/FatturaRicevutaFrontEnd/advancedSearch` (con `AnnoFiscale`, `PageNumber`, `PageSize≤2000`) dà l'elenco; `POST /services/FatturaRicevutaFrontEnd/ExtractXmlInvoiceReceived` (con `Id`) dà l'XML in base64 nel campo `Content`. Va chiamato con `Ext.Ajax.request` (un `fetch` nudo dà 401) e decodificato con `atob` + `TextDecoder`. L'output del tool JS si tronca a ~1.000 caratteri: salva gli XML (o un TSV) come download di un Blob, non leggerli dall'output troncato.
- **Fatture in Cloud**: le note sul token manuale e sugli endpoint delle righe sono nel repo privato `rbr-suite` ma non erano installate nel plugin — vedi "Modalità 2" più sotto per i dettagli di autenticazione e limiti.

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

Nota sui nomi: il prodotto che il titolare cita a voce col marchio commerciale può avere un altro nome e un altro fornitore (il distributore) in fattura — es. un nome detto a voce può corrispondere a un marchio diverso di un altro distributore, con un nome tutto diverso in fattura. Per trovarne il costo cerca per distributore e formato nelle righe fattura, e se non torna chiedi al titolare: una trascrizione vocale può storpiare ancora di più il nome.

### 1-bis. Mappa della spesa (prima di scendere sul singolo fornitore)
Prima di analizzare un fornitore in profondità, uno sguardo d'insieme evita di perdere il quadro generale:
- **Spesa per fornitore anno su anno**: chi esce, chi entra, e la crescita degli acquisti contro quella dei ricavi. Un food cost che sale può spiegarsi con un cambio di fornitori (fornitori usciti e fornitori nuovi entrati con prezzi diversi) più che con un rincaro sui prodotti esistenti.
- **Canale d'acquisto**: conta le fatture da supermercato/cash&carry (numero, frequenza, importo medio). Molte fatture piccole e frequenti (es. una ogni 1-2 giorni, media ~200 €) indicano acquisti senza programmazione pagati a prezzi di dettaglio — il rimedio passa dal menu (meno referenze, piatti fissi, acquisto a bancale: rimando a `menu-engineering`). Se il supermercato è del gruppo, guarda il prezzo di trasferimento.
- Quando il food cost di bilancio è sopra il teorico (controllo top-down di `foodcost-cliente`), questa mappa è il primo controllo sul fronte acquisti.

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

**Prezzo effettivo = valore netto ÷ quantità netta, mai una riga sola.** Il
prezzo effettivo di un prodotto presso un fornitore è `(importo fatturato −
note di credito − righe negative/abbuoni dello stesso prodotto) / (quantità
fatturata − quantità accreditata)`, sul periodo. Uno sforamento o un rincaro
non si segnala mai leggendo una singola riga: una riga isolata sopra il
concordato può nascondere un prezzo medio del periodo in linea, se c'è un
accredito successivo che la compensa. Occhio anche agli **omaggi in natura**
(es. un cartone omaggio ogni N): l'omaggio entra nella quantità, quindi il
prezzo unitario reale è `pagato / (pagati + omaggi)`, da calcolare prima di
segnalare un rincaro. Nota per lo script: righe con `PrezzoTotale < 0`
dentro un documento TD01 sono un accredito e andrebbero sottratte dalla
quantità/importo acquistati (non sommate) e abbinate al prodotto per
`CodiceArticolo` — comportamento da verificare e correggere con un test su
un XML reale che contenga questo caso prima di toccare
`costruisci_analisi.py`, non applicare la correzione alla cieca.
Nello Storico Prezzi e nel calcolo dei rincari conta il **prezzo netto del
periodo**: su una finestra corta (es. 8 giorni) una nota di credito non
ancora arrivata può far sembrare sforato un prodotto che non lo è.

**Pulizia di nomi e righe prima di confrontare i prezzi**:
- togli il riferimento DDT in coda al nome articolo (es. pattern tipo "RIF.
  DDT …") prima di raggruppare per prodotto — altrimenti ogni consegna
  diventa un articolo "nuovo" e lo Storico Prezzi si spezza;
- togli codici lotto e sigle ingredienti dentro il nome, altrimenti un
  prodotto diventa più voci distinte;
- se confronti con un listino o un file esterno, applica la **stessa
  normalizzazione su entrambi i lati** (spazi multipli, maiuscole,
  unescape delle entità HTML tipo `&apos;`/`&amp;`): senza, prodotti scritti
  in modo leggermente diverso escono dal controllo in silenzio;
- separa le righe non-merce (sponsorizzazioni, spese edili, servizi) dai
  prodotti food prima del food cost;
- dopo ogni modifica a filtri/regex, verifica che i numeri chiave (es.
  conteggio sforamenti, giorni di trasporto doppio) restino identici prima e
  dopo — i casi speciali (trasporti, righe di rettifica) vanno intercettati
  PRIMA del filtro del rumore, mai dopo.

**Righe di rettifica non-prodotto** (es. "ABBUONO COMMERCIALE", "SCONTO
STRIKE" con importo negativo, viste su fornitori di salumi) compaiono come
articoli a sé nel foglio Articoli, perché raggruppare per codice+descrizione
le tiene naturalmente separate dai prodotti veri. È corretto: segnalalo al
consulente ("il fornitore applica sconti a riga separata, già dentro il
totale netto"), non filtrarle via silenziosamente.

### Controlli di servizio: trasporti
Da fare su OGNI fattura, non a campione:
- Somma per fattura e per giorno le righe "Spese trasporto"/"Contributo trasporto" — alcuni fornitori spezzano il contributo su più righe per aliquota IVA, quindi si riconosce solo sommandole.
- Due addebiti nella **stessa fattura** sono contestabili: chiedi la nota di credito. Due fatture **diverse nello stesso giorno**: prima chiedi al locale se le consegne erano davvero due.
- I fornitori che emettono già 2+ fatture nello stesso giorno sono l'origine tipica del doppio contributo: vale la pena controllarli per primi.
- **Mini-ordini di rabbocco**: un trasporto fisso su un ordine piccolo pesa in proporzione molto di più. Leve: accorpare i rabbocchi, fissare un ordine minimo, confrontare la tariffa trasporto dello stesso grossista fra clienti diversi (può variare).
- Consegna un foglio con un giorno per riga, da contestare al fornitore.

I trasporti si escludono **solo** dalla lista per la ricerca di mercato (step 3, punto 1) e dal confronto `references/prompt_ricerca_mercato.md` — mai dai dati prima di questo controllo di servizio.

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

**Normalizzare all'unità è necessario ma non basta.** Prima di dire "conviene X"
verifica che sia la **stessa merce** per qualità, resa, durata e origine (es.
un olio di semi normale e uno alto oleico non sono la stessa merce: l'alto
oleico costa di più ma dura di più in friggitrice — non sono confrontabili
sul solo prezzo). Sul fresco il fornitore più conveniente cambia da prodotto
a prodotto: non indicare mai un "fornitore più conveniente" in blocco. Gli
acquisti fatti mentre il fornitore abituale è chiuso/in ferie sono ripieghi,
non allarmi: chiedi prima di segnalarli come anomalia.

**Premi contrattuali e accordi: chiedili prima di dire "conviene X".** Il
prezzo in fattura non mostra premi di fine anno, sconti volume o
finanziamenti legati al fornitore. Prima di consigliare di spostare acquisti
sul fornitore "che costa meno", chiedi al titolare gli accordi in essere.
Aggiungi al foglio Confronto Fornitori una colonna "Accordi/premi: sì / no /
da chiedere". Le liste ordini per il personale non devono mai avere prezzi
né indicare cambi di fornitore: prezzi e "dove conviene" vanno solo in una
copia riservata al titolare o al consulente, perché la decisione di
cambiare fornitore resta a loro, mai automatica. *(Nota da validare: una nota
di credito di puro premio, distinta da un reso vero, dovrebbe uscire dal
foglio "Resi - Note di credito" per non gonfiare l'incidenza dei resi — è
una deduzione dal comportamento dello script, non ancora verificata su un
caso reale: va controllata prima di cambiare la classificazione.)*

**Dalla variazione di prezzo alla negoziazione**: per ogni articolo calcola
prezzo primo, medio e ultimo del periodo e l'**impatto in €/mese** =
`(ultimo − primo) × quantità media mensile`, sul prezzo netto. Consegna un
CSV dei rincari e, su richiesta, una scheda di negoziazione per fornitore
(su ~6 mesi di fatture). Segnala come domande al fornitore, non come accuse:
lo stesso prodotto fatturato a due prezzi alternati nel tempo, o sconti
diversi sullo stesso articolo nella stessa fattura. Con un grossista
"tutto-in-uno", raggruppa gli articoli per famiglia (mare, carne/salumi,
oli, patate, pane/bun, salse, non-food) per misurare gli aumenti in corso di
stagione: la leva è bloccare i prezzi a inizio stagione sulle famiglie
principali.

### 5. Consegna

Manda i file Excel all'utente (un file per fornitore + l'eventuale
"Confronto Fornitori"). Nel messaggio di chiusura riassumi: spesa totale nel
periodo, punti "sopra mercato" con affidabilità Alta/Media da verificare col
fornitore, ed eventuali anomalie di dati segnalate durante la costruzione
(scostamenti imponibile, righe di rettifica, documenti non leggibili).

## Modalità 2: controllo ricorrente contro listino concordato
Distinta dal confronto col mercato dello step 3 (soglia ±8%, un'analisi una tantum): qui si confronta il prezzo pagato col **prezzo concordato con quel fornitore**, il confronto che si usa per contestare al fornitore. Passaci dopo l'analisi una tantum, quando ci sono 4-6 mesi di righe articolo. Dettaglio completo (listino concordato, tolleranze, automazione settimanale, liste ordini, trascrizione bolle) in `references/controllo-ricorrente-listino.md`.

In sintesi:
- **Listino di riferimento**: per ogni prodotto, il prezzo concordato o — se manca — la moda dello storico. Solido solo con molti acquisti allo stesso prezzo; con una sola fattura è debole e va fatto approvare dal cliente. Tolleranza: una soglia unica stretta (~2%) non regge sul fresco — si parte da ~15% su ortofrutta/fresco e si ritara dopo un mese (soglie da proporre, non ancora validate su più clienti).
- **Controllo mensile**: incidenza degli extra pagati sulla spesa merce (confrontare i mesi per incidenza, mai per importo secco) e numero di prodotti che sforano. Le soglie di avviso/non tollerabile le decide il cliente.
- **Giro settimanale**: fatture degli ultimi 8 giorni più bolle scansionate lette riga per riga (le fatture arrivano fino a ~12 giorni dopo la consegna). Le righe sopra il concordato vanno in una bozza di mail al fornitore, che manda sempre il consulente, mai in automatico.
- **Le bolle di una settimana sono un minimo**, non il totale: non calcolare da lì un food cost % reale senza dirlo (il consuntivo si fa sul mese, con gli inventari — vedi `foodcost-cliente`).
- **Automazione**: uno script settimanale (es. il lunedì) legge le fatture da Fatture in Cloud e manda la mail di controllo SOLO se ci sono sforamenti, trasporti doppi o prodotti nuovi — zero segnalazioni non vuol dire tutto in regola, verifica sempre la data dell'ultima fattura disponibile prima di dire "nessun problema" (un controllo può uscire "pulito" solo perché in Fatture in Cloud non è stata caricata nessuna fattura di recente). Il token manuale di Fatture in Cloud è una credenziale separata dalla sessione web: se scade o viene revocato l'API risponde `401 invalid_token` e il login del cliente sul sito NON lo riattiva — va rigenerato in Impostazioni → API → Token manuali, e il file del token tiene UNA sola riga `TOKEN=<TOKEN>` (mai il valore vero nel plugin o nei file condivisi).

Questa Modalità 2 è candidata a diventare una skill a sé ("sentinella-prezzi-fornitori") se il carico di lavoro lo giustifica — per ora resta qui.

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
  materie prime del File 02. Le bolle della settimana danno solo un minimo
  degli acquisti: il food cost consuntivo si fa sul mese con gli inventari.

## Fonti/contributi
(contributo di Andrea Chirivì, Noolas e altri clienti RBR, 2026-10-12. Skill originale di Leo Franco, da coinvolgere sulle modifiche a `costruisci_analisi.py` prima di applicarle.)



Se il cliente fornisce le fatture solo come PDF (scansioni o export senza
XML/p7m allegato — capita con alcuni fornitori grandi) e non hai il file
elettronico originale, il parsing riga per riga automatico non è possibile:
serve estrarre il testo del PDF e riconoscere le righe a mano (più lento, più
soggetto a errori di lettura numerica — controlla sempre i totali per
documento contro l'imponibile dichiarato nel PDF). Preferisci sempre chiedere
se esistono gli XML originali (spesso sì, anche quando il consulente ha solo
i PDF a portata di mano) prima di imboccare questa strada più lenta.

**Fornitori che fatturano solo i totali DDT, senza righe articolo** (spesso
del fresco): lo script scarta le righe senza quantità, quindi il fornitore
risulta quasi tutto nello "scostamento imponibile" o con articoli generici
tipo "merce come da DDT" — va segnalato al consulente, non lasciato passare
in silenzio. Per questi fornitori prendi i prezzi da un'altra fonte (bolle/
DDT, foglio prezzi del food cost, listino del fornitore) e marcali a listino
come "fonte non-fattura", con una tolleranza più larga (15% sull'ortofrutta).
