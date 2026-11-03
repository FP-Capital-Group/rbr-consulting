# Regole della carta RBR (decise da Marco — non ridiscuterle)

Consolidate da Cartabianca (set-ott 2026), Giurgés/Antipapa (set-ott 2026), Luna Blu (ott 2026).

## 1. Ingegnerizzazione
- **Massimo 7 voci per categoria.** Prima di disegnare: elenco categorie che sforano + chi esce.
  Pizze: massimo 4 gruppi (Luna Blu: tradizionali 6 · classiche 6 · speciali 6 · d'autore 3).
- **Ordine per margine**: n.2 in cima, **n.1 al 2° posto** (dove l'occhio si ferma), poi a scendere,
  **n.3 in fondo** (primacy/recency). Funzione `ordina()` in `scripts/comune.py`. `fisso=True` per
  tenere un ordine dato a mano quando Marco lo chiede.
- **Un solo segno per categoria, sul n.1**: cornice puntinata (Cartabianca bar), cornice sottile
  (Giurgés), asticella a sinistra alta quanto il testo, oppure banda piena (Luna Blu Misto mare).
  Al massimo un tipo di evidenza per categoria. Niente riquadri enormi o larghi tutta la pagina.
- **Foto solo sul n.1** (max 1 per pagina nelle carte bar; premium con foto grande).
- **Categoria premium / d'autore** (3 voci, prezzo alto, colore diverso o riquadro, in alto, con foto):
  fa da ancora. Dopo un risotto a 21 la pasta a 16-19 sembra giusta. Es. Luna Blu primi d'autore
  21-22-18, grandi secondi 28-28-26, pizze d'autore 14-16-15.
- **Decidi sulla matrice, non a gusto**: DOG fuori (anche doppioni: Gorgo calabrese = Diavola), PUZZLE
  spinti, STAR protette. Piatti freddi/insalate: scegli per **margine totale annuo** (margine × pezzi),
  non per margine unitario (Insalata Design resta perché Stella anche se a Marco non piace).
- **Piatti dello chef / del giorno**: niente risalto in carta (margine non controllato). Solo un riquadro
  "oggi in cucina" e li dice il personale.
- Non evidenziare ciò che non vende anche se rende (Pescatora a Luna Blu): evidenzia ciò che vende E rende.
- I "metà" e le porzioni da dividere (pizza in pala, metà 30 cm) di solito escono: spostano clienti da
  un piatto intero che rende di più (pala 7,73 € di margine ma 3,9 a persona).
- Stagione da calendario (21/3, 21/6, 23/9, 21/12). Carta invernale: max 2 piatti estivi.
- Zero piatti nuovi in cucina per Experience/percorsi: solo piatti già in carta.

## 2. Formati, upsell, ancore (le leve)
- **Formati dove la materia prima costa poco**, riquadro PRIMA della sezione a cui si applica, con icone:
  - Pasta "Che fame hai?": normale 100 g inclusa · abbastanza 150 g +4 · tanta 220 g +6 (Luna Blu;
    Antipapa +4/+6). Pranzo bar: giusta inclusa · abbondante +2 · extra +4. Grammature da validare in cucina.
  - Panini/burger: icone M · L · XL accanto al nome, legenda in una riga (L +4, XL +7). Con +3 l'hamburger
    in più non rende.
  - Contorni a formato fisso 8/10/12 ("tipo pokè"). Tazze: medio +0,50, grande +0,90; spremuta grande +1,50.
- **Impasti** (pizza): "Scegli il tuo impasto" tra tradizionali e classiche: integrale +2, croccante +2,5,
  senza lattosio +2 — con foto, stesse distanze del riquadro formati.
- **Aggiunte**: 3-4 con foto tonda, "La vuoi ancora più buona?" (bufala +3, stracciatella +3, crudo +3,
  porcini +3,5; bacon +2, cheddar +1,5, guanciale +2,5). Niente descrizione sotto gli upsell.
  Upsell scritti "+ 3", senza puntino davanti, poco evidenti.
- **Experience / menù componibili**: prezzo barrato piccolo (`<s>32</s> 27 a persona`, "pp" + "minimo 2"
  se vale per due). Serve a portare dolce e vino al tavolo, non a scontare. Sconto giusto ~10-15%
  (menù Giurgés al 21-28% erano troppo scontati → riportati a 24/31/37 con 29/37/43 barrati).
- **Formule bar senza sconto**: colazione completa = somma piena; "col caffè" = caffè + mignon a prezzo
  pieno; brunch completo = +5,3.
- **Coperto e servizio** espliciti (2-3 €), e verifica che la cassa lo batta davvero (Giurgés: carta 2,
  cassa 1 → leva +15k/anno).
- **Dolci e amari** con sezione propria o carta A5 a parte (amaro al 4-6% di penetrazione = leva sottovalutata).
- **Abbinamenti** con icona calice/boccale colorata, senza scritta "in abbinamento": solo dove ha senso
  (Luna Blu: solo pizze; Giurgés/Antipapa: solo sui primi 2 di ogni lista). Mai su tutto.
- Ogni leva in vista consulente ha la nota verde con **€/anno** e l'ipotesi dichiarata ("8 clienti su 100").
  Formula prezzo: `(nuovo − oggi)/1,1 × pezzi/mese × 12` (Cartabianca: `× 0,98`).

## 3. Prezzi
- Piccoli, **stesso carattere e colore tenue della descrizione**, attaccati in coda: `descrizione | 14,5`
  (o `· 14,5`; `NOME | prezzo` se non c'è descrizione). Mai in colonna, mai su riga da soli, mai bold,
  mai rosso, mai in evidenza.
- Niente €, niente ",00", niente zero finale: 10 · 12,5 · 2,4. Funzione `pf()`/`eur()`:
  `f'{x:.2f}'.rstrip('0').rstrip('.').replace('.',',')`.
- Decimali solo a decine fino a ,80. Niente ,90/,99.
- Ultima parola + "| prezzo" mai separati a capo (`white-space:nowrap` su coda, `coda_prezzo()`).
- **Sempre partendo dal prezzo attuale di cassa** (prezzo più battuto a quantità 1, non la media).
  Mai prezzo in carta sotto la cassa. Ribassi solo se li decide Marco. Aumenti piccoli: +0,50/+1 sui
  Plowhorse più venduti, +1 base, +2/+3 premium.
- "A persona": scrivilo solo se è vero (Marco: "è già a persona o te lo stai immaginando?").

## 4. Testi
- Categorie con nomi semplici: "I secondi", "Insalate" (non "Insalatone", non "Carne e pesce").
  Titolo con seconda parola in corsivo ok ("I primi *d'autore*").
- **Niente occhielli, sottotitoli, badge, frasi spiritose** sopra le categorie ("non mi fa impazzire
  quella scritta sopra le categorie"). Eccezioni approvate: tag "la più amata dai nostri clienti",
  "il consiglio dello chef", "la scelta dello chef / da provare / il più amato" (pranzo bar).
- Descrizioni = **ingredienti veri** (schede chef, fatture), con origine/qualità; più ricche sui piatti da
  spingere; su una riga se no resta una parola orfana; a capo dove lo chiede Marco (`|BR|`).
- Niente marche (Nutella → nocciola, Red Bull → energy drink, Campari → bitter soda), niente nomi di
  fornitori (Bedogni, Gennari, Beretta), niente frasi vuote ("tutte le nostre pizze cuociono nel forno a legna").
- Storytelling vero sui nomi: Santa Croce "la piazza dove nel 1970 Giovanni aprì il primo locale",
  "fatti in casa da nonna Maria", Tagliere *Luna Blu*. ⚠️ claim di origine ("pomodoro del territorio")
  solo se verificati in fattura.
- Una sola alternativa per voce (non "Viennese o Chip & Chop").
- Solo italiano salvo richiesta.

## 5. Legale
- **Asterisco congelati** in fondo alla descrizione, prima del prezzo (`…e limone* | 28`), mai sul nome.
  Va su tutti i prodotti congelati/abbattuti (pesce, frutti di mare).
- Piede piccolo sulle pagine di sinistra (mai sopra altri elementi):
  «I piatti che presentano l'asterisco potrebbero essere preparati con prodotti congelati o abbattuti in
  base alla disponibilità. L'elenco completo degli allergeni … è disponibile su richiesta … Prezzi espressi
  in euro. Coperto e Servizio | 3»
- Allergeni: o numeri UE 1-14 accanto al nome con legenda (Antipapa) o solo dicitura + documento scritto
  per piatto (D.Lgs 231/2017; Luna Blu, Cartabianca bar). Numeri stimati = ⚠️ da validare in cucina;
  se non validati, toglierli. Prudenza: pesto → 8 frutta a guscio.
- Dicitura HACCP abbattimento sul crudo di pesce.

## 6. Design
- **Sfondo bianco/carta chiaro** nelle pagine di lettura; scuro/pieno solo su copertina, Experience, retro, premium.
- Max 2 font (mai 2 serif o 2 bastoni insieme... salvo famiglia coerente), max 3 colori. Font e palette
  dal **brand reale** (post Instagram recenti > logo Facebook vecchio), HEX nel riepilogo.
- Titoli e categorie dritti (niente testo ruotato). Spaziature uniformi ("rendi tutte le dimensioni uguali").
- Riempi la pagina: niente vuoti, niente riquadri giganti. La pagina destra (dove cade l'occhio) prende la
  sezione che rende di più, corpo più grande.
- Copertina pulita: logo vero, nome, "dal 1980" — niente cerchi o grafiche "da loghi".
- Illustrazioni solo se eleganti (fine line art monocolore, ramo d'ulivo bordeaux) — no clip art.
- Grafiche/tabelloni per bar: **orizzontali** di default. Carte da tavola: libro A4 verticale.
- Mai testo sopra una foto.
- Menu digitale / QR al posto del cartaceo: NO (abbassa lo scontrino).

