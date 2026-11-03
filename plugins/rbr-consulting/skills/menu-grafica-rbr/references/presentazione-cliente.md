# Presentazione menu engineering al cliente

Deck = **slide di teoria di Marco "5 step per un menu WOW"** (PDF originale, 36 slide 1583×891 pt) +
slide "oggi" del cliente generate in HTML/SVG con WeasyPrint (`scripts/gen_presentazione_matrici.py`),
unite con `pypdf` nei punti giusti. Esempio: `consegne/2026-10-09/Presentazione_Menu_Engineering_LunaBlu.pdf`.

## Struttura (Luna Blu)
1-3 copertina, "Perché?" · 4 **Da dove partiamo** (n. piatti, venduti/mese, FC %, margine medio a piatto,
margine/mese) · 5 **margine per reparto** (cucina vs pizzeria: quota piatti e €/piatto) · 6 tabella margine
per categoria · 7 agenda 5 step · 8-12 Step 1 Limita la scelta · 13-17 **matrici del cliente** · 18-21 Step 2
posizione · 22-26 Step 3 conti/prezzi · 27-32 Step 4 estetica · 33-34 Step 5 emozione · 35 **un solo obiettivo**
(+20/25k €/anno, anche al mese e a coperto) · 36 grazie.

## Matrici (regola fissa di Marco)
- Asse X = **margine €** (profittabilità), asse Y = **pezzi venduti/mese** (scala radice `sq=True`, altrimenti
  i piatti poco venduti si schiacciano in fondo).
- Quadranti in italiano: **CLIENTE FELICE** alto-sx (#E3E6F2) = Plowhorse · **STELLE** alto-dx (#E2EFE4) ·
  **STOP** basso-sx (#F4E2E2) = Dog · **SFIDE** basso-dx (#F3EAD8) = Puzzle. Cerchi chiari per i piatti fuori stagione.
- Mai STAR/PLOWHORSE/PUZZLE/DOG né Enigmi/Cavalli/Cani, mai assi invertiti (il vecchio deck
  `Cartabianca_Menu_RBR.pdf` NON è un modello).

## Cosa NON mostrare
Solo la situazione di **oggi**. Niente pagine della carta nuova, niente "da 87 a 52 voci", decisioni per
quadrante, nuovi prezzi o nuovi nomi: sono la soluzione che Marco svela dopo.

## Dopo la call
Raccogli i punti aperti (rinomine, supplementi Experience, grammature da validare, foto vere da fare, carte
dolci/vini) in memoria cliente e applicali alla carta solo quando confermati.

