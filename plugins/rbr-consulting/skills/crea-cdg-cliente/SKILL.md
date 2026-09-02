---
name: crea-cdg-cliente
description: Crea il conto economico (File 01 CDG) di un nuovo cliente RBR dal modello standard, mono-store o multi-store. Usala quando devi "creare il CDG di un cliente nuovo", "impostare il conto economico", "duplicare il modello CDG", "fare il CDG raggruppato / aggregato a 2-3-4 store", "aggiungere uno store al CDG". Copre: scelta del modello giusto, copia e condivisione, bug noti del template da correggere, struttura righe/colonne, verifica di quadratura. NON compilare mai i dati senza aver prima riconciliato con la skill `riconciliazione-dati-cliente`.
---

# Crea CDG cliente (File 01 — Conto Economico)

## Perché esiste
Il **01 CDG** è il cuore del controllo di gestione RBR: RICAVI → Costi variabili → MDC → PMV → Costi fissi → EBITDA, mensile su più anni. I template hanno bug ricorrenti (zeri digitati al posto delle formule, % con denominatore fisso, trimestri sbagliati) che se non corretti inquinano tutti gli anni dal 2026 in poi. E ogni numero scritto in un CDG viene usato dal ristoratore per decidere: **prima riconciliazione, poi compilazione** — sempre.

## Quando usarla
- Onboarding cliente nuovo: serve il conto economico da modello.
- Cliente multi-punto-vendita: serve il CDG raggruppato (aggregato + tab per store).
- Aggiungere uno store a un CDG raggruppato esistente.

## Prerequisiti
- **Dati riconciliati** con la skill `riconciliazione-dati-cliente` (panoramica discussa, decisioni di mapping chiuse). Senza questo passaggio NON si compila.
- Il foglio del cliente condiviso come **Editor** con il service account **`fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com`** (Condividi → Editor). I service account non hanno quota Drive: non possono creare né copiare file, solo leggere/scrivere quelli condivisi.
- Per il caricamento fatture AdE nel CDG: skill `cdg-fatture` (pipeline CSV/XML → FATTURE.xlsx → Economico, con dry-run).

## Quale modello usare

| Caso | Modello | ID |
|---|---|---|
| Mono-store (standard) | Template `01 CDG` in cartella `_TEMPLATE` | `1TWimq1XprSPbO_GI47SMJUbxVH7_IZx1onG5bne-3J4` |
| Mono-store 2025-2030 (nuovo, stile Luna Blu) | Modello single-store "pulito" (tab: Scopo & Tutorial, Fatturato, Economico, Finanziario, Saldo debiti) | es. applicato: `1YGVUjwx92-ZxcSUGh2_V53NcwYIU3crc55VzubZtX0M` (Luna Blu) |
| 2 store | `01 CDG RAGGRUPPATO 2 STORE 2025-2030 - GIUGNO26` | `175ngbrIBccyD8JoLx63A1L7UoWumi3wQzAMjN1ZpD08` |
| 3 store | `01 CDG RAGGRUPPATO 3 STORE 2025-2030 - GIUGNO26` | `1z5K5ycVfJMCJiSVTtQwE6DcUTzavJfIs7zFR3uXrewQ` |
| 4 store | `01 CDG RAGGRUPPATO 4 STORE 2025-2030 - GIUGNO26` | `1hrVUV4FtFKEaACcuBUWjhCZ4zlsVZ132qt9BVdxCKV8` |

I modelli raggruppati stanno nella cartella Drive **Modelli RBR** (`1xLo0qrFQ_UE2kTbjeTviCu4Byer6ORbt`). Riferimento di stile multi-store: `001 CDG CARTABIANCA` (`1TrWa-8hZ6_MyJYafpuppQHY_KnQoWHvYGyjsdSWa3Ko`, 13 store). Esiste anche il flusso dal modello **NO G NO B** (`1rSESvO5K5L17cFC4c3dmPmP9LViVYawVRvAboCAudBo`, usato per WebApp SRL) — vedi "Flusso NO G NO B" in fondo.

## Procedura

