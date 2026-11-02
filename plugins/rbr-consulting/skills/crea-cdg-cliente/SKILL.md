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
2. **Denominatore fisso nelle %, righe 29-367**: il bug non si ferma a 29-80. Il denominatore fisso `$B$2` colpisce **tutte** le colonne % dei blocchi 2026-2030, righe 29-367 (fino a ~3.120 celle su una copia mono-store fresca). Fix: leggi le FORMULE (`valueRenderOption=FORMULA`), e con una regex trasforma ogni `=Xn/$B$2` con colonna X≠B in `=Xn/$X$2` (come fa già il blocco 2025), poi un solo `batchUpdate`. **I difetti variano da copia a copia** — su alcune il bug degli zeri in riga 2 non c'è, mentre compaiono `#REF!` o celle UTILE a 0 non previste: non applicare la lista alla cieca, fai sempre uno scan completo delle formule prima di correggere.
3. **riga 18 MOL, cella dic-26** (`AZ18`): costante invece della formula.
4. **Trimestri (righe 353-367)**: T2/T3/T4 come finestre mobili di 3 mesi → trimestri veri; denominatori % righe 361/363 uniformati; % fantasma negli slot mese 5-12 rimosse.
5. **Tabelle di Sheets sui tab Economico**: errore "nome colonna duplicato" su centinaia di colonne → rimuovere la Tabella SOLO dalla UI con **"Ripristina i dati non formattati"** dal menu del chip Tabella. ⛔ **Mai `deleteTable` via API né "Elimina tabella" dal menu: cancellano anche i dati** (verificato). Nessun impatto visivo.
6. Tab Fatturato: `#REF!` sulle % del primo anno → `0`; colonna UTILE = `=Economico!<mese>16` (EBITDA).
7. **riga 38 contributi, formula `=(SUM(D25:D36)*1,6*14*0,0741)-SUM(D25:D36)` (+66%)**: il `SUM` comprende anche la riga 26 "Extra stipendi" — va ristretto alla **sola riga 25** (netti in busta), perché sugli extra fuori busta non si versano contributi. Caso reale: EBITDA passato da 44.829 a 78.309 dopo la correzione su un periodo annuale. La formula resta attiva anche nei mesi non chiusi: appena si scrivono i netti aggiunge il gross-up anche su mesi futuri, quindi su quei mesi va azzerata o sostituita finché non sono chiusi. Controllo finale: personale del mese ≈ netti + extra + contributi.

Lo script `shared/scripts/cdg_aggregato/build*.py` (`compute_fixes`) corregge i bug 1-4 in automatico sul multi-store — vedi il README nella stessa cartella per la tabella completa. Per il bug 2 esteso (righe 29-367) e il bug 7 non esiste ancora uno script nel plugin: vanno corretti a mano con lo stesso metodo (lettura formule + regex + batchUpdate) finché non viene aggiunto uno script in `skills/crea-cdg-cliente/scripts/`.
*(contributo di Andrea Chirivì, 2026-10-12; bug 7 trovato con Roberto nel controllo del 09/10)*

**Aggiungere righe dentro un blocco con rollup** (es. mono-store GIUGNO26, blocco FORNITORI righe 270-327 con rollup `=SUM(D270:D327)` a riga 269, ma la tecnica vale per qualunque blocco a `SUM` fisso): se manca spazio, inserisci le righe **dentro** il range con `insertDimension` prima dell'ultima riga vuota del blocco (es. `startIndex=326, inheritFromBefore=true`) così i `SUM` si espandono da soli, poi `copyPaste` con `PASTE_FORMULA` di una riga esistente del blocco (es. r270, colonne B:FA) sulle righe nuove per riportare formule di totale riga e percentuali. Verifica dopo: rollup espanso e dry-run pulito. *(contributo di Marco Cuccaro, 2026-08-27)*

