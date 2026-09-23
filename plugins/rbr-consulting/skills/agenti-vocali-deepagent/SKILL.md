---
name: agenti-vocali-deepagent
description: Crea, corregge e allinea gli agenti vocali di prenotazione dei ristoranti sulla piattaforma Deep Agent (platform.deepagent.app), separando le skill di base comuni a tutti dalle specifiche del singolo locale. Usa SEMPRE questa skill quando l'utente parla di modificare o sistemare il prompt di un agente vocale, attivare un nuovo cliente su Deep Agent, correggere il comportamento di un assistente telefonico di un ristorante, analizzare una chiamata andata male, sistemare orari o menù dentro un agente, capire perché una prenotazione non è entrata nel gestionale, o nomina Deep Agent, DeepAgent, D-Pagent, agente virtuale, agente vocale, front dell'agente, Alice, Lucia, Giulia, Carmen o Duilio. Vale anche quando descrive solo il sintomo — "l'agente dice ai clienti di richiamare", "non prende il numero di telefono", "non trasferisce all'operatore", "sbaglia gli orari" — perché su questa piattaforma quasi ogni difetto vive in più punti contemporaneamente e va cercato prima di essere corretto.
---

# Agenti vocali di prenotazione su Deep Agent

> Skill condivisa da Luciano Purpi il 2026-09-03 (scansione skill), aggiornata con i suoi contributi del 04-13/09/2026.
> Nota dell'autore: crea, corregge e allinea gli agenti vocali di prenotazione dei ristoranti, separando le skill di base comuni a tutti dalle specifiche del singolo locale. Collaudata su 7 agenti in produzione. Dentro: i blocchi di base (numero di telefono, errore tecnico, trasferimento, descrizione dei tool, orologio di sistema), la checklist di configurazione, il template di prompt master e la verifica dell'aggancio al gestionale. Regole generalizzabili: l'operatore è una risposta a una richiesta e mai un'offerta; il numero di trasferimento non può essere una linea deviata sull'agente stesso; gli orari del prompt vanno allineati al gestionale come fonte di verità; numero di telefono riletto a gruppi nel riepilogo parlato.

Metodo per lavorare sugli agenti vocali che rispondono al telefono dei ristoranti clienti.

**Il principio che regge tutto:** ogni modifica è o una **skill di base** (vale per tutti gli
agenti) o una **specifica del ristorante** (vale per uno solo). Prima di toccare qualsiasi cosa,
chiediti quale delle due è. Skill → si applica a tutti. Specifica → solo a quel cliente.
Senza questa distinzione gli agenti divergono e ogni cliente diventa un caso a sé.

**File di riferimento** (in `references/`):
- `checklist-deepagent.md` — baseline delle impostazioni e configurazione scheda per scheda, collaudo
- `prompt-master-template.md` — prompt master con segnaposto da compilare
- `scheda-locale-esempio.md` — scheda locale compilata (Red Mike) e guasti tipici delle copie
- `verifica-gestionale-prenotazioni.md` — allineamento orari/capacità col gestionale (Resmio)
- `api-pubblicazione-deepagent.md` — API interne: backup, salvataggio, pubblicazione su agente attivo

---

## 1. Prima di scrivere: leggere sempre

Non applicare mai un blocco a scatola chiusa. I prompt degli agenti sono strutturati in modo
diverso l'uno dall'altro e le stesse regole compaiono con formulazioni differenti.

**Sequenza obbligatoria per ogni agente:**

1. Apri la scheda **Azioni** e annota i nomi **reali** dei tool
2. Apri la scheda **Istruzioni** e leggi il prompt
3. Solo allora scrivi

**Perché il passo 1 non si salta:** i nomi dei tool nei prompt sono sbagliati molto più spesso
di quanto sembri. Casi realmente trovati:

- un prompt citava `get_disponibilita_noolas` mentre il tool registrato era `get_disponibilit_noolas` (senza la "a" finale)
- due agenti invocavano `transfer_operator`, che **non esiste** su questa piattaforma
- un agente aveva nel toolkit `get_disponibilita` e `set_prenotazione` generici marcati `[DA SETTARE INSIEME]` mentre i tool veri erano `_barresi` — con ogni probabilità la causa del suo tasso di successo bassissimo

**Convenzioni della piattaforma:**

| Cosa | Nome reale |
|---|---|
| Verifica disponibilità | `get_disponibilit_<slug>` — **senza la "a" finale**, è lo standard di fatto |
| Registra prenotazione | `set_prenotazione_<slug>` |
| Trasferimento a operatore | `transfer_to_human` (nella UI: "Trasferisci a Umano") |
| Altri predefiniti | `end_call`, `skip_turn` |

**Non rinominare i tool per fare ordine.** Sono agganciati ai webhook del gestionale.
Si allinea il prompt al nome registrato, mai il contrario.

---

## 2. Trappole della piattaforma

Queste fanno perdere tempo o, peggio, fanno credere che una modifica sia stata applicata quando non lo è.

