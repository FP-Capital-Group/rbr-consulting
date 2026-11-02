---
name: onboarding-cliente-ghl
description: Procedura completa RBR per onboardare un nuovo cliente ristoratore su GoHighLevel — crea sub-location, applica lo Snapshot "RBR Blueprint v1", installa l'app OAuth v2, registra l'istanza MCP ghl2-[cliente], personalizza Custom Values e subject email, collega Resmio/sito/cassa al router Make e testa end-to-end. Usala quando il consulente dice "nuovo cliente su GHL", "onboarding [nome cliente]", "crea il sub-account per [cliente]", "applica il blueprint", "attiva il CRM per il cliente", "il cliente parte con la piattaforma". Tempo target 30-60 min (escluso WhatsApp + DNS).
---

# Onboarding nuovo cliente RBR su GoHighLevel

## Regola trasversale
**Ogni operazione GHL passa dai tool MCP `ghl2-<cliente>`** (LeadConnector MCP v2 ufficiale): prima `search_operations`, poi `describe_operation`, poi `execute_operation`. Mai curl diretto sull'API GHL, salvo operazioni assenti dal catalogo. Doc: `suite/memory/ghl_mcp_server.md`.

⚠️ **Niente parte verso clienti veri senza anteprima e ok esplicito del consulente.** Vale per ogni azione che raggiunge clienti reali: invio di una mail o un WhatsApp (anche uno solo), invio di massa, pubblicazione/attivazione di un workflow che spedisce (Step 9), Deploy del bot su un canale, post e campagne. Prepara tutto fino all'ultimo passo e mostra l'anteprima vera: testo, destinatari col loro numero, orario e link. Si parte solo dopo l'ok esplicito del consulente su QUELLA anteprima — un ok dato sul piano o su una domanda generica non vale per l'invio. Quando puoi, il tasto lo preme il consulente. I collaudi si fanno solo su contatti di prova dedicati (Step 10, `@rbr-test.local`), mai sul numero del locale. *(contributo di Andrea Chirivì, 2026-10-12)*

⚠️ **Regole API**: (1) mai passare `tags` nell'upsert del contatto — sovrascrive quelli esistenti; fai l'upsert senza tag, poi aggiungi il tag con la chiamata additiva `POST /contacts/{id}/tags`. (2) Nelle azioni del bot e dei workflow configurate dal browser non digitare chiavi o token: usa un endpoint che non richiede chiave (identifica il contatto con `{{contact.id}}`, controlla lato server) oppure fai incollare la chiave al consulente.

⚠️ **Prima di dare a un integratore esterno una chiave API o l'accesso al CRM**: fai una "fotografia" del sistema da confrontare dopo (flussi con stato e iscritti, campi, tag, valori personalizzati, webhook, calendari) e copie di riserva in bozza dei workflow critici (conferma, promemoria 4 ore), col perché nel nome. Poi sorveglia, senza spiegazioni. La Private Integration del connettore MCP legge anche `/workflows`, `/tags`, `/customValues`, `/customFields`, `/calendars`: usala per quello che il catalogo MCP non ha, senza crearne un'altra. L'API NON dà i passaggi interni dei workflow né l'Audit Log: si leggono a mano in UI. La lettura del token dal browser è bloccata dal classificatore di sicurezza: non riprovare.

## Pre-requisiti
- Accesso GHL come agency admin/owner (agency FP Capital, ID `V2w1nZiR44RfRvJTf6Oj`) — se non lo hai, chiedi a Marco
- Snapshot **"RBR Blueprint v1"** pubblicato (lo è dal 2026-05-28)
- App OAuth v2 **"Restaurant Business Revolution - Claude"** pubblicata (Private, Sub-Account, Agency Only Install)
- Dati cliente raccolti: nome brand, indirizzo, telefono, email, sito, social, ordine minimo, colore brand, logo URL, i subject delle offerte mail
- ⚠️ Prima cosa in assoluto: **carta di credito del cliente attaccata al subaccount** (`Settings → Billing → Add Card`, ricarica auto $50 con soglia $10-20) — GHL funziona a consumo, senza carta non parte niente

