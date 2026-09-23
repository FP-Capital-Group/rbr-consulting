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
- template (compaiono solo quelli **Active**, cioè approvati da Meta);
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
  dentro la pagina madre.
- Le pagine impiegano **30-60 secondi** a comparire: aspetta davvero prima di
  concludere che sono rotte.
- Se una vista resta bianca all'infinito, apri una scheda nuova e chiudi la vecchia.

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
