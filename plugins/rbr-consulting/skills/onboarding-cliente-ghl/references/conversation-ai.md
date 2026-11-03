# Conversation AI (bot di risposta) su GHL

Setup base dell'agente: UI GHL, AI Agents → Conversation AI. Qui le regole imparate sul campo.

## 0. Prima di accendere

(contributo di Andrea Chirivì, 2026-10-12)

1. **Leggi le chat vere prima di scrivere il prompt.** Da lì escono gli scenari di passaggio e le regole: su un caso reale circa il 70% del traffico WhatsApp erano "confermo" ai promemoria, le proposte di band/fornitori erano tutte ignorate, c'erano richieste rimaste senza risposta.
2. **Checklist prima dell'accensione.**
   - Costi verificati in `Settings → Billing → Wallet & Transactions`. Conversation AI è a consumo, ⚠️ stima indicativa ~0,02 $/messaggio (15-40 $/mese su un locale medio, ~1.200 risposte/mese) + add-on WhatsApp ~15 $/mese — stima precedente al cambio tariffe Meta del 30/09/2026 sulle risposte libere WhatsApp (prima gratuite, poi a pagamento verso Meta, vedi `whatsapp-ghl-locale/references/costi-limiti-misura.md`): da ricontrollare caso per caso.
   - A fine eventuale promo, controlla che Agent Studio, AI Studio e Ask AI siano a 0 se non usati.
   - Catena di avviso allo staff collaudata.
   - Vecchie autorisposte spente: app WhatsApp Business e Meta Business Suite (vedi "Automazioni native Meta" nelle Trappole, sotto).
   - Conferme con pulsanti invece della doppia richiesta.
   - Test end-to-end fatto (vedi sezione Collaudo).
   - Accensione graduale: prima Instagram e Facebook, poi WhatsApp.
3. **All'accensione si gestiscono solo richieste di oggi o future**: gli arretrati su prenotazioni passate non si riprendono.
4. **Limiti da mettere in conto col cliente**: su Instagram il bot non legge immagini né menzioni-allegato. Se il cliente scrive da un numero diverso da quello in scheda, l'invio va in "failed" finché lo staff non corregge il numero. Vocali e immagini funzionano solo in Auto-Pilot. Nei giorni di punta possono arrivare 90-140+ messaggi WhatsApp.

## 1. Auto-Pilot NON basta: serve il Deploy

(contributo di Andrea, 10/09/2026)

Nel nuovo AI Agents (Conversation AI 2.0), Mode = Auto-Pilot + canali in "Contact Assignment
Channels" NON fa rispondere il bot: quella selezione vale solo per i bot assegnati via workflow.
Per l'auto-risposta serve la tab **Deploy** (in italiano "Implementa") dell'agente: **Configure** su
ogni canale (WhatsApp → numeri, IG/FB → pagine) e **Update**. Senza deploy il bot è un motore acceso
in folle.

- Nel Deploy per canale c'è "Doesn't have tags" = esclusione contatti per tag (whitelist staff).
  I tag creati solo via API non compaiono nel widget finché non esistono nel registro tag della
  location: creali prima da Impostazioni → Tag.
- "Sviluppa" e "Implementa" NON sono bozza/pubblicato: "Implementa" è solo l'elenco dei canali.
  **Il prompt salvato è GIÀ LIVE** sui canali deployati (contributo di Luciano Purpi, 19/09/2026).
  Non esiste una bozza: testa le modifiche al prompt prima di salvarle.

## 2. Prompt: regole per canale e tono

### Solo il link vale per canale: su WhatsApp il bot prenota in chat se può

(contributo di Andrea Chirivì + Luciano Purpi, 2026-10-12 — decisione di Andrea, in produzione dal 24/09)

Su **WhatsApp**, se il bot ha l'azione di prenotazione, **prenota in chat**. Dati obbligatori: giorno,
ora, persone, nome e cognome, email (il telefono è il numero WhatsApp). Il link Resmio diventa il
ripiego solo dopo due tentativi falliti. Su **Instagram e Facebook**, e ovunque il bot non prenota,
resta la regola base: **solo il link, mai l'alternativa "se ha difficoltà ci scriva"**. La raccolta
dati a mano parte solo se è il cliente a dire che non riesce — vale anche per le risposte dello
staff. Ogni salto fuori dalla chat perde gente: caso reale, campagna gift card, 1.299 WhatsApp
consegnati → 108 sì → 89 link → 66 aperti → 1 prenotazione. Sulle richieste spontanee il link regge
meglio (altro caso: 32 link → 23 prenotazioni), ma il bot che prenota toglie anche quel salto.

