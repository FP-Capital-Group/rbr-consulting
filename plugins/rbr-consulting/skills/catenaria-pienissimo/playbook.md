# Playbook — Catenaria su Pienissimo Pro

Procedura operativa completa. Ordine consigliato: leggi le trappole, poi segui le fasi.

**Indice**
1. [Trappole dell'interfaccia](#1-trappole-dellinterfaccia)
2. [Accesso alle API](#2-accesso-alle-api)
3. [Creare le promozioni](#3-creare-le-promozioni)
4. [Tag di ingresso](#4-tag-di-ingresso)
5. [Preparare i testi](#5-preparare-i-testi)
5b. [Impaginazione grafica](#5b-impaginazione-grafica)
6. [Schemi dei nodi](#6-schemi-dei-nodi)
7. [Costruire e salvare](#7-costruire-e-salvare)
8. [Verifica e consegna](#8-verifica-e-consegna)

---

## 1. Trappole dell'interfaccia

Cinque comportamenti non ovvi. Costano ore se li scopri sbattendoci contro.

**La sessione non si eredita.** Il token sta in `sessionStorage`, non nei cookie: ogni scheda
nuova è slogata e viene rimandata al login. Non puoi inserire tu le credenziali — fai fare
l'accesso all'utente nella scheda che userai, e non aprirne altre.

**Le impostazioni dei nodi si aprono col tasto destro.** Il doppio clic non fa niente.
Il clic destro fisico spesso non arriva: usa un evento sintetico.

```js
document.querySelector('.drawflow-node.nodo_if .drawflow_content_node')
  .dispatchEvent(new MouseEvent('contextmenu', {bubbles:true, cancelable:true, view:window}));
```

**Il primo clic dopo ogni navigazione viene ignorato.** Angular finisce di montare la vista
dopo il caricamento. Dopo ogni `navigate`, aspetta e poi ripeti l'intera sequenza di clic:
la prima passata non scrive niente. Verifica sempre leggendo i valori invece di darli per fatti.

```js
[...document.querySelectorAll('input')].slice(0,8).map(i => i.value)
```

**I menù a tendina sono `ng-select`, non `<select>`.** Vanno pilotati con `mousedown` +
evento `input`, e il testo di ricerca precedente resta nel campo: svuotalo prima, o
concatenerà. Non usare BackSpace ripetuti per pulire: a campo vuoto il BackSpace cancella
le voci già selezionate.

```js
const st = Object.getOwnPropertyDescriptor(HTMLInputElement.prototype,'value').set;
const inp = sel.querySelector('input');
inp.dispatchEvent(new MouseEvent('mousedown',{bubbles:true}));
st.call(inp, 'TESTO'); inp.dispatchEvent(new Event('input',{bubbles:true}));
// poi clicca l'opzione con mousedown + click
```

Cicli lunghi vanno spezzati: oltre ~45 secondi l'esecuzione va in timeout. Fai blocchi da 8.

**Il widget di chat copre i pulsanti in basso a destra.** Nascondilo prima di cliccare
"Salva" nei pannelli laterali.

```js
document.querySelectorAll('[id^=zsiq],[class*=zsiq],#siqiframe').forEach(e => e.style.display='none');
```

---

## 2. Accesso alle API

Costruire ~155 nodi a drag & drop richiede ore ed è pieno di errori. Le API della piattaforma
accettano l'intera struttura in una chiamata sola.

**Base:** `https://backoffice.pnsapi.io/v4/backoffice`

| Endpoint | Uso |
|---|---|
| `/marketing/workflows/getWorkflows` | elenco catenarie (serve `versione=v2`) |
| `/marketing/workflows/getWorkflow` | struttura completa di una catenaria |
| `/marketing/workflows/saveWorkflow` | POST, salva la struttura |
| `/marketing/promo/getProMarketing` | elenco promozioni |
| `/clienti/getTags` | elenco tag |

**Il token non è leggibile direttamente.** Intercetta l'header `Authorization` da una
chiamata che la pagina fa comunque, e riusalo senza mai stamparlo.

```js
window.__cap = [];
const OO = XMLHttpRequest.prototype.open, OS = XMLHttpRequest.prototype.setRequestHeader,
      OSND = XMLHttpRequest.prototype.send;
XMLHttpRequest.prototype.open = function(m,u,...r){ this.__h={}; return OO.call(this,m,u,...r) };
XMLHttpRequest.prototype.setRequestHeader = function(k,v){ this.__h[k]=v; return OS.call(this,k,v) };
XMLHttpRequest.prototype.send = function(b){ window.__cap.push({h:this.__h}); return OSND.call(this,b) };
// poi naviga nel menù laterale (resta nella stessa pagina) e raccogli:
window.__auth = (window.__cap.find(x => x.h && x.h.Authorization) || {}).h;
```

Il token scade in fretta e ogni ricaricamento pagina azzera `window`: ricattura quando
ricevi un 401. La navigazione dentro il menù laterale invece conserva `window`, la barra
degli indirizzi no. Per portarti dietro dei dati tra ricaricamenti usa `localStorage`,
e ricordati di ripulirlo alla fine.

**Parametri comuni** — `id_multi` e `schema` sono specifici del locale e li leggi dalle
chiamate di rete che la pagina fa da sola:

```
schema=<schema>&ca=undefined&utente_modifica=admin&localiSelezionati=<id_multi>
&utente_loggato=undefined&tipo_utente=master&cod_univoco_login=<cod>
```

---

## 3. Creare le promozioni

Una per ogni blocco promo del funnel. Servono prima della catenaria: le mail devono
puntare al loro link coupon e le Condizioni devono poterle verificare.

`Marketing → Promozioni → +`

| Campo | Valore |
|---|---|
| Nome Interno | sigla riconoscibile, es. `LOB_2X1_BURGER` |
| Nome Pubblico | l'oggetto della mail promo |
| Codici Disponibili | `9999999` |
| Num. max utilizzi per coupon | `1` |
| Tipo Scadenza | `Giorni Validità` |
| Giorni Validità | `15` |

I 15 giorni non sono arbitrari: coprono esattamente il ramo remind (6 remind × 2 giorni),
così il coupon è ancora valido quando arriva l'ultimo promemoria.

Poi apri **Tipologia**:
- `Tipologia sconto`: **Valore** · **Percentuale** · **Omaggio** · **Aggiunta**
- `Prodotto da scontare`: multi-selezione dal listino POS. Per uno sconto sull'intero
  conto lascialo vuoto.

I nomi a listino spesso non coincidono con quelli nelle mail — cerca per parola chiave
prima di concludere che un prodotto non esiste (es. una "pinsa Piemontesina" può essere
a listino come `PIEMONTESINA`, senza prefisso).

**Il link coupon** compare dopo il salvataggio, in **Links e collegamenti → Link**, nella
forma `https://engine.pnsapi.io/v4/forms/viewPromo/?hashform=…`. Serve per le mail: prendilo
dal valore del campo, senza bisogno di leggerlo.

```js
const h = [...document.querySelectorAll('*')]
  .filter(e => e.children.length === 0 && /^Links e collegamenti$/.test(e.textContent.trim()));
h[0]?.click();
// poi leggi l'input che inizia con https://engine.pnsapi
```

**Non fermarti al coupon: la promozione ha due testi obbligatori** nel tab `MESSAGGI PROMO`,
e se restano vuoti il cliente che scarica il coupon trova una pagina bianca.

| Campo nel tab | Dove finisce | A cosa serve |
|---|---|---|
| Testo che appare sulla landing page | `testohtml` | la pagina **prima** del form: deve convincere a lasciare i dati |
| Testo che appare nel messaggio | `testo_custom` | il messaggio **dopo** il download, quello che porta il QR |
| Oggetto | `settings.oggetto` | oggetto di quel messaggio |

Il **QR lo aggiunge Pienissimo da solo**: non inserire `@@linkqrpromo@@`, o ne esci con due.

Sulla landing **non mettere il logo**: la piattaforma ne stampa già uno grande in cima alla
pagina, e il tuo comparirebbe subito sotto. Nel messaggio invece serve. Verificalo aprendo
il link della promozione: è l'unico modo per vedere davvero come viene.

Il salvataggio di questa pagina ha due trappole:
- il pulsante è `button.btn-circle.text-primary`, e la sua posizione cambia con lo scroll:
  trovalo nel DOM e chiamalo con `.click()` invece di cliccare a coordinate;
- **parte solo se il form è "sporco"**. Se stai scrivendo via API, tocca prima un editor
  (`document.execCommand('insertHTML', …)`), lascia salvare, e intercetta il payload: da lì
  modifichi `testohtml` / `testo_custom` e fai il POST.

L'oggetto fa storia a sé: **via API non si scrive**. Va impostato sul campo nella pagina
(setter nativo + eventi `input`/`change`, poi `.click()` sul pulsante), altrimenti resta vuoto.

Infine controlla `settings.remind.attivo`: sono i remind della piattaforma, che si sommano
ai remind della catenaria. Vanno lasciati spenti, o il cliente riceve due serie di solleciti.

---

## 4. Tag di ingresso

`Marketing → Tags → +`, nome parlante legato al funnel. È quello che il nodo Start ascolta.

Non assegnarlo ai contatti: lo fa l'utente quando decide di far partire il funnel.

Recupera `id_tag` da `/clienti/getTags` — serve nel nodo Start.

---

## 5. Preparare i testi

**Le uniche wildcard esistenti** sono `@@nome@@`, `@@cognome@@`, `@@email@@`,
`@@telefono@@`, `@@location@@`.

I funnel scritti a monte usano spesso anche `@@link@@` e `@@link_coupon@@`, che **in
Pienissimo non esistono**: se restano nel testo arrivano al cliente stampati così com'è.
Vanno sostituiti con collegamenti veri:

- `@@link@@` → il sito del locale
- `@@link_coupon@@` → il link coupon della promozione di quel blocco

```js
const esc = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
let b = esc(testo)
  .replace(/@@link@@/g, '<a href="' + sito + '" target="_blank">' + sito + '</a>')
  .replace(/@@link_coupon@@/g, '<a href="' + coupon + '" target="_blank">Scarica il coupon</a>')
  .split('\n').join('<br>');
```

Escapa l'HTML **prima** di inserire i tag `<a>`, altrimenti li rompi.

Carica i testi a blocchi con un separatore, molto più robusto che incollare JSON con
apostrofi e virgolette italiane:

```js
window.__addMails(`
###POS1|||Oggetto della mail
Ciao @@nome@@,
...corpo...
###POS2|||Altro oggetto
...
`);
```

---

## 5b. Impaginazione grafica

Il testo nudo funziona ma rende poco. `corpo_messaggio` accetta HTML completo — l'editor di
Pienissimo conserva tabelle, immagini e link — quindi conviene impaginare le mail come fa
la sezione Bozze: logo in testa, foto, testo, pulsanti.

**Le immagini prendile da quelle già caricate dal cliente**, non da fuori: sono approvate,
sono sul CDN di Pienissimo e non spariranno. Le trovi dentro le bozze esistenti.

```js
const urls = new Set();
for (const id of [/* id delle bozze */]) {
  const r = await window.__api('/marketing/bozze/getBozza', 'id_bozza=' + id);
  const bz = (p => Array.isArray(p) ? p[0] : p)(JSON.parse(r.body));
  [...(bz.corpo_messaggio || '').matchAll(/<img[^>]+src=["']([^"']+)["']/gi)]
    .forEach(m => urls.add(m[1]));
}
```

Poi **guardale prima di sceglierle**: rendile in una griglia nella pagina e fai uno
screenshot. Servono un logo (meglio la versione su fondo scuro), 4-6 foto o banner, e vanno
scartate quelle stagionali (Natale, San Valentino) che in un funnel perpetuo stonano.

**Struttura della mail** — tabelle e stili inline, che è l'unica cosa che i client di posta
rendono in modo affidabile: fascia nera col logo → foto a tutta larghezza → testo su fondo
bianco → pulsanti → fascia nera con il payoff e i contatti. Larghezza 600px.

**I pulsanti nascono dal testo, non si aggiungono sopra.** Ogni mail ha già la sua riga di
call to action (`Dai un'occhiata al menù 👉 <link>`): togli quella riga dal corpo e usane le
parole come etichetta del pulsante. Così il pulsante dice quello che diceva la mail e non
resta un link penzolante nel testo.

Un pulsante per mail, con la destinazione che cambia in base al tipo:
- mail promo e remind → *Scarica il coupon*, verso il link coupon della promozione
- mail di posizionamento → *Prenota il tuo tavolo*, verso un form di prenotazione dedicato

**Il form di prenotazione dedicato serve a sapere da dove arriva la prenotazione.** Non
riusare quello standard del locale: in quel caso le prenotazioni del funnel si mescolano a
tutte le altre e il ritorno diventa impossibile da leggere. Il cliente probabilmente lo fa
già — cerca in `Forms → Forms Prenotazioni` nomi come "promo 20% luglio": è quel pattern.

Il modo pulito è **duplicare** il form standard, non crearne uno da zero: eredita campi,
regole e testi che non conosci. Poi rinominalo col nome della campagna.

Due cose da controllare dopo la duplicazione, perché è lì che si sbaglia:
- **il duplicato nasce disattivo** — se lo lasci così il pulsante porta a un form spento;
- **verifica che il codice del link sia diverso** da quello del form originale, altrimenti
  la provenienza non si distingue davvero. Il parametro `hashform` è dell'account e resta
  uguale per tutti; quello che deve cambiare è `id`.

Usa il link della riga **Nuova Grafica** (`https://forms.pienissimo.pro/?hashform=…&id=…`).

```js
const btn = (b, primary) => '<a href="' + b.href + '" target="_blank" style="display:inline-block;' +
  (primary ? 'background:#c9a227;color:#111;border:2px solid #c9a227;'
           : 'background:#fff;color:#111;border:2px solid #111;') +
  'text-decoration:none;font-weight:bold;font-size:15px;line-height:1;' +
  'padding:14px 26px;border-radius:6px;margin:6px 5px;">' + b.label + '</a>';
```

Ruota le foto sull'indice della mail, altrimenti 57 mail identiche sembrano un errore.
Sposta il payoff finale dal corpo alla fascia nera, così non appare due volte.

**Verifica prima di salvare** che ogni mail abbia due pulsanti e due immagini, che le
mail promo puntino al coupon e che nessuna abbia perso testo:

```js
em.every(x => (x.data.corpo_messaggio.match(/margin:6px 5px;/g) || []).length === 2)
```

Se stai ritoccando una catenaria già salvata, **modifica solo `corpo_messaggio` dei nodi
`nodo_invia` e risalva l'oggetto così com'è**: nel frattempo il cliente potrebbe aver
aggiunto nodi a mano, e ricostruire da zero glieli cancellerebbe.

---

## 6. Schemi dei nodi

Struttura Drawflow: `struttura.drawflow.Home.data`, un oggetto con chiave = id numerico.

Ogni nodo: `{id, name, data, class, html, typenode:true, inputs, outputs, pos_x, pos_y}`
dove `class` e `html` valgono entrambi il nome del nodo.

**Collegamenti** — vanno scritti su entrambi i lati, altrimenti l'editor non disegna l'arco:

```js
nodes[from].outputs[out].connections.push({node: String(to), output: 'input_1'});
nodes[to].inputs.input_1.connections.push({node: String(from), input: out});
```

### nodo_start
```js
{ name:'nodo_start', udid, id_multi:['<id>'], ids_fidelity:[],
  tags:[{id_tag, tag, tipo:'custom', not_editable:false, visibile:true,
         id_multi:['<id>'], id_tag_custom:null}],
  text_custom_show:'<nome tag>', params_wa:{} }
```
Nessun input, un solo `output_1`.

### nodo_wait
```js
{ name:'nodo_wait', udid, id_multi:['<id>'], fidelityList:[], allActiveFidelity:[],
  tipo_attesa:'tempo', text_custom_show:'Dopo GG:3', gg_attesa:3,
  params_wa:{}, evento_scaduto:'' }
```

### nodo_invia
```js
{ name:'nodo_invia', udid, id_multi:['<id>'], fidelityList:[], allActiveFidelity:[],
  text_custom_show:'Email', tipo_invio:'1',
  nome_interno:'POS1',          // etichetta visibile sul nodo
  oggetto:'...', corpo_messaggio:'<html>',
  allowed_consenso_marketing:1, hide_unsubscribe_link:'0',
  allowed_only_wa_confermato_node_level:'DEF', params_wa:{} }
```
`tipo_invio`: `1` = Email · `2` = WhatsApp · `4` = Email + WhatsApp.
Con `4` serve anche un testo WhatsApp separato per ogni mail.

### nodo_if
```js
{ name:'nodo_if', udid, id_multi:['<id>'], fidelityList:[], allActiveFidelity:[],
  interazioni:{interazioni:[], massivi:null},
  promo_in:[{id_promozione, nome_promozione, nome_interno,
             nomeShow:'<interno> - <pubblico>', pwa:false, id_multi:['<id>']}],
  operatore_promo:'or',         // almeno una delle promo selezionate
  tipo_promo:'utilizzate',      // tutte | valide | utilizzate | scadute
  nome_interno:'CHECK PROMO1', params_wa:{} }
```
Due uscite: **`output_1` = Vero**, **`output_2` = Falso**.

`tipo_promo` è la scelta che conta: `utilizzate` continua i remind finché il coupon non
viene riscattato in sala, `valide` li ferma già allo scaricamento. In alternativa il nodo
può filtrare per tag (`tags[]` + `tipo_ricerca`) invece che per promozione.

---

## 7. Costruire e salvare

**Struttura della catena.** Il funnel alterna blocchi di posizionamento e blocchi promo:

```
Start
  → 3gg → POS → 3gg → POS …            (blocco posizionamento)
  → 2gg → PROMO → 2gg → Condizione     (blocco promo)
        Vero  → primo nodo del blocco successivo
        Falso → REM1 → 2gg → Condizione → … → REM6 → 2gg → Condizione
                                                 (Vero e Falso → blocco successivo)
```

Ogni blocco promo ha **7 Condizioni**: una dopo la promo e una dopo ciascuno dei 6 remind.
Le uscite Vero convergono tutte sul primo nodo del blocco successivo; dopo l'ultimo remind
ci convergono entrambe le uscite.

Le Condizioni puntano in avanti, a nodi non ancora creati: tienile in una lista di uscite
pendenti e collegale quando crei il primo nodo del blocco dopo.

Con 57 mail vengono **155 nodi**: 1 Start, 57 Invia, 62 Attendi, 35 Condizione.

**Layout** — posiziona su griglia (`x = 40 + col*250`, `y = 60 + riga*150`): posizionamento
in riga, blocchi promo con i remind incolonnati sotto. Non deve essere bello, deve essere
leggibile: l'utente può riordinare a mano.

**Salvataggio** — recupera prima il record esistente, sostituisci `struttura` e `settings`,
poi POST:

```js
w.settings  = {versione:'v2', tags:[id_tag], priorita:'20'};
w.attivo    = false;
w.struttura = {drawflow:{Home:{data: nodes}}};

await fetch('https://backoffice.pnsapi.io/v4/backoffice/marketing/workflows/saveWorkflow', {
  method:'POST',
  headers: Object.assign({'Content-Type':'application/json'}, window.__auth),
  body: JSON.stringify({ workflow:w, id_multi:'<id>', utente_modifica:'admin',
                         schema:'<schema>', localiSelezionati:['<id>'],
                         tipo_utente:'master', cod_univoco_login:'<cod>' })
});
```

Risposta attesa: `201` con `[{"id_workflow": <id>}]`.

Crea il contenitore della catenaria dall'interfaccia (`Catenaria → +`, dà l'id), poi
riempilo via API.

---

## 8. Verifica e consegna

Prima di dire che è fatto, controlla il grafo:

```js
// ogni nodo tranne lo Start ha almeno un ingresso
// nessuna uscita vuota, tranne l'ultima mail del funnel
// tutti i nodi raggiungibili partendo dallo Start
```

Poi rileggi la catenaria dal server e verifica che:
- il numero di nodi per tipo corrisponda
- nessuna mail abbia il corpo vuoto
- **nessun `@@link` sia rimasto** nei testi
- le mail promo e remind contengano il link coupon
- `attivo` sia `false`

Infine apri l'editor e guarda che i nodi si disegnino con i collegamenti, e apri un nodo
mail col tasto destro per controllare nome interno, oggetto e corpo.

**Consegna** dicendo esplicitamente che la catenaria è **non attiva** e che i contatti non
hanno ancora il tag: sono le due condizioni che devono verificarsi perché parta una mail,
e la scelta di quando spetta all'utente.

Elimina le catenarie di prova che hai creato e ripulisci le chiavi temporanee in
`localStorage`.
