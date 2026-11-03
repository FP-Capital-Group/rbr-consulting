# L'orecchio (flusso in entrata) e la gestione dello STOP

> Contributi di Luciano Purpi: opt-out come workflow (2026-09-04), STOP con Human
> Handover (2026-09-08), orecchio nella forma minima montato su Noolas (2026-09-13).

La gestione dello STOP è il **requisito minimo di compliance prima di qualsiasi invio
di massa**, e il tag che applica è il filtro con cui si escludono quelle persone
dagli invii successivi. Senza, "Rispondi STOP" nei Marketing è una promessa a vuoto.

**Un solo tag di esclusione per conto.** Lo standard è `whatsapp-stop` (Noolas); su
Red Mike è stato usato `no-marketing`. Se il conto ne ha già uno, usa quello e non
crearne un secondo: due tag diversi = filtri che ne guardano uno solo.

Quale strada:
- **sul numero NON risponde un agente AI** → Strada A (workflow orecchio);
- **sul numero risponde un agente Conversation AI** → Strada B (scenario di Human
  Handover). Se non la monti, uno "STOP" cade nello scenario generico "Human
  Requested" e il cliente si sente rispondere "Ti metto in contatto con un collega":
  sbagliato e maleducato per chi chiede di essere lasciato in pace.

In entrambi i casi: la condizione **"ha il tag di esclusione → esci"** va **in testa
a ogni flusso di marketing**, non solo come filtro nel CRM. E il template Marketing
porta comunque il pulsante nativo "Marketing opt-out" (vedi `trappole-template.md`).

## Strada A — Workflow "orecchio" nella forma minima (Noolas, 13 set 2026)

**Trigger**: Customer Replied → canale WhatsApp.
- **Ramo STOP**: messaggio contiene "stop" **OR** "basta" **OR** "cancellami" →
  1. tag `whatsapp-stop`;
  2. **risposta di conferma (free form)**;
  3. attesa 1 minuto;
  4. **DND in uscita sul SOLO canale WhatsApp**;
  5. rimuovi tag `consenso-marketing` (o azzera il campo consenso).
  **⚠️ Ordine obbligato: la conferma va PRIMA del DND, mai dopo.** Dopo il DND non
  esce più nulla sul canale: con l'ordine vecchio (DND poi conferma) il cliente non
  riceve mai la conferma e non sa se è stato ascoltato (montato così su Noolas il
  22/09/2026). Verifica in collaudo che la conferma arrivi davvero prima del DND.
- **Ramo None** (tutto il resto) → notifica interna a una persona precisa.
- Filtro sul trigger Customer Replied: aggiungi **Corpo del messaggio · Non contiene
  · `<testo del pulsante opt-out>`** (una frase sola; non è documentato se un elenco
  di valori conti come OR o AND). Il tap sul pulsante nativo "Marketing opt-out"
  conta come risposta del cliente e farebbe scattare anche l'orecchio: senza questo
  filtro il titolare riceve "ha risposto a parole" a ogni opt-out. Per i template in
  inglese aggiungi anche il testo del pulsante inglese e verifica.
  (contributo di Andrea Chirivì e Luciano Purpi, 2026-10-12)

Dettagli che costano un'ora se non li sai:
- **DND "per canali specifici", non "tutti i canali"**: in GHL il DND è per canale.
  Chi scrive STOP su WhatsApp non ti toglie il permesso di mandargli la conferma del
  tavolo per email.
- **Il connettore fra due condizioni nasce in AND.** Due "contiene" in AND non
  scattano mai (nessun messaggio contiene entrambe le parole) e TUTTO finisce nel
  ramo None. Portalo a **OR** dal selettore in fondo al ramo e verifica che
  l'etichetta fra le due condizioni sia diventata "Or".
- Il campo da confrontare si chiama **"Replied message"** (gruppo Contact reply).
- **Enable branches genera rami SOLO dai pulsanti, mai dalle risposte scritte.** Su
  una campagna, 116 persone su 224 hanno risposto a parole — più di chi ha premuto un
  pulsante. I filtri del trigger si sommano in AND e non vedono le etichette: monta
  il trigger "Customer Replied" sul canale WhatsApp + un If/Else DENTRO il flusso sul
  campo Tags (ha il tag della campagna E non ha già la richiesta E non ha già la
  consegna → aggiunge il tag che fa partire la consegna). Una frase d'apertura fissa
  nel template aiuta a riconoscere chi risponde. (contributo di Andrea Chirivì e
  Luciano Purpi, 2026-10-12)
