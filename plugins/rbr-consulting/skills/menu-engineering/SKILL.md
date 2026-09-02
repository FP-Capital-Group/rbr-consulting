---
name: menu-engineering
description: >-
  Metodo RBR di menu engineering — dai dati di vendita al menu grafico stampabile. Usala ogni volta che devi analizzare o rifare il menu di un ristorante cliente: "facciamo menu engineering", "analizza il menu di X", "quali piatti tenere/togliere", "rifammi il menu in PDF", "come posiziono i piatti", "revisione prezzi menu". Applica i 5 pilastri + matrice Kasavana-Smith (Star/Plowhorse/Puzzle/Dog), produce raccomandazioni di riposizionamento/pricing/design e genera il menu grafico professionale (PDF weasyprint+Jinja2, upload Drive). NON ridisegnare mai un menu senza aver prima classificato i piatti con questa skill.
---

# Menu engineering (dati → decisioni → menu grafico)

## Perché esiste
Il menu è lo strumento di vendita più letto del ristorante e quasi nessun ristoratore lo progetta con metodo. In RBR il menu si tratta come un asset economico: ogni piatto ha un margine e una popolarità, e la posizione/descrizione/prezzo si decidono sui numeri, non a occhio. Questa skill porta dal dato grezzo di vendita fino al PDF stampabile, passando per una classificazione oggettiva. La regola RBR: **prima classifichi i piatti, poi decidi il layout.** Un menu "bello" che spinge un Plowhorse nello sweet spot fa perdere soldi.

## Quando usarla
- Un cliente vuole rivedere, tagliare o ridisegnare il menu.
- Hai i dati di vendita (unità vendute) e i food cost e vuoi capire cosa tenere/spingere/togliere.
- Devi produrre un menu grafico professionale pronto per stampa o digitale.
- Il cliente lamenta margini bassi o "vendo solo i piatti che rendono poco".

## Prerequisiti
- Per ogni piatto: **nome, categoria, prezzo di vendita, food cost (€ o %), unità vendute** nel periodo (min 1 mese, meglio 3).
- Se manca il food cost o le unità vendute → classificazione non affidabile: raccoglili prima (vedi skill `riconciliazione-dati-cliente` per validare i dati).
- Stile del cliente: riferimento visivo, URL sito, screenshot o PDF di un menu esistente.
- Per l'output PDF: stack agente Alex (`agents/alex/`, weasyprint+Jinja2+Drive). API key e credenziali Drive stanno nel `.env` dell'agente, mai nel repo.

## Procedura

### 1. Prepara la matrice
Per ogni piatto calcola:
- **Margine di contribuzione** = prezzo (IVA esclusa) − food cost. Regola RBR: economici sempre IVA esclusa (÷1.1 ristorazione).
- **Popolarità** = unità vendute del piatto ÷ unità totali della categoria.
Confronta ogni piatto con le due mediane della sua categoria: sopra/sotto la mediana margine e sopra/sotto la mediana popolarità.

### 2. Classifica con Kasavana-Smith
| Quadrante | Popolarità | Margine | Cosa fare |
|-----------|-----------|---------|-----------|
| ⭐ STAR | Alta | Alto | Sweet spot, proteggi, non toccare prezzo né ricetta |
| 🐴 PLOWHORSE | Alta | Basso | Togli dallo sweet spot, riduci porzione o alza prezzo 2-3%, abbina add-on |
| 🧩 PUZZLE | Bassa | Alto | Promuovi: foto, descrizione ricca, sweet spot, box/callout |
| 🐕 DOG | Bassa | Basso | Elimina o nascondi in zona morta del menu |

### 3. Applica i 5 pilastri
1. **Limita la scelta** — max 7 piatti/categoria (Miller 7±2; studio marmellata: 6 opzioni convertono 10× di 24). Elimina i Dog, crea sotto-categorie se serve.
2. **Metti tutto al posto giusto** — Star e Puzzle negli sweet spot (variano per formato, vedi sotto). Primo e ultimo piatto della lista = più ricordati (primacy/recency) → mettici alto margine.
3. **Fai tornare i conti** — prezzi senza simbolo €, inline dopo la descrizione (mai colonna allineata a destra), no `.99` sui livelli medio-alti, anchor pricing (piatto costoso in cima alla sezione).
4. **Cura l'estetica** — max 1-2 foto/pagina (solo professionali, +30% vendite), max 3 colori e 2 font, white space attorno ai premium, max 2-3 box/callout per pagina.
5. **Emoziona** — nomi descrittivi (+27% vendite, Wansink 2001) e descrizioni sensoriali sui piatti da spingere, così l'attenzione va sul piatto e non sul prezzo.

**Sweet spot per formato:** pagina singola → centro-alto; bifold → metà alta pagina destra (Golden Triangle); trifold → pannello centrale; libro → prime 2 pagine (80% attenzione).

### 4. Scrivi le raccomandazioni
Produci un documento con, per ogni piatto: quadrante, azione consigliata, motivazione numerica. Elenca separatamente: piatti da togliere, prezzi da ritoccare (con nuovo prezzo proposto), piatti da promuovere e dove posizionarli. Numera le decisioni aperte da discutere col cliente.

### 5. Genera il menu grafico
Passa i dati all'agente Alex nel formato `menu_data` (`nome_ristorante`, `categorie[]` con `piatti[]` → `nome/descrizione/prezzo/nota`) + `style_config` (colori, font, layout, formato). Vedi `agents/alex/CLAUDE.md`.
- Estrai il brand del cliente da sito/screenshot/PDF (`brand_extractor`) o imposta i colori a mano.
- Scegli colori/font per tipo di locale (pizzeria: rosso+bianco+verde; fine dining: nero+oro; trattoria: marrone+crema…). Max 2 font, mai 2 serif insieme.
- `build_menu(menu_data, style)` → PDF; `build_menu_all(...)` → PDF + IDML editabile.
- `upload_to_drive(pdf, folder_id)` → link nella cartella cliente. Condividi come da baseline RBR.

## Regole RBR & trabocchetti
- ⚠️ Mediane **per categoria**, non sull'intero menu: un antipasto e un secondo non si confrontano.
- ⚠️ Food cost mancante = margine inventato. Non classificare a occhio, chiedi i dati.
- ⚠️ Non spingere mai un Plowhorse nello sweet spot: alza i volumi del piatto che rende meno.
- ⚠️ Prezzi economici sempre IVA esclusa; se la fonte non lo specifica assumi esclusa e segnala 🟡.
- ✅ Un menu ideale RBR: 5-7 categorie × 5-7 piatti, 2-3 Puzzle promossi, Dog eliminati, anchor in cima ad ogni sezione.
- ❌ Mai `.99`, mai simbolo €, mai colonna prezzi allineata a destra.
- Segreti/token → sempre dal `.env` dell'agente, mai scritti qui (repo condivisa col team).

## Definition of Done
- [ ] Ogni piatto ha margine di contribuzione e popolarità calcolati per categoria
- [ ] Ogni piatto classificato Star/Plowhorse/Puzzle/Dog contro le mediane di categoria
- [ ] Raccomandazioni scritte con azione + motivazione numerica per piatto
- [ ] Decisioni aperte (tagli, ritocchi prezzo) numerate e discusse col cliente
- [ ] 5 pilastri applicati al layout (scelta, posizione, prezzi, estetica, nomi)
- [ ] Menu grafico generato (PDF, eventuale IDML), caricato su Drive e condiviso