- **Il salvataggio può essere vietato senza dirlo.** Se gli agenti dei clienti sono stati spostati in workspace separati (i "clienti gestiti" del Portale Partner), l'account dell'agenzia li **vede ma non li può modificare**: al salvataggio compare "Errore nel salvataggio — Missing agent.update permission for this agent", e su alcuni agenti il salvataggio fallisce **in silenzio**, senza nessun avviso, lasciando il banner "Modifiche non salvate". Il Portale Partner è in sola lettura e non permette di impersonare il cliente. Verificare SEMPRE la persistenza ricaricando la pagina e riconfrontando la lunghezza del prompt: il banner e l'assenza di errore non sono prove che sia stato salvato.
- **Il Salva va premuto in una chiamata separata, se no non salva niente.** Se scrivi nella textarea via JS e clicchi Salva nello stesso blocco di codice, React non ha ancora propagato lo state: lo spinner gira, nessun errore, e non viene salvato nulla (successo su 8 agenti in fila: tutti "ok", nessuno salvato). Metodo: (1) scrivi nella textarea; (2) in una chiamata separata, dopo qualche secondo, clicca `[...document.querySelectorAll('button')].find(x=>x.innerText.trim()==='Salva').click()` (il click per coordinate è inaffidabile); (3) aspetta 15-20 secondi; (4) **verifica rileggendo dal server** (`agentBuilder.getById`, vedi `references/api-pubblicazione-deepagent.md`), non dalla textarea né dal banner: "Modifiche non salvate" resta acceso anche a salvataggio riuscito. (contributo di Luciano Purpi, 09/09/2026)
- **Salvato non vuol dire in onda.** Su un agente già ATTIVO, salvataggio (UI o API) e `elevenlabs.updateAgent` aggiornano solo il database della piattaforma: al telefono continua a girare la configurazione dell'attivazione. L'unica cosa che pubblica è il flusso del tasto "Attiva agente" (`deploy-simple/stream` con `allowCreate:false`). Procedura, errori intermittenti e verifica in `references/api-pubblicazione-deepagent.md`. (contributo di Luciano Purpi, 12/09/2026)
- **I dialoghi di modifica tool si aprono solo con doppio clic** sul pulsante Modifica, a circa 2 secondi di distanza, poi bisogna attendere 12-14 secondi. Con un clic singolo non si aprono mai.
- **I tool sono condivisi tra agenti, non duplicati.** Al salvataggio può comparire la scelta "Tutti gli agenti" / "Solo questo agente": rispondere **sempre "Solo questo agente"**, altrimenti la modifica si propaga a clienti diversi. Anche le *copie* di un agente condividono i tool con l'originale.
- **Il campo "Obiettivo principale" torna indietro da solo** dopo alcuni salvataggi. Va ricontrollato a fine sessione. Nella configurazione scrive `personality.agentGoal` e `primaryGoal`; il `success_goal` di primo livello (`['Make a sale']` su tutti) è un default della piattaforma senza significato, non va "corretto".
- **L'endpoint del gestionale è lo stesso per più clienti** (un ingresso unico che smista a valle). Non è un errore di copia-incolla e non va "corretto".
- **Modalità Avanzata** deve essere attiva perché il prompt arrivi all'agente così com'è.

---

## 3. Le skill di base

Vanno su **ogni** agente. Sostituire `{{TOOL_TRANSFER}}` col nome reale letto nella scheda Azioni.

### Blocco A — Raccolta del numero di telefono

L'agente **non ha accesso al numero del chiamante**. Se il prompt gli fa proporre "uso questo
numero da cui stai chiamando?", il cliente risponde "sì" e l'agente resta senza cifre: a quel
punto riempie il campo con un segnaposto inventato e la prenotazione non entra.

```xml
<step>Chiedo SEMPRE il numero facendomelo dire a voce: "Mi lasci un numero di cellulare per la prenotazione?" — Non propongo MAI di "usare questo numero da cui stai chiamando": non ho accesso al numero del chiamante e non posso recuperarlo da nessuna parte.</step>
<step>REGOLA CRITICA — il campo phone deve contenere SOLO cifre realmente pronunciate dal cliente in questa conversazione. Non invento, non deduco, non uso segnaposto né valori di esempio come "testPhone", "phone", "numero", "N/A", "non fornito" o simili.</step>
<step>Se il cliente risponde in modo generico — "sì", "yes", "va bene", "usa questo", "quello da cui chiamo" — quella NON è un numero. Chiedo il numero in modo esplicito ma naturale, con una domanda sola: "Perfetto, e un numero di cellulare?". Non chiedo MAI di dettarmelo "cifra per cifra", "una alla volta" o "lentamente": è la richiesta che fa scandire il cliente, allunga le pause e mi fa perdere le prime cifre.</step>
<step>MENTRE IL CLIENTE DETTA IL NUMERO STO ZITTO — regola vincolante: da quando comincia a dirlo e finché non ha finito non parlo, non dico "sì", non lo incoraggio e non riempio le pause. Se sento una pausa a metà numero uso skip_turn e aspetto: sta pensando, non ha finito. Se lo interrompo lui ricomincia da capo e io perdo le cifre che aveva già detto. Se ricomincia da capo tengo per buona SOLO l'ultima sequenza completa, e prima di usarla le applico il controllo qui sotto.</step>
<step>CONTROLLO SUL NUMERO — rilettura, non conteggio: non conto le cifre davanti al cliente e non dico MAI che il numero è corto, incompleto o non valido. Quando ha finito di dettarlo glielo RILEGGO a gruppi (tre cifre, tre cifre, quattro cifre) e chiedo "È giusto?". Se conferma, quel numero vale così com'è, anche se a me sembra strano. Se dice che è sbagliato gli chiedo di ridirmelo una volta sola, poi lo rileggo di nuovo e chiedo conferma un'ultima volta. Numeri esteri, con +39 o fissi li accetto come dettati: le 10 cifre che cominciano per 3 sono solo un'indicazione, non una regola da imporre.</step>
<step>Il numero è un dato bloccante: senza cifre vere non registro la prenotazione. Se dopo due richieste il cliente non me lo dà, non invento nulla e non registro: passo la chiamata a un operatore con {{TOOL_TRANSFER}}.</step>
<step>Il numero di cellulare entra SEMPRE nel riepilogo finale prima della registrazione, riletto a gruppi (tre cifre, tre cifre, quattro cifre), così il cliente può correggermi. Se lo corregge, glielo rileggo di nuovo a gruppi e gli chiedo conferma prima di procedere.</step>
```

