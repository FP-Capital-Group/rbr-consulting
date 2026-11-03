---
name: funnel-email-crm
description: Genera il PDF (e il .txt gemello) del funnel email CRM (catenaria) per un cliente ristorante/pizzeria — 57 mail (posizionamento + 5 promo + 30 remind), la variante a tre binari, la variante breve "catenaria alla lista esistente → fidelity" e la newsletter settimanale di racconto, tutte sulla regola della promessa d'oro (apre con la promessa, offerta solo in fondo). PDF ReportLab con pagina di riepilogo. Usa quando l'utente chiede di scrivere la catenaria, il funnel email, le mail CRM di un locale, "genera i testi catenaria", "catenaria alla lista", "riattiva la lista", "porta la lista nella fidelity", "newsletter", "mail settimanale alla lista". Il file prodotto è l'input delle skill mail-funnel-ghl (caricamento su GoHighLevel) e catenaria-pienissimo (caricamento su Pienissimo Pro).
---

# Prompt: Genera il PDF del Funnel Email CRM per un cliente ristorante

## ISTRUZIONI PER CLAUDE

Devi generare un PDF completo del funnel email CRM per un cliente ristorante/pizzeria.
Il PDF verrà salvato sul Desktop dell'utente.

---

## ✅ CHECKLIST — DATI DA FORNIRE A CLAUDE

Prima di procedere, fornisci questi 4 punti. Senza di essi Claude non può iniziare.

**1. Nome del locale**
> es. Pizzeria Cipriano

