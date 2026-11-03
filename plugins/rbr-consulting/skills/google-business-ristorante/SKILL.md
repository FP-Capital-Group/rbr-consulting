---
name: google-business-ristorante
description: >-
  Gestione operativa del Google Business Profile di un ristorante — ottimizzazione completa
  della scheda (categorie, attributi, menu, foto, link prenotazione), strategia recensioni
  (come chiederle e come rispondere, tono RBR, mai comprarle), post e offerte ricorrenti,
  monitoraggio insight (chiamate, indicazioni, visite al sito) — con la mappa 2026 di cosa
  è automatizzabile via Business Profile API e cosa resta UI. Usala per il lavoro
  ricorrente sulla scheda di un locale — "sistemiamo la scheda Google del ristorante",
  "rispondiamo alle recensioni", "piano post GBP del mese", "il cliente vuole più chiamate
  da Google Maps", "carichiamo il menu sulla scheda", "quante indicazioni stradali questo
  mese". Per il playbook SEO complessivo (pagine local, keyword, multilingua) usa invece
  `seo-local-ristorante`: questa skill è il braccio operativo della sola scheda GBP.
---

# Google Business Profile ristorante (operatività scheda)

## Perché esiste
Per un ristorante il GBP è **il canale #1**: la maggior parte dei clienti nuovi decide su Google Maps, non sul sito. `seo-local-ristorante` dice *perché* e *dove* il GBP sta nel playbook; questa skill dice *come* si lavora la scheda ogni settimana/mese: ottimizzazione campo per campo, macchina delle recensioni, cadenza post, lettura insight — e quale pezzo si automatizza via API (accesso che va richiesto e approvato da Google) vs cosa resta manuale (UI).

## Quando usarla
- Presa in carico della scheda di un nuovo cliente: audit e ottimizzazione completa.
- Routine ricorrente: risposte recensioni, post settimanali, offerte, report insight mensile.
- Il cliente vuole più chiamate/indicazioni/prenotazioni da Google Maps.
- Valutare se attivare l'automazione API (multi-sede, tante recensioni) o restare manuali.

