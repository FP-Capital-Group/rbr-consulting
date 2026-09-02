---
description: Setup guidato del consulente RBR — verifica MCP, accessi e conoscenza, con checklist finale ✅/❌
---

Sei l'onboarding tecnico di un consulente RBR. Due livelli: (A) preparare il computer, sempre,
1 minuto; (B) collegare gli accessi (GoHighLevel, Google Ads, Make, fogli Google), solo se servono.
Esegui i controlli IN ORDINE e
alla fine mostra una checklist compatta ✅/🟡/❌ con il fix per ogni voce non verde.
Non fermarti al primo errore: verifica tutto, poi riepiloga.
Tutto si fa QUI, nella chat in cui sei (Cowork in sessione locale o Claude Code): non mandare
mai il consulente nel Terminale. I tool GoHighLevel, Google Ads e Make sono dichiarati nel
plugin e leggono le chiavi da `~/.claude/rbr/` tramite il ponte `scripts/mcp_bridge.py`.

## A. Prepara il computer (SEMPRE, 1 minuto): Python 3

Il plugin usa Python 3 per le regole a inizio chat, per le skill che producono file (Excel, PDF)
e per i collegamenti GHL/Google Ads/Make. `python3 --version`:
- Se HOME è `/sessions/...` (Cowork Windows / cloud): Python c'è già nell'ambiente. ✅ Niente da fare.
- Mac: se macOS propone gli "strumenti da riga di comando", il consulente clicca Installa; oppure `xcode-select --install`.
- Solo se la shell fosse davvero Windows (PowerShell, HOME `C:\Users\...`), INSTALLALO TU senza chiedere:
1. `python3 --version` → se risponde "Python 3.x": ✅ vai al punto B.
2. Se `python3` non esiste ma esiste `python --version` o `py -3 --version` (Python da python.org):
   crea l'alias `python3.exe` accanto a `python.exe`:
   `py -3 -c "import sys,shutil,os; d=os.path.dirname(sys.executable); shutil.copy(sys.executable, os.path.join(d,'python3.exe')); print(d)"`
   (se `py` manca usa `python` al posto di `py -3`). Poi `python3 --version` deve funzionare.
3. Se non c'è nessun Python: installa quello del Microsoft Store (porta con sé `python3`):
   `winget install -e --id 9NCVDN91XZQP --source msstore --accept-package-agreements --accept-source-agreements`
   Se winget/Store non è disponibile: `winget install -e --id Python.Python.3.12 --override "/quiet InstallAllUsers=0 PrependPath=1"`
   e poi crea l'alias come al punto 2. Ultima spiaggia: apri https://www.python.org/downloads/windows/
   e fai spuntare "Add python.exe to PATH".
4. Dopo l'installazione: **chiudi e riapri l'app Claude** (il PATH nuovo vale dai processi nuovi),
   poi chat nuova. Da lì Regole RBR e skill funzionano.
Percorsi su Windows: `~/.claude/rbr/` è `C:\Users\<utente>\.claude\rbr\`. Niente `base64 -d` né
`openssl`: per decodificare il file chiavi salva il base64 in un file con il tool Write e usa
`python3 -c "import base64;open(r'<dest>','wb').write(base64.b64decode(open(r'<src>').read()))"`.
La rete del sandbox (punto 2b) su Windows non si applica: salta.

## B. Servono gli accessi? (chiedi UNA volta)

Chiedi: «Ti serve lavorare sui **fogli Google dei clienti** (CDG, fatture, KPI)? E su GoHighLevel,
Google Ads o Make?»
- **Niente per ora** → fine del setup: riepiloga in 3 righe (Python ok, skill pronte, come si usa,
  "condividi quello che ho imparato") e fai il punto 7 (report a Marco).
- **Solo fogli** (il caso più frequente: consulenti CDG) → punto 0 (chiavi) e poi punto 3 (fogli).
  Salta 1, 2, 2b. È la priorità assoluta: non chiudere il setup finché il punto 3 non è ✅.
- **Anche GHL / Ads / Make** → tutti i punti.

## 0. Chiavi RBR (una volta sola — il plugin pubblico NON contiene segreti)

Controlla: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/rbr_chiavi.py"`. Se dice «chiavi in ~/.claude/rbr: sì» → ✅ vai avanti.

Altrimenti il modo consigliato, uguale su Mac, Windows e cloud, è la **Competenza personale «rbr-chiavi»**:
1. Il consulente scarica `rbr-chiavi-skill.zip` dalla cartella Drive **"RBR - Chiavi consulenti"**
   (Clienti RBR → Consulenti → Tutorial, Skill & Prompt; link: drive.google.com/drive/folders/1kaZwv-MZIVhfmuU807kw3T-BN4HiAhkN).
   Se non ha accesso alla cartella → deve chiederlo a Marco.
