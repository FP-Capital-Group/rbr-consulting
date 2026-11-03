---
name: market-discovery-ristorante
description: >-
  Ricerca di mercato RBR per un ristorante (esistente o da aprire) nella sua zona — perimetro di attrazione, domanda locale (keyword, stagionalità, occasioni d'uso), censimento competitor via Google Maps/delivery/social, gap di posizionamento (matrice categoria × zona, framework Merenda) e scheda di sintesi 1 pagina che alimenta adv, SEO e campagne. Usala quando serve una "market discovery", "analisi di mercato", "studia la zona", "analisi competitor", "dove apriamo", "posizionamento nella zona", "com'è il mercato in [città/quartiere]", o prima di lanciare ads/promo per un locale di cui non conosci il contesto competitivo.
---

> **Nuovo cliente? Parti dal Mega-prompt Posizionamento RBR** — `prompt-posizionamento.md`
> in questa cartella: percorso conversazionale a 5 fasi (fotografia → esplorazione angoli →
> validazione → frase di posizionamento → piano 90 giorni) che usa i dati di questa market
> discovery. Insieme formano il quadro generale d'ingaggio del cliente.

# Market Discovery ristorante (zona, domanda, competitor, posizionamento)

## Perché esiste
In RBR il posizionamento viene PRIMA dell'offerta e delle ads (`strategia-marketing-rbr`): un locale deve essere "il numero 1 di qualcosa" nella testa del cliente della SUA zona (Merenda). Ma non si sceglie "di cosa essere primi" a tavolino: si scopre studiando il mercato reale — chi c'è in zona, cosa cerca la gente, dove i competitor deludono. Questa skill è il metodo per farlo con numeri e fonti, non con impressioni. Il suo output dimensiona anche i 3 moltiplicatori (Abraham): quanti clienti nuovi ci sono da prendere in zona, che scontrino regge il mercato, che occasioni di ritorno esistono.

## Quando usarla
- Nuovo cliente RBR: prima consulenza strategica, serve la fotografia del suo mercato.
- Apertura/nuova sede: "dove apriamo?", "conviene questa zona?".
- Riposizionamento: il locale non si distingue, promo che non funzionano, "siamo uguali a tutti".
- PRIMA di `adv-ristorante`, `seo-local-ristorante` o `campagna-locale` se il posizionamento di zona non è mai stato validato.

## Cosa NON fa (confini con le altre skill)
- Non fa l'audit SEO né le pagine local → `seo-local-ristorante` (che però consuma le keyword di zona trovate qui).
- Non imposta le campagne → `adv-ristorante` (che consuma posizionamento, angoli e pricing di zona trovati qui).
- Non costruisce l'offerta/promo → `strategia-marketing-rbr` + `campagna-locale` (a valle del posizionamento).

## Strumenti
- **WebSearch / WebFetch** — ricerche, recensioni, guide di zona, dati demografici/turistici, articoli locali.
- **`mcp__google-ads__get_google_ads_keyword_ideas`** (se account disponibile) — volumi di ricerca reali per le keyword local; altrimenti Google Trends + stima dichiarata come tale.
  **Area**: misura la domanda su un'area costruita a mano coi comuni nel raggio reale del passo 1, non
  sulla provincia (una provincia include spesso comuni fuori bacino e gonfia i volumi). **Export CSV**:
  è UTF-16, separatore TAB, con due righe di intestazione da saltare. **Account**: se l'account Google
  Ads collegato non vede quello del cliente, usa il Keyword Planner da un altro account accessibile
  (i volumi non cambiano, la granularità sì) — per lavorare sulle campagne del cliente serve invece il
  suo account. **Famiglie d'intento**: raggruppa le parole per famiglia con la somma mensile e misura
  SEMPRE prima di proporre un'occasione o un angolo: un'occasione con domanda zero su due fonti
  (Keyword Planner + Search Console) non diventa la proposta numero uno solo perché piace.
- **Automazione UI del browser** (browser tool) — scraping UI dove l'API non arriva: Google Maps (lista competitor, rating, n° recensioni, fascia prezzo, e i **"temi più citati"** — la scheda Maps mostra la parola con il numero di recensioni che la usano, es. "pizza napoletana 75"; non è nell'API Places, serve il browser), Glovo/Just Eat/Deliveroo (chi domina il delivery in zona — dal delivery si prende solo la STRUTTURA del menu: categorie, formati, contorni, mai i prezzi, gonfiati dalla consegna), TheFork/TripAdvisor (anche i prezzi dei menu fissi/pranzo dei concorrenti si trovano nelle recensioni, con la data: confronta la composizione oltre al prezzo). Regola API-first: prova prima WebSearch/WebFetch, il browser è il fallback.
- **Regola d'oro: ogni numero ha una fonte citata** (URL + data di rilevazione). Un numero senza fonte non entra nella scheda.

