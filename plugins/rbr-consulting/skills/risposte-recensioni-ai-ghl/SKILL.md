---
name: risposte-recensioni-ai-ghl
description: Attiva e calibra le risposte automatiche alle recensioni Google di un ristorante con Reviews AI di GoHighLevel (Reputation) — collegamento schede GBP, agente con prompt RBR multilingua e SEO, tono, attesa, blocco delle recensioni sensibili, smaltimento dell'arretrato in Drip Mode. Usala quando il consulente dice "rispondi in automatico alle recensioni", "attiva Reviews AI", "il cliente ha 1.500 recensioni senza risposta", "copia il risponditore di Mister Pizza su X", "le risposte alle recensioni sono tutte uguali", "sistema il prompt delle recensioni". Metodo nato su Mister Pizza e replicato su Raíces (set 2026).
---

# Risposte automatiche alle recensioni con Reviews AI (GHL)

## Perché esiste
Rispondere alle recensioni fa SEO locale (Google legge le risposte), mostra un locale vivo
e recupera i clienti scontenti. Quasi nessun ristoratore lo fa con costanza: su Raíces
c'erano ~1.600 recensioni, 1.576 senza risposta. Reviews AI di GHL lo fa da solo, ma con il
prompt di default risponde in inglese, sempre con la stessa frase, e a volte ammette colpe
che il locale non ha. Questa skill è il modo RBR di accenderlo senza rischi.

## Quando usarla
- Cliente con sub-account GHL e schede Google Business collegate (o da collegare).
- Arretrato di recensioni senza risposta, o risposte fatte a mano in modo irregolare.
- Per l'ANALISI delle recensioni (punti forti/deboli, piano) usa invece `analisi-reputazione-locale`.

## Prerequisiti
1. Sub-account GHL del cliente operativo (`onboarding-cliente-ghl`) e istanza MCP `ghl2-<cliente>`.
2. **Scheda Google Business collegata DAVVERO** (Settings → Integrations → Google). L'account Google
   già collegato per Analytics/Ads **non è** il Google Business Profile: la scheda si collega col suo
   «Connect» proprio e l'OAuth dell'account proprietario (password/passkey le mette il cliente o il
   titolare, mai il consulente). Il popup OAuth si apre in una finestra separata: se l'automazione non
   la vede, cercarla con osascript (URL che contiene `accounts.google.com`) e portarla davanti. Un
   consenso rimasto a metà mostra un badge rosso «1» col tooltip «disconnesso» (l'icona di avviso non
   fa nulla): si riapre da «+ Aggiungi un altro account» nel dialogo Gestisci, poi in Reputazione →
   Integrazioni compare «Collega le pagine». Sincronizzazione ferma: staccare e riattaccare la scheda
   GBP in Integrazioni.
   **Controllo del primo giorno** (va fatto sempre, prima di toccare il resto): se in Reputazione ci
   sono SOLO recensioni Facebook, la scheda Google non è mai stata collegata e Reviews AI non tocca
   Google Maps — tutto il resto della skill è inutile finché non si risolve. Verifica che il mirror
   sia completo confrontando la distribuzione per stelle di Maps con il pull della lista in GHL.