### 1. Copia il modello
La copia va fatta **dal browser del proprietario** (File → Crea una copia) spuntando **"Condividilo con le stesse persone"** — altrimenti il service account perde l'accesso e non si lavora più via API. In alternativa un connettore Drive OAuth (`copy_file`), ma ⚠️ la copia via API fa perdere al service account la scrittura (i permessi diretti non si ereditano): dopo la copia va **ricondiviso come Editor** con `fp-cdg-service@…`. Nota: i modelli raggruppati hanno un **Apps Script allegato** ("Gestione righe") che si copia insieme al foglio.
L'unico check affidabile dell'accesso in scrittura è un **write test** (update di una cella scratch, poi ripulita).

### 2. Rinomina e intesta
- Nome file: `01 CDG <CLIENTE> 2025-2030`.
- `A1` del tab Economico: dal placeholder (`Pinocchio` nei modelli) al nome cliente/store.
- Multi-store: rinomina i tab con i nomi reali dei locali (es. "Economico Sole", "Economico Cimatori"). ⚠️ Le intestazioni store della riga 1 dell'Aggregato sono **testo statico**: se rinomini gli store aggiorna anche la riga 1.

### 3. Correggi i bug noti del template (verificati su più copie)
1. **riga 2 RICAVI**: celle mese con `0` digitato al posto di `=somma righe 3:6` → senza fix il CE resta a 0.
2. **righe 29-80**: % con denominatore fisso `$B$2`/`$AB$2` → percentuali sbagliate dal 2026 al 2030; ripuntare alla colonna propria.
3. **riga 18 MOL, cella dic-26** (`AZ18`): costante invece della formula.
4. **Trimestri (righe 353-367)**: T2/T3/T4 come finestre mobili di 3 mesi → trimestri veri; denominatori % righe 361/363 uniformati; % fantasma negli slot mese 5-12 rimosse.
5. **Tabelle di Sheets sui tab Economico**: errore "nome colonna duplicato" su centinaia di colonne → rimuovere la Tabella SOLO dalla UI con **"Ripristina i dati non formattati"** dal menu del chip Tabella. ⛔ **Mai `deleteTable` via API né "Elimina tabella" dal menu: cancellano anche i dati** (verificato). Nessun impatto visivo.
6. Tab Fatturato: `#REF!` sulle % del primo anno → `0`; colonna UTILE = `=Economico!<mese>16` (EBITDA).

Lo script `shared/scripts/cdg_aggregato/build*.py` (`compute_fixes`) corregge i bug 1-4 in automatico sul multi-store — vedi il README nella stessa cartella per la tabella completa.

**Aggiungere righe dentro un blocco con rollup** (es. mono-store GIUGNO26, blocco FORNITORI righe 270-327 con rollup `=SUM(D270:D327)` a riga 269, ma la tecnica vale per qualunque blocco a `SUM` fisso): se manca spazio, inserisci le righe **dentro** il range con `insertDimension` prima dell'ultima riga vuota del blocco (es. `startIndex=326, inheritFromBefore=true`) così i `SUM` si espandono da soli, poi `copyPaste` con `PASTE_FORMULA` di una riga esistente del blocco (es. r270, colonne B:FA) sulle righe nuove per riportare formule di totale riga e percentuali. Verifica dopo: rollup espanso e dry-run pulito. *(contributo di Marco Cuccaro, 2026-08-27)*

### 4. Conosci la struttura (righe/colonne)
**Mono-store nuovo (Economico, righe 1-367):** r2 RICAVI (=somma 3:6, dettaglio da etichettare) · r7 Costi variabili (r8 inventario iniziale, r9 Acquisti = r268 TOT FORNITORI, r10 inventario finale) · r11 MDC · r12 PMV (Personale-Mkt-Vendite) · r13 MOD · r14 Costi fissi · r16 EBITDA · r18-21 MOL attuale/anno prec./differenza + Da fatturare FP (= MOL diff/2) · r24-80 dettaglio personale/marketing/delivery · r353-367 comparazione trimestri. Colonne per anno: `TOTALE | % | 12 × (mese, %)` — 2025: B(TOT)+D,F,…,Z; 2026: AB(TOT)+AD,…,AZ. 6 anni 2025→2030.
**Multi-store (Economico Aggregato):** per periodo un blocco `TOTALE | % | STORE 1 | % | STORE 2 | % …` = `2 + 2×N` colonne; colonne totali = `1 + 13 × blocco × 6 anni` (2 store = 469 col, 3 = 625, 4 = 781). Colonne store = riferimento diretto al tab store; % store = calcolate sui ricavi del *singolo* store. Gruppi colonne a 2 livelli, chiusi di default. I tab **Fatturato** (Aggregato + per store) si auto-alimentano: `FATTURATO` = r2 Economico, `UTILE` = r16 EBITDA, YoY dal 2° anno, progressivo azzerato a gennaio.