(contributo di Andrea Chirivì, 12/10/2026)

## Procedura

### 1. Perimetro: la zona vera, non quella immaginata
Definisci il **raggio reale di attrazione** del locale (o del punto candidato):
- **Tipo di bacino**: quartiere (pizzeria d'asporto ~1-2 km), città (locale destinazione ~10-15 min auto), turistico (centro storico/località balneare → il bacino sono i flussi, non i residenti). Molti locali sono un mix: quantifica le componenti (proxy: lingua delle recensioni Google → % turisti).
- **Chi vive/lavora/passa nella zona**: residenti (età, famiglie vs single — dati ISTAT/comune via WebSearch), uffici e poli di lavoro (pranzo feriale), scuole/università, hotel e attrazioni (turisti), cinema/teatri/stadi (flussi serali a evento).
- **Barriere fisiche**: fiumi, ferrovie, ZTL, parcheggio, e anche cose minori come una fermata del bus
  sul lato sbagliato della strada — possono bloccare un flusso che sulla carta sembrava scontato.
- **Un polo vicino non vuol dire clienti**: prima di costruirci sopra una campagna, misura gli ingressi
  reali generati dal polo (scuola, ufficio, università) e l'effetto degli eventi, e studia il percorso
  fisico fra il polo e il locale — un polo a 100-200 m può non portare quasi nessuno se nel mezzo c'è
  un ostacolo anche piccolo.

Output del passo: mappa mentale del bacino con 2-4 **segmenti cliente della zona** (es. "coppie 30-45 del quartiere", "impiegati pranzo feriale", "turisti EN mag-set") e peso stimato di ciascuno. **Se il locale esiste già**, prima del posizionamento lancia un sondaggio di 6 domande ai clienti veri (con chi vieni, quante volte al mese, spesa a persona, come ci hai conosciuto, cosa apprezzi, cosa ti farebbe tornare — montato su GHL): le risposte pesano i segmenti reali invece di una stima "a sensazione" del titolare, e le domande aperte alimentano il filtro CLIENTE del passo 4.

(contributo di Andrea Chirivì, 12/10/2026; sondaggio 6 domande da Roberto Falcon, Mastermind RBR settembre 2026)

### 2. Domanda: cosa cerca la gente della zona
- **Keyword local**: "ristorante/pizzeria/<cucina> + <città/quartiere>", "migliore <piatto> a <città>", "<piatto> vicino a me", varianti EN se c'è componente turistica ("best pizza in <city>"). Volumi da keyword planner (via MCP Google Ads) o Google Trends; se stimati, dichiaralo con ⚠️.
- **Stagionalità**: Google Trends 12-24 mesi sulle keyword principali + calendario locale (eventi, fiere, stagione turistica). Segna i mesi di picco e di morto — servono ad `adv-ristorante` per il budget.
- **Occasioni d'uso** presenti in zona e loro copertura: pranzo lavoro, cena coppia, famiglie weekend, gruppi/compleanni, aperitivo, turisti, delivery serale. Per ciascuna: c'è domanda? chi la serve oggi? (incrocio col passo 3). **Domanda online quasi nulla ≠ occasione da scartare**: se un'occasione non si cerca su Google, si vince per prossimità (insegna, vetrina, convenzioni, partnership coi poli del passo 1), non con ads/SEO — cambia i canali, non toglie l'occasione dalla lista dei candidati.

### 3. Offerta: censimento competitor
⚠️ **Se il locale cliente porta il nome di una catena** con altre sedi in città, prima di censire
isola cosa è SUO: scheda Maps (l'indirizzo può essere un'altra via), listini sulle app delivery ("–
Centro", "– Via…"), recensioni, inserzionista nel Centro trasparenza Google. Le altre sedi sono
concorrenti con lo stesso nome: non attribuirgli dati, recensioni o listini del cliente, e ricorda che
anche le ricerche sul marchio si spalmano sulle altre sedi (il volume del nome non è tutto suo).

Censisci i competitor nel bacino (non tutta la città: solo il raggio del passo 1). Per ciascuno, tabella con:

| Campo | Fonte |
|---|---|
| Nome, categoria (pizzeria, trattoria, fine dining…) | Google Maps |
| Rating e **n° recensioni** (il volume pesa più del voto) | Google Maps |
| Fascia prezzo (€/€€/€€€, scontrino stimato dal menu) | Maps + sito/menu |
| **Temi più citati su Maps** (parola × n° recensioni che la usano, es. "pizza napoletana 75") | Maps (browser, non è in Places API) |
| Presenza delivery e ranking (chi esce primo su Glovo/Just Eat/Deliveroo in zona) | app aggregatori (a mano se serve) |
| Social: follower, frequenza post, se rispondono alle recensioni | IG/FB, Maps |
| Posizionamento dichiarato (di cosa si dicono "i migliori") | sito, bio, insegna |

Per 6-8 competitor e per il cliente, in un'ora i temi più citati dicono chi possiede già quale parola e
quale casella è libera: incrocia col Keyword Planner nel passo 4.

**Miniera d'oro: le recensioni negative dei competitor.** Leggi le 1-2 stelle degli 5-8 competitor principali e clusterizza i difetti ricorrenti (attesa lunga, personale scortese, porzioni, rumore, prezzo/qualità, no opzioni gluten-free/veg…). Ogni difetto ricorrente della zona = **opportunità di posizionamento** per il cliente ("il locale dove NON succede X"). Cita 2-3 recensioni esemplari per cluster (testo + data).

### 4. Gap di posizionamento (framework Merenda)
Costruisci la **matrice categoria × zona**: righe = categorie/specializzazioni possibili (pizza napoletana, carne alla brace, senza glutine certificato, cucina di pesce, brunch, famiglie con bimbi…), colonne = chi le occupa già nel bacino e con che forza (rating × volume recensioni × coerenza del messaggio).

- Cerca le celle **vuote o presidiate male**: categoria con domanda (passo 2) ma senza un "numero 1" riconoscibile → lì il cliente può essere primo.
- **Matematica della nicchia** (validazione): la nicchia scelta deve reggere i numeri. Stima: bacino × % segmento interessato × frequenza plausibile × scontrino di zona → confronta col fatturato che il locale deve fare (coperti × servizi). Una nicchia "libera" ma da 50 coperti/mese non è un posizionamento, è un hobby. Se la nicchia è stretta, verifica che sia il **cavallo di battaglia** di un locale che serve anche il resto, non l'unico prodotto. **Per una tribù** (celiaci, vegani, famiglie con bimbi) la domanda si conta in persone, non in ricerche: il volume della keyword di nicchia dice quale canale usare, non se la nicchia esiste. Prima di scartarla per poche ricerche guarda i filtri delle directory di categoria (es. quanti locali compaiono nel filtro "senza glutine" di TripAdvisor della zona, e se il cliente c'è) e le community di settore.
- Il posizionamento candidato deve superare **i tre filtri e le quattro regole**, non bastano due su tre.
  **I TRE FILTRI**: (1) VENDUTO — fra le prime categorie per quantità nella matrice di
  `menu-engineering`; (2) MARGINE — in euro per porzione sopra la media del menu, mai in % di food
  cost; (3) CLIENTE — la cosa più citata nelle risposte aperte dei sondaggi e nelle recensioni. I
  PUZZLE (margine alto, venduto basso) sono candidati di "serie B": prima si spingono, poi si guarda se
  il venduto sale. Se nessun candidato passa tutti e tre, il locale non ha un posizionamento ma un
  elenco di piatti: il lavoro diventa accorciare il menu (→ `menu-engineering`), non scrivere la frase.
  **LE QUATTRO REGOLE** (se ne salta una, non regge): DOMANDA (la cerca anche chi non conosce il
  locale, su guide/classifiche/Google?); MARGINALITÀ (se il 30% in più dei clienti la ordinasse, il
  margine diretto salirebbe? se scende, è scelta sbagliata); CREDIBILITÀ (prove con anno e giuria, n°
  recensioni, nome e provenienza dei fornitori — coincide col test del vicino del percorso di
  posizionamento); SCALABILITÀ (deve stare in una scheda tecnica o una procedura: se sta solo nelle
  mani di una persona, è una persona — e le persone se ne vanno). Restano SPAZIO e MATEMATICA DELLA
  NICCHIA sopra.
- **Se il locale esiste già, valida anche sui dati di cassa, non solo a stima.** (a) **Tavoli di
  nicchia**: dal dettaglio scontrini, isola i tavoli con almeno un piatto della nicchia candidata e
  confronta quota di tavoli, spesa a coperto e a tavolo con gli altri — il valore spesso sta nel
  TAVOLO (chi sceglie il locale per quel piatto porta tutto il tavolo), non nel singolo piatto. (b)
  **Forbice prenotazione/cassa**: le note di prenotazione sono un pavimento, non il quadro reale — una
  parte di chi ha un bisogno/allergia lo dice solo a tavola, mai in prenotazione; valuta di aggiungere
  la domanda in prenotazione. (c) **Campioni piccoli**: un indizio statistico debole si scrive "indizio,
  non prova", non si presenta come fatto. (d) **Riverifica sul venduto**: la parola candidata si
  ricontrolla con almeno 3 mesi di vendite per piatto/reparto prima della call col cliente — un piatto
  che "sembra" il posizionamento ma non cresce nel venduto reale non lo è. (e) Le ipotesi nascono dai
  numeri di cassa (quota d'incasso per reparto/fascia); le spinte del titolare che i numeri non reggono
  si congelano, dichiarandolo.
- **Due livelli, canali diversi**: se la nicchia è stretta, scrivi sia il MOTORE per tutti (canali di
  massa: ads generiche, scheda Google, social) sia il CAVALLO DI BATTAGLIA di nicchia (canali della
  tribù: filtri di TripAdvisor/Google, directory e community, carta, domanda in prenotazione) — i due
  messaggi non competono per lo stesso spazio. Verifica che il cliente compaia nei filtri della tribù
  pertinenti (es. filtro "senza glutine" di TripAdvisor): se manca, farsi taggare è spesso una mossa
  gratuita.

(contributo di Andrea Chirivì, 12/10/2026; i tre filtri e le quattro regole sono di Roberto Falcon,
Piano Marketing RBR v1.0)

### 5. Sintesi: la scheda market discovery (1 pagina)
Produci la **scheda market discovery** — 1 pagina, questa struttura fissa:

1. **Bacino** — raggio, segmenti cliente con peso, stagionalità (3 righe)
2. **Posizionamento raccomandato** — LA frase (formato Merenda) + 2 alternative scartate e perché
3. **3 angoli di attacco** — i 3 difetti/gap di zona più sfruttabili, ognuno agganciato a un moltiplicatore Abraham (più clienti / scontrino / frequenza)
4. **Pricing di zona** — fascia dei competitor + dove si colloca il cliente (mai "il più economico": il prezzo segue il posizionamento). Questo pricing passa a `menu-engineering` e `carta-menu-rbr`: ogni ritocco di prezzo dei menu fissi del cliente si riconcilia col mercato di zona, non solo coi costi — si confronta col mercato PRIMA di proporre; se il consulente decide diversamente, il rischio si annota e non si ripropone.
5. **Canali prioritari** — dove sta l'attenzione del bacino (Google local, Meta, delivery, GBP, partnership host-beneficiary con poli del passo 1) in ordine di leva. Se la nicchia è stretta, separa i canali di massa (motore) da quelli di tribù (cavallo di battaglia) — vedi passo 4.
6. **Fonti** — elenco numerato URL + data rilevazione

La scheda è l'**input diretto** per: `adv-ristorante` (angoli, keyword, stagionalità, turisti), `seo-local-ristorante` (keyword local, USP per le pagine sede), `campagna-locale` e `strategia-marketing-rbr` (offerta sul posizionamento scelto).

### 6. Consegna
Se la market discovery va consegnata al cliente (non solo uso interno), impacchettala come relazione Word brandizzata con la skill **`relazione-rbr`**: titolo, sezioni della scheda + appendice con tabella competitor e cluster recensioni, fonti in coda. Condividi secondo le regole di default sharing del progetto.

## Regole RBR & trabocchetti
- ⚠️ **Mai numeri senza fonte**: volumi keyword, n° recensioni, prezzi — tutto con URL e data. Se è una stima, scrivi "stima" con ⚠️.
- ⚠️ **Il bacino non è la città**: censire i competitor di tutta Firenze per una pizzeria di quartiere gonfia l'analisi e nasconde i veri rivali. Prima il raggio, poi il censimento.
- ⚠️ **Rating senza volume non vale**: 5,0 con 12 recensioni < 4,4 con 2.400 recensioni. Pesa sempre rating × volume.
- ⚠️ **Nicchia libera ≠ nicchia buona**: la cella vuota della matrice va SEMPRE validata con la matematica della nicchia (passo 4). Se i numeri non reggono, era vuota per un motivo.
- ⚠️ **Recensioni negative del cliente stesso**: se il locale esiste già, passa al setaccio anche le SUE — i difetti percepiti vanno risolti prima di costruirci sopra un posizionamento, o le ads amplificano il problema.
- ⚠️ **Turisti**: quantificali con proxy verificabili (lingua recensioni, hotel nel raggio), non a sensazione — cambia canali, lingue e stagionalità di tutto il piano.
- ⚠️ **API-first**: WebSearch/WebFetch prima, automazione UI del browser solo dove è l'unica via (Maps, aggregatori). Niente scraping massivo: bastano i 5-10 competitor rilevanti del bacino.
- ⚠️ **"Unico/primo/l'unico certificato" si verifica con fonti terze**: prima di scriverlo, cerca i competitor con la stessa caratteristica (registro/app dell'ente certificatore, TheFork, prenotatori, menu online, recensioni). Una certificazione non si pubblica finché non hai il numero dell'attestato.
- ⚠️ **Due ricerche di posizionamento = verifica incrociata**: se esistono due ricerche (due sessioni, o una valutazione esterna), prima di consegnare verificale punto per punto alle fonti e registra le correzioni in una tabella in fondo al file diagnostico. Per orari e giorni di chiusura fanno fede Google, TheFork e il locale, non le directory generaliste.
- ⚠️ **La market discovery scade**: se tra la scheda e la call di posizionamento sono passate più di 2-3 settimane, prima della call rifai almeno il censimento del bacino e la verifica delle celle vacanti — una categoria libera tre settimane fa può non esserlo più. Ogni scheda riporta la data di rilevazione in testa, non solo sulle singole fonti.
- 🟡 Il posizionamento raccomandato si **discute col cliente/consulente prima** di diventare la base di ads e campagne: la scheda è una proposta, non una sentenza.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Bacino definito (raggio, segmenti con peso, barriere) e tipo di mercato dichiarato (quartiere/città/turistico/mix)
- [ ] Domanda mappata: keyword local con volumi (fonte dichiarata), stagionalità 12+ mesi, occasioni d'uso coperte/scoperte
- [ ] Censimento competitor del bacino completo (tabella) + cluster dei difetti ricorrenti dalle recensioni negative con esempi citati
- [ ] Matrice categoria × zona costruita e nicchia candidata validata con la matematica della nicchia (e coi tre filtri + quattro regole se arriva a candidato finale)
- [ ] Nicchia misurata sui dati di cassa del locale (se esiste) e parola ricontrollata sul venduto degli ultimi 3 mesi
- [ ] Scheda market discovery 1 pagina prodotta (posizionamento + 3 angoli + pricing + canali + fonti numerate)
- [ ] Ogni numero della scheda ha fonte con URL e data; le stime sono marcate ⚠️
- [ ] Affermazioni di unicità verificate su fonti terze; se ci sono due ricerche/versioni, tabella delle correzioni
- [ ] Market discovery non più vecchia di 2-3 settimane rispetto alla call di posizionamento (altrimenti: censimento e celle vacanti rifatti)
- [ ] Posizionamento discusso con cliente/consulente (🟡) prima di passare ad `adv-ristorante` / `seo-local-ristorante` / `campagna-locale`
- [ ] Se consegnabile al cliente: relazione Word prodotta con `relazione-rbr`
