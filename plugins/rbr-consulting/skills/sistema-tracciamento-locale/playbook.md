# Playbook — come si monta ogni pezzo

Riferimento tecnico della skill `sistema-tracciamento-locale`. Tutto quello che segue è
stato eseguito e verificato su un cliente vero (Noolas Pub, luglio–agosto 2026). Dove una
cosa non funziona è scritto che non funziona, con il motivo.

---

## FASE A — Le fondamenta

### A1 · L'anagrafica e il consenso

Quasi ogni locale arriva con una lista da un sistema precedente. **Va importata dal
pannello, non via API**: l'importazione CSV popola i campi personalizzati, la scrittura via
API no (vedi *Limiti duri* più sotto).

Campi da mappare all'import, oltre all'anagrafica:

| Campo | Perché serve |
|---|---|
| `presenze` | quante volte è venuto → distingue nuovo da abituale |
| `data ultima presenza` | da quanto manca → innesca la catenaria di ritorno |
| `consenso marketing` | 0/1 — **senza questo non si scrive a nessuno** |

⚠️ Il campo data spesso arriva con **due formati mescolati** (`AAAA-MM-GG` e `GG/MM/AAAA`):
normalizzalo prima di usarlo per segmentare, o metà lista sparisce dai filtri.

### A2 · Gestionale prenotazioni → CRM

Devono arrivare sul contatto: giorno, orario, numero di persone, stato, fonte.

**Verifica su una prenotazione vera.** La catena impiega ~15 minuti: **aspetta almeno 20
minuti prima di dichiararla rotta.** Una diagnosi affrettata qui ha già prodotto due falsi
allarmi («il workflow salta i contatti esistenti», «la fonte si perde nel travaso»),
entrambi smentiti.

⚠️ **Non cercare il contatto in cima alla lista dei più recenti**: la lista è ordinata per
data di *creazione*, quindi un cliente già in rubrica che prenota oggi non compare mai in
alto. Cercalo per nome o email.

### A3 · Il tag dell'arrivo

Il gestionale distingue *confermato* da *arrivato*. Solo il secondo conta: le prenotazioni
si disdicono, le persone sedute no.

Verifica che qualcuno in sala lo esegua davvero, contando i tag su un campione di contatti
recenti. Su un campione di 100 al Noolas: 52 prenotazioni, **26 arrivati** — la procedura
era viva, non scritta e mai applicata.

### A4 · L'informativa

Apri l'URL e **leggi il contenuto**. Una policy disattivata risponde `200` e dice
«La Privacy Policy di questo Sito Web non è più attiva». Senza informativa attiva restano
scoperti popup, newsletter e moduli — non solo l'eventuale caricamento dati alle
piattaforme.

---

## FASE B — Il sito

### B1 · Pixel e analytics

**Mai dentro il contenuto di una pagina.** Al Noolas il pixel viveva dentro il blocco di
una home fatta col page builder: cambiando home è uscito dal sito e per settimane nessuno
se n'è accorto.

Su WordPress la via robusta è un **mu-plugin** (`wp-content/mu-plugins/`): si carica da sé
senza attivazione, copre ogni pagina, e per rimuoverlo basta cancellare il file.

Va marcato per il consenso, con la stessa regola già usata dal sito per l'analytics:

```html
<script type="text/plain" class="_iub_cs_activate" data-iub-purposes="4">…</script>
```

⚠️ Se il cliente ha una landing su un **sottodominio servito da un'altra piattaforma**,
quella non eredita né pixel né banner: vanno installati a parte. La via che non costringe a
reincollare codice ogni volta è un unico `tracking.js` sul server del cliente, caricato
dalla landing.

### B2 · La sorgente parlante

È il pezzo che rende nominativa tutta la misura a valle. Al clic su un pulsante di
prenotazione si riscrive il link in un **link diretto** al gestionale, con una `source`
che dice **pagina + canale**:

```
https://app.<gestionale>.com/<slug>/widget?source=sito-il-menu.google
```

Il canale si ricava dal codice del clic pubblicitario presente nell'URL di atterraggio:

| Parametro trovato | Canale |
|---|---|
| `gclid`, `gbraid`, `wbraid` | `google` |
| `fbclid` | `meta` |

Si conserva in `localStorage` per 30 giorni, **solo se il consenso è stato dato**.

🔑 **Separatore: il PUNTO.** Verificato: `|` diventa `%7C` e `~` diventa `%7E` passando da
`URLSearchParams`, mentre `.` e `_` passano intatti.

