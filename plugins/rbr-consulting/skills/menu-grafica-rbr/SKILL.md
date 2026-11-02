---
name: menu-grafica-rbr
description: >-
  Tutto il know-how RBR su menu engineering e creazione grafica dei menu, distillato dai lavori veri su
  Cartabianca (bar + ristoranti Tennis/Club, ott 2026) e Luna Blu (Parma, carta inverno + menu esterno
  120x70, ott 2026), più Giurgés/Antipapa. Copre: dati di vendita dalla cassa (CIC, Zucchetti, iPratico,
  CEI) → food cost → matrice per categoria → scelte di contenuto e prezzi → carta stampabile (libro A4,
  soffietto, A5 dolci, pranzo bar, cartello grande formato, volantini, adesivi, tabelloni) → foto piatti
  (ChatGPT + scontorno) → PDF di stampa con abbondanza → listino per la cassa → presentazione al
  cliente → consegna su Drive. Usala SEMPRE quando Marco dice "fammi il menu/la carta di X", "rifai la
  carta", "menu come Cartabianca / come Luna Blu", "menu esterno / cartello / tabellone", "carta dolci",
  "carta pranzo", "volantino brunch", "adesivi orari", "foto dei piatti", "presentazione menu
  engineering", "prezzi nuovi in cassa", "PDF per la tipografia", oppure corregge una carta già fatta.
---

# Menu RBR — dall'engineering alla carta stampata

> Skill condivisa da Marco Cuccaro il 2026-10-12 (scansione skill).

Questa skill è la **memoria operativa**: regole decise da Marco, specifiche grafiche, trappole già
pagate e template funzionanti. Si appoggia a due skill del plugin, non le sostituisce:
- `rbr-consulting:menu-engineering` → teoria (5 pilastri, Kasavana-Smith).
- `rbr-consulting:carta-menu-rbr` → artifact a doppia vista + `pdf_menu.py` (copia in `scripts/`).

**Regola zero (Marco):** «pronto» = lo posso mandare in tipografia adesso senza toccarlo. Se c'è un
segnaposto, una stima, una foto finta o un colore a occhio NON è pronto: scrivilo in cima con ⚠️.

## Mappa dei file di questa skill
| File | Cosa contiene |
|---|---|
| `references/regole-carta.md` | **Le regole decise** (ingegnerizzazione, prezzi, descrizioni, evidenze, legale). Leggere SEMPRE. |
| `references/grafica-e-stampa.md` | Formati, palette/font usati, scale tipografiche, CSS, trappole WeasyPrint/Chrome, abbondanza, tipografie |
| `references/foto-piatti.md` | Pipeline foto: ChatGPT (prompt), recupero immagini, scontorno rembg/PIL, piatti bianchi, webp |
| `references/dati-e-matrice.md` | Estrazione venduto per gestionale, food cost, soglie matrice, stagioni, €/anno delle leve, listino cassa |
| `references/presentazione-cliente.md` | Deck "5 step per un menu WOW": struttura, matrici in italiano, cosa NON mostrare |
| `references/caso-cartabianca.md` | Caso completo Cartabianca (bar, pranzo, ristoranti, listino, feedback Emiliano/Luciano) |
| `references/caso-lunablu.md` | Caso completo Luna Blu (carta 8 facciate, menu esterno 120×70, 15 giri di correzioni) |
| `references/errori-da-non-ripetere.md` | Tutti i feedback negativi di Marco, in una lista |
| `scripts/` | `pdf_menu.py`, `stampa_abbondanza.py`, `scontorna_foto.py`, `prep_foto.py`, `comune.py` (`pf()`, `ordina()`), `parse_mesi.py`/`stagioni.py`/`matrici.py` (Zucchetti → matrice), `gen_presentazione_matrici.py`, `clip.sh` (salva immagine dagli appunti), `adesivi_orari.py` |
| `templates/` | Generatori pronti: `lunablu_libro/` (libro A4 doppia vista), `lunablu_esterno/` (120×70), `cartabianca_bar/` (libro bar, pranzo, volantino), `cartabianca_ristoranti/` (Tennis/Club + dolci A5 + allergeni), `giurges_antipapa/` (soffietto + libro), `listino_cassa/` |

Sorgenti originali (vivi, nel repo RBR AI): `data/cartabianca/carta_menu/` (+ `bar/`, `rigenera.sh`),
`consegne/2026-10-09/` (Luna Blu), `data/lunablu/menu_inverno_2026/` (json di lavoro),
`giurges-antipapa/carte-menu/`, `data/cartabianca/listino_cassa/`.