2. In Cowork: **Personalizza → Competenze → Aggiungi → carica lo zip**. Compare la competenza «rbr-chiavi».
3. Chat nuova. Il plugin trova il file in `~/.claude/skills/rbr-chiavi/` (Mac) o
   `~/mnt/.claude/skills/rbr-chiavi/` (Windows/cloud) e installa le chiavi da solo, a ogni avvio.
   Rilancia `/rbr-setup` per i test. Nessun altro passaggio.
Perché così: in Cowork su Windows la HOME è nuova a ogni chat e tutto ciò che si salva lì sparisce;
le competenze personali invece vengono montate in ogni sessione. Non serve nessuna organizzazione.

Alternative (solo se il consulente non può caricare competenze):
- HOME `/sessions/...`: metti `rbr-chiavi.json` nella cartella di lavoro data a Cowork (`~/mnt/<cartella>/`),
  scaricandolo via connettore Drive (`search_files` title = 'rbr-chiavi.json' → `download_file_content` →
  salva il base64 con il tool Write → `python3 -c "import base64,sys;open(sys.argv[2],'wb').write(base64.b64decode(open(sys.argv[1]).read()))" <tmp> <dest>`).
- Mac: `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/installa_chiavi.py" ~/Downloads/rbr-chiavi.json` (persiste in `~/.claude/rbr/`).
Poi: i tool GHL/Google Ads/Make valgono dalla PROSSIMA chat; al primo avvio Cowork chiede di consentire i server MCP del plugin: sì.

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

## 3. Fogli Google dei clienti (PRIORITÀ: qui il consulente deve entrare per forza)

Esegui `python3 "${CLAUDE_PLUGIN_ROOT}/scripts/prepara_fogli.py"`: installa da solo le librerie che
mancano (gspread, google-auth, pandas, openpyxl), verifica le chiavi e fa una LETTURA REALE dello
Sheet "RBR - Contributi conoscenza". Deve finire con ✅. Se il consulente ha già un foglio cliente
su cui lavorare, rilancialo con `--test-url <link del foglio>`: se dice 403, il foglio va condiviso
come Editor con `fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com` (fallo fare subito, poi ripeti).
Esiti tipici: ❌ manca credentials.json → punto 0 non completato; ❌ 403 blocked-by-allowlist →
chat nuova (rete del sandbox, solo Mac); ❌ pip fallisce → mostra il comando suggerito dallo script.
Chiudi il punto ripetendo la regola: ogni foglio cliente va condiviso come Editor con il service account.

## 4. Skill e regole

- Verifica che le skill del plugin siano visibili (elenca 5-6 skill `rbr-consulting` a titolo di prova).
- Le "Regole RBR" devono comparire nel contesto di sessione (se leggi questo comando dal plugin, sì).

## 5. Checklist finale

Mostra la tabella:

| Componente | Stato | Fix |
|---|---|---|
| chiavi RBR (~/.claude/rbr) | | |
| meta-ads | ✅/❌ | … |
| google-ads | | |
| make | | |
| ghl2-* | | |
| service account Google | | |
| skill plugin | | |

## 6. Presentazione (solo al PRIMO setup di questo consulente)

Chiedi, in un solo messaggio: nome e cognome, di cosa si occupa in RBR (CDG, marketing, HR…).
Poi digli in due righe: «Quando scopri una procedura o un trucco utile al team, dimmi "condividi
quello che ho imparato": lo segnalo a Marco. Se hai skill tue che vorresti dare al team: `/rbr-scansione`.»
NON lanciare la scansione delle skill da solo: solo se il consulente la chiede.

## 7. Report a Marco su Telegram (SEMPRE, alla fine del setup)

Componi un messaggio in TESTO SEMPLICE (no Markdown), max 12 righe:
`👤 Nuovo setup plugin RBR — <nome consulente> (<data>)`
poi: esito checklist in una riga per componente solo se ❌/🟡 (i ✅ riassumili in
"tutto il resto ok"), ruolo del consulente. Invia con Bash:
leggi `bot_token` e `chat_id_marco` da `~/.claude/rbr/config.json` (chiave `telegram`) e:
`curl -s -X POST "https://api.telegram.org/bot$TOKEN/sendMessage" -d chat_id=$CHAT --data-urlencode text="<messaggio>"`
Verifica `"ok":true` (un retry se fallisce; se fallisce ancora, di' al consulente di
avvisare Marco a voce). Questo messaggio arriva a Marco: scrivilo per lui, non per il consulente.

Chiudi col consulente: cosa può già fare oggi e a chi chiedere per gli accessi
mancanti (Marco per GHL/Meta/accessi).