E nella sezione conversioni dati:

```xml
<rule>Telefono → formato numerico continuo, senza spazi né separatori, esattamente le cifre dettate dal cliente. Se il cliente indica il prefisso internazionale lo mantengo. È VIETATO riempire il campo phone con segnaposto, valori di esempio, testo descrittivo o stringhe non numeriche: se il contenuto non è fatto di cifre, il campo è sbagliato e la prenotazione non va registrata.</rule>
```

> ⚠️ **Perché rilettura e non conteggio** (contributo di Luciano Purpi, 04/09/2026). La prima
> versione del blocco faceva contare le cifre all'agente e ripetere il numero se "corto". Caso
> reale (Red Mike, 2/9/2026): il cliente detta un cellulare valido di 10 cifre, l'agente risponde
> "mi risulta corto", il cliente lo ripete due volte, l'agente non lo accetta e trasferisce
> all'operatore — tavolo disponibile, prenotazione persa. Contare cifre a orecchio è una delle
> cose che un modello vocale sbaglia di più (l'ASR rende "undici" come 11, i gruppi si fondono),
> e "ti manca una cifra" dà del bugiardo al cliente. Sostituito e verificato live su tutti e 7
> gli agenti il 4/9/2026. Per applicarlo in massa su prompt non identici: tagliare fra due
> marker (da `CONTROLLO OBBLIGATORIO SULLE CIFRE` a `rifaccio il controllo a ogni ripetizione.`
> incluso) verificando che la distanza sia sotto i 1500 caratteri — se è più lunga il prompt è
> diverso e va guardato a mano — e poi sostituire `rifaccio il controllo delle 10 cifre prima
> di procedere` con `glielo rileggo di nuovo a gruppi e gli chiedo conferma prima di procedere`.
> Verificare poi **sul comportamento**, non sulla stringa (vedi §4-bis): "10 cifre" può essere
> diventato "dieci cifre".

> ⚠️ **Cercare anche negli esempi tradotti.** Se il prompt ha un blocco `<language_handling>`
> con frasi di esempio in inglese, la vecchia domanda sul numero del chiamante vive spesso
> **anche lì** — ed è la versione che l'agente usa con i clienti stranieri. In un caso reale è
> sopravvissuta a una prima correzione proprio in quel punto ed era esattamente quella che
> aveva causato il guasto.

> ⚠️ **La domanda accorpata va tenuta, ma va detto cosa fare quando il cliente risponde a
> metà.** Chiedere "nome, cognome e cellulare" in un turno solo è giusto — separarle fa sembrare
> la chiamata un interrogatorio. Il problema è che il cliente spesso risponde solo con il nome, e
> se il prompt non prevede la ri-domanda per il pezzo mancante l'agente **se la inventa** — e
> quello che pesca è la frase sulle cifre pensata per un altro caso, che diventa "me lo detti
> cifra per cifra?". Da lì il cliente scandisce, l'agente gli va sopra, e le prime cifre si
> perdono. Nel prompt va scritto esplicitamente: se la risposta è parziale, chiedo **solo** il
> pezzo mancante, con una domanda breve — "Perfetto Mario, e un numero di cellulare?" — senza
> rifare la lista di quello che mi serve.

> ⚠️ **La stessa regola è scritta con parole diverse su ogni agente: cercare con regex, non con
> stringhe esatte.** Applicando il blocco su sette agenti, la frase da sostituire compariva in
> tre forme — `chiedo le cifre esplicitamente — "..."`, `Chiedo le cifre in modo esplicito e
> gentile: "..."` e `chiedo le cifre in modo esplicito e gentile ("...")` — e su due agenti non
> c'era affatto. Cercare `/cifre (esplicitamente|in modo esplicito)/` e, dove manca, inserire il
> blocco subito dopo la regola che vieta i segnaposto nel campo phone. Stessa cosa per la
> domanda accorpata: `/(\(2\) |2\. )?[Nn]ome, cognome e numero di cellulare li chiedo SEMPRE insieme/`.

> ⚠️ **Il riepilogo va cercato, non dato per scontato — e a volte non c'è.** Su un agente
> (Osteria Barresi) il toolkit dichiarava *"Registra la prenotazione dopo conferma esplicita del
> riepilogo"* ma nel workflow il riepilogo parlato **non esisteva**: si passava dalla verifica
> disponibilità direttamente a `set_prenotazione`. Su un altro (Mister Pizza) il numero veniva
> riletto solo *"se il cliente ha lasciato un numero diverso da quello della chiamata"* — una
> condizione che l'agente non può valutare, perché il numero del chiamante non ce l'ha: nei
> fatti il telefono non veniva mai riletto. Prima di aggiungere il telefono al riepilogo,
> verificare che il riepilogo ci sia e che non sia subordinato a una condizione impossibile.

> ⚠️ **Le difese vanno messe insieme.** Togliere il "cifra per cifra" riduce la probabilità,
> ma è la **rilettura a gruppi con conferma**, ripetuta nel **riepilogo finale**, che intercetta
> il guasto quando succede lo stesso: è il cliente a correggere, non l'agente a giudicare. Un
> numero sbagliato passato al gestionale non produce un errore leggibile: produce una
> prenotazione che non entra e un cliente che riattacca convinto di avere il tavolo.

### Blocco B — Errore tecnico: mai rimandare, sempre passare

Se l'agente dice "richiami in pizzeria", al numero della pizzeria risponde di nuovo lui.
È un giro a vuoto garantito e il cliente è perso.

```xml
<api_errors>Se la verifica della disponibilità o la registrazione della prenotazione non riesce al primo tentativo, riprovo una volta. Se fallisce di nuovo, NON invito MAI il cliente a richiamare, né a telefonare al locale, né a passare dal sito: a quel numero rispondo io, quindi rimandarlo lì significa fargli rifare la stessa chiamata e ritrovare lo stesso problema. La regola è una sola: passo la chiamata a un operatore con {{TOOL_TRANSFER}}, restando in linea con lui fino al trasferimento. Dico qualcosa come: "Guarda, ho un problema tecnico e non riesco a registrarla io, quindi al momento la prenotazione NON è ancora presa. Non ti faccio richiamare: ti passo subito un collega che te la inserisce lui." Poi pronuncio la frase di attesa ed eseguo il trasferimento.
REGOLA CRITICA sul riepilogo: il collega che riceve la chiamata NON ha ascoltato la conversazione e non gli arriva nessun riepilogo da me, quindi NON dico MAI al cliente "così non devi ripetere tutto" — sarebbe falso e lo lascerebbe scoperto. Prima di trasferire gli ripeto i dati ad alta voce (giorno della settimana, data, ora, coperti, nome e cognome) spiegando a cosa servono: "Ti ripeto i dati così li hai pronti da dare al collega, che te la inserisce lui."
Solo se il trasferimento a sua volta non riesce, allora — e solo allora — mi scuso e gli lascio il numero diretto. (Tutto tradotto nella sua lingua.)</api_errors>
```

**Il trasferimento non porta contesto.** L'operatore che riceve la chiamata non ha ascoltato
nulla e non riceve nessun riepilogo: è una telefonata che gli arriva e basta. Qualsiasi
formulazione tipo *"così non devi ripetere tutto"* è quindi falsa, e lascia il cliente convinto
che il collega sappia già — mentre dovrà ridire ogni cosa. Il riepilogo va fatto lo stesso, ma
va inquadrato per quello che è: dare al cliente i dati freschi da dettare.

### Regola sullo stato della prenotazione

Va dentro `transfer_handling`, o nei guardrail se il blocco non c'è. Serve a non lasciare mai
il cliente con l'idea sbagliata di avere un tavolo.

```
REGOLA — STATO DELLA PRENOTAZIONE: se trasferisco mentre stavo raccogliendo o registrando una prenotazione, per qualunque motivo, dico SEMPRE al cliente in modo esplicito a che punto siamo, e non lo lascio mai riattaccare con un dubbio.
- Se la prenotazione NON è stata registrata: lo dico chiaramente ("al momento la prenotazione non è ancora presa, la completi con il collega") e lo avviso che dovrà ridare i dati, perché il collega non ha ascoltato la chiamata.
- Se la prenotazione ERA già stata registrata con successo prima del trasferimento: lo dico altrettanto chiaramente ("la prenotazione è già confermata, ti passo il collega per l'altra cosa"), così non teme di perderla.
Non do mai per scontato che il cliente sappia in che stato siamo: è la cosa che gli interessa di più.
```

Copre due casi che sembrano diversi ma producono lo stesso danno: il problema tecnico a metà
prenotazione, e il cliente che stava prenotando e poi chiede altro che richiede l'operatore. In
entrambi rischia di riattaccare credendo di avere un tavolo che non esiste.

### Blocco C — Il trasferimento va dichiarato come strumento

Errore ricorrente: il trasferimento esiste sulla piattaforma con i numeri configurati, ma il
prompt **non lo elenca tra i tool**. L'agente quindi non sa di poterlo usare e ripiega sul
"richiami più tardi".

Nel toolkit:

```xml
<tool name="{{TOOL_TRANSFER}}">Passa la chiamata a un operatore. Va usato per: gruppi oltre il massimo gestibile, richiesta esplicita del cliente, modifiche a prenotazioni esistenti, preordini telefonici, e SEMPRE quando un problema tecnico impedisce di verificare la disponibilità o di registrare la prenotazione. REGOLA OBBLIGATORIA: prima di invocare questo strumento pronuncio SEMPRE la frase di attesa che avvisa il cliente del trasferimento e lo invita a non riattaccare anche se sente silenzio. Non trasferisco mai senza prima averla detta.</tool>
```

E come blocco a sé:

```xml
<transfer_handling>
REGOLA VINCOLANTE — vale per OGNI passaggio all'operatore: gruppi oltre il massimo, richieste fuori scope, modifiche a prenotazioni esistenti, problemi tecnici che impediscono la prenotazione, o richiesta esplicita del cliente.

PRIMA di invocare {{TOOL_TRANSFER}} dico SEMPRE al cliente, con tono caldo e parlato, una frase che: (1) annuncia il trasferimento, così capisce che non è caduta la linea; (2) lo avvisa che per qualche secondo potrebbe sentire silenzio; (3) gli chiede di non riattaccare e restare in linea.

Frase da usare (o variante naturale con lo stesso significato, tradotta nella lingua del cliente):
"Resta in linea un momento, ti passo subito un collega. Per qualche secondo potresti sentire silenzio: è normale, non riattaccare, la persona arriva a breve."

{{REGOLA_SEDE}}

Solo DOPO aver pronunciato la frase di attesa eseguo il trasferimento. Non trasferisco mai in silenzio.
Se il trasferimento non va a buon fine, non rimando il cliente al sito e non lo lascio in sospeso: resto con lui, gli dico che al momento non riesco a passargli nessuno, e provo a risolvere io quello che posso.
</transfer_handling>
```

**`{{REGOLA_SEDE}}` — solo per i locali con più sedi.** Si omette per sede singola.

```
REGOLA SULLA SEDE — vincolante: ogni sede ha un suo numero e un suo operatore, quindi trasferisco SEMPRE alla sede a cui si riferisce la richiesta del cliente, mai a una sede generica e mai a una diversa da quella di cui stavamo parlando.
- Se stavo prenotando o verificando la disponibilità, la sede è già quella scelta dal cliente all'inizio della chiamata: la uso e basta. NON la richiedo, la so già.
- Se il cliente chiede un operatore per un motivo diverso, trasferisco alla sede di cui stavamo parlando in quel momento.
- Chiedo quale sede SOLO se davvero non è mai stata nominata in tutta la chiamata.
Quando annuncio il trasferimento nomino la sede ad alta voce, così il cliente sente che sta andando nel posto giusto.
```

### Blocco D — Descrizione del tool (scheda Azioni, non prompt)

**Il blocco più sottovalutato.** Se i *Body Parameters* del tool sono vuoti e la descrizione è
generica o troncata, il modello **improvvisa la struttura del JSON a ogni chiamata**. Di solito
indovina; quando manca un dato, riempie il buco con un segnaposto.

Nel campo *"Cosa deve fare questo tool?"* (max 500 caratteri):

```
Crea una nuova prenotazione per {{LOCALE}}. Body: dataPrenotazione ("AAAA-MM-GG HH:MM"), nomePrenotazione (nome e cognome), phone, ResmioUtente, numeroPersone, email, noteCliente. CRITICO — phone: SOLO le cifre dettate a voce dal cliente in questa conversazione. VIETATO usare segnaposto o esempi come "testPhone", "phone", "N/A": non esiste un numero fornito dal sistema. Se il cliente non ha dettato cifre, non chiamare questo tool.
```

E per la verifica disponibilità:

```
Verifica la disponibilità di un tavolo da {{LOCALE}}. Passa la data in formato AAAA-MM-GG, l'orario in formato 24 ore HH:MM e il numero di coperti. Va chiamata SEMPRE prima di raccogliere i dati anagrafici del cliente: non ha senso chiedere nome e numero se poi lo slot non è disponibile. Non proporre mai al cliente un orario alternativo senza averlo prima verificato con questo tool.
```

> Verificare i nomi dei campi aprendo una chiamata riuscita nella cronologia. **Non definire i
> Body Parameters veri e propri** senza coinvolgere chi gestisce l'endpoint: passare da "nessuno
> schema" a "schema esplicito" può rompere un'integrazione che oggi funziona.

### Blocco F — L'orologio di sistema

L'agente **non sa che ore sono**. Se il prompt gli dice "guarda l'ora e scegli", la deduce da
come parla il cliente ("pomeriggio" diventa sera) e sbaglia: chiamata delle 16:34 trasferita al
numero della sera, con la regola oraria già scritta e corretta. Il segnaposto di sistema
`{{system__time_utc}}` scritto nel testo del prompt **sopravvive alla pubblicazione** e a ogni
chiamata viene sostituito con l'orario reale (verificato in onda l'11/9/2026). Il nome
"Blocco F" è quello usato nel parco agenti.

