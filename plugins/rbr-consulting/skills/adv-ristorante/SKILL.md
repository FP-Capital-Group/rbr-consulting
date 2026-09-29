---
name: adv-ristorante
description: Variante ristorazione RBR per impostare l'advertising a pagamento di un ristorante — Google Ads (keyword locali + set EN per turisti) + funnel Meta a 3 livelli (TOFU/MOFU/BOFU), con KPI nord = COSTO PER PRENOTAZIONE. Usala quando devi mettere online o rivedere le ads di un locale — "piano Google Ads e Meta per un ristorante", "advertising per la steakhouse", "campagna a pagamento per il locale", "quanto mi costa una prenotazione dalle ads", "funnel Meta per il ristorante", "keyword per i turisti". Orchestra i pacchetti skill generici cla-ads-* e aia-ads-* applicando i benchmark RBR (costo per prenotazione, stagionalità, turisti). Opera sugli account via i tool MCP mcp__google-ads__* e mcp__meta-ads__*.
---

# Advertising ristorante (Google + Meta, KPI = costo per prenotazione)

## Perché esiste
Le skill di ads generiche (`cla-ads-*`, `aia-ads-*`) sono ottime per audit, keyword, funnel, budget e copy — ma ragionano in CTR/CPC/ROAS e-commerce. Un ristorante è un'altra bestia: il risultato non è un click né un carrello, è **una prenotazione o un ordine reale**. Questa skill è la **variante ristorazione** che orchestra quelle skill generiche imponendo i benchmark RBR: KPI nord unico = **costo per prenotazione**, attenzione a **stagionalità** e **turisti**, tracciamento delle conversioni vere (Resmio/chiamate/delivery), letture sempre segmentate (locale vs turista, per creatività) — mai aggregate.

> 💡 **Nota — usa i pacchetti skill già pronti.** Per l'esecuzione di dettaglio NON reinventare: esistono già skill globali che coprono ogni fase e che questa skill orchestra:
> - **Audit account**: `cla-ads-audit`, `cla-ads-google`, `cla-ads-meta`, `aia-ads-audit`, `aia-ads-quick`
> - **Keyword Google**: `aia-ads-keywords`, `cla-ads-google`
> - **Funnel Meta**: `aia-ads-funnel`, `cla-ads-plan`
> - **Budget/ROI**: `aia-ads-budget`, `cla-ads-budget`, `cla-ads-math`
> - **Copy/creatività**: `aia-ads-copy`, `aia-ads-hooks`, `aia-ads-video`, `cla-ads-creative`, `cla-ads-create`
> - **Landing/tracciamento**: `cla-ads-landing`, `aia-ads-landing`, `cla-ads-attribution`
>
> Il compito di questa skill è **calarle sul ristorante**: sostituire i loro KPI di default col costo per prenotazione e aggiungere i vincoli RBR sotto.

## Quando usarla
- Devi impostare da zero l'adv a pagamento di un ristorante (Google + Meta).
- Devi rivedere/ottimizzare campagne ristorante già attive.
- Il cliente chiede "quanto mi costa una prenotazione" o vuole più coperti/ordini dalle ads.
- Locale con componente turistica (recensioni/pubblico in parte in inglese).

## Prerequisiti
- Account **Google Ads** del cliente accessibile via MCP (`mcp__google-ads__*`); id account e login-customer-id corretti.
- Account **Meta** del cliente accessibile via MCP (`mcp__meta-ads__*`); ad account nel rollout MCP (altrimenti fallback documentato).
- **Sistema di prenotazione** tracciabile: Resmio (o simile), numero per le chiamate, link delivery (Glovo/Deliveroo/Just Eat).
- Posizionamento e USP del locale, zona/raggio, sedi, eventuale stagionalità (es. località balneare).
- Credenziali/token SEMPRE dal `.env` o dai wrapper MCP — mai in chiaro nel file (repo condivisa col team).

## Procedura

