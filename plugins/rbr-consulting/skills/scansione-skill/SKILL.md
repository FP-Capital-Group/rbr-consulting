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
Segnala anche le skill personali che hanno lo stesso nome di una skill già nel plugin RBR
(flag `doppione plugin: identica/diversa`, confronto file per file) e i percorsi citati nel
SKILL.md che non esistono dentro la cartella (flag `file mancanti`). (contributo di Andrea
Chirivì, 2026-10-12)

### 2. Classificazione (tu, Claude)
Per ogni voce decidi, leggendo descrizione e se serve il SKILL.md:
- **UTILE AL TEAM** — riguarda ristorazione, marketing/adv, CRM (GHL/Make/Pienissimo),
  controllo di gestione, dati/report, documenti per clienti, automazioni ripetibili.
- **PERSONALE / NON PERTINENTE** — altri business del consulente, vita privata, dev
  generico, tool già coperti da una skill RBR equivalente (dillo: "coperta da X").
- **PUBBLICA** — skill scaricata da un marketplace pubblico: non ricopiarla, proponi di
  citarla come tool consigliato (nome + link + casi d'uso RBR).
Filtri duri: voci con flag `segreti` → si condividono solo dopo pulizia (lo script
oscura i token, ma verifica); `file esterni` o `file mancanti` → normalizzare il percorso
NON basta, perché il collega quei file non li ha. Ogni file che la skill usa (script,
template, font, Excel, `MASTER_SHEET_URL`, cartelle come `~/CDG_condiviso` o
`~/Desktop/Clienti/...`) deve stare DENTRO la cartella della skill ed essere citato con un
percorso relativo. Se sta fuori, o lo si porta dentro prima di condividere, o la voce resta
"da completare" e non parte (caso del 05/10: a Nicola la skill delle fatture non funzionava
per file mancanti sul computer dell'autore).
CLAUDE.md e memoria personale: MAI in blocco. Se contengono una regola/procedura
di team, estraila come contributo testuale con `contribuisci-conoscenza`.

### 3. Proposta (un solo messaggio)
Tabella: `# | Skill | Perché utile al team | Proposta (condividi / cita / salta / togli — doppione del plugin)`.
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
Se il `--dry-run` mostra file saltati che la skill usa davvero (font, logo, template Excel
o Word), la condivisione via Sheet arriva monca: usa lo zip di backup in
`~/Desktop/da_condividere_rbr/` e avvisa Marco, oppure togli la dipendenza.

### 5. Chiusura
✅ "Condivise N skill: <nomi>. Marco le valuta nel digest settimanale e decide se entrano nel plugin di tutti (
riceve il report su Telegram). Le skill restano in locale finché non entrano nel plugin;
quando ci sono, alla scansione successiva la copia locale passa in backup (vedi Regole)."
Se chiamata da `/rbr-setup`, riporta l'elenco per il report a Marco.

## Regole
- L'autore decide: niente condivisione senza conferma esplicita.
- Un consulente può ripetere la scansione in qualsiasi momento (`/rbr-scansione`): le
  skill già condivise vanno segnate "già nel cervello condiviso" (controlla se esiste
  `skills/<nome>` nel plugin o una riga `skill-nuova:<nome>` recente).
- Niente segreti nuovi nello Sheet: token e chiavi passano da Marco.
- **Doppione del plugin**: una skill personale che esiste anche nel plugin fa doppione e
  può essere usata al posto della versione aggiornata. Prima si confronta (diff/flag
  `doppione plugin`). Se la copia locale ha contenuti che il plugin non ha, vanno prima
  mandati con `contribuisci-conoscenza` (o come skill-nuova). Poi, con l'ok del consulente,
  la cartella si SPOSTA in `~/.claude/rbr/skill-personali-sostituite-dal-plugin-<data>/` e
  non si cancella mai. In locale restano solo le skill che il plugin non ha.
- **Skill condivisa autosufficiente**: non deve dipendere da file che stanno solo sul
  computer dell'autore. Prima di proporla, controlla che ogni percorso citato nel SKILL.md
  esista dentro la cartella (flag `file mancanti`/`file esterni` dell'inventario).
  (contributo di Andrea Chirivì, 2026-10-12; origine: Marco, decisione riunione consulenti
  del 05/10/2026, caso di Nicola)