**2. URL Google Maps del locale**
> es. https://maps.app.goo.gl/...
> *(Claude cerca SOLO fatti verificati dall'URL Maps: indirizzo, telefono, orari, recensioni, premi/riconoscimenti — se un dato non si trova non si inventa, si lavora sul posizionamento dato dal cliente o si chiede. Vedi "Prove nelle mail".)*

**3. Descrizione del posizionamento del cliente**
> Cosa lo rende unico: chef, tecnica, ingredienti, storia, premi, territorio…
> es. "Pizza napoletana con farine certificate Residuo Zero, Mario Cipriano pizzaiolo napoletano, 3 Spicchi Gambero Rosso, locale nel quartiere San Frediano a Firenze"

**4. Lista delle 5 promo**
> Per ognuna: cosa offre e condizioni principali
> es.
> 1. 2x1 su tutte le pizze
> 2. 30% di sconto su tutto il conto
> 3. Bottiglia di vino a scelta in omaggio
> 4. Padellino farcito in omaggio (3 gusti a scelta)
> 5. Dolce per tutto il tavolo in omaggio

---

## REGOLE FISSE DI SCRITTURA

- **Apertura di ogni mail:** `Ciao @@nome@@,`
- **In ogni mail va sempre incluso almeno un elemento di posizionamento del cliente** (un dato, un riconoscimento, un dettaglio sulla tecnica, sulla storia o sul prodotto che rafforza l'identità del locale)
- **Chiusura di ogni mail:** frase tipica associata al cliente — unica, non generica. Claude ne propone 3 opzioni e aspetta la scelta prima di generare il PDF
- **Formato frase di chiusura:** `[frase ad effetto]` + a capo + `Il team di [Nome Locale] [emoji]` — senza indirizzo, telefono o link
- **CTA delle mail promo:** `🎟️ Scarica il coupon` → variabile `@@link_coupon@@`
- **Variabili CRM:** `@@nome@@` · `@@link@@` · `@@link_coupon@@`
- **Tono:** narrativo, caldo, frasi brevi, paragrafi di 1-3 righe, storytelling emozionale che porta alla CTA

- **Persona grammaticale — regola fondamentale:**
  La comunicazione è sempre **IO → TU** (o **IO → LEI** per locali eleganti/lusso). Mai usare il plurale "noi/volevamo".
  - ❌ "Volevamo ricordarti che…" — impersonale, nessuno sa chi parla
  - ✅ "Voglio ricordarti che…" — diretto, personale, coinvolgente
  - ✅ "Le volevo ricordare che…" — tono distinto per locali di lusso
  Il "noi" è ammesso **solo** quando si fa riferimento esplicito allo staff/team del locale (es. "noi in cucina scegliamo ogni ingrediente con cura"). In tutti gli altri casi: prima persona singolare.

---

## REGOLA DELLA PROMESSA D'ORO

Prima di scrivere serve la **promessa d'oro** del cliente in una riga, approvata da chi segue
il cliente. Deve passare 4 filtri: domanda che esiste già, marginalità, credibilità,
scalabilità. Servono almeno **3 prove verificabili**: numeri, premi con anno e giuria, nomi
propri (vedi sotto "Prove nelle mail").

**Ordine dentro OGNI mail, comprese promo e remind** (non solo nelle mail di posizionamento):
1. si apre con la promessa (un fatto, una scena, un numero, una prova), **mai con l'offerta**;
2. il corpo la dimostra con UNA sola idea;
3. un ponte porta all'invito;
4. l'offerta va in fondo, piccola e legata al contesto (ultimo terzo o P.S.);
5. **mai** "sconto", "promo", "gratis" o percentuali nell'oggetto, nel preheader e nella prima frase.

**Mai mandare l'offerta da sola.** Unica eccezione, rara: se il posizionamento è già
fortissimo e riconosciuto, un 30% secco può reggersi da solo.

Una catenaria già attiva si riscrive **in place**: stessa struttura, cambiano solo i testi,
così chi è già dentro il funnel non perde il segno.

I 10 controlli prima della consegna di ogni mail (se uno non passa, si riscrive): vedi
`references/promessa-doro.md`.
*(contributo di Roberto/RBR — Piano Marketing RBR v1.0; confermato in produzione da Andrea Chirivì, 2026-10-12)*

---

## PROVE NELLE MAIL

- Dall'URL Google Maps del locale si cercano **solo fatti verificati**: riconoscimenti,
  guide, numero e tono delle recensioni, quartiere, anno di apertura. Se un dato non si
  trova **non si inventa**: si lavora sul posizionamento dato dal cliente, oppure si chiede.
- **Test della prova** (Roberto): se metti il nome di un concorrente al posto di quello del
  locale e la frase resta vera, non è una prova.
- **TheFork non si cita mai come prova** (né voto né classifiche): è il mercato dello sconto
  e va contro il posizionamento. Le prove vengono da TripAdvisor, Google, guide e premi con
  l'anno, anni di attività.
- Anche luoghi e distanze vanno verificati prima di citarli (mai una distanza "a sensazione").
*(contributo di Andrea Chirivì — fatti verificati, mai TheFork; Roberto/RBR — test del concorrente, 2026-10-12)*

---

## TONO DEI REMIND (crescente per ogni promo)

| Remind | Tono |
|---|---|
| R1 | Soft reminder — l'offerta è ancora disponibile |
| R2 | Rinforzo del valore — qualità e benefici dell'offerta |
| R3 | Promemoria con urgenza lieve |
| R4 | Social proof — una prova vera (numero di recensioni, una frase che torna spesso nelle recensioni), mai "molti clienti stanno già approfittando" se non è un dato |
| R5 | Ultimi giorni — la promo sta per terminare |
| R6 | 48 ore — ultima chiamata, scadenza imminente |

**Struttura obbligatoria di ogni remind:**
1. Frase di promemoria offerta (IO → TU, mai "volevamo")
2. **2-3 righe di posizionamento** — ricordano perché scegliere questo locale (ingredienti, tecnica, chef, premi, atmosfera…)
3. CTA: `🎟️ Scarica il coupon` + `@@link_coupon@@`

Un remind senza posizionamento è troppo scarno: con le 2 foto nel template la mail diventa quasi solo immagini, con rischio spam alto.

**Foto nei remind: solo 1 immagine in alto (header). Nessuna foto nel body o in fondo.**
Le mail di posizionamento e promo possono avere 2 foto se il testo è adeguato.
Ratio testo/immagine bassa = penalità antispam.

---

## STRUTTURA DEL FUNNEL (57 mail totali)

| Blocco | Tipo | Quantità |
|---|---|---|
| Apertura | Posizionamento | 4 mail |
| Promo 1 | Promo + 6 Remind | 7 mail |
| | Posizionamento | 3 mail |
| Promo 2 | Promo + 6 Remind | 7 mail |
| | Posizionamento | 3 mail |
| Promo 3 | Promo + 6 Remind | 7 mail |
| | Posizionamento | 3 mail |
| Promo 4 | Promo + 6 Remind | 7 mail |
| | Posizionamento | 3 mail |
| Promo 5 | Promo + 6 Remind | 7 mail |
| Chiusura | Posizionamento | 6 mail |
| **TOTALE** | | **57 mail** |

---

## VARIANTE A TRE BINARI (quando il CRM conosce le visite)

Se il locale ha nel CRM data ultima visita e numero visite (tipicamente GHL con ponte dal
gestionale), proponi la catenaria a **tre binari separati** invece del funnel lineare:
RACCONTO a tutti (mai sconti) · PREMIO a chi viene (una cosa, mai uno sconto, non prevedibile) ·
RIAGGANCIO a chi si è fermato (l'unico con offerte). Regola: la promozione è uno strumento per chi
non viene, non un premio per chi viene. Tetti: max 3 gesti/anno a persona, di cui max 1 sconto;
silenzio promozionale 90 giorni dalla visita; invio giovedì 11:30. Il testo automatico dice solo
cose sempre vere (prodotti come repertorio, non come stock del giorno).
Dettagli, freno anti-cliente-da-sconto e tempi del riaggancio: `references/tre-binari.md`
(contributo di Luciano Purpi, 13/09/2026).

---

## VARIANTE BREVE: catenaria alla lista esistente → fidelity (mossa 8 di Roberto)

Da usare quando il locale ha una **lista ferma** (contatti senza automazioni attive) e la
mossa scelta dal Piano Marketing RBR è la 8.

- Prima si pulisce e si segmenta la lista: fonte, zona di residenza, ultima visita.
- Una sola idea per messaggio, e ogni messaggio apre con la promessa:
  - **giorno 0**: chi siamo oggi, la promessa e la prima prova;
  - **giorno 3**: la prova più forte (premio, prodotto, processo);
  - **giorno 6**: persone e territorio;
  - **giorno 9**: l'invito — "iscriviti alla fidelity, il regalo ti aspetta";
  - **giorno 14**: ultimo richiamo con scadenza vera.
- Mail e WhatsApp insieme dove c'è il consenso. Chi si iscrive esce dalla sequenza ed entra
  nel benvenuto.
- Dopo la sequenza, **riattivazioni per sempre**: chi non viene da 90 giorni riceve un motivo
  concreto (è il riaggancio della variante a tre binari sopra); chi è venuto una sola volta
  riceve un invito entro 30 giorni.
- Se la lista non c'è o è minuscola, la mossa salta e la lista si costruisce prima con altre
  leve di acquisizione contatti.

Trigger per riconoscere quando usarla: "catenaria alla lista", "riattiva la lista", "porta
la lista nella fidelity".
*(contributo di Roberto/RBR — Piano Marketing RBR v1.0, mossa 8, settembre 2026)*

---

## MAIL FUORI CATENA: COMPLEANNO

- L'oggetto e l'inizio del corpo **non nominano il regalo**. Prima viene il perché festeggiare
  proprio qui, con gli elementi del posizionamento (es. tavoli grandi che si accostano,
  musica, piatti da dividere). Poi il regalo, insieme alla CTA, più una riga per i gruppi
  grandi ("ti preparo tutto su misura"). Se il regalo sta in cima, la mail diventa un buono
  sconto e il posizionamento sparisce.
- Due mail:
  - **A**, per chi ha giorno e mese di nascita, 15 giorni prima, oggetto "Dove lo festeggi?";
  - **B**, per chi ha solo il mese, 10 giorni prima che il mese cominci, oggetto "Il mese
    prossimo compi gli anni".
- La mail B parte solo con la condizione **tag del mese E campo giorno/mese di nascita
  vuoto**, altrimenti chi ha entrambi i dati riceve due mail. In fondo chiede il giorno
  esatto con un link d'iscrizione alla fidelity.
- La soglia del regalo (es. per gruppi grandi) si scrive come incentivo ("se siete almeno in
  dieci"), non come paletto che esclude.
- Il testo deve restare generico, senza dati specifici di un altro cliente.
*(contributo di Andrea Chirivì, 2026-10-12 — versione definitiva dopo test con il regalo in
cima, risultato peggiore)*

---

## PRIMA PAGINA DEL PDF (riepilogo automatico)

Il PDF inizia con una pagina di riepilogo:
1. **4 riquadri colorati** con i contatori: Posizionamento · Promozioni · Remind · Totale mail
2. **Tabella delle promo** (colonne: Promo, Tipo/Offerta, Descrizione)
3. **Schema dei 6 remind** con il tono crescente
4. **Frase di chiusura** scelta

Poi il funnel completo con label colorate:
- 🟡 Giallo = posizionamento
- 🟢 Verde = promo
- 🔵 Ciano = remind

---

## WORKFLOW PASSO-PASSO

1. L'utente fornisce i 4 dati della checklist
2. Claude cerca il locale sul web — **solo fatti verificati** (indirizzo, telefono, orari, recensioni, riconoscimenti): vedi "Prove nelle mail"
3. Claude propone 3 opzioni di frase di chiusura — **aspetta la scelta dell'utente**
4. Claude scrive ed esegue uno script Python con ReportLab (vedi "TECH" sotto per la convenzione motore/dati separati)
5. Il PDF viene salvato sul Desktop come: `Funnel_Email_[NomeLocale]_[Città].pdf`, insieme al file `.txt` gemello per il copia-incolla

---

## TECH: generazione PDF

Usa **ReportLab** (non WeasyPrint — non è disponibile su macOS senza librerie di sistema).

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
```

Struttura dello script:
- Lambda `S(name, **kw)` per creare stili in modo compatto
- Funzione `add(tipo, label, oggetto, lista_paragrafi)` per ogni mail
- Funzione `section(titolo, tipo)` per i titoli di blocco
- Variabile globale `CHIUSURA` con la frase scelta
- Prima pagina: riepilogo con `Table` (riquadri contatori + tabella promo + schema remind) — **senza PageBreak**, separato dal funnel con `HRFlowable`

### Convenzione motore/dati separati (da portare a regime)

⚠️ **Nota per chi usa questa skill**: esiste una versione locale più avanzata del motore
(script + font), tenuta finora fuori dal plugin — qui restano documentate la convenzione e
le trappole note, ma lo **script e il font vanno copiati nel plugin da chi li ha** (non
sono stati creati/fabbricati in questa integrazione: un font o uno script non verificati
non vanno spacciati per quelli testati).

1. **File separati**: un template `scripts/template_funnel_pdf.py` (il motore, non si tocca)
   e, a fianco, un file dati per cliente (es. `dati_funnel.py`) con `NOME_LOCALE, CITTA,
   CHIUSURA, PROMOS, MAILS, SEZIONI`. Le correzioni si fanno solo nel file dati. La chiusura
   va aggiunta in automatico a ogni mail dal motore, non ripetuta in `MAILS`. Se le mail non
   sono 57, lo script deve avvisare e stampare il conteggio, da mostrare alla consegna.
2. **Emoji**: con Helvetica non si vedono. Serve un font monocromatico con licenza libera
   (es. OFL) registrato nello script, con ogni sequenza emoji avvolta in un tag di font
   dedicato via regex (intervalli Unicode emoji + selettori di variazione + ZWJ). Se il font
   manca, il testo deve uscire senza emoji **senza rompere lo script**.
3. **Percorso del font risolto relativo allo script** (es. `os.path.dirname(os.path.abspath(__file__))`),
   mai un percorso fisso assoluto: il template gira da una copia nello scratchpad, non dalla
   cartella originale della skill.
4. **File `.txt` gemello**: `Funnel_Email_<Locale>_<Città>.txt`, scritto dallo stesso script,
   un blocco per mail separato da una riga di 70 `=`, con etichetta, "Oggetto:", corpo e
   chiusura. È il file da usare per il copia-incolla, perché dal PDF le emoji si copiano male.
   `mail-funnel-ghl` e `catenaria-pienissimo` accettano sia il PDF sia il `.txt` come input.
*(contributo di Andrea Chirivì, 2026-10-12)*

---

## ESEMPIO DI MESSAGGIO DA INVIARE A CLAUDE

```
Genera il funnel email CRM per questo cliente:

Nome: Pizzeria Da Mario
Google Maps: https://maps.app.goo.gl/...
Posizionamento: pizza napoletana con farine biologiche, forno a legna,
Mario Esposito pizzaiolo con 20 anni di esperienza, locale in zona Prati a Roma

Promo:
1. Antipasto della casa in omaggio
2. 2x1 su tutte le pizze
3. 20% di sconto su tutto il conto
4. Bottiglia di vino a scelta in omaggio
5. Dolce per tutto il tavolo in omaggio
```
