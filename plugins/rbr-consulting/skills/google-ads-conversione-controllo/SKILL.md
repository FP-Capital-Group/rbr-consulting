---
name: google-ads-conversione-controllo
description: Chiude il cerchio di una campagna Google Ads di un ristorante — crea la conversione «Prenota» sul widget di prenotazione (TheFork, Resmio o simili dentro iframe), mette il tag sul sito rispettando il banner cookie, verifica che parta DOPO il consenso, lancia la campagna mettendo in pausa le Smart vecchie e imposta un controllo giornaliero automatico con riepilogo Telegram e un'unica regola di ritocco permessa. Usala quando il consulente dice "misura le prenotazioni da Google Ads", "metti il tag di conversione", "la campagna non registra conversioni", "lancia la Search e controlla ogni giorno", "il tag c'è ma non traccia", "fammi un controllo quotidiano delle ads". Il piano della campagna lo fa adv-ristorante; questa skill la rende misurabile e sorvegliata.
---

# Google Ads: conversione Prenota + controllo giornaliero

> Metodo nato su Raíces (24/09/2026). KPI nord RBR: **costo per prenotazione** — senza questa
> conversione la campagna ottimizza sui clic e il KPI non si può leggere.

## Prerequisiti
- Campagna Search pronta (`adv-ristorante`), MCP `google-ads` con accesso all'account del cliente.
- Accesso al sito (`sito-wordpress-ristorante` per i siti nuovi, `sito-wordpress-cliente-mcp` per quelli esistenti).
- Sapere quale banner cookie usa il sito e con che categoria blocca gli script.

## Procedura
1. **Conversione**: via MCP (`execute_google_ads_mutate`) crea una ConversionAction WEBPAGE,
   categoria BOOK_APPOINTMENT, **SECONDARIA** (osservazione), conteggio una per clic,
   valore fisso 1 €. Prendi il `send_to` (`AW-<id>/<label>`).
   ⚠️ **Standard RBR dal 03/10/2026**: la conversione **primaria** (quella su cui
   l'algoritmo ottimizza) è la **prenotazione onorata importata offline** col gclid (vedi
   sezione "Import offline delle onorate" sotto). Il clic nel widget come primaria fa
   ottimizzare sui tocchi, non sulle prenotazioni (Barresi: 42 «conversioni» contro 39
   prenotazioni vere). Finché l'import offline non è pronto si può tenere il blur-trick come
   primaria **solo temporaneamente**, scritto nella memoria cliente con la data in cui si
   passa all'offline.
   ⚠️ **Come arriva davvero il gclid a Resmio (correzione 2026-10-12, `rbr-track.js` non
   esiste nel plugin)**: il gclid viaggia in `booking_request_parameters`, MAI nel `comment`.
   Resmio riempie quel campo SOLO leggendo `document.referrer` (l'indirizzo della pagina che
   ospita il widget), e SOLO se il widget sta dentro un iframe (`parent !== window`). Il link
   diretto `app.resmio.com/...` aperto da solo NON porta mai il gclid (al Noolas: 0 su 900
   prenotazioni con la cattura via comment). Montaggio che funziona, verificato con
   prenotazione vera: (a) pagina sul dominio del locale con un iframe il cui `src` è il link
   diretto `app.resmio.com/<slug>/widget?source=…` (non il bundle `widget.js`, altrimenti la
   fonte si perde); (b) `referrerpolicy="no-referrer-when-downgrade"` sull'iframe, applicato
   dopo il consenso cookie, con ricarica dell'iframe; (c) se il gclid è solo in
   `localStorage`, rimetterlo nell'URL della pagina con `history.replaceState` per la durata
   del caricamento e poi toglierlo; (d) `gbraid`/`wbraid` viaggiano come
   `utm=gbraid_<valore>`; (e) non ricaricare l'iframe se l'utente ha già toccato il modulo.
   Il `comment` NON si usa per catturare il gclid: il ponte Resmio→GHL lo scrive nei campi
   coupon (`codicesconto`, `active_coupon_code`), e sui clienti col middleware QR il `comment`
   è il contratto `code:` di `campagna-locale`. **Non ancora provati**: iPhone/Safari e il caso
   "gclid solo in memoria" con una prenotazione vera.
2. **Evento sul widget** (il widget è un iframe cross-origin: i clic dentro non si vedono):
   - *blur trick*: su `window.blur`, se `document.activeElement` è un IFRAME con `thefork` (o `resmio`)
     nello `src` → conversione;
   - in più, clic su qualsiasi `a[href*="thefork"]` (tasti che aprono la pagina intera);
   - una sola conversione per pagina (flag `sent`).
   Modello pronto in `tag-modello.html`.
2-bis. **La conversione arriva alla campagna?** Dopo ogni azione nuova o cambiata, controlla in
   Campagne → Segmenta → Azione di conversione che la riga compaia sotto la SINGOLA campagna:
   può succedere che la scheda dell'azione conti mentre il report segmentato dà 0, perché
   l'azione è esclusa dagli obiettivi di conversione SPECIFICI della campagna (si corregge da
   ingranaggio campagna → Ottimizzazione budget e offerte → Obiettivi di conversione). Ogni
   calo o aumento di conversioni va letto segmentato per azione e con la cronologia delle
   modifiche alle azioni: un crollo può essere solo un cambio di misura, non un peggioramento.
