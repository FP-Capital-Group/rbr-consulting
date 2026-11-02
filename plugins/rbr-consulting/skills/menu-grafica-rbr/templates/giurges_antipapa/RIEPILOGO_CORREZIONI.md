# Carte Giurgés e Antipapa — revisione STAMPA 07/10/2026

⚠️ BOZZA: serve il sì di Luca sulla lista piatti (consegne/2026-10-07/giurges_antipapa_proposta_piatti_2026-10-07.md) + le cose in fondo.
Versione 06/10 archiviata in `_archivio_2026-10-06/`. Output: `consegne/2026-10-07/{giurges,antipapa}_carta_stampa_2026-10-07.{html,pdf}`.

## Colori, font, logo: presi dal brand vero (post Instagram 2026), non a occhio
- **Giurgés**: terracotta **#CB6028** (sfondo dei post e logo attuale IG), ruggine **#A4441C**, crema **#F2E8DA**, testo marrone #3A2219.
  Il vecchio arancio #F84C1E veniva dal logo Facebook (vecchio): sui post 2026 il colore è terracotta. Logo vero (lettering crema dal file 720 px) su terracotta.
  Titoli bastone pesante (Bricolage Grotesque 800) come «HYDRATION BREAK», testo Oswald, corsivo Caveat Brush come «sorsi e mozzichi». Niente verde: sui canali non c'è.
- **Antipapa**: bordeaux **#690F33**, corallo **#E63D2A**, verde **#08311F**, lilla **#8C83D0** (post «ANTI FAME» e «La pausa pranzo»).
  Logo = wordmark vero «ANTIPAPA · BEATO RISTORO» ricavato dal post (non più la «A» ridisegnata). Titoli Tilt Neon (bastone tondo monolinea come il lettering), testo Archivo.

## Formato (deciso, non cambiato)
- Giurgés: soffietto **3 ante e mezza** come chiesto da Marco (10–11/09), nella misura Mister Pizza 580×297 (ante 160+160+160+100) della versione 06/10. Il 366 mm della skill è la stessa struttura in piccolo: tenuta la misura più recente.
- Antipapa: libro A4, 8 facciate (2 A3 piegati), posizioni approvate l'11/09.