## Domande da fare PRIMA (un solo messaggio numerato, solo quelle che mancano)
1. Formato e misure di stampa (libro A4 a facciate? soffietto? A5? cartello?) e dove si stampa.
2. Brand: logo vettoriale, colori, font, menu attuale stampato (se non c'è → li ricavo da Instagram/sito e scrivo gli HEX).
3. Foto vere disponibili o le genero io (ChatGPT dalla foto vera del piatto).
4. Stagione e piatti oggi attivi in cassa; prezzi attuali di ogni voce.
5. Chi dà il sì finale (titolare) e chi in cucina valida ingredienti/allergeni/grammature.

## Procedura (ordine fisso: numeri → menu → marketing)
1. **Venduto completo** dal gestionale, per stagione (inverno ≠ estate), in pezzi/mese. Alias dei tasti
   rinominati in cassa. → `references/dati-e-matrice.md`.
2. **Food cost** dal file 02 del cliente (materie prime IVA esclusa, prezzo ÷1,1). Stime marcate "stima".
3. **Matrice per categoria** (mai sull'intero menu). Classifica anche fuori carta ed estivi, ma le soglie
   si calcolano solo sui piatti in carta della stagione.
4. **Scelte di contenuto** da mostrare a Marco in un messaggio PRIMA di disegnare: categorie oltre 7 e chi
   esce, premium (3 voci), formati/upsell, prezzi nuovi (sempre partendo dal prezzo attuale di cassa),
   leve in €/anno. Niente piatti che non sono in cassa.
5. **Unica fonte prezzi**: un foglio/JSON (`prezzi_live.json` a Cartabianca, riga dati in `gen_carta.py`
   a Luna Blu). Mai prezzi scritti a mano nell'HTML.
6. **Carta**: parti dal template del formato giusto in `templates/`, applica `references/regole-carta.md`.
   Artifact a doppia vista (cliente/consulente) quando serve mostrarla in call; un solo URL, ripubblicato.
7. **Foto**: vere o generate dalla foto vera (`references/foto-piatti.md`). Mai foto di un altro piatto.
8. **PDF**: `python3 scripts/pdf_menu.py libro|soffietto carta.html Out.pdf --extra-css stampa.css` →
   deve dire `OK … N pagine`. Poi **guarda i PNG** (`pdftoppm -r 40 -png Out.pdf prova`) pagina per pagina.
   Per la tipografia: `scripts/stampa_abbondanza.py` (3 mm + colore esteso al bordo), CMYK e foto originali.
9. **Listino cassa** (se cambiano i prezzi): `templates/listino_cassa/build_listino.py` → xlsx per locale
   + "Da verificare" / "Nuovi da creare" + riepilogo 2 pagine per il titolare. Carta e cassa partono insieme.
10. **Revisione**: agente `rbr-reviewer` + checklist sotto. Poi Drive nella cartella del cliente (stessi ID
    a ogni giro, md5 dopo upload) + link a Marco. Commit a ogni versione, nota nella memoria cliente.

## Giri di correzione
- Cambia **solo** quello che Marco chiede, alla lettera. Non rimescolare posizioni già approvate.
- Aggiorna lo stesso file/URL/ID, non crearne di nuovi. Le varianti si fanno come copia (`_v9` accanto alla `_v8`).
- Se una richiesta è ambigua ("aumento leggero dei prezzi") chiedi prima di toccare la carta.

## Checklist prima di consegnare
- [ ] Formato confermato; tutte le pagine stesse misure; numero facciate multiplo di 4 per il libro.
- [ ] ≤7 voci per categoria; ordine per margine (n.2, **n.1 secondo**, …, n.3 in fondo); un solo segno per categoria, sul n.1.
- [ ] Prezzi: piccoli, stesso font della descrizione, attaccati in coda (`… | 14,5`), niente €, niente ,00, mai colonna/rosso/bold.
- [ ] Ogni voce esiste in cassa; nessun prezzo in carta sotto la cassa; ribassi decisi da Marco.
- [ ] Descrizioni = ingredienti veri, niente marche/fornitori, asterisco congelati a fine descrizione.
- [ ] Piede legale (congelati, allergeni su richiesta, coperto) sulle pagine di sinistra, mai sopra altri elementi.
- [ ] Colori/font dal brand reale, HEX nel riepilogo; logo vero (se bassa risoluzione → ⚠️ chiedere vettoriale).
- [ ] Foto vere o generate da foto vera, stesso stile; nessun riquadro "FOTO"; elenco "foto da fare" se mancano.
- [ ] Anteprime PNG guardate: niente testo tagliato, attaccato al bordo, parole orfane, riquadri sbilanciati.
- [ ] Stagione giusta (niente piatti estivi a ottobre, max 2 eccezioni).
- [ ] In consegna: ⚠️ in cima per tutto ciò che è stima/da validare (allergeni, grammature, ingredienti, foto, bleed).

