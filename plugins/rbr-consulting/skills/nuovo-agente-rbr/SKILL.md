---
name: nuovo-agente-rbr
description: >-
  Scaffolding di un nuovo agente AI RBR nel monorepo RBR AI: copia del template
  agents/_template/, 3 domande obbligatorie (cosa fa, canale, output dove), registrazione in
  master_brain.md e memory/, convenzioni deploy Render. Usala quando Marco o un consulente dice
  "nuovo agente [nome]", "creiamo un agente che...", "aggiungi un bot RBR". Richiede il monorepo
  RBR AI clonato in locale (/Users/marco/Desktop/AI/RBR AI o equivalente): senza quel repo la
  skill non è applicabile.
---

# Nuovo agente RBR (scaffolding dal template)

Crea un nuovo agente dell'ecosistema RBR (come Keith, Tony, Alex, rbr-translate) seguendo le
convenzioni del monorepo. Fonte delle regole: `RBR AI/CLAUDE.md` (comandi rapidi + intent map),
`memory/master_brain.md`, `agents/_template/CLAUDE.md`.

## Prerequisiti
- Monorepo `rbr-ai` in locale (`/Users/marco/Desktop/AI/RBR AI/`).
- Nome dell'agente (un nome proprio breve, minuscolo: keith, tony, alex, ciro…).

## Procedura

### 1. Le 3 domande obbligatorie (in UN solo messaggio)
Da `RBR AI/CLAUDE.md`, intent map "nuovo agente <nome>". Prima di toccare file chiedi, numerate:
1. **Cosa fa** l'agente (una riga di ruolo)
2. **Su quale canale** vive (default RBR: **Telegram** — è l'interfaccia preferita di Marco)
3. **Output dove** (Google Sheets, Drive, PDF in chat, Excel, …)

Non chiedere altro: il resto sono convenzioni fisse qui sotto.

### 2. Copia il template
```bash
cp -R "/Users/marco/Desktop/AI/RBR AI/agents/_template" "/Users/marco/Desktop/AI/RBR AI/agents/<nome>"
```
Il template contiene solo `CLAUDE.md` (niente skeleton di codice). Compila i placeholder:
- `# [NOME AGENTE] — [Ruolo breve]`
- Identità: "Sei **RBR AI** che lavora su **<NOME>**, <descrizione una riga>"
- "Leggi sempre prima": lascia il riferimento al master brain
- Sezioni: **Stato attuale** (checklist ⬜/✅), **File principali**, **Stack**, **Deploy**

Stack ricorrente degli agenti esistenti (usalo come default se compatibile con le 3 risposte):
Python + `python-telegram-bot` (polling) o FastAPI+webhook, Claude via `anthropic`,
`python-dotenv`; segreti in `.env` locale (mai committati) e come env vars su Render.

### 3. Registra l'agente in master_brain.md
Aggiungi una sezione in `memory/master_brain.md` sotto "Agenti attivi / in costruzione",
nello stesso formato delle esistenti (vedi Keith/Tony):
- `### <emoji colore> <NOME> — <Ruolo>`
- **Ruolo**, **Canale** (bot Telegram + token quando creato su @BotFather), **Server/Deploy**,
  **Repo**, **File locali**, **Stack**, **Sa fare** (elenco), **Backlog**

### 4. Crea la memoria dell'agente
Convenzione da `RBR AI/CLAUDE.md`: dettaglio tecnico → `memory/agent_<nome>.md` + riga di indice
in `memory/MEMORY.md` sezione "Dettaglio agenti" (formato: `[agent_<nome>.md](agent_<nome>.md) —
<Nome>: <cosa contiene>`). All'inizio può essere corto: architettura decisa + link ai file.

### 5. Aggiorna il CLAUDE.md di root
In `RBR AI/CLAUDE.md`:
- riga in "Agenti attivi (cartella `agents/`)": `- **<nome>** — <ruolo breve>`
- voce nell'intent map se l'agente ha un trigger naturale (es. "buste paga <mese>" → Tony)

### 6. Convenzioni deploy (Render)
Pattern di riferimento: Keith (`agents/keith/CLAUDE.md`).
- Servizio su **Render**, deploy automatico dal push GitHub (~2 min). Keith documenta
  `git add -A && git commit && git push origin main` dalla cartella agente; il CLAUDE.md di root
  indica `git push render main` — ⚠️ i due doc divergono, verifica il remote effettivo del
  nuovo servizio e scrivilo nel CLAUDE.md dell'agente.
- Env vars sul dashboard Render, mai nel codice. Set tipico (da Keith):
  `ANTHROPIC_API_KEY`, `TELEGRAM_BOT_TOKEN`, `GOOGLE_SA_JSON` (service account base64, se usa
  Sheets/Drive), `WEBHOOK_SECRET`.
- Prima del deploy va bene girare in locale in polling (pattern Tony/rbr-translate); il passaggio
  a webhook è un'evoluzione, non un requisito del giorno 1.

### 7. Stile dell'agente (non negoziabile, da master_brain.md)
- Italiano sempre, risposte brevi, niente fronzoli
- Tutte le domande mancanti in UN messaggio numerato, mai ripetere domande già risposte
- Emoji di sistema: ✅ OK · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata
- Se scrive su Google Sheets: valori IVA esclusa (÷1.1 ristorazione), mai sovrascrivere formule
  o dati esistenti senza conferma (regole "I 5 FILE RBR" in master_brain.md)

## Regole & trabocchetti
- ❌ Mai modificare `agents/_template/`: solo copiarlo.
- ⚠️ Token bot Telegram: crearlo su @BotFather, metterlo in `.env` e su Render.
- ⚠️ Se l'agente tocca GHL: ogni operazione via MCP `ghl2-<cliente>` (search_operations →
  describe_operation → execute_operation), mai curl diretto — doc `suite/memory/ghl_mcp_server.md`.
- Prima della consegna passa l'output al sub-agente `rbr-reviewer` (DoD del progetto);
  `quality/DEFINITION_OF_DONE.md` è previsto dal CLAUDE.md di root — se assente, scrivilo alla
  prima occasione.

## Definition of Done
- [ ] 3 domande fatte in un solo messaggio e risposte registrate
- [ ] `agents/<nome>/` creato dal template, CLAUDE.md compilato (identità, stato, stack, deploy)
- [ ] Sezione agente in `memory/master_brain.md`
- [ ] `memory/agent_<nome>.md` creato + riga in `memory/MEMORY.md`
- [ ] `RBR AI/CLAUDE.md` aggiornato (lista agenti + eventuale intent map)
- [ ] Convenzioni deploy Render documentate nel CLAUDE.md dell'agente (remote git verificato)