### 0. Account Google Ads nuovo: uscire dal wizard senza creare una Smart Campaign
Un account appena creato parte nel flusso guidato "Crea la tua prima campagna" (3 step, l'ultimo è la fatturazione) e via API risponde `CUSTOMER_NOT_ENABLED`; ogni URL `/aw/campaigns` reindirizza a `/aw/signup/`. Per uscirne senza creare una Smart Campaign: arrivare allo step "Scegli un obiettivo" e cliccare il link piccolo in fondo "Non puoi ancora lanciare una campagna? Configura solo un account" → porta alla conferma impostazioni (paese/fuso/valuta, **irreversibili**) e poi alla fatturazione.
- ⚠️ Il wizard può precompilare i dati con quelli di un **altro cliente già presente nel login** (visto su Red Mike: profilo attività, sito e descrizione erano di un altro locale) — controllare e correggere sempre sito, nome attività, descrizione e categorie.
- ⚠️ Nello step "Collega gli account" sono **prespuntati** il Profilo attività Google e il canale YouTube personale del consulente — deselezionarli se non sono del cliente.
- ⚠️ Nello step pagamento il "Profilo pagamenti" proposto può essere quello di **un'altra società** già nel login — se si conferma, la spesa del cliente viene fatturata a quella società. Usare sempre "Cambia" e verificare l'intestatario.
- L'account resta inaccessibile finché la fatturazione non è completata.

### 1. Audit e posizionamento
Parti da `cla-ads-audit`/`aia-ads-audit` sugli account esistenti. Poi fissa il posizionamento RBR: USP reale (es. senza glutine, carne premium, forno a legna), zona, raggio, sedi, stagionalità. Se il percepito è alto (fine dining), **evita gli sconti** come gancio: usa ganci esperienziali. Individua i **competitor** locali (conquesting) e la quota di **pubblico turistico** (guarda la lingua delle recensioni).

### 2. Google Ads — keyword locali + set EN turisti
Usa `aia-ads-keywords`/`cla-ads-google` per costruire la struttura, poi applica i vincoli RBR:
- **Ad group per intento** (steakhouse / ristorante di carne / brace / bistecca-fiorentina / iper-local / occasioni…). Non un solo gruppo generico.
- **Keyword oro iper-local**: es. `ristorante Via <strada>` in match esatta — CPC basso, conversione altissima.
- **Campagna EN turisti SEPARATA**, targeting per **presenza fisica** in città (non interesse) — es. "best steak in <città>".
- **Conquesting**: il nome del competitor può essere keyword, **MAI nel testo dell'annuncio** (policy marchi Google).
- **Negativi** su misura: ricette, lavoro/curriculum, corsi, gratis, franchising, ingrosso, supermercato. NON mettere negativo un termine che è anche il brand (es. "macelleria" se il locale è anche macelleria).
- **Raggio**: parti stretto (8-10 km, solo presenza fisica), allarga solo coi dati.
- Setup via `mcp__google-ads__*` (crea campagna/ad group/keyword/RSA/sitelink; imposta geo e lingua).

### 3. Meta — funnel a 3 livelli (TOFU/MOFU/BOFU)
Usa `aia-ads-funnel` per l'ossatura, poi cala i vincoli RBR:
- **TOFU (freddo)**: video sizzle / rituale del locale, Advantage+ broad locale + un braccio freddo turisti EN/ES. La creatività è ~70-80% del risultato: 4-6 asset nuovi/mese, Reel 9:16.
- **MOFU (tiepido)**: viewers ≥50% del video, engager Pagina/IG. Attiva a regime, non al giorno 1 (le audience partono vuote).
- **BOFU (caldo)**: retargeting Pixel + engager + **Lookalike 1-3% dalla lista clienti CRM (GHL)** — vantaggio ingiusto: Lead Ads → GHL → follow-up automatico.
- **Sequenza di lancio**: Mese 1 = solo freddo + LAL da GHL; retargeting/tiepido dal Mese 2 quando i pubblici hanno volume.
- **Ripartizione base indicativa**: ~30% freddo locale, ~10% freddo turisti, ~20% tiepido, ~40% caldo+LAL (adatta al budget e alla fase).
- Setup via `mcp__meta-ads__*` (campaign/adset/ad, custom audience, pixel). Nota RBR: il targeting "persone in visita" è deprecato via API → proxy turisti = **geo centro + lingue non-IT**.

### 4. Tracciamento conversioni (il pezzo che rende reale il KPI)
Senza questo, il "costo per prenotazione" non esiste. Le conversioni vere per un ristorante:
- **Prenotazione onorata** (Resmio) come conversione primaria — metodo corretto (contributo di Luciano Purpi, 2026-09-03): le pagine/link si marcano con `?utm=<landing>-<canale>` (Resmio tiene nel campo invisibile `booking_request_parameters` SOLO le chiavi esattamente `gclid` e `utm`: `utm_source`/`utm_content` ecc. vengono buttati) e l'iframe ha `referrerpolicy="no-referrer-when-downgrade"`; poi si caricano come **conversioni offline** (`mcp__google-ads__upload_google_ads_click_conversions` col `gclid`) solo le prenotazioni **onorate** — escluse cancellate e no-show (17-20%). Setup tecnico → skill `sito-landing-ristorante`, Tracciamento.
  - ❌ **Correzione: il blur-trick sul widget NON è una conversione primaria.** Conta il primo clic dentro l'iframe, non la prenotazione: su Barresi 42 "conversioni" in 14 giorni contro 39 prenotazioni TOTALI dal sito, e "Massimizza le conversioni" ottimizzava su tocchi. Dove è già installato → solo micro-conversione secondaria.
  - Il GTM nativo di Resmio (`gtm_conversion_tracking_enabled`) è **solo nel piano Ultimate** (+60 €/mese da Premium); l'add-on Marketing da 19,90 € NON lo contiene. La strada gclid/utm è gratis e dà un segnale migliore: non far comprare Ultimate per questo (listino e dettagli in `suite/memory/resmio.md`).
- **Chiamata** (estensione chiamata + tap-to-call dal sito, ≥30s).
- **Click ordine delivery** (Glovo/Deliveroo/Just Eat).
- Lato Meta: stessa logica — il canale entra via `?utm=` nel `booking_request_parameters`; un evento `Schedule` sul click del widget è solo segnale intermedio, mai la misura delle prenotazioni. Occhio al **cookie banner** che blocca il pixel senza consenso.
- Marca **primarie** solo le conversioni di prenotazione/chiamata/delivery; declassa a secondarie le vecchie azioni ridondanti dell'agenzia per non gonfiare i conteggi.

### 5. Budget, KPI e ottimizzazione
Usa `aia-ads-budget`/`cla-ads-math` per allocazione e break-even, ma valuta tutto sul **costo per prenotazione reale** (spesa ÷ prenotazioni ONORATE attribuite al canale in Resmio), NON su CPC/CTR. Come si costruisce il denominatore senza illudersi (contributo di Luciano Purpi, 2026-09-03 — numeri reali di un locale stagionale, agosto 2026, in `references/costo-per-prenotazione.md`):
- **Ogni attribuzione è un pavimento, mai una misura**: il `source` Resmio copriva il 38% delle prenotazioni, walk-in 44% delle righe, agente vocale tutto senza source. La provenienza si ricostruisce incrociando `source` + `comment`/`notes` + `booking_request_parameters`, e nel report si dichiara cosa resta non attribuito.
- **CPA sulle onorate**: no-show + cancellate = 17-20%, concentrati su TheFork e agente vocale. Caso reale: Google CPA 34,30 € (ROAS 1,51, margine +127 €) vs Meta CPA 212 € (ROAS 0,24, −1.587 €).
- **Prima di scalare, il costo MARGINALE, non il medio**: budget Google +56% → prenotazioni Google +15% mentre il locale cresceva +45% da solo; CPA marginale ~74 € contro 24,65 € medio.
- **La pubblicità segue la domanda**: in piena stagione spesa e prenotazioni di canale non correlano (r ≈ 0), i canali non pagati correlano col totale. È un indizio, non una prova causale — ma cambia la conversazione sul budget.
- Definisci **kill-switch** concreti col cliente (es. CPL sopra soglia dopo X€ spesi per adset → stop/cambio creatività).
- **Scala solo con costo/tavolo reale sotto soglia**, misurato dalle prenotazioni, non dalle metriche di piattaforma.
- Report **termini di ricerca** ogni 3-4 giorni le prime 2 settimane (Google).
- **Stagionalità**: nei locali stagionali (balneari) concentra budget nella finestra alta; fuori stagione riduci o spegni — ma verifica col marginale che in alta stagione la spesa aggiuntiva porti davvero tavoli in più.
- **Un URL diverso per annuncio**: se tutte le inserzioni puntano allo stesso URL l'attribuzione per annuncio si azzera (6 annunci su 8 in un mese). Obiettivo Meta "Traffico" compra clic, non tavoli (23.017 clic a 0,08 € → 15 prenotazioni).

## Regole RBR & trabocchetti
- ⚠️ **KPI nord = costo per prenotazione**, mai CPC/CTR/ROAS come stella polare. Se non è misurabile, prima sistema il tracciamento (punto 4), poi spendi.
- ⚠️ **Letture sempre segmentate** (locale vs turista, per creatività) — mai il dato aggregato, nasconde i vincitori.
- ⚠️ **Turisti = presenza fisica + lingua**, non "interesse per la città". Il travel_in Meta è deprecato via API.
- ⚠️ **Competitor solo come keyword**, mai nel copy annuncio (marchi).
- ⚠️ **Non mettere negativo il brand** (es. "macelleria" per un ristorante che è anche macelleria).
- ⚠️ **Cookie banner/Consent Mode** possono azzerare pixel/tag senza consenso → verificalo, spiega i volumi bassi con questo.
- ⚠️ **Doppio conteggio GA4 / container GTM multipli**: non smontare tag alla cieca (rischio rompere le conversioni Ads live) — diagnostica prima, tocca con l'ok del cliente.
- ⚠️ **Meta ha disattivato in silenzio alcuni breakdown di reporting** (dal 6/8/2026): per gli ad account senza opt-in esplicito, i breakdown *device*, *fascia oraria* e *frequency* spariscono senza errore — l'API risponde 200 con valori vuoti/zero. Prima di leggere un report segmentato per device/ora come "zero risultati", verifica l'opt-in sull'account: altrimenti rischi di prendere decisioni su un dato mancante scambiato per reale.
- 💡 **Opportunità (19/8/2026) — Meta Instant Forms ora prenota direttamente**: gli Instant Form (Lead Ads) supportano un link di scheduling incollato dall'inserzionista — al submit del form si apre un widget calendario in thank-you page con i dati del lead precompilati. **GHL è supportato al lancio** (insieme a Calendly), HubSpot da inizio agosto, disponibilità globale prevista per ottobre. Per un ristorante è un salto: BOFU caldo (punto 3) può saltare il passaggio "Lead Ads → GHL → follow-up manuale/automatico" e prenotare il tavolo/l'evento nello stesso funnel pubblicitario. Da valutare sui prossimi setup Meta con calendario GHL attivo — verificare disponibilità sull'ad account prima di promettere il collegamento.
- 👀 **Da monitorare — Meta Business Agent** (annuncio agosto 2026): agente IA di Meta che risponde ai clienti, consiglia prodotti dal catalogo, qualifica lead e chiude vendite su WhatsApp/Messenger/Instagram. Sovrapposizione potenziale con le automazioni GHL/il consulente umano nella gestione dei messaggi — nessuna azione operativa ora, ma da tenere d'occhio quando/se disponibile sugli ad account dei clienti RBR (rischio: il cliente lo attiva senza avvisare e si sovrappone ai flussi GHL).
- 👀 **GoHighLevel Ask AI genera bozze di campagne Meta** (segnalato agosto 2026): utile per velocizzare il setup iniziale, ma resta bozza — verificare SEMPRE targeting, budget e creatività prima di dare l'approvazione esplicita richiesta per la pubblicazione. Non sostituisce i vincoli RBR di questa skill (KPI costo per prenotazione, segmentazione locale/turista).
- 👀 **Meta One (lanciato 15/9/2026)**: nuovo abbonamento business a 4 livelli (Essential $14.99, Advanced $49.99, Expert $149, Max $499/mese) che impacchetta strumenti AI (Meta Business Agent), scheduling contenuti IG/FB, analytics estese (storico 90gg, confronto con 10 competitor), gestione team senza condividere password. Nessuna azione ora: da valutare caso per caso solo se un cliente chiede "vale la pena abbonarsi" — non sostituisce gli ads (KPI resta costo per prenotazione), è un layer di gestione organica/AI in più.
- 👀 **Meta ha reso il WhatsApp Click-to-Chat un obiettivo di campagna a sé** (agosto 2026), con sequenze automatiche post-click (messaggio di benvenuto, domande di qualificazione) gestite da Ads Manager senza passare dalla WhatsApp Business API. Da valutare per i ristoranti che oggi gestiscono prenotazioni/richieste via WhatsApp: possibile step BOFU aggiuntivo nel funnel (punto 3), da testare prima di proporlo come standard.
- ⚠️ **Verifica SEMPRE il pixel/tag dopo il deploy con l'ID reale, non col nome della funzione**: un grep generico su `fbq(` o `connect.facebook.net` risulta positivo anche quando è rimasto il placeholder letterale `fbq('init','PIXEL_ID')` — visto su redmike.it, live da 2 mesi senza raccogliere un solo evento. Verifica corretta: `curl -sL https://sito.it | grep -c '<pixel_id_reale>'` (deve dare >0) e `grep -c PIXEL_ID` (deve dare 0); in browser `window.fbq.getState().pixels` deve elencare l'ID giusto e deve esistere il cookie `_fbp`. Stessa logica per GA4 (`G-XXXX`) e Google Ads (`AW-XXXX`). Dettagli tecnici (script idempotente di iniezione, tracciamento Resmio via `utm`/`gclid` in `booking_request_parameters`) → skill `sito-landing-ristorante`, sezione Tracciamento.
- ⚠️ **Meta Ads Manager: quattro trappole di lettura** (contributo di Luciano Purpi, 2026-09-10):
  1. **Account "introvabile"**: la ricerca del selettore guarda il NOME dell'account, che spesso non contiene il cliente (caso reale: account "AC 1" di un business del cliente, condiviso nel portfolio di un'altra società del gruppo). Entra in OGNI portfolio e leggi la riga "Owned by <business>" sotto ogni account; controlla anche Gmail (`from:facebookmail.com`) per inviti mai accettati. Solo dopo dichiari che l'accesso manca. `business.facebook.com/latest/settings/ad_accounts` chiede la 2FA con passkey: la fa solo il titolare, noi ci fermiamo lì.
  2. **Tabella campagne su canvas**: `get_page_text` non restituisce le righe finché non ha finito di caricare → aspetta 15-20 s e rileggi.
  3. **Periodi lunghi piantano la pagina** (20+ campagne): interroga UN MESE ALLA VOLTA (`&date=2026-04-01_2026-04-30`) e somma. Meglio ancora i tool `mcp__meta-ads__*` quando l'account è nel rollout.
  4. **Copertura parziale**: prima di calcolare CPL/ROAS confronta i lead attribuiti dall'account coi lead realmente entrati nei moduli nel mese — se ne spiega solo una frazione (caso reale 382 su 1.422) c'è un secondo account che non vedi e il costo calcolato è falso.
