# Dati di vendita, food cost, matrice, listino cassa

## Venduto per gestionale (sempre COMPLETO, mai un campione)
- **Cassa in Cloud (Cartabianca)**: `/reports/sold/products` → `profit` è il RICAVO, prezzo unitario =
  `profit/quantity`. Negli scontrini `/documents/receipts` invece `price` è già unitario (non dividere).
  Prezzo di listino vero = il più battuto nelle righe a quantità 1, non la media.
  Popolarità normalizzata sul tempo in carta: `agents/cic/fetch_venduto_settimanale.py` +
  `popolarita_tempo_in_carta.py` (quota nella categoria nelle settimane attive × n. piatti attivi; <0,70 = poco popolare).
  Pranzo a rotazione: venduto giornaliero × menu del giorno dal sito (revisioni WordPress) × meteo;
  modello di scelta logit (`agents/cic/menu_autunno.py`).
- **Zucchetti (Luna Blu)**: PDF mensili `vendite_YYYY-MM.pdf` → `pdftotext` → `scripts/parse_mesi.py`
  (regex righe articolo `qta / importo` + subtotali categoria) → `mesi.json`. L'xls `VendutoArticoli`
  copre i mesi mancanti (totale − somma mesi già presi). **Alias dei tasti rinominati** (`scripts/stagioni.py`):
  l'xls usa i nomi nuovi retroattivamente (TIROLESE→TONNO SAP SICILI, ZUPPA COZZE→IMPEPATA COZZE…).
- **iPratico**: skill `rbr-consulting:estrai-dati-ipratico` (training=1; Totalizzazioni → DETTAGLIO
  CATEGORIA PER QUANTITÀ; non la pagina "Products profit margin" che è un campione).
- **CEI Smart Manager (Giurgés)**: Statistiche → Advanced → Plu → Export.
- Cerca sempre i **fuori carta** venduti (Sandwich Ribs 141 pz, Tyrsos calice più venduto non in carta) e i
  prodotti già in cassa da valorizzare (focaccia Antipapa 2.298 pz = n.1 del locale).

## Stagioni
Due matrici separate: inverno (es. ott→mag, ÷ mesi) ed estate. Unità = **pezzi/mese** (`pzm(k,s)`).
La carta invernale si costruisce sulla matrice invernale.

## Food cost
- File 02 del cliente (Google Sheet nativo: scrivere cella per cella via API; xlsx non nativo: chirurgia XML,
  mai openpyxl load+save che cancella i grafici). Locale it_IT: `=C6/1,1`, separatore `;`.
- Prezzi €/kg dalle fatture XML; scarti standard in arancio "da confermare con una pesata" (`scripts/plan.py`,
  dizionario STD: calamari 40%, alici 50%, prezzemolo 40%, carciofi latta 65%, crosta parmigiano 10%…).
- Piatti senza ricetta: stima per analogia, marcata "stima" / "STIMA RBR".
- Controlla le unità sul listino (bar Cartabianca usava articoli da ristorante: cotto 11,26 vs 7,94).
- **Margine = prezzo/1,1 − FC** (IVA esclusa su entrambi). Coperto/servizio fuori dal food cost.
- Split food/drink: il drink cost può superare il food cost (bibite 33 cl, birre in bottiglia).

## Matrice (per categoria)
- Soglia popolarità = `Q/n × 0,7` (70% della media pezzi); soglia margine = media pesata sui pezzi.
- Soglie solo sui piatti in carta della stagione; fuori carta/estivi classificati ma non spostano le soglie.
- Prezzo dei fuori carta = prezzo medio di cassa arrotondato a 0,5.
- Script: `scripts/matrici.py` → `matrici.json`. Classi interne STAR/PLOWHORSE/PUZZLE/DOG; **al cliente in
  italiano** (vedi presentazione).
- Piatti "per 2": margine anche a persona.

## Leve in €/anno
- Prezzo: `(p1 − p0)/1,1 × pz/mese × 12`. Formati/upsell: ipotesi di adozione dichiarata ("8 su 100").
- Luna Blu: +14k €/anno a parità di volumi sulla carta; obiettivo in presentazione +20/25k (mix 37/63 → 50/50
  +7.000, ingegnerizzazione +3.900, prezzi +9.500), espresso anche al mese e a coperto.
- Cartabianca: listino +148,8k €/anno reali (non i 202k del foglio: in 45 prodotti il "prezzo oggi" del foglio
  era sotto la cassa). Scontrino: +0,10 bar ≈ 73,6k/anno; +0,50 pranzo ≈ 26,6k/anno.

## Unica fonte prezzi
Foglio "Prezzi definitivi" con colonne Oggi · Marco · Cliente · Titolare → PREZZO FINALE (precedenza
titolare, poi cliente; "NO" = resta il prezzo di oggi). `prezzi_live.py` → `prezzi_live.json` → carte.
Per gli aumenti in cassa si usa il prezzo vero di cassa (`listino.json`), mai la colonna "oggi" (media del venduto).

## Listino per la cassa (`templates/listino_cassa/build_listino.py`)
- Xlsx un tab per locale: ID prodotto, prezzo oggi/nuovo, pezzi 12 mesi, effetto €/anno; tab "Da verificare",
  "Nuovi da creare", "Non più in cassa"; `payload_cassa.json`.
- Si carica solo se il prezzo sale e il prezzo di cassa è fisso. Ribassi, salti >+35%, prezzi liberi e a peso
  → "Da verificare". Si carica il prezzo del LOCALE, non quello generale.
- Ogni voce nuova della carta (porzioni +2/+4, tazze medio/grande, contorno medio…) va creata in cassa PRIMA di stampare.
- Carico in cassa a locali chiusi (domenica sera), partenza il lunedì con le carte nuove; prima settimana
  controllo scontrini. Riepilogo 2 pagine per il titolare (`riepilogo_massimo.html`): quanto vale per locale,
  cosa cambia per il cliente, cosa deve decidere, chi fa cosa e quando.

