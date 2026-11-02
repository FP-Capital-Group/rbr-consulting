---
name: campagna-locale
description: >-
  Pipeline RBR per lanciare una campagna offerta di un locale, dall'idea al coupon in cassa. Usala ogni volta che devi far partire una promo di un ristorante — "lanciamo un'offerta per il locale", "creiamo una landing per la promo 10 euro", "genera il QR e il codice sconto", "campagna coupon per i turisti", "mandiamo la mail dell'offerta ai clienti". Copre tutto il flusso: offerta → landing WordPress parametrizzata → QR code → coupon sul POS iPratico → email nel CRM GHL. NON improvvisare landing o codici a mano: segui questa pipeline per non rompere il tracciamento e la cassa.
---

# Campagna locale (offerta → landing → QR → coupon → email)

## Perché esiste
In RBR un'offerta non è "un post con uno sconto": è una **catena tracciata** che parte dall'idea e arriva al coupon che lo staff scansiona in cassa. Ogni anello ha un codice univoco (`code`) che lega landing, QR, POS e CRM. Se salti un passaggio o inventi un codice a mano, il tracciamento si spezza: non sai più quanti clienti sono arrivati da quale canale, e la cassa non riconosce lo sconto. Questa skill fissa l'ordine giusto e gli strumenti giusti.

## Quando usarla
- Devi lanciare una promo di un locale (sconto €, %, prodotto gratis) su uno o più canali.
- Devi creare la landing di un'offerta e il relativo QR/coupon.
- Devi rigenerare o clonare un'offerta esistente per un nuovo target (es. turisti EN, riattivazione).
- Serve mandare ai clienti la mail con il codice/QR dell'offerta.

## Prerequisiti
- **Sheet master offerte/landing** del locale (sorgente di verità dei `code`, URL landing, URL QR). Per Mister Pizza: Sheet 1 "Modifiche sito" (mapping offerta→URL + source) e Sheet 2 "Descrizioni offerte + QR". Ogni locale ha i suoi.
- Accesso **WordPress** del sito (REST API + Application Password) per pubblicare/parametrizzare la landing.
- Accesso al **POS iPratico** del locale per creare il coupon (installazioni separate per brand — es. Mister Pizza e Dirigì sono account distinti).
- Istanza MCP CRM del cliente (`ghl2-<cliente>`) per l'email; token nel `.env`, mai in chiaro nel file.
- Tono email RBR (vedi Regole).

## Procedura

### 1. Definisci l'offerta e il `code`
**Da dove parte l'offerta**: prima di fissare il `code`, guarda i coperti per giorno della settimana e
lega l'offerta alla sera più debole (un giovedì fiacco e un sabato pieno possono costare uguale in
regalo/sconto per coperto, con incasso molto diverso). Calcola il costo del regalo/sconto per coperto e
quanti coperti servono per restare in utile: un'offerta che non regge il margine per coperto non parte.
Fissa sempre una scadenza vera e, se serve, un numero di coperti disponibili. Quattro forme tipiche:
menu a prezzo chiuso col prodotto del posizionamento; omaggio a chi prenota (alto valore percepito, food
cost basso); sconto chiaro con scadenza; regalo in € sulla prossima cena. **Aggancia l'offerta a una
linea o famiglia di prodotti** (es. tre panini di una stessa selezione, ognuno col suo abbinamento), non
a un piatto singolo: così non cade quando un piatto esce di carta. Ogni nome, abbinamento e prezzo
citato si legge dal menu vivo del cliente prima di scriverlo, mai da un'offerta di un altro locale.

(contributo di Andrea Chirivì, 12/10/2026; metodo "da dove parte l'offerta" di Roberto Falcon, Piano
Marketing RBR v1.0 — a chi mandarla resta da allineare col resto del plugin)

Fissa: tipo sconto (€, %, prodotto gratis), target (italiani / turisti EN / riattivazione / hotel…), canale (facebook-adv, google-adv, instagram, riattivazione, hotel). Genera un `code` **parlante**: a vista deve dire offerta + target (es. `10euroturistaeng1`, `BRO10EU`, `10eurosett2`). Formato libero ma chiaro, con due vincoli di cassa (contributo di Luciano Purpi, 2026-09-03): **niente trattini** (iPratico li mangia: `amico-portato` diventa `AMICOPORTATO`) e **una sola grafia** (iPratico distingue le maiuscole: `10wifiprenotazione` e `10WIFIPRENOTAZIONE` sono due codici diversi). Registra il `code` nello Sheet master — **è lui la chiave di tutta la catena**.