## Step 1 — Crea sub-location (UI Agency, ~5 min)
1. Agency View → **Sub-Accounts → + Create Sub-Account**
2. Business Name = nome cliente reale · Address = indirizzo locale · **Time Zone `Europe/Amsterdam`** (GHL non offre Rome, stesso fuso) · Currency `EUR` · Industry Restaurant
3. **Apply Snapshot durante la creazione: `RBR Blueprint v1`** → Save → attendi 2-5 min
4. Verifica post-snapshot (via MCP o UI): **14 Custom Field + 13 Custom Values + 3 tag (`locale`, `turista`, `fidelity`) + 15 email template (13 catenaria: Locali Sett 1-9 + Turisti 1-4, più 2 trigger: Compleanno e Review Request — per questo gli oggetti da impostare allo Step 5 sono 13) + 2 workflow** (Smistamento Lead + Funnel RBR). Se manca qualcosa → skill `diagnosi-suite`, sezione "Snapshot non applicato".
5. ⚠️ Se la valuta del sub-account è rimasta vuota, i moduli nascono in USD e mostrano "$"; resta congelata nei moduli creati prima, anche mettendo EUR dopo (è solo estetico, il valore salvato è un numero puro — si aggira scrivendo € nell'etichetta). Su un sub-account nuovo, imposta **EUR prima di creare qualsiasi modulo**.

## Step 2 — Installa app OAuth v2 + sync token (~2 min)
L'app v2 è Private + Agency Only Install: NON è visibile nel marketplace del cliente, solo in quello agency (oppure via Install Link bookmark "🔧 Install RBR app", URL in `GHL_OAUTH_SA_INSTALL_LINK` in `mister-pizza/.env`).

1. Agency View → App Marketplace → cerca "Restaurant Business Revolution - Claude" → **Install** → Choose Location = sub-location del cliente → **Authorize**
2. Il browser mostra "site can't be reached" → **normale, ignora**
3. Sync token in Neon Postgres:
   ```bash
   cd ~/"Desktop/AI/RBR AI/mister-pizza"
   .venv/bin/python scripts/ghl_sync_all_locations.py
   ```
   Lo script usa il Company token → genera location_token per ogni sub-account installata → salva in Neon. (Il servizio Render zero-touch NON è deployato: il sync manuale è lo standard, deciso da Marco 2026-05-29.)

## Step 3 — Registra l'istanza MCP `ghl2-<cliente>` per tutto il team (~2 min)

Dal plugin v2.8.0 le istanze GHL sono dichiarate nel plugin e le chiavi stanno sul Mac di ogni
consulente. Per un cliente nuovo (lo fa Marco, o chi ha il repo `rbr-suite`):
1. `tools/rbr-chiavi.json` → in `mcp_servers` aggiungi `ghl2-<cliente>` copiando una voce
   esistente e cambiando `instance=<cliente>` nell'URL e `locationId` nell'header (il PIT agency
   è unico). Aggiorna lo stesso file su Drive ("RBR - Chiavi consulenti").
2. `plugins/rbr-consulting/.mcp.json` → aggiungi la riga
   `"ghl2-<cliente>": {"command": "python3", "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/mcp_bridge.py", "ghl2-<cliente>"]}`.
3. Bump patch in `plugin.json` + riga in `CHANGELOG.md` → `python3 tools/build_public_plugin.py --push`
   (o lasci fare alla routine del lunedì).
4. Ogni consulente: `/rbr-setup` (ri-scarica le chiavi) e chat nuova quando arriva l'aggiornamento.
Sul Mac di Marco l'istanza personale a scope utente (`claude mcp add -s user ghl2-<nome> -- ~/Desktop/AI/GoHighLevel-MCP/run-v2-instance.sh OAUTH <LOCATION_ID>`) resta facoltativa.

## Step 4 — Personalizza i 13 Custom Values (~5 min, via MCP)
I 13 Custom Values arrivano dallo snapshot con valori demo (RBR Demo). Sovrascrivili con i dati reali via `ghl2-<cliente>`: `search_operations` per "custom values" → `describe_operation` → `execute_operation`.

| Custom Value | Valore |
|---|---|
| `nome_brand` | Nome esatto cliente |
| `logo_url` | URL logo (CDN/WordPress cliente) |
| `colore_primario` | Hex brand (es. `#cd0017`) |
| `indirizzo` | Indirizzo completo |
| `telefono` | Numero locale |
| `email_locale` | Email del locale |
| `sito_url` / `instagram_url` / `facebook_url` | URL cliente |
| `whatsapp_url` | `https://wa.me/<numero>` |
| `landing_base_url` | Base URL per CTA mail |
| `ordine_minimo` | Spesa minima T&C (es. "30") |
| `footer_delivery_html` | HTML Glovo/Deliveroo o vuoto |

Una volta riempiti, tutte le 15 mail della catenaria si personalizzano da sole (usano `{{cv.*}}`).

## Step 5 — Subject delle 13 mail (~10 min, UI)
Le mail blueprint hanno subject `-` (placeholder). Il subject NON sta nel template: si setta nel nodo **Send Email** del workflow **Funnel RBR** (design GHL). Apri il workflow → per ogni Send Email node sostituisci `-` con il subject dell'offerta cliente (Locali Sett 1-9, Turisti 1-4). ⚠️ L'API GHL non scrive i workflow e l'editor canvas non è automatizzabile via browser → va fatto a mano in UI.

## Step 6 — Collega il cliente al router Make (~10 min)
1. **Riga nel Data Store `rbr_clients` (id 131658)**: key = `facility_id` Resmio (o `client_source`), campi `client_key`, `brand_key`, `location_id_ghl`, `webhook_smistamento_url` (URL inbound webhook del workflow Smistamento Lead — è NUOVO per ogni cliente dopo snapshot, si legge dal canvas), `webhook_qr_url` (se attivo), `brand_name`, `lang_default`, `active: true`. Puoi usare il form `https://marcocuccaro0309.github.io/rbr-forms/onboard-cliente.html` o la UI Make
2. **Resmio** (se il cliente ce l'ha): dashboard Resmio → Settings → Integrations → Add Webhook → URL = **hook universale `https://hook.eu1.make.com/8f726kbr6l5swrcf8mjf9q7hvr52go73`** (NON il webhook GHL diretto). ⚠️ Va configurato per OGNI facility. Solo UI: l'API key Resmio è read-only sui webhook
3. **Sito / cassa fidelity**: POST JSON al webhook universale col payload standard 8 campi — vedi skill `make-scenario-dod` e `suite/memory/rbr_payload_standard.md`
4. **Coupon** (se il cliente ha promo): record in `rbr_coupons` (id 131659), key `{brand_key}:{code}`, oppure `python3 shared/make_sync_coupons.py --client-key <key> --csv coupons.csv`. Gli stessi code vanno creati anche in iPratico (anagrafica promozioni)

## Step 7 — Dominio email + landing (~15 min + DNS 24-48h)
- **Sending domain**: `Settings → Email Services → Dedicated Domain` → il cliente aggiunge SPF + DKIM (`mailo._domainkey`, `mailo2._domainkey`) + Return-Path (`bounce.<dominio>`) sul suo DNS → verifica GHL in 24-48h. Senza, le mail partono ma con deliverability bassa
- **Custom landing domain**: `Settings → Domains` → CNAME `offerta.<dominio>` → `funnels.gohighlevel.com`, SSL automatico → aggiorna il Custom Value `landing_base_url`
- Lo Snapshot NON porta la config dominio: va rifatta per ogni cliente
- ⚠️ **SPF**: un solo record `v=spf1` con TUTTI i mittenti del dominio (max 10 lookup). Se la posta del locale è su Google Workspace, serve anche `include:_spf.google.com` oltre a `include:spf.leadconnectorhq.com` (GHL) e mailgun — la posta scritta a mano dalla casella del locale non supera l'SPF senza quel pezzo.
- ⚠️ **DMARC**: con il sottodominio dedicato (`mail.<dominio>`), un DMARC `adkim=s; aspf=s` fa fallire DMARC su TUTTE le email, anche su Gmail. Usa `v=DMARC1; p=none; adkim=r; aspf=r`.
- ⚠️ **CNAME della landing**: il target si legge in `Settings → Domains` del sub-account (NON è detto sia `funnels.gohighlevel.com` — può essere es. `sites.<provider>.cloud`). Su alcuni registrar (es. MisterDomain) il punto finale è obbligatorio (`sites.ludicrous.cloud.`), altrimenti il pannello accoda il dominio. GHL emette il certificato da sé: verifica con risposta 200 su `/` e sul path. I pannelli del registrar non si pilotano: prepara la riga, falla incollare al titolare, verifica sul nameserver autoritativo e su 8.8.8.8.
- Sui conti già partiti ricontrolla comunque dominio e certificati: su diversi account sono stati trovati mancanti o impostati male.
- ⚠️ **Mail finite in spam/fallite su Outlook, Hotmail, Live, MSN**: apri SEMPRE gli errori di consegna veri (statistiche dell'invio → Failed → messaggio) prima di fare ipotesi. Il codice `5.7.1 … part of their network is on our block list (S3140)` vuol dire che l'IP condiviso LC Email/Mailgun del sub-account è nella blocklist Microsoft — non dipende dal DNS e da soli non si risolve: va chiesto a GHL di spostare il conto su un altro IP o di darne uno dedicato (a pagamento). Intanto conta i contatti su domini Microsoft, tienili fuori dai primi invii e raggiungili su WhatsApp. Tieni questa causa separata da altre (caselle inesistenti/piene, indirizzi storpiati dal precompilato Meta). *(diagnosi confermata il 17/08/2026; da verificare se GHL ha poi spostato l'IP)*
- ⚠️ **Verifica il dominio di invio PRIMA di qualunque campagna**: senza dominio verificato GHL spedisce dal dominio condiviso `mg.msgsndr.net` con mittente `nome+gmail.com@mg.msgsndr.net`; con un from `@gmail.com` e SPF/DKIM non allineati Gmail manda in SPAM quasi sempre (verificato su Red Mike il 3/9). Meglio un sottodominio dedicato (`mail.<dominio-cliente>.it`) così non si tocca la posta esistente del cliente (contributo di Luciano Purpi, 04/09/2026)
- ⚠️ **Limiti invio email**: i sub-account nuovi partono a **1.000 mail/giorno** (warm-up automatico LC Email, sale in ~4 settimane se la reputazione è buona; tetto IP condiviso 15.000/giorno). L'override è per singolo account: Agency View → Sub-Accounts → cliente → Advanced Settings → Limits → Email → "Update Limit". Alzare il numero NON alza la reputazione: serve dominio dedicato + SPF/DKIM/DMARC + warm-up. Dettagli: `suite/memory/ghl_email_sending_limits.md`

## Step 7bis — Social e moduli Meta (~10 min)
*(contributo di Andrea Chirivì, 2026-10-12)*
1. Due collegamenti indipendenti: `Settings → Integrations` (lead ads, Messenger, recensioni) e `Marketing → Social Planner` (pubblicazione post e statistiche). Collegare il primo NON collega il secondo. Instagram si aggancia col login Facebook.
2. **Moduli istantanei**: `Settings → Integrations` → la pagina si apre vuota, clicca la scheda **All Integrations → Facebook → Manage**. Controlla che la pagina sia spuntata, la connessione Facebook+Instagram verde e il Sync Time su "New Leads" (solo i contatti nuovi, non lo storico). Mappatura campi in **Facebook Form Fields Mapping**. Esci con **Cancel**, mai con "Update and Continue". ⚠️ GHL non divide il "Nome completo" di Meta: finisce tutto in `firstName`, `lastName` resta vuoto.
3. ⚠️ **Token**: l'endpoint di verifica restituisce un campo `expire` con una data già passata anche quando il collegamento funziona, perché GHL rinnova i token da sé. Per dire se è scaduto davvero contano `isExpired` e una prova funzionale (stato Connected nel Social Planner, una chiamata alle statistiche che risponde), mai la sola data `expire`. Annota la scadenza dei token del Social Planner nella checklist del cliente.

## Step 8 — WhatsApp Business (opzionale, 3-7 giorni Meta)
`Settings → WhatsApp → Connect` → login Meta Business Manager del cliente → scansione QR dal WhatsApp Business sul telefono del locale. Costo: add-on WhatsApp GHL ~15 $/mese + costo Meta a messaggio template consegnato (dettagli e cifre aggiornate: skill `whatsapp-ghl-locale`, references/costi-limiti-misura.md), pagato dal cliente. Ricordagli di aprire l'app almeno 1 volta ogni 14 giorni o la connessione cade. Template `copy_conferma_prenotazione` (Utility) usa merge tag `{{contact.booking_when_text}}` ecc. → nel workflow serve un Create/Update Contact che valorizzi i custom field booking PRIMA del Send WhatsApp. Dettagli: `suite/quality/ghl_procedura_team_rbr.md` §6. Metodo completo del canale (template, consenso, STOP, invio di massa): skill `whatsapp-ghl-locale`.

**Opt-out nei template WhatsApp marketing senza toccare il testo**: aggiungi il pulsante nativo di risposta rapida "Marketing opt-out" → Meta compila da sé piè di pagina ed etichetta (stringhe fisse, tradotte in automatico). Soddisfa l'obbligo di opt-out senza rimettere in approvazione un testo già approvato (contributo di Luciano Purpi, 13/09/2026).

## Step 9 — Attiva i workflow (~1 min)
Nella sub-location: Workflows → **Smistamento Lead** → verifica stato **Published** (non draft) → toggle **Active ON**.
⚠️ **Funnel RBR va tenuto in bozza finché non è personalizzato per il cliente** (Step 4-5): attivarlo prima cancella i turisti e manda mail segnaposto.
⚠️ La pubblicazione di un workflow (o il salvataggio di un prompt, es. DeepAgent) può essere bloccata dai controlli di sicurezza dell'assistente. In quel caso prepara tutto, premi tu Pubblica/Salva, poi verifica che sia davvero in onda: **Published + Active**, agente attivato. *(contributo di Andrea Chirivì, 2026-10-12)*

## Step 10 — Test end-to-end (~10 min)
Con email test identificabili (`test-onboard-XXX@rbr-test.local` — cleanup facile):
1. POST `source=sito` al webhook → contatto creato + tag `locale`
2. POST `source=fidelity-cassa` + `birthday` → tag `locale`+`fidelity` + Date of Birth popolata
3. Prenotazione finta Resmio (o POST `action=BOOKING_CREATED`) → CF booking popolati + tag + eventuale WhatsApp/QR
4. Cleanup contatti test (search per `@rbr-test.local` via MCP, delete)
5. **Avvisi allo staff**: fai l'inventario dei nodi "Notifica interna". Se il sotto-account non ha Sistema telefonico, i nodi SMS risultano "Eseguito" ma non partono → sostituiscili con Notifica interna EMAIL all'utente titolare (dettagli `suite/memory/gohighlevel.md`)
6. ⚠️ **"Test your agent" (simulatore del bot) esegue le azioni come in produzione**: una prova può creare una prenotazione VERA su Resmio se il contatto di prova ha il numero del locale. Usa sempre un contatto di prova dedicato (mai il numero del locale), prepara prima il giro di annullo, e ripulisci alla fine. Per il collaudo della catena completa (bot → API/webhook → gestionale → conferma) vedi `references/conversation-ai.md`, sezione Collaudo. *(contributo di Andrea Chirivì + Luciano Purpi, 2026-10-12)*

Se i test passano → onboarding completato ✅. Aggiorna il calendario clienti in `suite/quality/ghl_procedura_team_rbr.md` §17.

## Modello base del conto e conti ereditati
Struttura target da montare uguale su ogni locale (tre strati Fondamenta → Servizio → Crescita,
nove flussi standard con nomi fissi, campi standard e tipi, famiglie di etichette, segnali da leggere
nella lista flussi, ordine di riordino di un conto ereditato): **`references/modello-base-locale.md`**.
Due regole da non dimenticare mai:
- **Tag per segmentare, campo per innescare**: i tag che arrivano dal ponte del gestionale si sommano
  → "tag aggiunto" scatta solo alla prima visita. Innesco ripetibile = Contact Changed sul campo di stato.
- **Etichetta = stato, campo = dato**: risposte a sondaggi, anno di nascita, fasce d'età vanno in campi.

## Conversation AI (bot di risposta)
Regole di campo in **`references/conversation-ai.md`**: Auto-Pilot non basta, serve il **Deploy**
per canale; il prompt salvato è già live. Il bot manda SOLO il link di prenotazione — eccetto su
WhatsApp, dove se ha l'azione di prenotazione **prenota in chat** (il link resta il ripiego dopo due
tentativi falliti); su IG/FB e ovunque non prenoti, mai offrire l'alternativa. Se il bot prenota,
preferisci un'azione **API Call diretta** verso una rotta del locale (più robusta del flusso con
"Informazioni di contatto" + attesa + webhook); serve comunque una rete di sicurezza lato server che
intercetti le prenotazioni promesse ma non registrate. *(contributo di Andrea Chirivì, 2026-10-12)*

## Cosa NON tocchi mai senza Marco
- Snapshot agency `RBR Blueprint v1` (lo modifica solo Marco)
- App OAuth v1/v2 · Rebilling/margini agency
- I 14 Custom Field standard (non rinominare/cancellare)
- Workflow base (Smistamento, Funnel, QR) — se devi modificarli, duplica e modifica la copia
- Time zone del subaccount già in produzione
- Sub-account **FP Capital Group** (`KAODAZKquYEJ0rGDANB0`): è dell'agency host, non toccare

## Riferimenti
- `suite/memory/procedura_onboarding_cliente_ghl.md` — step-by-step ufficiale Marco
- `suite/memory/ghl_blueprint_rbr.md` + `blueprint_monosede.md` — cosa contiene il blueprint
- `suite/memory/ghl_blueprint_v2_data_store.md` — Data Store Make e router
- `suite/memory/zero_touch_oauth_architecture.md` — architettura OAuth/Neon
- `suite/quality/ghl_procedura_team_rbr.md` — manuale completo consulente (checklist §15, sessione 1 ora §16)
- Problemi durante l'onboarding → skill `diagnosi-suite`
