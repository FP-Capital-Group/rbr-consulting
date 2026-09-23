---
name: ottimizzazione-tavoli-resmio
description: Riorganizza l'assegnazione dei tavoli di una serata su Resmio per liberare capacità reale — ricompatta le prenotazioni già prese, sblocca le fasce che il sistema dà per esaurite e tiene sgombri i tavoli giusti per i walk-in. Usa questa skill quando l'utente manda un link alla timeline o al piano sala di Resmio, chiede di analizzare o ottimizzare l'organizzazione dei tavoli di stasera o di una data, dice che una fascia oraria non dà disponibilità o che un gruppo non entra, chiede dove incastrare una prenotazione, parla di combinazioni o accostamenti di tavoli, di walk-in, di coperti persi, di turni e rotazione dei tavoli, oppure nomina un locale cliente insieme a Resmio, timeline, piano sala, prenotazioni serali. Vale anche quando la richiesta sembra piccola ("mi trovi un tavolo per 10 alle 21?"): la risposta utile arriva quasi sempre da un riassetto, non da una ricerca.
---

# Ottimizzazione dei tavoli su Resmio

> Skill condivisa da Luciano Purpi il 2026-09-03 (scansione skill).
> Nota dell'autore: riorganizza l'assegnazione dei tavoli di una serata su Resmio per liberare capacità reale — ricompatta le prenotazioni prese, sblocca le fasce date per esaurite, tiene sgombri i tavoli per i walk-in. Risponde con i dati alla domanda che i clienti fanno di continuo («non c'è disponibilità», «dove metto un tavolo da 10»). Su un locale ha misurato ~25 posti sterilizzati al picco su 129 bloccati e un parco tavoli invertito rispetto alla domanda. Contiene anche le API Resmio in lettura/scrittura e le trappole.

Un locale che sembra pieno quasi sempre non lo è. Ha i **posti** liberi ma non i **tavoli**:
capacità sparsa in briciole da due mentre chi arriva è in tre o in quattro. Il sistema
risponde "non disponibile" con la sala al 50%.

Questo lavoro toglie le briciole di mezzo e restituisce tavoli interi.

**Leggi `api-resmio.md`** per come si interroga e si scrive su Resmio (endpoint, campi,
autenticazione) e **`trappole.md`** prima di modificare qualsiasi cosa: sono lezioni pagate
su clienti veri, e almeno due di quelle evitano di fare danni in sala.

## Il criterio che decide ogni assegnazione

**Il tavolo giusto non è quello della taglia giusta. È quello la cui finestra libera
combacia con la durata della tavolata.**

La capienza è solo un vincolo minimo. Se un quattro-posti è prenotato alle 20:00, alle 19:00
ci metti una coppia da 60 minuti invece di lasciarlo vuoto: il buco si chiude e non hai
consumato nessun altro tavolo.

Il corollario è la ragione per cui funziona: riempiendo i buchi corti, le **finestre lunghe
restano intere**. E una finestra lunga su un tavolo grande è l'unica cosa che ti permette di
dire sì a chi arriva senza prenotare.

Fra due assegnazioni valide vince sempre quella che **lascia liberi tavoli interi**, non
quella che spreca meno posti. Perdere qualche coperto teorico per tenere sgombro un otto-posti
è un buon affare: metà del fatturato di questi locali entra dalla porta senza prenotare.

## Il metodo è fisso, il locale no

Quello che questa skill conserva è il **ragionamento e l'obiettivo**. I numeri di un locale
non valgono per un altro, e non valgono nemmeno per lo stesso locale fra due settimane: i
tavoli si spostano, le combinazioni cambiano, una sala viene chiusa per la stagione.

Quindi **ogni volta, prima di calcolare qualsiasi cosa, rileggi da Resmio**:

| Cosa | Perché non puoi darlo per scontato |
|---|---|
| Tavoli, nomi e capienze | cambiano con la stagione e con i dehors |
| Gruppi / sale | una sala può essere stata aggiunta o dismessa |
| Combinazioni configurate | sono l'unico elenco di accostamenti che qualcuno ha validato |
| Override sulle risorse | tavoli o sale bloccati per un periodo, spesso senza motivo scritto |
| Orari di apertura e capienza per slot | il tetto per fascia è un limite di cucina, non di sala |
| Durate per numero di persone | il turno reale è una cosa che sa solo il cliente |

Nessuno di questi si deduce dalla planimetria e nessuno si eredita da un cliente precedente.
Leggili, e se qualcosa sembra strano — una sala vuota tutta la sera, una fascia sempre a zero —
non aggirarlo: è quasi sempre il problema, non un dettaglio.

Quando scopri qualcosa che vale oltre la serata — il codice del locale, quali accostamenti il
cliente ha confermato come impossibili, la soglia di coppie che ha scelto, il turno reale —
**salvalo in memoria**. È il tipo di informazione che costa una domanda al cliente ogni volta
che non ce l'hai.

## La sequenza

### 1. Fotografa la serata

Scarica prenotazioni, tavoli, gruppi, combinazioni e override della data richiesta. Poi
calcola, slot per slot da 15 minuti, **quanti tavoli sono liberi per l'intera durata di una
seduta** — non quanti sono vuoti in quell'istante. È una distinzione che cambia tutto: un
tavolo vuoto alle 20:30 ma prenotato alle 20:45 non è disponibile per nessuno.

Separa il conteggio per classe: due posti, quattro, sei, sette e più. Il quadro utile è
quello che mostra *quale taglia* è finita, non quanti posti restano.

### 2. Misura dove si rompe davvero

Il numero che dimostra il problema è **`available_authenticated`** dell'endpoint
`availability`: i posti che Resmio considera ancora vendibili. Quando cade a zero mentre la
sala è a metà, hai trovato il punto in cui il locale sta rifiutando soldi. Registralo prima
di toccare qualsiasi cosa: sarà la prova che il lavoro ha funzionato.

Se la richiesta è di analisi o strategia — non un incastro al volo — allarga lo sguardo alle
ultime 3-4 settimane e calcola il **picco di tavolate contemporanee per classe**, con mediana
e 90° percentile, confrontato con quanti tavoli di quella taglia il locale possiede. Quasi
sempre emerge un buco strutturale su una classe sola (di solito i quattro-posti), e quello è
il vero argomento da portare al cliente: nessun riassetto lo risolve, serve cambiare il parco
tavoli o riaprire una sala.

Guarda anche la quota di **walk-in** sullo storico. Se è alta, la riserva di tavoli sgombri
non è prudenza: è il canale principale.

### 3. Fissa i paletti con il cliente, prima di calcolare

Tre decisioni non sono tue. Chiedile in blocco, con i numeri dello storico a supporto, e non
partire finché non hai risposta:

- **Quali tavoli si possono accostare fisicamente.** Mai dedurlo dalla planimetria: vedi
  `trappole.md`.
- **Quanti tavoli da due restano sempre liberi** come rete per le coppie che arrivano senza
  prenotare. Porta il dato: quante coppie in contemporanea al picco, quante ne possiede.
- **Quanti tavoli grandi tenere sgombri** e fino a che ora.

Chiedi anche se le **durate** configurate corrispondono al turno reale, e se il ricambio è
immediato o serve un cuscinetto fra un turno e l'altro. Il cuscinetto costa caro — misuralo e
mostraglielo invece di deciderlo tu.

### 4. Ricompatta

Assegna partendo dalle tavolate **più vincolate** — le più numerose, poi per orario — perché
hanno meno alternative. Le piccole entrano dopo, nei buchi che restano.

Per ogni prenotazione, fra le unità libere che la contengono scegli quella con il **residuo
temporale minore**: la somma dei minuti sprecati prima e dopo dentro la finestra libera. A
parità, preferisci il tavolo meno versatile — i grandi e i combinabili si consumano per
ultimi, perché servono a chi arriverà.

Poi tre correzioni che rendono il piano applicabile:

- **Congela i gruppi da 8 in su** dove sono, se stanno su una combinazione valida. Spostarli
  produce catene lunghe e sposta anche tutti gli altri.
- **Passata di rientro**: per ogni prenotazione spostata, se il tavolo di partenza è ancora
  libero e non serve alla riserva, rimettila dov'era. Taglia gli spostamenti a vuoto —
  tipicamente da 45 a 20 — senza perdere nulla del risultato.
- **Rifiuta i guadagni che non pagano.** Se liberare un tavolo in più costa quindici
  spostamenti a catena, non farlo e spiega perché. In sala la confusione ha un costo che nel
  foglio non si vede.

### 5. Verifica prima di scrivere

Sul piano calcolato, controlla e riporta:

- nessuna sovrapposizione sullo stesso tavolo
- nessuna tavolata su una capienza inferiore al numero di persone
- nessuna prenotazione rimasta senza tavolo
- la riserva di coppie non scende mai sotto la soglia concordata
- quali tavoli restano intonsi per tutta la serata, e quanti posti sono

Poi presenta il piano **prima di applicarlo**, con il confronto prima/dopo sui tavoli liberi
al picco. Un documento visivo con la timeline tavolo per tavolo si verifica in un minuto;
una lista di venti spostamenti no.

### 6. Applica, e dimostra il risultato

Una sola prenotazione per prima, poi controlla che non sia partita nessuna mail all'ospite
(`trappole.md` spiega come). Solo dopo il resto, in sequenza.

Alla fine rileggi **tutta** la serata da Resmio — non fidarti dei codici di risposta — e
rimisura `available_authenticated` sulle fasce che prima erano a zero. Il salto da 0 a
tredici o quattordici posti vendibili in una fascia di punta è il risultato vero: quei posti
tornano in vendita su Google, TheFork e sito nello stesso istante.

## Quando la richiesta è "dove metto questo gruppo?"

Non cercare un tavolo libero: cerca **la strada più corta per liberarne uno**.

1. Elenca le combinazioni che reggono quel numero e **chi le occupa**, con orari e nomi. Spesso
   una è bloccata da una sola prenotazione, e quella si sposta.
2. Per ogni bloccante, verifica se ha un'alternativa. Se non ce l'ha, quella strada è chiusa —
   dillo, non girarci intorno.
3. Conta gli spostamenti di ogni strada e presenta le opzioni con il loro costo reale, incluse
   quelle che richiedono una decisione del cliente (creare un accostamento nuovo, spostare
   l'ospite di un quarto d'ora, aprire una sala chiusa).
4. Se nessuna strada è a costo zero, **chiedi**: il cliente conosce la sala e vede opzioni che
   nei dati non ci sono — una saletta bloccata nel sistema ma apribile, un accostamento che
   fate solo per i gruppi.

## Come si riferisce il lavoro

Numeri, non aggettivi. "Alle 20:30 il sistema vendeva 0 posti con la sala al 40%" vale più di
"c'erano margini di miglioramento".

Il confronto che conta è **tavoli interi liberi al picco, prima e dopo**, seguito dai posti
tornati vendibili. Poi la lista degli spostamenti, raggruppata per motivo — libera i grandi,
riempie un buco, riordino a catena — perché così si verifica in un minuto invece che in dieci.

E chiudi sempre con quello che il riassetto **non** risolve: se mancano cinque quattro-posti
tutte le sere, dillo. È l'unica parte del lavoro che cambia qualcosa domani.
