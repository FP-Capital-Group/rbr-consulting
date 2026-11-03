# Google Sheets/Drive — modello di accessi RBR (chi condivide cosa, come lavora Claude)

**Regola d'oro: ogni foglio su cui Claude deve leggere/scrivere va condiviso come
Editor con il service account** `fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com`.
È l'unica condivisione sempre obbligatoria. Poi, per gli umani:
- `fpcgmedia@gmail.com` → proprietario/editor dei file marketing (la proprietà resta a RBR)
- Marco (`marco.cuccaro2015@gmail.com`) → editor dove vuole visibilità

## Come funziona il service account (SA)

Il SA è un utente-robot: ha un'email ma nessuna password/login. Si autentica con la
chiave `credentials.json` (installata da `/rbr-setup` in `~/.claude/rbr/`). Flusso:
1. Lo script Python (gspread/oauth2client) firma la richiesta con la chiave
2. Google riconosce fp-cdg-service
3. L'API Sheets verifica che il SA sia Editor sul foglio → legge/scrive

Niente OAuth, niente profili browser: identico su ogni Mac, in Cowork e nelle routine
cloud. **I consulenti non hanno bisogno di alcun account Google**: l'identità la mette
il plugin.

## Trabocchetto: il SA non possiede file

Il SA non ha quota Drive: un file creato da zero dal SA finisce senza spazio. Flusso RBR:

| Operazione | Come |
|---|---|
| Nuovo foglio (CDG, KPI…) | Copia da modello posseduto da un umano (Marco/fpcgmedia); la copia eredita cartella e proprietà → il SA la compila (`files().update`/gspread) |
| Foglio del cliente | Cliente/consulente lo condivide Editor col SA — proprietà resta al cliente |
| File marketing nuovi | Creati nella cartella Drive "RBR Marketing" di fpcgmedia (condivisa col SA): proprietà fpcgmedia, mani del SA |

Nota storica: esiste anche il SA `rbr-bot` (pipeline interne Marco/Misterpizza). Per i
consulenti e il plugin vale SOLO fp-cdg-service.

## Dove NON deve stare la chiave (contributo di Andrea Chirivì, 2026-10-12)

`fp-cdg-service` è Editor su **tutti** i CDG dei clienti RBR e vede l'intero albero
Clienti RBR. Copiare `credentials.json` sull'hosting di un locale (WordPress, PHP,
cron del cliente) aprirebbe a quel server i dati di **tutti gli altri clienti**. Gli
script che scrivono su Google Sheets girano **solo sul computer del consulente o in
un ambiente RBR**. Se serve un'automazione lato cliente, usa un service account
**dedicato** con accesso solo ai fogli di quel cliente, mai `fp-cdg-service`.

## API vs MCP — quando usare cosa

- **Script + SA (via principale)**: tutto ciò che scrive celle con precisione (CDG,
  fatture, KPI). Pipeline collaudata: dry-run → conferma → write → verifica totali.
- **Connettore Google Drive MCP** (claude.ai/Cowork, OAuth umano): cercare e leggere
  ("trova il foglio economico di Barresi", PDF sul Drive). La routine del lunedì lo usa
  per il Circolo. Non adatto a scritture chirurgiche su celle.

Regola per i consulenti: **cercare/leggere → connettore Drive; scrivere numeri →
Claude col service account.** L'unica cosa da ricordare: condividere il foglio in
Editor col SA, una volta per foglio.

## Errori tipici

- "Permission denied" dallo script → il foglio NON è condiviso col SA (o è Viewer
  invece di Editor)
- File creato dal SA sparito/senza spazio → violata la regola "il SA non possiede
  file": ripartire da una copia del modello fatta da un umano
- Due caricamenti dello stesso periodo → gli importi si sommano (vedi skill
  cdg-fatture): mai ricaricare senza verificare
- **`[400] The document must not be an Office file`**: un `.xlsx` caricato su
  Drive e aperto in modalità compatibilità **non è un Google Sheet**, e l'API Sheets
  risponde 400. Si riconosce dall'ID corto nell'URL (circa 33 caratteri contro 44 di
  un vero Google Sheet) e dalla scritta ".XLSX" accanto al titolo. Rimedio: File →
  Salva come Foglio Google, poi ri-condividi in Editor col service account il file
  **nuovo** (ha un URL diverso dall'originale). (contributo di Andrea Chirivì,
  2026-10-12)
- **Il SA non può caricare un file NUOVO in My Drive**: errore 403 "Service Accounts
  do not have storage quota" (il SA può comunque leggere un file già caricato e
  verificarne dimensione e md5). Per un binario nuovo (zip di una skill, PDF, xlsx
  da conservare) carica dal **browser del consulente** (Drive → Nuovo → Caricamento
  file). Per **aggiornare** un file già condiviso usa "Gestisci versioni" /
  "Sostituisci file esistente": tiene ID, link e condivisioni esistenti e lascia la
  versione vecchia nella cronologia — ricaricarlo da zero crea invece un secondo
  file con un link diverso. Dopo il caricamento controlla dimensione e md5 contro la
  copia locale. (contributo di Andrea Chirivì, 2026-10-12; equivalente via API non
  ancora verificato su binari)