**Dove va conta quanto cosa dice.** Messo dentro il blocco dei trasferimenti (dove era nato),
il modello lo legge come una regola sui trasferimenti e continua a non sapere che ore sono nel
resto della chiamata. Va **da solo, in alto, subito dopo `<environment>`**, prima di qualsiasi
regola che dipende dall'ora, e si apre dicendo che è la prima cosa da guardare.

```xml
<orologio_di_sistema>RIFERIMENTO ORARIO DI SISTEMA — è la PRIMA cosa che guardo in ogni chiamata, prima ancora di capire cosa vuole il cliente. L'orario UTC di questa chiamata è {{system__time_utc}}. L'ora italiana è quella UTC più DUE ore quando è in vigore l'ora legale (dall'ultima domenica di marzo all'ultima domenica di ottobre) e più UNA ora nel resto dell'anno. Uso SOLO questo riferimento per sapere che ore sono e che giorno è: non lo deduco da quello che dice il cliente né da come mi saluta. Ogni volta che devo scegliere un comportamento che dipende dall'ora — quale numero uso se il trasferimento ha fasce diverse, il saluto di chiusura, se siamo aperti adesso, la disponibilità di oggi — guardo prima qui e mi dico l'ora in formato 24 ore. Se il riferimento risulta vuoto o illeggibile non tiro a indovinare: scelgo il comportamento più prudente e, se devo trasferire, uso il numero della fascia diurna.
VENIRE ADESSO — vale SOLO se l'ora italiana di ADESSO, letta qui sopra, è già dentro l'orario di servizio. Se siamo prima dell'apertura, "fra dieci minuti" non esiste: dico l'ora di apertura e propongo quella, senza mai spacciare un orario più tardi per "fra poco". Se invece siamo già dentro l'orario, non do per scontato che l'istante esatto sia prenotabile: verifico il primo quarto d'ora utile successivo e, se c'è posto, dico "Vieni pure adesso, ti segno alle [orario]: tanto il tempo che arrivi siamo lì". ATTENZIONE: il PRIMO orario che mi restituisce il gestionale NON vuol dire "fra poco" — è il primo orario prenotabile della giornata, che quasi sempre coincide con l'apertura. Prima di presentarlo come "adesso" lo confronto con l'ora vera: se dista più di mezz'ora da questo momento non è "adesso", quindi dico l'orario esatto e lascio scegliere al cliente. Non dico MAI "non c'è posto" solo perché l'ora esatta di questo momento non risulta prenotabile.
DISPONIBILITÀ VUOTA DENTRO L'ORARIO — se la verifica di disponibilità torna vuota mentre siamo ancora dentro l'orario in cui si prenota, non liquido il cliente con "non c'è posto": può essere un problema tecnico e il locale magari ha spazio. Gli dico che non riesco a prenotare io e passo la chiamata all'operatore, invece di mandarlo via.</orologio_di_sistema>
```

