# Trappole di strumento che falliscono IN SILENZIO

Tutte hanno la stessa forma: **nessun errore, dato sbagliato**. Non appartengono a una sola
skill: leggile ogni volta che automatizzi browser, fogli, gestionali o scrivi in massa sui
dati di un cliente.

---

## A. Strumenti (contributo di Luciano Purpi, 2026-09-03)

### 1. `pbcopy` storpia gli accenti verso Chrome
Li scrive in una codifica letta come MacRoman: "Società" → "Societ√†", "Santé" → "Sant√©".
Se quella colonna è la chiave di un CERCA.VERT, le righe accentate non agganciano e
producono voci "DA ASSEGNARE" fantasma (successo su 3 fornitori su 164).
**Come**: copiare negli appunti in UTF-8 esplicito
```bash
osascript -e 'set the clipboard to (read POSIX file "/percorso/file.tsv" as «class utf8»)'
```
poi riverificare riscaricando il foglio con `export?format=csv&gid=N`.

### 2. Google Sheets gviz: `sheet=<nome>` sbagliato restituisce la PRIMA scheda
Nessun errore: fa credere rotta una scheda che non lo è (falso allarme reale).
**Come**: usare sempre `gid=` e `headers=0` (senza, gviz fonde le prime righe
nell'intestazione e i conteggi escono sbagliati). Per file con molte schede meglio
l'export xlsx (sezione B.2).

### 3. CodeMirror (WPCode, Impreza/USOF e simili): `cm.setValue()` non salva
Non sporca il flag "modificato" del pannello: il pulsante Salva invia il valore VECCHIO.
**Come**: `navigator.clipboard.writeText(nuovoTesto)` (serve prima un clic nella pagina per
il focus) → clic dentro l'editor → Cmd+A → Cmd+V → Salva. Verifica su un URL DIVERSO
(`&v=2`): ricaricare lo stesso indirizzo può servire la bfcache con la modifica NON salvata
e far sembrare riuscito un salvataggio fallito.

### 4. iPratico Cloud: "⟳ Aggiorna" in alto NON salva
È il ricarica-locale e butta via le modifiche senza avvisare. Il salvataggio vero è
`input[type=submit].button-save-update` ("Salva") IN FONDO alla pagina. Verificare sempre
ricaricando.

### 5. Google Sheets pilotato da browser
Cmd+R (riempi a destra) Chrome lo intercetta come ricarica; la cancellazione in blocco di
un intervallo viene bloccata; la Casella del nome spesso non prende il focus al primo clic
e il testo finisce nella cella selezionata (una volta ha sovrascritto un'intestazione).
**Come**: selezionare l'intervallo dalla Casella del nome → screenshot che mostri il
riferimento giusto → digitare le formule separate da `\n` in una sola azione. Dove
possibile, Sheets API al posto del browser.

### 6. GoHighLevel: Form Builder v2 e "Crea un flusso di lavoro" non pilotabili
Il Form Builder gira in un iframe fuori dall'albero di accessibilità e ignora i clic
sintetici (tab che non commutano, elementi del canvas non selezionabili); anche "Crea un
flusso di lavoro" non risponde. L'editing dei nodi DENTRO un workflow esistente invece
funziona. **Pattern**: il consulente crea il guscio vuoto con un clic, l'automazione lo
riempie. Un campo personalizzato MONETARIO non cambia più tipo dopo la creazione: per
importi in euro interi crearlo subito di tipo Numero.

---

## B. Metodo sui dati del cliente

### 1. Backup prima di sovrascrivere, rilettura dopo: il 202 non è una prova
(contributo di Luciano Purpi, 2026-09-08)

**Regola**: prima di sovrascrivere in massa dati di un cliente (testi, configurazioni,
anagrafiche) si fa una COPIA; dopo aver scritto si RILEGGE dal server. Un 202 dice solo che
la richiesta è stata accettata. **Perché**: su 10 locali Resmio, 1 campo su 47 non si
salvava — un nome inventato per analogia che l'API ignorava in silenzio (status 202).

**Verifica dopo la scrittura** — confronto campo per campo, restituendo solo conteggio e
nomi dei campi diversi (mai i testi, fanno troncare l'output):
```js
const ko = Object.entries(campi).filter(([k,v]) => riletto[k] !== v).map(([k]) => k);
```
**Accortezze**
- Testi con accenti passati come JSON con `ensure_ascii=True` (diventano `\uXXXX`) e
  controllo esplicito di un accento nel dato riletto.
- Mandare al browser TEMPLATE + tabella delle variabili (pochi KB), non i campi già espansi
  (decine di KB): meno traffico, meno corruzione.

### 2. Portare dati dal browser al disco senza farli passare dalla chat
(contributi di Luciano Purpi, 2026-09-08 e 2026-09-10)

**Problema**: l'output di `javascript_tool` si tronca (~1.000 caratteri per elemento), ogni
chiamata JS ha un tetto di ~45 s, e l'estensione Chrome oscura i campi sensibili
(queryParams, cookie, URL con querystring → `[BLOCKED]`). Far tornare migliaia di righe
come risultato del tool è lento, costoso e fa transitare dati personali nel contesto.

**Metodo**: si elabora TUTTO dentro la pagina e si fa scaricare un file.
1. Raccolta a pagine con la sessione già loggata, accumulando in una globale
   (es. `window.RG.rows`): una fonte/un modulo per chiamata, il totale si controlla con una
   chiamata separata (il lavoro prosegue anche se la risposta va in timeout).
2. Download del risultato (finisce in `~/Downloads`, poi si legge in locale con Python):
   ```js
   const blob = new Blob([righe.join('\n')], {type:'text/csv'});   // o JSON.stringify(dati,null,1)
   const a = document.createElement('a');
   a.href = URL.createObjectURL(blob); a.download = 'backup-cliente-AAAA-MM-GG.csv';
   document.body.appendChild(a); a.click(); a.remove();
   ```
   Poi `cp ~/Downloads/<file>` nella cartella di lavoro e verifica che il conteggio torni e
   gli accenti siano integri.
3. Google Sheet pesanti: `docs.google.com/spreadsheets/d/<id>/export?format=xlsx` aperto con
   navigate scarica il file con la sessione dell'utente → `openpyxl` (più affidabile di gviz
   con molte schede).
4. **Campo oscurato ma serve solo la sua classificazione** (es. canale di un lead dagli UTM):
   calcolare l'etichetta DENTRO la pagina e restituire solo quella (`ADV_IG`, `ORGANICO`).

Verificato su Jotform (17.830 contatti in 3 chiamate) e sui registri Sheet di un cliente.
I file scaricati con dati personali restano in locale: niente upload, niente repo.
