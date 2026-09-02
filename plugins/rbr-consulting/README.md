# RBR Consulting — Il cervello dei consulenti RBR

Plugin Claude Code con conoscenza, procedure, regole e integrazioni di
**Restaurant Business Revolution**. Un consulente lo installa e il suo Claude lavora
come quello di Marco: stesse skill, stesse regole, stessi accessi.

## Installazione (per il consulente)

Marketplace **pubblico** (nessun segreto dentro), con auto-aggiornamento:
```
/plugin marketplace add marcocuccaro0309/rbr-consulting
/plugin install rbr-consulting@rbr-consulting
```
Riavvia, poi esegui **`/rbr-setup`**: installa le chiavi RBR (file privato `rbr-chiavi.json`
fornito da Marco → service account, Telegram, MCP GHL/Google Ads/Make a scope utente),
attiva l'auto-update del marketplace, verifica accessi e conoscenza e ti dice cosa manca.
Da lì ogni nuova versione arriva da sola: l'hook di sessione `hooks/auto_update.py` fa il pull
del marketplace a ogni avvio e installa la versione nuova (attiva dalla chat successiva). Guida completa giorno-1: [`ONBOARDING.md`](../../ONBOARDING.md) nel repo.

## Cosa contiene

### Cervello strategico
- **strategia-marketing-rbr** — framework Jay Abraham (3 moltiplicatori, preeminence,
  risk reversal), Alex Hormozi (value equation, grand slam offer, core four) e Frank
  Merenda (posizionamento, risposta diretta, catenaria) applicati alla ristorazione +
  **tono di voce RBR**. Si attiva prima di ogni output strategico o di copy.

### Regole sempre attive + Conoscenza live (hook di sessione)
Le regole RBR (`hooks/regole-rbr.md`) vengono iniettate in OGNI sessione: italiano,
API-first, GHL solo via MCP, riconciliazione prima del CDG, anteprima prima di scrivere
su dati cliente, emoji di sistema, DoD. Nello stesso hook `conoscenza_live.py` legge il
tab "Conoscenza live" dello Sheet contributi (service account, cache 12h) e inietta le
ultime novità del team: quello che UN consulente impara arriva a TUTTI alla sessione
successiva, senza ricaricare il plugin. Avvisa anche se esiste una versione più nuova.

### Cervello condiviso (in due direzioni)
- `contribuisci-conoscenza` — procedure/fix/trucchi → righe nello Sheet "RBR - Contributi conoscenza"
- `scansione-skill` + `/rbr-scansione` — inventario delle skill che il Claude del consulente
  conosce già, filtro personale/RBR, condivisione di intere skill (`skill-nuova:<nome>`)
- Routine cloud del lunedì (`aggiorna-conoscenza-rbr`): fonde contributi e skill nuove nel
  plugin, cerca online le novità (suite, Meta/Google, AI, business, formatori), rilascia la
  versione, aggiorna zip Drive + Conoscenza live, manda il report Telegram a Marco.

### Integrazioni MCP
Nel plugin (nessuna chiave): `meta-ads` (OAuth Facebook del consulente sul BM RBR).
Installate da `/rbr-setup` a scope utente con le chiavi private (`rbr-chiavi.json`):
`google-ads` (account RBR via pipeboard) · `make` · **tutte le istanze GHL `ghl2-<cliente>`**
(PIT agency: misterpizza, personalg, democliente, dirigi, redmike, cipriano, barresi —
cliente nuovo = una riga con il suo locationId in `rbr-chiavi.json`, la aggiunge Marco).

### Skill operative (30)

**Cervello condiviso**
- `contribuisci-conoscenza` — esporta procedure/fix imparati nello Sheet contributi (fusi ogni lunedì)
- `scansione-skill` — inventario delle skill locali del consulente e condivisione di quelle utili al team
- `aggiorna-conoscenza-rbr` — la routine del lunedì (persone + mondo → plugin, zip, Conoscenza live, Telegram)

