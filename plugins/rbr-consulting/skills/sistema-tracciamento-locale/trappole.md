# Trappole — le lezioni già pagate

Ognuna di queste è costata giorni di lavoro o soldi veri su un cliente vero. Rileggile
**prima** di ogni intervento, non dopo il danno.

---

## Sul metodo di diagnosi

**Prima di dichiarare rotto un pezzo, verifica come quel pezzo viene usato davvero.**
Un `curl` che restituisce errore su un URL con spazi non dice niente sul telefono del
cliente: i client email e iOS codificano gli spazi da soli. Una diagnosi da riga di comando
non è una diagnosi sul campo.

**Aspetta prima di dichiarare rotta una catena lenta.** La sincronizzazione
gestionale → CRM impiega ~15 minuti. Due falsi allarmi sono nati da controlli fatti dopo
tre.

**Un conteggio sbagliato dallo strumento non è un guasto del sistema.** Un `grep` in shell
che dava «pixel assente» era un artefatto di encoding: il pixel c'era. Rifai i conteggi in
Python prima di annunciare un guasto.

**Quando una nota dice che qualcosa è rotto, deve dire come è stato verificato e quando.**
Una nota imprecisa si propaga: ogni sessione che la rilegge ne ricava la stessa conclusione
sbagliata. Non è l'errore di una chat, è l'errore del taccuino.

---

## Sul tracciamento

**Cambiare il percorso di un clic spegne le misure che poggiavano sul passaggio tolto.**
Migliorando la sorgente dei link di prenotazione si è accecata per tre giorni la conversione
principale di Google Ads, che contava l'apertura di una pagina che nessuno caricava più.
👉 *Quando cambi un percorso, controlla subito quale conversione stava sopra il passaggio
che hai rimosso.*

**Un pixel dentro il contenuto di una pagina è un pixel che sparirà.** Basta che qualcuno
rifaccia la home.

**Un blocco «incorpora» di un page builder gratuito non esegue il codice: lo stampa a
schermo.** Per un anno i clienti hanno visto due blocchi di codice in pagina e la
piattaforma non ha ricevuto un dato.

**Due conversioni che descrivono lo stesso gesto gonfiano l'ottimizzazione.** Una sola
guida le offerte; le altre restano misure di controllo.

**Gli obiettivi «specifici per la campagna» scavalcano quelli dell'account.** Si può
impostare tutto correttamente a livello generale e non funzionare comunque.

**Il conteggio «ogni conversione» invece di «una» gonfia del ~70%** quando lo stesso utente
ripete il gesto.

**Le azioni locali (indicazioni stradali, chiamate, visite in negozio) arrivano con 3-5
giorni di ritardo** e vengono attribuite alla data del clic: riempiono i giorni
all'indietro. 👉 *Gli ultimi 3-4 giorni non si leggono mai come definitivi, e nessun
confronto fra periodi deve includerli.*

**Il banner dei cookie fa sparire dal 25% al 90% dei clic dichiarati dalle piattaforme.**
Non è traffico finto: è misurazione mancante, e vale per tutti i canali. Prima di
concludere «questa piattaforma mente», confronta il suo traffico **organico** col suo
traffico **a pagamento**: stessa app, stesso browser, e la differenza che resta è qualità
del traffico, non tecnologia.

---

## Sui moduli e sul CRM

**Prima di costruire un prefill, leggi quali campi sono obbligatori.** Un campo
obbligatorio non precompilato blocca la cassa, e non si scopre finché non c'è un cliente
davanti.

**L'elemento generico della libreria non è il campo del CRM.** Trascinandolo si crea un
contenitore con un nome casuale che non scrive da nessuna parte. 👉 *La verifica è la
chiave del campo.*

**Il costruttore si tiene in cache l'elenco dei campi**: un campo creato un minuto prima non
compare finché non ricarichi la pagina. E i campi nuovi finiscono **in fondo** alla lista.

**La virgola nei decimali viene ignorata:** `27,80` → `2780`. Senza errore, senza avviso.

**Due offerte sullo stesso modulo di riscatto si marcano a vicenda.** Ogni automazione
ascolta il proprio modulo: se il modulo è condiviso, un solo invio marca *utilizzati*
entrambi i coupon di chi li ha tutti e due. Un modulo per offerta, duplicato dallo stesso
originale — il gesto in cassa resta uno perché è il QR a sapere di quale offerta è.

