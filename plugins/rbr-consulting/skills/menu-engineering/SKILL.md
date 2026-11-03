---
name: menu-engineering
description: >-
  Metodo RBR di menu engineering — dai dati di vendita al menu grafico stampabile. Usala ogni volta che devi analizzare o rifare il menu di un ristorante cliente: "facciamo menu engineering", "analizza il menu di X", "quali piatti tenere/togliere", "rifammi il menu in PDF", "come posiziono i piatti", "revisione prezzi menu". Applica i 5 pilastri + matrice Kasavana-Smith (Star/Plowhorse/Puzzle/Dog), produce raccomandazioni di riposizionamento/pricing/design e genera il menu grafico professionale (PDF weasyprint+Jinja2, upload Drive). NON ridisegnare mai un menu senza aver prima classificato i piatti con questa skill.
---

# Menu engineering (dati → decisioni → menu grafico)

## Perché esiste
Il menu è lo strumento di vendita più letto del ristorante e quasi nessun ristoratore lo progetta con metodo. In RBR il menu si tratta come un asset economico: ogni piatto ha un margine e una popolarità, e la posizione/descrizione/prezzo si decidono sui numeri, non a occhio. Questa skill porta dal dato grezzo di vendita fino al PDF stampabile, passando per una classificazione oggettiva. La regola RBR: **prima classifichi i piatti, poi decidi il layout.** Un menu "bello" che spinge un Plowhorse nello sweet spot fa perdere soldi.

## Quando usarla
- Un cliente vuole rivedere, tagliare o ridisegnare il menu.
- Hai i dati di vendita (unità vendute) e i food cost e vuoi capire cosa tenere/spingere/togliere.
- Devi produrre un menu grafico professionale pronto per stampa o digitale.
- Il cliente lamenta margini bassi o "vendo solo i piatti che rendono poco".

## Prerequisiti
- Per ogni piatto: **nome, categoria, prezzo di vendita, food cost (€ o %), unità vendute** nel periodo (min 1 mese, meglio 3).
- Se manca il food cost o le unità vendute → classificazione non affidabile: raccoglili prima (vedi skill `riconciliazione-dati-cliente` per validare i dati).
- ⚠️ **Venduto completo, non un campione.** Su iPratico la pagina *Products profit margin* sembra la scorciatoia (ha il "Costo medio di acquisto") ma restituisce poche decine di prodotti su centinaia: la matrice esce sbagliata. Il venduto vero sta in *Totalizzazioni* → *DETTAGLIO CATEGORIA PER QUANTITÀ*; le righe di *DETTAGLIO VARIANTI* sono quasi tutte istruzioni di cucina o marcatori di portata già contati (non sommarle), salvo nei menù a formula dove i piatti scelti vanno usati al posto del forfait. Procedura: skill `estrai-dati-ipratico`. *(contributo di Luciano Purpi, 2026-09-03)*
- Stile del cliente: riferimento visivo, URL sito, screenshot o PDF di un menu esistente.
- Per l'output PDF: stack agente Alex (`agents/alex/`, weasyprint+Jinja2+Drive). API key e credenziali Drive stanno nel `.env` dell'agente, mai nel repo.

## Procedura

### 1. Prepara la matrice
Per ogni piatto calcola:
- **Margine di contribuzione** = prezzo (IVA esclusa) − food cost. Regola RBR: economici sempre IVA esclusa (÷1.1 ristorazione).
- **Popolarità** = unità vendute del piatto ÷ unità totali della categoria.
Confronta ogni piatto con le due mediane della sua categoria: sopra/sotto la mediana margine e sopra/sotto la mediana popolarità.

*(contributo di Andrea Chirivì, 2026-10-12)* Tre regole aggiuntive:
- Margine e food cost si calcolano **due volte**: sul listino e sull'incassato (con
  sconti da aggregatore il cibo spesso incassa sotto listino mentre le bevande incassano
  il listino pieno). Il target di food cost si fissa sull'incassato.
- Per i piatti con prezzo che varia, usa il **prezzo medio vero di cassa** (valore ÷
  pezzi), non quello di carta.
- I piatti da condividere (taglieri, piatti per 2-6) si misurano **a persona, per ogni
  formato**: il formato più "celebrato" può essere quello che rende meno a testa. Un
  prezzo nuovo si carica in cassa partendo dal prezzo fisso di cassa, non dal teorico.

### 2. Classifica con Kasavana-Smith
| Quadrante | Popolarità | Margine | Cosa fare |
|-----------|-----------|---------|-----------|
| ⭐ STAR | Alta | Alto | Sweet spot, proteggi, non toccare prezzo né ricetta |
| 🐴 PLOWHORSE | Alta | Basso | Togli dallo sweet spot, riduci porzione o alza prezzo 2-3%, abbina add-on |
| 🧩 PUZZLE | Bassa | Alto | Promuovi: foto, descrizione ricca, sweet spot, box/callout |
| 🐕 DOG | Bassa | Basso | Elimina o nascondi in zona morta del menu |