3. **Consenso**: il blocco va messo in modo che il banner cookie lo gestisca (es. `type="text/plain"` +
   categoria statistiche/marketing, come fa il banner del sito). Mai farlo partire prima del consenso.
4. **Inserimento** in coda al footer con un marker di versione (`<!-- cliente-gads-v1 -->`), idempotente.
5. **Verifica vera, non a vista** — due passaggi nel browser:
   - con cookie RIFIUTATI: nessuna chiamata `googletagmanager`/`doubleclick`;
   - dopo «Accetta tutti»: si caricano `gtag/js?id=AW-…`, esiste `google_tag_manager['AW-…']`, partono
     `google.com/ccm/collect` e `ad.doubleclick.net/ccm`. Controlla con l'ID REALE, non col nome della funzione.
6. **Lancio**: attiva la Search, metti in **pausa le Smart** dello stesso account (si cannibalizzano),
   controlla billing APPROVED e annunci APPROVED (il primo giorno possono stare in PENDING).
   Fai l'inventario completo delle azioni di conversione prima di toccare gli obiettivi: le
   Smart dismesse lasciano spesso azioni duplicate (es. più azioni "Chiamate" tutte Primarie),
   che agganciandole doppiano il conteggio. Per le chiamate: asset di chiamata a livello
   account (monitoraggio ON, registrazione OFF), azione "Chiamate dagli annunci" aggiunta
   SEMPRE agli obiettivi specifici della campagna di ricerca (altrimenti viene esclusa anche
   se predefinita per l'account), durata minima **30 secondi** (a 60 si perdono le
   prenotazioni rapide). Un'azione appena creata non conta i clic di prima: zero conversioni
   nei primi giorni non vuol dire che è rotta (le azioni locali arrivano anche con 3-5 giorni
   di ritardo). Il click-to-call della scheda Maps non si può mettere negli obiettivi
   dell'account e si legge a mano ogni mese.
7. **Controllo giornaliero**: scheduled task (es. ogni giorno alle 9) che legge con GAQL spesa, impression,
   clic, CPC, conversioni per gruppo **e per azione di conversione** (non solo in totale) e manda il
   riepilogo su Telegram al consulente, incluso **lo stato della fatturazione dell'account e la
   pubblicazione delle campagne** (via GAQL — individua i campi con `query_google_ads_api_docs`). Il
   banner "Nuova forma di pagamento obbligatoria" in interfaccia blocca le campagne se non risolto, e
   solo il titolare può aggiungere un metodo di pagamento alternativo: il riepilogo deve dare l'allarme
   subito. **Unica modifica automatica permessa**: +0,20 € di CPC a un gruppo con 0 impression per 2
   giorni di fila, con un tetto (es. 1,50 €). Tutto il resto (budget, keyword, pausa) solo su ok del
   consulente.
8. **Controllo settimanale — tasso di cattura del gclid**: prenotazioni con `gclid` in
   `booking_request_parameters` ÷ prenotazioni arrivate da clic Google (source `.google`) nello
   stesso periodo. Se è a zero o scende, la cattura è rotta anche se il sito sembra a posto (al
   Noolas non ha mai scritto niente per 12 giorni prima di essere scoperto). Collauda al lancio
   e dopo ogni modifica allo snippet con una prenotazione vera dopo un clic vero su un annuncio
   vero, poi annullata — anche da iPhone/Safari, svuotando la cache del sito.
9. **Controllo mensile — verità contro il gestionale**: confronta le conversioni dichiarate da
   Google con le prenotazioni marcate nel gestionale come arrivate da Google (source `.google`
   su Resmio). Calcola costo per onorata e per coperto seduto: sulle Performance Max in
   particolare, separa quanto viene da chi cercava già il nome del locale (marchio) dal resto,
   perché il marchio gonfia il numero di conversioni dichiarate senza portare clienti nuovi.
   Caso reale: 28 conversioni dichiarate a 11,36 € l'una, ma solo 20 prenotazioni vere col
   badge (26,30 €/onorata, 8,09 €/coperto); il 58% della spesa andava su ricerche del nome del
   locale. Proporre di escludere il marchio dalla PMax è una decisione che prendono il
   consulente e l'agenzia del cliente, non un'azione automatica.
10. **Terreno comune**: gli obiettivi di conversione sono l'unico punto di contatto quando più
    persone lavorano sullo stesso account (es. uno sulla struttura campagne, uno sulla misura
    del ritorno). Non si cambia niente senza allinearsi, perché ogni modifica cambia su cosa
    ottimizzano TUTTE le campagne. Ogni modifica si scrive nella memoria cliente con data e
    motivo.

