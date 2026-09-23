---
name: kpi-sheet-cliente
description: Crea o aggiorna il Google Sheet KPI settimanale del cliente (stile Red Mike / Barresi / Luna Blu). Usala quando devi "creare il file 05 KPI di un cliente nuovo", "aggiornare i KPI settimanali", "impostare il foglio incassi settimanale", "aggiungere un canale al KPI" o caricare i dati della settimana. Imposta struttura colonne, KPI (incasso totale, sala/delivery/cerimonia, coperti, ore, costo personale, recensioni), date dinamiche e update in-place via Drive API senza rompere il layout.
---

# KPI Sheet cliente (05 KPI Manager settimanale)

## Perché esiste
Il **05 KPI Manager** è il file operativamente più importante: si aggiorna ogni settimana ed è quello che il consulente guarda per capire come va il locale. Deve restare pulito, con i giornalieri come input e il tab settimanale tutto a formule. Un update fatto male (colonne spostate, formule rotte, dati del cliente sovrascritti) fa perdere fiducia. La regola: **il cliente compila solo gli input giornalieri, tutto il resto è formula**.

## Quando usarla
- Onboarding cliente nuovo: serve il file KPI settimanale.
- Aggiornamento settimanale: caricare/rivedere gli incassi della settimana.
- Modificare il layout (aggiungere un canale, una voce recensioni, "saldo delivery").

## Prerequisiti
- Dati riconciliati (skill `riconciliazione-dati-cliente`) se stai caricando un nuovo periodo.
- Accesso Drive: connettore OAuth di Marco per copiare + service account `rbr-bot@rbr-ai` (Editor sul file) per scrivere. Se manca l'accesso, chiedi a Marco.
- Python con `openpyxl`. Token/credenziali dal `.env` o `shared/credentials/` — mai incollarli nel repo.
- ID template `05 KPI Manager`: `1YFxdKPeJuer9I-Y_fc3NsvN8brHPvkZETERFleg3pjI` (in cartella `_TEMPLATE`). In alternativa clona un KPI cliente già pulito (es. `005 KPI Barresi`) e ripulisci i residui.

## Procedura

### 1. Crea il file (nuovo cliente)
Duplica il template `05 KPI Manager` **oppure** clona un KPI cliente collaudato (Barresi/Luna Blu) e rimuovi i tab residui del cliente precedente (es. "MENU CICCIA"). La copia la fa Marco dal browser o il connettore OAuth: **mai il service account** (niente quota Drive). Metti il file nella cartella Drive del cliente (dentro la cartella clienti condivisa, così Luciano la vede per ereditarietà).

### 2. Imposta i tab
- **`KPI <Cliente>`** (settimanale, tutto formule): righe per KPI, colonne per settimana. Blocco per anno; le settimane 2026 partono dopo il 2025. Convenzione settimane **lun-dom** (S1-2025 = 30/12/24–5/1/25, S1-2026 = 29/12/25–4/1/26).
- **`Giornaliero 2025` / `Giornaliero 2026`** (input del cliente): una riga per giorno. Colonne per canale — incasso, transazioni, TM, coperti per Sala; incasso+conteggi per ASPORTO / GLOVO / DELIVEROO / JUST EAT; COSTI; GIFT CARD (Distribuite/Rientrate). Il cliente compila SOLO incasso + conteggi; totale e transazioni medie sono formule.
- **`Costi`**: registro libero (Data, Motivazione, Importo, Sett./Anno automatici).
- Se il cliente ha "nero" da tracciare, aggiungi `Incassi Extra` (verde) e `Spese Extra` (rosso), registri Data/Motivazione/Importo con Sett./Anno automatici e totale in alto.

### 3. KPI principali del tab settimanale
Incasso TOTALE (+coperti), incasso Sala / Delivery / Asporto / Cerimonia, coperti, ore lavoro, costo personale, recensioni **Google / TripAdvisor / TheFork**, gift card. Aggiungi Best Ever / Media anno e Δ vs anno precedente.
- **Best Ever e Media auto-estendibili** su un foglio a 52 settimane, invece di allungare gli intervalli a mano ogni settimana: `=IFERROR(MAX(FILTER($D{r}:$BC{r}, $D${riga_chiave}:$BC${riga_chiave}>0)),"")` (e `AVERAGE` per la media), dove la riga chiave è una riga sempre valorizzata quando la settimana è reale (es. Coperti Sala). Caso reale: ha sostituito sette intervalli finali diversi e otto righe "Best Ever" che in realtà facevano `SUM` delle prime 11 settimane. Formula scritta per locale en_US: adatta separatore e nomi al locale del foglio (vedi sotto). *(contributo di Luciano Purpi, 2026-09-03)*

