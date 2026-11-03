# Builder GHL: workflow, editor email, attese, campi personalizzati

Trappole del lavoro in UI dopo aver caricato i template.

## Prima di aprire il builder: scheda visibile (contributo di Luciano Purpi e Andrea Chirivì, 2026-10-12)

**Trappola n.1, causa della maggior parte dei "il builder non risponde".** Se la
scheda Chrome non è quella attiva della sua finestra, o la finestra è coperta da
un'altra app (anche Claude a schermo intero), `document.visibilityState` vale
`hidden` e l'app Automation non monta o si congela; `document.hasFocus()` può dire
`true` lo stesso — **non è una prova**.

**Sintomi**: (A) pagina bianca col titolo della scheda giusto e `.hl-loader-container`
nel DOM; (B) builder disegnato ma i clic sui nodi non aprono il pannello, menu "…" e
dialog di conferma non rispondono, il primo clic dopo un dialog viene perso, rotella
morta; canvas bianco con `FirebaseError: Missing or insufficient permissions` = **scheda
congelata, non sessione scaduta**. Ricaricare da nascosta non basta.

**Diagnosi in una riga, prima di concludere qualunque cosa**:
`{vis: document.visibilityState, loader: !!document.querySelector('.hl-loader-container')}`

**Rimedio**: porta la scheda in primo piano — `osascript` `activate` + `set active tab
index` sull'**ULTIMO** indice con quell'URL (le schede vecchie con lo stesso URL
ingannano) — poi ricarica da visibile; Escape pulisce l'overlay scuro. Soluzione
stabile se il consulente lavora su altro: sposta Chrome su un **secondo schermo**
(`set bounds of front window to {...}`) e tieni il builder come scheda attiva;
`activate` da solo non regge. Il canvas si sbianca anche passando per Impostazioni e
tornando indietro; se nulla funziona, logout/login del titolare (lo fa lui).
Reputation e Conversation AI si caricano anche da nascoste: non provano che la
scheda sia a posto. Se uno screenshot mostra l'iframe bianco, uno zoom sulla stessa
regione spesso lo cattura.

## Il builder SI PILOTA a scheda visibile — correzione della regola vecchia

(contributo di Luciano Purpi, metodo a schermate, e Andrea Chirivì, conferma sul
campo 22/09/2026 — superata la regola precedente osservata a scheda nascosta)

**Via API pubblica i workflow restano in sola lettura** (nessuna creazione o
modifica via API). Ma **nel browser il builder SI PILOTA a screenshot + clic se la
scheda è visibile** (vedi sopra "trappola n.1"): montati e pubblicati workflow
interi lavorando così. Restano **non pilotabili**: Form Builder v2, page builder dei
funnel e Brizy, il pulsante "Crea un flusso di lavoro" (si clona, vedi sotto), la
casella Cerca, lo scroll e il menu ⋮ della lista. Se i clic non arrivano, **prima la
diagnosi `visibilityState`**, poi si dichiara il blocco — non il contrario.

Restano valide le regole commerciali e di sicurezza: **non si promette al cliente
che il workflow lo montiamo noi**, si prepara comunque la **specifica di montaggio
blocco per blocco**, la **pubblicazione** (interruttore Draft/Publish) e ogni invio
li decide una persona dopo l'anteprima.

⚠️ **Mai far modificare un workflow da un'automazione non presidiata.** Le modifiche
ai workflow (agganciare un template, cambiare un nodo, pubblicare) si fanno **solo
in una sessione col consulente presente**, mai da un'attività programmata, un
`/loop` o uno script lasciato girare: un aggancio automatico di template da un task
programmato ha generato un loop da 575 messaggi su un cliente reale. La regola pesa
di più ora che il builder si pilota. (contributo di Andrea Chirivì, 2026-10-12)

## Creare un workflow nuovo (contributo di Luciano Purpi e Andrea Chirivì, 2026-10-12)

