# -*- coding: utf-8 -*-
"""
report_kit — impaginazione di una relazione reputazionale in PDF.

Serve a non riscrivere ogni volta trecento righe di boilerplate ReportLab.
Importi, componi il documento chiamando le funzioni nell'ordine in cui vuoi
che appaia, e chiudi con build().

    import sys; sys.path.insert(0, "<cartella della skill>")
    from report_kit import *

    doc = Report("~/Downloads/Analisi.pdf",
                 kicker="ANALISI RECENSIONI · 16 MAGGIO – 16 AGOSTO 2026",
                 titolo="Locale — Città",
                 sottotitolo="Punti forti, punti deboli e piano operativo",
                 footer="Locale · Analisi recensioni · agosto 2026")

    doc.kpi([("8,79", "media TheFork /10<br/>265 recensioni"),
             ("10,2%", "sotto il 7/10<br/>27 casi")])
    doc.panel("<b>La tesi in tre righe.</b> …")
    doc.h1("Dove siamo", "1")
    doc.p("…")
    doc.table([["Periodo", "N.", "Media"], ["Giugno", "66", "8,77"]], [40, 20, 20])
    doc.build()

Note pratiche
-------------
* Il markup ammesso nei testi è quello dei Paragraph di ReportLab:
  <b>, <i>, <br/>, <font color='#B3121D'>. Le entità HTML vanno scritte
  come &euro; &rarr; &mdash; &bull; e simili.
* Mai usare caratteri Unicode di apice/pedice (₀¹²): i font base non li
  hanno e ReportLab disegna quadrati neri. Usa <sub> e <super>.
* Le larghezze di colonna si passano in **millimetri**, come numeri semplici.
  La somma deve fare 161 (la larghezza utile della pagina A4 con questi margini).
* Non inserire interruzioni di pagina dentro una sezione: lascia fluire il testo
  e usa page_break() solo fra un capitolo e l'altro, altrimenti restano
  mezze pagine bianche.
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph,
                                Spacer, Table, TableStyle, KeepTogether,
                                HRFlowable, PageBreak)

__all__ = ["Report", "INK", "MUTED", "ACCENT", "GREEN", "BAND", "BLUE", "AMBER", "colors"]

# Palette. ACCENT è l'unico colore da cambiare per adattarla al brand del locale.
INK    = colors.HexColor("#1A1A1A")
MUTED  = colors.HexColor("#6B6B6B")
ACCENT = colors.HexColor("#B3121D")
GREEN  = colors.HexColor("#1F6F43")
RULE   = colors.HexColor("#DCDCDC")
BAND   = colors.HexColor("#F5F2EF")
BLUE   = colors.HexColor("#EEF3F8")
AMBER  = colors.HexColor("#FBF3E7")

PAGE_W = 161.0  # mm utili


def _s(name, **kw):
    base = dict(name=name, fontName="Helvetica", fontSize=9.6, leading=14.2,
                textColor=INK, alignment=TA_LEFT, spaceAfter=0)
    base.update(kw)
    return ParagraphStyle(**base)


class Report:
    def __init__(self, path, kicker="", titolo="", sottotitolo="", footer="",
                 accent=None, meta_title=None, meta_subject=None):
        self.path = path
        self.footer = footer
        self.accent = accent or ACCENT
        self.meta_title = meta_title or titolo
        self.meta_subject = meta_subject or sottotitolo
        self.story = []

        self.st_title  = _s("t",  fontName="Helvetica-Bold", fontSize=22, leading=26)
        self.st_sub    = _s("s",  fontSize=11.5, leading=15.5, textColor=MUTED)
        self.st_kicker = _s("k",  fontName="Helvetica-Bold", fontSize=8, leading=11,
                            textColor=self.accent)
        self.st_h1     = _s("h1", fontName="Helvetica-Bold", fontSize=14.5, leading=18)
        self.st_h2     = _s("h2", fontName="Helvetica-Bold", fontSize=11, leading=14.5)
        self.st_h3     = _s("h3", fontName="Helvetica-Bold", fontSize=9.8, leading=13.5,
                            textColor=self.accent)
        self.st_body   = _s("b",  spaceAfter=6)
        self.st_small  = _s("sm", fontSize=8.3, leading=11.6, textColor=MUTED)
        self.st_quote  = _s("q",  fontName="Helvetica-Oblique", fontSize=9.1, leading=13,
                            textColor=colors.HexColor("#3D3D3D"), leftIndent=8)
        self.st_th     = _s("th", fontName="Helvetica-Bold", fontSize=8.6, leading=11.5,
                            textColor=colors.white)
        self.st_td     = _s("td", fontSize=8.8, leading=12.4)
        self.st_num    = _s("n",  fontName="Helvetica-Bold", fontSize=18, leading=20,
                            textColor=self.accent, alignment=TA_CENTER)
        self.st_numlab = _s("nl", fontSize=7.5, leading=9.8, textColor=MUTED,
                            alignment=TA_CENTER)
        self.st_script = _s("sc", fontName="Helvetica-Bold", fontSize=9.6, leading=14,
                            textColor=colors.HexColor("#14402A"))

        if kicker or titolo:
            self._cover(kicker, titolo, sottotitolo)

    # ---------------------------------------------------------------- copertina
    def _cover(self, kicker, titolo, sottotitolo):
        a = self.story.append
        a(Spacer(1, 4))
        if kicker:
            a(Paragraph(kicker.upper(), self.st_kicker)); a(Spacer(1, 7))
        a(Paragraph(titolo, self.st_title)); a(Spacer(1, 3))
        if sottotitolo:
            a(Paragraph(sottotitolo, self.st_sub))
        a(Spacer(1, 8))
        a(HRFlowable(width="100%", thickness=2.4, color=self.accent))
        a(Spacer(1, 14))

    # ---------------------------------------------------------------- testo
    def h1(self, testo, numero=None):
        """Titolo di capitolo, con il numeretto rosso sopra."""
        blk = []
        if numero:
            blk += [Paragraph(str(numero).upper(), self.st_kicker), Spacer(1, 2)]
        blk += [Paragraph(testo, self.st_h1), Spacer(1, 3),
                HRFlowable(width="100%", thickness=1.1, color=self.accent, spaceAfter=8)]
        self.story.append(KeepTogether(blk))

    def h2(self, testo):
        self.story += [Spacer(1, 6), Paragraph(testo, self.st_h2), Spacer(1, 3)]

    def h3(self, testo):
        self.story += [Spacer(1, 4), Paragraph(testo, self.st_h3), Spacer(1, 2)]

    def p(self, testo, piccolo=False):
        self.story.append(Paragraph(testo, self.st_small if piccolo else self.st_body))

    def bullets(self, voci):
        for v in voci:
            self.story.append(Paragraph(
                "&bull;&nbsp;&nbsp;" + v,
                _s("li", leftIndent=11, firstLineIndent=-11, spaceAfter=4)))
        self.story.append(Spacer(1, 4))

    def spazio(self, h=8):
        self.story.append(Spacer(1, h))

    def page_break(self):
        self.story.append(PageBreak())

    # ---------------------------------------------------------------- blocchi
    def _boxed(self, testo, bg, bar, style):
        t = Table([[Paragraph(testo, style)]], colWidths=[PAGE_W * mm])
        t.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
            ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ("LINEBEFORE", (0, 0), (0, -1), 2.2, bar),
            ("BACKGROUND", (0, 0), (-1, -1), bg)]))
        self.story += [Spacer(1, 2), t, Spacer(1, 9)]

    def panel(self, testo, tono="info"):
        """Riquadro per una conclusione. tono: info | buono | attenzione."""
        t = {"info":       (BLUE,  colors.HexColor("#3F6E9E")),
             "buono":      (colors.HexColor("#EDF5EF"), GREEN),
             "attenzione": (AMBER, colors.HexColor("#C4881F"))}[tono]
        self._boxed(testo, t[0], t[1], _s("bx", fontSize=9.1, leading=13))

    def script(self, testo):
        """Frase da far dire allo staff, alla lettera."""
        self._boxed("&ldquo;" + testo + "&rdquo;",
                    colors.HexColor("#EDF5EF"), GREEN, self.st_script)

    def quote(self, testo, fonte=None):
        """Citazione testuale da una recensione. `fonte` = piattaforma, data, voto."""
        righe = [[Paragraph(testo, self.st_quote)]]
        if fonte:
            righe.append([Paragraph(fonte, self.st_small)])
        t = Table(righe, colWidths=[PAGE_W * mm])
        t.setStyle(TableStyle([
            ("LEFTPADDING", (0, 0), (-1, -1), 9), ("RIGHTPADDING", (0, 0), (-1, -1), 7),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBEFORE", (0, 0), (0, -1), 2.2, self.accent),
            ("BACKGROUND", (0, 0), (-1, -1), BAND)]))
        self.story += [Spacer(1, 2), t, Spacer(1, 7)]

    def table(self, righe, larghezze_mm, intestazione=True):
        """Prima riga = intestazione. Larghezze in mm, somma 161."""
        data = [[Paragraph(c, self.st_th if (intestazione and i == 0) else self.st_td)
                 for c in r] for i, r in enumerate(righe)]
        t = Table(data, colWidths=[w * mm for w in larghezze_mm],
                  repeatRows=1 if intestazione else 0)
        cmds = [("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("LINEBELOW", (0, 0), (-1, -2), 0.5, RULE)]
        if intestazione:
            cmds += [("BACKGROUND", (0, 0), (-1, 0), INK),
                     ("LINEBELOW", (0, 0), (-1, 0), 0, colors.white)]
            for r in range(2, len(righe), 2):
                cmds.append(("BACKGROUND", (0, r), (-1, r), colors.HexColor("#FAF8F7")))
        t.setStyle(TableStyle(cmds))
        self.story += [t, Spacer(1, 9)]

    def kpi(self, voci):
        """Fascia di numeroni. voci = [(valore, etichetta), …], da 2 a 5."""
        w = (PAGE_W / len(voci)) * mm
        celle = []
        for val, lab in voci:
            inner = Table([[Paragraph(val, self.st_num)],
                           [Paragraph(lab, self.st_numlab)]], colWidths=[w])
            inner.setStyle(TableStyle([("TOPPADDING", (0, 0), (-1, -1), 2),
                                       ("BOTTOMPADDING", (0, 0), (-1, -1), 2)]))
            celle.append(inner)
        t = Table([celle], colWidths=[w] * len(voci))
        t.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), BAND),
            ("TOPPADDING", (0, 0), (-1, -1), 9), ("BOTTOMPADDING", (0, 0), (-1, -1), 9),
            ("LINEAFTER", (0, 0), (-2, -1), 0.6, colors.HexColor("#E2DCD7")),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
        self.story += [t, Spacer(1, 11)]

    # ---------------------------------------------------------------- build
    def build(self):
        footer, muted, rule = self.footer, MUTED, RULE

        class _Doc(BaseDocTemplate):
            def afterPage(self):
                c = self.canv
                c.saveState()
                c.setStrokeColor(rule); c.setLineWidth(0.5)
                c.line(24 * mm, 16 * mm, 186 * mm, 16 * mm)
                c.setFont("Helvetica", 7.4); c.setFillColor(muted)
                c.drawString(24 * mm, 11.5 * mm, footer)
                c.drawRightString(186 * mm, 11.5 * mm, "Pag. %d" % c.getPageNumber())
                c.restoreState()

        doc = _Doc(self.path, pagesize=A4,
                   leftMargin=24 * mm, rightMargin=24 * mm,
                   topMargin=20 * mm, bottomMargin=22 * mm,
                   title=self.meta_title, subject=self.meta_subject,
                   author="Analisi reputazionale")
        doc.addPageTemplates([PageTemplate(
            id="main",
            frames=[Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")])])
        doc.build(self.story)
        return self.path