- ⚠️ **Mai token/API in chiaro** nel repo condiviso: opera via `mcp__google-ads__*`, `mcp__meta-ads__*`, credenziali dal `.env`.
- 🟡 Go-live e scale di budget = conferma col cliente; kill-switch concordati per iscritto.
- ✅ Emoji di sistema RBR nei report: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Audit account fatto (via `cla-ads-*`/`aia-ads-*`) e posizionamento/stagionalità/turisti definiti
- [ ] Google Ads: ad group per intento + keyword iper-local + set EN turisti separato + negativi (brand escluso) + geo/raggio impostati via MCP
- [ ] Meta: funnel TOFU/MOFU/BOFU con Advantage+ broad + braccio turisti + LAL da GHL, sequenza di lancio definita
- [ ] Tracciamento conversioni attivo e verificato: prenotazione (Resmio) + chiamata + delivery lato Google; Pixel + `?utm=` per canale lato Meta (evento sul widget solo secondario)
- [ ] Solo le conversioni di prenotazione/chiamata/delivery sono primarie (vecchie azioni declassate)
- [ ] **Costo per prenotazione reale** misurabile sulle ONORATE (gclid/utm in `booking_request_parameters` + conversioni offline), quota non attribuita dichiarata, costo marginale controllato prima di ogni scale; kill-switch + soglia di scale concordati col cliente
- [ ] Nessun blur-trick/click widget come conversione primaria di bidding; un URL distinto per annuncio
- [ ] Letture impostate segmentate (locale vs turista, per creatività), non aggregate