Il pulsante "Crea un flusso di lavoro" non riceve clic sintetici nemmeno dopo un
reload: lo preme il consulente (guscio vuoto), oppure si **CLONA** una riga
esistente dal menu "…", che porta trigger e struttura. Alternativa: **"Build using
AI"** dentro un workflow nuovo monta lo scheletro (trigger, attese, tag) da una
frase, ma va sempre ripulito — mette le stesse azioni in TUTTI i rami dell'If/Else,
non applica il filtro del trigger (lo scrive solo nel nome), sbaglia campi
personalizzati e filtri. Pulizia: menu "…" del nodo → Delete action → Delete (la
conferma va data due volte), rimetti a mano il filtro del trigger, riapri ogni nodo.
**Nel prompt all'AI builder va solo la struttura, mai il testo dei messaggi**: i
testi si incollano dopo nei nodi.

## Entrare nel sub-account e aprire il workflow giusto (contributo di Luciano Purpi e Andrea Chirivì, 2026-10-12)

Se l'utente entra dal pannello dell'agenzia, prima "Click here to switch" sul
sub-account, altrimenti ogni URL diretto rimbalza alla dashboard dell'agenzia; poi ci
si muove coi clic del menu (es. Sites → Forms). L'URL del singolo workflow è
`/automation/workflow/<id>` al **SINGOLARE**: col plurale la pagina resta bianca. Il
primo ingresso conviene dalla lista `automation/workflows` con l'icona "Open in new
tab" accanto al nome. La lista compare dopo circa 15 secondi (prima schermata
bianca) e non scorre con rotella o PagGiù; la casella Cerca dentro l'iframe non
riceve clic sintetici: per un workflow preciso usa l'URL singolare con l'id letto
via API (`GET /workflows/?locationId=`).

## Canvas dei workflow

(contributo di Luciano Purpi, 13/09/2026 e 2026-10-12 — la riga sul trascinamento
era osservata a scheda nascosta, corretta sotto)

- La rotellina fa **pan verticale** (non zoom; nel builder nuovo "Standard builder"
  muove poco); lo zoom si cambia coi pulsanti +/− in basso a sinistra. **A scheda
  visibile la tela SI sposta** trascinando un'area vuota in modalità mano: dopo il
  trascinamento i nodi non si aprono finché non torni in modalità selezione col
  pulsante mano/freccia in basso a sinistra. Il nodo si apre cliccando la **RIGA
  CENTRALE** del riquadro (non titolo né bordo); cliccare un altro nodo aggiorna il
  pannello; l'icona ⤢ in alto a destra porta il pannello in modale (le tendine non
  restano tagliate). A zoom basso il clic non aggancia: "adatta alla vista" e clic al
  centro esatto, oppure menu "…" del nodo. Screenshot a piena risoluzione prima di
  cliccare una voce di tendina (mai pixel ricalcolati da uno screenshot ridotto). I
  nodi si chiamano tutti "Email"/"Wait" e si riconoscono solo aprendoli. **Publish**
  è l'interruttore in alto a destra e a volte vuole un secondo clic.
- La minimappa non è cliccabile.
- Niente JS né lettura della pagina dentro il canvas: solo schermate e clic.
- "Trova e sostituisci" NON tocca il testo delle email: lavora solo su valori personalizzati e tag.
- Gli URL diretti di GHL falliscono spesso (la rotta `/emails/templates` non carica mai): passa dalla
  barra laterale. La libreria modelli è `/v2/location/<id>/marketing/emails/all`.

## Condizioni e rami (contributo di Luciano Purpi e Andrea Chirivì, 2026-10-12)

