---
name: onboarding-cliente-ghl
description: Procedura completa RBR per onboardare un nuovo cliente ristoratore su GoHighLevel — crea sub-location, applica lo Snapshot "RBR Blueprint v1", installa l'app OAuth v2, registra l'istanza MCP ghl2-[cliente], personalizza Custom Values e subject email, collega Resmio/sito/cassa al router Make e testa end-to-end. Usala quando il consulente dice "nuovo cliente su GHL", "onboarding [nome cliente]", "crea il sub-account per [cliente]", "applica il blueprint", "attiva il CRM per il cliente", "il cliente parte con la piattaforma". Tempo target 30-60 min (escluso WhatsApp + DNS).
---

# Onboarding nuovo cliente RBR su GoHighLevel

## Regola trasversale
**Ogni operazione GHL passa dai tool MCP `ghl2-<cliente>`** (LeadConnector MCP v2 ufficiale): prima `search_operations`, poi `describe_operation`, poi `execute_operation`. Mai curl diretto sull'API GHL, salvo operazioni assenti dal catalogo. Doc: `suite/memory/ghl_mcp_server.md`.

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
4. Verifica post-snapshot (via MCP o UI): **14 Custom Field + 13 Custom Values + 3 tag (`locale`, `turista`, `fidelity`) + 15 email template + 2 workflow** (Smistamento Lead + Funnel RBR). Se manca qualcosa → skill `diagnosi-suite`, sezione "Snapshot non applicato".

## Step 2 — Installa app OAuth v2 + sync token (~2 min)
L'app v2 è Private + Agency Only Install: NON è visibile nel marketplace del cliente, solo in quello agency (oppure via Install Link bookmark "🔧 Install RBR app", URL in `GHL_OAUTH_SA_INSTALL_LINK` in `mister-pizza/.env`).

1. Agency View → App Marketplace → cerca "Restaurant Business Revolution - Claude" → **Install** → Choose Location = sub-location del cliente → **Authorize**
2. Il browser mostra "site can't be reached" → **normale, ignora**
3. Sync token in Neon Postgres:
   ```bash
   cd "/Users/marco/Desktop/AI/RBR AI/mister-pizza"
   .venv/bin/python scripts/ghl_sync_all_locations.py
   ```
   Lo script usa il Company token → genera location_token per ogni sub-account installata → salva in Neon. (Il servizio Render zero-touch NON è deployato: il sync manuale è lo standard, deciso da Marco 2026-05-29.)

## Step 3 — Registra l'istanza MCP `ghl2-<cliente>` (~1 min)
```bash
claude mcp add -s user ghl2-<nome> -- ~/Desktop/AI/GoHighLevel-MCP/run-v2-instance.sh OAUTH <LOCATION_ID>
```
- L'istanza si connette **solo DOPO** che l'app SA è installata sulla sub-account (Step 2)
- In modalità OAuth valgono i limiti di scope dell'app SA: niente calendari/fatture/pagamenti/prodotti (quei tool danno 401). Per scope completi serve un PIT (lo crea Marco): `run-v2-instance.sh <SUFFISSO>` con `GHL_PRIVATE_INTEGRATION_TOKEN_<SUFFISSO>` in `mister-pizza/.env`

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
- ⚠️ **Limiti invio email**: i sub-account nuovi partono a **1.000 mail/giorno** (warm-up automatico LC Email, sale in ~4 settimane se la reputazione è buona; tetto IP condiviso 15.000/giorno). L'override è per singolo account: Agency View → Sub-Accounts → cliente → Advanced Settings → Limits → Email → "Update Limit". Alzare il numero NON alza la reputazione: serve dominio dedicato + SPF/DKIM/DMARC + warm-up. Dettagli: `suite/memory/ghl_email_sending_limits.md`

## Step 8 — WhatsApp Business (opzionale, 3-7 giorni Meta)
`Settings → WhatsApp → Connect` → login Meta Business Manager del cliente → scansione QR dal WhatsApp Business sul telefono del locale. Costo ~$11/mese + ~5¢/msg, pagato dal cliente. Ricordagli di aprire l'app almeno 1 volta ogni 14 giorni o la connessione cade. Template `copy_conferma_prenotazione` (Utility) usa merge tag `{{contact.booking_when_text}}` ecc. → nel workflow serve un Create/Update Contact che valorizzi i custom field booking PRIMA del Send WhatsApp. Dettagli: `suite/quality/ghl_procedura_team_rbr.md` §6.

## Step 9 — Attiva i workflow (~1 min)
Nella sub-location: Workflows → **Smistamento Lead** e **Funnel RBR** → verifica stato **Published** (non draft) → toggle **Active ON**.

## Step 10 — Test end-to-end (~10 min)
Con email test identificabili (`test-onboard-XXX@rbr-test.local` — cleanup facile):
1. POST `source=sito` al webhook → contatto creato + tag `locale`
2. POST `source=fidelity-cassa` + `birthday` → tag `locale`+`fidelity` + Date of Birth popolata
3. Prenotazione finta Resmio (o POST `action=BOOKING_CREATED`) → CF booking popolati + tag + eventuale WhatsApp/QR
4. Cleanup contatti test (search per `@rbr-test.local` via MCP, delete)

Se i 3 test passano → onboarding completato ✅. Aggiorna il calendario clienti in `suite/quality/ghl_procedura_team_rbr.md` §17.

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
