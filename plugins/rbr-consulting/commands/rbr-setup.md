---
description: Setup guidato del consulente RBR — verifica MCP, accessi e conoscenza, con checklist finale ✅/❌
---

Sei l'onboarding tecnico di un consulente RBR. Esegui questi controlli IN ORDINE e
alla fine mostra una checklist compatta ✅/🟡/❌ con il fix per ogni voce non verde.
Non fermarti al primo errore: verifica tutto, poi riepiloga.

## 0. Chiavi RBR (una volta sola — il plugin pubblico NON contiene segreti)

Controlla se esiste `~/.claude/rbr/credentials.json`. Se manca:
1. Chiedi al consulente di scaricare `rbr-chiavi.json` dalla cartella Drive **"RBR - Chiavi consulenti"** (Clienti RBR → Consulenti → Tutorial, Skill & Prompt, già condivisa col team: drive.google.com/drive/folders/1kaZwv-MZIVhfmuU807kw3T-BN4HiAhkN). Di solito finisce in `~/Downloads/rbr-chiavi.json`.
   Se il consulente ha il connettore Google Drive attivo, puoi cercare tu il file
   (`search_files` title = 'rbr-chiavi.json') e leggerlo, salvandolo in ~/Downloads.
2. Esegui: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/installa_chiavi.py" ~/Downloads/rbr-chiavi.json`
   (prima con `--dry-run` per mostrare cosa farà). Installa: service account Google,
   token Telegram, server MCP GHL/Google Ads/Make a scope utente, allowlist rete, marketplace
   con auto-update. Poi il consulente può cancellare il file scaricato.
3. Avvisa: MCP e rete valgono dalla PROSSIMA chat. Se stai facendo il primo setup,
   chiedi di aprire una chat nuova e rilanciare `/rbr-setup` per i test dei punti 1-3.
Se `~/.claude/rbr/credentials.json` esiste già: ✅ e vai avanti.

## 1. MCP del plugin (installati automaticamente con il plugin)

Per ciascuno fai una chiamata reale di test (usa ToolSearch se i tool non sono caricati):
- **meta-ads** → prova a listare gli ad account. Se chiede login: guida l'utente
  nell'OAuth Facebook (deve usare l'utenza aggiunta al Business Manager RBR — accesso: Marco).
- **google-ads** → `list_google_ads_customers`. Il token è quello dell'account RBR
  (pipeboard) già configurato nel plugin: se fallisce, segnala a Marco.
- **make** → `users_me`.

## 2. GoHighLevel (`ghl2-<cliente>`)

Le istanze GHL sono registrate a scope utente dal punto 0 (`~/.claude.json`, non nel plugin):
1. Verifica che esistano i tool `ghl2-*` (ToolSearch "ghl2") e fai una chiamata di
   prova su un'istanza (es. `search_operations` su ghl2-democliente).
2. Se un cliente che il consulente segue NON ha l'istanza: serve un PIT per quella
   sub-location → chiederlo a Marco, che aggiorna `rbr-chiavi.json` (basta il locationId,
   il PIT agency è unico) e il consulente rilancia `installa_chiavi.py`.

## 2b. Rete del sandbox (la sistema già il punto 0)

`installa_chiavi.py` aggiunge i domini all'allowlist (`sandbox.network.allowedDomains` in
`~/.claude/settings.json`). Verifica solo che ci siano (errore tipico se manca: `403
blocked-by-allowlist` su oauth2.googleapis.com); se manca qualcosa rilancia lo script.