🔑 **Lo script deve essere difensivo**: ogni errore lascia il link intatto. Un pulsante di
prenotazione rotto costa più di una misura mancante.

### B3 · L'evento di conversione

Due livelli da non confondere:

1. L'evento arriva ad Analytics → **contrassegnalo evento chiave**
2. Importalo nella piattaforma pubblicitaria → **verifica che sia attribuito alla singola
   campagna**, non solo all'account

⚠️ **Gli obiettivi «specifici per la campagna» scavalcano i predefiniti dell'account.** Una
campagna può ignorare completamente la conversione che hai appena impostato come
predefinita. Al Noolas questo ha prodotto tre giorni di diagnosi sbagliata su ritardi di
consolidamento e modelli di attribuzione. Si controlla in:
*campagna → impostazioni → Obiettivi di conversione*.

⚠️ **Una sola conversione guida le offerte.** Due azioni che descrivono lo stesso gesto
(clic sul pulsante e apertura della pagina) contano la stessa persona due volte, e la
piattaforma ci calcola sopra quanto pagare il clic successivo.

---

## FASE C — La macchina dell'offerta

### C1 · Modulo di cattura

Nome, email, telefono. Nient'altro: ogni campo in più è gente che abbandona.

Se la campagna è su Meta, usa il **modulo istantaneo** dentro la piattaforma, tipo
«intenzione più elevata» (aggiunge un passaggio di conferma: è il filtro contro i tocchi
per sbaglio).

⚠️ **Un modulo istantaneo, una volta creato, non è più modificabile**: si può solo
duplicare. Tienilo in bozza finché il cliente non l'ha approvato.

### C2 · Il modulo di riscatto — uno per offerta, duplicato dallo stesso originale

**Ogni offerta ha il SUO modulo di riscatto**, duplicato dall'originale così i campi e
l'aspetto restano identici. In cassa il gesto resta uno — si inquadra il QR e basta —
perché **è il QR a sapere di quale offerta è**: ogni QR punta al modulo della sua offerta.

⛔ **Perché non un modulo condiviso** (era la regola iniziale, si è rivelata sbagliata):
ogni automazione di riscatto ascolta il proprio modulo. Se due offerte ascoltano lo stesso
modulo, chi ha scaricato entrambi i coupon se li vede marcare *utilizzati* tutti e due con
un solo invio — i conteggi dei riscatti diventano falsi e il cliente perde un coupon mai
usato. Trovato sui dati veri: un contatto di prova portava tutti e quattro i tag.

Se un modulo condiviso è già in circolazione dentro QR già consegnati, **quello non si
tocca** (i QR nelle caselle della gente puntano lì): l'offerta nuova prende un modulo
duplicato nuovo, e si rinomina il vecchio perché dica a quale offerta serve. I trigger
seguono l'id, non il nome: rinominare è sicuro.

Campi:

| Campo | Chi lo riempie | Obbligatorio |
|---|---|---|
| nome, cognome | il QR | no |
| telefono, email | il QR | **sì** |
| **coperti** | il collaboratore | **sì** |
| **scontrino** | il collaboratore | **sì** |

