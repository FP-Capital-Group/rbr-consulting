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
passa lo stesso — **a meno che** in Organizzazione dei tavoli › Elementi di base sia **spenta**
l'opzione "Abilita le prenotazioni manuali dei tavoli bloccati e occupati" (quando è accesa
compaiono "Mostra tutti i tavoli" e la fascia gialla). **Senza** quell'opzione, un override su
una sala intera blocca **anche il pannello**: la sala non può liberare né spostare tavoli in
servizio. Il rovescio: con l'opzione accesa, dalla fascia gialla si possono sovrapprenotare
tavoli già occupati — Resmio avvisa ma non blocca. Anche le Eccezioni (Vacanze ed eccezioni)
possono vincolare il manager allo stesso modo. Quindi: override solo per tavoli che
fisicamente non ci sono, e verifica sempre quell'impostazione prima di dire "l'override non
tocca il pannello". *(contributo di Andrea Chirivì, 2026-10-12 — corregge e condiziona
l'indicazione precedente)*

Su Dirigì la Saletta era bloccata per la stagione, e per questo era invisibile a Resmio quando
è arrivato un gruppo da 10 che non entrava da nessuna parte. La soluzione l'ha data il
cliente: mettilo in Saletta, che di combinazioni da 10 ne aveva già una configurata. Zero
spostamenti, sala principale intatta.

Quindi: quando una sala è bloccata, **chiedi perché**. Se è chiusa per personale è un conto,
se è tenuta come valvola fuori sistema è un'altra — e in quel caso è la prima cosa da guardare
quando qualcosa non entra. Ricordati poi di dire alla sala di apparecchiarla: nel sistema
risulta ancora bloccata e nessuno se ne accorge.

### Controllo completo degli override, a ogni fine settimana

- A ogni giro: `GET resource_overrides?limit=200`, poi tieni solo quelli con
  `begins ≤ adesso ≤ ends`, unendo tutti i `resources` coinvolti (usa una lista fissa: errori
  di questo tipo sono già capitati più volte in un mese).
- Resmio vende online anche un tavolo "fuori uso" se **non** ha un override attivo (caso
  reale: 6 persone vendute su un tavolo da 4 dismesso). Ogni tavolo dismesso deve avere il suo
  override, e va controllato anche l'**anno** di scadenza: se ne trovano con `ends` nel futuro
  lontano (es. 2048/2049), inerti e dimenticati.
- Gli override con scadenza vanno in agenda **prima** della fine, con la decisione del cliente
  sulla proroga (`PATCH ends`). Un'eccezione stagionale scaduta da sola ha mandato gente in
  sale chiuse. Un override lungo mesi si confonde facilmente con un blocco di giornata: guarda
  `ends` e verifica sul widget di quella data.
- Per i blocchi **ricorrenti** (es. palco ogni venerdì) serve un override **per data**: l'API
  non ha ricorrenza vera (il campo `series` esiste ma non va usato). Si rinnovano con un
  promemoria, tenendo conto del cambio d'ora.
- Quando si chiude una sala, le prenotazioni future già assegnate ai suoi tavoli **restano
  lì**: vanno elencate e spostate (o fatte spostare dalla sala) prima della data di chiusura.
- I tavoli bloccati si escludono **a mano** da ogni assegnazione: Resmio non lo impedisce da
  solo.
*(contributo di Andrea Chirivì, 2026-10-12)*

### Come assegna Resmio da solo (widget, Google, agente vocale)

Questa skill copre soprattutto l'assegnazione fatta da noi; Resmio assegna anche in automatico
sulle prenotazioni online. Regole osservate:
- La `priority` dei tavoli (più alta = scelta prima) e quella delle sale
  (`resource_groups.priority`) contano **solo a parità di capienza**. Fra capienze diverse
  vince sempre il singolo tavolo che calza meglio, in qualunque sala — dividere una sala in più
  sale non cambia questo comportamento. Le combinazioni non hanno priorità propria e perdono
  sempre contro un singolo tavolo che calza. Per guidare il riempimento si agisce sulle
  capienze dichiarate o si blocca la sala per la serata, non sulla priorità da sola.
- Un abbinamento è vendibile online solo se **tutti** i suoi tavoli sono liberi e non
  bloccati: un override su un solo tavolo toglie anche ogni combinazione che lo contiene. Per
  vendere un tavolo solo a sala piena senza perdere la coppia che lo contiene, non si blocca:
  lo si mette **ultimo in priorità**.
