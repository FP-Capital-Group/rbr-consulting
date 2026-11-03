# Invio WhatsApp di massa

> Contributi di Luciano Purpi (2026-09-08): Bulk WhatsApp da Contatti, checklist
> prima dell'invio, messaggio di benvenuto in coexistence.

## Dove si fa: Contatti, non Workflow

Per mandare un template a una lista **non serve costruire un workflow**:
**Contatti → seleziona (o "Select all N") → More → Send WhatsApp.**

La schermata "Bulk WhatsApp" chiede:
- nome azione;
- **numero mittente** (sceglilo sempre a mano: il "predefinito" può essere quello
  sbagliato, vedi SKILL.md);
- template (⚠️ nel menu compaiono ANCHE template **non ancora approvati**: verifica
  sempre che sia "Active" prima di sceglierlo — correzione di Andrea Chirivì,
  2026-10-12);
- fallback SMS opzionale;
- modalità:
  - Send all at once;
  - Send at scheduled time;
  - **Send in drip mode** → data/ora di partenza, Batch quantity, Repeat after
    (ore/giorni), Send on (giorni della settimana), Time Window (dalle/alle). Il fuso
    mostrato Europe/Amsterdam è lo stesso di Roma.

**Il drip è la ragione per cui questa strada batte il workflow**: rilasci a lotti e
non bruci un numero nuovo.

### Trappole dell'interfaccia (verificate 7 set 2026)
- Le viste Contatti e Workflow girano in **iframe cross-origin**
  (`client-app-*.leadconnectorhq.com`). Nei **Workflow i click sintetici NON arrivano**
  dentro l'iframe: quella schermata non è pilotabile da automazione. In **Contatti
  invece funzionano**. Aprire l'URL dell'iframe da solo non serve: si autentica solo
  dentro la pagina madre. (⚠️ Per il builder dei workflow questa regola è superata a
  scheda visibile: vedi `mail-funnel-ghl/references/builder-ghl.md`.)
- Le pagine impiegano **30-60 secondi** a comparire: aspetta davvero prima di
  concludere che sono rotte.
- Se una vista resta bianca all'infinito, apri una scheda nuova e chiudi la vecchia.
  Causa più comune: la finestra Chrome è coperta (`document.visibilityState =
  hidden`), non un guasto — vedi SKILL.md "Trappole d'ambiente".

### Trappole dei filtri Contatti (contributo di Luciano Purpi, 2026-10-12)
"Aggiungi filtro" crea un gruppo **OR**: l'AND si fa con "Aggiungi un filtro
annidato". Cambiare operatore **svuota il valore**. Dopo aver cambiato un chip si
toglie il vecchio, si applica e si **RILEGGE il contatore** (caso osservato: letti 4
contatti dove erano 143). Dopo "Seleziona tutto N" la barra azioni si sposta: un
clic sulla vecchia posizione di "Più" può aprire "Elimina in blocco" per errore.
Chiudere il dialogo di successo azzera la selezione; il checkbox d'intestazione
prende solo i 20 contatti della pagina e resta attivo cambiando pagina; in
"Etichetta è uno tra" un doppio clic **deseleziona**; il toast "rimozione
etichette" dopo "Aggiungi" è una traduzione sbagliata dell'interfaccia, non un
errore reale.

## Checklist prima di premere invio

Sembrano ovvi e non li fa nessuno.

### 1. La rubrica del ristoratore contiene i fornitori
I contatti importati dal telefono del titolare non sono clienti: sono clienti +
fornitori + servizi + numeri salvati per lavoro. Caso Red Mike (set 2026): su 126
contatti esaminati, 21 da escludere — fornitori di bibite, Metro, materiali, carne,
panini, focaccine, un bar, una casa di riposo, perfino il chatbot di un operatore
telefonico, più alcuni "Cliente" senza nome vero. Mandare "ho 10 euro in regalo per
la tua prossima cena" al fornitore delle bibite è una figuraccia con chi lavora col
locale ogni giorno.

**Come**: crea un tag `fornitore`, cerca per parole chiave (Bibite, Metro, Bar,
Ristorante, Srl, Forno, Ingrosso, Plastic, Carne, Cliente, nomi di aziende locali),
tagga ed escludi dal filtro d'invio. Togli anche i **contatti di prova** creati
durante il setup.

### 2. Il numero WhatsApp è nuovo? Scaldalo
Un numero in stato "Coexistence" con quality rating **vuoto** non ha nessuna
reputazione presso Meta. Il rischio **non è il limite giornaliero** (sul portfolio
dell'agenzia è già alto, vedi `costi-limiti-misura.md` — irrilevante per liste da
qualche centinaio): il rischio sono le **segnalazioni**. Bastano poche persone che
bloccano nelle prime ore e la qualità del numero crolla, con limitazioni a seguire.

