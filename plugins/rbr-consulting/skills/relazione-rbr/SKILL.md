---
name: relazione-rbr
description: Genera relazioni/report professionali .docx brandizzati RBR (Restaurant Business Revolution) — header col logo, filetti rossi, tabelle, callout, firma. Usala quando il consulente chiede un "report RBR", una "relazione" per un cliente ristoratore (CDG, food cost, ottimizzazione personale, analisi vendite, piano marketing, relazione di ripartenza/una tantum) da consegnare in Word. Copre anche le regole di scrittura RBR per ogni documento al cliente (voce, cosa non scrivere mai, come e quando consegnare) — non solo la generazione del .docx.
---

# RBR Report

Building block riutilizzabili per produrre relazioni Word brandizzate RBR con stile coerente (rosso `#E30613`, navy `#1F4D78`, header/footer, tabelle, callout, firma), più le regole di scrittura RBR che valgono per ogni documento consegnato al cliente.

## Regole di scrittura (valgono per ogni documento al cliente)
1. **Voce**: prima persona del consulente che scrive — "ho analizzato", "ti propongo", "abbiamo misurato".
2. **Destinatario**: "tu", oppure "voi" se i titolari sono più di uno, oppure il nome del locale. Mai "il cliente".
3. **Vietate le frasi da lettore intermedio** ("da riportare al cliente", "il consulente può proporre", "X dovrà…") e le **sezioni-meta** (avvertenze, cose da dire a voce, task interni tipo "serve a noi"): quelle vanno in chat o nel diario, mai nel documento.
4. Con più soci si scrive al plurale. Con un socio solo: niente "tu per tu", niente citazioni di chi ha detto cosa, niente parole del cliente rigirate a lui.
5. **Niente riepiloghi** di cose già dette in call: solo i fatti nuovi o verificati che servono a decidere.
6. **Niente promesse operative o di risultato** e niente frasi che dichiarano RBR migliore di altri. Si scrive per obiettivi e proposte.
7. **Firma**: sempre il nome del consulente che presenta il documento, mai un nome fisso o "Restaurant Business Revolution" — vedi API `signature()` sotto, che ora richiede il nome esplicito (nessun default).

(contributo di Andrea Chirivì, 2026-10-12)

## Che relazione stai scrivendo
Distingui il tipo PRIMA di scrivere: la struttura e cosa entra/esce cambiano.

- **Relazione di piano** (cosa cambia e cosa fare): pagina 1 "cosa vi propongo" con le decisioni da prendere; poi "da decidere"; poi "cosa cambia" a capitoli per area; in chiusura l'elenco completo delle cose da fare a caselle e la checklist "da fare e da mandarmi". **Fuori**: analisi del passato/confronti con l'anno prima, previsioni in €, date di calendario (si scrive "entro il mese"), conti delle leve non ancora decisi (si scrivono "da valutare insieme"). Niente "chi fa cosa": l'operativo lo fa il titolare, il consulente non è sul posto. Prezzi solo se già decisi e calcolati sul food cost e provati in cucina, altrimenti si descrive solo la direzione.
- **Relazione di call o punto di lavoro**: aggiornamento puntuale, stessa voce e stesse regole di scrittura.
- **Analisi** (punto dati, CE, analisi menu): documenti separati, vedi sotto per il CE.
- **Relazione una tantum** (percorso a pagamento, es. 5.000 €): titolo-guida "perché fatturi tanto e non guadagni". Arriva dopo CE, analisi economica e food cost, e chiude con azioni scritte su menu e percorso — serve a vendere il percorso. È specifica: cosa fare, come farlo, cosa dire, con le frasi alla lettera quando servono. Non deve aver paura di dare valore (principio di Roberto Falcon: "la difficoltà non è avere il piano, è farlo"). **Attenzione**: "come farlo e cosa dire" non contraddice il punto 5 (niente riepiloghi) né "niente chi fa cosa" della relazione di piano — il come e le frasi ci sono, assegnazioni e calendario no.
- **Il conto economico coi numeri (perdite, EBITDA) si mostra al titolare in call, mai per iscritto nel pacchetto del percorso.** Per iscritto vanno road map, checklist, relazione del punto di lavoro e i file di analisi (food cost, modello di business).

(contributo di Andrea Chirivì, 2026-10-12; tipo "una tantum" — origine: Roberto Falcon)