### 5. Compila (SOLO dopo riconciliazione)
- Per le fatture passive AdE usa la skill **`cdg-fatture`**: prima **dry-run** (`carica_google_sheet.py FATTURE.xlsx "<url>"`), riepilogo all'utente, poi `--write` solo su conferma esplicita. Multi-store: un FATTURE.xlsx per store con `--sheet "Economico <Store>"`, **mai scrivere sulla tab Aggregato** (è solo formule).
- **Regola IVA**: ricavi scritti come **formula visibile `=lordo/1,1`** nelle celle (scorporo IVA 10% a vista); costi = imponibile SDI (già IVA esclusa, nessuno scorporo); il Finanziario (se mai si farà) = IVA inclusa.
- Locale it_IT dei fogli: formule via API con separatore `;` e decimali con virgola (per lo scorporo via API usare `*10/11`, con `1.1` → #ERROR).

### 6. Verifica di quadratura
- **EBITDA del CDG = totale indipendente del sorgente al centesimo, mese per mese** (es. a soli costi caricati: EBITDA = −costi esatto). Se non torna, c'è un errore da trovare, non da arrotondare.
- Multi-store: `verify3.py`/`verify4.py` iniettano dati di test, controllano `TOTALE = somma store`, % e tab Fatturato, e ripristinano gli zeri.
- `#DIV/0!` a modello vuoto: **si lasciano** (decisione Marco), spariscono coi dati.

### 7. Consegna
Condividi come Editor con `fp-cdg-service@…` (se non già fatto) e registra il file nel **Registry Clienti** (`1_iBuD5T7ECeS0-QD9pKYPgJtHWlMbwGFi84yryteJck`, colonna `file_01_cdg_id`).

## Aggiungere uno store a un CDG raggruppato esistente
Procedura completa nel README di `shared/scripts/cdg_aggregato/`: duplicateSheet dei tab Economico/Fatturato dell'ultimo store, inserimento di 2 colonne per periodo nell'Aggregato (da destra a sinistra, dentro il gruppo store), copyPaste dei formati, riscrittura griglia con `build_grid`, verifica.
⚠️ **Gotcha colonna A**: `build_grid` NON produce la colonna A (etichette voci). Scrivere la griglia da A1 le **cancella**: scrivere sempre **da B in poi**. La colonna A non dipende dal numero di store (ripristinabile da `Economico Aggregato!A1:A367` di un modello sano).

## Flusso NO G NO B (modello vecchio, xlsx via openpyxl)
Per il template NO G NO B (WebApp SRL, Cartabianca, RedMike) la pipeline è diversa: copia col connettore → download in .xlsx → trasformazione **openpyxl preservando la struttura completa** (categorie → sotto-categorie → voci-foglia, formule di rollup, gruppi collassabili — MAI svuotare la struttura di dettaglio lasciando solo la macro) → condivisione col SA → iniezione `drive.files().update(media=xlsx)` → **polling anti-race** (leggere una cella nota finché riflette il nuovo contenuto) prima di ogni edit live → rifiniture via Sheets API targettizzando il foglio **per sheetId** (non `sheets[0]`). Le voci-foglia del modello sono spesso **formule** (es. `=33148/1.22`), non numeri: la pulizia deve svuotare le celle mensili formule incluse, tenendo i subtotali. Ogni voce sorgente → UNA foglia (copertura completa = riconciliazione esatta). Dettagli: `RBR AI/memory/flusso_conto_economico_da_modello.md` + `cliente_webapp_srl.md`.

## Regole RBR & trabocchetti
- ⛔ **MAI compilare senza riconciliazione preventiva** (skill `riconciliazione-dati-cliente`).
- ⛔ **Il foglio Finanziario NON si tocca** (regola Marco; la sua Tabella di Sheets resta).
- ⛔ Mai eliminare righe dai tab store di un raggruppato: l'Aggregato referenzia **per riga fissa** → le righe si **nascondono**, non si eliminano (c'è l'Apps Script "🧰 Gestione righe" nei file che lo hanno: compatta/aggiungi/mostra).
- ⚠️ Il loader fatture **somma** sulle celle: non ricaricare due volte lo stesso periodo.
- ⚠️ Mai sovrascrivere dati o gruppi/outline sistemati a mano dal cliente o da Marco: se il file è stato editato a mano, solo edit live puntuali, mai re-iniezione dell'xlsx.
- ⚠️ Rate limit Sheets 60 read/min: un solo `values.batchGet`, niente loop di get singoli.
- ⚠️ Investimenti/una tantum fuori gestione: riga dedicata **sotto l'EBITDA**, non inclusa nei rollup (pattern Raices r17 "Investimenti (fuori gestione)").
- ⚠️ **Mono-store GIUGNO26 — commissioni POS preimpostate**: in Gestione finanziaria (riga 257) la voce "Commissioni POS" ha già una formula attiva `=ricavi_mese*0,0068`. Va bene lasciarla come stima, ma ricordarsene in fase di quadratura: EBITDA atteso = ricavi netti − costi caricati − 0,68% dei ricavi. Senza tenerne conto la verifica al centesimo sembra sballata di ~0,7% dei ricavi ogni mese. *(contributo di Marco Cuccaro, 2026-08-27)*

## Lacune note (da completare con Marco)
- L'ID di un modello mono-store 2025-2030 "master" da duplicare non è documentato nelle memory: è documentato il template `01 CDG` in `_TEMPLATE` e i casi applicati (Luna Blu). Chiedere a Marco quale usare come sorgente per i nuovi mono-store.
- Le memory interne usano il service account `rbr-bot@rbr-ai.iam.gserviceaccount.com` (infrastruttura di Marco); per i consulenti col plugin vale `fp-cdg-service@…` come sopra.

## Definition of Done
- [ ] Modello giusto (mono/N store) copiato con permessi preservati, write test del SA ok
- [ ] Bug template corretti (r2, %, MOL, trimestri, Tabelle rimosse via UI)
- [ ] A1/nomi tab/riga 1 intestati al cliente
- [ ] Dati caricati solo dopo riconciliazione, con dry-run prima della scrittura
- [ ] EBITDA riconciliato al centesimo contro un totale indipendente, mese per mese
- [ ] Ricavi con formula `=lordo/1,1` a vista; costi a imponibile; Finanziario intatto
- [ ] File nel Registry Clienti, condiviso Editor con il service account

## ID dei modelli ufficiali su Drive (rilevati 2026-08-11, accesso via service account)

Cartella modelli: `FPCG Cartella modello` → `Modelli RBR` (`1xLo0qrFQ_UE2kTbjeTviCu4Byer6ORbt`):

| Modello | ID Drive |
|---|---|
| 01 CDG RAGGRUPPATO 2025-2030 (mono-store, GIUGNO26) | `182qhB_3CH95w6iaI84gbbLyXNiIM9FA11M8RrzAKkW0` |
| 01 CDG RAGGRUPPATO 2 STORE 2025-2030 | `175ngbrIBccyD8JoLx63A1L7UoWumi3wQzAMjN1ZpD08` |
| 01 CDG RAGGRUPPATO 3 STORE 2025-2030 | `1z5K5ycVfJMCJiSVTtQwE6DcUTzavJfIs7zFR3uXrewQ` |
| 01 CDG RAGGRUPPATO 4 STORE 2025-2030 | `1hrVUV4FtFKEaACcuBUWjhCZ4zlsVZ132qt9BVdxCKV8` |
| 03 Analisi Economica - Modello | `1KDHEp-REQNYNsCI4ojFwccm1uRPVfsdSWaI-12UIM_A` |
| 02 Food Cost - Modello (xlsx) | `1lqruldWnTR-liXy5xDZtow5dgYHJRNkG` |

Il service account vede l'intero albero **Clienti RBR** (`1SV6ldqSJ2SzZdYXTrzjM8oim52vr0RQN`,
una cartella per cliente): la copia del modello va fatta con `files().copy` direttamente
nella cartella del cliente (il SA non può possedere file fuori dalle cartelle condivise).
