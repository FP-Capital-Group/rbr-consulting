---
name: make-scenario-dod
description: Standard RBR per creare o modificare scenari Make — payload universale 8 campi, router unico RBR-Clienti con Data Store, pattern moduli (returnWrapped, onerror, ifempty), Definition of Done con test pre-deploy, e attivazione post-fix (dopo ogni PATCH blueprint: start + verifica isPaused=false E isinvalid=false). Usala quando il consulente dice "nuovo scenario Make", "modifica lo scenario", "aggiungi un canale al router", "collega il form del sito a Make", "PATCH del blueprint", "lo scenario non si attiva", "aggiungi un cliente/coupon al Data Store". Preferisci sempre i tool MCP mcp__make__* alle chiamate curl.
---

# Scenari Make — standard RBR (Definition of Done)

## Regole trasversali
- **Usa i tool MCP `mcp__make__*`** (scenarios_get, scenarios_update, scenarios_activate, scenarios_run, executions_list, data-store-records_*, validate_blueprint_schema, validate_module_configuration, hooks_*) — curl sull'API Make solo per operazioni non coperte (es. `/dlqs`). Se proprio serve curl: token `MAKE_API_TOKEN` in `.env` (mai hardcoded), base `https://eu1.make.com/api/v2/`, e SEMPRE header `User-Agent` non-default (es. `curl/7.0`) — il WAF CloudFlare di Make blocca gli UA Python di default con 403 `error code: 1010`.
- **Piano B se il connettore MCP Make è giù nella sessione**: interroga lo stesso server MCP da
  script, JSON-RPC in POST (`initialize` → `tools/call`), riusando `Mcp-Session-Id`. Header
  obbligatori: `Accept: application/json, text/event-stream`, `MCP-Protocol-Version: 2025-06-18`,
  `User-Agent` esplicito (stesso WAF Cloudflare dell'errore 1010 sopra).
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
- **⚠️ GetRecord + AddRecord sulla STESSA key nella stessa esecuzione** = `Record is locked by the
  scenario`. Se lo scenario legge lo stato precedente da un Data Store e lo riscrive
  (`overwrite: true`), due eventi ravvicinati sullo stesso record (es. due update dello stesso
  record) fanno morire l'esecuzione in modo sistematico sull'AddRecord: tutto quello che sta a
  valle non gira. Col Sentinel l'errore va in DLQ invece di spegnere lo scenario — lo scenario
  resta attivo e valido, ma il lavoro non si fa mai, quindi il sintomo è "DLQ che cresce con lo
  scenario attivo e valido". **FIX:** se basta reagire a uno stato finale, togli il Data Store e
  filtra sullo stato letto dall'API (non serve la memoria del precedente). Se serve davvero la
  transizione fra stati, lettura e scrittura vanno su record diversi, o la scrittura va a fine
  flusso — 🟡 non ancora collaudato, da verificare prima di usarlo come standard. Non riguarda un
  GetRecord in sola lettura su `rbr_clients` del router.
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
5. Verifica side-effect: i payload TEST non devono creare contatti reali → email `test-router-XXX@rbr-test.local` / `test-onboard-XXX@rbr-test.local` (cleanup: search GHL per `@rbr-test.local` via MCP ghl2, delete). Il cleanup comprende anche lo **stato lato server** sporcato dal collaudo: registri, contatori, tavoli finti. Se il server MCP GHL in uso non espone la cancellazione dei contatti (il catalogo MCP ufficiale GHL non ha il delete), cancella via REST `DELETE /contacts/{id}` col PIT della location.
6. **Dove vive il processo** (contributo di Luciano Purpi, 2026-09-03): se deve girare da solo, deve girare FUORI dalla sessione (scenario Make, routine cloud, cron sul server, GitHub Actions). Un loop ospitato in una scheda del browser o in una sessione Claude NON è un'automazione: si ferma quando il Mac va in sospensione (caso reale: 41 ore di blackout, 5 prenotazioni su 10 mai arrivate in sala) e nessun tuning in sessione lo risolve. Se per forza resta in una scheda, al cliente si dichiara **presidiato**, non attivo. Monitoraggio sull'**orologio dell'ultimo giro** (alert se più vecchio di N minuti), non sull'esito dell'ultimo giro.
   - ⚠️ **Le attività programmate LOCALI dell'app Claude** (`~/.claude/scheduled-tasks/`) partono
     solo se l'app è aperta; se è chiusa partono al primo avvio successivo, e col Mac in
     sospensione non girano — stesso difetto del loop nel browser. Vanno bene per giri di
     controllo o report che tollerano un ritardo, non per processi critici (sync prenotazioni,
     recupero annulli, avvisi). Prima di fidarti di una di queste attività, controlla con
     `list_scheduled_tasks` / `list_task_runs` quando è girata davvero.
   - **Orologio a 3 livelli per un giro ogni N minuti:** (1) scenario Make di 1 solo modulo HTTP
     GET verso l'endpoint del giro, con gettone (`?t=`) e gestione errore "Ignore" (evita che un
     4xx/5xx disattivi lo scenario, cfr. nota handleErrors sopra), schedulato ogni 5 min — fa SOLO
     il battito, niente scritture sui contatti; (2) `wp-cron` solo come riserva: su un sito
     WordPress poco visitato non è un orologio affidabile; (3) cron di sistema del server (es.
     Plesk) come terzo livello, se il piano lo consente — 🟡 livello ancora da attivare/verificare
     caso per caso. Sentinella sull'ora dell'ultimo giro (es. `ultimo_giro < 20 min`) dentro un
     giro di controllo quotidiano.
   - **Routine sulla stessa API a quota** (Fatture in Cloud oraria, GHL ~60/min, Sheets 60
     read/min) non vanno lanciate in parallelo: si rubano la quota e una fallisce (es. FIC
     risponde 403 `USAGE_LIMIT_REACHED` con header `retry-after`). Accorpale come passi dello
     stesso giro, in ordine dopo le estrazioni da cui dipendono. Le routine con fonti e consegne
     diverse restano separate, così un guasto non ferma le altre.
