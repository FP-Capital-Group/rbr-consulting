# Trappole WordPress: dettagli tecnici richiamati da SKILL.md

Riferimenti puntuali per i casi in cui il connettore MCP non basta o il sito nasconde
comportamenti non ovvi. Verificato sul campo da Andrea Chirivì (contributi raccolti fino al
12/10/2026, alcuni già in coda dal 12-13/09).

## Plesk: una cartella omonima scavalca la pagina WP
Una cartella fisica in `httpdocs` con lo stesso slug di una pagina (es. `httpdocs/cassa/index.html`)
serve il suo contenuto, mentre la pagina WordPress resta pubblicata e invisibile. Sintomo: il sito non
corrisponde al database, le revisioni sembrano sparite. Ordine di diagnosi quando una pagina "non si
aggiorna": 1) via FTP, cerca una cartella omonima in `httpdocs`; 2) cache di pagina (vedi sotto); 3)
solo dopo, il database. Togliendo la cartella la pagina WP torna a rispondere.

## Contenuti che WordPress riscrive
1. **wpautop** inserisce `<p>` dentro gli `<script>` inline: stringhe JS con HTML danno `SyntaxError` e
   la pagina resta ferma sul caricamento. Lo stesso dentro gli `<style>` se restano righe vuote.
2. **wptexturize** trasforma `&` in `&#038;` negli script inline: `&&` e le query string si rompono in
   silenzio.
3. `€`, `—`, `·` scritti nel PHP escono come entità HTML (`&#8364;`) se finiscono in un `textContent`:
   nelle stringhe JS usa gli escape unicode (`€`).
4. Nel **CSS mai caratteri non-ASCII dentro `content:`** (`content:"·"` diventa `&#183;` a schermo): usa
   l'escape CSS `content:"\00B7"` — in una stringa Python non raw va scritto `"\\00B7"` (un solo
   backslash fa leggere `\00` come NUL).

Regola: uno script con logica va in un mu-plugin, nell'hook `wp_footer` filtrato con `is_page()`, e non
lo tocca nessuno. Se proprio resta inline: niente `&`, condizioni annidate al posto di `&&`, niente
righe vuote, tutto dentro un blocco `wp:html`. Correggi sia le pagine pubblicate sia le fonti degli
script, sennò il difetto torna. Diversa dalla regola delle email GHL (solo ASCII + entità): non
confondere le due.

## Page builder

