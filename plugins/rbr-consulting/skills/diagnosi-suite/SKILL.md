---
name: diagnosi-suite
description: Troubleshooting della suite RBR (Resmio, Make, GHL, iPratico) organizzato per sintomo → causa probabile → fix. Usala quando il consulente dice "le conferme WhatsApp non arrivano", "Resmio dà 401/403", "il cliente ha prenotato ma il contatto non è in GHL", "il QR non è arrivato", "lo scenario Make è in errore / si è disattivato", "webhook che non arrivano", "il token è scaduto", "lo snapshot non ha portato le mail/i workflow", "iPratico non risponde". Parti sempre dal sintomo e risali la pipeline Resmio → Make → GHL → iPratico.
---

# Diagnosi suite RBR (sintomo → causa → fix)

La pipeline standard è: **Resmio/sito/cassa → webhook universale Make → scenario `RBR-Clienti` (6054617) → GHL Smistamento Lead → mail/WhatsApp/QR → iPratico actor**. Ogni sintomo va localizzato lungo questa catena. Operazioni GHL sempre via MCP `ghl2-<cliente>` (search_operations → describe_operation → execute_operation), operazioni Make via tool `mcp__make__*`.

---

## 1. Resmio risponde 401/403

**Causa probabile: la chiave API è stata rigenerata o revocata.** Verità vitali (incident 2026-05-31):
- **UNA chiave per utente-account, account-wide**: la chiave MP copre tutte e 3 le facility MP. MP e Dirigì sono **account distinti** con chiavi distinte — non scambiarle
- Rigenerare la chiave OVUNQUE in UI invalida la precedente → tutto va a 401 finché non aggiorni `.env` + moduli Make + GitHub Secrets
- Resmio ha già revocato chiavi silenziosamente (release interna) — support: "non sappiamo perché". Se una chiave muore, qualcuno l'ha rigenerata o Resmio ha fatto pulizia
- ⚠️ **TRAPPOLA test**: `GET /v1/facility/<id>/` è PUBBLICO, risponde 200 per qualsiasi facility anche di account terzi. **NON usarlo per verificare una chiave.** Il test valido è `GET https://app.resmio.com/v1/facility/<id>/bookings/?limit=1` con header `Api-Key: <key>` → 200 = ok, 401 = chiave non copre quell'account
- **Throttle per-IP** dopo raffiche di 401: si sblocca da solo in ~30-40 min (metti in pausa lo scenario durante il fix)

**Fix (procedura rapida):**
1. app.resmio.com (account giusto!) → Settings → Integration → "resmio Api Details" → rigenera/copia la key
2. Verifica con il GET bookings sopra su una facility dell'account
3. Sostituisci la chiave nell'header `Api-Key` dei moduli GET Resmio degli scenari Make interessati (via `mcp__make__scenarios_get`/`scenarios_update`)
4. Aggiorna `RESMIO_*_KEY` in `.env` di `RBR AI/mister-pizza` + GitHub Secrets (`RESMIO_MP_KEY`, `RESMIO_DIRIGI_KEY`)
5. Riattiva lo scenario e verifica `isPaused=false` E `isinvalid=false` (skill `make-scenario-dod`)
6. Sintomo classico della chiave morta: mail d'errore `parseDate('')`, GHL Create Contact "no value was found for any of the mapped fields", WhatsApp SKIPPED — e lo scenario risulta "OK" perché il 401 non blocca il flow

Incident completo + storia chiavi: `suite/memory/incident_resmio_key_revoked_20260531.md`.

## 2. Webhook che non arrivano (prenotazione fatta, niente contatto/QR/WhatsApp)

