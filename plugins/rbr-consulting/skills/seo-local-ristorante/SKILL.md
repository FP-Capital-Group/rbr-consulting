---
name: seo-local-ristorante
description: >-
  Playbook SEO local B2C RBR per il sito di un ristorante — audit (Yoast, struttura pagine), creazione pagine local SEO per sede/città, ottimizzazione Google Business Profile, multilingua per i turisti (widget GTranslate). Usala quando lavori sulla visibilità organica di un locale — "SEO local per il sito del ristorante", "perché il locale non si trova su Google", "creiamo le pagine pizzeria + città", "sistemiamo la scheda Google del ristorante", "il sito è solo in italiano, servono i turisti", "audit SEO del ristorante". Un ristorante è LOCAL SEO B2C: pagine per sede, GBP, recensioni, schema Restaurant — NON keyword software/e-commerce.
---

# SEO local ristorante (B2C: sede, GBP, multilingua)

## Perché esiste
Un ristorante vive di ricerche **local con intento** ("pizzeria Firenze Duomo", "steakhouse vicino a me", "best pizza in florence") e della sua **scheda Google Business Profile**, non di keyword commerciali generiche. Il grosso degli errori nasce dal riusare metodi/keyword pensati per altri business (software, e-commerce): non funzionano e fanno perdere tempo. Questa skill fissa il playbook giusto per un locale B2C e i suoi trabocchetti reali.

## Quando usarla
- Il sito di un ristorante non si trova per le ricerche local giuste.
- Devi fare un audit SEO di un locale e definire le priorità.
- Mancano le pagine per sede/città o la scheda Google è ferma/mal configurata.
- Il locale ha pubblico turistico e il sito è solo in italiano.

## Prerequisiti
- ⚠️ **Siti fatti con `sito-wordpress-ristorante`**: multilingua con TranslatePress e traduzioni scritte (niente GTranslate/traduzione automatica), stelle e recensioni statiche (mai Places dal browser), plugin SEO facoltativo; accesso con l'utente admin del consulente. Le indicazioni GTranslate/Yoast qui sotto valgono per i siti esistenti che li hanno già.
- Accesso **WordPress** del sito (REST API + Application Password) per audit ed editing.
- **SEO plugin**: Yoast o All in One SEO (AIOSEO). Verifica quale c'è prima di toccare
  meta, sitemap o noindex: filtri, API e limiti sono diversi (vedi §3 "Limiti AIOSEO").
  *(contributo di Andrea Chirivì, 2026-10-12)*