> ⚠️ **La conversione ora legale/solare va scritta dentro il blocco.** Con solo "UTC più due
> ore", a fine ottobre l'agente sbaglia fascia di un'ora e nessuno se ne accorge finché un
> cliente non finisce sul numero sbagliato.

> ⚠️ **Perché "VENIRE ADESSO" è scritto così.** La prima stesura diceva "verifico il primo
> quarto d'ora utile successivo": il modello l'ha letta come "il primo della lista", che è
> sempre l'apertura. Caso reale (Geb Garden, domenica 13/9 ore 13:06): cliente che vuole venire
> fra un quarto d'ora, agente che lo segna "alle diciotto e un quarto, tanto il tempo che
> arrivi siamo lì", cliente che riattacca. Lezione generale: quando una regola lavora su dati
> restituiti da un tool, va detto anche **cosa NON è** quel dato.

(contributi di Luciano Purpi, 12/09/2026, e correzione del 13/09/2026 — in onda su tutti e 8
gli agenti del parco il 13/9/2026)

---

## 4. Il resto del prompt master

Oltre ai blocchi di base, un agente ben fatto ha:

- **Postura umana** — "sono una persona, non un sistema", mai citare altri brand o assistenti
- **Una domanda alla volta**, con le sole due eccezioni dichiarate: orario+coperti insieme, nome+cognome+cellulare insieme
- **Multilingua completo** — rilevamento dalla prima frase, apertura ambigua, cambio lingua a metà chiamata, frasi di esempio dichiarate come traducibili, nomi propri invariati
- **Verifica disponibilità PRIMA dei dati anagrafici** — raccogliere nome e numero per poi scoprire che non c'è posto fa perdere il cliente
- **Nome e cognome entrambi obbligatori**, con richiesta esplicita del cognome
- **Mail non bloccante**: si chiede **una volta sola**, dopo il numero; se il cliente esita, scherza o cambia argomento non si insiste e si va avanti col campo vuoto (contributo di Luciano Purpi, 04/09/2026: insistere sulla mail spazientisce il cliente)
- **Riepilogo parlato e conferma esplicita** prima di registrare, con giorno della settimana + data per far emergere i malintesi
- **Mai proporre un orario non verificato** via API
- **Guardrail**: niente ordini al telefono, niente piatti o prezzi inventati, niente codici prenotazione, privacy rimandata al sito