Link di prenotazione con source dedicato per canale (`?source=bot-whatsapp`, `bot-instagram`,
`bot-facebook`) per misurare cosa porta l'automazione. **Divieto esplicito nel prompt, canale per
canale**: su Instagram solo `bot-instagram`, su Facebook solo `bot-facebook`, su WhatsApp solo
`bot-whatsapp`, mai altro — il bot può confondersi e mandare il source sbagliato (caso reale: 4 su 4
casi di `bot-whatsapp` mandato anche su IG/FB), rendendo invisibile il ritorno dei social. Dopo una
settimana controlla le provenienze delle prenotazioni; nel report i `bot-*` vanno mappati come canali
separati.

### Altre regole di prompt

- Breve non vuol dire freddo: sempre una parola di cortesia prima ("Certo!", "Buonasera!"), mai "ecco
  il link" secco.
- Il bot NON vede lo stato della prenotazione. Mai "confermata", "annullata" o "riceverà la conferma"
  per richieste che lo staff deve valutare (asporto, modifiche, gruppi): la formula è "Mettiamo in
  lavorazione la sua richiesta e le rispondiamo a breve". Al massimo legge l'ultimo messaggio
  automatico, altrimenti passa allo staff.
- ⚠️ Con l'accettazione automatica spenta su Resmio, le prenotazioni del bot nascono "unconfirmed" e
  il cliente riceve subito dopo il WhatsApp "NON confermata": testo del bot e flusso di attesa vanno
  allineati alla scelta del locale (oppure la sala accetta subito) — soluzione definitiva ancora da
  trovare.
- "Il sistema dice chiuso" o "non mi fa andare avanti" vuol dire che quell'orario è al completo (il
  widget Resmio mostra "chiuso"): il bot propone un altro orario o passa allo staff. Regola provata
  nel pannello prima di salvarla.
- Mai inventare: niente adattamenti su intolleranze, mai l'orario di chiusura, mai "ingresso libero".
  Se manca nella knowledge base, si passa allo staff.
- **Coupon**: non si dà su richiesta. A chi lo chiede in DM il bot risponde con garbo che è un regalo
  che arriva per altre vie, manda il link di prenotazione col source del proprio canale e non
  raccoglie dati a mano. Chi il coupon ce l'ha lo mostra al tavolo: uno per tavolo, non si sommano
  (due coupon = due prenotazioni, a tavoli lontani). Se prenota il bot, nota "COUPON" sulla
  prenotazione. ⚠️ L'eventuale etichetta dedicata lato gestionale (es. etichetta rossa su Resmio per
  la sala) va verificata alla prima prenotazione in cui deve scattare davvero.
- **Dopo la visita, risposta a parole del cliente** (contributo di Andrea Chirivì, introdotta nel
  prompt v7 del 23/09, ancora presente nel v14): il bot prima legge e capisce, poi si regola così.
  - Contento o racconta la serata → ringrazia con calore, riprende un dettaglio preciso (piatto,
    serata, chi ha servito) e invita con garbo a scriverlo anche su Google. Il link va **scritto per
    esteso nel testo**, così si apre nel browser vero e non in quello interno di WhatsApp.
  - Tiepido o con un suggerimento → grazie senza discutere, più il link.
  - Lamentela o disservizio → NIENTE link: scuse sincere, chiede cosa è successo, passa allo staff.
  - "Grazie", "ok" o un'emoji → silenzio.
  - Mai chiedere né nominare le cinque stelle, mai promettere nulla in cambio, mai insistere.
  Non è gating: la richiesta col link l'hanno già ricevuta tutti, si evita solo di rimandarla a chi
  si lamenta. Questa regola vale per "il messaggio dopo la visita", qualunque sia (sondaggio di
  gradimento o richiesta diretta di recensione) — non è legata a un formato specifico.

## 3. Bot che prenota: dall'azione API Call alla rete di sicurezza

(contributo di Andrea Chirivì, supera il disegno a flusso di Luciano Purpi su Barresi, 19/09/2026)

### Metodo collaudato: un'azione «API Call» diretta

Al posto di "Informazioni di contatto" + flusso + attesa, un'unica azione **API Call** (es.
"Registra prenotazione tavolo") verso una rotta del server del locale, con `silenzioso=1` se la
conferma la manda già il ponte. Il body JSON lo raccoglie l'AI: data e ora `GG/MM/AAAA HH:MM`,
persone, nome, cognome, email, note, più un campo **OBBLIGATORIO** `conferma` (la parola con cui il
cliente ha detto sì). La risposta va mappata: esito, messaggio, orari alternativi.