Risali la catena in quest'ordine:
1. **Il webhook Resmio esiste per QUELLA facility?** Incident MP 2026-06-11: Duomo e Mestre non avevano NESSUN webhook configurato — non era un bug, mancava proprio. UI Resmio → `/<facility>/settings/integration#developers` → deve esserci `https://hook.eu1.make.com/8f726kbr6l5swrcf8mjf9q7hvr52go73` con eventi BOOKING_CREATED/UPDATED. Solo UI (API read-only sui webhook)
2. **Lo scenario `RBR-Clienti` è attivo e ha ricevuto l'esecuzione?** `mcp__make__scenarios_get` (6054617): `isActive`, `isPaused`, `isinvalid`, `dlqCount`. Poi `mcp__make__executions_list` / History. Se lo scenario è auto-disattivato → sezione 5
3. **Il cliente è nel Data Store?** `rbr_clients` (131658): record con key = `facility_id`/`client_source`, `active: true`, `webhook_smistamento_url` valorizzato. Se manca la riga, il filter "cliente trovato" scarta tutto in silenzio
4. **Payload standard corretto?** Almeno `client_source` + `action` + email O phone (`suite/memory/rbr_payload_standard.md`). Senza email e phone il flow scarta l'evento
5. **Workflow GHL attivi?** Via `ghl2-<cliente>`: Smistamento Lead e Funnel RBR devono essere Published + Active. Il QR richiede il workflow "QR Email" attivo e il coupon presente in `rbr_coupons` (131659) con key `{brand_key}:{code}`
6. Replay possibile: ri-POSTa `{action: "BOOKING_CREATED", id: <booking>, facility_id: <facility>}` al webhook universale

## 3. Token / connessioni scadute

- **Token GHL morti (PIT 403 "does not have access", OAuth 401 "Invalid refresh token"/"Invalid JWT")**: serve ri-autorizzazione — rigenerare il PIT nella location (Settings → Private Integrations) e/o reinstallare l'app OAuth + rilanciare `scripts/ghl_sync_all_locations.py`. È successo il 2026-06-11 (tutti i token giù insieme). Se non hai accesso agency → **chiedi a Marco**
- **401 su singoli tool MCP ghl2 in modalità OAuth**: non è un token scaduto — sono i limiti di scope dell'app SA (niente calendari, fatture, pagamenti, prodotti). Serve PIT o estensione scope: chiedi a Marco
- **403 `error code: 1010` su API GHL/Make da script**: CloudFlare WAF che blocca User-Agent di default Python — usa sempre un UA non-default (es. `curl/7.0`). Non è un problema di token
- **WhatsApp disconnesso** ("Action Required" in Settings → WhatsApp): la connessione cade se il cliente non apre l'app WhatsApp Business sul telefono del locale almeno 1 volta ogni 14 giorni. Fix: Disconnect → riconnetti con lo stesso flusso Meta (login Business Manager + scansione QR). ⚠️ GHL non espone lo stato connessione WhatsApp via API — si vede solo in UI. Per token/asset Meta Business scaduti oltre questo caso → **chiedi a Marco**
- **Chiave Resmio** → sezione 1 · **apiKey iPratico** → sezione 6

## 4. Snapshot GHL non applicato (mail/workflow/campi mancanti)

Dopo "Apply Snapshot RBR Blueprint v1" l'applicazione richiede **2-5 minuti**. Poi verifica (via `ghl2-<cliente>` o UI) che ci sia tutto:
- **14 Custom Field** (3 RFM + 6 statistiche + 5 booking/QR) · **13 Custom Values** (con valori demo, da personalizzare) · **3 tag** `locale`/`turista`/`fidelity` · **15 email template** · **2 workflow** Smistamento Lead + Funnel RBR

Cose che lo snapshot **non porta MAI** (non sono anomalie): sending domain email, custom landing domain, WhatsApp, limite invio email, riga Make `rbr_clients`. E l'**Inbound Webhook URL** del workflow Smistamento è NUOVO per ogni cliente (va riletto dal canvas, non copiato dal demo).

Se dopo l'attesa mancano asset dello snapshot → lo snapshot agency lo gestisce solo Marco: **chiedi a Marco** (non ricreare i pezzi a mano, escono disallineati dai cloni futuri).

## 5. Errori Make (scenario in errore, disattivato, DLQ)

**Sistema errori standard (Sentinel V4)**: ogni modulo HTTP critico di RBR-Clienti ha onerror = log in Data Store `rbr_error_log` (131753) + Break retry 3 tentativi ogni 5 min → al 4° fallimento il bundle finisce in **DLQ** (intervento manuale). Dashboard: UI Make → Data Stores → `rbr_error_log` (filtra `classification=persistent` per quelli da fixare; `resolved: true` quando sistemato). Doc: `suite/memory/rbr_error_sentinel.md`.

