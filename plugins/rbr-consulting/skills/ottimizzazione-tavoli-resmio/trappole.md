# Trappole

Lezioni pagate su clienti veri. Le prime due evitano danni in sala, le altre fanno risparmiare
un giro di lavoro buttato.

## Mai dedurre un accostamento dalla planimetria

Le coordinate dei tavoli in Resmio dicono quanto sono vicini, **non se si possono unire**. In
mezzo ci passa un corridoio di servizio, una colonna, un dislivello, o semplicemente due
tavoli di altezza diversa.

Su Dirigì avevo proposto `9+10`: distanza identica ad altre coppie che il locale unisce
abitualmente, e in sala non si accostano. Il piano andava rifatto da capo.

**L'unico elenco affidabile di accostamenti è `resource_combinations`**, perché quelli
qualcuno li ha provati. Se il piano ne richiede uno nuovo, elencalo al cliente e fattelo
confermare **prima** di calcolare, non dopo. E quando un accostamento viene bocciato, chiediti
se altri dello stesso tipo lo sono — se cade `9+10`, probabilmente cadono anche `14+15` e
`23+24`, ed è meglio ricalcolare senza tutta la famiglia che scoprirlo un pezzo alla volta.

## Un blocco non è una sala che non esiste

Gli `resource_overrides` tolgono i tavoli dalla **vendita online**. L'assegnazione manuale
passa lo stesso.

Su Dirigì la Saletta era bloccata per la stagione, e per questo era invisibile a Resmio quando
è arrivato un gruppo da 10 che non entrava da nessuna parte. La soluzione l'ha data il
cliente: mettilo in Saletta, che di combinazioni da 10 ne aveva già una configurata. Zero
spostamenti, sala principale intatta.

Quindi: quando una sala è bloccata, **chiedi perché**. Se è chiusa per personale è un conto,
se è tenuta come valvola fuori sistema è un'altra — e in quel caso è la prima cosa da guardare
quando qualcosa non entra. Ricordati poi di dire alla sala di apparecchiarla: nel sistema
risulta ancora bloccata e nessuno se ne accorge.

## Prova uno spostamento prima di farne venti

`PATCH` sui tavoli di una prenotazione **non** manda mail all'ospite — verificato — ma è una
scrittura su prenotazioni vere di gente che stasera si presenta, e una mail partita non si
richiama.

Fai il primo spostamento da solo, rileggi la prenotazione e controlla che `last_reply_sent`
sia rimasto invariato e lo `status` non sia cambiato. Poi procedi col resto. Costa trenta
secondi e ti mette al riparo da un comportamento che potrebbe cambiare con una versione di
Resmio.

Alla fine rileggi **tutta** la serata: codici `202` non garantiscono che il piano sia coerente.
Controlla sovrapposizioni, capienze e prenotazioni rimaste senza tavolo.

## L'ottimo teorico non è applicabile

Il primo piano che avevo prodotto era matematicamente migliore e chiedeva **46 spostamenti su
51 prenotazioni**. Inapplicabile: in sala nessuno riesce a tenere in testa un rimescolamento
totale, e metà di quei movimenti erano scambi fra tavoli equivalenti che non cambiavano nulla.

Un piano da 20 spostamenti che ottiene il 90% del risultato vale più di uno da 46 che ottiene
il 100%. Costruisci sempre la **passata di rientro** (rimetti dov'era chi può tornarci) e
misura il costo in spostamenti di ogni guadagno prima di proporlo.

## Le briciole ingannano

Guardare i **posti** liberi porta fuori strada: 28 posti liberi al picco sembrano tanti finché
non scopri che sono quattordici tavoli da due e che nessuna famiglia di quattro può sedersi.

Conta sempre per classe di tavolo, e conta la disponibilità **per l'intera durata di una
seduta**, non nell'istante. Sono le due misure che descrivono il locale come lo vive chi sta
alla porta.

## Attenzione a chi consuma i due-posti

I tavoli da due sembrano sempre in eccesso guardando una sera sola. Sullo storico di tre
settimane, su un locale di mare in agosto, le sole coppie walk-in ne occupavano fino a 13 in
contemporanea su 19 disponibili.

Prima di unirli per fabbricare quattro-posti, misura il picco di coppie in contemporanea sullo
storico e concorda una **soglia minima di due-posti sempre liberi**. Poi rispettala come
vincolo duro nell'algoritmo, verificandola su ogni slot della durata della prenotazione che
stai piazzando — non solo all'istante di inizio.

## Il tetto per fascia è un limite di cucina

`opening_hours` ha una `capacity` per ogni fascia da 15 minuti. Non è la capienza della sala:
è quante persone il locale accetta di far arrivare in quella finestra, e serve a proteggere il
forno.

Se gli arrivi di una fascia ci si avvicinano, il problema non è più l'assegnazione dei tavoli.
Portalo al cliente come domanda — la cucina regge di più? — e nel frattempo lavora sulla
distribuzione, spingendo le fasce semivuote invece di forzare quella satura.

## Dettagli operativi che il piano non vede

Le note delle prenotazioni contengono passeggini, seggioloni, celiaci. Un piano perfetto sui
numeri può concentrare tre passeggini in un corridoio alle 20:30 perché i tavoli assegnati
sono affiancati.

Leggi le note, e se vedi concentrazioni segnalale insieme al piano. Non è un errore
dell'algoritmo, è un'informazione che serve a chi accoglie.