Vale dalle SESSIONI NUOVE: avvisa l'utente che dopo il setup deve aprire una chat
nuova perché Google/Telegram funzionino. Verifica anche il toggle Cowork
"Esegui nuove attività nel cloud" = OFF (chiedi all'utente: Impostazioni → Cowork).

## 3. Google (Sheets/Drive via service account)

- Verifica che esista `~/.claude/rbr/credentials.json` (installata al punto 0) e la skill `cdg-fatture`.
- Ricorda la regola: ogni foglio cliente va condiviso in Editor con
  `fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com`.
- Verifica dipendenze Python: `pip3 show pandas openpyxl gspread oauth2client` (installa se mancano, chiedendo prima).

## 4. Repo suite (conoscenza)

- Controlla se `rbr-suite` è clonato in locale (chiedi il percorso se non lo trovi in
  `~/Desktop`, `~/Documents`, `~/dev`). Se manca: `git clone https://github.com/marcocuccaro0309/rbr-suite.git`
  (serve accesso al repo privato → Marco).
- Se presente: `git pull` per allinearla.

## 5. Conoscenza e regole

- Verifica che le skill del plugin siano visibili (elenca quelle `rbr-consulting`).
- Verifica che l'hook regole sia attivo (le "Regole RBR" devono comparire nel contesto di sessione — se leggi questo comando dal plugin, molto probabilmente sì).
- **Conoscenza live — prova visibile per il consulente**: esegui
  `python3 "${CLAUDE_PLUGIN_ROOT}/hooks/conoscenza_live.py"` e MOSTRA in chat le prime
  3-4 righe di novità che stampa (con la data di aggiornamento). Serve a far vedere al
  consulente, nero su bianco, che il cervello condiviso è collegato: quel blocco di solito
  finisce solo nel contesto di Claude a inizio sessione, non a schermo. Esiti:
  - stampa le righe con la data di oggi/recente → ✅ Conoscenza live attiva.
  - stampa ma con un ⚠️ "plugin vX installato, disponibile vY" → ✅ attiva, ma segnala al
    consulente di aggiornare lo zip (cartella Drive versioni).
  - non stampa nulla o errore rete → 🟡 rete sandbox non ancora sistemata (vedi punto 2b):
    dopo il fix funzionerà dalla prossima sessione. Non è bloccante.

## 6. Checklist finale

Mostra la tabella:

| Componente | Stato | Fix |
|---|---|---|
| chiavi RBR (~/.claude/rbr) | | |
| meta-ads | ✅/❌ | … |
| google-ads | | |
| make | | |
| ghl2-* | | |
| service account Google | | |
| repo rbr-suite | | |
| skill plugin | | |
| Conoscenza live (hook) | | |

## 7. Presentazione e scansione delle skill (solo al PRIMO setup di questo consulente)

1. Chiedi al consulente, in un solo messaggio: nome e cognome, di cosa si occupa in RBR
   (CDG, marketing, HR…), da quanto lavora coi metodi RBR.
2. **Scansione skill** (skill `scansione-skill`, obbligatoria al primo setup): lancia
   `python3 "${CLAUDE_PLUGIN_ROOT}/skills/scansione-skill/scripts/scansiona_skill.py" --json /tmp/inventario_skill.json`,
   classifica le voci (utili al team / personali / pubbliche), proponi in tabella cosa
   condividere e aspetta la conferma 🟡. Le confermate partono con `condividi_skill.py`
   (prima `--dry-run`). CLAUDE.md e memoria personale MAI in blocco: solo regole di
   team estratte come contributi testuali.
3. Chiedi: "Hai metodi, procedure o trucchi che usi già e che il team dovrebbe avere,
   anche non scritti in una skill? Raccontameli, li strutturo io." Per OGNI cosa utile
   usa `contribuisci-conoscenza` (una riga per concetto, autore = il consulente).
4. Se il consulente ha fretta: registra solo nome e ruolo e ricordagli `/rbr-scansione`
   e "condividi quello che ho imparato" per farlo dopo.

## 8. Report a Marco su Telegram (SEMPRE, alla fine del setup)

Componi un messaggio in TESTO SEMPLICE (no Markdown), max 12 righe:
`👤 Nuovo setup plugin RBR — <nome consulente> (<data>)`
poi: esito checklist in una riga per componente solo se ❌/🟡 (i ✅ riassumili in
"tutto il resto ok"), ruolo del consulente, le skill condivise dalla scansione (nomi) e
l'elenco dei contributi testuali raccolti al punto 7 (titoli) o "nessun contributo per ora". Invia con Bash:
leggi `bot_token` e `chat_id_marco` da `~/.claude/rbr/config.json` (chiave `telegram`) e:
`curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" -d chat_id=$CHAT --data-urlencode text="<messaggio>"`
Verifica `"ok":true` (un retry se fallisce; se fallisce ancora, di' al consulente di
avvisare Marco a voce). Questo messaggio arriva a Marco: scrivilo per lui, non per il consulente.

Chiudi col consulente: cosa può già fare oggi e a chi chiedere per gli accessi
mancanti (Marco per GHL/Meta/accessi).
