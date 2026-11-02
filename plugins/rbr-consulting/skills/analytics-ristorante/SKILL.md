---
name: analytics-ristorante
description: >-
  Misurazione e lettura dati del sito di un ristorante — setup GA4 con gli eventi che contano
  per un locale (click prenotazione, tap telefono, indicazioni stradali, form, menu/PDF),
  collegamento Search Console, lettura mensile (brand vs non-brand, pagine di ingresso,
  conversioni per canale) e diagnosi tipiche (traffico che non prenota, calo organico).
  Usala quando devi misurare o interpretare i dati del sito di un locale — "installiamo
  GA4 sul sito del ristorante", "quante prenotazioni arrivano dal sito", "il traffico c'è
  ma non prenota nessuno", "report mensile analytics per il cliente", "è calato l'organico",
  "colleghiamo Search Console". Opera API-first: MCP ufficiale Google Analytics
  (`analytics-mcp`) + Search Console API; UI solo come fallback.
---

# Analytics ristorante (GA4 + Search Console)

## Perché esiste
Un ristorante non vende pageview: vende **prenotazioni, chiamate e persone che entrano dalla porta**. GA4 out-of-the-box misura tutto tranne questo. Questa skill fissa il setup di misurazione giusto per un locale (gli eventi che contano davvero), la lettura mensile standard che il consulente RBR porta al ristoratore, e le diagnosi tipiche — il tutto via MCP/API, senza vivere dentro l'interfaccia GA4.

## Quando usarla
- Setup misurazione da zero sul sito di un ristorante (GA4 + Search Console).
- Report mensile per il cliente: cosa è successo, da dove arrivano le prenotazioni.
- Diagnosi: "tanto traffico ma zero prenotazioni", "l'organico è calato", "le ads girano ma non vedo risultati".
- Verificare che le conversioni usate dalle ads (vedi `adv-ristorante`) siano tracciate correttamente.

## Prerequisiti
- Accesso alla **property GA4** e alla proprietà **Search Console** del sito con l'identità Google del team: **fpcgmedia@gmail.com** (almeno Viewer su GA4, utente su GSC). Se la property vive su un altro account del cliente → primo step: farsi aggiungere.
- ⚠️ Se `analytics.google.com` apre la schermata "crea il tuo primo account", non vuol dire che GA4 non esiste: la proprietà può stare sotto un altro profilo Google dello stesso browser. Prima di concluderlo prova `?authuser=1`, `?authuser=2` e così via, oppure il selettore account — vale anche per Google Ads e Search Console. Creare per errore una proprietà nuova porta dritto al doppio tracciamento (vedi sotto). *(contributo di Andrea Chirivì, 2026-10-12)*
- **MCP ufficiale Google Analytics** (`analytics-mcp`, team Google, da maggio 2026 — repo `googleanalytics/google-analytics-mcp`, doc su developers.google.com/analytics/devguides/MCP). Read-only (Data API + Admin API GA4), stato *experimental*. Installazione:
  ```bash
  claude mcp add analytics-mcp --scope user \
    -e "GOOGLE_APPLICATION_CREDENTIALS=<path credenziali JSON>" \
    -e "GOOGLE_PROJECT_ID=<progetto GCP>" \
    -- pipx run analytics-mcp
  ```
  Serve un progetto Google Cloud con **Analytics Data API + Admin API abilitate** e credenziali ADC (OAuth desktop o service account, scope `analytics.readonly`). Tool esposti: `run_report`, `run_realtime_report`, `run_funnel_report`, `get_account_summaries`, `get_property_details`, `get_custom_dimensions_and_metrics`.
- **Search Console**: NON esiste MCP ufficiale Google (ad agosto 2026) → usa la **Search Console API** diretta (service account JSON aggiunto come utente alla proprietà GSC) o un MCP community (es. `mcp-server-gsc`). In mancanza, export CSV dalla UI.
- Accesso **GTM/WordPress** del sito per installare tag ed eventi (il setup eventi si fa lì, non in GA4).
- Credenziali/JSON sempre fuori dal repo condiviso (`.env` o path locale) — mai in chiaro.

## Procedura

