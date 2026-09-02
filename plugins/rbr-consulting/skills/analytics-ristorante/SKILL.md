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
- Se il widget prenotazione è in **iframe esterno** (Resmio): il click sul widget si traccia, la prenotazione confermata no → per il dato vero incrocia col gestionale prenotazioni (vedi `adv-ristorante` punto 4).
- **Collega Search Console alla property GA4** (Amministrazione → Collegamenti Search Console): sblocca query e landing organiche dentro GA4.
- **Novità (agosto 2026) — collegamento nativo GA4 ↔ Google Business Profile**: da Amministrazione, "Collegamenti" ora include anche il GBP (oltre a Search Console/Google Ads). Una volta collegato, GA4 aggiunge da solo una sezione Report dedicata con le metriche della scheda (chiamate, indicazioni, click sito) su finestra rolling 6 mesi. Va collegato dove il cliente ha già la scheda su `google-business-ristorante`: riduce il lavoro di sommare a mano i dati GBP + sito nel report mensile (vedi punto 4 di quella skill).
- Verifica **no doppio tracciamento** (doppio GA4/container GTM multipli — trabocchetto noto, vedi `seo-local-ristorante` punto 6): diagnostica prima, non smontare tag alla cieca.

### 2. Lettura mensile via MCP
Con `analytics-mcp` → `run_report` (mese vs mese precedente e vs stesso mese anno prima — i ristoranti sono stagionali, il confronto giusto è YoY):
- Sessioni e utenti per **canale** (organic, paid, direct, social, referral).
- **Key event per canale**: quale canale porta prenotazioni/chiamate, non solo traffico.
- **Pagine di ingresso**: la home domina? Le pagine local per sede (se esistono) portano traffico?
- Quota **mobile** (tipicamente 75-85% per un ristorante: se il sito mobile è lento, è lì il problema).
- Da Search Console API: click/impression/posizione, **brand vs non-brand** (regex sul nome del locale), query local chiave, CTR delle pagine sede.
- **Novità (agosto 2026) — report "Ricerca generativa" in Search Console**: nuova sezione dedicata a impression/pagine/paesi/dispositivi per le superfici AI Overviews e AI Mode, separata dalla ricerca classica. Utile per spiegare al cliente un eventuale calo di click nonostante impression stabili (il traffico viene "assorbito" dalla risposta AI prima del click) — da aggiungere alla lettura mensile quando il volume è significativo.

### 3. Diagnosi tipiche
- **Traffico che non prenota**: guarda i key event, non le sessioni. Cause tipiche in ordine: CTA prenota non visibile above-the-fold su mobile → widget prenotazione rotto/lento → traffico informativo (query definizioni, vedi trabocchetto `seo-local-ristorante`) → cookie banner che blocca i tag (i dati ci sono ma non li vedi).
- **Calo organico**: prima separa brand/non-brand in GSC. Calo brand = problema di notorietà/stagione (non SEO); calo non-brand = confronta le posizioni delle query local chiave, cerca pagine cadute, verifica cannibalizzazioni o modifiche recenti al sito.
- **"Le ads non funzionano"**: verifica che i key event GA4 e le conversioni Google Ads misurino la stessa cosa; spesso la campagna converte ma il tracciamento è rotto o duplicato.

### 4. Mini-report mensile standard RBR
Le 8-10 metriche da portare al ristoratore, sempre con confronto mese precedente e YoY:
1. Utenti totali sito
2. Sessioni organiche (e % non-brand da GSC)
3. Click GSC totali + posizione media query local #1
4. **Prenotazioni dal sito** (click_prenotazione — e prenotazioni reali dal gestionale se disponibile)
5. **Chiamate dal sito** (click_telefono)
6. Richieste indicazioni stradali (click_indicazioni)
7. Aperture menu (click_menu)
8. **Canale che porta più prenotazioni** (non più traffico)
9. Tasso di conversione sito → azione (key event / sessioni)
10. Se attive ads: **costo per prenotazione** (dato che arriva da `adv-ristorante` — qui si verifica solo che il tracciamento regga)

Una pagina, linguaggio da ristoratore ("questo mese il sito ha generato X prenotazioni e Y chiamate"), niente gergo GA4.

## Regole RBR & trabocchetti
- ⚠️ **API-first**: dati sempre via `analytics-mcp` / Search Console API. UI GA4/GSC  solo per quello che l'API non copre: creazione property, configurazione key event, collegamento GSC, DebugView.
- ⚠️ **L'MCP GA4 è read-only**: la configurazione (property, eventi, key event) si fa in GTM e nell'admin GA4, non via MCP. Ed è *experimental*: se un tool fallisce, fallback su Data API diretta o UI.
- ⚠️ **Sessioni e utenti non sono il KPI**: il KPI di un ristorante è quante azioni reali (prenotazioni, chiamate, indicazioni) il sito genera. Un report di solo traffico è un report inutile.
- ⚠️ **Confronto YoY, non solo mese su mese**: agosto vs luglio per un locale di città è sempre un disastro apparente. La stagionalità si legge sull'anno.
- ⚠️ **Cookie banner/Consent Mode**: possono tagliare il 30-50% dei dati. Prima di diagnosticare un "calo", verifica che non sia cambiato il consenso.
- ⚠️ **Widget iframe (Resmio) non traccia la conversione finale**: il numero vero di prenotazioni vive nel gestionale, GA4 misura l'intento. Non spacciare i click per prenotazioni confermate.
- ⚠️ **Doppio GA4/GTM**: diagnostica, non smontare alla cieca (rischio rompere conversioni Ads live).
- ⚠️ **Mai credenziali JSON in chiaro** nel repo condiviso.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Accesso GA4 + GSC ottenuto su fpcgmedia@gmail.com; `analytics-mcp` funzionante sulla property del cliente
- [ ] I 5 eventi ristorante installati via GTM, marcati key event, verificati in DebugView/realtime
- [ ] Search Console collegata alla property GA4; brand vs non-brand separabile
- [ ] Nessun doppio tracciamento; consenso/cookie banner verificato
- [ ] Mini-report mensile impostato (10 metriche, confronti MoM + YoY) e leggibile da un ristoratore
- [ ] Se ci sono ads attive: coerenza verificata tra key event GA4 e conversioni delle campagne