Il "When" ha tre condizioni: solo WhatsApp, solo dopo il sì al riepilogo, una chiamata per
prenotazione coi dati dell'**ULTIMO** riepilogo — mai nello stesso turno in cui arriva l'ultimo dato
(rischio di saltare il "Confermo?").

Cosa fa la rotta:
- **(a)** Aggiorna nome e cognome del contatto GHL prima di prenotare: il numero può essere già in
  CRM con un altro nome, e la conferma WhatsApp saluterebbe la persona sbagliata (resta da
  verificare se farlo anche per le prenotazioni dal sito).
- **(b)** Se l'orario è pieno, restituisce i 6 orari liberi più vicini all'ora chiesta, arrotondati
  alla mezz'ora, non i primi della serata (coi primi quattro il bot arrivava a dire che un orario
  richiesto non c'era).

Regole nel prompt: dopo un esito negativo rifai il riepilogo e richiama l'azione; dì "la segno" solo
dopo un nuovo esito positivo; orari solo a mezz'ore.

**Perché**: l'azione "Informazioni di contatto" scrive solo i campi VUOTI e, se eseguita coi dati del
riepilogo precedente, la prenotazione può perdersi silenziosamente (es. chiesto un giorno/ora per N
persone, prenotato il giorno/ora della richiesta precedente). Collaudata dal vivo: prenotazione in 2
secondi. Il metodo a flusso di Luciano resta valido dove non c'è un server per la rotta (vedi sotto).

⚠️ Per la rotta usata nel metodo a flusso, il nodo Webhook di GHL vuole i parametri in
**QUERYSTRING**: col body JSON risponde 412. Data e ora in ora locale `AAAA-MM-GG HH:MM`. Il nodo
Webhook ha due posti con lo stesso nome di parametro — la querystring dell'URL (letta davvero) e
"Dati di personalizzazione"/body (ignorato): modificare solo il secondo non fa niente. Meno
rilevante con l'API Call diretta sopra.

### ⚠️ Rete di sicurezza: la frase in chat non prova l'azione (da verificare il ramo "prenota")

Il bot può scrivere "la segno subito", "è confermata" o "Mettiamo in lavorazione…" senza aver
chiamato l'azione (caso reale: 28 promesse in due settimane, 2 prenotazioni perse). Il bot chiama
l'azione sulle chat senza storico, ma non su quelle che contengono già lo stesso botta e risposta. La
rete è un giro lato server che gira **fuori sessione**:
- ⚠️ **(a) Non ancora scattato su un caso vero, resto da verificare sul campo**: tre minuti dopo una
  promessa senza prenotazione registrata, rilegge l'ultimo riepilogo. Se è chiaro e il cliente non ha
  già un tavolo quel giorno, prenota; altrimenti mette una nota sul contatto e il tag di passaggio
  allo staff.
- **(b) Confermato**: chi è in attesa di conferma — si legge la sua chat. Un sì breve vecchio di 90
  secondi diventa conferma sul gestionale. Un'altra risposta senza seguito per 10 minuti fa partire
  il tag di passaggio e l'avviso.
- Alternativa senza server: flusso senza trigger lanciato dall'agente — tag → attesa 2 min → si
  azzera PRIMA il tag che il ponte metterà (chi ha già prenotato in passato lo ha) → webhook →
  avvisi → svuota campi → attesa 20 min (il ciclo del ponte tipico è 10 min). Se il tag del ponte
  manca, parte un'email di ALLARME ("inseriscila a mano, poi scrivigli che è tutto a posto: lui pensa
  di avere il tavolo"). Se il ponte è fermo l'allarme suona anche a prenotazione presente: il nodo
  Webhook non espone la risposta, quindi si controlla col segnale del ponte.
- Il simulatore non basta: il collaudo si fa dal vivo (vedi sezione Collaudo).

## 4. Human Handover e ripiego

(contributo di Andrea Chirivì, 2026-10-12)