### 1. Setup misurazione (una volta per cliente)
- Property GA4 dedicata al sito (una per brand, non per sede), fuso Europa/Roma, valuta EUR, retention dati 14 mesi.
- **Eventi ristorante** (via GTM, click/submit listener) — questi e solo questi diventano **key event**:
  - `click_prenotazione` — click sul widget/CTA prenota (Resmio, TheFork, form)
  - `click_telefono` — tap su link `tel:` (quasi solo mobile: è la conversione principale)
  - `click_indicazioni` — click su "Indicazioni"/link Google Maps
  - `invio_form` — submit form contatti/eventi/gruppi
  - `click_menu` — apertura menu/PDF (micro-conversione, indica intento)
- ⚠️ **Modulo ospitato su un altro dominio (GHL)**: se il CTA o il popup porta a un form su `api.leadconnectorhq.com/widget/form/...`, la persona esce dal sito — GA4 non vede l'invio (`form_submit` non arriva mai), il gclid si perde e la conversione Ads segna "nessuna conversione recente". Non è rotta, è cieca. Due strade, entrambe verificate sul campo:
  - **(a) Form in iframe** (es. dentro un popup) + ascoltatore dei `postMessage` in arrivo da `leadconnectorhq.com`/`msgsndr.com`: l'invio riuscito è il messaggio `["set-sticky-contacts","_ud",{...}]` (il gemello `embedded_iframe_undefined` va ignorato). Su quel messaggio manda l'evento GA4 e il `Lead` di Meta, una volta per visita. Scrivi il filtro sui messaggi osservati con uno spione durante un invio vero, mai su un'ipotesi — un filtro su `submit|success|thank` non scatta mai. Collaudata dal vivo: `fbq('track','Lead')` e l'evento GA4 partiti davvero. È la strada da preferire quando il form resta in un popup.
  - **(b) Form come pagina esterna**: usa una pagina di ringraziamento sul dominio del locale (On Submit → Redirect to URL nel form GHL) e il key event diventa il `page_view` di quella pagina. Il costruttore di eventi senza codice di GA4 accetta come trigger solo `page_view` e `form_submit`, niente clic in uscita. La pagina va in noindex. Nota operativa: nel builder moduli di GHL le schede Edit/Settings non rispondono ai clic automatici, il redirect lo imposta il consulente a mano.
  *(contributo di Andrea Chirivì, 2026-10-12)*
- Se il widget prenotazione è in **iframe esterno** (Resmio): il click sul widget si traccia, la prenotazione confermata no → per il dato vero incrocia col gestionale prenotazioni (vedi `adv-ristorante` punto 4).
- **Canale di provenienza dentro Resmio** (contributo di Luciano Purpi, 2026-09-03): il campo giusto è `booking_request_parameters` (invisibile all'ospite, non va in mail, a differenza di `comment`). Resmio tiene SOLO le chiavi esattamente `gclid` o `utm` — `utm_source`, `utm_medium`, `utm_campaign`, `utm_content` vengono **scartati** (su Barresi le pagine marcate `utm_content` per giorni hanno passato solo il gclid di Google, niente da Meta, mail o telefono). Marcatore corretto: `?utm=<landing>-<canale>`, che GA4 ignora (non sporca l'attribuzione organica). Le UTM standard per GA4 restano sui link, ma non aspettarti di ritrovarle in Resmio. Serve anche `referrerpolicy="no-referrer-when-downgrade"` sull'iframe del widget (setup → `sito-landing-ristorante`, Tracciamento).
- **Collega Search Console alla property GA4** (Amministrazione → Collegamenti Search Console): sblocca query e landing organiche dentro GA4.
- **Novità (agosto 2026) — collegamento nativo GA4 ↔ Google Business Profile**: da Amministrazione, "Collegamenti" ora include anche il GBP (oltre a Search Console/Google Ads). Una volta collegato, GA4 aggiunge da solo una sezione Report dedicata con le metriche della scheda (chiamate, indicazioni, click sito) su finestra rolling 6 mesi. Va collegato dove il cliente ha già la scheda su `google-business-ristorante`: riduce il lavoro di sommare a mano i dati GBP + sito nel report mensile (vedi punto 4 di quella skill).
- Verifica **no doppio tracciamento** (doppio GA4/container GTM multipli — trabocchetto noto, vedi `seo-local-ristorante` punto 6): diagnostica prima, non smontare tag alla cieca.