## Import offline delle onorate
La conversione primaria (vedi passo 1) si costruisce così:
- **Non le conversioni avanzate per i lead** (email/telefono cifrati): quando la prenotazione
  avviene sul dominio del gestionale (Resmio) l'aggancio è quasi sempre a zero righe. La strada
  è l'**Importazione dai clic col gclid**: colonne Google Click ID / Conversion Name /
  Conversion Time / Conversion Value / Conversion Currency (modello standard di Google, da
  confermare sul file scaricato dal pannello al primo caricamento), più `Parameters:TimeZone=+0200`.
  In alternativa l'MCP `upload_google_ads_click_conversions`.
- **Categoria "Lead convertito"**, non "Prenotazione appuntamento" (che guida già le offerte e
  si inquinerebbe). Nome azione identico alla colonna Conversion Name. **Conteggio "Ogni
  conversione"**: ogni visita è un evento vero, è un'eccezione motivata alla regola "una per
  clic" che vale per i clic sul sito. Finestra clic 90 giorni.
- ⚠️ **Da verificare** (azione mai ricevuto un caricamento vero): valore con "usa valori
  diversi" = coperti × scontrino medio senza IVA, così un tavolo da 20 vale dieci volte uno da
  2; e le colonne esatte del CSV del gclid.
- Un'azione in stato "Inattivo" con 0 conversioni non ha una casella da spuntare: non le è mai
  arrivato un dato, si sistema solo col primo caricamento vero.
- **Fogli Google è l'unica origine programmata sicura** (mai un hash su un URL HTTPS aperto). Il
  foglio va condiviso con l'account di servizio di Google Ads
  `987223412-100000002-account@partnercontent.gserviceaccount.com` (compare con una barra
  rovesciata davanti, è un artefatto dell'interfaccia): senza condivisione l'anteprima dice
  "File non trovato", e il connettore Drive non basta — condivide il titolare del foglio. Le
  due dichiarazioni (termini sui dati clienti, consenso utenti UE) impegnano la società verso
  Google: le fa o le autorizza per iscritto il titolare, mai il consulente da solo, e serve
  un'informativa attiva che citi la misurazione.
- Controlli prima di ogni caricamento: valore e valuta sempre insieme (valore vuoto con EUR fa
  rifiutare le righe); nessuna data nel futuro (Google rifiuta le conversioni con data futura —
  ⚠️ per i locali che chiudono dopo mezzanotte è da verificare se lo slittamento di data nasce
  in Resmio o nel ponte verso GHL: le date future vanno comunque escluse o corrette).
- **Passaggio di consegne fra conversioni primarie** (blur-trick/evento → onorata offline,
  vecchia azione → nuova), sempre con questa sequenza: (1) prima del primo caricamento riuscito,
  porta l'azione nuova a **Secondaria** se è già negli obiettivi dell'account (misurata ma non
  guida le offerte); (2) promuovila a Primaria solo quando compare sotto la campagna con un
  numero suo e il volume regge (Massimizza le conversioni vuole circa 30 conversioni/mese); (3)
  la vecchia azione NON si toglie prima — lasciarla attiva insieme alla nuova per i primi giorni
  evita giorni a zero conversioni con l'offerta automatica senza segnale; appena la nuova
  attribuisce con regolarità, la vecchia si toglie SUBITO (lasciarla oltre tiene un doppio
  conteggio e falsa il CPA).

## Regole RBR & trabocchetti
- Il nome account nell'MCP può uscire «Unknown»: identifica sempre per customer ID.
- Il gruppo «conquest» sui competitor: il nome del concorrente mai nei testi degli annunci.
- Sitelink e callout coerenti col sito: se il sito non ha WhatsApp, nessun sitelink WhatsApp.
- Un tag «installato» ma mai verificato dopo il consenso vale zero: può restare muto per mesi.
- Se aggiungi Meta nello stesso footer, stesso metodo (evento `Schedule` sul widget) e stessa verifica.

## Definition of Done
- [ ] Conversione widget (secondaria) creata, `send_to` salvato nella memoria cliente
- [ ] Cattura del gclid verificata con una prenotazione vera (iframe sul dominio del locale, non link diretto), non col solo `comment`
- [ ] Import offline prenotazioni onorate col gclid impostato come primaria (o data prevista scritta in memoria)
- [ ] Tag online sotto consenso, verificato con cookie rifiutati E accettati
- [ ] Search attiva, Smart in pausa, annunci approvati, inventario azioni di conversione fatto (niente duplicati ereditati dalle Smart)
- [ ] Obiettivi di conversione specifici della campagna verificati (report segmentato per azione ≠ 0)
- [ ] Task giornaliero attivo con riepilogo Telegram (incluso stato fatturazione), regola di ritocco scritta nella memoria cliente
- [ ] Tasso di cattura del gclid controllato ogni settimana

## Fonti/contributi
- Pacchetto migliorie del 2026-10-12 (Andrea Chirivì, casi Noolas e Bella Ischia), costruito sulla scoperta di Luciano Purpi che Resmio tiene gclid/utm solo in `booking_request_parameters`.
