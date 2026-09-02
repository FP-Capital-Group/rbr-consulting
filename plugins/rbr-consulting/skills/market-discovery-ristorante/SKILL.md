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
- **Automazione UI del browser** (browser tool) — scraping UI dove l'API non arriva: Google Maps (lista competitor, rating, n° recensioni, fascia prezzo), Glovo/Just Eat/Deliveroo (chi domina il delivery in zona), TheFork/TripAdvisor. Regola API-first: prova prima WebSearch/WebFetch, il browser è il fallback.
- **Regola d'oro: ogni numero ha una fonte citata** (URL + data di rilevazione). Un numero senza fonte non entra nella scheda.

## Procedura

### 1. Perimetro: la zona vera, non quella immaginata
Definisci il **raggio reale di attrazione** del locale (o del punto candidato):
- **Tipo di bacino**: quartiere (pizzeria d'asporto ~1-2 km), città (locale destinazione ~10-15 min auto), turistico (centro storico/località balneare → il bacino sono i flussi, non i residenti). Molti locali sono un mix: quantifica le componenti (proxy: lingua delle recensioni Google → % turisti).
- **Chi vive/lavora/passa nella zona**: residenti (età, famiglie vs single — dati ISTAT/comune via WebSearch), uffici e poli di lavoro (pranzo feriale), scuole/università, hotel e attrazioni (turisti), cinema/teatri/stadi (flussi serali a evento).
- **Barriere fisiche**: fiumi, ferrovie, ZTL, parcheggio. Un locale a 800 m "in linea d'aria" può essere fuori bacino se in mezzo c'è una barriera.

Output del passo: mappa mentale del bacino con 2-4 **segmenti cliente della zona** (es. "coppie 30-45 del quartiere", "impiegati pranzo feriale", "turisti EN mag-set") e peso stimato di ciascuno.

### 2. Domanda: cosa cerca la gente della zona
- **Keyword local**: "ristorante/pizzeria/<cucina> + <città/quartiere>", "migliore <piatto> a <città>", "<piatto> vicino a me", varianti EN se c'è componente turistica ("best pizza in <city>"). Volumi da keyword planner (via MCP Google Ads) o Google Trends; se stimati, dichiaralo con ⚠️.
- **Stagionalità**: Google Trends 12-24 mesi sulle keyword principali + calendario locale (eventi, fiere, stagione turistica). Segna i mesi di picco e di morto — servono ad `adv-ristorante` per il budget.
- **Occasioni d'uso** presenti in zona e loro copertura: pranzo lavoro, cena coppia, famiglie weekend, gruppi/compleanni, aperitivo, turisti, delivery serale. Per ciascuna: c'è domanda? chi la serve oggi? (incrocio col passo 3).

### 3. Offerta: censimento competitor
Censisci i competitor nel bacino (non tutta la città: solo il raggio del passo 1). Per ciascuno, tabella con:

| Campo | Fonte |
|---|---|
| Nome, categoria (pizzeria, trattoria, fine dining…) | Google Maps |
| Rating e **n° recensioni** (il volume pesa più del voto) | Google Maps |
| Fascia prezzo (€/€€/€€€, scontrino stimato dal menu) | Maps + sito/menu |
| Presenza delivery e ranking (chi esce primo su Glovo/Just Eat/Deliveroo in zona) | app aggregatori (a mano se serve) |
| Social: follower, frequenza post, se rispondono alle recensioni | IG/FB, Maps |
| Posizionamento dichiarato (di cosa si dicono "i migliori") | sito, bio, insegna |

**Miniera d'oro: le recensioni negative dei competitor.** Leggi le 1-2 stelle degli 5-8 competitor principali e clusterizza i difetti ricorrenti (attesa lunga, personale scortese, porzioni, rumore, prezzo/qualità, no opzioni gluten-free/veg…). Ogni difetto ricorrente della zona = **opportunità di posizionamento** per il cliente ("il locale dove NON succede X"). Cita 2-3 recensioni esemplari per cluster (testo + data).

### 4. Gap di posizionamento (framework Merenda)
Costruisci la **matrice categoria × zona**: righe = categorie/specializzazioni possibili (pizza napoletana, carne alla brace, senza glutine certificato, cucina di pesce, brunch, famiglie con bimbi…), colonne = chi le occupa già nel bacino e con che forza (rating × volume recensioni × coerenza del messaggio).

- Cerca le celle **vuote o presidiate male**: categoria con domanda (passo 2) ma senza un "numero 1" riconoscibile → lì il cliente può essere primo.
- **Matematica della nicchia** (validazione): la nicchia scelta deve reggere i numeri. Stima: bacino × % segmento interessato × frequenza plausibile × scontrino di zona → confronta col fatturato che il locale deve fare (coperti × servizi). Una nicchia "libera" ma da 50 coperti/mese non è un posizionamento, è un hobby. Se la nicchia è stretta, verifica che sia il **cavallo di battaglia** di un locale che serve anche il resto, non l'unico prodotto.
- Il posizionamento candidato deve superare il test Merenda: una frase sola, ripetibile a un amico, con prove verificabili (non aggettivi).

### 5. Sintesi: la scheda market discovery (1 pagina)
Produci la **scheda market discovery** — 1 pagina, questa struttura fissa:

1. **Bacino** — raggio, segmenti cliente con peso, stagionalità (3 righe)
2. **Posizionamento raccomandato** — LA frase (formato Merenda) + 2 alternative scartate e perché
3. **3 angoli di attacco** — i 3 difetti/gap di zona più sfruttabili, ognuno agganciato a un moltiplicatore Abraham (più clienti / scontrino / frequenza)
4. **Pricing di zona** — fascia dei competitor + dove si colloca il cliente (mai "il più economico": il prezzo segue il posizionamento)
5. **Canali prioritari** — dove sta l'attenzione del bacino (Google local, Meta, delivery, GBP, partnership host-beneficiary con poli del passo 1) in ordine di leva
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
- 🟡 Il posizionamento raccomandato si **discute col cliente/consulente prima** di diventare la base di ads e campagne: la scheda è una proposta, non una sentenza.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Bacino definito (raggio, segmenti con peso, barriere) e tipo di mercato dichiarato (quartiere/città/turistico/mix)
- [ ] Domanda mappata: keyword local con volumi (fonte dichiarata), stagionalità 12+ mesi, occasioni d'uso coperte/scoperte
- [ ] Censimento competitor del bacino completo (tabella) + cluster dei difetti ricorrenti dalle recensioni negative con esempi citati
- [ ] Matrice categoria × zona costruita e nicchia candidata validata con la matematica della nicchia
- [ ] Scheda market discovery 1 pagina prodotta (posizionamento + 3 angoli + pricing + canali + fonti numerate)
- [ ] Ogni numero della scheda ha fonte con URL e data; le stime sono marcate ⚠️
- [ ] Posizionamento discusso con cliente/consulente (🟡) prima di passare ad `adv-ristorante` / `seo-local-ristorante` / `campagna-locale`
- [ ] Se consegnabile al cliente: relazione Word prodotta con `relazione-rbr`
