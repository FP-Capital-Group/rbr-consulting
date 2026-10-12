# Grafica e impaginazione — come deve essere fatto un sito RBR

Riferimento visivo: Cartabianca Ristoranti (stile «Eataly»: bianco, beige, un colore di marca forte, foto grandi,
pochi elementi), Raíces (prenotatore a schede in home), Red Mike (barra mobile, nav a 2 bottoni).
Il sito deve sembrare **il locale**, non un template: colori, logo, foto e parole sono le sue.

## 1. Principi (in ordine di importanza)
1. **Prenotare è la cosa più facile della pagina.** In ogni schermata c'è un modo di prenotare a portata di pollice
   (vedi `prenotatore.md`).
2. **Foto vere, grandi, calde.** Una foto vera del locale vale più di dieci sezioni. Senza foto vera: blocco a
   tinta (beige/colore di marca) col nome, mai stock spacciata per il locale.
3. **Poco testo, concreto.** Ogni sezione: un titolo che dice una cosa, 1-3 righe, un bottone. Niente muri di testo,
   niente «benvenuti nel nostro sito».
4. **Mobile prima di tutto.** L'80-90% delle visite di un ristorante arriva dal telefono: si disegna a 390 px e poi si
   allarga.
5. **Coerenza assoluta:** stesso font per tutti i titoli, 2 misure di bottone, un solo beige, stessi angoli ovunque.

## 2. Colori
- **Si leggono dal brand** (logo, insegna, menu stampato, tovagliette, sito vecchio): metodo e script in
  `sito-landing-ristorante/references/colori-brand.md`. Si scrivono gli HEX nel riepilogo per il cliente.
- Struttura della palette (5 ruoli, tutti in `theme.json`):
  | Ruolo | Uso | Esempio Cartabianca |
  |---|---|---|
  | Bianco | sfondo principale | `#FFFFFF` |
  | Beige / neutro caldo | sfondo sezioni alterne, blocchi senza foto | `#F5EFE0` |
  | Colore di marca | bottoni pieni, link, etichette, fascia annunci | rosso `#A6192E` (hover `#86121F`) |
  | Scuro | piè di pagina, titoli su chiaro | marrone `#2E170D` / `#4A2617` |
  | Testo + grigio caldo + linea | corpo, secondari, bordi | `#1E1A17`, `#5E544C`, `#E8E2DA` |
- **Contrasto ≥ 4,5:1** su ogni coppia testo/sfondo (testo grande ≥ 3:1). Il giallo/arancio di marca su bianco non
  passa: si scurisce per il testo e si tiene pieno solo dove ci va testo scuro sopra.
- Locale senza identità di colore: toni caldi (rosso, terracotta, ocra, bordeaux, verde oliva scuro). Vietati rosa
  pallido, azzurro, viola, grigio freddo come colore principale.

## 3. Tipografia
- **2 font**: uno per i titoli con carattere (serif tipo Lora, o il font del logo se libero), uno per il testo ben
  leggibile (sans tipo DM Sans/Inter). Caricati **dal sito stesso** (woff2 in `assets/fonts/`), mai da Google Fonts.
- Misure (mobile → desktop): H1 36/40 → 46/48 · H2 28/32 → 32/40 · H3 22 · corpo 16/24 (mai sotto 16 px su mobile) ·
  etichette 14 px 600 maiuscolo con un po' di spaziatura · prezzi nel font del testo.
- Un solo H1 per pagina. Titoli in frase normale (non TUTTO MAIUSCOLO), niente punti esclamativi.

## 4. Bottoni, card, foto
- Bottoni a pillola (raggio 999), **2 misure** (50 px normale, 40 px piccolo) × **3 varianti**: pieno (colore di
  marca), contorno, bianco su foto. Testo 14 px 700, verbi d'azione: «Prenota un tavolo», «Chiama», «Vedi il menu».
- Area tocco ≥ 48×48 px. Niente emoji nei bottoni (icone SVG se servono).
- Card: angoli 6 px, foto in alto, titolo, 1 riga, link/bottone. Foto con angoli 16 px.
- Foto: originali ≥ 1600 px, caricate in webp (~1600 px lato lungo, qualità ~78); copertine solo con foto ≥ 1200 px;
  card ≥ 400 px. Alt descrittivo IT/EN. Mai foto con persone riconoscibili senza consenso (es. foto di clienti prese da
  Google: vietate).
- Hero e prima foto: **mai** `loading="lazy"`; tutto il resto sì.

## 5. Spazi e griglia
- Contenitore testo 760 px, largo 1200 px; sezioni con 40 px (mobile) / 80 px (desktop) sopra e sotto.
- Sezioni alterne bianco/beige per dare ritmo, mai due sezioni beige attaccate.
- Griglia locali/card: 4 per riga sopra 1100 px, 3 sotto, 2 sotto 860, 1 sotto 560.

## 6. Header e footer
**Header** (sticky, 56 px su mobile):
- Logo a sinistra (link alla home), voci al centro (max 5: Menu, Locali, Eventi, Chi siamo, Contatti), a destra
  2 bottoni: **«Prenota»** pieno + uno secondario (contorno: «Chiama» o «Ordina»), selettore lingua IT|EN a pillole.
- Sotto 1100 px: hamburger (tre linee → X), dentro voci + lingua; i 2 bottoni restano visibili o passano nella barra
  in basso.
