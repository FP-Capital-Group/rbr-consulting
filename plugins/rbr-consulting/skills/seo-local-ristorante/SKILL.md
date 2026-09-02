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
- Accesso **WordPress** del sito (REST API + Application Password) per audit ed editing.
- **SEO plugin** installato (tipicamente Yoast) per meta/title/schema.
- Proprietà/accesso al **Google Business Profile** di ogni sede (leva local #1). Spesso è su un account Google diverso da quello "principale" del cliente → verificalo subito.
- Accesso a **Google Search Console** (export ultimi 3 mesi, filtro Italia) per l'analisi keyword; senza è a stima.
- Dati sede ufficiali: indirizzo, telefono, orari per ogni sede (NAP), USP reale del locale.
- Credenziali/token sempre dal `.env` o wrapper — mai in chiaro nel file (repo condivisa col team).

## Procedura

### 1. Inquadra il business: LOCAL SEO B2C
Prima di tutto decidi l'angolo: keyword **local + intento** ("pizzeria <città> <quartiere>", "pizza asporto <zona>", "migliore <cucina> a <città>") + eventuale **USP** ad alto intento e bassa concorrenza (es. "pizzeria senza glutine <città>" se il locale è certificato). NON inseguire ricerche informative/definizioni ("storia della pizza", "cosa contiene il lattosio"): tante impression, CTR ~0, zero clienti.

### 2. Audit (Yoast + struttura pagine + GSC)
- **Search Console**: export 3 mesi. Metriche = Impression (domanda), Posizione media (1-3 top, 1-10 pag.1, 11+ ≈ 0 traffico), CTR. Separa **brand** da **non-brand**: la crescita sta nel non-brand.
- **Quick win**: volume alto + posizione 5-12 → una spinta e sei in pagina 1. Massima priorità. (Es. tipico: una keyword local con buona posizione ma CTR bassissimo = title/snippet da rifare, win enorme.)
- **On-page**: 1 solo H1 con keyword, title keyword nei primi 60 char, meta description orientata al clic, contenuto per intento, FAQ con schema.
- **Struttura pagine**: censisci cosa esiste. Nei siti ristorante spesso ci sono solo landing coupon/fidelity/funnel e **mancano le pagine local per sede** — è il gap principale. Le pagine funnel interne → valuta **noindex**.
- **Cannibalizzazione**: più URL (home + PDF menù + thank-you page) che competono sulla stessa query → 1 pagina canonica + link interni con anchor keyword; noindex ai template che rubano ranking.

### 3. Crea le pagine local SEO mancanti (una per sede/città)
Per ogni sede: URL parlante (`/pizzeria-<città>-<quartiere>/`), H1 con keyword local, contenuto ricco per intento (quartiere, USP, orari, come arrivare, FAQ), **schema JSON-LD `Restaurant`** con NAP reale, geo, orari, telefono, `aggregateRating` (da Google Places), `potentialAction` Reserve/Order. Collega le sedi con un **hub store-locator** (`/le-nostre-pizzerie/`, `ItemList`) hub-and-spoke, e cross-linka le pagine tra loro con anchor keyword.

⚠️ **Limite Yoast**: `_yoast_wpseo_title`/`metadesc` spesso NON scrivibili via REST. Sblocca con uno snippet che li registra come scrivibili, oppure impostali dal pannello WP admin.

### 4. Google Business Profile (leva local #1)
- Verifica **su quale account** vivono le schede (spesso non è l'account principale del cliente) — è il primo blocco tipico.
- Configura per sede: categoria principale (es. Pizzeria) + secondarie, attributi reali (senza glutine, vegano, asporto, domicilio), NAP coerente, prenotazioni, foto.
- **Post GBP**: cadenza 1/settimana per sede (schede spesso ferme da anni = segnale morto).
- **Recensioni**: rispondi mirroring keyword naturali (senza forzare la città), gestione low-rating verso email dedicata.
- NAP consistente tra sito, GBP e citazioni esterne (TheFork, TripAdvisor, portali di categoria).

### 5. Multilingua per i turisti (GTranslate)
Se il locale ha pubblico turistico, attiva **GTranslate** (piano free = traduzione client-side JS, no URL dedicati/SEO): utile per l'esperienza EN dei turisti in loco, non per rankare in inglese (per quello servono pagine EN dedicate — vedi punto 3, es. `/gluten-free-pizza-<città>/`).
- **Selettore SEMPRE bottom-left** (standard RBR su tutti i siti).
- Trabocchetti noti: altri widget in basso a sx (Cookiebot, chat) coprono il selettore → nascondili via Custom CSS di GTranslate; il campo Custom CSS **escapa `>`** → usa solo selettori discendenti, mai child combinator; i **widget iframe esterni** (es. Resmio) NON vengono tradotti (limite noto); su WP Engine/Aruba svuota la cache dopo le modifiche.

### 6. Tecnico e monitoraggio
- Verifica **canonicalizzazione** (http/non-www → https/www) e **redirect 301 mirati** da eventuali domini vecchi (un redirect tutto-sulla-home = soft 404, perdita autorità).
- Controlla **doppio conteggio GA4 / container GTM multipli**: diagnostica, non smontare alla cieca (rischio rompere conversioni Ads).
- Core Web Vitals / velocità: interventi a rischio layout (minify/defer, lazy load) SOLO supervisionati.
- Imposta uno snapshot KPI ricorrente: clic tot, **non-brand** (leva crescita), posizione+CTR delle keyword local chiave, clic del dominio vecchio (target → 0).

## Regole RBR & trabocchetti
- ⚠️ **TRABOCCHETTO #1 — le keyword di un altro business NON valgono per un ristorante.** Caso reale: un pacchetto SEO di **velocissimo.app** (software gestionale per ristoranti) portava keyword commerciali tipo "software pizzeria", "gestionale ristorante". **NON valgono per un locale come Mister Pizza.** Di quel materiale si riusa il **METODO** (GSC, prioritizzazione, cannibalizzazione, on-page), **mai** le keyword: un ristorante è **LOCAL SEO B2C** (pizzeria + città + quartiere, GBP, recensioni, schema Restaurant), non e-commerce/SaaS. Se vedi keyword "software/gestionale/prezzo licenza" in un piano ristorante, è il segnale che qualcuno ha copiato dal business sbagliato.
- ⚠️ **Non inseguire ricerche informative/definizioni**: impression alte, CTR ~0, zero clienti.
- ⚠️ **GBP spesso su un account Google diverso**: verifica la proprietà prima di promettere ottimizzazioni.
- ⚠️ **Domini vecchi ancora indicizzati** = migration leak: pretendono 301 mirati pagina→pagina.
- ⚠️ **GTranslate free ≠ SEO multilingua**: traduce per l'utente, non crea URL indicizzabili → per rankare EN servono pagine EN vere.
- ⚠️ **Yoast meta via REST bloccati** e **Custom CSS che escapa `>`**: limiti tecnici noti, gestiscili come al punto 3/5.
- ⚠️ **Interventi su velocità/tracciamento = supervisionati**: rischio rompere layout o conversioni live.
- ⚠️ **Mai token/credenziali in chiaro** nel repo condiviso: dal `.env` o wrapper.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Angolo confermato come **local B2C** (nessuna keyword software/e-commerce nel piano)
- [ ] Audit fatto: GSC brand vs non-brand, quick win identificati, cannibalizzazione mappata, pagine funnel valutate per noindex
- [ ] Pagine local per sede create/pubblicate con H1+title+meta local e schema `Restaurant` (NAP reale) + hub store-locator + cross-link
- [ ] Google Business Profile verificato (proprietà + account giusto), categorie/attributi/NAP a posto, cadenza post attiva
- [ ] Multilingua GTranslate attivo (selettore bottom-left) se ci sono turisti; pagine EN dedicate dove serve rankare in inglese
- [ ] Tecnico verificato: canonicalizzazione, 301 mirati da domini vecchi, no doppio GA4; snapshot KPI non-brand impostato
