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

**Anche lo strumento di anteprima gviz collassa le celle vuote**: le colonne possono sembrare
slittate rispetto al foglio reale (diagnosi sbagliata su un foglio che invece era allineato).
Prima di dichiarare righe slittate, rileggi cella per cella con l'export csv/xlsx in Python,
non con l'anteprima.
*(contributo di Andrea Chirivì, 2026-10-12)*

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

**Altre trappole del portale iPratico**: mai Escape nei pannelli, chiude senza salvare. Un
pannello riaperto conserva lo scroll: i clic alla cieca finiscono nei campi sbagliati. I
"Salva" dei form ingredienti sono `input submit`; "Salva e chiudi" ha spazi non standard nel
testo, quindi cerca "salva" e "chiudi" separati. Alcuni multiselect condividono le stesse
opzioni fra campi diversi: si scelgono per etichetta della sezione, non a occhio. I dialoghi si
impilano nel DOM: la verifica vera si fa sempre dall'API, non dalla pagina.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 5. Google Sheets pilotato da browser
Cmd+R (riempi a destra) Chrome lo intercetta come ricarica; la cancellazione in blocco di
un intervallo viene bloccata; la Casella del nome spesso non prende il focus al primo clic
e il testo finisce nella cella selezionata (una volta ha sovrascritto un'intestazione).
**Come**: selezionare l'intervallo dalla Casella del nome → screenshot che mostri il
riferimento giusto → digitare le formule separate da `\n` in una sola azione. Dove
possibile, Sheets API al posto del browser.

### 6. Comandi che ignorano i clic sintetici — non solo GHL
Il Form Builder GHL v2 gira in un iframe fuori dall'albero di accessibilità e ignora i clic
sintetici (tab che non commutano, elementi del canvas non selezionabili); anche "Crea un
flusso di lavoro" non risponde. L'editing dei nodi DENTRO un workflow esistente invece
funziona. **Pattern**: il consulente crea il guscio vuoto con un clic, l'automazione lo
riempie. Un campo personalizzato MONETARIO non cambia più tipo dopo la creazione: per
importi in euro interi crearlo subito di tipo Numero.

Lo stesso comportamento (clic sintetici ignorati) si trova anche fuori da GHL: Meta Gestione
inserzioni (tendina "Luogo della conversione", selettore del raggio), tendine "Match delle
condizioni" di alcuni editor di automazioni, link "rimuovi questo elemento" di alcuni builder
drag-and-drop. **Pattern generale**: prepara tutto il resto, chiedi al consulente o al titolare
il singolo clic, poi verifica a schermo il valore impostato (un'inversione tipo "Is"/"Is not"
rovescia l'effetto).

**Form Builder GHL con clic veri** (browser integrato o input di sistema): funziona, ma il
primo "Save" può salvare solo una parte mentre nel builder sembra tutto a posto — verifica
sempre con un `curl` sull'URL pubblico del modulo. Il pallino arancione sul pulsante indica
modifiche non salvate. Il colore del pulsante non accetta l'esadecimale digitato (serve il
selettore colore). Il messaggio finale sta in Settings → On Submit → Message.
*(contributo di Andrea Chirivì, 2026-10-12)*

---

### 7b. Sync TheFork → Resmio: importare le nuove non basta
Oltre alla regola dell'attività programmata (sotto): le **disdette** fatte su TheFork restano
confermate su Resmio e vanno annullate prima del servizio (entro l'orario concordato). I
**cambi di coperti** non si riportano da soli (es. 6 su TheFork contro 4 seduti). Il giro
confronta anche stato e coperti delle prenotazioni già importate, non solo le nuove — nella
checklist settimanale "sync TheFork vivo" diventa "sync TheFork vivo e allineato (nuove,
disdette, coperti)".
*(contributo di Andrea Chirivì, 2026-10-12)*

### 8. Lista virtualizzata in una scheda collassata: totali giusti, righe mancanti
Se la scheda Chrome ha `window.innerHeight = 0` (collassata o nascosta), le liste
virtualizzate (es. TheFork) rendono solo le prime righe: i totali dichiarati sono giusti ma i
nomi/righe mancano, **senza nessun errore**. Scroll e resize non bastano: apri una scheda
nuova. Controllo obbligatorio su ogni lettura: la somma dei valori letti deve tornare col
totale dichiarato dalla pagina.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 9. Chrome pilotato: lavorare sulla scheda giusta e in primo piano
`browser_batch` lavora sempre sulla scheda **attiva** anche passando un `tabId`: uno screenshot
di una scheda precisa va chiesto in una chiamata singola col `tabId`. La finestra con la scheda
guidata non è sempre quella in primo piano — in quel caso i clic non arrivano: trova la scheda
per URL, porta la finestra davanti, attiva la scheda e **ricaricala**, perché solo dopo il
reload `visibilityState` diventa `"visible"`. Un browser interno a pannello nascosto non
registra i clic: le prove d'invio si fanno sempre in Chrome in primo piano. Le immagini lazy
non si caricano in una scheda in background.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 10. Lo screenshot non è una prova: si misura
Niente caccia a difetti visti solo in uno screenshot: un hero che sembra nero in cattura può
avere luminosità vera (disegnalo su un canvas e misurala), un modulo incorporato può apparire
bianco per 1-2 secondi mentre carica, un iframe può uscire bianco nello screenshot normale e
leggibile con uno zoom sulla stessa regione. Prima di concludere "la pagina non ha caricato"
fai uno zoom. Prova non distruttiva per sapere se i clic arrivano: digita nel campo Search e
verifica se la lista si filtra. Si misura (pixel, dimensioni, stile calcolato) o si verifica in
primo piano dopo uno scroll vero — mai solo "a occhio" sullo screenshot.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 11. PDF con font cifrato o pagine scansionate: rasterizzare
Un PDF che sembra testuale può restituire testo illeggibile perché il font è cifrato (es. F24
di uno studio paghe): rendi la pagina in PNG (PyMuPDF o equivalente) e leggi l'immagine. Stesso
trattamento per pagine scansionate dove l'estrazione testo non rende nulla: rasterizza pagina
per pagina. Segnale d'allarme: testo estratto senza parole riconoscibili — in quel caso non
consegnare zeri, rasterizza.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 12. Pagina Claude con database condiviso: non scrivibile da chi ha un altro account
Una pagina Claude con database condiviso non è scrivibile da chi usa un account Claude diverso:
dal menu Condividi esce solo "visualizzare". Per uno strumento di squadra serve un piano Team
con tutti dentro, oppure uno spazio web proprio.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 13. Sync TheFork → Resmio come ciclo nel browser: si ferma quando il Mac dorme
Un ciclo (loop, `/loop`, script in una scheda Chrome) che copia le prenotazioni TheFork su
Resmio **muore in silenzio** appena il Mac va in stop: su Dirigì è rimasto fermo **41 ore**
e in un giorno si è persa metà delle prenotazioni. **Regola (03/10/2026):** il sync TheFork
gira solo come **attività programmata** (scheduled task / routine cloud / GitHub Actions /
cron su server) con un controllo «sync vivo» nel giro settimanale della checklist
marketing (`checklist-marketing-rbr`). Mai come ciclo nel browser del consulente.

**Attività programmate: durevoli, verificate e idempotenti.** I giri creati dentro una sessione
di Claude (cron di sessione, `/loop`) vivono in memoria: spariscono se il processo si riavvia —
e con loro le schede Chrome collegate — e comunque scadono da soli dopo qualche giorno senza
errori. Prima di dare per vivo un giro, controlla l'elenco reale delle attività programmate
(mai fidarsi a memoria): per un sync vero serve un'attività durevole o un server. Un'attività
che parte due volte non deve riscrivere niente: la seconda esecuzione fa solo un ricontrollo in
sola lettura. Una verifica partita prima dell'orario previsto fa solo il controllo preventivo e
lascia il conteggio vero al giro programmato.
*(contributo di Andrea Chirivì, 2026-10-12)*

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
(contributi di Luciano Purpi, 2026-09-08 e 2026-09-10; correzione di Andrea Chirivì, 2026-10-12)

**Problema**: l'output di `javascript_tool` si tronca (~1.000 caratteri per elemento), ogni
chiamata JS ha un tetto di ~45 s, e l'estensione Chrome oscura i campi sensibili
(queryParams, cookie, URL con querystring → `[BLOCKED]`). Far tornare migliaia di righe
come risultato del tool è lento, costoso e fa transitare dati personali nel contesto.

⚠️ **Correzione importante**: il download di un Blob riesce **UNA sola volta per sessione**.
Dal secondo download Chrome blocca i download automatici **senza dirlo**: su un'estrazione di
decine di file, più della metà possono andare persi senza errore, e i file compaiono uno per
volta invece che tutti insieme. Il metodo sotto resta valido per **un singolo file**; per tanti
file servono le varianti (a)/(b).

**Metodo base**: si elabora TUTTO dentro la pagina e si fa scaricare un file.
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

**(a) Tanti file = UN pacchetto**: fetch dei report dentro la pagina, un unico oggetto
(base64 per i binari), **un solo** Blob scaricato, poi uno script Python che lo spacchetta
nella cartella del cliente e ripulisce `Downloads`.

**(b) Alternativa senza download**: scrivi il JSON in un `<pre>` della pagina
(`document.body.innerHTML='<pre id="d"></pre>'`, poi `textContent`) e leggilo con
`get_page_text`, che regge ~50.000 caratteri per chiamata. Prima del dump fai l'escape
`\uXXXX` dei caratteri non ASCII (`get_page_text` altera doppi spazi e NBSP) e confronta uno
SHA-256 calcolato in pagina e in locale (bastano i primi 16 caratteri) — lo stesso controllo
vale quando incolli un testo lungo in una pagina via JS.

**(c) Non funzionano**: fetch dalla pagina verso `localhost`/`127.0.0.1` (resta appesa sul
permesso "rete locale" di Chrome) e la clipboard.

**(d) Output del `javascript_tool`**: tronca fra ~1.000 e 2.000 caratteri e oscura sia URL con
query string (usa `split('?')[0]`) sia qualunque script che nomini `document.cookie` — restituisci
sempre solo numeri o etichette, mai l'oggetto intero.

Verificato su Jotform (17.830 contatti in 3 chiamate) e sui registri Sheet di un cliente, e con
cinque fonti indipendenti sulla correzione del download singolo.
I file scaricati con dati personali restano in locale: niente upload, niente repo.

### 1b. Zero anomalie non vuol dire tutto a posto
Ogni controllo automatico che legge dati altrui (fatture, cassa, prenotazioni) deve scrivere nel
risultato **"dati fino al …"** per ogni fonte, e prima di dichiarare "nessun problema" verifica
la data dell'ultimo dato letto. Caso reale: un controllo prezzi fornitori è uscito pulito per
due settimane perché nella fonte non entrava nessuna fattura da giorni (token scaduto,
registrazioni ferme) — il controllo non aveva trovato nulla perché non c'era niente da
controllare, non perché fosse tutto a posto. Un controllo che non è riuscito a leggere si scrive
come **SALTATO**, mai come "a posto".
*(contributo di Andrea Chirivì, 2026-10-12)*

### 3. Script lunghi nel browser: timer rallentati, 45 secondi, navigazione
1. **Niente `setTimeout`/`requestAnimationFrame`** negli script del tool JS: con la scheda in
   secondo piano Chrome rallenta i timer (fino a 1 giro al minuto) e la chiamata scade a 45 s —
   un loop in background CON pause non avanza.
2. **Lavoro sotto i 45 s**: fetch in parallelo con `Promise.all`, risultato nella stessa
   chiamata.
3. **Lavoro più lungo**: blocchi lanciati **senza `await`** che accumulano su `window.X`,
   riletti con chiamate successive, senza pause dentro al blocco.
4. Se uno script deve restare vivo in una scheda ("presidiato"): il tempo si conta con un Web
   Worker; **navigare nella scheda la uccide senza avviso** (scheda dedicata, "NON CHIUDERE,
   NON NAVIGARE"); Chrome apre al massimo 6 connessioni HTTP/1.1 per host — due cicli sulla
   stessa API si intasano per minuti, quindi un giro alla volta con guardia e timeout, mai due
   ponti nello stesso Chrome, storico errori con l'orario.
*(contributo di Andrea Chirivì, 2026-10-12 — la correzione vale per i loop con pause; l'accumulo
su `window` senza timer di cui sopra resta valido)*

### 4. Modificare script e catene di comandi senza romperli in silenzio
1. Le modifiche agli script generatori si fanno **per righe o blocchi identificati**, mai con
   sostituzioni regex multi-riga (`re.S`): una regex troppo "golosa" può distruggere un
   generatore intero.
2. Le catene modifica → rigenera → carica si fermano al **primo errore** (`&&` o `set -e`). Il
   file rigenerato si guarda prima di caricarlo, e dopo il caricamento si confronta il file
   online con quello locale (un caso reale: file vecchi ricaricati come "v2", scoperto solo
   perché il destinatario ha restituito lo stesso hash).
3. Quando aggiungi un filtro per togliere righe-rumore, guarda cosa gira **dopo**: prima
   intercetta i casi speciali, poi filtra (un filtro troppo ampio ha spento per sempre un
   controllo collegato).
Verifica obbligatoria dopo ogni patch: i numeri chiave restano identici prima e dopo.
*(contributo di Andrea Chirivì, 2026-10-12)*

### 5. Chiamate HTTP e FTP da script che falliscono in silenzio
Sempre un timeout esplicito (`curl -m 40`, `timeout=` in Python): `urllib` sui `POST` può
restare appeso senza errore, e `curl` da zsh può dare `HTTP 000` su una scrittura fallita. Una
richiesta per record, un corpo `.json` per record con `curl --data @file` (letti da file di
testo con `read` possono dare 400), l'id verificato nella risposta. In zsh `set -- $q` non
spezza le parole: i cicli su più parametri vanno fatti in Python.
**FTP**: sopra qualche KB un `426 Transfer aborted` (`curl` rc=18) può lasciare sul server un
file **vuoto**, senza errori visibili a valle. Usa `--ftp-skip-pasv-ip` e verifica la dimensione
remota dopo ogni caricamento, ritentando finché coincide.
*(contributo di Andrea Chirivì, 2026-10-12 — FTP confermato; la parte HTTP è prudenza generale,
non ancora isolata a una causa singola)*
