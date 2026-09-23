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

## Formati
| Formato | Quando | Struttura (NON cambiare le posizioni una volta approvate) |
|---|---|---|
| **Soffietto 3 ante e mezza** (366×297 mm, ante 100+100+100+66) | pub, brace, panini, locale informale | Fronte: anta 1 antipasti + insalate + contorni · anta 2 *premium in alto* (colore diverso) + panini + riquadro misure · anta 3 griglia (prodotto-foto, prodotto-foto) + spina + vini · mezza anta i menù componibili. Retro: copertina, manifesto, info, dolci + amari |
| **Libro A4** (210×297 per facciata) | trattoria, ristorante con percorso degustazione | Copertina → apri: sinistra antipasti, destra il percorso → apri: sinistra paste premium in alto / formati / paste normali sotto, destra secondi premium in alto / secondi normali sotto → dietro dolci, amari, bevande, servizio + allergeni |

## Regole di ingegnerizzazione (decise da Marco, valgono per ogni carta)
- **Massimo 7 voci per categoria.** Prima di disegnare elenca le categorie che sforano e cosa esce.
- **Ordine per margine con il n.1 in SECONDA posizione** (dove l'occhio si ferma per primo), poi a
  scendere. Il posto in classifica compare solo in vista consulente (`.rank`).
- **Si decide sulla matrice, non a gusto**: i DOG escono, i PUZZLE si spingono (es. la tartare di
  Giurges resta e sale di prezzo anche se vende poco, perché ha margine alto). Mai togliere un piatto
  ad alto margine senza guardare la matrice.
- **Tre modi di evidenziare**, massimo uno per tipo per categoria: `.pieno` (riquadro tutto colorato,
  angoli arrotondati) · `.bordo` (solo contorno) · `.spicca`/`.asta` (asticella a sinistra). Niente
  riquadri enormi.
- **Categoria premium** (3 voci, prezzo alto, colore diverso, in alto): fa ancoraggio — dopo 24 € un
  piatto da 14,50 sembra il prezzo giusto. Premium con la foto accanto.
- **Formati/misure** dove la materia prima costa poco: pasta Classica 100 g inclusa · Rafforzata
  150 g +6 · Padellone 220 g +12 (con icone piatto / piatto grande / padella); panini M inclusa · L +5
  · XL +9 + chip delle aggiunte. Il riquadro formati va PRIMA della sezione a cui si applica.
- **Abbinamento su ogni piatto**: vino (icona calice colorata per tipo) o birra (icona boccale colorata:
  bianca, chiara, ambrata, rossa, scura). Senza scritta "in abbinamento".
- **Menù componibili / percorso**: servono a far arrivare dolce e vino al tavolo, non a scontare.
  Percorso degustazione solo con piatti già in carta (zero referenze nuove in cucina).
- **Servizio e coperto** esplicito (2,00–2,50 €), dolci e amari con sezione propria (l'amaro al 4-6% di
  penetrazione è la leva più sottovalutata).
- Piatti "per 2": in vista consulente mostra anche il margine **a persona**. I "metà" (es. metà 30 cm)
  di solito vanno tolti: spostano clienti da un piatto intero che rende di più.
- Ogni leva in vista consulente ha la sua nota verde con **€/anno** calcolati sul venduto reale
  (ipotesi di adozione dichiarata: "bastano 8 clienti su 100"). A fine lavoro, riepilogo del potenziale totale.

## Regole di design (feedback di Marco, non ridiscuterle)
- **Sfondo bianco/carta chiaro** nelle pagine di lettura (lo scuro solo su copertina, premium, menù).
- **Prezzi piccoli, dentro la descrizione** (`descrizione · 14,50`), mai in colonna, mai in evidenza.
- Tutti i titoli e le categorie **dritti** (niente testo ruotato). Niente descrizioni di categoria
  lunghe o "spiritose" invadenti; i nomi goliardici solo dove li ha il cliente.
- Font e palette presi dal menu attuale del cliente (Giurges: Bowlby One + Oswald, arancio/verde;
  Antipapa: Oswald + Archivo, vino/rosa/panna). Riempi la pagina: niente vuoti, niente riquadri giganti.
- Foto: riquadri segnaposto `FOTO` con icona, pochi e piccoli (prodotto-foto, prodotto-foto), finché il
  cliente non manda le foto vere.
- Allergeni con i numeri a fianco del nome (legenda in fondo) + dicitura HACCP abbattimento.

## Procedura
1. Prepara la tabella piatti per categoria (nome, descrizione ufficiale, prezzo attuale → nuovo,
   margine, FC, pezzi, classe). Proposte di prezzo **sempre partendo dal prezzo attuale** (vedi
   regola "prezzo attuale prima di proporre"): aumenti piccoli (+0,50/+1) sui PLOWHORSE più venduti.
2. Mostra a Marco in un messaggio: categorie oltre 7 voci e chi esce, premium proposti, formati, leve con €/anno.
3. Scrivi l'HTML partendo dall'esempio del formato giusto. Struttura da mantenere perché lo script PDF
   la riconosce: `.bar` con i due bottoni + `.piano`; soffietto → `.blocco > .menu > section.anta`
   (`.mezza` per la mezza anta); libro → `.spread > .doppia > section.pag`; piatto →
   `.p > .nome/.riga, .desc (con .prezzo), .vin/.birra, .mk`; note → `p.nota`. Icone come `<symbol>` +
   `<use href>`.
4. Carica il skill `artifact-design`, pubblica con Artifact (una sola URL, ridistribuisci sullo stesso
   file a ogni giro). Verifica entrambe le viste.
5. Iterazioni con Marco: cambia SOLO quello che chiede, non rimescolare le posizioni già approvate.
6. PDF di stampa (vista cliente, senza note):
   ```
   python3 scripts/pdf_menu.py soffietto carta.html Menu_<Cliente>_<anno>.pdf --extra-css esempi/stampa_soffietto.css
   python3 scripts/pdf_menu.py libro     carta.html Menu_<Cliente>_<anno>.pdf
   ```
   Lo script dice `OK … N pagine` o `⚠️ ATTESE`. Sul libro compatta da solo se una facciata sfora.
   Sul soffietto le ante tagliano quello che sfora (non vanno a pagina nuova): **guarda sempre il PNG**
   (`pdftoppm -r 40 -png out.pdf prova`) prima di consegnare e, se serve, riduci la scala nel CSS extra.
7. Consegna: link artifact (per la call) + PDF (per il grafico/tipografia) + riepilogo €/anno.

## Trappole WeasyPrint (già pagate)
- Il **flex orizzontale** per affiancare ante/pagine le impila → ante a coordinate assolute (lo fa lo script).
- I **flex verticali** con `gap` sballano → blocchi + margini (lo fa lo script).
- Il bordo **dashed** manda in overflow il calcolo del tratteggio e blocca il render → diventa solid.
- `<use href="#id">` non viene risolto → lo script inlinea i `<symbol>`.
- Stesso formato di pagina su tutte le facciate: mai una pagina più lunga delle altre.

## Collegamenti
`menu-engineering` (classificazione a monte) · `foodcost-cliente` (file 02) · `estrai-dati-ipratico` ·
`strategia-marketing-rbr` (tono dei testi) · `relazione-rbr` (relazione che accompagna la carta).