- Proprietà/accesso al **Google Business Profile** di ogni sede (leva local #1). Spesso è su un account Google diverso da quello "principale" del cliente → verificalo subito.
- Accesso a **Google Search Console** (export ultimi 3 mesi, filtro Italia) per l'analisi keyword; senza è a stima.
- Dati sede ufficiali: indirizzo, telefono, orari per ogni sede (NAP), USP reale del locale.
- Credenziali/token sempre dal `.env` o wrapper — mai in chiaro nel file (repo condivisa col team).

## Procedura

### 1. Inquadra il business: LOCAL SEO B2C
Prima di tutto decidi l'angolo: keyword **local + intento** ("pizzeria <città> <quartiere>", "pizza asporto <zona>", "migliore <cucina> a <città>") + eventuale **USP** ad alto intento e bassa concorrenza (es. "pizzeria senza glutine <città>" se il locale è certificato). NON inseguire ricerche informative/definizioni ("storia della pizza", "cosa contiene il lattosio"): tante impression, CTR ~0, zero clienti.

**SEO e posizionamento sono due linguaggi separati** *(contributo di Andrea Chirivì,
2026-10-12)*: la SEO va dove la gente cerca (misura la domanda sul raggio vero — Keyword
Planner sui comuni a 15-20 km, non la provincia intera), il posizionamento resta quello
del locale (vedi `strategia-marketing-rbr`). SEO col linguaggio del posizionamento =
invisibili; posizionamento col linguaggio della SEO = un locale qualunque. La geografia
sta in title, meta description, pagina contatti e footer — nel corpo ripete solo ciò che
il titolo ha già detto. Mai una formula geografica fissa ripetuta su tutte le pagine:
alterna varianti naturali ("Taranto e provincia", "in provincia di Taranto", "Taranto").
Mai una frazione o un paese minore come geografia dichiarata del locale: se il locale sta
vicino a una città più cercata, testi e titoli parlano della città dove la gente cerca,
ma lo schema Restaurant tiene sempre l'`addressLocality` vera, coerente col GBP.

### 2. Audit (Yoast + struttura pagine + GSC)
- **Search Console**: export 3 mesi. Metriche = Impression (domanda), Posizione media (1-3 top, 1-10 pag.1, 11+ ≈ 0 traffico), CTR. Separa **brand** da **non-brand**: la crescita sta nel non-brand.
- **Quick win**: volume alto + posizione 5-12 → una spinta e sei in pagina 1. Massima priorità. (Es. tipico: una keyword local con buona posizione ma CTR bassissimo = title/snippet da rifare, win enorme.)
- **On-page**: 1 solo H1 con keyword, title keyword nei primi 60 char, meta description orientata al clic, contenuto per intento, FAQ con schema. *(contributo di Andrea Chirivì,
  2026-10-12)*: conta nel testo la parola per cui la pagina deve essere trovata (una
  pagina che non nomina mai il suo prodotto chiave non viene trovata). Un H1 solo, con
  fatti veri presi dal menu; i paragrafi di riempimento si riscrivono con prezzi, tagli,
  ingredienti, orari. Gerarchia: titoli di sezione H2, sottotitoli H3, mai salti da H1 a
  H4; attenzione al doppio H1 (un contenuto con un suo H1 sotto il titolo del tema, o
  nascosto via CSS — Google lo legge comunque; uno slider che clona la slide duplica
  l'H1) — controlla sempre sull'HTML renderizzato, non sul sorgente. Il suffisso
  automatico " - Nome locale" può spingere il title oltre i 60 caratteri: misura la
  lunghezza col suffisso incluso. Title e meta description passano dalla no-list e dalle
  regole di testo del cliente come ogni altro testo, e si ricontrollano ogni volta che
  cambia la homepage o si sostituisce una pagina (non li ereditano automaticamente).
- **Struttura pagine**: censisci cosa esiste. Nei siti ristorante spesso ci sono solo landing coupon/fidelity/funnel e **mancano le pagine local per sede** — è il gap principale. Le pagine funnel interne → valuta **noindex**. *(contributo di Andrea Chirivì,
  2026-10-12)*: audit sui **comuni vicini**, non solo sulla sede — per ogni comune del
  raggio vero somma la domanda su "<prodotto> <comune>" + "<comune> <prodotto>" e
  verifica se il sito lo nomina almeno una volta. Un comune con domanda e mai nominato è
  la prossima pagina local da fare (concorrenza bassa, miglior valore/fatica), prima
  delle pagine di prodotto generico.
- **Pagine sottili sullo stesso tema** (es. eventi diversi dello stesso tipo): accorpale
  in una pagina forte come SEZIONI intere (non riassunti), ognuna col suo bottone
  Prenota. Le vecchie pagine vanno in bozza con un 301 verso `/pagina/#sezione` — nel
  redirect l'ancora va DOPO la query, altrimenti l'indirizzo si rompe; serve
  `scroll-margin-top` (~130px) perché la barra fissa non copra l'ancora. Dopo
  l'accorpamento: zero link interni residui, voce di menu tolta, sitemap pulita.
  *(contributo di Andrea Chirivì, 2026-10-12)*
- **Cannibalizzazione**: più URL (home + PDF menù + thank-you page) che competono sulla stessa query → 1 pagina canonica + link interni con anchor keyword; noindex ai template che rubano ranking. **Menu: pagina HTML, non PDF** *(contributo di Andrea Chirivì,
  2026-10-12)* — Google non legge bene un PDF pesante del menu. Crea una pagina HTML con
  tutte le voci e i prezzi, fai puntare lì la voce di navigazione "Menu" e metti il
  vecchio PDF in 301. Lo schema JSON-LD `Menu` (sezioni e piatti con nome, descrizione,
  prezzo) si genera dalla stessa pagina, col suo `@id` uguale all'URL di `hasMenu` nello
  schema Restaurant. Controlla a vista anche in dark mode. Se serve un "menu da
  mandare" in PDF, generalo dalla pagina menu (fonte unica): un PDF vecchio rilinkato a
  parte rimette in giro prezzi e frasi superate.

### 3. Crea le pagine local SEO mancanti (una per sede/città)
Per ogni sede: URL parlante (`/pizzeria-<città>-<quartiere>/`), H1 con keyword local, contenuto ricco per intento (quartiere, USP, orari, come arrivare, FAQ), **schema JSON-LD `Restaurant`** con NAP reale, geo, orari, telefono, `aggregateRating` (da Google Places), `potentialAction` Reserve/Order. Collega le sedi con un **hub store-locator** (`/le-nostre-pizzerie/`, `ItemList`) hub-and-spoke, e cross-linka le pagine tra loro con anchor keyword.

**Pagine "vicino a &lt;comune&gt;" per i comuni del raggio** (anche con una sede sola)
*(contributo di Andrea Chirivì, 2026-10-12)*: una pagina o articolo per ogni comune del
raggio con domanda misurata (vedi §2), mai cloni per tutti i comuni della provincia
(pagine fotocopia col solo nome del paese cambiato = doorway, penalizzate da Google).
Slug tipo `/pizzeria-vicino-<comune>/`, fatti veri (distanza, minuti in auto, come
arrivare, parcheggio, cosa si mangia, orari, Prenota con sorgente propria). Non fingere
mai una sede in quel comune: schema Restaurant e NAP restano quelli veri (vedi §1).
Subito dopo, indicizzazione manuale in Search Console (§6).

⚠️ **Limite Yoast**: `_yoast_wpseo_title`/`metadesc` spesso NON scrivibili via REST. Sblocca con uno snippet che li registra come scrivibili, oppure impostali dal pannello WP admin.

**Limiti AIOSEO** *(contributo di Andrea Chirivì, 2026-10-12)*:
- **Titolo e descrizione**: `POST /wp-json/aioseo/v1/post` vuole sia `id` sia `postId`
  (col solo `postId` risponde "Post ID is missing"). La chiamata SOVRASCRIVE: se mandi
  solo la description, il title si azzera e torna quello automatico "Pagina - Sito".
  Passa sempre title e description insieme, con backup prima e rilettura dopo.
- **Opzioni**: `POST /aioseo/v1/options` risponde `success:true` ma non sempre salva —
  verifica sempre col pannello.
- **Sitemap**: le pagine tecniche si tolgono da AIOSEO → Sitemap → Impostazioni avanzate
  → "Escludi articoli/pagine" (molto più veloce del noindex pagina per pagina). Da
  codice valgono solo i filtri `aioseo_sitemap_indexes`/`aioseo_sitemap_posts`: quelli
  del core (`wp_sitemaps_*`) e quelli di Yoast non hanno effetto. Togli dalla sitemap
  anche le URL in 301 e i tipi tecnici (popup, form). Prima di stimare il lavoro, leggi
  il meta robots vero: spesso molte pagine tecniche sono già noindex.
- **Noindex**: i campi robots scritti via REST spesso non hanno effetto (noindex via API
  inaffidabile). Funziona un mu-plugin che scrive il meta noindex in `wp_head` a
  priorità 0 e l'header `X-Robots-Tag` in `template_redirect`. In alternativa, noindex
  dal pannello o pagina non linkata. Prima di caricare un mu-plugin, verifica la sintassi
  caricando il file con un nome casuale: un 200 vuoto significa sintassi buona (un errore
  in un mu-plugin manda giù il sito).
- **Cache**: su un sito in cache il PHP non gira per chi visita — svuota la cache prima
  di verificare qualunque modifica. Controlla l'header `wpo-cache-status` su un URL
  SENZA query string (un `?cb=` salta la cache e mostra una versione che i visitatori
  non ricevono).

### 4. Google Business Profile (leva local #1)
- Verifica **su quale account** vivono le schede (spesso non è l'account principale del cliente) — è il primo blocco tipico.
- Configura per sede: categoria principale (es. Pizzeria) + secondarie, attributi reali (vegano, asporto, domicilio), NAP coerente, prenotazioni, foto. Su Google **non esiste**
  l'attributo né la categoria "senza glutine" (vedi `google-business-ristorante`): la
  nicchia SG passa da descrizione, menu e recensioni, non dagli attributi GBP.
- **Post GBP**: cadenza 1/settimana per sede (schede spesso ferme da anni = segnale morto).
- **Recensioni**: rispondi mirroring keyword naturali (senza forzare la città), gestione low-rating verso email dedicata.
- NAP consistente tra sito, GBP e citazioni esterne (TheFork, TripAdvisor, portali di categoria).
- **Audit della presenza online** *(contributo di Andrea Chirivì, 2026-10-12)*: un'ora a
  cercare il locale come lo cercherebbe un cliente, su directory e social. Cerca:
  identità vecchia sulle directory (categoria o nome sbagliati su TheFork, Restaurant
  Guru, piattimenu, PagineGialle — si rivendicano e si correggono tutte), profili doppi
  (più pagine FB/IG, blog vecchi, telefoni morti — un profilo per canale), orari diversi
  da una piattaforma all'altra. Sulle directory coi **filtri dietetici** (TripAdvisor
  senza glutine, vegano, celiaco), verifica se il locale compare nel filtro della sua
  zona: farsi taggare è la mossa gratuita, e vale anche quando il locale non compare per
  niente nonostante una buona quota di clienti con quell'esigenza.

### 5. Multilingua per i turisti (GTranslate)
Se il locale ha pubblico turistico, attiva **GTranslate** (piano free = traduzione client-side JS, no URL dedicati/SEO): utile per l'esperienza EN dei turisti in loco, non per rankare in inglese (per quello servono pagine EN dedicate — vedi punto 3, es. `/gluten-free-pizza-<città>/`).
- **Selettore SEMPRE bottom-left** (standard RBR su tutti i siti).
- Trabocchetti noti: altri widget in basso a sx (Cookiebot, chat) coprono il selettore → nascondili via Custom CSS di GTranslate; il campo Custom CSS **escapa `>`** → usa solo selettori discendenti, mai child combinator; i **widget iframe esterni** (es. Resmio) NON vengono tradotti (limite noto); su WP Engine/Aruba svuota la cache dopo le modifiche.
- **Attiva il riconoscimento della lingua del browser** (di solito disponibile anche
  nella versione free): senza, il plugin parte sempre in italiano finché il visitatore
  non clicca la bandierina, e una campagna ads in inglese paga clic che atterrano in
  italiano. Le ads EN devono puntare a pagine EN vere, o almeno a un sito col
  rilevamento lingua attivo. *(contributo di Andrea Chirivì, 2026-10-12, origine
  Luciano Purpi)*

### 6. Tecnico e monitoraggio
- Verifica **canonicalizzazione** (http/non-www → https/www) e **redirect 301 mirati** da eventuali domini vecchi (un redirect tutto-sulla-home = soft 404, perdita autorità).
- **Vecchio dominio**: controlla sempre `robots.txt` (la riga Sitemap può puntare ancora
  al vecchio dominio), il footer di ogni pagina, menu stampati, biglietti, insegne e
  profili social. Un dominio scaduto può essere ripreso da siti di spam con cloaking
  geografico mentre resta citato ovunque. *(contributo di Andrea Chirivì, 2026-10-12,
  origine Luciano Purpi — caso Barresi)*
- Controlla **doppio conteggio GA4 / container GTM multipli**: diagnostica, non smontare alla cieca (rischio rompere conversioni Ads).
- Core Web Vitals / velocità: interventi a rischio layout (minify/defer, lazy load) SOLO supervisionati — metodo dettagliato in `references/velocita-wordpress.md`.
- **Search Console** *(contributo di Andrea Chirivì, 2026-10-12)*: se la proprietà a
  dominio (`sc-domain:`) non è accessibile dall'account del locale, lavora sulla
  URL-prefix (`https://dominio/`) e verifica chi la possiede — se è verificata
  sull'account personale di un consulente, aggiungi il proprietario giusto da
  Impostazioni → Utenti e autorizzazioni. **Dopo ogni modifica, reindicizza**: la
  Richiesta di indicizzazione (Controllo URL) indicizza in minuti, la sitemap in giorni.
  Quota ~10-12 URL/giorno per proprietà (finestra mobile di ~24h): segnala prima le
  pagine che valgono, il resto arriva dalla sitemap. Rinvia la sitemap specifica se
  Google l'aveva letta prima che i contenuti esistessero, e collega le pagine nuove dalle
  pagine più visitate (home, menu).
- **Dopo un intervento on-page, leggi i risultati per pagina**: le impressioni possono
  salire mentre CTR e posizione media peggiorano — è diluizione (il sito entra su tante
  ricerche nuove in 9ª-12ª posizione), non un calo. A questa scala l'organico non riempie
  il locale da solo: il valore sta nelle pagine già in posizione ~3. Il primo controllo
  sulle pagine esistenti si fa a ~10 giorni; un blog nuovo si giudica più avanti (tempi
  precisi da verificare pagina per pagina su Search Console). *(contributo di Andrea
  Chirivì, 2026-10-12)*
- Imposta uno snapshot KPI ricorrente: clic tot, **non-brand** (leva crescita), posizione+CTR delle keyword local chiave, clic del dominio vecchio (target → 0).

### 7. Blog del locale *(contributo di Andrea Chirivì, 2026-10-12)*
Serve a intercettare le ricerche con intento locale misurate sul raggio vero (§1), in
ordine di valore/fatica, partendo dalle query già in posizione 8-11. Gli articoli
enciclopedici portano impressioni ma non clic: servono solo come supporto ai link
interni, non come obiettivo primario. Credibilità senza nominare altri locali (nemmeno
un altro locale dello stesso titolare): diluisce il focus e fa pubblicità ai
concorrenti — la credibilità viene da contenuti utili e specifici e da voci vere già in
casa. Tecnica: immagine in evidenza su ogni articolo, title col suffisso entro 60
caratteri, link al blog dalle pagine forti (home, menu), indicizzazione manuale (§6).
Usa una sorgente per articolo (`?source=blog-<slug>`) invece di un unico `source=blog`,
per sapere quale articolo porta davvero al tavolo. *(Le chiusure consigliate per
intenzione del lettore — pronto a venire / vuole ordinare / curioso — e i tempi di
giudizio del blog sono ancora da verificare su più casi: non integrati qui.)*

## Regole RBR & trabocchetti
- ⚠️ **TRABOCCHETTO #1 — le keyword di un altro business NON valgono per un ristorante.** Caso reale: un pacchetto SEO di **velocissimo.app** (software gestionale per ristoranti) portava keyword commerciali tipo "software pizzeria", "gestionale ristorante". **NON valgono per un locale come Mister Pizza.** Di quel materiale si riusa il **METODO** (GSC, prioritizzazione, cannibalizzazione, on-page), **mai** le keyword: un ristorante è **LOCAL SEO B2C** (pizzeria + città + quartiere, GBP, recensioni, schema Restaurant), non e-commerce/SaaS. Se vedi keyword "software/gestionale/prezzo licenza" in un piano ristorante, è il segnale che qualcuno ha copiato dal business sbagliato.
- ⚠️ **Non inseguire ricerche informative/definizioni**: impression alte, CTR ~0, zero clienti.
- ⚠️ **GBP spesso su un account Google diverso**: verifica la proprietà prima di promettere ottimizzazioni.
- ⚠️ **Domini vecchi ancora indicizzati** = migration leak: pretendono 301 mirati pagina→pagina.
- ⚠️ **GTranslate free ≠ SEO multilingua**: traduce per l'utente, non crea URL indicizzabili → per rankare EN servono pagine EN vere.
- ⚠️ **Yoast meta via REST bloccati** e **Custom CSS che escapa `>`**: limiti tecnici noti, gestiscili come al punto 3/5.
- ⚠️ **Interventi su velocità/tracciamento = supervisionati**: rischio rompere layout o conversioni live.
- ⚠️ **Mai token/credenziali in chiaro** nel repo condiviso: dal `.env` o wrapper.
- ⚠️ **AIOSEO via REST sovrascrive** i campi non inviati; **noindex AIOSEO via REST è
  inaffidabile** (vedi §3). *(contributo di Andrea Chirivì, 2026-10-12)*
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Angolo confermato come **local B2C** (nessuna keyword software/e-commerce nel piano)
- [ ] Audit fatto: GSC brand vs non-brand, quick win identificati, cannibalizzazione mappata, pagine funnel valutate per noindex
- [ ] Pagine local per sede create/pubblicate con H1+title+meta local e schema `Restaurant` (NAP reale) + hub store-locator + cross-link
- [ ] Google Business Profile verificato (proprietà + account giusto), categorie/attributi/NAP a posto, cadenza post attiva
- [ ] Multilingua GTranslate attivo (selettore bottom-left) se ci sono turisti; pagine EN dedicate dove serve rankare in inglese
- [ ] Tecnico verificato: canonicalizzazione, 301 mirati da domini vecchi, no doppio GA4; snapshot KPI non-brand impostato
- [ ] Sitemap senza pagine tecniche né URL in 301 (vedi §3 "Limiti AIOSEO")
- [ ] Pagina menu HTML con schema Menu pubblicata; PDF del menu non linkato (o generato dalla pagina)
- [ ] Audit presenza online fatto: directory rivendicate, un profilo per canale, orari allineati
- [ ] robots.txt e footer senza riferimenti a eventuali domini vecchi del cliente
- [ ] Rilevamento lingua del browser attivo sul plugin di traduzione (se free)
- [ ] Comuni del raggio con domanda misurata nominati su almeno una pagina "vicino a &lt;comune&gt;"
