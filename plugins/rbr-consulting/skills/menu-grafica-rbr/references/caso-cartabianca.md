# Caso Cartabianca (gruppo bar + ristoranti, Firenze/Prato — set-ott 2026)

Persone: Massimo (store manager/titolare, ultima parola sui prezzi), Emiliano (bar/operativo), Elisabetta,
Luciano Purpi (RBR, analisi). Gestionale: Cassa in Cloud. Sorgenti vive: `data/cartabianca/carta_menu/`
(ristoranti) e `data/cartabianca/carta_menu/bar/` (bar). Copie in `templates/cartabianca_*`.

## Cosa è stato prodotto
- **Ristoranti Tennis e Club**: libro A4 8 facciate stile Eataly bianco (Lora, amaranto #8A1C2B), pagina
  Experience su foto con velo amaranto, blocchi "grandi secondi" rosso pieno e "primi d'autore" in cornice
  con foto a mezzo; carta dolci A5 rossa (amari e caffè sul retro), carta allergeni A4, PDF tipografia con
  abbondanza 3 mm. Rigenera: `rigenera.sh` (prezzi_live → build → pdf_menu → perche_piatti → extra_carte).
  `Perche_ogni_piatto_Tennis_Club.xlsx` = motivazione di ogni piatto.
- **Libro bar A4 (colazione/bar)** e variante Panciatichi con brunch: Cormorant + EB Garamond, marroncino,
  cornice puntinata rossa sul n.1, combo su fascia crema, misure tazze sotto il nome ("piccolo 1,6 · medio 2,1 ·
  grande 2,5"). Generatore `build_libro_bar.py` (+ `build_formati.py` dati/leve, `build_grafiche.py` font/foto).
- **Carta pranzo bar (v9)**: A4 4 facciate 1 colonna, secondi a destra più grandi, fasce a 3 misure con cerchi
  concentrici ("Che fame hai?" giusta/abbondante +2/extra +4; contorni 8/10/12), riquadro "oggi in cucina".
  `build_pranzo_v9.py` + `stile_pranzo.css` (congelato) + `stampa_pranzo_v9.css`.
- **Volantino brunch** (bozza con fascia rossa e filigrana BOZZA; poi non servito: brunch solo nel libro Panciatichi).
- **Adesivi nuovi orari** A5 per sede (Chrome headless): `scripts/adesivi_orari.py`.
- Tabelloni verticali / schermo TV bar (`build_grafiche.py`, `build_bar_eataly.py`). ⚠️ Default orizzontale.
- **Listino cassa** + riepilogo Massimo + aumenti prezzi (`aumenti_prezzi.py`).
- Analisi scontrino medio pranzo vs bar (pranzo = scontrino con ≥1 piatto entro le 16).

## Decisioni di contenuto (Emiliano 07-08/10 + Marco)
- Niente uovo alla Benedict; pancake da prodotto pronto; "Il classico" (roast-beef/arista/fesa) a 13 al posto
  del petto di pollo; pasta corta solo pomodoro 8 o pesto 8,5; "Due mignon" 2,4 al posto del tiramisù;
  "Mezzaluna" → "Ciabattina"; schiacciate a 5; torna il carpaccio di bresaola (fuori tonno e fagioli);
  pizza in pala eliminata; brunch pilota solo a Panciatichi; grafiche ristoranti non servono.
- Luciano 06/10: brunch in alto dove cade l'occhio, copertina pulita, prezzo in fondo alla descrizione,
  primo e secondo del giorno fuori carta, contorni a formato fisso, secondi più in evidenza, mai testo su foto.

## Lezioni specifiche
- Un solo foglio prezzi con precedenza Massimo; carte generate da `prezzi_live.json`.
- 45 prodotti con "prezzo oggi" del foglio sotto la cassa → usare sempre il prezzo vero di cassa.
- Caesar 13 in cassa vs 12 nel foglio → resta 13 (mai sotto la cassa).
- Ogni voce nuova (porzioni, tazze, spremuta grande, contorno medio) creata in CIC prima della stampa.
- PDF su Drive sugli stessi ID (una volta ricaricato su ID sbagliato), md5 dopo upload. Il service account
  non crea file: file vuoto col connettore di Marco, poi `files().update` col SA.
- Aperti a ott: documento allergeni bar; prezzi nuovi Tennis/Club (fiorentina 60 €/kg, spiedino 16, misticanza 6)
  da riportare in cassa; pezzi brunch Panciatichi da creare in cassa.
- Note complete: `consegne/2026-10-08/NOTA_Cartabianca_menu_feedback_Emiliano.md`,
  `data/cartabianca/_handover/2-1_menu_bar.md`, `call_luciano_2026-10-06_menu.md`, `prezzi_bar_revisione.md`.