GPT 4.1 a volte scrive la chiamata allo strumento come testo (JSON col nome dell'azione) invece di
eseguirla. GHL allora manda la frase fissa e non modificabile "I am sorry, I do not have enough
information to help you.": niente passaggio, niente tag, staff mai avvisato — quasi sempre su
disdette (caso reale: 7 casi).

Rimedi:
- **Final Message in italiano su OGNI scenario**, compreso "Human Requested", che di fabbrica è in
  inglese.
- Nel prompt: "sempre italiano salvo cliente che scrive in un'altra lingua" e "prima la frase, poi
  l'azione, mai nomi di azioni o JSON nel testo".
- Una **guardia esterna** ogni 2 minuti cerca la frase fissa nelle conversazioni, manda la correzione
  al cliente e avvisa lo staff. Se continua, cambia modello.

## 5. Passaggio allo staff e riattivazione del bot dopo l'handover

(contributo di Andrea Chirivì, 2026-10-12)

Oltre agli scenari di fabbrica (Human Requested, Lack of information, Failed to resolve) e allo
scenario Disiscrizione (vedi `whatsapp-ghl-locale/references/orecchio-e-stop.md`), serve uno
scenario **"Passaggio allo staff"** per: lamentele, eventi privati e torte, gruppi oltre soglia,
asporto, candidature, modifiche e disdette.

Ogni passaggio: assegna la conversazione, mette il tag "human handover", crea un task e manda un
messaggio finale in italiano che non promette ("Mettiamo in lavorazione la sua richiesta e le
rispondiamo a breve"). Poi mette in pausa il bot su quella chat.

⚠️ **Va spuntato "Reactivate bot after" con N ore (valore da decidere col cliente/locale)**: senza,
il contatto resta "AI Bot (inactive)" per sempre. Togliere l'assegnatario NON lo riaccende: va
rimesso **Active** dal riquadro accanto al campo messaggio. Caso reale: 17 chat WhatsApp su 100 senza
più risposte del bot (0 su 14 assegnate, 14 su 14 libere), due disdette rimaste senza lavorazione.

Scrivi le condizioni strette: solo le proposte musicali vanno al referente artistico; agenzie,
fornitori, app e sondaggi ricevono una riga ("scriva a info@…") e NON vanno allo staff; band e
menzioni nelle storie (allegati che il bot su Instagram non legge) meritano un grazie fatto a mano.

## 6. Impostazioni dell'agente

(contributo di Andrea Chirivì, 2026-10-12)

Nel prompt: nessuna risposta a messaggi automatici, truffe e phishing, link nudi e "Message type is
currently not supported"; mai più di una risposta di cortesia consecutiva (caso reale: un
risponditore automatico ha innescato 11 risposte del bot in 3 minuti, fermate solo da un invio
fallito; a un phishing il bot ha scritto tre paragrafi).

In **Timing & Pacing**: tetto di messaggi per conversazione (indicativo: 75) e attesa di 2 secondi.

"**Send bot to sleep when I send a Manual/Workflow Message**" va lasciato OFF quando le conferme
partono via API o workflow e lo staff interviene spesso: con ON si spegnerebbe il bot su metà delle
chat. Il silenzio dopo la risposta di una persona si ottiene col prompt, non con questo switch (con
OFF il bot risponde anche dopo un template di workflow, es. ringrazia e manda il link dopo la
richiesta recensione). È una scelta da fare consapevolmente su ogni sub-account.

## Knowledge base del bot

(contributo di Andrea Chirivì, 2026-10-12)

La KB è il crawl delle pagine della sitemap del sito, collegata con trigger. Il crawl non contiene
eventi futuri, partite trasmesse, opzioni vegane o senza glutine, ingresso libero o no — senza
queste cose il bot inventa. Rimedio: una pagina web non linkata con le note di servizio della
settimana, aggiunta al crawler e aggiornata insieme ai turni (su WordPress con AIOSEO il noindex non
si imposta via REST). Leggi regolarmente la sezione "Knowledge gaps" (le domande rimaste senza
risposta: aria condizionata, caparra, partite, disdette) e rispondi con quella pagina.

## Manutenzione del prompt

(contributo di Andrea Chirivì + Luciano Purpi, 2026-10-12)

- Tetto di **2.000 parole** (il contatore GHL ne conta 1-2 in più): ogni regola nuova si compensa
  togliendo doppioni.
- Ogni versione si salva in un file numerato (`Bot_prompt_vNN_data.txt`) e si rilegge dopo il
  ricaricamento della pagina.
- Le modifiche si fanno in un momento tranquillo, con prova dal vivo, mai a servizio in corso: il
  prompt salvato è già live (vedi §1).
- Una frase che deve uscire identica si scrive nel prompt con "rispondi con queste parole:" seguito
  dal testo, poi si collauda nel simulatore — altrimenti GPT 4.1 la parafrasa e ne perde il punto
  (caso reale: sul coupon spariva la parola "regali").
- Scrivendo "- " a inizio riga l'editor crea un elenco puntato e mangia il trattino: dopo ogni
  incolla rileggi il prompt.

## Trappole

- **Agent Logs non mostrano i messaggi dei workflow**: nel registro (AI Agents → Agent Logs → View
  details) compaiono solo i messaggi del cliente e le risposte del bot, non quelli partiti dai
  workflow — il bot non li "vede". Un'azione o regola con condizione "solo se l'ultimo messaggio
  automatico proponeva…" non scatta mai. Aggancia condizione e prompt al **TESTO della risposta del
  cliente** (es. il testo del pulsante "Va bene, confermo"), con quella regola per prima nel prompt.
- **Automazioni native Meta che rispondono al posto del bot**: risposte in 1 secondo con un tono
  diverso dal bot (es. "Come ti chiami?") vogliono dire due bot sulla stessa chat — un'automazione
  nativa Meta. Le autorisposte di Messenger e Instagram non stanno in GHL ma in **Meta Business
  Suite → Posta → Automazioni** ("Risposta automatica", "Messaggio di assenza"). Business Suite si
  apre di default sul portfolio di un altro cliente: controlla il portfolio. L'interruttore nella
  lista e quello in Modifica non salvano: entra in Modifica, togli le spunte Messenger e Instagram,
  premi "Salva modifiche", poi ricarica e verifica. Il Messaggio di assenza scatta con la Posta in
  stato "Assente"; può riaccendersi da solo e non c'è registro attività: ricontrolla nel giro
  settimanale. Controlla anche la destinazione "messaggi" delle inserzioni attive e gli automatismi
  dell'app Instagram (Impostazioni → Strumenti per aziende, solo da telefono). *(contributo di Andrea
  Chirivì, 2026-10-12)*