- L'assegnazione automatica **ignora** le richieste scritte nel `comment`.
- Il test valido è solo una prenotazione vera dal widget pubblico
  (`app.resmio.com/<slug>/widget?people=N&date=AAAA-MM-GG`), poi si legge `facility_resources`.
  La finestra "Nuova prenotazione" dello staff **non segue** la stessa logica di priorità. Nei
  test usa email e telefono inesistenti nel CRM: con quelli di un cliente vero si sovrascrive
  il suo contatto. L'automatismo si accende in Organizzazione dei tavoli › Elementi di base.
- **Da verificare**: la scelta della sala nel widget (`widget_room_choice_enabled`,
  `widget_any_room_choice_disabled`), spenta di default — cambia il widget visibile sul sito,
  va attivata solo con l'ok esplicito del titolare.
*(contributo di Andrea Chirivì, 2026-10-12)*

## Prova uno spostamento prima di farne venti

`PATCH` sui tavoli di una prenotazione **non** manda mail all'ospite su Resmio — verificato —
ma è una scrittura su prenotazioni vere di gente che stasera si presenta, e una mail partita
non si richiama. Nota: questo vale per lo spostamento tavoli, non per ogni `PATCH` — **annullare**
una prenotazione (`status: cancelled`) può mandare la mail di annullo se c'è l'`email`, vedi
`api-resmio.md`.

Fai il primo spostamento da solo, rileggi la prenotazione e controlla che `last_reply_sent`
sia rimasto invariato e lo `status` non sia cambiato. Poi procedi col resto. Costa trenta
secondi e ti mette al riparo da un comportamento che potrebbe cambiare con una versione di
Resmio.

Alla fine rileggi **tutta** la serata: codici `202` non garantiscono che il piano sia coerente.
Controlla sovrapposizioni, capienze e prenotazioni rimaste senza tavolo.

**Se il locale ha un ponte Resmio→GHL (o un altro CRM)**, ogni modifica — via API o dal
pannello — può arrivare lì come "nuovo appuntamento creato" invece che come aggiornamento: una
sola cena può generare sette appuntamenti. Un workflow agganciato all'appuntamento con rientro
aperto manderebbe un messaggio al cliente già a tavola. Quindi, prima di spostamenti in
blocco: verifica cosa fa il ponte del locale (non basta controllare `last_reply_sent` su
Resmio), non spostare a servizio aperto, correggi solo ciò che è davvero sbagliato (ogni
`PATCH` inutile è un evento inutile sul ponte). Nei giri a ciclo (A→B, B→C, C→A) procedi in
sequenza, una `PATCH` per prenotazione, senza tavoli d'appoggio: la `PATCH` accetta un tavolo
ancora occupato (`202` anche con due prenotazioni sullo stesso tavolo), quindi verifica prima
che i tavoli d'arrivo siano liberi, escluse le prenotazioni in movimento. Con un ponte
proprio (gestito da RBR), le `PATCH` a stato invariato non duplicano.
*(contributo di Andrea Chirivì, 2026-10-12 — completa questa sezione: "verificato" valeva solo
per Resmio, non per i ponti verso il CRM)*

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

