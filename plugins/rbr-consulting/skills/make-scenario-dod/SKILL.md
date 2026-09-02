---
name: make-scenario-dod
description: Standard RBR per creare o modificare scenari Make — payload universale 8 campi, router unico RBR-Clienti con Data Store, pattern moduli (returnWrapped, onerror, ifempty), Definition of Done con test pre-deploy, e attivazione post-fix (dopo ogni PATCH blueprint: start + verifica isPaused=false E isinvalid=false). Usala quando il consulente dice "nuovo scenario Make", "modifica lo scenario", "aggiungi un canale al router", "collega il form del sito a Make", "PATCH del blueprint", "lo scenario non si attiva", "aggiungi un cliente/coupon al Data Store". Preferisci sempre i tool MCP mcp__make__* alle chiamate curl.
---

# Scenari Make — standard RBR (Definition of Done)

## Regole trasversali
- **Usa i tool MCP `mcp__make__*`** (scenarios_get, scenarios_update, scenarios_activate, scenarios_run, executions_list, data-store-records_*, validate_blueprint_schema, validate_module_configuration, hooks_*) — curl sull'API Make solo per operazioni non coperte (es. `/dlqs`). Se proprio serve curl: token `MAKE_API_TOKEN` in `.env` (mai hardcoded), base `https://eu1.make.com/api/v2/`, e SEMPRE header `User-Agent` non-default (es. `curl/7.0`) — il WAF CloudFlare di Make blocca gli UA Python di default con 403 `error code: 1010`.
- **Prima di creare uno scenario per un cliente specifico, chiediti se basta aggiungere un campo al Data Store** e gestirlo nel router universale `RBR-Clienti`. È la regola d'oro.

## Architettura di riferimento (1 router per tutti i clienti)
- Scenario **`RBR-Clienti`** (id `6054617`, cartella RBR `350534`) — core produzione
- Webhook universale: `https://hook.eu1.make.com/8f726kbr6l5swrcf8mjf9q7hvr52go73` (hook `3175860`)
- Data Store **`rbr_clients`** (id `131658`, key = `facility_id` Resmio o `client_source`) e **`rbr_coupons`** (id `131659`, key = `{brand_key}:{code}`)
- Scenari onboard: `RBR-Onboard-Cliente` (6055051) e `RBR-Onboard-Promo` (6055411)
- Flow router: webhook → GetRecord rbr_clients (key `ifempty(facility_id; client_source)`) → GET Resmio (graceful) → POST Smistamento GHL → Router (branch coupon: lookup + POST QR | branch iPratico: search + create actor)

## Payload universale — gli 8 campi standard
Ogni canale non-Resmio (form sito, cassa POS, fidelity, landing, app) POSTa JSON al webhook universale:

| Campo | Required | Esempio |
|---|---|---|
| `client_source` | ✅ | `dirigi-jesolo` (= key del record in `rbr_clients`) |
| `action` | ✅ | `LEAD_NEW`, `FORM_CONTACT`, `LANDING_COUPON_REQUEST`, `FIDELITY_SIGNUP`, `FIDELITY_REDEEM` |
| `first_name` / `last_name` | — | |
| `email` | — | necessaria per iPratico + QR |
| `phone` | — | E.164 con `+` (decide lingua mail IT/EN) |
| `birthday` | — | `YYYY-MM-DD` |
| `coupon_code` | — | `BENVENUTO20PERC` |

**Almeno email O phone**, altrimenti il flow scarta l'evento. NON mandare `location_id_ghl`, webhook URL, api key o descrizioni coupon: il router li recupera dai Data Store. Resmio è l'eccezione: manda il suo payload nativo (`facility_id` + `id`), il router lo riconosce e arricchisce via GET API. Specifica completa: `suite/memory/rbr_payload_standard.md`.

### Aggiungere un nuovo canale (zero scenari nuovi)
1. Trova il `client_source` in `rbr_clients` (`mcp__make__data-store-records_list` su 131658)
2. Configura il canale per POST al webhook universale col payload standard
3. Test 1 evento → History di RBR-Clienti + contatto in GHL + actor iPratico
4. Annota in `rbr_clients.notes`: "live channel: <nome>"

## Naming e organizzazione
- `RBR-<funzione>` per scenari core multi-cliente · `RBR-<funzione>-<cliente>` solo se inevitabile · `<CLIENTE> — <funzione>` è legacy da deprecare
- Cartella `RBR`/`Comuni` (350534) per gli scenari core; cartelle per locale per i legacy
- Ogni modulo con nome leggibile in `metadata.designer.name` (es. `[Resmio only] GET booking (graceful fail)`)

