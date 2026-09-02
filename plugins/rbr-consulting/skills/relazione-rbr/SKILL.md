---
name: relazione-rbr
description: Genera relazioni/report professionali .docx brandizzati RBR (Restaurant Business Revolution) — header col logo, filetti rossi, tabelle, callout, firma. Usala quando il consulente chiede un "report RBR", una "relazione" per un cliente ristoratore (CDG, food cost, ottimizzazione personale, analisi vendite, piano marketing) da consegnare in Word.
---

# RBR Report

Building block riutilizzabili per produrre relazioni Word brandizzate RBR con stile coerente (rosso `#E30613`, navy `#1F4D78`, header/footer, tabelle, callout, firma).

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
  ...signature('Restaurant Business Revolution'),
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
| `signature(nome)` | default "Leo Franco" | blocco firma a destra |
| `buildDocument(children, outputPath)` | array, path | scrive .docx (Promise) |

Colori `C`: `RED e30613` (negativi/sezioni) · `ACCENT 1F4D78` (navy) · `BLACK 333333` · `LIGHT 666666` · `WHITE` · `GREY F5F5F5` (callout).
Larghezze colonne in twips, somma ≈ ≤ 8500 (margini pagina A4 1700 twips lato).

## Note ambiente (Mac di Marco)
- `docx` installato in `scripts/node_modules`.
- Anteprima PDF: **LibreOffice non installato** → per vedere il risultato aprire il .docx in Pages/Word, oppure convertire con lo strumento disponibile.
