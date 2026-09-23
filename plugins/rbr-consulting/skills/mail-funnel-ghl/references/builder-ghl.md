# Builder GHL: workflow, editor email, attese, campi personalizzati

Trappole del lavoro in UI dopo aver caricato i template. Automazione browser in generale (iframe,
pagina bianca da scheda nascosta): `suite/memory/gohighlevel.md`, sezione Builder GHL.

## I workflow si montano a mano: consegna la specifica

(contributo di Luciano Purpi, 10/09/2026)

Non esiste API per creare/modificare workflow e l'editor gira in un iframe cross-origin
(`client-app-automation-workflows.leadconnectorhq.com`) che non riceve gli eventi sintetici di
Claude in Chrome (`contentDocument` null, `read_page` vede solo una region vuota "Workflow Builder";
l'URL dell'iframe aperto da solo resta in caricamento perché manca il token passato via postMessage).
**Non promettere mai al cliente che l'automazione la creiamo noi via browser.**

Cosa si fa a distanza:
1. importare contatti e tag via Contacts → Import (l'input file è nascosto: rendilo visibile via JS,
   poi `file_upload`);
2. leggere lo stato dei workflow a screenshot (nome, stato, iscritti totali e attivi, ultima modifica);
3. consegnare la **specifica di montaggio blocco per blocco** (trigger, rami, azioni, testi già
   scritti) che il cliente o il consulente monta in ~20 minuti.

Con clic e tastiera "veri" (browser integrato di Claude Code, o input di sistema) il canvas si
lavora a schermate e clic, con le trappole sotto.

## Canvas dei workflow

(contributo di Luciano Purpi, 13/09/2026)

- La rotellina SCORRE in verticale, non ingrandisce. Il trascinamento NON sposta la tela. La
  minimappa non è cliccabile.
- Niente JS né lettura della pagina dentro il canvas: solo schermate e clic.
- "Trova e sostituisci" NON tocca il testo delle email: lavora solo su valori personalizzati e tag.
- Gli URL diretti di GHL falliscono spesso (la rotta `/emails/templates` non carica mai): passa dalla
  barra laterale. La libreria modelli è `/v2/location/<id>/marketing/emails/all`.

## Email nei workflow: il nodo può avere una copia propria

(contributo di Luciano Purpi, 19/09/2026 — precisa la regola "modifica dalla libreria" del 13/09)

Il nodo Email può avere una COPIA PROPRIA del contenuto, diversa dal modello collegato: la spunta
**"Sincronizza le modifiche al modello"** è spesso TOLTA. In quel caso modificare il modello in
Marketing → Email → Modelli NON cambia cosa ricevono i clienti.

- Dalla libreria modelli si modifica solo se il nodo ha la sincronizzazione accesa (allora sono lo
  stesso oggetto, e ci arrivi con una ricerca per nome invece di venti scorrimenti).
- Altrimenti guarda e modifica SEMPRE la copia nel nodo: menu ⋮ sull'anteprima → "Modifica il design".
- Caso reale: la mail di consegna gift card diceva "grazie per aver prenotato" a chi NON aveva
  prenotato (testo di un'altra variante finito nel flusso sbagliato) e l'unico pulsante era "Guarda
  il menu". Spiegava da sola "15 sì → 0 prenotazioni". Il modello, non usato, puntava a un'altra
  landing: anche l'attribuzione era sbagliata.
- Vedi anche: "Select existing template" nel nodo non persiste (`suite/memory/gohighlevel.md`).

**Metodo sicuro per modificare la copia:** clic nel pannello codice, cmd+a cmd+c, leggi la clipboard
con `osascript -e 'the clipboard as «class utf8»'` (NON pbcopy: storpia gli accenti; `pbpaste` va bene solo per il collaudo dei link, dove gli accenti non contano),
modifica in locale, fai il diff, rimetti in clipboard con osascript, cmd+a cmd+v, poi RICOPIA e
ri-diffa prima di salvare. L'editor riformatta l'indentazione al paste: confronta ignorando le righe
vuote e con grep mirati sulle stringhe che ti interessano.

**Tre salvataggi in fila:** "Salva" nell'editor del design → "Salva azione" sul nodo → "Salva" sul
workflow. Saltarne uno = perso tutto.

**Controllo di routine:** su ogni funnel a più passi verifica che il testo dell'email corrisponda al
punto del percorso in cui si trova il cliente. I testi migrano fra flussi quando si duplicano i workflow.

## HTML nell'editor email: si incolla, non si scrive

(contributo di Luciano Purpi, 13/09/2026)

L'editor chiude i tag da solo: digitando `</div>` ottieni `</div>>`. Passa dagli appunti di sistema:

```bash
osascript -e 'set f to POSIX file "/percorso/email.html"' -e 'set the clipboard to (read f as «class utf8»)'
```

poi clic dentro il codice, cmd+a, cmd+v. NON usare `do shell script "cat ..."`: converte gli a-capo
in CR e l'HTML arriva su una riga sola.

Modifica chirurgica (un id immagine, un URL): clic appena prima dell'estensione, il cursore cade UN
CARATTERE PIÙ A SINISTRA del previsto → Right per correggere, Backspace a blocchi con uno zoom di
controllo ogni tanto. Backspace sì, Delete no.

## Attesa "fino a giovedì"

Interno → Attendi → tipo "Finché non si apre una finestra ricorrente" → Ogni settimana → spunta solo
giovedì → ora. Le colonne del selettore sono ore | minuti | secondi | AM-PM: è facilissimo mettere
30 nei secondi e ritrovarsi alle 11:00:30. Il pannello mostra le **prossime cinque occorrenze**: si
verifica lì, non nel campo. (Perché giovedì 11:30: skill `funnel-email-crm`, `references/tre-binari.md`.)

Fuso orario: GHL non ha Europe/Rome, si usa Amsterdam (GMT+02:00). Se il sotto-account è già così
NON toccarlo: cambiarlo sposta tutte le attese già programmate.

## Dialogo campi personalizzati

I menu Tipo e Oggetto si sovrappongono e si annullano a vicenda. Ordine che funziona: **prima
Oggetto, poi Tipo, poi nome e cartella**. Un campo alla volta, verificando in lista prima del successivo.