7. **Automazione che scrive su sistemi vivi** (tavoli Resmio, contatti GHL, messaggi ai clienti):
   (a) interruttore on/off nel codice o in un file (es. `LIBERA_RESMIO=false`, `acceso.txt`), così
   si spegne senza toccare il codice; (b) modalità PROVA: gira sui dati veri ma scrive solo nel
   registro quello che avrebbe fatto; (c) audit avversario prima di accendere, con più revisori +
   uno scettico sui casi limite, usando dati di serate vere (walk-in non registrati, pagamenti
   parziali, numeri di tavolo uguali in sale diverse, guardie su orari); (d) lettura del registro
   di almeno una serata in prova; (e) accensione solo con l'ok del titolare.

## ⭐ Attivazione post-fix (regola obbligatoria)
Se l'automazione scrive su sistemi vivi, prima di riattivarla vale il punto 7 della DoD
(interruttore, modalità prova, audit avversario, ok del titolare).

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
| `Record is locked by the scenario` / esecuzione ferma a poche ops, bundle in DLQ | GetRecord+AddRecord sulla stessa key con eventi ravvicinati dello stesso record | Togli il Data Store se basta lo stato finale, altrimenti record separati |

Per errori runtime, DLQ e incident → skill `diagnosi-suite`.

## Documentazione obbligatoria
Ogni nuovo scenario `RBR-*` va documentato in `suite/memory/ghl_blueprint_v2_data_store.md`: nome + ID + cartella, webhook URL, flow ad alto livello, per quale cliente, side-effect, test verificato (data + risultato).

(contributo di Andrea Chirivì, 12/10/2026, su: trappola Data Store, orologio locale vs cloud, DoD
sulle automazioni che scrivono su sistemi vivi, orologio a 3 livelli, routine su API a quota,
piano B MCP, cleanup collaudo)

## Riferimenti
- `suite/quality/DEFINITION_OF_DONE_make_scenarios.md` — lo standard completo
- `suite/memory/rbr_payload_standard.md` — payload universale
- `suite/memory/make_scenarios.md` — storia scenari, incident e trabocchetti
- `suite/memory/rbr_error_sentinel.md` — sistema errori
- Onboarding cliente nuovo (riga rbr_clients, webhook Resmio) → skill `onboarding-cliente-ghl`
