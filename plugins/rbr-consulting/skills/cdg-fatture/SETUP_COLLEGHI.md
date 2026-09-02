# CDG Fatture — Setup per i colleghi

> ℹ️ Da agosto 2026 questa skill si installa col **plugin `rbr-consulting`**
> (vedi `ONBOARDING.md` nel repo `rbr-suite`): niente più copie manuali di cartelle.
> Qui restano solo i prerequisiti specifici.

## Cosa fa
1. Unisce i CSV del periodo (export Agenzia delle Entrate) in un unico file
2. Genera `FATTURE.xlsx` (pulizia dati, note di credito in negativo, categorie automatiche)
3. Cerca online e categorizza i fornitori nuovi (lo fa Claude, con tua conferma)
4. Carica i dati sul foglio Google "Economico" del cliente, sommando nelle celle giuste

Il **database fornitori→categoria** è un Google Sheet condiviso: ogni collega legge/scrive
lo stesso foglio in tempo reale via API — anche lavorando in parallelo su clienti diversi
non ci si sovrascrive a vicenda.

## Prerequisiti (una volta sola)

1. **Librerie Python**:
   `pip3 install pandas openpyxl gspread oauth2client`
   Solo per clienti multi-punto-vendita con XML: `brew install openssl poppler`
   (openssl per le fatture firmate .p7m, poppler per i PDF allegati alle fatture).
2. **Service account**: `credentials.json` viene installato da `/rbr-setup` in `~/.claude/rbr/` — tieni il
   plugin/repo **privato**: è una chiave d'accesso.
3. **Per ogni cliente**, condividi il suo foglio "Economico" in **Editor** con:
   `fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com`
4. (Opzionale) Per correggere il master fornitori a mano da browser, fatti condividere
   il Google Sheet master in Editor sul tuo account (chiedi a chi lo gestisce).

## Uso quotidiano
1. Metti i CSV del periodo in una cartella di lavoro qualsiasi.
2. Apri Claude Code in quella cartella e scrivi: *"carica queste fatture sul foglio del
   cliente"* (incolla l'URL quando te lo chiede).
3. Claude mostra prima un'anteprima (dry-run), poi — alla tua conferma — scrive e
   verifica che i totali quadrino.

## Regole d'oro
- **Non caricare due volte lo stesso periodo**: gli importi si SOMMANO → raddoppierebbero.
- I fornitori nuovi vengono categorizzati e salvati nel database condiviso: aiuta tutti.
- In dubbio, fermati al dry-run e controlla l'anteprima prima di scrivere.