## Pattern moduli (trappole note)
- **GetRecord**: `returnWrapped: false` nel mapper è **obbligatorio** (senza, fallisce silenzioso)
- **AddRecord**: il sub-oggetto si chiama `data` (non `record`), con `overwrite: true` per idempotenza
- **Filter "cliente trovato"**: NON su `{{2.client_key}}` non vuoto (GetRecord con chiave inesistente ritorna campi vuoti senza errore) — usa presenza di `brand_key` o `location_id_ghl`
- **Filter su flow lineare BLOCCA il branch** (non salta solo il modulo): se serve "salta ma continua" → Router con 2 routes, oppure `handleErrors: true` (HTTP) / `ifempty(...)` (mapping)
- **Make NON ha `and()/or()/not()`** come funzioni → `if` annidati
- **Funzioni built-in senza virgolette**: `newline`, `now`, ecc. — con le virgolette diventano stringhe letterali
- **Fallback dati persona**: `{{ifempty(3.data.X; 1.X)}}` (Resmio se c'è, altrimenti payload originale). E ogni riferimento a `3.data.X` va guardato sull'esistenza del booking (`if(1.id; 3.data.X; "")`) — un GET graceful che riceve HTML mette la stringa grezza in `.data` e inquina tutti i campi
- **⚠️ `handleErrors: true` senza `onerror` è una bomba**: un singolo 4xx fa fallire l'esecuzione e Make disattiva+invalida lo scenario, accodando i webhook di TUTTI i clienti (incident 2026-07-12). Ogni modulo HTTP con handleErrors DEVE avere un handler onerror
- **Error handling standard RBR (Sentinel V4)**: ogni modulo HTTP critico ha onerror = AddRecord in `rbr_error_log` (Data Store `131753`) + `builtin:Break` con retry=true, count=3, interval=5 min. Al 4° fallimento → DLQ permanente (intervento manuale). Vedi `suite/memory/rbr_error_sentinel.md`
- **PATCH blueprint via API**: il campo `blueprint` va passato come **stringa JSON** (`json.dumps`), non oggetto raw
- **Prima di ogni PATCH: backup del blueprint** in `data/make_backups/scenario_<id>_pre_<motivo>_<data>.json` (pattern consolidato in `suite/memory/make_scenarios.md`)

## Definition of Done — test pre-attivazione
Prima di dichiarare uno scenario pronto:
1. `mcp__make__validate_blueprint_schema` → nessun errore
2. `mcp__make__validate_module_configuration` sui moduli critici → tutti valid
3. Test POST con payload finto al webhook → verifica execution history
4. Per ogni branch del Router: test separato con payload che attiva quel branch
5. Verifica side-effect: i payload TEST non devono creare contatti reali → email `test-router-XXX@rbr-test.local` / `test-onboard-XXX@rbr-test.local` (cleanup: search GHL per `@rbr-test.local` via MCP ghl2, delete)

## ⭐ Attivazione post-fix (regola obbligatoria)
**Dopo OGNI PATCH al blueprint di uno scenario:**
1. Riattiva: `mcp__make__scenarios_activate` (equivalente `POST /scenarios/:id/start`)
2. Rileggi lo scenario (`mcp__make__scenarios_get`) e verifica **`isPaused: false` E `isinvalid: false`** — entrambi, prima di dichiarare lo scenario attivo
3. Trabocchetto: dopo un PATCH ai flag DLQ, `isinvalid` NON si auto-resetta finché i `metadata.designer.messages` di warning stale non vengono svuotati esplicitamente — senza pulizia l'activate fallisce con "Scenario contains errors"
4. Nota: i Break con `retry: true` richiedono `metadata.scenario.dlq=true, dataloss=true` nel blueprint, altrimenti lo scenario resta invalid

## Disattivare scenari legacy
1. NON cancellare, solo deactivate (preserva la history)
2. Prefisso `[DEPRECATED YYYY-MM-DD]` nel nome
3. Aggiorna `suite/memory/ghl_blueprint_v2_data_store.md` con la data
4. Soak 7 giorni — se nessuno reclama, considera permanente

## Errori noti (sintomo → fix)
| Sintomo | Causa | Fix |
|---|---|---|
| `filterRoot.map is not a function` | Filter SearchRecord con sintassi non-array | Usa `[[{...}]]` |
| `Validation failed for 1 parameter(s)` | Campo mandatory mancante nel mapper | `validate_module_configuration` per scoprirlo |
| `Function 'and' not found!` | `and(x; y)` usato come funzione | if annidati |
| Flow si ferma a 2-3 ops | Filter blocca il branch lineare | Router o handleErrors/ifempty |
| `isinvalid: true` dopo update | Riferimenti mapper rotti o messages stale | Verifica `{{N.X}}` + pulisci designer.messages |

Per errori runtime, DLQ e incident → skill `diagnosi-suite`.

## Documentazione obbligatoria
Ogni nuovo scenario `RBR-*` va documentato in `suite/memory/ghl_blueprint_v2_data_store.md`: nome + ID + cartella, webhook URL, flow ad alto livello, per quale cliente, side-effect, test verificato (data + risultato).

## Riferimenti
- `suite/quality/DEFINITION_OF_DONE_make_scenarios.md` — lo standard completo
- `suite/memory/rbr_payload_standard.md` — payload universale
- `suite/memory/make_scenarios.md` — storia scenari, incident e trabocchetti
- `suite/memory/rbr_error_sentinel.md` — sistema errori
- Onboarding cliente nuovo (riga rbr_clients, webhook Resmio) → skill `onboarding-cliente-ghl`