- Inserendo un If/Else col "+" fra due nodi, la coda della catena finisce da sola nel
  **PRIMO ramo** e None va a fine: la condizione si scrive al contrario (es. `Tags
  NON include stato-attivo` → continua con l'email) e nel ramo None si mette il "Vai
  a" verso il Wait subito dopo l'email saltata. Dopo ogni inserimento ricontrolla
  cosa c'è nell'altro ramo.
- Il "Vai a" si configura in due tempi: Salva azione, poi clic sul nodo bersaglio
  (diventa verde).
- "Rimuovi dal flusso → Un altro flusso" preseleziona il flusso corrente: togli il chip.
- ⋮ → Copia azione → incolla sotto: la condizione porta con sé tutte le regole.
- **MAI "Delete contact" a fine funnel** (cancella la memoria del rifiuto: usa un
  tag di archivio, es. `turista-archivio`) **e MAI un "Go to" che torna all'inizio**
  (loop infinito su una catena lunga: usa un tag di fine, es.
  `nurture-locale-finito`).
- La riga sotto il riquadro del nodo è **troncata** (es. "Phone contiene 39" era
  "+39"): apri sempre il nodo prima di dichiarare un difetto.
(Punti 5-6 valgono anche nei controlli di collaudo per i conti ereditati, vedi
`collaudo-catenaria.md`.)

## Tendine, etichette e campi dei nodi (contributo di Luciano Purpi e Andrea Chirivì, 2026-10-12)

Per tipo di menu: operatori e campi (Phone, Contiene, unità, DND, tipo evento) =
**doppio clic o clic sul chevron**; picker dei campi e menu del trigger = **clic
singolo**; selettori multipli di etichette/canali = **UN clic alla volta** (il
secondo deseleziona; un doppio clic ha infilato Call accanto a WhatsApp in un nodo
DND), poi screenshot e conta dei chip prima di salvare. Hover prima del clic sui
chip dei tag esistenti, altrimenti "Tags cannot be empty". "Aggiungi nuova etichetta"
col doppio clic la crea due volte (chip +1 nascosto da togliere). La ricerca
etichette filtra con 2-3s di ritardo. I tag si creano PRIMA (Impostazioni → Tag o
API `POST /locations/{id}/tags`) e poi si scelgono come esistenti; se il nodo Add
tag mostra il pallino rosso "Errors found" col chip già dentro, il tag non esiste
nella location: crealo, togli il chip e riselezionalo. **Nodo Email**: se compili il
Nome mittente compila anche l'Email mittente, altrimenti "There are issues in some
of your fields"; lasciati vuoti valgono i predefiniti del sub-account. Testo nei
campi: da clipboard (`osascript` + cmd+v) quando la digitazione è bloccata. (Nota:
"clic sulla voce poi Invio" vale per altre tendine GHL, non per quelle del builder.)

## Leggere e completare i workflow dal backend interno (contributo di Andrea Chirivì, 2026-10-12)

Con la sessione GHL aperta nel browser e l'header `token-id` della pagina (preso con
un hook XHR, **MAI salvato su file**): la struttura completa di un workflow si legge
via `backend.leadconnectorhq.com/workflow/<loc>/<id>` e i trigger via
`…/trigger?workflowId=<id>` (serve a collaudare senza screenshot). Un trigger nuovo
si crea con `POST` su `…/trigger` con `workflowId` in **camelCase** nel corpo,
altrimenti resta orfano. I campi personalizzati in serie si creano con
`POST backend.leadconnectorhq.com/locations/<id>/customFields`, più veloce della
maschera del dialogo (vedi sotto, che resta valida per il caso a mano). I tag con
l'API pubblica `POST /locations/{id}/tags`. La pubblicazione resta di una persona
(Draft/Publish). ⚠️ Endpoint non documentati, possono cambiare senza preavviso; i
campi via `customFields` sono stati creati una volta sola: riprova su un secondo
conto prima di farne il metodo standard.

## Catene che partono da un modulo Meta (Lead Ads) (contributo di Andrea Chirivì, 2026-10-12)

Il trigger "Facebook Lead Form Submitted" mostra la tendina dei moduli **VUOTA**
finché non aggiungi prima il filtro "Page is" con la pagina: è l'ordine dei filtri,
non un guasto dell'integrazione. Un modulo rinominato si cerca col nome nuovo; i
trigger seguono l'id, quindi rinominare è sicuro. Lo strumento di test di Meta
(`developers.facebook.com/tools/lead-ads-testing`) non lascia scrivere nome ed
email e manda dati finti a `test@meta.com`: prova solo il passaggio Meta → GHL.
L'email si prova con "Test workflow" su un contatto vero del consulente. A fine
prova togli il contatto finto creato dal tester.

## Email nei workflow: il nodo può avere una copia propria

(contributo di Luciano Purpi, 19/09/2026 — precisa la regola "modifica dalla libreria" del 13/09)