3. **Piano AI attivo** («unlimited AI Employee», lo attiva l'agenzia/Marco): senza, non si possono
   creare agenti con prompt e firma propri. Verificalo PRIMA di promettere al cliente risposte con il
   tono del locale.
4. Dal cliente: nome con cui firmare (es. «Cesar - Raíces»), nomi ufficiali dei locali, piatti firma,
   mail per i problemi concreti, **regole di merito che tornano nelle negative** (divisione del conto,
   condizioni sconti/coupon, episodi passati da ammettere o no) e **la voce delle negative** (di
   default: a nome di tutto il locale, mai un nome singolo né "i titolari" — vedi Procedura, NEGATIVE).
   Chiedile tutte in un solo messaggio.

## Procedura
1. **Reputation → Settings → Reviews AI** → modalità **Auto Responses** (non «Suggestions»),
   **solo col piano AI attivo e l'agente RBR creato** (punto 3 dei Prerequisiti). Senza piano,
   «Auto Responses» si può selezionare lo stesso ma è la modalità **legacy generica**: solo
   tempo di attesa, niente prompt, niente firma, risposte generiche. Senza piano resta su
   «Suggestions», e l'arretrato si smaltisce col metodo a costo zero (sotto).
2. **Agente**: dal cliente già calibrato (Mister Pizza) prendi **struttura e guardie**
   (blocchi LANGUAGE e REGISTER, regole delle negative, divieti) — voce, lessico, empatia e
   posizionamento si riscrivono DA ZERO per il cliente nuovo, non si copiano. Campi: nome
   agente («Risponditore Recensioni <Cliente>»), business name, tono **Friendly +
   Solution-Oriented**, voce «We», firma nel campo firma (NON nel prompt: il prompt vieta
   firme per evitare doppioni). Se esiste un agente **«Legacy Reviews AI»**, disabilitalo dal
   menu ⋮ (altrimenti risponde lui al posto del nostro: risposte notturne, lingue mescolate o
   sbagliate sono quasi sempre sue).
3. **Prompt** — struttura RBR (modello completo in `prompt-modello.md`):
   - LINGUA: quella della recensione; se è solo stelle, dedotta dal nome (nome italiano → italiano,
     nome chiaramente straniero → quella lingua, altro alfabeto latino → inglese). Una sola lingua per risposta.
   - REGISTRO: «tu» di default in IT/ES/FR/PT, formale solo con recensioni polemiche; tedesco sempre «Sie».
   - IDENTITÀ: nomi ufficiali dei locali (mai soprannomi di zona), cosa è il locale in una riga.
   - SEO: ripetere il piatto che il cliente ha lodato col nome giusto + al massimo 1-2 keyword
     locali («tacos de birria», «ristorante messicano a Firenze») solo se ci stanno. Zero keyword nelle negative.
   - VARIETÀ: aprire e chiudere in modo diverso, le risposte stanno una accanto all'altra.
   - NEGATIVE (≤3 stelle): ringraziare, dispiacersi per come è andata, MAI ripetere l'accusa come
     fatto («ci spiace che abbiate aspettato», non «ci spiace di aver dimenticato l'ordine»), mai
     promettere rimborsi/sconti/azioni, mai scuse operative inventate. Invito alla mail SOLO se c'è
     qualcosa di concreto da verificare (conto, ordine, allergia, prenotazione, persona dello staff).
     **Voce di default: a nome di tutto il locale, senza gerarchie e senza nomi singoli** — mai «ce ne
     occupiamo noi titolari» né «uno di noi (tre)», perché scavalca i collaboratori che fanno il
     servizio ogni sera. Niente chiusure "a tu per tu" (niente "di' che sei tu quello della
     recensione"). Una variante in prima persona del titolare si usa SOLO se il titolare la chiede
     esplicitamente, e va scritta nel prompt come scelta sua, non come default.
     **Le negative (≤3★) le approva il titolare una per una prima della pubblicazione**, non basta
     la revisione del consulente (Hold sensitive le trattiene, ma la decisione è sua).
   - DIVIETI: telefoni, indirizzi, promo, sconti, riferimenti all'automazione, frasi vuote
     («saremo più attenti», «lavoreremo per»).
   Il prompt copiato da un altro cliente va ripulito da TUTTI i nomi e dalle espressioni tipiche di
   quel cliente: template, prompt dei bot e risposte alle recensioni non si copiano mai, solo il
   metodo.
4. **Sicurezza**: **Hold sensitive reviews = ON** (le risposte rischiose aspettano revisione umana).
   Attesa agente 1 min; attesa globale come Mister Pizza (15 min) — si imposta a mano.
5. **Arretrato**: crea una regola **Drip Mode** (es. tutti i giorni 9-17) per le recensioni vecchie,
   così non escono centinaia di risposte nello stesso minuto. Senza Drip l'arretrato non si smaltisce.
   Il target si ricalcola da solo dopo ogni sync, non serve ricreare la campagna. Se l'arretrato è
   grosso e il piano AI non è ancora attivo, vedi "Arretrato senza piano AI" sotto.
6. **Test**: fai generare 5 risposte di prova su recensioni reali (1 positiva con testo, 1 solo stelle,
   1 straniera, 1 negativa concreta, 1 negativa di gusto) e controllale contro le regole prima di attivare.
7. Salva il prompt finale nei file del cliente (`data/<cliente>/marketing/reviews_ai_prompt_<cliente>.txt`).
8. **Dopo un'ondata di risposte in blocco** (arretrato smaltito, Drip Mode partito): rileggi TUTTO
   dal server (pull della lista), non solo le 5 prove iniziali del punto 6 — possono emergere
   riscritture non passate, risposte fuori tono o in lingua sbagliata. A 48 ore dall'ondata,
   ricontrolla chi ha cambiato voto sulle negative: nel CRM il voto si aggiorna e la vecchia
   risposta resta appesa sotto la stella nuova — riscrivila ripostando (sovrascrive senza
   cancellare). Rispondere alle vecchie negative non è archeologia: anche una recensione del 2022
   può cambiare voto dopo la risposta.

## Arretrato senza piano AI (metodo a costo zero)
Per centinaia di recensioni arretrate quando il piano AI non è ancora attivo, o per correggere
risposte sbagliate già pubblicate, si pilota Reputation dal browser con la sessione già aperta
(Reputation non è in iframe). Le chiamate a `backend.leadconnectorhq.com` non compaiono nei log
di rete standard: serve un hook su XMLHttpRequest che intercetti header e URL della lista, con
filtro esatto su `pathname === '/reputation/reviews'`. Lista via `GET
/reputation/reviews?filterParams[locationId][0][value]=<loc>&pageSize=100&pageNumber=N`
(parametri `pageSize`/`pageNumber`, non `page`/`limit`); `replies[]` vuoto = senza risposta;
`source 71` = Facebook. Senza piano i testi li scrive Claude con le regole del prompt RBR e la
firma del locale (mai «agente AI»); con piano si possono generare dall'agente via API
(`/reputation/ai-reviews/generate-reply/job` → poll su `/replies/{jobId}/status`). Pubblicazione:
`POST /reputation/reviews/google/reply` o `.../facebook/reply` — ripostare sulla stessa
recensione SOVRASCRIVE la risposta esistente, utile per correggere senza cancellare. Ritmo:
blocchi piccoli con una pausa fra una richiesta e l'altra; su Facebook procedere una richiesta
alla volta, mai in parallelo (recensioni vecchie possono comunque essere rifiutate). Le negative
le approva il titolare una per una prima della pubblicazione, come al punto 3. Se il controllo di
sicurezza del client blocca l'esecuzione o la pubblicazione diretta, prepara i testi in un file e
fallo pubblicare a mano dal titolare o dal consulente.
*(metodo di Luciano Purpi, cliente Barresi; rifiniture di Andrea Chirivì sul Noolas — pacchetto
migliorie 2026-10-12)*

## Regole RBR & trabocchetti
- La tendina della **lingua di riserva** resta su English e non si cambia in automazione: falla a mano.
- Le risposte manuali restano possibili: da GBP, `google.com/local/business/<ID>/customers/reviews`
  (fuori dall'iframe della ricerca la tastiera funziona) → Rispondi → rientrare dalla lista dopo ogni invio.
- Mai frasi tipo «lascia una recensione e hai lo sconto»: vietato da Google.
- Il prompt copiato da un altro cliente va ripulito da TUTTI i nomi (locali, piatti, firma, mail).
- **TripAdvisor** è fuori da GHL: la risposta esce col nome dell'account che la scrive (da un
  account consulente compare «Nome Cognome, Agenzia/Consulente»). Se il cliente vuole le
  risposte a suo nome serve il SUO login, da chiedere prima di scriverne centinaia.

## Definition of Done
- [ ] Scheda GBP collegata col Connect del proprietario (non l'account Ads/Analytics) e recensioni Google visibili in Reputazione — controllo del primo giorno fatto
- [ ] Piano AI verificato; se assente, agente resta su Suggestions e arretrato smaltito col metodo a costo zero
- [ ] Agente Legacy Reviews AI disabilitato, se presente
- [ ] Auto Responses attivo, schede di tutti i locali collegate
- [ ] Prompt ricalibrato (lingua, registro, nomi locali, piatti, mail) e salvato nei file cliente
- [ ] Regole di merito e voce delle negative concordate col titolare; negative approvate una per una prima della pubblicazione
- [ ] Hold sensitive ON, firma nel campo firma, attese impostate
- [ ] Drip Mode per l'arretrato creato (o deciso con Marco di non farlo)
- [ ] 5 risposte di prova controllate e mostrate al consulente
- [ ] Dopo un'ondata in blocco: audit riga per riga dal server e ricontrollo a 48h di chi ha cambiato voto sulle negative

## Fonti/contributi
- Pacchetto migliorie del 2026-10-12 (Andrea Chirivì, casi Noolas e Barresi), con contributi di Luciano Purpi (metodo a costo zero, agente Legacy, trappole OAuth) citati nel testo.