**Controllo di gestione**
- `cdg-fatture` — CSV Agenzia Entrate → FATTURE.xlsx → foglio "Economico" (script Python + service account + master fornitori condiviso)
- `riconciliazione-dati-cliente` — validazione dati PRIMA di compilare il CDG
- `crea-cdg-cliente` — creare il conto economico del cliente da modello (mono e multi-store)
- `analisi-modello-business` — File 03: CE per fasce orarie e reparti, heat-map turni, saving
- `foodcost-cliente` — File 02: food cost Attuale vs Nuovo, margine per piatto, FC teorico vs bilancio
- `kpi-sheet-cliente` — Google Sheet KPI settimanale
- `analisi-buste-paga` — cedolini PDF → Excel costo del lavoro
- `mappa-turni` — cedolini → mappa colori griglia turni

**Suite / CRM**
- `onboarding-cliente-ghl` — nuovo cliente su GHL: sub-location, snapshot, OAuth, istanza MCP, test end-to-end
- `make-scenario-dod` — scenari Make secondo lo standard RBR (payload 8 campi, router, DoD, attivazione post-fix)
- `diagnosi-suite` — troubleshooting: Resmio 401/403, webhook, token, snapshot GHL, errori Make, iPratico
- `segmentazione-rfm` — segmenti RFM sui contatti GHL + tagging via MCP

**Marketing & funnel**
- `funnel-email-crm` — genera le 57 mail della catenaria (PDF)
- `mail-funnel-ghl` — carica i template del funnel su GoHighLevel via API
- `catenaria-pienissimo` — monta la catenaria nel backoffice Pienissimo Pro
- `campagna-locale` — offerta → landing → QR → coupon POS → email CRM
- `adv-ristorante` — Google Ads + funnel Meta, KPI = costo per prenotazione
- `seo-local-ristorante` — playbook SEO local

**Web & presenza locale**
- `market-discovery-ristorante` — analisi di mercato della zona: domanda, competitor, gap di posizionamento → scheda 1 pagina
- `sito-landing-ristorante` — sito completo (metodo siti-ristoranti) + landing di campagna, con DoD di pubblicazione
- `analytics-ristorante` — GA4 (5 eventi ristorante) + Search Console: setup, lettura mensile, mini-report 10 metriche (MCP ufficiale GA incluso)
- `google-business-ristorante` — scheda Google Business: ottimizzazione, macchina recensioni, post, insight, API vs UI

**Prodotto & contenuti**
- `menu-engineering` — matrice Kasavana-Smith + menu grafico
- `traduci-pdf` — PDF EN→IT reimpaginato per la stampa (logica agente rbr-translate)
- `relazione-rbr` — relazioni Word brandizzate RBR (logo, filetti rossi, tabelle, firma) per ogni consegna al cliente

**Sistema**
- `strategia-marketing-rbr` — vedi sopra (include le sintesi mensili del Circolo degli Imprenditori)
- `aggiorna-conoscenza-rbr` — auto-aggiornamento conoscenza (routine cloud attiva: lunedì ~08:00 IT)
- `contribuisci-conoscenza` — **il cervello condiviso**: quello che un consulente impara
  finisce nello Sheet "RBR - Contributi conoscenza" (via service account) e ogni lunedì
  viene fuso nel plugin di tutti. Da usare sempre prima di aggiornare il plugin.
- `nuovo-agente-rbr` — scaffolding nuovo agente AI RBR (richiede monorepo RBR AI in locale)

### Agenti
- `rbr-reviewer` — applica la Definition of Done a ogni output rilevante prima della consegna.

### Comandi
- `/rbr-setup` — onboarding tecnico guidato con checklist ✅/❌.

## Manutenzione

Le skill codificano le memory di `suite/memory/`: quando una procedura cambia, aggiorna
prima la memory, poi la skill. Le novità esterne le porta dentro `aggiorna-conoscenza-rbr`
(consigliato: schedulata ogni lunedì). Dopo modifiche: commit + push DENTRO `suite/`,
poi aggiorna il puntatore del submodule nel monorepo `RBR AI`.

> ⚠️ Repo privato con chiavi operative in chiaro (scelta esplicita: il team deve essere
> operativo subito). Mai renderlo pubblico; chiave rigenerata = aggiornare doc + `.env` + Make + GitHub Secrets.