---

## 4-bis. Come si scrive un divieto che regge

Vale per qualsiasi prompt (agenti vocali, bot GHL, …). Un divieto scritto male non tiene, e te
ne accorgi solo riascoltando le chiamate. Caso reale: agente che dopo aver indirizzato un
ordine d'asporto chiudeva con "Vuoi anche prenotare un tavolo per la cena?", con il divieto già
scritto nel prompt.

1. **Vieta la funzione, non la formulazione.** Il divieto citava una frase tra virgolette; il
   modello ha usato altre parole e si è sentito in regola. Scrivi la regola sull'effetto ("non
   mettere sul piatto un servizio che il cliente non ha chiesto"), dichiara gli esempi come
   esempi e aggiungi "vale anche per formulazioni che qui non compaiono".
2. **Zero eccezioni** su un comportamento da spegnere. Un "al massimo dillo una volta, come
   informazione" è la porta da cui rientra tutto.
3. **Ogni divieto vuole la sua alternativa positiva**, possibilmente con la formula esatta
   (qui: una domanda neutra, "Ti serve altro?"). Il solo "non fare" lascia un vuoto che il
   modello riempie da sé.
4. **Aggiungi un paragrafo "cosa NON è vietato"**, se no il divieto spegne anche comportamenti
   utili (proporre un orario alternativo, chiedere se è un'occasione speciale).
5. **Verifica sul comportamento, non sulla stringa.** Cercare il marcatore letterale nel prompt
   dà falsi negativi appena qualcuno riformula. Si riascoltano le chiamate.

Il difetto più pericoloso è quello che **nessuno ha scritto nel prompt**: la domanda sul tavolo
il modello se l'era inventata per servizievolezza, e nessuno degli altri agenti aveva la
difesa. Se un comportamento emergente fa danno su un agente, sono esposti tutti: la correzione
è una skill di base. (contributo di Luciano Purpi, 09/09/2026)

---

## 5. Il layer del ristorante

L'unica parte da compilare all'attivazione. Se una voce non si applica, **scriverla comunque**
in modo esplicito: una variabile vuota diventa un'invenzione in chiamata. Dove manca il dato,
scrivere una regola di comportamento che non afferma fatti — per esempio *"non ho una mail da
comunicare, se me la chiedono rimando al sito"* — invece di lasciare un segnaposto.

Nome agente e voce · brand e concept · sedi (una o più) · indirizzo, telefono, mail, sito,
social, URL privacy · **i tre orari del locale (vedi sotto)** ·
giorni di chiusura · massimo coperti gestibili in autonomia → soglia di trasferimento ·
anticipo minimo per il last minute · asporto e delivery: dove rimandare · menù (in Knowledge
Base, non nel prompt) · regime alimentare e protocollo allergeni · promozioni e condizioni ·
operatore: esiste, in che fasce, numeri diversi per ambiti diversi · servizi fuori scope ·
nomi tool e gestionale · primo messaggio · criteri di successo

> ⚠️ **I tre orari del locale non sono uno** (contributo di Luciano Purpi, 12/09/2026). Quasi
> ogni locale ne ha tre: (1) quando il **locale** è aperto (spesso fino a tarda notte);
> (2) l'**ultima ordinazione in cucina**; (3) l'**ultimo slot prenotabile** sul gestionale, che di
> solito chiude prima. Con solo il primo nel prompt l'agente si contraddice: caso reale (Geb
> Garden, 11/9 ore 23:20) — "sì, siamo aperti fino alle due e la cucina lavora", poi il
> gestionale non ha slot e "per stasera non ho orari". In attivazione chiedi al cliente tutti e
> tre e scrivili separati, con cosa dire in ciascuna fascia:
> - prima dell'apertura → "apriamo alle X" e propone di prenotare;
> - in servizio → flusso normale;
> - ultimi 45 minuti prima della chiusura prenotazioni → prenota ma avvisa che l'ultimo tavolo è alle X;
> - fra chiusura prenotazioni e chiusura cucina → NON prenota, ma manda il cliente lo stesso:
>   "a quest'ora non riesco più a prenotarti, però la cucina prende l'ultima ordinazione alle X:
>   se arrivi adesso fai in tempo, in sala ti sistemano" (non promette il tavolo; sono clienti
>   che prima si perdevano);
> - dopo la chiusura cucina → per mangiare è tardi, offre il locale aperto fino a X per bere
>   qualcosa e propone un'altra sera.
>
> La regola regge solo con il **Blocco F** (senza orologio l'agente non sa in che fascia siamo).
> Su Resmio: `opening_hours` = fascia prenotabile, `visual_opening_hours` = orario mostrato agli
> ospiti.

> ⚠️ **Asporto e domicilio: far scegliere al cliente, non indovinare.** Se il locale ha
> entrambi i canali, l'agente non deve dedurre quale vuole il cliente da una frase generica.
> In una chiamata reale il cliente ha detto *"devo ordinare una pizza da portare a casa"* e
> l'agente l'ha mandato sul **domicilio**: ma "da portare a casa" quasi sempre vuol dire che
> se la porta via lui, cioè asporto. Nel prompt va messa una domanda-filtro obbligatoria prima
> di dare qualsiasi indicazione — *"La vuoi a domicilio, o passi a ritirarla tu?"* — con
> l'elenco delle frasi ambigue ("da portare a casa", "a casa", "per stasera") e di quelle già
> chiare (che non vanno ri-chieste). Sbagliare canale manda il cliente su un percorso diverso
> e l'ordine si incasina, quindi la domanda in più costa molto meno dell'errore.
> **Attenzione a come è formulata la domanda:** se la consegna la fa un portale (Deliveroo,
> Glovo…) e non il locale, l'agente non deve dire *"te la portiamo noi"* — è falso e crea
> l'aspettativa sbagliata su chi arriva alla porta e su chi risponde se qualcosa va storto.
> Si chiede in modo neutro: *"a domicilio o passi a ritirarla tu?"*.

> ⚠️ **"Non ho capito" non si risolve ripetendo identico.** Nella stessa chiamata l'agente ha
> ripetuto due volte la stessa identica frase, parola per parola, e il cliente non ha capito
> lo stesso. Va scritto esplicitamente: alla richiesta di ripetere, spezzare l'indicazione in
> passaggi corti e darli uno alla volta, invece di rifare la frase intera.

**Menù e FAQ lunghe vanno in Knowledge Base**, non nel prompt: su un agente vocale la latenza
conta e i menù cambiano di stagione. Nel prompt solo ciò che governa il flusso (fasce
prenotabili, soglie, chiusure, allergeni, dove rimandare).

---

## 6. Il campo "Obiettivo principale" e il tasso di successo

Non deve **mai** contenere il prompt. È il campo che l'AI legge per classificare l'esito di ogni
chiamata: se ci finisce dentro il prompt, il tasso di successo diventa un numero senza
significato. Errore trovato su più agenti contemporaneamente.

**Il criterio deve elencare TUTTI gli esiti che sono un buon lavoro per quel locale, non solo
la prenotazione** (contributo di Luciano Purpi, 09/09/2026). Con il vecchio criterio
"prenotazione registrata oppure operatore" un agente risultava al 14-17%, il più basso del
parco, e sembrava rotto: riascoltando, erano quasi tutti ordini d'asporto gestiti bene, marcati
"obiettivo non raggiunto". Quel numero misurava la quota di chiamate che erano prenotazioni,
non la qualità dell'agente. Indizio: durate quasi tutte sotto il minuto, incompatibili con una
prenotazione vera (ne servono almeno due).

Testo standard (adattalo ai canali del locale):

```
La chiamata è riuscita se: (1) la prenotazione è stata registrata con {{TOOL_PRENOTAZIONE}}; (2) la chiamata è stata passata a un operatore; (3) il cliente voleva ordinare ed è stato indirizzato al canale giusto; (4) il cliente chiedeva un'informazione (orari, indirizzo, menù, allergeni) e l'ha ricevuta corretta. È fallita se: la richiesta non è stata capita, sono state date informazioni sbagliate, il cliente voleva un tavolo e non è stato né registrato né trasferito, la chiamata si è chiusa senza risolvere.
```

Il campo della UI scrive `configuration.personality.agentGoal` e `primaryGoal` (vedi §2).
Cambiarlo vale **solo da quel momento in poi**: le chiamate già passate restano classificate
com'erano. Tratta la data del cambio come **azzeramento della baseline** e dillo al cliente, se
no il confronto mese su mese è falso. (Baseline al 4/9/2026, criterio vecchio: Red Mike 17%,
Noolas 31%, Duilio 59%.)

---

## 7. Diagnosticare un agente che si comporta male

Partire sempre dalla registrazione della chiamata, non dalle ipotesi. Nella cronologia, aprire
il dettaglio e guardare **i parametri effettivamente passati ai tool**: è lì che si vede se un
campo è arrivato vuoto o con un valore inventato.

Ordine di indagine:

1. **Controlla il `phone` nei parametri passati al tool.** Prima di ogni altra ipotesi (il conteggio lo fai tu sul payload, mai l'agente davanti al cliente). Un `phone` da 9 cifre invece di 10 fa rifiutare la prenotazione senza che da nessuna parte compaia un messaggio comprensibile, e l'agente lo racconta al cliente come "problema tecnico". Il controllo si fa in due mosse: aprire il chip del tool nella trascrizione e leggere il payload, poi aprire una chiamata **riuscita** dello stesso agente e confrontare campo per campo. Se l'unica differenza è il telefono, hai finito.
2. **I tool registrati corrispondono a quelli citati nel prompt?** È la causa più frequente e la più invisibile.
3. **La descrizione del tool dice il nome del locale giusto?** Su quattro agenti su cinque diceva il nome di un altro cliente, residuo di duplicazioni.
4. **La regola incriminata esiste in più punti del prompt?** Controllare sempre anche gli esempi tradotti.
5. **Il campo Obiettivo contiene i criteri o il prompt?**
6. **Il gestionale è allineato?** L'agente può annunciare gli orari giusti e poi interrogare un gestionale rimasto sui vecchi turni: la prenotazione si perde senza che nessuno capisca perché.

---

## 8. Prima di andare live

- [ ] Blocchi A, B, C nel prompt, con i nomi tool reali
- [ ] Blocco F (orologio) da solo subito dopo `<environment>`, con la regola ora legale/solare
- [ ] I tre orari (locale, cucina, prenotazioni) scritti separati
- [ ] Blocco D nelle descrizioni di entrambi i tool
- [ ] `{{REGOLA_SEDE}}` solo se multisede
- [ ] Trasferimento configurato, un numero per sede, soglie coerenti col prompt
- [ ] Campo Obiettivo con tutti gli esiti buoni e i fallimenti (§6)
- [ ] Pubblicato con "Attiva agente" e prompt in onda riletto (`references/api-pubblicazione-deepagent.md`)
- [ ] Nessun `[DA COMPILARE]` / `[DA SETTARE]` rimasto
- [ ] Orari allineati tra prompt e gestionale
- [ ] Modalità Avanzata attiva
- [ ] **Prova telefonica reale**

**Cosa provare al telefono**, in ordine di importanza:

1. **Prenotazione completa** — poi verificare che arrivi sul gestionale e che il campo `phone` contenga le cifre giuste
2. **Numero dato in modo vago** — rispondere "sì, va bene questo": l'agente deve insistere e chiedere le cifre
3. **Numero dettato con una pausa in mezzo** — dire le prime tre cifre, fermarsi due secondi, poi continuare: l'agente deve stare zitto e aspettare, non riempire la pausa
4. **Numero sbagliato** — alla rilettura a gruppi rispondere "no, è sbagliato": l'agente deve chiederlo una volta sola, rileggerlo e chiedere conferma. E dettare un numero valido: non deve MAI dire che è corto o non valido
5. **Telefono nel riepilogo** — verificare che lo rilegga prima di chiedere la conferma finale
6. **Trasferimento** — chiedere un tavolo sopra la soglia: deve annunciare, avvisare del silenzio, e solo poi passare
7. **Lingua straniera dalla prima frase** — deve rispondere in quella lingua da subito e chiedere comunque le cifre
8. **Domanda su allergeni** — deve dire la verità senza minimizzare e senza esitare
9. **"Posso venire adesso?"** prima dell'apertura e a fine servizio — deve dire l'ora di apertura o la fascia cucina, mai spacciare l'apertura per "fra poco"

---

## 9. Modifiche a rischio

Alcune cose non vanno fatte in automatico, per ragioni diverse dalla difficoltà tecnica.

- **Non pubblicare modifiche nei giorni o negli orari di punta del locale.** Un front nuovo si mette in onda quando, se qualcosa va storto, ci sono pochi coperti in gioco.
- **Archiviare il prompt precedente** prima di sostituirlo: il rollback deve essere un copia-incolla. Prima di una modifica di massa, backup di tutti i prompt in un JSON (procedura in `references/api-pubblicazione-deepagent.md`).
- **Non promettere l'assoluto sugli allergeni.** Se un cliente celiaco chiede della contaminazione, l'agente deve rispondere con sicurezza e spiegare **come** si lavora — ambiente separato, utensili dedicati, cottura in teglia dedicata — ma non dichiarare "zero rischio" quando la lavorazione non è completamente separata (forno condiviso, per esempio). Una prova concreta come "lo facciamo da oltre dieci anni e non abbiamo mai avuto un problema" convince più di una garanzia assoluta, ed è vera e verificabile. Una garanzia sanitaria falsa su una chiamata registrata è un rischio per la persona e per il locale.
- **Se un account del gestionale contiene più clienti**, verificare il nome della sede in cima alla pagina prima di ogni singola modifica. Nel dubbio, non toccare.