- Fascia annunci opzionale sopra l'header (40 px, colore di marca): una frase sola («Pranzo di lavoro dal lunedì al
  venerdì»), mai un carosello di avvisi.
- Header in flusso (niente `position:absolute` centrato: con loghi larghi si sovrappone).

**Barra fissa in basso su mobile** (sotto 768 px): 2 bottoni a metà larghezza «Chiama» | «Prenota» (nella pagina
di un locale: telefono e prenotatore di QUEL locale).

**Footer** (colore scuro, testo chiaro): per ogni locale indirizzo + link «Indicazioni» (apre Google Maps in nuova
scheda) + telefono `tel:` + orari; social; link Privacy, Cookie, «Preferenze cookie»; **dati obbligatori**
(ragione sociale, sede, P.IVA — vedi `normative.md`); credito discreto opzionale.

## 7. Pagine — struttura sezione per sezione

### Home
1. **Copertina / carosello** (100% larghezza, foto vera del locale): H1 = cosa + dove («Pizzeria napoletana a
   Parma»), sottotitolo di 1 riga col perché, bottone «Prenota un tavolo» (+ «Vedi il menu» contorno).
2. **Prenota subito** (sezione `#prenota`): widget, a schede se più locali (`prenotatore.md`). È la seconda cosa
   che si vede, prima di qualsiasi storia.
3. **Perché venire da noi**: 3 punti concreti con icona o foto (il piatto firma, l'ingrediente, l'esperienza). Niente
   «qualità, passione, tradizione».
4. **Il menu in evidenza**: 3-6 piatti con foto vera e nome (card cliccabili → pagina menu), bottone «Tutto il menu».
5. **I locali** (se più di uno): card con foto, indirizzo, «Prenota» e «Scopri».
6. **Dicono di noi**: stelle e numero recensioni reali con link alla scheda Google; riconoscimenti verificati (testate,
   guide) come wordmark/logo con link alla fonte.
7. **Eventi e feste**: 1 foto + 2 righe + bottone verso `/eventi/`.
8. **Club / fidelity** (se c'è): cosa si riceve (regali), modulo `novita` o bottone.
9. **Dove siamo**: indirizzo, orari, telefono, «Indicazioni».

### Pagina locale `/locali/<nome>/` (una per sede)
Testata con foto del locale e H1 «<Nome> – <tipo> a <città/quartiere>» → riga info (indirizzo, orari, telefono,
Indicazioni) → **prenotatore di quel locale** con «Chiama» sopra e «Preferisci essere richiamato?» sotto → 3 motivi /
cosa trovi qui → foto (galleria 3-6) → menu di quel locale → FAQ (parcheggio, cani, celiaci, bambini, gruppi) → «Gli
altri locali». Stagionali: fuori stagione avviso «riapre a …» e niente prenotazione.

### Menu `/menu/`
HTML vero (indicizzabile, traducibile), non PDF né foto del menu. Categorie nell'ordine del menu stampato, indice a
chip in alto che resta visibile; per piatto: nome, descrizione breve, prezzo piccolo a destra senza «€» e senza «,00»,
icone allergeni/veg opzionali. Foto di categoria solo se coerente. In fondo: nota allergeni + coperto + «Prenota».
Più locali con menu diversi: una sezione per locale o pagina per locale. Il PDF stampabile → skill `carta-menu-rbr`.

### Prenota `/prenota/`
H1 «Prenota un tavolo» → schede/widget per locale con ancore `#<locale>` → piano B (telefono + modulo richiamami) →
FAQ brevi (gruppi oltre X persone, eventi, disdetta).

### Eventi `/eventi/`
Copertina → tipi di evento (compleanno, aziendale, laurea, comunione…) con foto → «come funziona in 3 passi» → modulo
`evento` → foto sale/terrazze con capienze.

### Contatti, Chi siamo, Privacy/Cookie
Contatti = locali con tutti i dati + modulo `contatto`. Chi siamo = storia vera, persone vere, foto vere (facoltativa).
Privacy/Cookie = testi in `normative.md`, ultimo aggiornamento in testa.

### 404
Messaggio breve + «Prenota» + «Vai alla home».

## 8. Cose vietate (nate da errori)
- Recensioni inventate o «Recensione Google» scritte da noi. Popup che coprono il prenotatore. Più di 2 bottoni nella nav.
- Animazioni d'ingresso, parallasse, elementi che si muovono al passaggio del mouse, autoplay di video con audio.
- Bandiere emoji (su Windows diventano lettere), widget di traduzione automatica.
- Sfondo foto dietro i moduli (solo tinta unita). Foto di categoria a caso. Disclaimer «sito dimostrativo».
- Prezzi in rosso o col «,00». Slogan come H1. «Cucina romana» a Lodi (mai dedurre la regione da «trattoria»).
- Mappe Google caricate in pagina senza consenso (usa link «Indicazioni» o mappa dopo il clic).

## 9. Controllo finale della grafica
Screenshot a 360, 390, 768, 1280 px di ogni pagina IT ed EN; nessuno scroll orizzontale; header che non si
sovrappone tra 1024 e 1280; contrasto verificato; un solo font per i titoli; bottoni nelle 2 misure; nessun stile
inline (`grep 'style="'` sul sorgente delle pagine ≈ solo quelli generati da WordPress).