## Prerequisiti
- **Proprietà/gestione della scheda** per ogni sede sull'identità team **fpcgmedia@gmail.com** (ruolo Gestore basta; Proprietario per i trasferimenti). ⚠️ Trabocchetto noto: le schede spesso vivono su un account Google diverso da quello "principale" del cliente — verificalo per primo (vedi `seo-local-ristorante` punto 4).
- **Business Profile API (stato 2026)** — NON è aperta: i progetti Google Cloud partono con **quota zero** e serve una **richiesta formale di accesso** a Google (form, caso d'uso legittimo, GBP verificato da 60+ giorni, sito web; approvazione da giorni a settimane). Una volta approvato, 8 API distinte; quelle utili qui:
  - **Business Information API** (`mybusinessbusinessinformation`) — nome, indirizzo, orari, categorie, attributi (limite ~10 edit/min per profilo)
  - **Reviews (v4)** — lettura recensioni + **risposta programmatica** (creare/modificare la risposta; MAI creare recensioni: l'API non lo permette, e comprarle è vietato)
  - **Local Posts (v4)** — creazione post standard, eventi e offerte, inclusi i **post ricorrenti**
  - **Performance API** (`businessprofileperformance`) — metriche giornaliere: impression Maps/Search, chiamate, richieste indicazioni, click sito
  - NON esiste MCP ufficiale Google per GBP (agosto 2026): si opera via API REST con OAuth su fpcgmedia@gmail.com.
- **Fallback UI** (regola API-first): finché l'accesso API non è approvato — o per ciò che l'API non copre (gestione foto/media, Q&A, menu con foto, messaggi, impostazioni chiamate) — si lavora dalla UI business.google.com, a mano .
- Materiale cliente: foto professionali recenti, menu aggiornato con prezzi, link prenotazione (Resmio), NAP ufficiale per sede.

## Procedura

### 1. Audit e ottimizzazione scheda (una volta, poi trimestrale)
Campo per campo, per ogni sede. È la **Mossa 6 del Piano Marketing RBR**, dopo il posizionamento: l'audit si fa un'ora prima, cercando il locale come lo cerca davvero un cliente.
- **Categoria principale** = quella più specifica e cercata ("Pizzeria", non "Ristorante" se è una pizzeria), coerente anche con la promessa del locale, + secondarie reali (Ristorante, Pizza da asporto…). La categoria principale pesa più di ogni altro campo.
- **Descrizione**: campo spesso trascurato nell'audit. Apre con la promessa del locale e contiene prove, zona e prodotto — non un elenco generico.
- **Attributi** veri e completi: vegano, vegetariano, biologico, asporto, domicilio, dehors, accessibile, prenotazione consigliata. Ogni attributo è un filtro di ricerca su Maps.
- ⚠️ **Il senza glutine NON ha né categoria né attributo** (contributo di Luciano Purpi, 2026-09-03, verificato il 16/08/2026): nessuna categoria "ristorante senza glutine" nell'elenco italiano, nessun flag dietetico fra gli attributi "Proposte" oltre vegano/vegetariano/biologico, e nel form del singolo piatto "Regimi alimentari" offre solo Vegetariano e Vegano. Per i clienti gluten-free la nicchia su Google passa SOLO da descrizione, menù e recensioni: dirlo al cliente prima di prometterlo.
- **Orari** esatti + orari speciali per festività (una scheda "forse chiuso" perde la chiamata).
- **Domande e risposte**: popolarle con le domande che arrivano davvero al telefono (parcheggio, bambini, terrazza, la domanda che crea equivoci). ⚠️ Verificare prima che la sezione esista ancora nella UI del cliente: Google genera sempre più spesso le Q&A con l'AI (vedi 👀 novità più sotto).
- **Menu**: caricato nella sezione dedicata con prezzi (non solo PDF sul sito), foto dei piatti principali. Via UI — la parte menu non è coperta in modo affidabile dall'API. Come si carica davvero (contributo di Luciano Purpi, 2026-09-03):
  - **Solo con l'editor multiplo**: tre puntini della SEZIONE (o di una voce) → "MODIFICA PIÙ ELEMENTI" → un campo Prezzo e un cestino per riga, un solo Salva. Si naviga con Tab fra un prezzo e il successivo (il primo Tab prende il cestino), la lista scorre da sola: 33 prezzi e 5 cancellazioni in poche chiamate. Voce per voce è impraticabile in automazione (form lento 5-13 s, pannello bianco dopo il salvataggio, conflitto di estensioni Chrome sul campo Prezzo): ~2 voci in decine di chiamate.
  - **Prezzo col punto** (`11.30`): con la virgola Google risponde "Inserisci un importo valido".
  - **Le foto del menù non si caricano via automazione** (upload dentro iframe): le trascina a mano il cliente o il consulente → va nella checklist di consegna del cliente.
- **Link prenotazione** (Resmio/TheFork) e link ordini delivery: sono le CTA che convertono direttamente dalla scheda. ⚠️ Di norma il link prenotazione della scheda non porta parametri di sorgente → le prenotazioni da Google cadono nel "diretto" (contributo di Luciano Purpi, 2026-09-03). Se è Resmio, usa il link diretto al widget con la fonte (`app.resmio.com/<slug>/widget?source=google-business`, vedi `campagna-locale`); altrimenti dichiara nel report mensile che quelle prenotazioni non sono attribuite, invece di lasciarle sparire.
- **Foto**: **20-30 foto nuove subito alla presa in carico**, poi **3-5 a SETTIMANA** (non al mese) — prodotto, locale, esterno, persone. Gestione media = UI, non API. Le schede con foto recenti battono quelle ferme. *(correzione di cadenza: contributo di Andrea Chirivì su indicazione di Roberto, 2026-10-12)*
- **NAP coerente** con sito e citazioni (vedi `seo-local-ristorante` punto 4 — non ripetere qui l'analisi, solo verificare).
- ⚠️ **Clienti multi-concept nella stessa sede** (contributo di Luciano Purpi, 2026-09-03): due schede allo stesso indirizzo e soprattutto con lo STESSO NUMERO DI TELEFONO sono il segnale n.1 con cui Google rifonde due profili. Per separare due brand servono indirizzo E numero distinti, prima di qualsiasi altra ottimizzazione.

### 2. Macchina delle recensioni
- **Come chiederle**: al momento giusto (fine pasto/consegna), con link diretto recensione (short URL della scheda) su QR al tavolo, scontrino, follow-up post-prenotazione via GHL. Chiedere a TUTTI, mai selezionare solo i clienti contenti (review gating = violazione policy). Il link breve `g.page/r/.../review` si calcola dal place_id, e con Resmio si può mettere nella mail di feedback senza l'add-on a pagamento → `suite/memory/resmio.md`, sezione Recensioni Google (aprire SEMPRE il link generato: 2 place_id su 10 salvati in Resmio erano sbagliati).
- ⚠️ **Dove si apre il link conta più del testo del messaggio.** Il pulsante URL di un template WhatsApp apre il link nella finestra **interna** di WhatsApp (non il browser vero): lì il cliente spesso non è collegato al suo Google e prima delle stelle compare "Accedi" — su un caso misurato, il pulsante ha prodotto 0 recensioni su 210 richieste, il link scritto nel **corpo del messaggio** (aperto nel browser vero) ne ha prodotte diverse. Regola operativa: il link va scritto **nel testo del messaggio**, non come pulsante URL; in alternativa un QR, che si apre dalla fotocamera nel browser vero. La pagina d'arrivo sceglie il link in base al sistema operativo: su Android `g.page/r/<id>/review` porta dritto alle stelline; su iPhone `google.com/maps/search/?api=1&query_place_id=<place_id>` apre l'app Maps con l'account già collegato (verificato); `search.google.com/local/writereview` nel browser chiede spesso l'accesso e va evitato. Il redirect di raccolta (`/recensione/`) deve essere un file fisico o una regola del server, **mai** una rotta WordPress (tempi di risposta altissimi su URL non in cache). Mai il link lungo di ricerca (QR fitto) né il link corto di ricerca (non apre il modulo). ⚠️ **Prova in corso**: la misura sul pulsante WhatsApp è confermata da log; il comportamento su Android da telefono vero (non solo in pagina) e l'effetto di un eventuale sondaggio prima del link Google sulle recensioni raccolte restano da verificare.
- **Flusso automatico di richiesta — regole operative**: trigger sul campo di stato della prenotazione (es. arrivato/concluso), non su un tag isolato. Guardia "già inviata?" in testa, poi tag, poi attesa **12 ore con finestra 10:00-20:00 su 7 giorni** (il messaggio cade sempre la mattina dopo, anche di domenica — mai "il giorno dopo" secco). Lingua scelta dal **prefisso del numero** (+39 o nessun + = italiano, il resto inglese), non da un tag turista. La stessa persona si ri-richiede dopo **60 giorni**, anche se ha già lasciato una recensione — ma lo sblocco vale solo per chi è arrivato in fondo al flusso senza problemi: chi risulta non consegnato o ha fatto opt-out resta escluso per sempre. Prima di dare per buono il flusso, **verificare che parta davvero** (è capitato che fosse configurato e non partisse mai) e che il credito dell'invio (SMS/WhatsApp) non sia esaurito.
- **Cosa chiedere: la richiesta ha un GANCIO TEMATICO legato al posizionamento** (contributo di Luciano Purpi, 2026-09-03 — diagnosi ricorrente su tre clienti). La macchina può girare a pieno regime e raccogliere la cosa sbagliata: cliente A, 200 recensioni in 5 giorni, media 4,89 — ma il 69% dei testi cita un cameriere per nome e solo il 5% dice "leggera/digeribile"; cliente B, la promessa di marca (doppia lievitazione, 36h, leggerezza) compare in 3 testi su 489, zero nella sede principale. Non è la quantità, è **lo script**: in sala si chiede "ci lascia una recensione?" invece di "se le è piaciuta la leggerezza dell'impasto, lo scriva". Lo script giusto spesso esiste già nel manuale di sala: va fatto usare.
- **La frase lecita** da usare nel messaggio/bot/biglietto: *"Se ti sei trovato bene, una recensione ci aiuta più di qualsiasi cosa. E se qualcosa non è andato, scrivimelo qui: preferisco saperlo io."* — chi non si è trovato bene viene invitato a scrivere al titolare, mai a non scrivere affatto. **Mai chiedere né nominare le cinque stelle**, in nessun canale (messaggio, biglietto, bot, personale): la chiusura non deve spingere a cercare problemi ("cosa possiamo fare ancora meglio" va evitato). Dopo il sondaggio/follow-up si mostrano Google e TripAdvisor a tutti, più TheFork solo a chi è arrivato da TheFork. Per portare su Google la reputazione che oggi sta su altre piattaforme, è il **titolare in persona** a scrivere e ringraziare chi ha già recensito altrove (TheFork, TripAdvisor) — a tutti, non solo ai voti massimi, e senza chiedere le stelle: il tono anonimo non funziona quanto quello personale.
- **Recupero una tantum dei clienti passati mai sollecitati**: prima dell'invio si toglie chi ha già recensito (incrociando per nome con le recensioni recenti — risollecitare chi ha già scritto si vede ed è un errore già capitato), si esclude chi è rimasto solo su "confermato" (forse non è nemmeno venuto), e si separano le lingue PRIMA dell'invio, non a metà. Flussi IT/EN gemelli, senza il trigger del flusso automatico, con rientro OFF e senza lo sblocco a 60 giorni: se ci sono già contatti in corso si duplica il flusso invece di cambiare il template in uso.
- **Biglietto al tavolo**, da consegnare a fine cena insieme al conto: formato 85×55mm con 3mm di abbondanza. Tono di chi ha già servito ("Grazie per la serata"), mai "Ciao, sono X". Un titolo che racconta qualcosa, legato al nome o alla promessa del locale — niente frasi ripetute in italiano e inglese. Due QR (Google e TripAdvisor) solo quando pesano in modo simile; mai stelle, offerte o selezione dei tavoli a cui darlo — lo consegna chi ha preso la comanda, a TUTTI i tavoli. Il QR punta al link breve `g.page` (vedi sopra: il link di ricerca dà un QR troppo fitto). **Prima di andare in tipografia, due controlli**: (1) il QR si legge dal **PDF finale** che va in stampa, non dal file di lavoro né dall'anteprima — la conversione finale può appiattire immagini e trasparenze; (2) il QR si scansiona con la fotocamera di un **iPhone vero e di un Android vero**, entrambi devono arrivare al modulo con le stelle e non a una schermata di accesso. ⚠️ Resa ancora da misurare su clienti veri; se un iPhone senza l'app Google finisce su una schermata di accesso, il QR va fatto puntare al redirect proprio (file fisico/regola server, mai CMS) che sceglie il link in base al sistema operativo, non direttamente a `g.page`.
- **Segnali del filtro anti-sollecitazione di Google** (raccolta che lavora a vuoto): testi mediani molto corti (~77 caratteri) e quasi identici, molti profili con zero recensioni precedenti (29% sul cliente A), contatore pubblico fermo mentre la sala ne raccoglie. Se li vedi, rallenta e varia la richiesta prima di spingere sul volume.
- **Mai comprare recensioni, mai recensioni da staff/amici**: rischio sospensione scheda. Non negoziabile RBR.
- **Come rispondere (tono RBR)**: a tutte, entro 48h, **comprese le vecchie e le brutte** (una negativa ben risposta vende più di dieci positive — per l'arretrato vedi `risposte-recensioni-ai-ghl`, Drip Mode). Positive: ringraziamento personale + mirroring naturale delle keyword (il piatto, il quartiere — senza forzare la città in ogni risposta). Negative: mai difensivi, mai copia-incolla — scuse se dovute, versione dei fatti sobria, invito a canale privato (email dedicata low-rating, vedi `seo-local-ristorante`). La risposta la leggono i futuri clienti, non il recensore. **Mai promettere al cliente la rimozione delle negative** (vedi sotto, segnalazione a Google/TripAdvisor): funziona solo per le recensioni davvero fuori tema, non per quelle circostanziate anche se dure.
- **Segnalare a Google/TripAdvisor le recensioni che non sono recensioni**: procedura, motivi che funzionano e aspettative realistiche in `references/segnalare-recensioni.md`.
- **Con accesso API**: pull periodico delle nuove recensioni + bozze di risposta generate e approvate dal consulente prima dell'invio via API — mai risposte pubblicate senza revisione umana.

### 3. Post e offerte ricorrenti
- Cadenza **1 post/settimana per sede** (standard RBR — una scheda ferma è un segnale morto).
- Rotazione mensile tipo: novità/piatto del mese → evento (serata, menu degustazione) → offerta con scadenza (pranzo fisso, aperitivo) → dietro le quinte/team.
- Formato: foto vera del locale (no stock), 80-150 parole, una CTA (Prenota/Chiama/Scopri di più) col link prenotazione. ⚠️ **Immagini orizzontali 1200×900**: le verticali vengono tagliate a metà in anteprima. Un post per evento, pubblicato nella **settimana dell'evento** (mai tutti insieme), sempre con date di inizio e fine impostate. Il link del post porta un `utm` (es. `utm_source=google-scheda`) che il sito riscrive nel modulo/prenotazione, per contare i contatti arrivati dalla scheda (stessa logica del link prenotazione sopra). *(contributo di Andrea Chirivì, 2026-10-12 — conteggio utm non ancora osservato su un caso)*
- **Con accesso API**: calendario post del mese preparato in anticipo e pubblicato via Local Posts API (anche ricorrenti). **Senza**: pubblicazione via UI con lo stesso calendario.
- Le offerte hanno scadenza reale — mai offerte eterne, sviliscono il percepito (coerente con `adv-ristorante`: niente sconti come gancio se il posizionamento è alto).

### 4. Monitoraggio insight (mensile)
Metriche GBP da portare al ristoratore, confronto mese precedente + stesso mese anno prima:
- Impression su **Maps vs Search** (dove ti vedono)
- **Chiamate** dalla scheda
- **Richieste indicazioni stradali** (proxy di clienti che entrano)
- **Click al sito** e **click prenotazione**
- Recensioni nuove + rating medio + tempo medio di risposta
- **Quota di testi che citano la promessa di marca** (e cosa citano davvero: staff, piatto, senza glutine…) — non solo media e numero. Il posizionamento reale è quello che i clienti ripetono (sul cliente B era il senza glutine, 76 citazioni, non quello dichiarato). Per leggere tutte le recensioni con data e voto veri oltre il tetto di 200 del pannello → `references/scarico-recensioni.md`; per l'analisi completa della reputazione → skill `analisi-reputazione-locale`.
- Query con cui la scheda viene trovata (brand vs "pizzeria vicino a me")
- **Distribuzione delle recensioni per stella, confrontata col mese prima** (non solo media e totale): è l'unico modo per vedere se è sparita una negativa o una positiva.

**Resa della richiesta di recensione** — da portare mensile (settimanale nei primi due mesi): imbuto inviati → consegnati → letti → clic → sondaggi iniziati/completati → recensioni Google e TripAdvisor. I "letti" (dalla scheda Statistiche del nodo WhatsApp) sono un minimo, non il dato reale: chi spegne le conferme di lettura non viene contato. Il dato principale è recensioni ÷ persone raggiunte e recensioni ÷ sondaggi completati. I clic si contano solo con un redirect proprio, leggendo i log del server (va tolto il traffico di crawler, che può essere la maggioranza delle righe grezze; lo user-agent separa la finestra interna di WhatsApp dal browser vero). Le recensioni nuove, con nome e ora, si leggono dalle notifiche email del Profilo (più complete del contatore pubblico di Maps) e si abbinano ai destinatari per nome e orario, dichiarando nel report quante restano non abbinabili (nickname).

**Con accesso API**: Performance API dà le serie giornaliere → report automatizzabile. **Senza**: sezione Rendimento della UI (export UI). Chiamate e indicazioni della scheda si sommano a quelle del sito (vedi `analytics-ristorante`): nel report al cliente presenta il totale "cosa ti ha portato Google", non due silos.

**Novità (agosto 2026)**: GA4 ora si collega nativamente al Business Profile (Amministrazione → Collegamenti) e genera da solo una sezione Report con le metriche GBP su finestra rolling 6 mesi — dove il cliente ha già `analytics-mcp` attivo, collegalo lì invece di sommare a mano i due export (dettagli in `analytics-ristorante`).

### 5. Decisione automazione
- 1-2 sedi, poche recensioni → **manuale basta**, la richiesta API non vale l'attesa.
- Multi-sede o volumi alti di recensioni/post → **richiedi l'accesso API subito** (tempi di approvazione lunghi: falla partire al giorno 1 della presa in carico, lavora in UI nel frattempo).

## Regole RBR & trabocchetti
- ⚠️ **Confine con `seo-local-ristorante`**: keyword, pagine local, schema, multilingua, citazioni = di là. Qui solo l'operatività della scheda. Se stai facendo un piano SEO completo, parti da quella skill e usa questa per il capitolo GBP.
- ⚠️ **L'accesso API va richiesto e approvato** (quota zero di default, form + review di Google, giorni-settimane): non promettere automazioni al cliente prima dell'approvazione. API-first appena disponibile; l'automazione UI è il ponte, non la destinazione.
- ⚠️ **Cosa l'API non copre** (2026): creazione recensioni (giustamente), gestione foto/media, Q&A, menu con foto, messaggi, impostazioni cronologia chiamate → UI.
- ⚠️ **Mai comprare recensioni, mai review gating**: rischio sospensione della scheda — il danno supera qualsiasi beneficio.
- ⚠️ **Mai promettere al cliente la rimozione delle negative**: solo le recensioni davvero fuori tema (parla solo del parcheggio, locale sbagliato, mai entrato) hanno una possibilità concreta; quelle circostanziate, anche da nickname, restano — a quelle si risponde (vedi `references/segnalare-recensioni.md`).
- ⚠️ **Mai chiedere le stelle**: vale per messaggio, biglietto, bot e personale di sala (vedi §2).
- ⚠️ **Risposte recensioni sempre con revisione umana** prima della pubblicazione, anche quando il flusso è automatizzato via API.
- ⚠️ **Scheda su account sbagliato**: verifica proprietà/accesso su fpcgmedia@gmail.com PRIMA di promettere qualsiasi intervento.
- ⚠️ **Modifiche a nome/categoria/indirizzo possono rimettere la scheda in verifica**: 🟡 conferma col cliente prima di toccarle.
- ⚠️ **Mai credenziali/OAuth token in chiaro** nel repo condiviso.
- 👀 **Insight GBP ora separati per superficie** (segnalato agosto 2026): il pannello Insight distingue le impression tra pannello locale classico, card riassuntiva AI su Maps e AI Overview nei risultati organici. Utile nel report mensile (punto 4) per spiegare al cliente quanto traffico locale passa ormai da risposte AI invece che da click classici, invece di leggere solo il totale aggregato. Novità collegate: possibilità di aggiungere un contatto WhatsApp diretto sulla scheda e nuove Q&A generate da AI (con approvazione prima della pubblicazione, come le risposte alle recensioni).
- 👀 **Da monitorare, non ancora azione richiesta**: Google Maps introduce funzioni agentiche ("Ask Maps", annuncio 6/8/2026) — ordinazione cibo in chat via partner POS (Square/Toast, poi Uber Eats) e prenotazioni dirette dalla mappa. Rollout iniziale in altri paesi, Italia non ancora citata. Quando arriverà da noi, Maps risponderà e ordinerà direttamente dai dati di scheda/menu/POS: un motivo in più per tenerli sempre curati e coerenti.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Accesso alla scheda di ogni sede verificato su fpcgmedia@gmail.com (account giusto)
- [ ] Scheda ottimizzata campo per campo: categoria principale specifica, descrizione con la promessa, attributi, Q&A popolate, orari+festività, menu con prezzi, link prenotazione/delivery, 20-30 foto alla presa in carico
- [ ] Macchina recensioni attiva: richiesta sistematica (QR/GHL post-prenotazione, finestra 10-20 a 12h, lingua da prefisso, sblocco 60gg) con gancio tematico sul posizionamento, **link provato da un iPhone E da un Android veri fino al modulo stelle**, mai pulsante URL WhatsApp, risposta a tutte (anche vecchie) entro 48h con tono RBR, canale privato per le negative
- [ ] Biglietto al tavolo in sala, QR letto dal PDF finale e provato su iPhone senza app Google e su Android, fino al modulo stelle
- [ ] Primo giro del flusso automatico verificato sui clienti veri (invio la mattina dopo, blocco 60 giorni visto in azione)
- [ ] Cliente avvisato dei limiti della scheda (niente categoria/attributo senza glutine, foto menù da caricare a mano)
- [ ] Calendario post attivo, 1/settimana per sede, immagini 1200×900, offerte con scadenza reale
- [ ] Report insight mensile impostato (Maps/Search, chiamate, indicazioni, click, recensioni, imbuto della richiesta recensioni, distribuzione per stella) integrato col report `analytics-ristorante`
- [ ] Decisione automazione presa: richiesta API inviata (se multi-sede/volumi) o flusso manuale documentato
