---
description: Setup guidato del consulente RBR — verifica MCP, accessi e conoscenza, con checklist finale ✅/❌
---

Sei l'onboarding tecnico di un consulente RBR. Esegui questi controlli IN ORDINE e
alla fine mostra una checklist compatta ✅/🟡/❌ con il fix per ogni voce non verde.
Non fermarti al primo errore: verifica tutto, poi riepiloga.
Tutto si fa QUI, nella chat in cui sei (Cowork in sessione locale o Claude Code): non mandare
mai il consulente nel Terminale. I tool GoHighLevel, Google Ads e Make sono dichiarati nel
plugin e leggono le chiavi da `~/.claude/rbr/` tramite il ponte `scripts/mcp_bridge.py`.

## 0. Chiavi RBR (una volta sola — il plugin pubblico NON contiene segreti)

Controlla se esiste `~/.claude/rbr/credentials.json`. Se manca, procurati `rbr-chiavi.json`
— **prima in automatico, senza far scaricare nulla al consulente**:
1. **Via connettore Google Drive** (il consulente lo ha quasi sempre collegato in Claude):
   `search_files` con query `title = 'rbr-chiavi.json'` → prendi l'`id` → `download_file_content`
   (torna il JSON in base64) → salvalo con Bash:
   `echo '<base64>' | base64 -d > ~/Downloads/rbr-chiavi.json` (poi verifica con
   `python3 -c "import json;json.load(open('$HOME/Downloads/rbr-chiavi.json'))"`).
   Il file sta nella cartella Drive **"RBR - Chiavi consulenti"** (Clienti RBR → Consulenti →
   Tutorial, Skill & Prompt, già condivisa col team). Se `search_files` non lo trova: il
   consulente non ha accesso all'albero Clienti RBR → chiederlo a Marco.
2. **Fallback manuale** (solo se il connettore Drive non è disponibile): chiedi al consulente
   di scaricare il file da drive.google.com/drive/folders/1kaZwv-MZIVhfmuU807kw3T-BN4HiAhkN
   in `~/Downloads/`.
3. Esegui: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/installa_chiavi.py" ~/Downloads/rbr-chiavi.json`
   (prima con `--dry-run` per mostrare cosa farà). Installa: service account Google,
   token Telegram, chiavi dei server MCP GHL/Google Ads/Make (`~/.claude/rbr/mcp_servers.json`,
   lette dal ponte del plugin), allowlist rete, marketplace con auto-update. Poi cancella
   `~/Downloads/rbr-chiavi.json` (le chiavi sono in ~/.claude/rbr/).
4. Avvisa: i tool GHL/Google Ads/Make e la rete valgono dalla PROSSIMA chat. Se stai facendo
   il primo setup, chiedi di aprire una chat nuova e rilanciare `/rbr-setup` per i test dei
   punti 1-3. In Cowork, alla prima chat dopo il setup compare la richiesta di consentire i
   server MCP del plugin: va accettata.
Se `~/.claude/rbr/credentials.json` esiste ma manca `~/.claude/rbr/mcp_servers.json` (setup
fatto con una versione precedente alla 2.8.0): riesegui il punto 3 (ri-scarica le chiavi e
rilancia `installa_chiavi.py`), poi chat nuova.
Se entrambi esistono: ✅ e vai avanti.

## 1. MCP del plugin (tutti dichiarati nel plugin: nessuna configurazione a mano)

I tool si chiamano `mcp__plugin_rbr-consulting_<server>__…` (usa ToolSearch se non sono
caricati). Per ciascuno fai una chiamata reale di test:
- **meta-ads** → prova a listare gli ad account. Se chiede login: guida l'utente
  nell'OAuth Facebook (deve usare l'utenza aggiunta al Business Manager RBR — accesso: Marco).
- **google-ads** → `list_google_ads_customers`. Token dell'account RBR (pipeboard): se
  fallisce con errore di token, segnala a Marco.
- **make** → `users_me`.
- **ghl2-<cliente>** → `search_operations` su ghl2-democliente, poi `describe_operation` +
  `execute_operation` di `get-location` (deve rispondere `success: true`).
Se google-ads/make/ghl2 NON compaiono o falliscono con "chiavi RBR non installate": il ponte
non trova `~/.claude/rbr/mcp_servers.json` → punto 0, poi chat nuova. Se la chat è stata
aperta prima del setup: basta una chat nuova.

## 2. Cliente GHL mancante

Le istanze `ghl2-<cliente>` sono quelle dichiarate nel plugin (una riga nel `.mcp.json`) con la
chiave in `rbr-chiavi.json`. Se un cliente che il consulente segue non c'è: chiederlo a Marco,
che aggiunge il locationId alle chiavi (il PIT agency è unico) e la riga nel plugin (release
automatica del lunedì o immediata). Poi il consulente rilancia `/rbr-setup` (punto 0,
ri-scarica le chiavi) e, arrivato l'aggiornamento, apre una chat nuova.

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
  `~/Desktop`, `~/Documents`, `~/dev`). Se manca: `git clone https://github.com/FP-Capital-Group/rbr-suite.git`
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
  - stampa ma con un ⚠️ "plugin vX installato, disponibile vY" → ✅ attiva; l'auto-update
    lo porterà alla versione nuova al prossimo riavvio (se non succede: `/plugin update rbr-consulting`).
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
