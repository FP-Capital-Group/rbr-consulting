---
name: scansione-skill
description: Scansiona le skill, i comandi e gli agenti che il Claude di questo consulente conosce già (fuori dal plugin RBR), li classifica in "utili al team RBR" vs "personali/non pertinenti" e, dopo conferma, condivide quelli utili col cervello condiviso (righe skill-nuova nello Sheet contributi, fuse nel plugin il lunedì). Usa al primo /rbr-setup, quando l'utente dice "guarda che skill ho", "cosa posso condividere col team", "condividi la mia skill X", o dopo che ha installato/creato una skill nuova.
---

# Scansione skill del consulente → cervello condiviso

Ogni consulente arriva con il suo Claude già "educato": skill personali, comandi,
agenti, plugin. Alcune sono oro per il team (un metodo di analisi, uno script per un
gestionale, un template), altre sono personali (altri business, hobby, dev generico).
Questa skill fa l'inventario, propone cosa condividere, e condivide SOLO con l'ok
dell'autore.

## Procedura

### 1. Inventario (script, zero giudizio)
```
python3 "<cartella di questa skill>/scripts/scansiona_skill.py" --json /tmp/inventario_skill.json
```
(la cartella è `${CLAUDE_PLUGIN_ROOT}/skills/scansione-skill/`; se la variabile non è
disponibile, trovala con Glob `**/scansione-skill/scripts/scansiona_skill.py`).
Lo script guarda: `~/.claude/skills`, `~/.claude/commands`, `~/.claude/agents`, plugin
Claude Code e Cowork installati, skill/comandi di progetto sotto Desktop/Documents/dev,
e SEGNALA (senza proporli in blocco) i file CLAUDE.md e la memoria personale.
Esclude il plugin RBR e i plugin pubblici Anthropic. Non invia nulla.

### 2. Classificazione (tu, Claude)
Per ogni voce decidi, leggendo descrizione e se serve il SKILL.md:
- **UTILE AL TEAM** — riguarda ristorazione, marketing/adv, CRM (GHL/Make/Pienissimo),
  controllo di gestione, dati/report, documenti per clienti, automazioni ripetibili.
- **PERSONALE / NON PERTINENTE** — altri business del consulente, vita privata, dev
  generico, tool già coperti da una skill RBR equivalente (dillo: "coperta da X").
- **PUBBLICA** — skill scaricata da un marketplace pubblico: non ricopiarla, proponi di
  citarla come tool consigliato (nome + link + casi d'uso RBR).
Filtri duri: voci con flag `segreti` → si condividono solo dopo pulizia (lo script
oscura i token, ma verifica); `path personali` → ok, lo script li normalizza a `~/`.
CLAUDE.md e memoria personale: MAI in blocco. Se contengono una regola/procedura
di team, estraila come contributo testuale con `contribuisci-conoscenza`.

### 3. Proposta (un solo messaggio)
Tabella: `# | Skill | Perché utile al team | Proposta (condividi / cita / salta)`.
Poi: "Confermi? Puoi togliere/aggiungere numeri." 🟡 Aspetta la risposta. Se il
consulente ha fretta: chiudi con "puoi rifarlo quando vuoi con /rbr-scansione".

### 4. Condivisione (solo le confermate)
Per ogni skill confermata:
```
python3 "<cartella skill>/scripts/condividi_skill.py" "<Nome Cognome>" "<path skill>" --nota "<quando usarla e perché è utile, 1-2 frasi>"
```
Prima esegui con `--dry-run` per mostrare all'autore i file che partono; poi senza.
Lo script scrive righe `skill-nuova:<nome>` nello Sheet "RBR - Contributi conoscenza"
(un file per riga, SKILL.md per primo, parti da 45k caratteri). Serve
`pip3 install gspread google-auth`; se il service account non vede lo Sheet → ⚠️ avvisa
Marco e salva lo zip della skill in `~/Desktop/da_condividere_rbr/` come backup.
Per le voci "cita": una riga testuale con `contribuisci-conoscenza` (area `tool`).

### 5. Chiusura
✅ "Condivise N skill: <nomi>. Marco le valuta nel digest settimanale e decide se entrano nel plugin di tutti (
riceve il report su Telegram). Le skill restano anche in locale, non cambia nulla per te."
Se chiamata da `/rbr-setup`, riporta l'elenco per il report a Marco.

## Regole
- L'autore decide: niente condivisione senza conferma esplicita.
- Un consulente può ripetere la scansione in qualsiasi momento (`/rbr-scansione`): le
  skill già condivise vanno segnate "già nel cervello condiviso" (controlla se esiste
  `skills/<nome>` nel plugin o una riga `skill-nuova:<nome>` recente).
- Niente segreti nuovi nello Sheet: token e chiavi passano da Marco.
