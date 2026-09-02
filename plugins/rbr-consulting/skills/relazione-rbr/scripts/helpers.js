/**
 * RBR Report — building block riutilizzabili per relazioni .docx brandizzate RBR.
 * Ricostruito dalla guida rbr-report-guida.md. Richiede il pacchetto `docx`.
 *
 * Espone le funzioni via module.exports E mette a disposizione come GLOBAL
 * (TableRow, TableCell, Paragraph, TextRun) così gli script contenuto possono
 * usare `new TableRow({...})` senza import espliciti, come da guida.
 */
const fs = require('fs');
const {
  Document, Packer, Paragraph, TextRun, AlignmentType,
  Table, TableRow, TableCell, WidthType, BorderStyle, ShadingType,
  TabStopType, TabStopPosition, HeadingLevel, PageNumber,
} = require('docx');

// ---- Palette RBR ----------------------------------------------------------
const C = {
  RED:    'E30613', // numeri negativi, sezioni, header tabella
  ACCENT: '1F4D78', // navy, subheading
  BLACK:  '333333', // testo corpo
  LIGHT:  '666666', // testo secondario
  WHITE:  'FFFFFF',
  GREY:   'F5F5F5', // sfondo callout
};

const FONT = 'Calibri';
const NO_BORDER = { style: BorderStyle.NONE, size: 0, color: 'FFFFFF' };

// ---- Primitive ------------------------------------------------------------
function spacer(twips = 160) {
  return new Paragraph({ spacing: { before: 0, after: 0, line: twips } , children: [new TextRun('')] });
}

function redLine() {
  // Filetto rosso sottile: paragrafo con bordo inferiore rosso.
  return new Paragraph({
    spacing: { before: 20, after: 20 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 15, color: C.RED, space: 1 } },
    children: [new TextRun('')],
  });
}

function sectionLabel(n, testo) {
  const title = new Paragraph({
    spacing: { before: 40, after: 40 },
    children: [
      new TextRun({ text: `${n}. `, bold: true, color: C.RED, font: FONT, size: 26 }),
      new TextRun({ text: testo, bold: true, color: C.BLACK, font: FONT, size: 26 }),
    ],
  });
  return [spacer(120), title, redLine(), spacer(80)];
}

function subheading(testo) {
  return new Paragraph({
    spacing: { before: 120, after: 60 },
    children: [new TextRun({ text: testo, bold: true, color: C.ACCENT, font: FONT, size: 23 })],
  });
}

function actionLabel(n, titolo) {
  return new Paragraph({
    spacing: { before: 100, after: 40 },
    children: [
      new TextRun({ text: `Azione ${n} — `, bold: true, color: C.RED, font: FONT, size: 22 }),
      new TextRun({ text: titolo, bold: true, color: C.BLACK, font: FONT, size: 22 }),
    ],
  });
}

function body(testo, opts = {}) {
  const { bold = false, color = C.BLACK, align, after = 120, italic = false, size = 21 } = opts;
  const alignment = align === 'center' ? AlignmentType.CENTER
    : align === 'right' ? AlignmentType.RIGHT
    : align === 'justify' ? AlignmentType.JUSTIFIED
    : AlignmentType.LEFT;
  return new Paragraph({
    alignment,
    spacing: { after, line: 276 },
    children: [new TextRun({ text: testo, bold, italics: italic, color, font: FONT, size })],
  });
}

function bullet(testo, opts = {}) {
  const { bold = false, color = C.BLACK } = opts;
  return new Paragraph({
    spacing: { after: 60, line: 264 },
    indent: { left: 260, hanging: 180 },
    children: [
      new TextRun({ text: '•  ', bold: true, color: C.RED, font: FONT, size: 21 }),
      new TextRun({ text: testo, bold, color, font: FONT, size: 21 }),
    ],
  });
}

function callout(testo) {
  return new Table({
    width: { size: 100, type: WidthType.PERCENTAGE },
    borders: {
      top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER,
      insideHorizontal: NO_BORDER, insideVertical: NO_BORDER,
    },
    rows: [new TableRow({
      children: [new TableCell({
        shading: { type: ShadingType.CLEAR, fill: C.GREY, color: 'auto' },
        margins: { top: 120, bottom: 120, left: 160, right: 160 },
        children: [new Paragraph({
          children: [new TextRun({ text: testo, italics: true, color: C.BLACK, font: FONT, size: 21 })],
        })],
      })],
    })],
  });
}

