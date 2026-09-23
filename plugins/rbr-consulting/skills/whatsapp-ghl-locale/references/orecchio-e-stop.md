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
- **Ramo STOP**: messaggio contiene "stop" **OR** "basta" (aggiungi "cancellami" se
  vuoi) →
  1. tag `whatsapp-stop`;
  2. rimuovi tag `consenso-marketing`;
  3. **DND in uscita sul SOLO canale WhatsApp**;
  4. risposta breve di conferma (es. "Va bene, non ti scriviamo più. Se cambi idea
     siamo qui.").
- **Ramo None** (tutto il resto) → notifica interna a una persona precisa.

Dettagli che costano un'ora se non li sai:
- **DND "per canali specifici", non "tutti i canali"**: in GHL il DND è per canale.
  Chi scrive STOP su WhatsApp non ti toglie il permesso di mandargli la conferma del
  tavolo per email.
- **Il connettore fra due condizioni nasce in AND.** Due "contiene" in AND non
  scattano mai (nessun messaggio contiene entrambe le parole) e TUTTO finisce nel
  ramo None. Portalo a **OR** dal selettore in fondo al ramo e verifica che
  l'etichetta fra le due condizioni sia diventata "Or".
- Il campo da confrontare si chiama **"Replied message"** (gruppo Contact reply).
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
toccare i workflow (che spesso non sono nemmeno pilotabili dall'automazione browser).

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

## Test prima di dire fatto

Con un contatto di prova: scrivi "STOP" → controlla tag, DND solo WhatsApp, risposta
ricevuta (una sola, non "ti passo un collega"), e che il contatto sia escluso dal
filtro del prossimo invio.