### 4. Conosci la struttura (righe/colonne)
**Mono-store nuovo (Economico, righe 1-367):** r2 RICAVI (=somma 3:6, dettaglio da etichettare) · r7 Costi variabili (r8 inventario iniziale, r9 Acquisti = r268 TOT FORNITORI, r10 inventario finale) · r11 MDC · r12 PMV (Personale-Mkt-Vendite) · r13 MOD · r14 Costi fissi · r16 EBITDA · r18-21 MOL attuale/anno prec./differenza + Da fatturare FP (= MOL diff/2) · r24-80 dettaglio personale/marketing/delivery · r353-367 comparazione trimestri. Colonne per anno: `TOTALE | % | 12 × (mese, %)` — 2025: B(TOT)+D,F,…,Z; 2026: AB(TOT)+AD,…,AZ. 6 anni 2025→2030.
**Multi-store (Economico Aggregato):** per periodo un blocco `TOTALE | % | STORE 1 | % | STORE 2 | % …` = `2 + 2×N` colonne; colonne totali = `1 + 13 × blocco × 6 anni` (2 store = 469 col, 3 = 625, 4 = 781). Colonne store = riferimento diretto al tab store; % store = calcolate sui ricavi del *singolo* store. Gruppi colonne a 2 livelli, chiusi di default. I tab **Fatturato** (Aggregato + per store) si auto-alimentano: `FATTURATO` = r2 Economico, `UTILE` = r16 EBITDA, YoY dal 2° anno, progressivo azzerato a gennaio.

**Mappa dettagliata del mono-store GIUGNO26** (il primo fornitore/voce sta SULLA riga
indicata, non dopo): Pubblicità r52, Provvigioni r81, Materiali r121, Servizi r157, Utenze
r244. Solo i blocchi **FORNITORI** (totale in r269, voci r270-327) e **INVESTIMENTI** (totale
in r341, voci r342-352) hanno l'etichetta-totale sulla riga **prima**: la regola "l'etichetta
è il totale, si scrive dalla riga dopo" vale solo per questi due blocchi, non per tutti. Il
blocco INVESTIMENTI ha 11 righe: alla r353 c'è l'intestazione della comparazione trimestri,
alla r354 la riga RICAVI. Oltre la r352 non si scrive: i fornitori piccoli si aggregano con
etichette parlanti o si inseriscono righe dentro il blocco con la tecnica di inserimento
descritta sopra (bug 2026-08-27). Personale: r25 netti, r26 extra, r38 contributi, r40-41
partite IVA/fuori busta (vedi "Personale" sotto). La r15 "Costi produttivi" è `=D12+D14` (il
totale dei costi di struttura): non è una voce da compilare a mano. Il TOTALE della
comparazione trimestri non è l'anno finché il bug 4 non è corretto. Dopo ogni
riclassificazione le righe si spostano: **rileggi sempre la colonna A prima di scrivere**.
*(contributo di Andrea Chirivì, 2026-10-12)*

#### Personale
- **r25** contiene i netti reali dei cedolini, mese per mese.
- **r26** contiene il totale dichiarato dal titolare meno i netti del mese, persona per
  persona (per chi lavora a giornata: giornate × tariffa − busta; per gli esterni: a forfait).
  Mai sommare busta piena ed extra pieno: spesso sono le stesse persone (bustina più contante).
  Se il risultato è negativo resta così — fa fede il totale del titolare. **r26 si compila solo
  dopo che il titolare ha dichiarato a voce, in call, quanto paga fuori busta e a chi**; fino a
  quel momento resta a `0`. Non si ricava da estratti conto, prelievi, contanti o chat, e la
  cifra **non si scrive mai** in messaggi, gruppi WhatsApp o documenti. Finché r26 è a 0, il
  mese si legge come "EBITDA parziale, senza extra" (vedi §6 Verifica).
- Cuoco o collaboratori a **partita IVA** e compensi fuori busta vanno nelle righe **40-41**
  (non subiscono il gross-up della riga 38), mai nelle righe 25-36. Fatture mensili di una
  persona fisica senza IVA (qualche migliaio di € al mese) sono spesso personale a partita IVA
  e non "Servizi": prima di classificarle chiedi chi è. Le ritenute 1040 dei professionisti sono
  già in Servizi e non si contano di nuovo.
- Conta sul serio persone e cedolini (nomi vs. numero cedolini: doppi fogli, ingressi a metà
  mese).
- **Soci che lavorano senza busta** (società di persone, ditte individuali): i soci che
  prelevano un fisso dall'utile o lavorano senza cedolino entrano in una riga "Compensi soci" a
  costo figurativo (confermato coi bonifici degli estratti conto). Senza questa riga l'EBITDA è
  falso (casi reali: un EBITDA apparentemente negativo diventato positivo, o viceversa, solo
  aggiungendo questa riga). Il CE resta REALE — non si crea un secondo CE "con soci inquadrati"
  impostato in modo diverso dal reale (metodo superato: dava risultati inspiegabili). Se serve
  anche la vista "tutto in regola", si fa un prospetto gemello in fondo al tab: stesse righe del
  blocco personale, in formula sul reale, con una riga Delta, **fuori da ogni totale**.