- Notifica interna di tipo **"Notification"** (in-app): non costa e non esce
  dall'account. La **"Pagina di reindirizzamento" è OBBLIGATORIA**: finché non la
  scegli il salvataggio fallisce con un generico "Please check the fields for valid
  inputs". Metti **Conversazione**, così il clic apre la chat giusta.
- **"A quale tipo di utente"** va scelto: "Tutti gli utenti" è il ripiego quando non
  sai chi risponde, ma la regola resta: se non decidi CHI riceve la sveglia hai
  ricostruito il silenzio un piano più in alto.
- **"Consenti il rientro" acceso**: un cliente scrive più volte.

## Strada B — Scenario di Human Handover "Disiscrizione" (Red Mike, 8 set 2026)

Negli scenari di Human Handover del Conversation AI **ogni scenario ha un Final
Message proprio e può applicare tag** al contatto: lo STOP si monta lì dentro, senza
toccare i workflow. (Nota: la regola "i workflow non sono pilotabili dall'automazione
browser" è superata se la scheda Chrome è visibile — vedi `mail-funnel-ghl` per il
dettaglio.)

**⚠️ Reactivate bot after deve essere SPUNTATO.** Se la casella non è spuntata, dopo
l'handover il contatto resta "AI Bot (inactive)" **senza scadenza**, per sempre:
caso osservato, 17 chat su 100 rimaste mute, due disdette della sera mai lavorate.
Togliere l'owner dal contatto non lo riattiva; si rimette Active dal riquadro con le
stelline accanto al campo messaggio. Controlla la spunta in ogni scenario di
handover e fai un giro periodico delle chat assegnate. (contributo di Andrea
Chirivì, 2026-10-12)

Agente → Actions → Human Handover → **+ New Scenario**:
- **Scenario name**: "Disiscrizione"
- **Trigger condition**: "Il cliente chiede di non ricevere più messaggi"
- **Example phrases**: "STOP", "non scrivetemi più", "cancellami dalla lista"
- **Assign to**: la persona del locale (+ "Skip assigning if contact has an assigned user")
- **Final Message**: la conferma vera per il cliente, es. "Va bene, non ti scriviamo
  più. Se cambi idea siamo qui."
- **Reactivate bot after**: lungo (8 ore o più)
- **Custom tags**: il tag di esclusione del conto (`whatsapp-stop` o `no-marketing`)
  + "human handover"

**Trappola**: il campo tag dentro l'agente accetta SOLO tag già esistenti, e la
ricerca per testo non filtra (scrive "No matching result" anche per tag che
esistono). Creali prima in **Settings → Tags**, poi sceglili scorrendo la tendina a
mano.

Da verificare sul conto: lo scenario applica il tag, ma il DND WhatsApp e la
rimozione di `consenso-marketing` non li fa. Se servono (liste con consenso
registrato), aggiungi un piccolo workflow "Tag Added: `<tag di esclusione>` →
rimuovi `consenso-marketing` + DND WhatsApp".

## DND di massa via import CSV

Le azioni di massa su Contatti non hanno un'opzione DND diretta: si fa con un
**import CSV** con colonna `DND = true`, modalità "Update contacts only", colonna
`Contact Id` mappata su "Contact ID". L'ultimo passo dell'import chiede di
confermare il consenso di tutti i contatti del file (clausola anti-liste comprate):
se il file include persone senza consenso, conferma solo dopo averlo detto al
cliente, non in silenzio. Il DND non è un tag "non contattare" (un tag da solo non
blocca niente) né la cancellazione del contatto (perde la memoria del rifiuto).
(contributo di Luciano Purpi, 2026-10-12)

## Test prima di dire fatto

Con un contatto di prova: scrivi "STOP" → controlla tag, DND solo WhatsApp, risposta
ricevuta (una sola, non "ti passo un collega"), e che il contatto sia escluso dal
filtro del prossimo invio.