Gli orari prenotabili si **scrivono** sull'endpoint `/openinghours` (`opening_hours` è solo il
campo in lettura del facility). Sono blocchi con giorni, orari e una `capacity` per fascia, la
cui unità è il `booking_interval` del facility — **non sempre 15 minuti** (spesso 30 =
coperti per mezz'ora). Per aprire prima un solo giorno si crea un blocco nuovo per quel
giorno, togliendolo dall'altro, con backup degli orari prima di modificare. Il codice d'errore
`BOOKING_CREATE_ERROR_RUSH_HOUR_BLOCKED` segnala il limite di fascia raggiunto. Nell'interfaccia,
Prenotazioni › Orari › Limiti dell'ora di punta accetta righe separate per giorno (es.
dom-gio 35, ven 40, sab 36). Le prenotazioni partono dall'apertura della cucina. I campi orario
in UI sono tendine MUI (si clicca, poi si sceglie nel popover `.MuiPopover-root`): solo la
capacità è un input diretto. Per il calcolo del tetto vedi `capacita-e-fasce.md`.
*(contributo di Andrea Chirivì, 2026-10-12 — corregge l'indicazione precedente su opening_hours)*

Non è la capienza della sala: è quante persone il locale accetta di far arrivare in quella
finestra, e serve a proteggere la cucina (vedi sopra quale reparto, in `capacita-e-fasce.md`).

Se gli arrivi di una fascia ci si avvicinano, il problema non è più l'assegnazione dei tavoli.
Portalo al cliente come domanda — la cucina regge di più? — e nel frattempo lavora sulla
distribuzione, spingendo le fasce semivuote invece di forzare quella satura.

**Import da altri canali (TheFork compresa)**: widget, agente vocale e operatore vedono la
disponibilità in tempo reale, ma gli import via API e gli ingrandimenti a mano la scavalcano.
Prima di ogni import conta i coperti attivi della fascia: se sfora si importa comunque (il
posto è già venduto altrove) ma si segnala. TheFork non conosce il tetto di Resmio: la fascia
su TheFork va chiusa a mano prima della saturazione e comunque sotto i 2 posti residui (TheFork
non vende a 1 posto). Anche un import tardivo si fa con un tavolo assegnato e rispettando le
durate fra i turni.
*(contributo di Andrea Chirivì, 2026-10-12)*

**Dove mettere il link/widget quando il locale ha ENTRAMBI Resmio e TheFork**: Resmio su TUTTI i
canali propri (sito: header, home dopo la copertina, barra fissa mobile; Google; social; bio)
TRANNE TheFork. Su TheFork le prenotazioni online restano ATTIVE, così chi entra dal portale/app
TheFork prenota con lo sconto; il ristoratore riporta a mano ogni prenotazione TheFork su Resmio
per evitare doppie occupazioni. **Trappola**: in TheFork Manager (Settings → Service setup →
servizio → step 3 Online availability) l'interruttore "This service can accept online
reservations" NON spegne solo il widget sul sito — chiude le prenotazioni online ovunque (portale,
app, widget, Tripadvisor) e quindi anche gli sconti: non toccarlo. Per togliere TheFork dal sito
basta sostituire i link `widget.thefork.com` con il link Resmio (su Divi: `button_url` nei moduli
`et_pb_button` + voce di menu). Le modifiche di disponibilità su TheFork si propagano sul widget in
qualche secondo/minuto (le date si chiudono/riaprono a scaglioni): ricontrollare dopo un reload.
*(contributo di dietstreetfood@gmail.com, 2026-11-05, caso Gino's Forno e Brace, Aragona)*

## Dettagli operativi che il piano non vede

Le note delle prenotazioni contengono passeggini, seggioloni, celiaci. Un piano perfetto sui
numeri può concentrare tre passeggini in un corridoio alle 20:30 perché i tavoli assegnati
sono affiancati.

Leggi le note, e se vedi concentrazioni segnalale insieme al piano. Non è un errore
dell'algoritmo, è un'informazione che serve a chi accoglie.

**Come leggere `num` e le note, in dettaglio:**
- `num` non è affidabile con i bambini ("4 adulti + due seggioloni" può risultare `num: 4`):
  si riconta dalla nota — seggiolone o rialzo = posto pieno — e `num` si corregge solo verso
  l'alto.
- Nel `comment` separa il rumore (marcatori automatici di sito/integrazioni, note TheFork) dalle
  richieste vere. Le allergie vanno segnalate al passe e non pesano sull'assegnazione dei
  tavoli; i passeggini si segnalano alla sala.
- Le richieste di posizione ("vicino alla musica") le ignora l'assegnazione automatica. Le sere
  di evento ordina i tavoli per distanza dal palco (`table_location_horizontal`/`_vertical`) e
  sposta solo chi non ha chiesto nulla.
- Le note arrivate da un altro canale (es. TheFork: allergie, vegetariano) non arrivano su
  Resmio se la sala inserisce a mano: a ogni import vanno copiate nel `comment`.
- **Doppioni apparenti**: una tavolata grande divisa su due tavoli con lo stesso nome (es. 28
  persone = 14+14) **non** è un doppione. Prima di annullare, leggi coperti, tavoli e note di
  entrambe le prenotazioni. Un doppione vero si annulla senza messaggio al cliente — vedi il
  metodo in `api-resmio.md`.
*(contributo di Andrea Chirivì, 2026-10-12)*
