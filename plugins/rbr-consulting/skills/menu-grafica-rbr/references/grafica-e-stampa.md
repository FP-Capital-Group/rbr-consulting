# Grafica e stampa — specifiche usate davvero

## Formati approvati
| Formato | Misure | Struttura | Esempio |
|---|---|---|---|
| Libro A4 a facciate | 210×297, 8 facciate (2 A3 piegati) — sempre multiplo di 4 | 1 copertina · 2 antipasti (+insalate) · 3 Experience · 4 primi d'autore + formati + pasta · 5 grandi secondi + secondi + contorni · 6-7 pizze · 8 retro | Luna Blu, Antipapa, Tennis/Club |
| Libro bar A4 | 4 facciate, interne divise in 2 metà da 132 mm con filetto | copertina · caffè+pasticceria · bar · retro | Cartabianca bar |
| Carta pranzo A4 | 4 facciate, 1 colonna | copertina · pasta + insalate/freddi · **secondi a destra** (corpo più grande, `padding-top:30mm`) · per finire + allergeni + logo | Cartabianca pranzo bar |
| Soffietto 3 ante e mezza | 580×297 rifilato, ante 160+160+160+100 (formato vecchio Mister Pizza); versione piccola 366×297 (100+100+100+66) | fronte: antipasti · premium in alto + panini · griglia + spina + vini · mezza anta menù; retro speculare: dolci/amari · copertina | Giurgés |
| Carta dolci A5 | 148×210, amari e caffè sul retro | | Cartabianca |
| Allergeni A4 | tabella piatti × 14 allergeni | | Cartabianca, Giurgés |
| Cartello esterno | 1200×700 mm, 1 pagina | testata + griglia 6 colonne cucina/pizze | Luna Blu |
| Volantino | A4 | 8 voci numerate su 2 colonne | Brunch Panciatichi |
| Adesivi orari | A5 verticale, 1 pagina per sede | | Cartabianca |

**Il formato si decide con Marco prima di disegnare e non si cambia mai da soli.**

## Palette e font usati (riferimento, ma per un cliente nuovo si prendono dal SUO brand)
- **Luna Blu**: `--blu:#1E2A6E; --blu-2:#3B4C9B; --cielo:#9DBDE3; --ghiaccio:#EEF3FA; --carta:#FFFFFF;
  --linea:#D9DFEC; --testo:#1B2140; --soft:#5C6584; --fondo:#0E1431`. Font **Lora** (400-700 + corsivo)
  + **Jost** 400/500 per scritte di servizio (maiuscoletto spaziato). Bodoni Moda bocciato (poco leggibile).
- **Cartabianca bar (libro)**: `--fondo:#FFFDF9; --titolo:#4A2617; --nome:#8A5A2B; --testo:#4A3A2E;
  --soft:#8C7A6A; --linea:#E7DCCB; --crema:#F4EDE1; --punti:#A6192E`. Cormorant Garamond + EB Garamond.
  "Bellissimo, stile Eataly/Starbucks, font puliti, marroncino".
- **Cartabianca pranzo bar**: marrone #4A2617, rosso #A6192E, panna #F5EFE0, testo tenue #7A6A5E, prezzo
  #9C8C7E, separatore `|` #D6C8B4. DM Sans maiuscolo semibold (nomi 11,8pt) + Lora corsivo (titoli 27pt, desc 10,9pt).
- **Cartabianca ristoranti Tennis/Club**: stile Eataly bianco, solo Lora, nomi maiuscoli amaranto #8A1C2B,
  testo #4A3F38, pagina #FFFFFF; Experience su foto tavola con velo amaranto radiale (0,93 centro → 0,78 bordi).
- **Giurgés**: terracotta #CB6028, ruggine #A4441C, crema #F2E8DA, testo #3A2219; Bricolage Grotesque 800
  + Oswald + Caveat Brush. **Antipapa**: bordeaux #690F33, corallo #E63D2A, verde #08311F, lilla #8C83D0;
  Tilt Neon + Archivo.
- Vista consulente: `.mk{background:#D7E4F7;color:#132050}` · `.nota{background:#C7E5D2;color:#10241B}`.
- Icone abbinamento (`<symbol id="calice">`/`boccale` con `style="--w:..."`): vini bianco #E4D08A,
  bollicine #F2E7C4, rosso #7E1B33, rosso frizzante #A3324F; birre chiara #E8B93A, bianca #F3E3A0,
  non filtrata #D39A2E, rossa #A8401F, scura #4A2A18.

## Scala tipografica (libro A4 Luna Blu)
- Categoria `h2.cat` 25pt Lora 500 · nome `.nome` 11,5pt/600 · desc `.desc` 9pt lh 1,5 colore soft ·
  pagine pizze nome 8,4pt · pagina "ariosa" nome 14pt, desc 10,2pt, titolo 30pt · piede 6,4pt ·
  tag Jost 6,6pt maiuscolo .14em su blu raggio 999px.
- Spaziature uniformi: `.piatti>.p{margin-bottom:3.4mm}` `.sec{margin-bottom:6mm}`
  `h2.cat{margin-bottom:3.4mm}` `.pag{padding:16mm 15mm 22mm}`.