## Foto: solo vere
- Tolte tutte le foto ChatGPT. Foto vere = post Instagram del locale (`foto_vere/`).
- Giurgés: Americano a Roma (sul n.1 dei panini), ribs, burger, cucina (retro). 30 CM, Tagliata, Pezzi Grossi, Tiramisù: niente foto vera → impaginati senza foto.
- Antipapa: nessuna foto vera coerente con un piatto in carta (il polpo su Instagram è con un'altra crema) → piatti senza foto; foto della tavola in copertina, sala sul retro.
- ⚠️ Le foto Instagram sono a 360–640 px: per la stampa servono gli originali del fotografo/agenzia di Luca.

## Contenuti = proposta piatti 07/10
- Giurgés: antipasti 7, panini 7 (rientra Porchetta Pork), Pezzi Grossi 3 (novità fatte con ingredienti già in linea), griglia 5, insalate 2 (fuori Polpo Salad), contorni 4, dolci 6 (Lotus tra i gusti). **Coperto 2,5.**
- Antipapa: antipasti 7 (rientrano Antipasto conviviale, polpette di salsiccia, frittelle di cavolfiore), maritozzi 3, paste 4 + 1 di stagione (gnocchi zucca e porcini, già in cassa), secondi 6 (rientrano rollè e cacciatora), dolci 5 (tutti in cassa).
- Tolti perché NON in cassa: paste d'autore (astice, ricciola, risotto), costata, filetto, ricciola.
- Antipapa: numeri allergeni accanto ai piatti tolti (erano stimati) finché la cucina non li valida.

## Manca per mandare in tipografia
1. Sì/no di Luca su ogni riga della lista.
2. Ingredienti da confermare: Porchetta Pork, Sandwich Ribs, 30 CM, Cestino, Pezzi Grossi (burrata in dispensa?); Antipasto conviviale (cosa c'è dentro), Anticucciolone (descrizione).
3. Foto originali ad alta risoluzione (o foto nuove dei piatti n.1: 30 CM, Tagliata, Fondano, Tagliere, Costoletta).
4. Logo vettoriale di entrambi (Antipapa ricostruito da post Instagram; Giurgés da file 720 px).
5. Allergeni validati dalla cucina (Antipapa) e foglio A4 allergeni Giurgés.
6. Decisioni Marco: patatine fuori dai panini (+2), prezzi interi o con un decimale, panini con/senza hamburger.

---

# Carte Giurgés e Antipapa — revisione 06/10/2026

Sorgenti: `giurges.py` + `giurges.css`, `antipapa.py` + `antipapa.css` (dati e regole dentro). Rigenera tutto:
`python3 giurges.py && python3 antipapa.py` (foto nuove: `../../tools/.venv_rembg/bin/python prep_foto.py`).

## Regole applicate (quelle di Cartabianca)
- Massimo 7 voci per categoria · ordine per margine: n.2 primo, n.1 secondo, n.3 in fondo
- Solo il n.1 evidenziato (cornice sottile), foto solo sul n.1
- Prezzo nello stesso carattere della descrizione, «descrizione | 14,5»: niente €, niente ,00, massimo un decimale
- Abbinamento birra/vino solo sui primi due di ogni lista
- Niente occhielli, sottotitoli e badge («da provare», «la più ordinata»…); testo legale piccolo su ogni pagina
- Descrizioni = solo ingredienti (dalle schede dello chef dove ci sono), niente frasi a effetto
- Font e colori dal brand online (Instagram/Facebook): Giurgés = arancio #F84C1E + crema del logo, serif nero tipo logo (Fraunces) + Oswald; Antipapa = bordeaux #690F33, rosso #E63D2A, verde e lilla dei post, carattere déco (Federo) + Archivio

## Giurgés — soffietto formato Mister Pizza
580 × 297 mm rifilato (+3 mm di abbondanza e crocini), ante 160 + 160 + 160 + 100. Il retro è speculare: a sinistra la mezza anta con dolci e amari, a destra la copertina col logo vero.

Cosa non tornava e ho corretto:
1. **Il 30 CM rimesso tra gli antipasti** (in cassa è già negli starters). È il n.1 per margine: in cornice con la foto. Per restare a 7 voci esce Caciocavallo e Salsiccia (FC 35%).
2. **Taglie panini**: non c'è più il riquadro sotto. Ci sono icone piccole M · L · XL accanto al nome dei burger, con la legenda in una riga: L +4, XL +7. Con +3 l'hamburger in più (~2,3 €) non rendeva quasi nulla.
3. **Prezzi in carta sotto la cassa**: Stinco 19 → 19,5, Ribs 15 → 15,5, Pollo Salad 13 → 13,5, Burrito 13 → 13,5.
4. **Birre**: in cassa la Helles è 20/40 cl, non 30/50. Corretto, e prezzi allineati alla cassa (Sogno Lucido 5,5/8, Leo Weiss 4,8/7).
5. **Vini rifatti sul venduto**. Il calice più venduto (Tyrsos) non era in carta. Il calice passa da 5 a 5,5.
6. **Sandwich Ribs aggiunto**: 141 pezzi in cassa, ma non era in carta.
7. **Amari dalla cassa**: entra il Jägermeister (65 pezzi), esce il Montenegro (17). Aggiunto il caffè.
8. **Menù fissi troppo scontati**: costavano il 21–28% in meno della somma della carta. Ora sono 24 / 31 / 37, con il prezzo pieno barrato (29 / 37 / 43). Il margine sale di circa 2,7 € a menù.
9. **Aggiunte**: tre sole, con foto tonda («La vuoi ancora più buona?»): bacon +2, cheddar +1,5, guanciale +2,5.
10. Il nome è scritto **Giurgés**, come nel logo. Indirizzo e telefono sono presi da piatti.menu e Instagram.

## Antipapa — libro A4, 8 facciate
1 copertina · 2 antipasti + maritozzi · 3 Experience · 4 paste · 5 secondi · 6 dolci + amari · 7 da bere + allergeni · 8 retro. Con 6 facciate non si può rilegare: ne servono 8, cioè due A3 piegati.

Cosa non tornava e ho corretto:
1. **Piatti estivi a ottobre**. Escono panzanella estiva, fiori di zucca e spaghettoni coi fichi. Entrano i maritozzi salati che la cassa vende già (porchettato 197 pezzi, alla fondana 136) e la calamarata al ragù di polpo.
2. **Dolci inventati**. «Dolce del giorno» e «tiramisù al cucchiaio» non esistono in cassa. I dolci veri sono il profiterole al tiramisù (329 pezzi) e i maritozzi dolci, tutti a 7.
3. **L'«amaro della casa» non esiste**: lista rifatta con gli amari della cassa (Erbes Izzi Gran Riserva è il più venduto).
4. **Ricette dello chef**:
   - il carpaccio è di **picanha**, non di manzo;
   - il tagliere **non ha la caciotta**;
   - nel brasato c'è anche il **cavolo nero**.
5. **Percorso → «Antipapa Experience»**: 58 a persona, con 64 barrato. La seconda portata ora è «antipasto di stagione», così la pagina vale tutto l'anno.
6. **Formati pasta**: +4 e +6 (erano +6 e +12), in un riquadro solo invece di ripeterli sotto ogni pasta.
7. **Focaccia calda a 3,5**, in evidenza sotto gli antipasti: con 2.298 pezzi è il prodotto n.1 del locale.
8. **Allergeni rinumerati** secondo la lista UE (1 glutine … 14 molluschi), con legenda completa a pagina 7.

## Da confermare con Luca prima della tipografia
1. Antipapa: i 3 **primi d'autore** (astice, ricciola, risotto al Cesanese) e i 3 **grandi secondi** (costata, filetto, ricciola) sono piatti nuovi della proposta di settembre. Lo chef li fa davvero?
2. Antipapa: gli allergeni sono stimati dalle ricette e vanno validati in cucina.
3. Giurgés: gli ingredienti di 30 CM, Cestino Goloso e Sandwich Ribs.
4. **Logo Antipapa vettoriale**: su Instagram c'è solo a 100 px. In copertina ho ridisegnato la «A».
5. Giurgés: coperto deciso da Marco a **2,50 €** (07/10), ma la cassa batte **SERVIZIO a 1 €**. Se lo battono a 2,50 sono circa **+15.000 €/anno**: è la leva più grande di tutte.
6. Le foto sono generate con ChatGPT e fanno da segnaposto: vanno sostituite con quelle vere dei piatti appena possibile.