| Sintomo | Causa probabile | Fix |
|---|---|---|
| Scenario **auto-disattivato** + webhook in coda | Un modulo HTTP con `handleErrors: true` ma SENZA onerror ha preso un 4xx → l'esecuzione fallisce → Make disattiva+invalida (incident 2026-07-12: 401 Resmio Red Mike, 99 webhook in coda 17h) | Aggiungi onerror al modulo (o `handleErrors: false` se il downstream è già guardato) → riattiva → verifica isPaused/isinvalid false. I webhook in coda vengono processati al riavvio — occhio al rate limit GHL 60/min (429 in DLQ; `maximum_runs_per_minute` del router è a 50 apposta) |
| DLQ che si accumulano con errori di **mapping** (`Invalid date`, `Bad control character`) | Payload senza booking → GET Resmio ritorna HTML → `3.data.campo` su una stringa restituisce l'intera stringa HTML (l'onerror NON cattura errori di mapping) | Guarda ogni uso di `3.data.X` sull'esistenza del record: `if(1.id; 3.data.X; "")` (fix 2026-07-01, già in produzione — se ricompare, un nuovo campo non è guardato) |
| `isinvalid: true` dopo un PATCH | Riferimenti mapper rotti, o `metadata.designer.messages` stale, o Break retry senza `dlq=true, dataloss=true` | Skill `make-scenario-dod`, sezione "Attivazione post-fix" |
| Esecuzione "OK" ma dati vuoti a valle | 401/4xx silenzioso su un GET (il modulo non valuta gli errori) | Sezione 1 (chiave Resmio) — controlla il body del GET nella History |
| Mail QR non parte ma tutto il resto ok | Coupon assente/`active:false` in `rbr_coupons`, o `webhook_qr_url` vuoto in `rbr_clients` | Aggiungi/attiva il record coupon (key `{brand_key}:{code}`) |

Endpoint DLQ (non nel catalogo MCP → curl ammesso): lista `GET /dlqs?scenarioId=:id`, cancella `DELETE /dlqs/:id`.

**Nota monitoring**: i 3 healthcheck GitHub (`make-healthcheck`, `resmio-healthcheck`, `ipratico-healthcheck`) sono **disattivati dal 2026-07-15** (gestione errori passata a una nuova persona). Per riattivarli: aggiornare il secret `TELEGRAM_CHAT_ID` nel repo `rbr-ai` + `gh workflow enable` — coordinati con Marco. Finché sono spenti, nessun alert automatico: il controllo di `dlqCount`/`isinvalid` è manuale.

## 6. iPratico non risponde / actor non creati

- **Host giusto**: `apicb.ipraticocloud.com` (l'host `api.ipratico.com` NON esiste). Auth: header `x-api-key` formato `shopId:secret`
- **Chiavi**: env var / GitHub Secrets `IPRATICO_API_KEY_<LOCALE>` (Duomo/Mestre/Pietra/Dirigì, in chiaro per il team in `suite/memory/ipratico_api.md`). Nel router la key arriva dal campo `ipratico_api_key` del record `rbr_clients`
- **Actor non creato**: serve l'email nel payload (il branch iPratico filtra "ha email + api_key"). I 3 locali MP condividono lo stesso pool business-actors
- **Actor duplicati**: l'API non ha check unicità su email/phone — il flow fa sempre search-by-email prima del create; se trovi duplicati, un create è passato senza search
- **429 / rate limit**: ~60 req/min empirico, retry con backoff
- **Numeri che non tornano col portale** (chiusure Z manuali invisibili, referenceDate vs closureDate, Z duplicate): è il dominio dell'API portale privata — vedi `suite/memory/ipratico_portal_api.md`; token portale rigenerato ad ogni cron via login auto (`scripts/refresh_ipratico_portal_token.py`). Il token MP dà **403 su Dirigì** (previsto, saltato dallo script)

## Se il sintomo non rientra in nessuna casella
Documenta cosa hai osservato (scenario, execution id, payload, risposta) e **chiedi a Marco** prima di toccare workflow GHL condivisi, snapshot o scenari core.

## Riferimenti
- `suite/memory/rbr_error_sentinel.md` · `make_scenarios.md` (storia incident) · `resmio.md` · `incident_resmio_key_revoked_20260531.md` · `dirigi_resmio_to_ghl.md` · `gohighlevel.md` · `ipratico_api.md` · `ipratico_portal_api.md`
- Standard scenari e attivazione post-fix → skill `make-scenario-dod`
- Setup cliente da zero → skill `onboarding-cliente-ghl`
