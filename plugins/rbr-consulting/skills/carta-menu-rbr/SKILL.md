---
name: carta-menu-rbr
description: >-
  Disegna la carta ingegnerizzata di un ristorante come artifact Claude interattivo con doppia vista
  (Vista cliente = il menu come lo legge chi si siede; Vista consulente = margini, food cost, posizione in
  classifica, classe Kasavana-Smith e €/anno di ogni leva) e poi ne tira fuori il PDF di stampa
  (soffietto a 3 ante e mezza o libro A4). Metodo nato sulle carte Giurges e Antipapa (Fondi, set 2026).
  Usala quando il consulente dice "fammi il menu ingegnerizzato di X", "ridisegna la carta", "fammi il menu
  come quello di Antipapa/Giurges", "menu a tre ante", "menu a libro", "voglio vedere i margini sul menu",
  "fammi il PDF del menu". Parte SEMPRE dopo la classificazione della skill menu-engineering.
---

# Carta menu RBR (artifact a doppia vista → PDF di stampa)

## Perché esiste
Il consulente deve far vedere al ristoratore **la carta nuova e perché rende di più** nello stesso
oggetto. L'artifact con il pulsante *Vista cliente / Vista consulente* fa entrambe le cose: in call si
mostra il menu pulito, poi si clicca e compaiono sotto ogni piatto margine, food cost, pezzi venduti e
le note verdi con i €/anno di ogni leva. Quando il cliente approva, lo stesso HTML diventa il PDF per
la tipografia. Esempi veri in `esempi/` (aprili come riferimento di struttura e CSS, non copiarli a occhi chiusi):
- `soffietto_giurges.html` — pub/brace, soffietto 3 ante + mezza, fronte e retro
- `libro_antipapa.html` — trattoria, libro A4 a facciate

## Prerequisiti (senza questi non si parte)
1. **Classificazione fatta** con la skill `menu-engineering` (Kasavana-Smith per categoria): margine
   €, FC %, pezzi venduti nel periodo, classe STAR/PLOWHORSE/PUZZLE/DOG. Fonte food cost: file 02 del
   cliente (costi materie prime **IVA esclusa**, prezzi di vendita ÷1,1).
2. **Venduto reale** dal gestionale (iPratico → skill `estrai-dati-ipratico`; CEI Smart Manager →
   Statistiche → Advanced → Plu). Serve anche per scovare i piatti venduti **fuori carta** e le
   combinazioni (es. "doppio" battuto 5 volte in 8 mesi = riga che vale zero perché non è scritta).
3. **Menu attuale del cliente** in PDF (font, colori, logo, nomi piatti e descrizioni ufficiali) e
   carta dei vini / birre se c'è: palette e font si prendono da lì.
4. **Formato deciso con Marco/consulente** prima di disegnare (vedi sotto). Non cambiarlo mai di testa tua.
   Chiedi sempre le **misure reali** della cartella e della copertina al cliente, non dare per scontato
   A4 (es. pagine 23,5×29,7 cm, copertina che regge 25×32, piega con viti a 3 cm → fascia della piega
   libera da contenuti, area utile ridotta). Le tavole si rifanno una volta sola, dopo le decisioni di
   contenuto. Se c'è un QR in carta, porta alla pagina del sito coi menu in più lingue (e quello SG) **in
   aggiunta** alla carta stampata, mai al posto suo.

## Formati
| Formato | Quando | Struttura (NON cambiare le posizioni una volta approvate) |
|---|---|---|
| **Soffietto 3 ante e mezza** (366×297 mm, ante 100+100+100+66) | pub, brace, panini, locale informale | Fronte: anta 1 antipasti + insalate + contorni · anta 2 *premium in alto* (colore diverso) + panini + riquadro misure · anta 3 griglia (prodotto-foto, prodotto-foto) + spina + vini · mezza anta i menù componibili. Retro: copertina, manifesto, info, dolci + amari |
| **Libro A4** (210×297 per facciata) | trattoria, ristorante con percorso degustazione | Copertina → apri: sinistra antipasti, destra l'**Experience** → apri: sinistra paste premium in alto / formati / paste normali sotto, destra secondi premium in alto / secondi normali sotto → dietro dolci, amari, bevande, servizio + allergeni |