## Mai per iscritto al cliente
- **Temi fiscali e delicati**: fuori busta ed extra ai dipendenti, acquisti senza fattura, prelievi, contanti, scarto fra cassa e corrispettivi, venduto non battuto, feste fuori cassa, rapporti col commercialista. Si trattano solo a voce in call, non si scrivono nemmeno su WhatsApp. Quando il tema serve comunque al piano (es. un divario di food cost, conti cancellati in cassa), scrivi **solo la regola e il controllo**, mai la cifra né la causa: es. "il divario sta fra la ricetta e la cassa" + le azioni (inventario, controllo acquisti, porzioni), la causa si dice solo in call.
- **Password dette in call**: non si scrivono da nessuna parte.
- **Rischi privati del cliente** (cause legali, trattative d'affitto) e **consigli negoziali interni nostri**: restano note interne.
- **Fornitori e agenzie terze** nominati o criticati, e persone dello staff.
- **Budget delle promo**.
- **Dati che non appartengono al cliente** (es. delivery fuori cassa) e confronti interni fra nostre ricerche.
- **Le nostre procedure e fonti** (chat rilette, Fathom, Plaud), compensi e acconti.
- **Mentori e metodi esterni** (nomi di mentor/metodi usati internamente), locali modello o altri clienti per nome: il ragionamento resta ma va scritto come proprio e motivato con un dato del cliente, oppure dichiarato come scelta da verificare. I confronti con altri clienti si fanno anonimi ("altri locali RBR"). Prima di consegnare: grep sui nomi dei mentori/metodi usati internamente e sui nomi di altri clienti.

(contributo di Andrea Chirivì, 2026-10-12)

## Altri deliverable al cliente
- **Deck da proiettare**: solo titolo e tabella. Si tolgono note esplicative, frasi a effetto e paragrafi di metodo sotto le tabelle — il racconto lo fa il consulente a voce. Unica eccezione: una riga pulita coi costi fissi d'azienda. Fonti, convenzioni e avvertenze restano nei file di lavoro, non nel deck. Prima di consegnare, una passata finale toglie ogni blocco di testo sotto le tabelle.
- **Fogli per lo staff**: una pagina sola, solo il gesto da fare (quale tasto, in che momento) in frasi corte all'imperativo. Fuori: spiegazioni/contesto, regole che valgono solo per noi, numeri e aneddoti di gestione, benefit del personale, frasi che mettono un reparto sopra l'altro. Stesso spirito già in uso in `analisi-reputazione-locale/relazione.md` (foglio A4 in cassa).

(contributo di Andrea Chirivì, 2026-10-12)

## Prima di consegnare
1. **Ogni numero si ricontrolla sulla fonte viva** (fatture, CRM, cassa), con un collaudo numerato e revisori scettici: errori tipici trovati così sono date di decorrenza sbagliate, conteggi errati, un "margine" che in realtà era un rapporto diverso e va ridefinito o tolto.
2. **Definizioni esplicite**: scrivi cosa intendi per "ritorno", "NPS", "coupon" ecc. — non lasciarle implicite.
3. **Frasi dette a voce dai titolari tenute separate dai fatti documentati**: le etichette dei parlanti nelle trascrizioni (es. Fathom) sono inaffidabili, una frase si attribuisce solo dal contesto.
4. **Verifica a più lenti**: voce impersonale residua, proposte date per fatte, numeri incoerenti fra pagine, temi fiscali sfuggiti, pagine con buchi, soglie inventate. (Attenzione: "mancano date e costi" NON è un difetto da cercare nella relazione di piano — è l'opposto, date e costi sono un difetto lì, vedi sopra.)
5. **Grep sui mentori/metodi interni e sui nomi di altri clienti** prima di mandare.
6. **La relazione non parte finché il consulente non l'ha letta, e la manda lui**: mai invio automatico.

(contributo di Andrea Chirivì, 2026-10-12)

## Consegna
- Prima di mandare un link Drive, verifica che la mail del cliente sia un account Google: se non lo è, i link non si aprono e si manda il **PDF in allegato**.
- Usa il canale che il cliente usa davvero (es. WhatsApp quando le mail non partono o non vengono lette).
- Il documento lo manda sempre il consulente, dopo averlo letto: niente invii automatici.

(contributo di Andrea Chirivì, 2026-10-12)

## Struttura
```
rbr-report/
├── SKILL.md
├── assets/logo.png          ← logo RBR rosso su bianco (header)
└── scripts/
    ├── helpers.js           ← building block docx (richiede npm `docx`: `cd scripts && npm install docx`, una volta)
    └── inject.py            ← inietta header (logo) + footer (numero pagina) via python-docx
```

## Workflow in 3 passi

### 1. Scrivi lo script contenuto `<Cliente>_content.js`
```js
const path = require('path');
const SKILL = __dirname.includes('scripts') ? path.dirname(__dirname) : '<percorso di questa cartella skill>'; // punta alla cartella della skill (dove stanno assets/ e scripts/)
const { C, spacer, redLine, sectionLabel, subheading, body, bullet, callout,
        cell, headerRow, buildTable, titleBlock, signature, buildDocument
      } = require(path.join(SKILL, 'scripts', 'helpers.js'));

buildDocument([
  ...titleBlock('Nome Ristorante', 'Tipo Relazione', 'Mese Anno'),
  ...sectionLabel(1, 'Presentazione'),
  body('Testo...'),
  buildTable([1500, 3000, 3700], [
    headerRow(['Mese','Ricavi','Note'], [1500,3000,3700]),
    new TableRow({ children: [
      cell('Gennaio', { width: 1500 }),
      cell('€ 28.400', { width: 3000, bold: true }),
      cell('−4%', { width: 3700, color: C.RED, bold: true }),
    ]}),
  ]),
  ...signature('<Nome del consulente che firma>'), // mai un nome fisso — vedi Regole di scrittura
], '/percorso/output_base.docx');
```
`TableRow`, `TableCell`, `Paragraph`, `TextRun` sono globali (esposti da helpers.js) → si usano senza import.

### 2. Esegui
```bash
node /percorso/<Cliente>_content.js
```
`require('docx')` risolve dal `node_modules` in `scripts/` della skill — se manca, esegui prima `npm install docx` dentro `scripts/` (una volta sola).

### 3. Inietta header/footer RBR
```bash
python3 <cartella-skill>/scripts/inject.py \
  output_base.docx  Relazione_<Cliente>.docx  "Tipo Relazione – Ristorante – Referente"
```

## API helpers.js
| Funzione | Parametri | Output |
|---|---|---|
| `spacer(twips=160)` | | paragrafo vuoto |
| `redLine()` | — | filetto rosso |
| `sectionLabel(n, testo)` | numero, stringa | `[spacer, titolo, redLine, spacer]` |
| `subheading(testo)` | stringa | titoletto navy bold |
| `actionLabel(n, titolo)` | numero, stringa | "Azione N — Titolo" |
| `body(testo, opts)` | `{bold,color,align,after,italic,size}` | paragrafo testo |
| `bullet(testo, opts)` | `{bold,color}` | bullet • rosso |
| `callout(testo)` | stringa | box grigio corsivo |
| `cell(testo, opts)` | `{width,bold,color,bg,align,size,noBorder}` | TableCell |
| `headerRow(labels, widths)` | array, array | riga header rossa, testo bianco |
| `buildTable(widths, rows)` | array twips, array TableRow | Table |
| `titleBlock(nome, sottotitolo, data)` | stringhe | blocco titolo centrato |
| `signature(nome)` | nome obbligatorio, nessun default — il consulente che presenta il documento | blocco firma a destra |
| `buildDocument(children, outputPath)` | array, path | scrive .docx (Promise) |

Colori `C`: `RED e30613` (negativi/sezioni) · `ACCENT 1F4D78` (navy) · `BLACK 333333` · `LIGHT 666666` · `WHITE` · `GREY F5F5F5` (callout).
Larghezze colonne in twips, somma ≈ ≤ 8500 (margini pagina A4 1700 twips lato).

## Stile e ambito
Lo stile RBR (regole di scrittura, colori, struttura) vale per **ogni documento al cliente**: relazione di piano, relazione di call, report, checklist. Fa eccezione solo la carta/menu, che usa colori e font del locale (vedi `carta-menu-rbr`).

## Note ambiente (Mac di Marco)
- `docx` installato in `scripts/node_modules`.
- Anteprima PDF: **LibreOffice non installato** → per vedere il risultato aprire il .docx in Pages/Word, oppure convertire con lo strumento disponibile.
- Uscita in PDF: sorgente HTML in stile RBR + PDF da **Chrome headless** — WeasyPrint può non funzionare su alcuni Mac (manca `libgobject`). Il motore PDF RBR (`rbr_relazione.py`) è citato anche in `analisi-venduto-fasce`.

## Fonti/contributi
(contributo di Andrea Chirivì, 2026-10-12; tipo "relazione una tantum" — origine: Roberto Falcon)