### 2. Lettura mensile via MCP
Con `analytics-mcp` → `run_report` (mese vs mese precedente e vs stesso mese anno prima — i ristoranti sono stagionali, il confronto giusto è YoY):
- Sessioni e utenti per **canale** (organic, paid, direct, social, referral).
- **Key event per canale**: `run_report` con dimensione `sessionSourceMedium`, filtro su `eventName` = evento di prenotazione, due metriche `totalUsers` ed `eventCount`. Nel report conta le PERSONE (`totalUsers`), non gli eventi: la stessa persona fa scattare l'evento più volte — caso reale, rapporto eventi/utenti 1,7, cioè contare gli eventi gonfiava il dato del 70%. Fallback da interfaccia: Rapporti → Coinvolgimento → Eventi → evento → dimensione secondaria "Sorgente/mezzo sessione". Ogni volta che il dato si cita, aggiungi in una riga le quattro cautele: periodo corto e numeri piccoli; prenotazioni avviate, non persone entrate; chi rifiuta i cookie non è misurato (valori minimi); telefono, Maps e Facebook restano fuori.
- **Pagine di ingresso**: la home domina? Le pagine local per sede (se esistono) portano traffico?
- **Da quale pagina parte chi va a prenotare**: nel report standard di GA4 "referrer pagina" non è selezionabile come dimensione secondaria. Serve un'Esplorazione forma libera (dimensione "Referrer pagina", filtro sulla pagina o sull'evento di prenotazione) oppure `run_report` con dimensione `pageReferrer`, filtrata sul `pagePath` di prenotazione. Se i pulsanti hanno già la sorgente parlante (`source=sito-<pagina>`), lo stesso dato si legge anche nel gestionale prenotazioni e serve da controllo incrociato.
- Quota **mobile** (tipicamente 75-85% per un ristorante: se il sito mobile è lento, è lì il problema).
- Da Search Console API: click/impression/posizione, **brand vs non-brand** (regex sul nome del locale), query local chiave, CTR delle pagine sede.
- **Novità (agosto 2026) — report "Ricerca generativa" in Search Console**: nuova sezione dedicata a impression/pagine/paesi/dispositivi per le superfici AI Overviews e AI Mode, separata dalla ricerca classica. Utile per spiegare al cliente un eventuale calo di click nonostante impression stabili (il traffico viene "assorbito" dalla risposta AI prima del click) — da aggiungere alla lettura mensile quando il volume è significativo.

### 3. Diagnosi tipiche
- **Traffico che non prenota**: guarda i key event, non le sessioni. Cause tipiche in ordine: CTA prenota non visibile above-the-fold su mobile → widget prenotazione rotto/lento → traffico informativo (query definizioni, vedi trabocchetto `seo-local-ristorante`) → cookie banner che blocca i tag (i dati ci sono ma non li vedi).
- **Calo organico**: prima separa brand/non-brand in GSC. Calo non-brand = confronta le posizioni delle query local chiave, cerca pagine cadute, verifica cannibalizzazioni o modifiche recenti al sito. ⚠️ **Calo brand**: prima di concludere "notorietà/stagione", quando la posizione è ferma, le impressioni sono stabili o in crescita e il CTR scende, escludi due cause correggibili. (1) Snippet peggiorato: dopo un cambio di home o la sostituzione di una pagina, titolo e descrizione SEO possono sparire e Google se li scrive da solo — a ogni cambio della pagina iniziale ricontrolla titolo e descrizione, e fai partire la finestra di confronto dopo la correzione. (2) Il pagato si prende i clic di marca: confronta sugli stessi giorni i clic organici sulle query del nome (GSC, regex sul nome) con i clic della campagna/gruppo Marca e della PMax (che intercetta anche il nome, report termini di ricerca). Finché non è provata resta un'ipotesi: la prova è una pausa della sola campagna/gruppo Marca per 3-4 giorni (solo col via libera del titolare), poi si guarda se i clic organici sul nome risalgono di pari misura e se le prenotazioni per canale restano uguali. Attenzione: la Marca di solito ha il miglior costo per conversione dell'account, quindi non è "inefficiente" — la domanda è solo quante di quelle persone sarebbero arrivate gratis. *(metodo di diagnosi confermato; un test di pausa reale non è mai stato eseguito — va usato per diagnosticare, non come conclusione già provata)*
- **"Le ads non funzionano"**: prima di leggere, difendere o importare in Ads un key event o una conversione, apri la sua definizione — in GA4: Amministrazione → Eventi → eventi creati o modificati (le condizioni); in Google Ads: Obiettivi → Conversioni (origine e azione). Scrivi in una riga cosa conta davvero: il nome lo dà chi l'ha creata (o Google in automatico) e da solo non prova niente. Caso reale: una conversione chiamata "Invio modulo per i lead" era in realtà un `page_view` sul path della pagina prenotazione, non un invio di modulo — era l'unica conversione negli obiettivi, quindi tutte le campagne ottimizzavano su una visualizzazione di pagina. ⚠️ Se più conversioni contano lo stesso gesto (es. "invio modulo" e "prenotazione avviata" entrambe principali), c'è doppio conteggio: vale la regola "una sola conversione guida le offerte" — verificalo sempre, perché una volta introdotto può restare attivo a lungo senza che nessuno se ne accorga. Verifica infine che i key event GA4 e le conversioni Google Ads misurino la stessa cosa; spesso la campagna converte ma il tracciamento è rotto o duplicato. *(contributo di Andrea Chirivì, 2026-10-12)*