**Come**: primo lotto piccolo come **sonda (~50 contatti)** in fascia diurna, **48
ore** di osservazione di quality rating e risposte, poi si alza. Il drip mode serve
esattamente a questo.

### 3. Messaggi automatici dell'app spenti (coexistence)
Se il titolare ha un messaggio di benvenuto nell'app WhatsApp Business, chi risponde
all'offerta riceve prima quello e poi il messaggio buono. Spegnerlo dal telefono del
titolare (Impostazioni → Strumenti per l'azienda → Messaggio di benvenuto; controlla
anche Messaggio di assenza e Risposte rapide). Dettagli nella SKILL.md.

### 4. Il resto
- STOP attivo e testato (`orecchio-e-stop.md`); filtro d'invio esclude il tag di
  esclusione e il tag `fornitore`.
- Marketing solo a chi ha `consenso-marketing`; liste fredde → procedura in
  `consenso-e-liste.md` (primo messaggio = consenso).
- Link del template tracciati `source=whatsapp-<campagna>`.
- **Credito del wallet controllato prima dell'invio.** Quando il wallet del
  sub-account si svuota, i template falliscono con "Location has insufficient
  funds" **senza nessun avviso**: un massivo può fermarsi a metà. Prima di un
  invio: credito ≥ N destinatari × costo a messaggio (vedi `costi-limiti-misura.md`
  per le cifre aggiornate); ricarica automatica consigliata **$25 con soglia $10**
  (una ricarica $10/soglia $0 non tiene il passo di un massivo). L'URL diretto del
  wallet resta bianco: entra da Settings → Billing → Wallet & Transactions.
  (contributo di Andrea Chirivì, 2026-10-12)

### 5. Rubrica entrata in coexistence: travaso e esclusioni (contributo di Luciano Purpi, 2026-10-12)
Poche ore dopo il collegamento in coexistence la rubrica del titolare entra nel
CRM: compaiono schede **senza nome**, col solo numero (clienti, fornitori,
conoscenti mischiati). Conta i contatti prima e dopo il collegamento, tagga in
blocco quelli creati quel giorno (`import-whatsapp-<data>`) ed escludili dagli
invii; costruisci la lista su "Nome non è vuoto" (tag `senza-nome`), perché "Ciao
{{1}}" manderebbe "Ciao , sono…" a migliaia di persone.

**Cinque esclusioni in AND prima di ogni invio**: `senza-nome`,
`import-whatsapp-<data>`, tag di esclusione (`no-marketing` / `whatsapp-stop`),
`whatsapp-non-raggiungibile`, chi ha già ricevuto il regalo/l'offerta. Fidati del
**contatore**, non della prima pagina della lista (ordinata per data: una pagina di
turisti recenti può sembrare migliaia di contatti ed essere solo una manciata).

**Ultimo controllo prima di premere invio**: leggi i NOMI della lista (sono usciti
un indirizzo email al posto del nome, e nomi/cognomi invertiti); togli chi ha già
fatto la cosa che chiedi (chi ha già recensito non si risollecita); escludi chi è
rimasto su `confirmed` (non è una visita avvenuta); mandati il messaggio e leggilo
(su un conto 3 template su 4 avevano le variabili scollegate, scoperto un'ora prima
di un invio da migliaia di contatti).

### 6. Massivo per una serata, lista da Resmio (⚠️ procedura confermata, risultati numerici da verificare caso per caso — contributo di Andrea Chirivì, 2026-10-12)
Lista: telefoni unici con prenotazione `arrived`/`seated`/`finished` su Resmio negli
ultimi 90 giorni, meno chi è già prenotato per quella sera; incrocio con GHL via
`/contacts/search/duplicate?number=`; filtro sul campo consenso marketing (sì = ok,
no = escluso, vuoto = chiedere al consulente); tag via API
(`POST /contacts/{id}/tags`) e poi Contatti → Filters → "Tag is". Template
Marketing con intestazione Image (locandina della serata) e pulsante "Visit
website" verso una landing con `?da=whatsapp` che firma la prenotazione Resmio con
una fonte dedicata. **Misura il giorno dopo** in due modi: fonte Resmio
`…-whatsapp` E incrocio dei telefoni della lista con le nuove prenotazioni (chi
risponde in chat e prenota col bot genera invece la fonte `bot-whatsapp`). Testo
sempre un invito in positivo, mai "abbiamo tavoli liberi".