**Regola dei tre allineamenti**: la stessa identica stringa deve esistere nel link dell'annuncio/landing (`?code=`), nella colonna del foglio generatore e nel campo `Codice` di iPratico. Ogni volta che ne tocchi uno, controlli gli altri due.

### 2. Landing page parametrizzata (WordPress)
Le landing sono già pubblicate e riusabili: cambia solo il querystring, non la pagina.
- Pattern URL: `https://<dominio>/<offerta>?code=<code>&source=<source>`
- Esempio: `https://www.misterpizza.it/10euro?code=10euroturistiita1&source=riattivazione`
- Mappa `offerta` → URL base dallo Sheet (es. 5euro, 10euro, 20euro, siciliana, calabrese). Se l'offerta è nuova, crea la landing base una volta sola, poi riusala parametrizzata.
- ⚠️ **Il `source` arriva a Resmio solo in certi setup** (contributo di Luciano Purpi, 2026-09-03): con l'embed classico `widget.js` Resmio lo riscrive SEMPRE con l'hostname della pagina, qualunque landing l'abbia generato. Passa intero solo col proxy PHP (Mister Pizza, Dirigì) o col link diretto al widget. **Check di 30 secondi prima di impostare l'attribuzione**: apri una landing, leggi l'URL dell'iframe generato, verifica che `source` sia sopravvissuto. Se no, il canale si traccia con `?utm=` in `booking_request_parameters` (skill `sito-landing-ristorante`, Tracciamento).
- **Senza landing né proxy** (mail, WhatsApp, QR, bio Instagram, bot): link diretto al widget `app.resmio.com/<slug>/widget?source=<canale-campagna>&comment=<offerta in chiaro + code:CODICE>` — porta in una riga la fonte per misurare e la nota che dice al cameriere cosa ha in mano il cliente. Funziona su qualsiasi locale Resmio (contributo di Luciano Purpi, 2026-09-05). Url-encoda il testo, niente emoji. Aggiungi `&date=AAAA-MM-GG` e/o `&people=<n>` per preselezionare giorno e ospiti (utile per landing di eventi, un `source` per serata). Dettagli e rimedio se il link è già partito senza comment → `references/codici-resmio-ipratico.md`.

### 3. QR code
Genera il QR che **contiene il `code` in chiaro** (lo staff lo scansiona in cassa, non serve che punti a un URL):
`https://quickchart.io/qr?size=800&captionFontSize=50&text=<code>`
Salva l'URL del QR nello Sheet 2 (Descrizioni offerte + QR), riga del `code`, con descrizione offerta nella lingua del target (turisti EN → inglese, italiani → italiano).
- Il QR col solo codice serve al **lettore di cassa**: inquadrato da un iPhone apre una ricerca web
  ("sito non nostro"). Non è un errore, ma quel QR non va dove lo inquadra il cliente (tovagliette,
  locandine, mail): lì serve invece il QR verso l'URL della landing (`sito-landing-ristorante`).
- Se generi i QR in locale con Python `segno`, usa sempre `segno.make(..., micro=False)`: sui testi
  corti `segno` produce Micro QR che molti lettori di cassa e telefoni non leggono. Verifica i QR
  decodificandoli dal PDF finale prima di stampare.
- In cassa stampa **una sola pagina**: QR dei codici attivi più quello della pagina coi moduli di
  riscatto, con le regole d'uso in sei righe. Il fascicolo completo dei regolamenti resta a parte. Il
  foglio vale come chiave e sta in cassa, non in sala.

(contributo di Andrea Chirivì, 12/10/2026)

### 4. Coupon sul POS (iPratico)
Per ogni `code` creato va ricreato il coupon sul gestionale iPratico del locale.