### Experience (pagina dedicata in carta)
Pagina piena nel colore del locale, prima cosa all'apertura (pagine 2-3): titolo "Experience …",
prezzo grande a persona, una riga su cosa è incluso, portate numerate I-II-III con scelta dalla carta,
foto sotto. Niente minimo di persone, a meno che non ci sia davvero una portata da dividere. Si riusa
solo il format (struttura, numerazione), mai prodotti, prezzi o nomi presi da un altro cliente.
L'esempio `esempi/libro_antipapa.html` (righe 264-276, 5 portate scelte da noi, "si ordina per tutto
il tavolo") mostra il vecchio percorso degustazione, non l'Experience: non copiarlo come modello attuale.
(contributo di Andrea Chirivì, 12/10/2026 — formato nato su casi 7 Ponti e Noolas)

## Regole di ingegnerizzazione (decise da Marco, valgono per ogni carta)
- **Massimo 7 voci per categoria.** Prima di disegnare elenca le categorie che sforano e cosa esce.
- **Ordine per margine con il n.1 in SECONDA posizione** (dove l'occhio si ferma per primo), poi a
  scendere. Il posto in classifica compare solo in vista consulente (`.rank`).
- **Si decide sulla matrice, non a gusto**: i DOG escono, i PUZZLE si spingono (es. la tartare di
  Giurges resta e sale di prezzo anche se vende poco, perché ha margine alto). Mai togliere un piatto
  ad alto margine senza guardare la matrice.
- **Tre modi di evidenziare**, massimo uno per tipo per categoria: `.pieno` (riquadro tutto colorato,
  angoli arrotondati) · `.bordo` (solo contorno) · `.spicca`/`.asta` (asticella a sinistra). Niente
  riquadri enormi. **Il riquadro va al piatto col margine in EURO più alto** della sua pagina/gruppo,
  mai a chi ha il FC % più basso né alla "star" di una categoria a margini bassi: prima di consegnare,
  per ogni pagina metti in fila i margini € e controlla che i riquadri stiano sui primi. **Niente
  riquadri o pagine a fondo nero** (illeggibili): pieno nel colore del locale, mai un blocco scuro con
  più voci dentro — una sola voce per riquadro pieno, le altre restano sulla carta chiara.
- **Categoria premium** (3 voci, prezzo alto, colore diverso, in alto): fa ancoraggio — dopo 24 € un
  piatto da 14,50 sembra il prezzo giusto. Premium con la foto accanto.
- **Costo variabile senza prezzo fisso**: Fiorentina senza prezzo ("chiedi al personale i tagli
  disponibili") o all'etto, funghi/tartufo "prezzo del giorno". Un ingrediente premium caro o
  incostante si toglie dalla carta o va a prezzo del giorno. Se il peso è scritto, deve coincidere con
  quello che esce davvero: verificarlo prima della stampa.
- **Doppione economico: si tiene solo la versione che rende.** Se lo stesso piatto esiste in due
  versioni (es. "base" a 6€ e "nostra" a 11€), l'economica diventa il prezzo più basso della carta,
  attira il cliente sbagliato e lascia metà margine: via.
- **Formati/misure** dove la materia prima costa poco: pasta Classica 100 g inclusa · Rafforzata
  150 g +6 · Padellone 220 g +12 (con icone piatto / piatto grande / padella); panini M inclusa · L +5
  · XL +9 + chip delle aggiunte. Il riquadro formati va PRIMA della sezione a cui si applica.
- **Abbinamento su ogni piatto**: vino (icona calice colorata per tipo) o birra (icona boccale colorata:
  bianca, chiara, ambrata, rossa, scura). Senza scritta "in abbinamento".
- **Menù componibili / percorso**: servono a far arrivare dolce e vino al tavolo, non a scontare.
  Percorso degustazione solo con piatti già in carta (zero referenze nuove in cucina). **Questa regola
  vale per tutta la carta**, non solo per i percorsi: ogni voce nuova nasce da ingredienti già comprati
  e basi già prodotte (es. padellino sulla pasta della pizza, bruschetta sul pane del mattino). Le
  grammature si prendono dalla ricetta che il locale usa già, non si ipotizzano, e si provano in cucina
  prima della stampa.
- **Niente offerte in carta**: formule promo, combo scontate, 2x1, aperitivi a prezzo speciale, promo
  settimanali non ci stanno — la carta vende a prezzo pieno, le offerte vivono in front end/campagne/CRM
  (`campagna-locale`). Restano i prezzi a persona e i menu fissi del pranzo (struttura di prezzo, non
  offerta). Le bevande non entrano mai nel prezzo dei piatti: il calice è un abbinamento consigliato,
  non un incluso. Le sezioni che occupano spazio senza margine (es. "per cominciare" di focaccia/olive
  senza marginalità) escono dalla carta.
- **Servizio e coperto esplicito, al prezzo ATTUALE.** Cambiare il prezzo di un piatto è
  ingegnerizzazione; **aumentare il coperto è una scelta di posizionamento** che il titolare decide a
  voce col consulente — mai scriverla in carta, brief al grafico o messaggi prima della decisione; resta
  nelle note interne come "da discutere" e il totale delle leve si presenta senza. Mai scrivere cosa
  comprende il coperto (focaccia, pane) senza conferma del cliente. Controllare sempre che la cassa batta
  davvero il coperto (capita che non sia battuto 1 volta su 3). Dolci e amari con sezione propria
  (l'amaro al 4-6% di penetrazione è la leva più sottovalutata).
- **Piatti da condividere (pentolaccia, taglieri, tagliata): sempre prezzo a persona** ("per 2", "per 4"
  — in cucina "per 4" = 4 porzioni), in una sezione "Da condividere". La pentola/tagliere arriva grande,
  il cameriere impiatta e lo lascia al centro; le versioni mini non si scrivono in carta. In carta
  nessuna regola su chi divide (la gestisce la sala); in cassa tasti per numero di persone; il prezzo a
  persona si ricalcola sul food cost della ricetta. Scrivere "a persona" solo quando è vero sia in
  cassa sia in cucina — un piatto da dividere preso in due a prezzo intero distrugge il margine.
- Ogni leva in vista consulente ha la sua nota verde con **€/anno** calcolati sul venduto reale
  (ipotesi di adozione dichiarata: "bastano 8 clienti su 100"). A fine lavoro, riepilogo del potenziale
  totale. **Ogni leva ha anche il numero che la giudica e la data del controllo** (es. contorno incluso
  nei secondi → scontrino medio del pranzo dopo 3 settimane; prodotto sostituito → quanto vende in un
  mese; Experience → food cost reale dopo ~4 settimane): le voci incerte restano fuori dal totale finché
  la conta non le giustifica. Nel totale, il margine delle voci **tolte** dalla carta si sottrae per
  intero (stima prudente, come se quei clienti non ordinassero altro) e va dichiarato come tale.

(contributo di Andrea Chirivì, 12/10/2026)

## Regole di design (feedback di Marco, non ridiscuterle)
- **Sfondo bianco/carta chiaro** nelle pagine di lettura (lo scuro solo su copertina, premium, menù).
- **Prezzi piccoli, dentro la descrizione** (`descrizione · 14,50`), mai in colonna, mai in evidenza.
- Tutti i titoli e le categorie **dritti** (niente testo ruotato). Niente descrizioni di categoria
  lunghe o "spiritose" invadenti; i nomi goliardici solo dove li ha il cliente.
- Font e palette presi dal menu attuale del cliente (Giurges: Bowlby One + Oswald, arancio/verde;
  Antipapa: Oswald + Archivo, vino/rosa/panna). Riempi la pagina: niente vuoti, niente riquadri giganti.
- Foto: riquadri segnaposto `FOTO` con icona, pochi e piccoli (prodotto-foto, prodotto-foto), finché il
  cliente non manda le foto vere. Lascia **sempre** lo spazio foto (col segnaposto che dice cosa
  fotografare) sulle voci in evidenza e sulle Experience anche nelle bozze, sui piatti che più meritano
  lo scatto (piatto d'immagine, piatto/pizza a margine più alto). Una foto sta **solo** accanto al piatto
  che ritrae — mai una foto generica accanto a un piatto diverso — e si scartano foto di piatti fuori
  carta o ambigue. Se il menu attuale è solo un PDF appiattito, le foto si recuperano a riquadri di
  coordinate sulla JPEG a piena risoluzione, ritagliando col fattore larghezza originale/larghezza render.
- Allergeni con i numeri a fianco del nome (legenda in fondo, **ordine Reg. UE 1169/2011**: 1 glutine ·
  2 crostacei · 3 uova · 4 pesce · 5 arachidi · 6 soia · 7 latte · 8 frutta a guscio · 9 sedano ·
  10 senape · 11 sesamo · 12 anidride solforosa · 13 lupini · 14 molluschi) + dicitura HACCP
  abbattimento. Asterisco "prodotto surgelato/abbattuto" in fondo alla descrizione dei piatti con
  prodotto congelato, con piede che lo spiega: verificarlo prima di promettere "pesce fresco" in copy o
  claim, perché la carta non deve smentirsi da sola. Prodotti venduti a peso: prezzo al kg o all'etto.
- **Senza glutine e AIC**: mai scrivere "certificati AIC" (la certificazione non esiste, è vietato
  presentarsi così). Dicitura corretta: "Aderiamo al programma Alimentazione Fuori Casa di AiC" (i
  minuscola, logo AFC ufficiale) — richiede il numero di attestato del locale, da chiedere prima di
  stampare. Niente bollini SG sui singoli piatti in carta principale (il cliente salterebbe la
  procedura in cucina): in carta solo "chiedete il nostro menu senza glutine", con un menu SG dedicato
  a prezzi già comprensivi dell'eventuale supplemento (verificato sul food cost delle versioni SG).
  Vedi anche `google-business-ristorante/SKILL.md` e `agenti-vocali-deepagent/SKILL.md` per le stesse
  regole lato Google Business e bot vocale.

(contributo di Andrea Chirivì, 12/10/2026)

## Procedura
1. Prepara la tabella piatti per categoria (nome, descrizione ufficiale, prezzo attuale → nuovo,
   margine, FC, pezzi, classe). Proposte di prezzo **sempre partendo dal prezzo attuale** (regola
   "prezzo attuale prima di proporre": si parte dal prezzo più battuto in cassa a quantità 1, mai un
   prezzo in carta sotto quello di cassa): aumenti piccoli (+0,50/+1) sui PLOWHORSE più venduti.
   Questo vale per i piatti **già in carta**: le voci nuove nascono da ingredienti/basi già in casa
   (vedi "Regole di ingegnerizzazione"), non si copia il prezzo di un piatto esistente.
   Se il menu attuale è un PDF impaginato da terzi senza il file sorgente (.indd/.ai), non si ricompone:
   si tolgono solo pagine intere oppure si rifà la carta da zero in HTML.
2. Mostra a Marco in un messaggio: categorie oltre 7 voci e chi esce, premium proposti, formati, leve con €/anno.
3. Scrivi l'HTML partendo dall'esempio del formato giusto. Struttura da mantenere perché lo script PDF
   la riconosce: `.bar` con i due bottoni + `.piano`; soffietto → `.blocco > .menu > section.anta`
   (`.mezza` per la mezza anta); libro → `.spread > .doppia > section.pag`; piatto →
   `.p > .nome/.riga, .desc (con .prezzo), .vin/.birra, .mk`; note → `p.nota`. Icone come `<symbol>` +
   `<use href>`.
4. Carica il skill `artifact-design`, pubblica con Artifact (una sola URL, ridistribuisci sullo stesso
   file a ogni giro). Verifica entrambe le viste.
5. Iterazioni con Marco: cambia SOLO quello che chiede, non rimescolare le posizioni già approvate.
6. **Ambiente.** Il WeasyPrint di sistema su Mac senza Homebrew non parte
   (`cannot load library 'libgobject-2.0-0'`). Senza sudo: ambiente conda-forge in home (micromamba:
   python 3.12, pango, ghostscript, poppler, qpdf + `pip weasyprint>=70`, pikepdf, numpy, pillow) e lancia
   `pdf_menu.py` con QUEL python, mai `python3` di sistema. Gli errori "Fontconfig error: ambiguous
   constant name" sono rumore, ignorali. Ripiego se l'ambiente non si riesce a montare: Chrome headless
   (`--headless --no-pdf-header-footer --print-to-pdf`) con un `@media print` che nasconde
   `.bar`/`.mk`/`.nota`/`.rank` e mette ogni `.pag` su una A4 — resta un ripiego, non la via principale.
7. PDF di stampa (vista cliente, senza note):
   ```
   python3 scripts/pdf_menu.py soffietto carta.html Menu_<Cliente>_<anno>.pdf --extra-css esempi/stampa_soffietto.css
   python3 scripts/pdf_menu.py libro     carta.html Menu_<Cliente>_<anno>.pdf
   ```
   Lo script dice `OK … N pagine` o `⚠️ ATTESE`. Sul libro compatta da solo se una facciata sfora, **ma
   non riempie**: su una carta corta (poche voci per categoria) le A4 escono vuote. In quel caso alza a
   mano la scala nel CSS extra (es. nomi 14→17 pt, descrizioni 9→10,2 pt, gap 4,2→7 mm) e rilancia.
   Sul soffietto le ante tagliano quello che sfora (non vanno a pagina nuova): **guarda sempre il PNG**
   di ogni facciata, libro compreso (`pdftoppm -r 40 -png out.pdf prova`), prima di consegnare e, se
   serve, riduci la scala nel CSS extra.
8. Controllo legale: checklist di `menu-engineering/references/normativa-menu.md` (allergeni, asterisco
   congelati sui singoli piatti, coperto vietato nel Lazio, DOP/provenienze documentate, QR mai da solo).
9. **Consegna**: link artifact (per la call) + PDF (per il grafico/tipografia) + riepilogo €/anno. Una
   decisione di prezzo **non è fatta finché non è in cassa**: dopo ogni carta nuova rileggi il listino
   del POS voce per voce (ogni voce nuova — formati, aggiunte, Experience, piatti a persona — va creata
   in cassa prima della stampa). Se l'impaginazione la fa un grafico esterno, l'HTML/PDF di RBR resta
   una bozza di struttura: manda un brief con ordine delle voci, prezzi dentro la descrizione senza €,
   max 2 evidenze per facciata, coperto scritto in chiaro al prezzo attuale (niente margini né food cost
   nel brief), più un pacchetto con bozza, marchio in PNG chiaro/scuro, menu attuale, foto e cosa
   cambierà ancora (prodotti, prezzi, etichette vini).

(contributo di Andrea Chirivì, 12/10/2026)

## Trappole di stampa (già pagate)
- Il **flex orizzontale** per affiancare ante/pagine le impila → ante a coordinate assolute (lo fa lo script).
- I **flex verticali** con `gap` sballano → blocchi + margini (lo fa lo script).
- Il bordo **dashed** manda in overflow il calcolo del tratteggio e blocca il render → diventa `dotted` o `solid`.
- `<use href="#id">` non viene risolto → lo script inlinea i `<symbol>`.
- Stesso formato di pagina su tutte le facciate: mai una pagina più lunga delle altre.
- `@media (max-width:900px)` **scatta anche in stampa** (210 mm ≈ 794 px a 96 dpi) e il PDF esce col
  layout da telefono: usa sempre `@media screen and (max-width:…)`.
- `padding-inline`/`gap` sui contenitori pensati per lo schermo spostano le facciate di qualche mm e
  l'abbondanza resta bianca su un lato: azzerali in stampa e controlla che ogni facciata parta dall'angolo.
- In WeasyPrint `margin-top:auto` dentro un flex verticale non spinge giù il numero di pagina: va
  sistemato via CSS di ritocco (`--extra-css`).
- Nei mockup con container query il padding in `cqw` messo sul contenitore si calcola sulla viewport:
  mettilo su un figlio interno.

## Riferimenti (casi Mastermind ed elementi di carta)
- **Trattoria (Firenze)**: da pannello di 41 voci a pieghevole di 4-8 voci → +11,5 € di coperto medio.
- **Pizzeria (Villanova d'Asti)**: mix pizza spostato dal 75% al 50% sul totale venduto.
- Elementi utili da valutare in carta, se pertinenti al cliente: bollini tipo "Best seller" solo se
  veri (dati reali, non decorazione); icona tartufo + riquadro dedicato ("Un'esperienza al tartufo +X");
  riquadro aggiunte a costo minimo ("Rendilo unico/tuo +X": stracciatella, pancetta, rucola...); pagina
  "La nostra storia"; produttori veri in copertina presi dalle fatture; prodotti premium all'etto (carne,
  pescato del giorno) con un'illustrazione che educa il cliente.

(contributo di Roberto Falcon, Mastermind RBR settembre 2026, applicato da Andrea Chirivì — 12/10/2026)

## Collegamenti
`menu-engineering` (classificazione a monte) · `foodcost-cliente` (file 02) · `estrai-dati-ipratico` ·
`strategia-marketing-rbr` (tono dei testi) · `relazione-rbr` (relazione che accompagna la carta) ·
`market-discovery-ristorante` (pricing di zona, prima di ritoccare i menu fissi).
