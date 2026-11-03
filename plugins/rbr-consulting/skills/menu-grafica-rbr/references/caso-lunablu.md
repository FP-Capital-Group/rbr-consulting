# Caso Luna Blu (ristorante-pizzeria dal 1980, Parma — 09/10/2026)

Titolare Salvatore (Salvo) Buonocore. Gestionale Zucchetti. Output in `consegne/2026-10-09/`, dati di lavoro in
`data/lunablu/menu_inverno_2026/`, template in `templates/lunablu_libro` e `templates/lunablu_esterno`.
Artifact doppia vista: https://claude.ai/artifact/MgZ45zngp9rWhwVN65xMhP (15 versioni sullo stesso URL).

## Numeri
- Inverno: 7,64 €/pz × ~1.045 pz/mese; pezzi 61% pizza / 39% cucina (ricavo 52/48); cucina 10,43 €/piatto,
  pizzeria 5,95 €/piatto → stesso margine mensile. FC teorico 22,3%.
- Carta: da 87 a **52 voci** (−40%): antipasti 7, insalate 3, contorni 4, primi d'autore 3, pasta 7,
  grandi secondi 3, secondi 4, pizze tradizionali 6, classiche 6, speciali 6, d'autore 3. +14k €/anno.

## Decisioni di Marco
- Base invernale, max 2 estivi nei primi (linguine allo scoglio, paccheri al polpo). Pizze in 4 gruppi.
  Panuozzi e maxi a metro fuori dalla carta; Margherita fuori carta ma in cassa a 8. "Alza tutto" (+1 base,
  contorni +0,5, premium +2/+3, lasagne 10→12, tagliatelle 15→18). Vini e dolci in carte a parte; birre ≥5,
  piccola spina 3,50.
- Experience `<s>32</s> 27 pp`: antipasto da dividere + una portata a testa + dolce da dividere (+1.700 €/anno).
- Formati pasta 100/150 g +4/220 g +6 (+470 €/anno); impasti integrale +2, croccante +2,5, senza lattosio +2;
  aggiunte bufala/stracciatella/crudo +3, porcini +3,5 (+820 / +1.100 €/anno).
- Tag: "la più amata dai nostri clienti" (Capricciosa), "il consiglio dello chef" (spaghettoni alle vongole).
- Posizione pizze: d'autore alto-dx, speciali basso-dx, tradizionali alto-sx, classiche basso-sx.
- Nomi: Mondiale → **Santa Croce** (piazza del primo locale 1970), Amalfi (origine famiglia), Tagliere Luna
  Blu, insalate greca/Brasile/Italia. Abbinamenti solo sulle pizze. Niente numeri allergeni, solo dicitura.

## Il giro delle correzioni (applicate alla lettera, una per volta)
Bodoni → Lora; Insalatone → Insalate; "a persona" verificato → `27 pp · minimo 2`; asterisco dal nome a fine
descrizione; prezzi decimali corti; Misto mare: box pieno → banda con foto che esce → più piccolo → "come era
prima, più grande" → "avvicinalo"; asticella alta solo quanto il testo; icone impasti stilizzate (no) →
colorate (no) → foto; "tirata" → "croccante" senza immagine; distanze impasti = "Che fame hai?"; piede solo a
sinistra; copertina senza cerchio, solo "dal 1980"; contorni +16 mm di aria e titolo 17pt; spaziature tutte
uguali; tolti fornitori dalle descrizioni, tolta la frase sul forno a legna, tolto il "puntino" negli upsell;
Blue Moon, Bronte, Mazara fuori; una sola alternativa (no "Viennese o Chip & Chop").
"Preparalo come se dovesse essere stampato."

## Menu esterno 120×70 cm
Cartello per bancone/forno e asporto leggibile a 1,5-2 m. `gen_esterno.py` riusa i dati di `gen_carta.py`
(exec della parte prima di `def premium`). Testata blu 74 mm, etichette LA CUCINA / LE PIZZE, griglia 6
colonne con filetto tra cucina e pizze. Rispetto alla carta: tornano 4 panuozzi (~7 € margine, sopra i 5,95
della pizza media — proposta da confermare); escono Experience, abbinamenti, Margherita. Senza bleed.

## Aperti dopo la call 09/10
Rinominare "Misto mare dello chef"; supplemento Experience per primi d'autore/grandi secondi; grammature
"Che fame hai?" da validare (Salvo: porzioni già abbondanti); panuozzi 4 più cari e particolari; carta dolci
e carta vini (636 bottiglie comprate, ~38 vendute col nome); foto vere dei 6 piatti reali (Salvo diffida AI);
stampa Pixartprinting con abbondanza; "aumento leggero dei prezzi" = ambiguo, chiedere.

## Contesto collegato
Menu convenzionati (55% dei ricavi, Blue Be): `consegne/2026-10-07/LunaBlu_Modello_Menu_Convenzionati.xlsx`
— 10 primi + 10 secondi + 6 contorni, rotazione 2 settimane, costo menu ≤3 € (~40% dei 7,45 netti), "spesa per 100 menu".