## Revisione del bot e audit delle conversazioni via API

(contributo di Andrea Chirivì, 2026-10-12)

Leggi per intero tutte le conversazioni dal go-live: `conversations/search`, poi
`conversations/{id}/messages`. Header `Version: 2021-04-15` e User-Agent non di default (Cloudflare
risponde 403, vedi `diagnosi-suite/SKILL.md`).

Come si capisce chi ha risposto: via API `userId = ""` è una persona dello staff, `userId = None` è
il bot. Su WhatsApp il bot ha il numero del locale formattato e testo non da template, le conferme
hanno testo da template, lo staff ha il numero non formattato. Su Instagram e Facebook bot e persona
si distinguono solo dalla latenza (bot sotto 30 s). I passaggi allo staff sono
`TYPE_ACTIVITY_EMPLOYEE_ACTION_LOG` con `humanHandoverAction`.

Metriche per canale: messaggi in arrivo, risposte del bot e umane, latenza mediana, passaggi per
motivo, quanti hanno avuto una risposta umana in chat. Ritorno: prenotazioni col source `bot-*` e
quante sono arrivate. Le disdette ricevute in chat vanno incrociate col gestionale: quelle rimaste
aperte diventano falsi no-show.

⚠️ **Sentinella delle chat rimaste senza risposta** (da spostare fuori sessione — oggi gira su
`launchd` del Mac di un consulente, va portata su server/cloud o dichiarata "presidiata" al
cliente): gira ogni 10 minuti fra le 12 e le 24 e legge le conversazioni GHL. Se un messaggio in
arrivo resta senza risposta oltre 10 minuti, avvisa con una notifica e un tag che riusa il template
degli handover, al massimo un avviso ogni 30 minuti (caso reale: il bot è rimasto muto 85 minuti, 22
messaggi senza risposta, senza causa visibile, e nessuno se n'è accorto).

## Collaudo

### Il simulatore esegue le azioni per davvero

(contributo di Andrea Chirivì + Luciano Purpi, 2026-10-12)

**"Test your agent" esegue le azioni come in produzione**: una prova ha creato una prenotazione VERA
su Resmio con un contatto di prova che aveva il numero del locale. Prima di provare nel simulatore
un'azione che scrive servono un contatto di prova dedicato (**mai il numero del locale**) e il giro
di annullo già pronto; alla fine ripulisci.

Collaudo della catena end-to-end col metodo a flusso (Luciano): contatto di prova, campi impostati a
mano, iscrizione manuale (Contatto → Azioni → Flussi di lavoro → +). Deve venire tutto verde: attesa,
"Crea prenotazione" 200 con id, avvisi, campi svuotati. Poi deve comparire il tag del ponte con la
conferma all'ospite: è l'ultima riga che dimostra che il giro si chiude. Controlla che data e coperti
nella risposta siano i valori NUOVI. Attenzione al fuso: un orario UTC tipo `...T20:30:00Z` è un'ora
avanti in CET. Pulizia: cancella la prenotazione e rileggila (404 atteso). Togli il contatto dal
workflow prima dei 20 minuti o parte un falso allarme.

La prova finale si fa comunque **dal vivo, da un telefono vero**.