🔑 **Prima di costruire il prefill, leggi quali campi sono obbligatori** (negli attributi
`data-required` dell'HTML del modulo pubblicato). Un campo obbligatorio non precompilato
blocca la cassa, e te ne accorgi col cliente davanti.

🔑 **Il campo va preso dalla sezione dei campi del CRM, non dalla libreria di elementi
generici.** Trascinando l'elemento generico si crea un contenitore con un nome a caso
(`monetary_5xk3`) che non scrive su nessun campo del contatto. **La verifica è la chiave
del campo**: deve essere il nome che hai dato, non `<tipo>_<casuale>`.

🔑 Il costruttore **si tiene in cache l'elenco dei campi**: un campo creato un minuto prima
non compare finché non ricarichi la pagina. E i campi nuovi finiscono **in fondo**
all'elenco, non in ordine alfabetico.

⚠️ **I decimali vogliono il punto.** Verificato: `27,80` viene salvato come **`2780`**,
senza errore e senza avviso — un importo cento volte più grande. Delle due l'una: o
l'etichetta impone il punto con un esempio visibile, o si tolgono i centesimi e si scrivono
solo gli euro interi. **La seconda è più robusta**: elimina la possibilità dell'errore
invece di doverla sorvegliare, e i centesimi non cambiano nessuna decisione.

### C3 · Il QR

**Non è un codice sconto: è il link al modulo di riscatto, già precompilato coi dati di
quella persona.** In cassa si inquadra con la fotocamera del telefono — nessuna app,
nessun lettore.

Si costruisce sui campi del contatto e si trasforma in immagine con un servizio pubblico:

```
https://api.qrserver.com/v1/create-qr-code/?size=320x320&margin=10&data=<URL-DEL-MODULO-CODIFICATO>
```

⚠️ **Dentro `data=` il `?` deve restare `%3F` e le `&` devono restare `%26`.** Se si
riscrivono come caratteri normali il QR apre un modulo vuoto e in cassa non si riconosce
nessuno. Le codifiche sopravvivono all'editor email se si incolla l'HTML nella vista codice.

⚠️ **Il telefono va sempre passato nel prefill**, non solo l'email: se è obbligatorio e
resta vuoto, il collaboratore non può inviare senza farsi dettare il numero.

🔴 **Il merge field del telefono NON restituisce il numero salvato ma la versione
formattata per gli umani** — con gli spazi e senza prefisso (`333 123 4567` invece di
`+393331234567`). Tre spazi dentro l'`src` dell'immagine = URL non valido: **il client di
posta non riesce nemmeno a chiedere il PNG e il QR non si vede**. Gmail ripulisce l'URL e
maschera il difetto; Outlook e iPhone no — per questo resta invisibile per settimane se
si prova solo su Gmail. **Nel QR va usato il merge field "raw" del telefono**
(`{{contact.phone_raw}}` in GoHighLevel, che restituisce `+39...` senza spazi) **e il
nome non si passa affatto**: spesso contiene nome+cognome con lo spazio, e al
riconoscimento non serve — il riconoscimento avviene sull'email.

🔴 **Su Outlook/Hotmail il QR può non vedersi comunque**: se il mittente non è considerato
fidato, Outlook non scarica le immagini e mostra il riquadro col testo alternativo. Non
c'è URL da correggere. Le due difese, entrambe:
1. sotto il QR, una **riga di testo** con l'email del cliente (`{{contact.email}}`): il
   testo si vede in qualunque posta e in cassa basta quella per il riscatto manuale;
2. in cassa, un **segnalibro per ciascun modulo di riscatto** (l'URL del modulo, aperto
   senza parametri): il collaboratore scrive email e dati a mano. I segnalibri **non sono
   intercambiabili** — ognuno segna la sua offerta. Il tag *utilizzato* scatta solo se il
   contatto ha già *scaricato*, quindi un'email sbagliata non crea un riscatto falso.

### C4 · Le due automazioni

**Consegna** — trigger: invio del modulo di cattura
```
Add Tag «coupon <offerta> scaricato»
  → EMAIL 1 (col QR)
  → attesa 3 giorni → se ha già il tag «utilizzato» → FINE
  → EMAIL 2 (sollecito)
  → attesa 4 giorni → se ha già il tag «utilizzato» → FINE
  → EMAIL 3 (ultimo giro, con la scadenza ancora davanti)
```

**Riscatto** — trigger: invio del modulo di riscatto · **rientro CONSENTITO**
```
Se il contatto ha il tag «coupon <offerta> scaricato»
  → Add Tag «coupon <offerta> utilizzato»
Altrimenti
  → ramo vuoto: un coupon mai emesso non si può riscattare
```

⚠️ **Il rientro dev'essere consentito** sul secondo: lo stesso modulo serve ogni cliente a
ogni visita, col rientro bloccato la seconda volta non partirebbe. Sul primo invece il
rientro **spento** è la scelta giusta (l'offerta si prende una volta sola) — ma ricordalo
quando provi: un contatto già passato nel workflow **non rientra mai più**, qualsiasi tag
gli si tolga. Ogni prova vuole un'email mai usata.

🔴 **Controlla la finestra oraria di comunicazione del workflow** (*Settings →
Communication → Time window*). Se è impostata tipo 11:00–21:00, chi scarica il coupon
dopo le nove di sera — l'ora esatta in cui la gente cerca dove andare a cena — non riceve
niente fino alle 11 del mattino dopo. Per un locale serale va allargata fino a chiusura o
tolta. È un'impostazione silenziosa: nessun errore, l'email parte solo il giorno dopo.

⚠️ **Nelle email del CRM solo ASCII + entità HTML** (`&mdash;` `&euro;` `&egrave;`).
I caratteri UTF-8 incollati diretti nella vista codice diventano spazzatura nell'email
consegnata (`,Äî 19,80 ,Ç¨` al posto di `— 19,80 €`). Nell'editor si vede tutto giusto:
il difetto compare solo nell'email ricevuta.

⚠️ **I tag non si ripuliscono da soli.** Alla seconda tornata della stessa offerta chi l'ha
già usata salta i solleciti: aggiungi un nodo che rimuove i due tag all'ingresso.

⚠️ Convenzione dei tag: **segui quella già presente nell'account del cliente**. Non
inventare `coupon-emesso`/`coupon-riscattato` se lì dentro si usa
`coupon <offerta> scaricato` / `utilizzato`.

### C5 · La prova end-to-end

Non «sembra funzionare»: si rilegge il dato arrivato.

1. Apri il QR **dal telefono**, non da `curl` — gli strumenti da riga di comando rifiutano
   gli spazi grezzi che i client email e iOS codificano da soli. Non trasformare il
   comportamento di `curl` in una diagnosi sul telefono del cliente
2. Verifica che il modulo si apra **precompilato**
3. Scrivi coperti e importo, invia
4. **Rileggi il contatto** e controlla tre cose: che i valori ci siano, che siano **numeri e
   non stringhe** (altrimenti nessuna somma funzionerà, e lo scopri fra tre mesi), e che il
   telefono non sia stato sovrascritto
5. **Leggi l'HTML dell'email davvero consegnata** (dal CRM, non dall'anteprima
   dell'editor): l'editor mostra i merge field non risolti, quindi il QR lì dentro sembra
   sempre giusto. I difetti — spazi nell'URL, caratteri storpiati — si vedono solo
   nell'email arrivata. E prova la ricezione anche su un indirizzo **non Gmail**: Gmail
   ripulisce gli URL e nasconde i difetti che Outlook e iPhone mostrano

---

## FASE D — La pubblicità

- **Il front end resta dentro la piattaforma.** Con un modulo istantaneo non si perde nessuno
  per strada; mandando al sito, gran parte del traffico non arriva mai
- **Scadenza e giorni validi.** Un'offerta senza scadenza diventa l'insegna sopra la porta.
  I giorni si scelgono dove la sala ha posto, non dove è già piena
- **Escludi l'anagrafica esistente dal pubblico.** Al Noolas non fu fatto subito: **il 67%
  dei contatti raccolti dal front end era già in rubrica**, cioè due terzi del budget hanno
  pagato per recapitare un buono a gente raggiungibile per email a costo zero
- **Il prodotto del front end è il nome**, non il piatto regalato. Se l'offerta non prende
  un contatto, è solo uno sconto

---

## Limiti duri da conoscere prima, non dopo

### GoHighLevel via API

| | |
|---|---|
| Leggere tutto (contatti, campi, tag, attribuzione) | ✅ |
| Applicare e togliere tag | ✅ |
| Campi standard (nome, email, telefono, città) | ✅ |
| **Scrivere nei campi personalizzati** | ❌ risponde «riuscito» e non scrive |
| **Creare campi personalizzati** | ❌ |
| **Creare o modificare moduli e workflow** | ❌ API in sola lettura |

**Conseguenza:** ogni contatore che deve vivere nel tempo si costruisce **sui tag**, non sui
campi. I campi si popolano da un modulo compilato o da un'importazione.

**Conseguenza 2:** moduli e workflow li monta il cliente (o il collega) a mano. Si prepara
la specifica passo per passo, non la si esegue.

### Paginazione dei contatti

`startAfter` da solo viene ignorato: servono **`startAfter` e `startAfterId` insieme**,
letti dalla risposta precedente. Ogni pagina da 100 va processata in uno script, mai letta
a mano.

### L'attribuzione pubblicitaria è già lì e nessuno la legge

Ogni contatto porta un array `attributions` con `adSource`, `utmCampaign`, `utmMedium`
(il gruppo di inserzioni), `utmContent` (il nome dell'inserzione), `utmAdId`. **Per Meta
questo è un segnale migliore della fonte del gestionale**: dà campagna, gruppo e singolo
annuncio, con nome e telefono della persona.

### Conversioni offline verso Google: non funzionano se la prenotazione è su un dominio di terzi

Le *conversioni avanzate per i lead* agganciano l'identificativo caricato a quello che il
tag Google aveva già raccolto **sul tuo sito** al momento del clic. Se la prenotazione
avviene su un dominio del gestionale, quel dato non è mai stato visto: **27 righe caricate,
0 riconosciute**, comprese quelle di persone che venivano davvero da Google Ads.

Non è un errore di formato. Non riproporre questa strada senza aver prima risolto il punto
di raccolta.

⚠️ **E non pubblicare mai un file di hash su un URL aperto**: un SHA-256 di numero di
telefono italiano si inverte con una rainbow table in pochi minuti.