**Cosa si può impostare**: sconto % o €, monouso o illimitato, validità per giorni e fasce orarie, flag
compleanno, applicabile a categorie/prodotti/tipologie d'ordine (Delivery, Take away), spesa minima, QR
per codice più PDF di tutti; vale su iPratico EAT, Web App e API pubbliche (lega al punto 3 di
`references/codici-resmio-ipratico.md` §5 su `sourceApps`). Con le **categorie** selezionate lo sconto
va riga per riga sul preconto; con **"Applicabile al totale"** sconta il conto intero. Uso RBR: offerte
per fascia, categoria o asporto senza strumenti esterni. I riscatti si leggono da Statistiche → Promo
codes del cloud (oltre all'endpoint `promo-codes-movements` già citato in `estrai-dati-ipratico/SKILL.md`).

⚠️ **Se il locale è o è stato su Pienissimo**, i Promo Codes di iPratico possono essere DISABILITATI a
favore di quelli Pienissimo: verifica l'interruttore prima di dare per scontato che un codice creato
funzioni in cassa (dettagli in `references/codici-resmio-ipratico.md` §5bis).

- **Mapping 1:1 offerta→coupon**: `5euro`→€5 off, `10euro`→€10 off, `20euro`→€20 off, `siciliana`→pizza siciliana gratis, `calabrese`→pizza calabrese gratis. Offerta nuova = nuovo mapping da decidere col cliente. **Omaggio senza codice**: quando l'offerta è un prodotto non addebitato (birra di benvenuto, dolce di compleanno) non creare un codice (il valore 0 è rifiutato dalla cassa) ma un **prodotto dedicato a 0 €** da battere al posto di quello vero, così il riscatto resta contato in cassa come vendita a 0 (`estrai-dati-ipratico/SKILL.md`: omaggio = `finalPrice == 0`). Duplicalo dal prodotto vero (eredita IVA e centro di lavoro) e usa "Propaga prezzo" per metterlo a 0 su tutti i listini; se il cliente sceglie fra più versioni, usa una VARIANTE OBBLIGATORIA (i gruppi "Varianti senza costo" non compaiono in cassa). Trappola del portale: mai premere Escape nei pannelli (chiude senza salvare).
- **Scadenza coupon**: di default durata lunga fissa `2025-01-01 → 2030-12-31` e al pubblico non si comunica nessuna scadenza. Se invece la campagna comunica una scadenza (mail, landing), la cassa deve avere **la stessa**: o accorci anche quella, o è scarsità finta (regola RBR: se scade, scade) (contributo di Luciano Purpi, 2026-09-04).
- Se il locale ha più brand/installazioni, **replica il coupon su ciascuna** (stesso `code`, POS diversi).
- **Controlli di creazione** (contributo di Luciano Purpi, 2026-09-03/04): spunta anche "API pubbliche" in `sourceApps` (parte vuoto: senza, il codice è invisibile all'API e il QR non arriva mai); per i buoni in euro tipo "€ - Valore sconto" (parte su "%"); un **HTTP 412 = codice già esistente**, non blocco d'account; i codici del locale possono stare nella vista `/anagrafiche-cloud/promo-codes/0` mentre la `/1` dice "nessun codice" — guardale entrambe prima di crearne uno doppio. Leggi dalla DataTable valore, spesa minima, `isReusable` (1 = riusabile all'infinito, anche dalla stessa persona: per una campagna a lista decidilo consapevolmente), date e canali, e confrontali col testo della campagna. Creazione via API (jQuery.ajax, form-urlencoded) → `references/codici-resmio-ipratico.md`. Sincronizza sempre la cassa dopo la creazione (§5 punto 12 della reference): un codice "non riconosciuto" il primo giorno spesso è solo da sincronizzare.

#### Ogni sconto ha un nome
Sconti cliente a regola fissa (TheFork per percentuale, gift card, compleanno) = **codici promozionali**;
sconti interni (direzione, reclamo, staff) = **tasti del tastierino** con nome parlante (max 8, si
configurano solo dall'iPad master). TheFork: codici dedicati sulle categorie del cibo alla carta
(esclusi coperto, bevande e richieste fuori menu — ⚠️ da ricontrollare caso per caso: capita che i
codici creati includano per errore anche categorie da escludere), app EAT, utilizzi illimitati, sconto
riga per riga sul preconto; i tasti "The fork x%" che scontano in riga unica sul subtotale vanno
eliminati. Lettura: un tasto compare in `statistics/orders` come riga subtotale con `variation.name` =
nome del tasto; i codici in Statistiche → Promo codes — nel controllo giornaliero leggi gli sconti per
nome, mai come voce unica. Un tasto sconto su categorie si calcola all'inserimento: i prodotti battuti
dopo non vengono scontati. ⚠️ **2x1 resta senza una strada pulita in cassa**: il conteggio vero resta nel
modulo di riscatto del CRM finché non si testa in cassa un metodo diverso — non presentarlo come
risolto.

### 5. Email nel CRM (GHL)
Manda ai clienti la mail con codice/QR via istanza MCP `ghl2-<cliente>` (segmenta per tag: città, target, riattivazione).
- **Tono asciutto, no marketing-speak**: al centro il codice e lo sconto, non gli aggettivi. "10€ di sconto da Mister Pizza. Mostra questo QR in cassa." Niente frasi da brochure.
- Rispetta eventuali frame di campagna (es. Glovo Firenze: mai nominare il vecchio partner, solo messaggio forward-looking).
- L'invio email a terzi è un'azione a conferma: prepara la bozza e il segmento, poi chiedi l'ok prima di spedire.

### 6. Registra e verifica
Scrivi tutto nello Sheet master (code, landing, source, QR) così resta la sorgente di verità. Verifica la catena end-to-end prima di dichiarare chiusa la campagna (vedi DoD).
- **Prima del lancio**: il codice stampato su landing, mail e materiali deve ESISTERE in cassa con lo stesso testo esatto. Caso reale Red Mike (3/9/2026): landing e testi con `10EURORIAPERTURA`, in cassa esisteva solo `RIAPERTURA10` — chi si fosse presentato non avrebbe avuto lo sconto, e la colpa sarebbe caduta sul cameriere (contributo di Luciano Purpi, 2026-09-04). **Le regole d'uso si spiegano a voce alla sala prima di accendere la campagna**, oltre a scriverle sul foglio di cassa (vedi regolamento unico in "Regole RBR & trabocchetti"): sono le domande che arrivano la prima sera, e se la sala non le conosce decide il cameriere al tavolo — e la colpa ricade su di lui, come nel caso Red Mike qui sopra.
- **Dopo il lancio si verifica dai codici DAVVERO usati**, non dal foglio: prenotazioni Resmio recenti + regex `code\s*:\s*([A-Za-z0-9_.-]+)` sul campo `comment` (su un cliente ha fatto emergere codici in circolazione che non esistevano né in cassa né nel foglio).

## Regole RBR & trabocchetti
- ⚠️ **Il `code` è la chiave di tutto**: usa SEMPRE il `code` esatto dello Sheet, non normalizzarlo (i prefissi non sono uniformi, es. `turistiita1` vs `turistaita2`). Un code sbagliato = anello rotto.
- ⚠️ **Landing = riuso parametrizzato**, non pagina nuova ogni volta. Cambia il querystring `?code=&source=`, non duplicare la pagina.
- ⚠️ **`code:CODICE` nella nota Resmio è un CONTRATTO col middleware QR**, non una convenzione (contributo di Luciano Purpi, 2026-09-03): il middleware dell'agenzia partner fa una regex su `code:` nel testo del `comment` e prende quello che segue. Niente `code:` = nessun QR, in silenzio (spostare il codice nel parametro `utm` ha spento i QR per due giorni su due clienti). Dopo `code:` va il CODICE (`code:GIFTCARDCASSA`), mai la descrizione. Prima di toccare un anello montato da terzi, leggi la tabella **chi legge cosa** in `references/codici-resmio-ipratico.md`. 🟡 Aperto: il `comment` finisce nella mail di conferma (l'ospite legge l'etichetta) — o si porta tutto in un parametro invisibile adeguando il middleware, o si tiene `code:` e si tolgono le note dal template mail; da decidere con chi mantiene il middleware.
- ⚠️ **In Resmio `comment` = nota dell'OSPITE, `notes` = nota dello STAFF** (contributo di Luciano Purpi, 2026-09-03): i codici offerta stanno nel `comment`. Cercarli in `notes` fa concludere che il tracciamento è morto (Mister Pizza + Dirigì: 400+ prenotazioni con `code:` in 3 mesi). Il `comment` arriva concatenato ai campi custom del widget (`Turista o Locale?: TuristaComment: code:...`): regex tollerante.
- ⚠️ **iPratico è manuale e per-installazione**: quello che fai su un brand va replicato sull'altro. Non dare per scontato che il coupon esista già.
- ⚠️ **Mai token/API key nel repo** (condiviso col team): CRM via MCP `ghl2-<cliente>`, credenziali WordPress e POS dal `.env`.
- ⚠️ **WordPress dietro Cloudflare/WP Engine**: i fetch non-browser possono dare 403 → usa il client REST autenticato con User-Agent browser; dopo modifiche svuota la cache.
- 🟡 **Email**: sempre conferma prima dell'invio a clienti reali; tono asciutto codice/sconto.
- **Regolamento unico delle promo**: le regole d'uso si fissano per TUTTE le promo del locale insieme,
  non promo per promo — due promo vive con vincoli diversi ("uno a persona" e "uno per tavolo")
  confondono la sala. Standard di default: un coupon per tavolo, non cumulabili fra loro (TheFork
  compreso); le eccezioni vanno dichiarate esplicitamente. Due coupon nella stessa compagnia: due
  prenotazioni separate a tavoli lontani, oppure il secondo per un'altra sera — mai promettere tavoli
  vicini, mai scriverlo in nota. Il coupon personale si scala per intero dal conto del tavolo (la
  ripartizione la decide il tavolo): va detto prima nei messaggi promo, non discusso in cassa. Validità
  e condizioni vanno scritte IDENTICHE in tutte le email della catena, nella landing e sul foglio di
  cassa, con le parole che la cassa capisce ("altre promozioni", non "iniziative"). I coupon si
  presentano sempre come regali.
- **Il coupon non si dà a chi lo chiede**, in chat, DM, telefono o sala: il coupon è un front end per
  chi lo trova online e lascia i dati, il prodotto è il contatto. Si risponde con garbo che non si
  distribuisce su richiesta, senza link/moduli/landing; il bot non raccoglie dati "per mandare il
  codice" e non passa la richiesta allo staff. Chi il coupon ce l'ha lo mostra al tavolo; se prenota col
  bot la nota dice "COUPON". **La frase è una sola per bot, agente vocale e staff**: sul bot GHL va
  introdotta con "rispondi con queste parole:", altrimenti il modello la parafrasa e perde il tono.
- **Promo e KPI fatti da terzi (agenzie): controlla prima che giri, ricostruisci i numeri alla fonte.**
  Prima che una promo di un'agenzia parta, controlla: recensioni inventate sulla landing (si tolgono
  subito, comunque vada); requisiti non verificabili senza una prova richiesta ("riservato agli
  studenti" senza chiedere l'ateneo); regolamento vuoto; nessuna scadenza/tetto/orario/prenotazione;
  nessun codice o tasto in cassa per misurarla; consenso marketing non libero (va sempre separato
  dall'adesione alla promo); landing esterna senza pixel e senza sapere dove finiscono i dati; promo
  che non nomina la differenza del locale (così il concorrente la copia uguale). KPI: mai analisi su
  screenshot dell'agenzia; "incasso stimato" e "% di utilizzo" con base ignota non si citano. Ricostruisci
  da CRM e cassa (coupon ≠ tavoli): costo per tavolo entrato = spesa ÷ coupon usati. Anche il canone
  dell'agenzia si verifica sulle fatture prima di citarlo.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

(contributo di Andrea Chirivì, 12/10/2026)

## Definition of Done
- [ ] `code` parlante creato e scritto nello Sheet master (offerta + target riconoscibili)
- [ ] Landing raggiungibile con URL parametrizzato `?code=&source=` (verificata 200)
- [ ] QR generato con `text=<code>` e URL salvato nello Sheet 2 + descrizione nella lingua del target
- [ ] Coupon iPratico creato con mapping corretto e scadenza `2025-01-01 → 2030-12-31`, replicato su tutte le installazioni del locale, provato in cassa dopo la sincronizzazione (non solo visto nel portale)
- [ ] Se il locale è/è stato su Pienissimo, interruttore Promo Code iPratico verificato
- [ ] Regole d'uso allineate col regolamento unico delle promo e spiegate alla sala prima dell'accensione
- [ ] Email preparata nel CRM con tono asciutto codice/sconto, segmento giusto, e **inviata solo dopo ok**
- [ ] Catena verificata end-to-end (scan QR → code leggibile → coupon riconosciuto in cassa)
- [ ] Tre allineamenti verificati: stessa stringa in link (`?code=`), foglio generatore e campo `Codice` iPratico (niente trattini, stessa grafia); `sourceApps` con "API pubbliche"; scadenza in cassa = scadenza comunicata
- [ ] `source` verificato nell'iframe generato (check 30 secondi) o canale tracciato con `utm`; `code:CODICE` presente nel `comment` dove c'è il middleware QR
