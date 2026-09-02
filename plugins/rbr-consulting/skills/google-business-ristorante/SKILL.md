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
Campo per campo, per ogni sede:
- **Categoria principale** = quella più specifica e cercata ("Pizzeria", non "Ristorante" se è una pizzeria) + secondarie reali (Ristorante, Pizza da asporto…). La categoria principale pesa più di ogni altro campo.
- **Attributi** veri e completi: senza glutine, vegano, asporto, domicilio, dehors, accessibile, prenotazione consigliata. Ogni attributo è un filtro di ricerca su Maps.
- **Orari** esatti + orari speciali per festività (una scheda "forse chiuso" perde la chiamata).
- **Menu**: caricato nella sezione dedicata con prezzi (non solo PDF sul sito), foto dei piatti principali. Via UI — la parte menu non è coperta in modo affidabile dall'API.
- **Link prenotazione** (Resmio/TheFork) e link ordini delivery: sono le CTA che convertono direttamente dalla scheda.
- **Foto**: minimo 3-5 nuove/mese (piatti, sala, dehors, team). Gestione media = UI, non API. Le schede con foto recenti battono quelle ferme.
- **NAP coerente** con sito e citazioni (vedi `seo-local-ristorante` punto 4 — non ripetere qui l'analisi, solo verificare).

### 2. Macchina delle recensioni
- **Come chiederle**: al momento giusto (fine pasto/consegna), con link diretto recensione (short URL della scheda) su QR al tavolo, scontrino, follow-up post-prenotazione via GHL (automazione: prenotazione onorata → SMS/email col link il giorno dopo). Chiedere a TUTTI, mai selezionare solo i clienti contenti (review gating = violazione policy).
- **Mai comprare recensioni, mai recensioni da staff/amici**: rischio sospensione scheda. Non negoziabile RBR.
- **Come rispondere (tono RBR)**: a tutte, entro 48h. Positive: ringraziamento personale + mirroring naturale delle keyword (il piatto, il quartiere — senza forzare la città in ogni risposta). Negative: mai difensivi, mai copia-incolla — scuse se dovute, versione dei fatti sobria, invito a canale privato (email dedicata low-rating, vedi `seo-local-ristorante`). La risposta la leggono i futuri clienti, non il recensore.
- **Con accesso API**: pull periodico delle nuove recensioni + bozze di risposta generate e approvate dal consulente prima dell'invio via API — mai risposte pubblicate senza revisione umana.

### 3. Post e offerte ricorrenti
- Cadenza **1 post/settimana per sede** (standard RBR — una scheda ferma è un segnale morto).
- Rotazione mensile tipo: novità/piatto del mese → evento (serata, menu degustazione) → offerta con scadenza (pranzo fisso, aperitivo) → dietro le quinte/team.
- Formato: foto vera del locale (no stock), 80-150 parole, una CTA (Prenota/Chiama/Scopri di più) col link prenotazione.
- **Con accesso API**: calendario post del mese preparato in anticipo e pubblicato via Local Posts API (anche ricorrenti). **Senza**: pubblicazione via UI con lo stesso calendario.
- Le offerte hanno scadenza reale — mai offerte eterne, sviliscono il percepito (coerente con `adv-ristorante`: niente sconti come gancio se il posizionamento è alto).

### 4. Monitoraggio insight (mensile)
Metriche GBP da portare al ristoratore, confronto mese precedente + stesso mese anno prima:
- Impression su **Maps vs Search** (dove ti vedono)
- **Chiamate** dalla scheda
- **Richieste indicazioni stradali** (proxy di clienti che entrano)
- **Click al sito** e **click prenotazione**
- Recensioni nuove + rating medio + tempo medio di risposta
- Query con cui la scheda viene trovata (brand vs "pizzeria vicino a me")

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
- ⚠️ **Risposte recensioni sempre con revisione umana** prima della pubblicazione, anche quando il flusso è automatizzato via API.
- ⚠️ **Scheda su account sbagliato**: verifica proprietà/accesso su fpcgmedia@gmail.com PRIMA di promettere qualsiasi intervento.
- ⚠️ **Modifiche a nome/categoria/indirizzo possono rimettere la scheda in verifica**: 🟡 conferma col cliente prima di toccarle.
- ⚠️ **Mai credenziali/OAuth token in chiaro** nel repo condiviso.
- 👀 **Insight GBP ora separati per superficie** (segnalato agosto 2026): il pannello Insight distingue le impression tra pannello locale classico, card riassuntiva AI su Maps e AI Overview nei risultati organici. Utile nel report mensile (punto 4) per spiegare al cliente quanto traffico locale passa ormai da risposte AI invece che da click classici, invece di leggere solo il totale aggregato. Novità collegate: possibilità di aggiungere un contatto WhatsApp diretto sulla scheda e nuove Q&A generate da AI (con approvazione prima della pubblicazione, come le risposte alle recensioni).
- 👀 **Da monitorare, non ancora azione richiesta**: Google Maps introduce funzioni agentiche ("Ask Maps", annuncio 6/8/2026) — ordinazione cibo in chat via partner POS (Square/Toast, poi Uber Eats) e prenotazioni dirette dalla mappa. Rollout iniziale in altri paesi, Italia non ancora citata. Quando arriverà da noi, Maps risponderà e ordinerà direttamente dai dati di scheda/menu/POS: un motivo in più per tenerli sempre curati e coerenti.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Accesso alla scheda di ogni sede verificato su fpcgmedia@gmail.com (account giusto)
- [ ] Scheda ottimizzata campo per campo: categoria principale specifica, attributi, orari+festività, menu con prezzi, link prenotazione/delivery, foto fresche
- [ ] Macchina recensioni attiva: richiesta sistematica (QR/GHL post-prenotazione), risposta a tutte entro 48h con tono RBR, canale privato per le negative
- [ ] Calendario post attivo, 1/settimana per sede, offerte con scadenza reale
- [ ] Report insight mensile impostato (Maps/Search, chiamate, indicazioni, click, recensioni) integrato col report `analytics-ristorante`
- [ ] Decisione automazione presa: richiesta API inviata (se multi-sede/volumi) o flusso manuale documentato