### 4. Scorporo IVA
Gli incassi **settimanali** vanno scorporati IVA (ristorazione 10% → `SUMIFS(...)/1,1`); i **giornalieri** restano al lordo (li compila il cliente). Applica lo scorporo dentro le formule del tab settimanale, non modificando gli input.

### 5. Update in-place (stesso link, senza rompere il layout)
1. **Export SEMPRE per ID** (non per nome: nelle cartelle possono esserci xlsx omonimi vecchi):
   `export?mimeType=…spreadsheetml.sheet` sull'ID del file.
2. Modifica con `openpyxl`, poi **PATCH** via Drive API `uploadType=media`.
3. ⚠️ **Prima di sovrascrivere**: apri con `data_only=True` e controlla se Marco o il cliente hanno inserito dati/tab a mano → preservali. Non rigenerare da script tab compilati manualmente senza chiedere.
4. Se cambi il layout colonne dei giornalieri → **ri-punta le formule** del tab settimanale (tieni una mappa colonne aggiornata).

### 6. Condivisione e consegna
Condividi con `rbr-bot@rbr-ai` come **Editor**, e come writer con `marco.cuccaro2015@gmail.com` + `lucianopurpi@gmail.com` (baseline RBR). Registra il file nel Registry Clienti. Manda al cliente il link (di solito via WhatsApp/Telegram tramite Marco).

## Regole RBR & trabocchetti
- ⚠️ Incassi settimanali IVA esclusa, giornalieri al lordo: non confonderli.
- ⚠️ Il rate limit Sheets è 60 read/min → un solo `batchGet`, niente loop di get singoli.
- ⚠️ **Il locale del foglio si LEGGE, non si assume.** Prima di scrivere formule verifica File → Impostazioni foglio di lavoro → Impostazioni internazionali (o via API `spreadsheets.get` → `properties.locale`), oppure testa una formula banale in una cella scratch. it_IT → separatore `;` e decimali con virgola; en_US → separatore `,`. Il nome tradotto delle funzioni (`SE`, `MEDIA`, `SE.ERRORE`, `FILTRO`) dipende dalla lingua dell'interfaccia e **non** è indizio del separatore: caso reale (KPI settimanale, 31/08/2026) interfaccia italiana + foglio en_US → formule col `;` tutte rotte, e l'errore si vede solo dopo. *(correzione di Luciano Purpi, 2026-09-03)*
- ⚠️ **Numeri via API** (gspread/Sheets, `USER_ENTERED`): passa i numeri come **float veri**, mai stringhe col punto: in locale italiano `'28.29'` diventa l'orario 28:29. E `worksheet.clear()` pulisce i valori ma non i formati: le celle restano a durata e mostrano `678.57.36` anche coi numeri giusti → dopo un clear riapplica `worksheet.format(range, {"numberFormat": {"type": "NUMBER"}})`. *(contributo di Andrea, 2026-09-10)*
- ❌ Mai sovrascrivere dati/tab compilati a mano dal cliente o da Marco senza conferma.
- ❌ Mai spostare le colonne input dei giornalieri senza ri-puntare le formule settimanali.
- File spazzatura vecchi nella cartella (xlsx omonimi non eliminabili dai nostri account): non toccarli via API, falli cancellare a Marco.

## Definition of Done
- [ ] File creato dal template `05 KPI` (o clone pulito), residui del cliente precedente rimossi
- [ ] Tab settimanale a formule + giornalieri input + registri costi/extra
- [ ] KPI completi (incassi per canale, coperti, ore, costo personale, recensioni, gift card)
- [ ] Scorporo IVA sui settimanali, giornalieri al lordo
- [ ] Update in-place per ID, dati esistenti del cliente verificati e preservati
- [ ] Condiviso Editor con `rbr-bot`, writer con Marco + Luciano, riga nel Registry Clienti