### Brizy
Il testo vive in **tre archivi**: `editor_data` nel postmeta brizy (base64 JSON, quello dell'editor),
`brizy-compiled-sections` (base64 JSON, quello che il sito mostra davvero) e `post_content` (solo copia
per la SEO). Cambiare solo `post_content` **non cambia il sito**. Nel compilato gli accenti sono
`\uXXXX` e le virgolette hanno la barra: la ricerca col testo grezzo non trova nulla; in `editor_data`
i link sono percent-encoded (serve una coppia cerca/sostituisci per ogni forma); possono esistere
blocchi orfani solo nel compilato. Cambia il testo con un endpoint PHP dedicato che scrive tutti e tre
gli archivi, con prova a secco, acceso solo per l'intervento.

Via REST **non cambia la struttura** (Brizy la ignora). Per rifare una pagina: crea la nuova in HTML
pulito dentro un blocco `wp:html`; la vecchia prende uno slug di parcheggio e va in bozza; la nuova
prende lo slug esatto (l'URL non cambia, non serve un 301, la vecchia resta recuperabile). Aggiorna poi
l'`object_id` della voce di menu — se punta a una bozza, WordPress nasconde la voce. Lo script di
generazione dev'essere idempotente, con prova a secco.

H1 nell'editor: Modifica con Brizy → titolo → icona T → Tipografia → Heading 1. Se poi cambi la
dimensione a mano il preset diventa "Personalizzato" e il tag torna `<p>`: cambia invece il preset
globale (ingranaggio → Stile). Attenzione ai preset incoerenti (H2 più grande dell'H1). Nel testo Quill
il triplo clic sfora il paragrafo: seleziona con un `Range` JS. Il backdrop FireBox nell'editor si
nasconde con uno `<style>`, mai rimuovendo nodi (React va in crash).

### Elementor
Il codice di tracciamento spesso non è nel tema ma negli snippet di Elementor Pro → Codice
personalizzato, su `/wp-json/wp/v2/elementor_snippet` (meta `_elementor_location`,
`_elementor_priority`, `_elementor_code`, in `context=edit`). Le condizioni di visualizzazione NON sono
esposte in REST: uno snippet creato via API rischia di non comparire da nessuna parte — accoda il
codice a uno snippet esistente già in head invece di crearne uno nuovo.

Per footer/header: leggi `meta._elementor_data` in `context=edit`, sostituisci la stringa e rimandala in
POST. Gli URL nel JSON hanno gli slash escapati (`https:\/\/`). Dopo il salvataggio servono ENTRAMBI gli
svuotamenti: Elementor → Strumenti → "Cancella file e dati", poi "Cancella cache" nella barra admin.
Le pagine Elementor non si modificano via API: si clonano.

(contributo per Elementor: Luciano Purpi, skill sistema-locale-completo)

## Pubblicare PHP e file via FTP
**FTP**: usa il dominio come host (segue da solo le migrazioni dell'hosting). Il certificato può non
corrispondere al dominio: con `curl -k` il canale è cifrato ma l'identità non è verificata, va accettato
consapevolmente. Con `curl --ssl-reqd` i file sopra ~16 KB si troncano (426, file vuoto sul server)
perché ProFTPD pretende il riuso della sessione TLS sul canale dati: carica con Python
`ftplib.FTP_TLS` + `prot_p` sottoclassato (`ntransfercmd` con `session=self.sock.session`) oppure con
`--ftp-ssl-control`, poi **riscarica e confronta**. L'FTP non dà né database né DNS; controlla se esiste
una cartella di staging.

**PHP**: un errore di parsing in un mu-plugin manda giù TUTTO il sito e non si disattiva da WordPress.
Prova di 10 secondi prima di mettere un file in `mu-plugins`: carica il file in `/httpdocs/` (o nello
staging) con un nome casuale e chiamalo in HTTPS con la guardia `if(!defined('ABSPATH')) exit;` — 500 =
errore, risposta vuota = sintassi buona (se il file controlla una chiave puoi vedere 403 invece di
vuoto: l'unico segnale certo è che NON sia 500). Poi cancella e sposta in `mu-plugins`. Per file grandi,
una copia `-collaudo.php` o una modalità `?prova=1` prima di sostituire il vero, con backup del
precedente. Trappola: un commento `//` a metà riga si mangia il resto della riga e dà 500. Cancella
sempre i file di diagnosi lasciati sul server a fine intervento.

Nota: "FTP semplice senza TLS" è una pratica superata — usa sempre `FTP_TLS`.

## Codice globale (CSS/JS/PHP)
1. Con la password per applicazioni, **Code Snippets** espone
   `/wp-json/code-snippets/v1/snippets[/<id>]` in lettura e scrittura (campo `code`; scope
   `head-content` per CSS/HTML nel `<head>`): CSS e JS globali in pochi secondi, senza toccare il page
   builder. Cancellare uno snippet via REST dà 500: disattivalo invece.
2. **WPCode** non espone nulla in REST (404), si tocca solo da wp-admin. Per battere una sua regola che
   non puoi modificare, ripeti la classe CSS (`.classe.classe`): la specificità sale e vince a
   prescindere dall'ordine di stampa.
3. **mu-plugin** (`wp-content/mu-plugins/`): si carica da solo, copre ogni pagina, si toglie cancellando
   il file. Va bene per redirect a mappa, noindex, pixel sotto consenso, CSS correttivo, barra fissa.
   Tieni sempre una copia locale di ogni file. Si pubblica solo con l'ok del titolare e dopo averlo
   mostrato — mai come aggiramento silenzioso di un blocco.

## Cache di pagina (WP-Optimize e simili)
Una verifica con `?cb=<casuale>` (o qualunque query string) salta la cache: vedi l'HTML giusto mentre il
visitatore reale riceve quello vecchio, anche con 200 su una pagina ritirata o un menu vecchio. Per
sapere cosa vede il cliente, controlla l'header `wpo-cache-status` su una richiesta SENZA query string.
Dopo ogni modifica lato server (menu, pagine, snippet, head, PHP), home compresa, svuota la cache prima
di concludere che "non ha preso". Via FTP si cancellano `wp-content/cache/wpo-cache/<dominio>/<slug>/index.html`
e il `.gz`, lasciando `index.php`. Può esistere una seconda cache (es. plugin di ottimizzazione diverso).

## Moduli e pagine che parlano con GHL
Un mu-plugin espone `/wp-json/<cliente>/v1/…`, valida, normalizza il telefono in `+39` e chiama GHL lato
server. La chiave GHL sta come costante in `wp-config.php` (backup prima), mai nel database né nel
plugin. Un endpoint pubblico (es. saldo) restituisce il minimo (nome di battesimo, saldo) e verifica che
il contatto appartenga alla location giusta.

Il collaudo vale **solo** compilando dalla pagina vera fino al contatto creato nel CRM: un endpoint può
rispondere bene a `curl` mentre il JS legge un `id` sbagliato (es. legge `ca_nome.value` ma l'id HTML è
`ca-nome` — gli id col trattino non diventano variabili globali, restano `undefined`, e il modulo non
ha mai funzionato pur sembrando a posto). Cancella i contatti di prova dopo il collaudo.

Per una pagina-app installabile sul telefono (cassa, conto cliente): manifest e icone dedicate; togli
l'icona del sito WordPress su quelle pagine se è nera su trasparente (su iOS diventa un quadrato nero).
Chi ha già l'icona sulla home del telefono deve toglierla e rimetterla. Dopo ogni modifica all'head,
svuota la cache della pagina.

## Pagine generate da script
Più pagine possono condividere un solo foglio di stile sorgente e nascere da script idempotenti: senza
argomenti fanno la prova a secco, con `--scrivi` pubblicano, e se la pagina esiste la riscrivono invece
di duplicarla. I numeri che cambiano (es. conteggio recensioni) stanno in una costante sola. Il tema
colora i titoli e vince sull'ereditarietà: ogni tag titolo va riportato al colore giusto a mano. Prima
di ogni rilancio controlla una regola-spia nel foglio sorgente (è capitato che il sorgente tornasse
indietro da solo). Variante utile: una pagina come `/eventi/` rigenerata via REST da un file dati unico
(`eventi.json`) — è HTML statico per la SEO e si aggiorna SOLO rilanciando lo script.

## Blog WordPress (parte tecnica — cosa scrivere resta in `seo-local-ristorante`)
Ogni articolo ha bisogno dell'immagine in evidenza, senza la quale l'elenco resta bianco; se manca una
foto pertinente si genera una copertina tipografica. Il nome dell'autore sta in tre posti (riga sotto il
titolo, meta author, JSON-LD): il CSS ne copre solo uno, quindi rinomina l'utente WordPress se serve.
`posts_per_page` si imposta dalle impostazioni REST. Oltre 4-5 articoli per chiamata REST si superano i
2 minuti: pubblica a blocchi, saltando gli slug già presenti.

## Pop-up FireBox modificati via REST
`GET`/`POST /wp-json/wp/v2/firebox/<id>?context=edit` legge e scrive il contenuto (`content.raw`,
blocchi Gutenberg) e le regole di visualizzazione (`meta.firebox_meta.rules`, es.
`{"name":"WP\\Pages","operator":"includes","value":["<id>"]}`). Backup prima, cache svuotata dopo. Si
può escludere il traffico di marca a pagamento (parametro dedicato nell'URL dell'annuncio) perché non
veda il pop-up. Il contenitore vero per il CSS è `#dialog<ID>.fb-dialog › .fb-container › .fb-content`,
non `.fbox-content`.

## Sito lento: hosting, nostro codice o avvio di WordPress?
(1) **Hosting o codice**: confronta il server web sull'IP diretto (es. 0,2 s) con l'account (10-18 s
anche su file statici e 404). Misura la latenza di notte coi client spenti: se resta alta è l'hosting.
Uno script di sola lettura dà il load medio (12-16 = macchina condivisa sovraccarica) e va cancellato
dopo l'uso. Confronto utile: un altro hosting dello stesso fornitore. Un `flock` bloccante e chiamate
HTTP del sito verso sé stesso possono trasformare un rallentamento in un blocco. Il piano condiviso
superiore non garantisce risorse: ha senso solo il semidedicato.
(2) ⚠️ **Ipotesi, non regola accertata**: se solo le richieste NON in cache sono lente (`wp-json`,
`wp-login`, redirect a 30-40 s costanti) mentre le pagine in cache e i PHP fuori da WordPress rispondono
in 0,1-0,5 s, il blocco è probabilmente nell'avvio di WordPress (plugin o database) — da confermare caso
per caso con un mu-plugin diagnostico che misura i tempi degli hook e delle chiamate HTTP in uscita,
solo col via libera del titolare.

(contributi di Andrea Chirivì, 12/10/2026, salvo dove diversamente indicato)