### 4. Mini-report mensile standard RBR
Le 8-10 metriche da portare al ristoratore, sempre con confronto mese precedente e YoY:
1. Utenti totali sito
2. Sessioni organiche (e % non-brand da GSC)
3. Click GSC totali + posizione media query local #1
4. **Prenotazioni dal sito** (click_prenotazione — e prenotazioni reali dal gestionale per canale `utm`/`gclid`, onorate vs cancellate/no-show, se disponibile)
5. **Chiamate dal sito** (click_telefono)
6. Richieste indicazioni stradali (click_indicazioni)
7. Aperture menu (click_menu)
8. **Canale che porta più persone verso la prenotazione** (non più traffico, contate come persone e non come eventi)
9. Tasso di conversione sito → azione (key event / sessioni)
10. Se attive ads: **costo per prenotazione** (dato che arriva da `adv-ristorante` — qui si verifica solo che il tracciamento regga)

Una pagina, linguaggio da ristoratore ("questo mese il sito ha generato X prenotazioni e Y chiamate"), niente gergo GA4.

## Regole RBR & trabocchetti
- ⚠️ **API-first**: dati sempre via `analytics-mcp` / Search Console API. UI GA4/GSC  solo per quello che l'API non copre: creazione property, configurazione key event, collegamento GSC, DebugView.
- ⚠️ **L'MCP GA4 è read-only**: la configurazione (property, eventi, key event) si fa in GTM e nell'admin GA4, non via MCP. Ed è *experimental*: se un tool fallisce, fallback su Data API diretta o UI.
- ⚠️ **Sessioni e utenti non sono il KPI**: il KPI di un ristorante è quante azioni reali (prenotazioni, chiamate, indicazioni) il sito genera. Un report di solo traffico è un report inutile.
- ⚠️ **Confronto YoY, non solo mese su mese**: agosto vs luglio per un locale di città è sempre un disastro apparente. La stagionalità si legge sull'anno.
- ⚠️ **Cookie banner/Consent Mode**: possono tagliare il 30-50% dei dati. Prima di diagnosticare un "calo", verifica che non sia cambiato il consenso.
- ⚠️ **Widget iframe (Resmio) non traccia la conversione finale**: il numero vero di prenotazioni vive nel gestionale, GA4 misura l'intento. Non spacciare i click per prenotazioni confermate (caso reale: il blur-trick contava 42 "conversioni" contro 39 prenotazioni totali dal sito). Il canale nel gestionale si legge da `booking_request_parameters` (`gclid`/`utm`), e ogni attribuzione resta un pavimento: dichiarare la quota non attribuita (vedi `adv-ristorante`, `references/costo-per-prenotazione.md`).
- ⚠️ **Doppio GA4/GTM**: diagnostica, non smontare alla cieca (rischio rompere conversioni Ads live).
- ⚠️ **Mai credenziali JSON in chiaro** nel repo condiviso.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Accesso GA4 + GSC ottenuto su fpcgmedia@gmail.com; `analytics-mcp` funzionante sulla property del cliente
- [ ] I 5 eventi ristorante installati via GTM, marcati key event, verificati in DebugView/realtime
- [ ] Search Console collegata alla property GA4; brand vs non-brand separabile
- [ ] Nessun doppio tracciamento; consenso/cookie banner verificato
- [ ] Mini-report mensile impostato (10 metriche, confronti MoM + YoY) e leggibile da un ristoratore
- [ ] Se ci sono ads attive: regola di ogni conversione primaria letta e scritta nella memoria cliente; coerenza verificata tra key event GA4 e conversioni delle campagne (nessun doppio conteggio)