// ---- Tabelle --------------------------------------------------------------
function cell(testo, opts = {}) {
  const { width, bold = false, color = C.BLACK, bg, align = 'left', size = 20, noBorder = false } = opts;
  const alignment = align === 'center' ? AlignmentType.CENTER
    : align === 'right' ? AlignmentType.RIGHT
    : AlignmentType.LEFT;
  const cellOpts = {
    margins: { top: 60, bottom: 60, left: 100, right: 100 },
    verticalAlign: 'center',
    children: [new Paragraph({
      alignment,
      children: [new TextRun({ text: String(testo), bold, color, font: FONT, size })],
    })],
  };
  if (width) cellOpts.width = { size: width, type: WidthType.DXA };
  if (bg) cellOpts.shading = { type: ShadingType.CLEAR, fill: bg, color: 'auto' };
  if (noBorder) cellOpts.borders = {
    top: NO_BORDER, bottom: NO_BORDER, left: NO_BORDER, right: NO_BORDER,
  };
  return new TableCell(cellOpts);
}

function headerRow(labels, widths) {
  return new TableRow({
    tableHeader: true,
    children: labels.map((l, i) => cell(l, {
      width: widths[i], bold: true, color: C.WHITE, bg: C.RED,
      align: i === 0 ? 'left' : 'center', size: 20,
    })),
  });
}

function buildTable(widths, rows) {
  const total = widths.reduce((a, b) => a + b, 0);
  const grey = 'D9D9D9';
  return new Table({
    width: { size: total, type: WidthType.DXA },
    columnWidths: widths,
    borders: {
      top:    { style: BorderStyle.SINGLE, size: 4, color: grey },
      bottom: { style: BorderStyle.SINGLE, size: 4, color: grey },
      left:   { style: BorderStyle.SINGLE, size: 4, color: grey },
      right:  { style: BorderStyle.SINGLE, size: 4, color: grey },
      insideHorizontal: { style: BorderStyle.SINGLE, size: 4, color: grey },
      insideVertical:   { style: BorderStyle.SINGLE, size: 4, color: grey },
    },
    rows,
  });
}

// ---- Blocchi di alto livello ---------------------------------------------
function titleBlock(nome, sottotitolo, data) {
  return [
    spacer(240),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
      children: [new TextRun({ text: nome, bold: true, color: C.BLACK, font: FONT, size: 44 })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 40 },
      children: [new TextRun({ text: sottotitolo, bold: true, color: C.RED, font: FONT, size: 26 })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { after: 80 },
      children: [new TextRun({ text: data, color: C.LIGHT, font: FONT, size: 22 })],
    }),
    new Paragraph({
      alignment: AlignmentType.CENTER,
      border: { bottom: { style: BorderStyle.SINGLE, size: 18, color: C.RED, space: 1 } },
      children: [new TextRun('')],
    }),
    spacer(200),
  ];
}

function signature(nome = 'Leo Franco') {
  return [
    spacer(320),
    new Paragraph({
      alignment: AlignmentType.RIGHT,
      spacing: { after: 20 },
      children: [new TextRun({ text: 'Cordiali saluti,', italics: true, color: C.LIGHT, font: FONT, size: 21 })],
    }),
    new Paragraph({
      alignment: AlignmentType.RIGHT,
      spacing: { after: 0 },
      children: [new TextRun({ text: nome, bold: true, color: C.BLACK, font: FONT, size: 22 })],
    }),
    new Paragraph({
      alignment: AlignmentType.RIGHT,
      children: [new TextRun({ text: 'Restaurant Business Revolution', color: C.RED, font: FONT, size: 20 })],
    }),
  ];
}

// ---- Documento ------------------------------------------------------------
async function buildDocument(children, outputPath) {
  const doc = new Document({
    styles: {
      default: {
        document: { run: { font: FONT, size: 21, color: C.BLACK } },
      },
    },
    sections: [{
      properties: {
        page: {
          size: { width: 11906, height: 16838 }, // A4
          margin: { top: 1440, bottom: 1440, left: 1700, right: 1700 },
        },
      },
      children,
    }],
  });
  const buffer = await Packer.toBuffer(doc);
  fs.writeFileSync(outputPath, buffer);
  return outputPath;
}

// Esponi come global per gli script contenuto (uso di `new TableRow(...)` senza import)
global.TableRow = TableRow;
global.TableCell = TableCell;
global.Paragraph = Paragraph;
global.TextRun = TextRun;
global.AlignmentType = AlignmentType;
global.WidthType = WidthType;
global.ShadingType = ShadingType;
global.BorderStyle = BorderStyle;

module.exports = {
  C, FONT, spacer, redLine, sectionLabel, subheading, actionLabel, body, bullet,
  callout, cell, headerRow, buildTable, titleBlock, signature, buildDocument,
  // riesporto anche le classi docx utili
  Document, Packer, Paragraph, TextRun, AlignmentType, Table, TableRow, TableCell,
  WidthType, BorderStyle, ShadingType,
};