- Cartello 120×70: h2 50pt, nome 26,5pt, desc 18pt, tag 12,5pt, piede 13pt; testata blu 74 mm, nome 62pt,
  "Menù" corsivo 74pt; griglia `repeat(6,1fr)`, column-gap 24mm, lati 34mm, top 100mm bottom 30mm.
  Foto 46-52 mm (webp 900 px → ~440 ppi, ok).

## Snippet CSS chiave
```css
/* prezzo discreto in coda */
.prezzo{font-weight:400;color:inherit;font-size:.92em;white-space:nowrap}
.sep{margin:0 1mm;opacity:.7}
.pz{font-family:var(--tf);font-style:normal;font-weight:400;font-size:8.8pt;color:var(--soft)}
/* n.1 con cornice puntinata (bar) */
.r.uno{border:1pt dotted var(--punti);padding:1.25mm 2.6mm;margin:.4mm -2.6mm}
/* n.1 pranzo: riquadro + etichetta + foto a destra */
.p.bx{display:flex;align-items:center;gap:5mm;border:1pt dotted #A6192E;padding:3mm 4mm 3mm 4.4mm;margin-left:-4.4mm;margin-right:-4mm}
.et{font-weight:700;font-size:6.6pt;letter-spacing:.2em;text-transform:uppercase;color:#A6192E}
/* banda piena con foto che esce (Luna Blu) */
.p.pienobox{position:relative;width:150mm;padding:4.6mm 40mm 4.8mm 6mm;background:var(--blu)}
.p.pienobox .foto.img{position:absolute;right:-6mm;top:50%;margin-top:-17mm;width:34mm;height:34mm}
/* asticella alta solo quanto il testo */
.p.asta.pfoto > div:first-child{border-left:2.6pt solid var(--blu);padding-left:5mm}
/* cornice interna di pagina (bar) */
.pag::before{content:"";position:absolute;top:6mm;left:6mm;right:6mm;bottom:6mm;border:.5pt solid var(--linea)}
/* filigrana bozza */
.bozza{opacity:.07;transform:rotate(-28deg)}
```

## PDF
- **Carte (libro/soffietto)**: `python3 scripts/pdf_menu.py libro carta.html Out.pdf --extra-css stampa.css`.
  Lo script: toglie `.bar .nota .mk .rank` e script, `dashed→solid`, inlinea i `<symbol>`, flex verticali →
  blocchi, `.pag{height:297mm;overflow:hidden;page-break-after:always}`, compatta da solo (fino a 5 livelli
  −6%) se escono più pagine. Deve dire `OK … N pagine`. Sul soffietto le ante tagliano ciò che sfora:
  guarda SEMPRE il PNG.
- **Formati singoli (cartello)**: WeasyPrint diretto
  `python3 -c "import weasyprint;weasyprint.HTML('x.html',base_url='.').write_pdf('x.pdf')"`.
- **Chrome headless** quando serve `inset:` o colore esatto (adesivi):
  `"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --user-data-dir=/tmp/cprof --no-first-run --no-pdf-header-footer --virtual-time-budget=5000 --print-to-pdf=OUT file://…html`
  (Chrome non si chiude da solo: aspetta che la dimensione del file smetta di cambiare, poi termina).
- Controllo: `pdftoppm -r 40 -png Out.pdf prova` e guarda ogni pagina; `pdffonts Out.pdf` per verificare
  i font incorporati (Google Fonts scaricati da WeasyPrint → serve internet).

## Trappole WeasyPrint (già pagate)
- Flex orizzontale si impila → coordinate assolute o `display:table/table-cell` (3 colonne insalate).
- Flex verticale con `gap` sballa → blocchi + margini. `.piatti`/`.misure` vengono forzati a block:
  per 2 colonne usa `column-count`; "Scegli il tuo impasto" funziona solo con classe `flist misure`.
- Bordo `dashed` blocca il render → solid (usa `dotted`).
- `<use href>` non risolto → lo script inlinea. `var(--x)` dentro `<use>` ignorato → colori fissi in `simboli.svg`.
- Niente `inset:` → top/left/right/bottom.
- Nomi classe che collidono con lo script: `.bar` (è la barra dell'artifact → nelle carte bar usa
  `vr/vn/vd/sbar/pz`), `.portata` (rinominata `.tappa`).
- Specificità: `.pag:not(.copertina)` batte `.secondi`; per la sola pag. 2:
  `.pag[class='pag']:not(.copertina):not(.secondi)`.
- PDF uscito con 2 pagine in più → mettere inline `.abb` e compattare.

## Tipografia / stampa
- Abbondanza 3 mm + crocini: `scripts/stampa_abbondanza.py` (A4 → 216×303, estende il colore del bordo).
  Luna Blu carta e cartello sono ancora SENZA abbondanza: aggiungerla prima di mandarli.
- PDF in RGB e foto web a bassa risoluzione → prima della tipografia: CMYK + foto originali (≥300 ppi a misura).
- Fornitori usati: Pixartprinting (libro A4 punto metallico 8 fac. 300 g plastificato, 50 pz ≈ 91 €);
  soffietto 580×297 solo tipografo locale (200-300 €/50 pz). Copie Cartabianca bar: 240
  (Panciatichi e Ingromarket 50, Calenzano e Prato 40, gli altri 30).
- Grafico esterno (Army): brief a raffica con misure, cosa togliere, QR.