*(contributo di Andrea Chirivì, 2026-10-12, con Roberto — call dell'08/10)*

#### Contratto a sviluppo
La riga **13 MOD** è il MOLD diretto: fatturato netto IVA − materia prima − personale −
marketing − provvigioni delle piattaforme. È la riga su cui RBR si fa pagare in un contratto a
sviluppo, confrontando lo stesso mese dell'anno prima. **L'anno precedente va sempre
compilato**: senza, una promessa sul margine non si può misurare. Prima della firma, cinque
punti da fissare col cliente: 1) il personale entra nei due anni con lo stesso criterio (se c'è
solo nell'anno nuovo, lo sviluppo è negativo per costruzione); 2) i costi fissi dell'anno base
sono completi; 3) il delivery non battuto è perimetro, non sviluppo; 4) si dichiara quale riga
si guarda, MOD o EBITDA, perché danno numeri diversi; 5) si tiene conto della stagionalità. Le
righe 18-21 "Da fatturare FP = MOL diff/2" sono una formula di compenso di default: va
adattata al contratto reale del cliente (es. soglia fissa + percentuale dell'eccedenza).
*(contributo di Roberto — MOLD diretto e anno precedente — e Andrea Chirivì, 2026-10-12 — i
cinque punti)*

### 5. Compila (SOLO dopo riconciliazione)
- Per le fatture passive AdE usa la skill **`cdg-fatture`**: prima **dry-run** (`carica_google_sheet.py FATTURE.xlsx "<url>"`), riepilogo all'utente, poi `--write` solo su conferma esplicita. Multi-store: un FATTURE.xlsx per store con `--sheet "Economico <Store>"`, **mai scrivere sulla tab Aggregato** (è solo formule).
- **Regola IVA**: ricavi scritti come **formula visibile `=lordo/1,1`** nelle celle (scorporo IVA 10% a vista); costi = imponibile SDI (già IVA esclusa, nessuno scorporo); il Finanziario (se mai si farà) = IVA inclusa.
- **Cosa entra nella riga 2 Ricavi**: scarica sempre anche le fatture EMESSE. Quelle al 22% di solito non sono ristorazione (sublocazione spazi, vendita attrezzature): restano fuori dai ricavi di ristorazione, altrimenti gonfiano lo scontrino medio senza un cliente in più. La sublocazione si legge in modo conservativo fuori dal CE, con l'affitto pieno a carico del ristorante; la vendita di un cespite è uno straordinario e non entra mai nell'EBITDA. Le **mance** (in cassa spesso un reparto "Tip IVA 0") vanno su una riga memo "di cui Mance" sotto i ricavi, che NON somma al totale; il mese non chiuso non si inserisce. Con più aliquote la formula è una somma di divisioni (es. `=a/1,1+b/1,22`), mai un `÷1,1` secco su tutto.
- **Locale del foglio: si LEGGE, non si assume.** Prima di scrivere formule verifica il locale del file (File → Impostazioni foglio di lavoro → Impostazioni internazionali, o via API `spreadsheets.get` → `properties.locale`) oppure testa una formula banale in una cella scratch. it_IT → separatore argomenti `;` e decimali con virgola; en_US → separatore `,` e decimali col punto. ⚠️ Il nome tradotto delle funzioni (`SE`, `MEDIA`, `SE.ERRORE`) dipende dalla lingua dell'interfaccia e **non** dice nulla sul separatore: caso reale, interfaccia italiana + foglio en_US → tutte le formule col `;` rotte. Per lo scorporo IVA via API la forma sicura in ogni locale è `*10/11` (con `1,1`/`1.1` rischi #ERROR se il locale non è quello atteso). *(correzione di Luciano Purpi, 2026-09-03)*
- **Scrittura valori via API** (`USER_ENTERED`): passa i numeri come **float veri**, mai stringhe col punto (`'28.29'` in locale italiano diventa l'orario 28:29); `clear()` pulisce i valori ma non i formati → dopo un clear riformatta a NUMBER. Dettagli in `kpi-sheet-cliente`. *(contributo di Andrea, 2026-09-10)*
- **Numeri mese per mese, mai dodicesimi**: chiedi cedolini e costi mensili di tutto il periodo, anno precedente compreso (l'elenco buste del consulente del lavoro è la lista dei mesi che mancano). Una voce in dodicesimi o stimata con l'incidenza annua è **provvisoria** e va dichiarata come tale. Le righe aggregate messe in attesa delle fatture AdE si **sostituiscono**, non si sommano: azzerale prima del ricaricamento (il loader somma sulle celle). Un costo fisso anomalo in un mese si spalma e si dichiara. Ogni scelta di questo tipo va scritta nel tab "Scopo & Tutorial" del mono-store (equivalente del tab "Fonti e logica" di `cdg-gruppo-bilanci-commercialista`).
- **Costi senza fattura**: affitti pagati a privati con bonifico, rate di prestiti, polizze, spese bancarie e spesso le commissioni POS non hanno fattura. Si chiedono gli **estratti conto di tutti i conti** (banca e conti di pagamento legati al POS, es. "Conto Aziendale SumUp": serve il *Resoconto transazioni*/estratto movimenti, non il report vendite del POS, che non è un estratto e può far concludere erroneamente che "il conto non paga"), si estraggono i movimenti in CSV quadrato al centesimo e si raggruppano per voce e mese. Delle rate si separa il capitale (fuori EBITDA, vedi sotto) dagli interessi; un prestito usato in parte per un'altra sede si ripartisce proporzionalmente. Quello che ha già una fattura nel CE non si ricarica una seconda volta. (La stessa regola vale per la riconciliazione dati cliente: gli estratti conto sono una fonte obbligatoria.)
- **Pubblicità (riga 52)**: non arriva intera dal CSV fatture AdE. Google Ads pagato con carta spesso non ha fattura SdI: il costo si prende dal **Riepilogo pagamenti (Fatturazione)** dell'account Google Ads, costo netto mese per mese, su tutto il periodo incluso l'anno precedente — **mai un annuo diviso 12** (cancellerebbe la stagionalità). Per Meta si usa la spesa mensile dell'account, quadrata come in `adv-ristorante`. Prima di scrivere controlla se le fatture della piattaforma sono già nel CSV AdE (capita che Meta fatturi direttamente alla società): usa **una sola fonte per piattaforma e per mese** — il loader somma sulle celle e la stessa spesa si conterebbe due volte. L'etichetta della riga deve dire quali piattaforme contiene davvero. Per un cliente RBR serve l'accesso in lettura alla fatturazione Google Ads (MCC): se manca, la cifra si chiede al titolare.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 6. Verifica di quadratura
- **EBITDA del CDG = totale indipendente del sorgente al centesimo, mese per mese** (es. a soli costi caricati: EBITDA = −costi esatto). Se non torna, c'è un errore da trovare, non da arrotondare. La quadratura al centesimo prova solo che è giusto ciò che è stato caricato, **non che c'è tutto**.
- Multi-store: `verify3.py`/`verify4.py` iniettano dati di test, controllano `TOTALE = somma store`, % e tab Fatturato, e ripristinano gli zeri.
- `#DIV/0!` a modello vuoto: **si lasciano** (decisione Marco), spariscono coi dati.
- **Controllo di completezza prima di leggere l'EBITDA**: mese per mese tutte le macro-righe devono essere compilate (personale r25/r26/r38, affitto, utenze, tasse, costi fuori fattura). Un mese senza buste ha il personale a zero e l'EBITDA appare gonfiato — anche contributi a cifra tonda vanno guardati con sospetto. Un mese incompleto si segnala con ⚠️ e il risultato si chiama **"EBITDA parziale"**, con l'elenco dei pezzi mancanti: non si presenta come risultato finale e non si stima in silenzio (le buste si chiedono). Una stima (es. timbrature × costo orario) è ammessa solo se dichiarata e approvata dal cliente — **da verificare** come metodo, non ancora standard.
- **Mese aperto e fatture in ritardo**: le fatture passive arrivano 2-4 settimane dopo, quindi il food cost dell'ultimo mese esce artificialmente più basso. Nel CE conviene avere due letture, "come si vede oggi" e "a fatture complete" (l'ultimo mese ricostruito al tasso del mese prima). Se i costi del mese aperto sono caricati ma i ricavi no, l'EBITDA annuo crolla artificialmente: o non si caricano i costi del mese aperto, o si legge il totale insieme alla colonna del mese separatamente.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 7. Consegna
Condividi come Editor con `fp-cdg-service@…` (se non già fatto) e registra il file nel **Registry Clienti** (`1_iBuD5T7ECeS0-QD9pKYPgJtHWlMbwGFi84yryteJck`, colonna `file_01_cdg_id`).

Quando il CE è completato: avvisa **Leo** e manda il file al cliente via **PEC** per la firma
(la PEC la manda il consulente, mai in automatico). Il formato esatto da dare al cliente è da
verificare (serve comunque un file che si apra davvero — un xlsx caricato su Drive che "non si
apre" è già capitato).
*(contributo di Andrea Chirivì, 2026-10-12, dalla riunione di team del 31/08 — PEC e avviso a
Leo confermati, formato file ancora da verificare)*

## Aggiungere uno store a un CDG raggruppato esistente
Procedura completa nel README di `shared/scripts/cdg_aggregato/`: duplicateSheet dei tab Economico/Fatturato dell'ultimo store, inserimento di 2 colonne per periodo nell'Aggregato (da destra a sinistra, dentro il gruppo store), copyPaste dei formati, riscrittura griglia con `build_grid`, verifica.
⚠️ **Gotcha colonna A**: `build_grid` NON produce la colonna A (etichette voci). Scrivere la griglia da A1 le **cancella**: scrivere sempre **da B in poi**. La colonna A non dipende dal numero di store (ripristinabile da `Economico Aggregato!A1:A367` di un modello sano).

## CDG ereditato (costruito da altri): checklist prima di leggerlo o consolidarlo
I bug del NOSTRO template sono sopra; un conto economico che arriva già scritto ha difetti diversi e più cari. *(contributo di Luciano Purpi, 2026-09-03)*
1. **Colonne-anno sfalsate**: su un CDG di gruppo la colonna "2025" conteneva il 2023 (anno di apertura). Si scopre incrociando il tab Fatturato dello STESSO file (la riga "gen-23" puntava a `Economico!D2`, mentre negli altri store la colonna D era "gen-25"). Controllo: verificare l'ancoraggio dell'anno incrociando due tab dello stesso file, prima di leggere qualunque numero.
2. **Lordizzatore automatico che raddoppia il personale**: una formula di lordizzazione (es. TFR = netto × 0,66) pensata per store che registrano il netto va **disattivata** sugli store che registrano già lo stipendio lordo (caso reale: 3 store su 4 a lordo, 1 a netto).
3. **Sotto-totali persi su singole colonne-anno** → EBITDA sovrastimato in silenzio (trovati +2.321 € e +1.320 €). E un MOD che ri-somma la pubblicità (marketing escluso dal MOD) non è standard: **va segnalato al cliente, non "corretto" di nascosto**.
4. **Un EBITDA che crolla può essere un artefatto contabile**: 157.483 → 83.785 in due anni, ma erano costi di struttura ribaltati (amministratore, area manager, stipendi sviluppo) passati da 47.857 a 202.039; depurato, l'EBITDA di locale era stabile (33,3% → 31,2% → 31,7%). Due livelli di lettura obbligatori sui gruppi:
   - **EBITDA DI LOCALE** = il locale al netto di tutto ciò che decide il gruppo (royalties, contributo marketing, canone servizi, affitto d'azienda, ribaltamenti) → confronta i locali e giudica chi li dirige.
   - **EBITDA DI GRUPPO** = somma degli EBITDA di locale − costi di struttura pagati davvero a terzi → giudica l'azienda.
Prima di mostrare numeri: riconciliare i ricavi con cassa e contabilità (skill `riconciliazione-dati-cliente`).

Altri difetti ricorrenti in un CE Excel fatto in casa dal cliente — apri le formule una per
una prima di usarlo: 5) la colonna del mese in corso è spesso una proiezione (personale a
segno positivo) che gonfia il totale annuo; 6) in alcuni mesi mancano i contributi del
personale (controlla prima gli F24); 7) i totali di un anno a volte saltano gennaio; 8) le
rimanenze possono avere il segno invertito; 9) le % dei margini sono spesso divise sempre per
una cella fissa; 10) il foglio di un anno precedente può avere il personale contato due volte
e ricavi stimati — in quel caso non è utilizzabile.
*(contributo di Andrea Chirivì, 2026-10-12)*

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
- ⚠️ **Mono-store GIUGNO26 — commissioni POS preimpostate**: in Gestione finanziaria (riga 257) la voce "Commissioni POS" ha già una formula attiva `=ricavi_mese*0,0068`. Se le commissioni POS sono **già** dentro una voce Servizi del cliente (fatture o addebiti già caricati), la riga 257 va **azzerata** — altrimenti si contano due volte. Nel CE definitivo la stima dello 0,68% si sostituisce con gli addebiti veri dell'estratto conto, o con la % reale della rete. *(contributo di Marco Cuccaro, 2026-08-27; completato da Andrea Chirivì, 2026-10-12)*
- **Rate di mutui e finanziamenti**: la quota capitale (mutuo, finanziamento lavori, assicurazione collegata) non è un costo di gestione — sta **fuori dall'EBITDA**, nel blocco investimenti sotto l'EBITDA finché il Finanziario del modello non è riparato. Spiegalo al cliente quando cita la rata come costo fisso. Gli interessi si separano dal capitale (vedi "Costi senza fattura" sopra).
- **Scritture via API — quattro trabocchetti**: (a) mai spostare un blocco leggendo con `UNFORMATTED_VALUE` — le celle-totale vengono lette come importi e riscritte come numeri, con doppio conteggio: riscrivi sempre dal sorgente (export fatture), mai dal foglio. (b) Svuotare un intervallo di celle mensili **cancella anche le formule del totale annuo di riga** (colonne B, AB, BB…): si ripristinano copiando la formula da una riga intatta dello stesso blocco, e dopo ogni pulizia si controllano i totali. (c) Range di somma troncati: un sotto-totale può fermarsi prima della fine del blocco lasciando una riga fuori senza errori visibili — verifica sempre che il range copra tutto il blocco, soprattutto dopo inserimenti di righe (il loader di `cdg-fatture` normalizza i SUM solo delle categorie che tocca, non quelli del personale). (d) Nel tab Fatturato le celle dei mesi sono **formule** (es. `B22 = Economico!AR2`): scriverci un numero rompe il collegamento — i ricavi si scrivono SOLO nella riga 2 dell'Economico.
- **Due locali con la stessa partita IVA** (centri di costo separati): le bollette si dividono per indirizzo; le fatture chiaramente dell'altra sede (affitto, carburante, utenze, TARI) si escludono. La merce comprata su una sede e portata all'altra gonfia il food cost della prima — si chiede al cliente di segnare la merce trasferita per qualche settimana, si stima il passato e, dove non si può dividere, si dichiara. Chi lavora a pranzo in una sede e a cena nell'altra si decide col cliente, persona per persona. Le spese comuni (consulente paghe, commercialista, TARI, SIAE, assicurazioni, auto, utenze, banca, carta, pulizie) si scrivono a metà con formula visibile `=importo/2`, scelta dichiarata nel foglio.
*(contributo di Andrea Chirivì, 2026-10-12, con Roberto — call dell'08/10)*

## Lacune note (da completare con Marco)
- L'ID di un modello mono-store 2025-2030 "master" da duplicare non è documentato nelle memory: è documentato il template `01 CDG` in `_TEMPLATE` e i casi applicati (Luna Blu). Chiedere a Marco quale usare come sorgente per i nuovi mono-store.
- Le memory interne usano il service account `rbr-bot@rbr-ai.iam.gserviceaccount.com` (infrastruttura di Marco); per i consulenti col plugin vale `fp-cdg-service@…` come sopra.
- **Tab Finanziario del modello mono-store GIUGNO26 (`182qhB…`)**: è la copia non ripulita di un aggregato multi-store di un altro cliente (titolo e debiti di un cliente diverso, `IMPORTRANGE` che danno 403, `#REF!`). Ogni copia lo eredita. Il difetto è confermato (riparato una volta su un cliente, 17/09); **non è ancora una procedura standard**, e contrasta con la regola "Il foglio Finanziario NON si tocca" più sotto — serve l'ok di Marco prima di definire una procedura di riparazione standard. Nel frattempo: non toccare il Finanziario senza l'ok esplicito di Marco.
- **Criterio contributi (riga 38 vs. contributiva reale)**: il plugin non dice quale dei due criteri è lo standard RBR quando servono per il confronto fra anni o per il CE reale. Da chiedere a Roberto o Marco.
*(contributo di Andrea Chirivì, 2026-10-12)*

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