Il nodo Email può avere una COPIA PROPRIA del contenuto, diversa dal modello collegato: la spunta
**"Sincronizza le modifiche al modello"** è spesso TOLTA. In quel caso modificare il modello in
Marketing → Email → Modelli NON cambia cosa ricevono i clienti.

- Dalla libreria modelli si modifica solo se il nodo ha la sincronizzazione accesa (allora sono lo
  stesso oggetto, e ci arrivi con una ricerca per nome invece di venti scorrimenti).
- Altrimenti guarda e modifica SEMPRE la copia nel nodo: menu ⋮ sull'anteprima → "Modifica il design".
- Caso reale: la mail di consegna gift card diceva "grazie per aver prenotato" a chi NON aveva
  prenotato (testo di un'altra variante finito nel flusso sbagliato) e l'unico pulsante era "Guarda
  il menu". Spiegava da sola "15 sì → 0 prenotazioni". Il modello, non usato, puntava a un'altra
  landing: anche l'attribuzione era sbagliata.
- Vedi anche: "Select existing template" nel nodo non persiste (`suite/memory/gohighlevel.md`).

**Metodo sicuro per modificare la copia:** clic nel pannello codice, cmd+a cmd+c, leggi la clipboard
con `osascript -e 'the clipboard as «class utf8»'` (NON pbcopy: storpia gli accenti; `pbpaste` va bene solo per il collaudo dei link, dove gli accenti non contano),
modifica in locale, fai il diff, rimetti in clipboard con osascript, cmd+a cmd+v, poi RICOPIA e
ri-diffa prima di salvare. L'editor riformatta l'indentazione al paste: confronta ignorando le righe
vuote e con grep mirati sulle stringhe che ti interessano.

**Tre salvataggi in fila:** "Salva" nell'editor del design → "Salva azione" sul nodo → "Salva" sul
workflow. Saltarne uno = perso tutto.

**Controllo di routine:** su ogni funnel a più passi verifica che il testo dell'email corrisponda al
punto del percorso in cui si trova il cliente. I testi migrano fra flussi quando si duplicano i workflow.

## HTML nell'editor email: si incolla, non si scrive

(contributo di Luciano Purpi, 13/09/2026; due strade e controllo copia, contributo di
Andrea Chirivì e Luciano Purpi, 2026-10-12)

**Controllo obbligatorio prima di reincollare**: se cmd+a non ha preso il fuoco
dell'editor, la copia esce di circa 600 byte e incollarla **distrugge il
template**; sotto i 2.000 byte non si incolla, si ricopia. Fra il clic nell'editor e
cmd+a servono 3-4 secondi; cliccare un chip porta il fuoco altrove e il testo
digitato finisce nell'Oggetto — clicca su testo semplice.

**Strada A (pannello codice)**, quella attuale: resta la prima scelta **con la
scheda visibile** (vedi sopra). L'editor chiude i tag da solo: digitando `</div>`
ottieni `</div>>`. Passa dagli appunti di sistema:

```bash
osascript -e 'set f to POSIX file "/percorso/email.html"' -e 'set the clipboard to (read f as «class utf8»)'
```

poi clic dentro il codice, cmd+a, cmd+v. NON usare `do shell script "cat ..."`: converte gli a-capo
in CR e l'HTML arriva su una riga sola.

**Strada B**, se la finestra Source code non risponde (Save che smette di
rispondere dopo il primo incollaggio, cmd+a che seleziona la pagina intera e fa
comparire "Unsaved changes"): incolla HTML **formattato** nell'editor visuale.
Negli appunti i **DATI HTML**, non il testo:
```bash
osascript -e 'set the clipboard to «data HTML<esadecimale>»'
```
poi clic nel testo, cmd+a (screenshot: deve essere evidenziato il testo, non la
pagina), cmd+v, Save action, Save. Trappola: l'editor visuale butta via il
background sui `<div>`; le zone colorate si costruiscono come `<table>` con
l'attributo `bgcolor` oltre allo `style`. ⚠️ La vecchia nota "la finestra codice
regge un solo incollaggio, ricaricare prima di ogni email" è **superata**: con le
entità HTML (vedi sotto) e il controllo del fuoco, regge più incollaggi.

Modifica chirurgica (un id immagine, un URL): clic appena prima dell'estensione, il cursore cade UN
CARATTERE PIÙ A SINISTRA del previsto → Right per correggere, Backspace a blocchi con uno zoom di
controllo ogni tanto. Backspace sì, Delete no.

### HTML solo ASCII + entità (contributo di Andrea Chirivì, 2026-10-12)

La shell e i corpi email si generano in **solo ASCII**, con le entità al posto dei
simboli (`&mdash;` `&euro;` `&egrave;` `&rsquo;`): in Python `html.encode('ascii',
'xmlcharrefreplace')`. Prima del POST o dell'incollaggio controlla che il file non
abbia byte fuori dall'ASCII: `python3 -c "open(f,'rb').read().decode('ascii')"` deve
passare senza errori. **Come si riconosce il guasto**: `‚Äî` o `‚Ç¬¨` al posto di `—`,
`‚Ç¬` al posto di `€`, `√®` al posto di `è` — sono byte UTF-8 letti come MacRoman, la
firma degli appunti (`pbcopy` senza `LANG UTF-8`, o `osascript` con `read f` senza
`class utf8`), **non un limite di GHL**. Con le entità il file regge qualunque
strada: pannello codice, editor visuale (strada B) e API. **Il controllo si fa
sull'email RICEVUTA su un telefono vero**: non vale l'editor e non vale la copia
scaricata con `pbpaste` (arriva già con gli accenti storpiati). La regola ASCII +
entità resta comunque giusta come cintura di sicurezza, anche se la causa più
probabile del guasto è la codifica degli appunti, non "GHL che non regge UTF-8".

### Modifiche puntuali nell'editor visuale (contributo di Andrea Chirivì, 2026-10-12, oggetto anche Luciano Purpi)

- **Action Name, Subject e Pre-Header**: clic nel campo, cmd+a, riscrivi tutta la
  riga; mai cmd+freccia destra e aggiunta (nell'Oggetto non funziona); triplo clic e
  digitazione a volte non prendono e la modifica si perde in silenzio — rileggi lo
  screenshot.
- Chiudendo un'azione appena salvata può comparire "Unsaved changes – discard?":
  falso allarme; Cancel, poi di nuovo Save action e Save.
- **Testo di un link senza perderlo**: mai selezionare tutta la scritta; clic in
  mezzo (mai sul primo o sull'ultimo carattere) e digita il testo nuovo, che eredita
  il link; l'avanzo si toglie con Maiusc+freccia destra contando i caratteri, poi
  Backspace; ciò che sta prima del link da inizio riga (cmd+freccia sinistra,
  Maiusc+destra). Una parola in testo normale: doppio clic e due Backspace,
  verificando con lo zoom cosa è evidenziato.
- **URL di un'immagine (es. il QR) senza finestra codice**: apri il nodo Email,
  scorri col puntatore sul pannello fino all'immagine, clic, nella barretta l'ultima
  icona è "Edit Image", campo Image URL: cmd+a, cmd+v, Update, poi Save action e
  Save aspettando "Saved!"; se l'immagine è a filo del bordo la barretta esce dallo
  schermo, scorri di 1-2 tacche.
- Nell'editor i merge field **non sono risolti**: il QR sembra sempre giusto, il
  difetto si vede solo nell'email consegnata.

## Attesa "fino a giovedì"

Interno → Attendi → tipo "Finché non si apre una finestra ricorrente" → Ogni settimana → spunta solo
giovedì → ora. Le colonne del selettore sono ore | minuti | secondi | AM-PM: è facilissimo mettere
30 nei secondi e ritrovarsi alle 11:00:30. Il pannello mostra le **prossime cinque occorrenze**: si
verifica lì, non nel campo. (Perché giovedì 11:30: skill `funnel-email-crm`, `references/tre-binari.md`.)

Fuso orario: GHL non ha Europe/Rome, si usa Amsterdam (GMT+02:00). Se il sotto-account è già così
NON toccarlo: cambiarlo sposta tutte le attese già programmate.

## Dialogo campi personalizzati

I menu Tipo e Oggetto si sovrappongono e si annullano a vicenda. Ordine che funziona: **prima
Oggetto, poi Tipo, poi nome e cartella**. Un campo alla volta, verificando in lista prima del successivo.