**Il merge field del telefono restituisce il numero formattato, con gli spazi e senza
prefisso.** Dentro l'`src` dell'immagine del QR quegli spazi rendono l'URL invalido: il QR
non si vede su Outlook e iPhone, mentre Gmail ripulisce e maschera il difetto. Nel QR si
usa il merge field *raw* del telefono e il nome non si passa affatto. 👉 *Le prove di
ricezione non si fanno solo su Gmail.*

**Su Outlook il QR-immagine può non vedersi mai** finché il mittente non è fidato: Outlook
non scarica le immagini, punto. La difesa è una riga di **testo** con l'email del cliente
sotto il QR, più il riscatto manuale in cassa (segnalibro del modulo, uno per offerta).

**I caratteri UTF-8 incollati nelle email del CRM diventano spazzatura** (`,Äî` al posto
di `—`). Solo ASCII + entità HTML, e la verifica si fa sull'email consegnata, non
nell'editor.

**La finestra oraria di comunicazione del workflow blocca le email serali in silenzio.**
Impostata 11–21 su un locale che vive di sera, chi scarica il coupon dopo le 21 riceve il
QR alle 11 del giorno dopo. Nessun errore da nessuna parte: si scopre solo guardandola.

**Un contatto già passato in un workflow senza rientro non rientra mai più**, qualsiasi
tag gli si tolga. Ogni prova end-to-end vuole un'email mai usata prima.

**Un numero di telefono senza prefisso internazionale blocca il salvataggio** del profilo
aziendale, e l'errore è una scritta rossa piccola che non impedisce di cliccare Salva.

**I tag non si ripuliscono da soli.** Alla seconda tornata della stessa offerta, chi l'ha
già usata salta i solleciti.

**La lista contatti è ordinata per data di creazione:** un cliente già in rubrica che
prenota oggi non compare mai in cima. Ha prodotto due diagnosi sbagliate di fila.

**Se il CRM è in subaffitto da un'agenzia, i workflow possono essere condivisi con altri
clienti.** Modificarne uno esce dal locale e colpisce aziende di terzi, e comunque viene
sovrascritto al prossimo aggiornamento. 👉 *Le correzioni si chiedono, non si applicano.*

**La traduzione automatica del browser riscrive i menu mentre ci clicchi dentro.**
Disattivala prima di lavorare in un pannello.

---

## Sulla pubblicità

**Le piattaforme riaccendono da sole quello che spegni.** Musica, animazioni, generazione
di testi e immagini: vanno ricontrollate su **ogni** inserzione nuova e su **ogni**
duplicazione — la finestra di duplicazione ripropone di sua iniziativa le opzioni appena
disattivate.

**I campi di testo perdono caratteri mentre digiti.** Succede anche su stringhe corte.
👉 *Scrivi a pezzi di 10-20 caratteri e rileggi ogni campo prima di passare oltre.*

**Prima di pubblicare, spunta la singola campagna nella lista.** Il pulsante generale
manderebbe online tutte le bozze in sospeso, comprese quelle vecchie di mesi. E il pulsante
«Duplica» sta subito accanto a «Pubblica», in una barra che cambia disposizione quando
selezioni una riga.

**Verifica l'account prima di toccare qualsiasi cosa.** Aprendo il gestore inserzioni si
finisce spesso su un account diverso da quello del cliente, con i suoi avvisi che non ti
riguardano.

**Il profilo social collegato all'inserzione torna da solo su quello sbagliato** a ogni
inserzione nuova, quando l'account ne gestisce più d'uno.

**Un posizionamento può bruciare metà budget in tocchi accidentali.** Al Noolas un solo
posizionamento comprava il 43% dei clic della campagna, e il 97,7% di quei clic non arrivava
mai sul sito.

**Il punteggio della campagna scende quando rifiuti i suggerimenti automatici.** Non è un
difetto: è il prezzo di tenere il controllo del messaggio.

---

## Sulle immagini e sui testi

**Su un'offerta di cibo l'immagine è il prodotto.** Foto del locale per gli eventi, foto del
piatto per le offerte su un piatto. E mai illustrare un'offerta con un prodotto che
dall'offerta è escluso.

**Prima di riusare una grafica dall'archivio, leggi la data stampata dentro l'immagine.**
Gli archivi sono pieni di locandine di edizioni passate con lo stesso titolo.

**Una landing di solo testo non si consegna.** Ogni schermata che vede un cliente — modulo,
landing, pagina di ringraziamento — vuole un'immagine.