*(contributo di Andrea Chirivì, 2026-10-12)* La matrice si legge anche **per reparto**:
se un reparto rende di più a piatto, diventa l'argomento di sala da proporre per primo al
tavolo e il soggetto delle campagne. L'obiettivo di menu engineering si scrive anche come
spostamento del mix fra reparti, col valore a coperto (es. mix pizza/cucina 75/25 →
50/50). Le Star sono i piatti da mettere in ads/campagne; i Puzzle si raccontano e si
fanno assaggiare in sala.

### 3. Applica i 5 pilastri
1. **Limita la scelta** — max 7 piatti/categoria (Miller 7±2; studio marmellata: 6 opzioni convertono 10× di 24). Elimina i Dog, crea sotto-categorie se serve.
   - **Listini lunghi (bar, gastronomie, banchi, carte vini/bevande)** *(contributo di
     Andrea Chirivì, 2026-10-12)*: il tetto di 7 voci non copre questi casi. Metodo:
     (1) **misura** — incrocia il listino di cassa col venduto, conta le voci attive senza
     vendite e il peso in cassa delle famiglie lunghe; (2) **verifica sugli acquisti** —
     controlla la carta bevande sulle fatture degli ultimi mesi, ciò che non si compra
     non si vende, i tasti con prodotti non più acquistati si puliscono; (3) **gruppi
     prima del taglio** — dividi la coda in: "negozio dentro il locale", banco fresco a
     rotazione minima (taglio urgente), vini (decisione di cantina, non di cassa: chiedi
     cosa è in conto vendita), accorpamenti, tasti di tracciamento dei menu fissi (non si
     toccano), errori di catalogo; (4) la misura della diluizione si porta al cliente
     prima del taglio, e la lista si chiude col titolare sul posto.
   - **Vincolo di produzione in cucina unica** *(contributo di Andrea Chirivì,
     2026-10-12)*: il menu si giudica anche sul numero di preparazioni contemporanee
     (pezzi per referenza a sera). Ogni taglio porta scritto il motivo (produzione o
     margine) — i contorni, ad esempio, spesso marginano bene e si tagliano solo per la
     produzione, a parità di porzioni vendute. Il food cost si confronta dentro la stessa
     famiglia (es. in friggitoria due fritti diversi possono avere FC molto diverso).
     Quando i margini dei piatti stanno in pochi euro di differenza, la matrice si fa ma
     conta poco: decidono preparazioni e scarto. Un prodotto nuovo si progetta sul collo
     di bottiglia delle attrezzature (es. una sola friggitrice).
2. **Metti tutto al posto giusto** — Star e Puzzle negli sweet spot (variano per formato, vedi sotto). Primo e ultimo piatto della lista = più ricordati (primacy/recency) → mettici alto margine.
3. **Fai tornare i conti** — prezzi senza simbolo €, inline dopo la descrizione (mai colonna allineata a destra), no `.99` sui livelli medio-alti, anchor pricing (piatto costoso in cima alla sezione).
4. **Cura l'estetica** — max 1-2 foto/pagina (solo professionali, +30% vendite), max 3 colori e 2 font, white space attorno ai premium, max 2-3 box/callout per pagina.
5. **Emoziona** — nomi descrittivi (+27% vendite, Wansink 2001) e descrizioni sensoriali sui piatti da spingere, così l'attenzione va sul piatto e non sul prezzo. Anche la foto sul piatto ad alto margine spinge le vendite; le decisioni si prendono sul margine in euro, non sulla percentuale *(contributo di Andrea Chirivì, 2026-10-12)*.

**Sweet spot per formato:** pagina singola → centro-alto; bifold → metà alta pagina destra (Golden Triangle); trifold → pannello centrale; libro → prime 2 pagine (80% attenzione).

### 4. Scrivi le raccomandazioni
Produci un documento con, per ogni piatto: quadrante, azione consigliata, motivazione numerica. Elenca separatamente: piatti da togliere, prezzi da ritoccare (con nuovo prezzo proposto), piatti da promuovere e dove posizionarli. Numera le decisioni aperte da discutere col cliente.

Le scelte che costruisce il consulente (composizione, prezzi, grammi di una proposta) si
portano al cliente come **proposta da approvare in blocco**, non come verifiche voce per
voce. Al cliente si chiedono solo i suoi fatti (piatti SG, ricette e grammi esistenti,
costi d'acquisto mancanti): le decisioni aperte numerate restano solo per i veri bivi
(es. un piatto Star che lo chef vuole togliere). *(contributo di Andrea Chirivì,
2026-10-12)*

**Quando arriva una carta nuova** (dello chef o nostra) da approvare, verifica sempre sul
venduto di cassa prima di approvarla: riprezzatura dei piatti tenuti a volumi costanti
della stagione giusta, incasso dei piatti tolti (e perché sono stati tolti — se un piatto
marginava comunque, toglierlo per il food cost è stato un errore), buchi della carta
(pagina pranzo assente, SG invisibile, categorie oltre 7 voci), voci senza costo, e il
confronto fra le versioni successive della carta sui volumi della stagione giusta
(abbassare i prezzi fra una bozza e l'altra senza accorgersene costa caro). Segnala il
rischio volumi quando il prezzo nuovo supera molto quello pagato l'anno prima.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 5. Genera il menu grafico
Passa i dati all'agente Alex nel formato `menu_data` (`nome_ristorante`, `categorie[]` con `piatti[]` → `nome/descrizione/prezzo/nota`) + `style_config` (colori, font, layout, formato). Vedi `agents/alex/CLAUDE.md`.
- Estrai il brand del cliente da sito/screenshot/PDF (`brand_extractor`) o imposta i colori a mano.
- Scegli colori/font per tipo di locale (pizzeria: rosso+bianco+verde; fine dining: nero+oro; trattoria: marrone+crema…). Max 2 font, mai 2 serif insieme.
- `build_menu(menu_data, style)` → PDF; `build_menu_all(...)` → PDF + IDML editabile.
- `upload_to_drive(pdf, folder_id)` → link nella cartella cliente. Condividi come da baseline RBR.

### Controlli standard da fare all'inizio (contributo di Luciano Purpi, 2026-09-03)
- **Pulizia del venduto prima della matrice** *(contributo di Andrea Chirivì, 2026-10-12)*:
  (a) piatto caricato due volte nel POS in categorie diverse → cerca per nome normalizzato
  su tutte le categorie e somma prima di classificare; (b) varianti SG dello stesso piatto
  si escludono come doppioni del piatto base (dividerebbero la popolarità); (c) verifica
  l'unità di vendita in cassa per i piatti a peso (kg vs porzioni) prima di usare volumi e
  margini; (d) escludi dalla classifica i giorni di guasto del registratore; (e) dichiara
  quanta parte dell'incasso copre la matrice (es. 94,8%) e cosa resta fuori apposta
  (coperto, menu cerimonie); (f) prendi i volumi nella stagione della carta che stai
  facendo (un +€/anno sui volumi estivi non vale per il menu invernale).
- **Cassa senza dettaglio per piatto**: se la cassa batte voci generiche ("primo piatto",
  "menu completo") la matrice non si può costruire. Soluzione: menu battuto a prezzo
  pieno + tasti a 0€ per i singoli piatti dentro i menu fissi, tasti specifici al posto di
  quelli generici, un tasto per ogni formato (es. tagliere da 3/4/5/6 persone, ognuno col
  suo food cost) e due tasti seduto/asporto. Servono almeno 3 mesi di dati. Nella pulizia
  degli articoli "morti" NON si cancellano mai i tasti a 0€ che tracciano i piatti dentro
  i menu fissi, né la busta d'asporto.
- **Audit della carta in vigore contro cassa e cucina**: confronta riga per riga la carta
  stampata col venduto e con quello che la cucina produce davvero (piatti senza prezzo
  stampato, piatti con un ingrediente non più in uso). Il prezzo mancante si ricava dal
  venduto (valore ÷ pezzi) e si verifica col prezzo battuto prima di stampare. Confronta
  anche i coperti reali coi coperti battuti in cassa: un tavolo su tre senza coperto
  battuto è una leva misurabile (vedi skill `analisi-venduto-fasce`, trappola "coperto non
  battuto").
- **Food cost splittato food / drink**, con coperto e servizio FUORI da entrambi (è ricavo senza costo). Il drink cost può superare il food cost e nessuno lo guarda: pizzeria reale giu-lug 2026 food 21,3% vs **drink 22,2%**, colpa di bibite in bottiglia 33 cl (Coca Cola/Sprite/Fanta ~26,5%) e birre in bottiglia (28-30%); reggono solo acqua (10-18%) e spritz (17-20%). In pizzeria le bevande devono finanziare il margine, non eroderlo.
- **Prezzi divergenti sui canali**: stessa pizza a 9 / 10 / 11,50 fra menu del sito, POS e piattaforma delivery. Va allineato (o deciso) prima di classificare.
- **Il canale cambia il margine**: la matrice è per piatto, ma un piatto venduto in delivery con commissione al 32% rende molto meno che in sala. Se il delivery pesa, leggi la classificazione insieme al margine per canale della skill `analisi-modello-business`.
- **Menu delivery integrato**: se il POS pubblica il menu tramite un middleware (es. Deliverect), il Menu Manager della piattaforma è vuoto e senza pulsante "crea" — non è un bug. Si modifica nel middleware (dal portale viene sovrascritto al primo sync): chiedi al cliente le credenziali del middleware PRIMA di promettere il lavoro sul menu delivery.

### Bevande e vino *(contributo di Andrea Chirivì, 2026-10-12)*
- Il drink cost si legge **per famiglia**, non solo in totale: bibite/aperitivi/birre/
  cocktail stanno al 15-23%, i vini in bottiglia al 43-50% (è normale: sul vino si
  guadagna in valore assoluto). Il vino in bottiglia si legge in € di margine, non fa
  scattare da solo l'allarme "drink > food".
- Il calice è spesso la voce che rende di più a persona: carta corta (2 fissi, 2 a
  rotazione, una bollicina), sempre proposto come abbinamento al piatto, mai incluso nel
  prezzo. Escono i calici troppo cari o che non girano.
- Pezzi per coperto: dal venduto calcola "uno ogni N coperti" per vino/acqua/dolci e la %
  di tavoli col dolce, poi porta la leva in euro (+1€ a coperto × coperti di stagione) —
  *da verificare su più clienti, metodo usato finora su un caso solo*.
- Per i locali con cantina: confronta le bottiglie comprate da fattura con bottiglie e
  calici battuti in cassa. Un divario forte segnala vino non battuto (menu evento, vino
  della casa, bollicine al calice, vino usato in cucina) o venduto sotto carta. Verifica
  prima gli inventari del gestionale: possono essere incompleti.

### 6. Misura dopo il lancio *(contributo di Andrea Chirivì, 2026-10-12)*
Confronta il venduto per articolo mese per mese, prima e dopo il cambio carta: scrivere o
non scrivere un piatto ne cambia le vendite, e un piatto che sale dopo essere stato
scritto non deve uscire. Scomponi il valore del menu rifatto in **effetto listino**
(variazione % dei prezzi) ed **effetto mix/porzioni** (pezzi ogni 100 coperti per
categoria, prima e dopo): il margine a coperto è la somma dei due, moltiplicato per i
coperti dal lancio — è il valore del menu da presentare al cliente.

## Normativa (ott 2026)
Prima di consegnare qualsiasi carta: `references/normativa-menu.md` — allergeni (menu o registro scritto + dicitura), asterisco su ogni piatto congelato, menu con prezzi esposto fuori, QR mai da solo, coperto vietato nel Lazio, legge antifrode 75/2026 (DOP/provenienze solo se documentati), niente bistecca/filetto per piatti vegetali.

## Regole RBR & trabocchetti
- ⚠️ Mediane **per categoria**, non sull'intero menu: un antipasto e un secondo non si confrontano.
- ⚠️ Food cost mancante = margine inventato. Non classificare a occhio, chiedi i dati.
- ⚠️ Non spingere mai un Plowhorse nello sweet spot: alza i volumi del piatto che rende meno.
- ⚠️ Prezzi economici sempre IVA esclusa; se la fonte non lo specifica assumi esclusa e segnala 🟡.
- ✅ Un menu ideale RBR: 5-7 categorie × 5-7 piatti, 2-3 Puzzle promossi, Dog eliminati, anchor in cima ad ogni sezione.
- ❌ Mai `.99`, mai simbolo €, mai colonna prezzi allineata a destra.
- Segreti/token → sempre dal `.env` dell'agente, mai scritti qui (repo condivisa col team).

## Definition of Done
- [ ] Ogni piatto ha margine di contribuzione e popolarità calcolati per categoria
- [ ] Ogni piatto classificato Star/Plowhorse/Puzzle/Dog contro le mediane di categoria
- [ ] Raccomandazioni scritte con azione + motivazione numerica per piatto
- [ ] Decisioni aperte (tagli, ritocchi prezzo) numerate e discusse col cliente
- [ ] 5 pilastri applicati al layout (scelta, posizione, prezzi, estetica, nomi)
- [ ] Checklist legale di `references/normativa-menu.md` passata
- [ ] Menu grafico generato (PDF, eventuale IDML), caricato su Drive e condiviso
- [ ] Venduto pulito prima della matrice (doppioni, varianti SG, unità a peso, stagione)
- [ ] Se c'è una carta nuova da approvare: verificata sul venduto di cassa prima del sì
- [ ] Dopo il lancio: misurato l'effetto sul venduto per articolo e il valore in coperti
