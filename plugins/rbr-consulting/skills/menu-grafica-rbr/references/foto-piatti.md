# Foto dei piatti

## Gerarchia
1. **Foto vere del cliente** (fotografo/agenzia, originali ad alta risoluzione). Instagram va bene per la
   bozza ma è a 360-640 px: per la stampa servono gli originali.
2. **Foto generate su ChatGPT partendo dalla foto VERA del piatto** (telefono/cucina), stesso piatto,
   stessi ingredienti, stessa porzione. Tutte nella stessa chat per avere lo stesso stile.
3. Se manca: impagina senza foto, oppure illustrazione fine line monocolore. **Mai la foto di un altro
   piatto, mai stock, mai riquadro "FOTO" in stampa.** Elenco "foto da fare" nella consegna.

⚠️ I titolari diffidano delle foto AI "inventate" (Salvo a Luna Blu dopo la call 09/10; scottona
Cartabianca bocciata finché non rifatta da foto vera; Giurgés: tolte tutte le ChatGPT il 07/10).
Aggiunte e impasti (ingredienti singoli) possono restare generati. Per i piatti veri dai al cliente le
istruzioni per la foto col telefono: porzione vera, luce di finestra, una dall'alto e una a 45°, il tavolo
del locale come sfondo.

Marco non vuole servizi a pagamento (Gemini scartato): ChatGPT sul suo account + strumenti locali gratis.

## Prompt base (stile Eataly, Cartabianca)
> Fotografia professionale per il menu di un ristorante italiano di alto livello, stile Eataly. Usa la foto
> allegata come riferimento: mantieni ESATTAMENTE lo stesso piatto, gli stessi ingredienti, la stessa porzione
> e lo stesso piatto di servizio, non aggiungere e non togliere cibo. Piatto scontornato su sfondo bianco
> puro, appoggiato su una superficie di vetro bianco lucido con un riflesso morbido sotto. Luce naturale
> diffusa da sinistra, vista a 30 gradi, colori naturali e appetitosi, cibo a fuoco e nitido. Nessun testo,
> nessuna posata, nessun oggetto intorno. Formato orizzontale 4:3, alta risoluzione.

Poi una riga per piatto con ingredienti precisi e cosa NON mettere (es. "NON carpaccio a fette, NON rucola").
Aggiunte: "Solo un tartufo nero intero con due lamelle… formato quadrato 1:1". Prompt completi:
`templates/cartabianca_ristoranti/prompt_foto_chatgpt.md`, `templates/cartabianca_bar/prompt_foto_pranzo.md`.

**Variante trasparente (Luna Blu)**: "…food photography per il menu di una pizzeria storica di Parma…
dall'alto leggermente inclinata… luce naturale morbida. Sfondo TRASPARENTE (PNG scontornato, nessun tavolo,
nessuna ombra)… 1024×1024… niente testo". A volte ChatGPT disegna una finta scacchiera: rigenerare
(o `prep_foto.py` la scontorna con rembg se il PNG non ha canale alfa).

Illustrazione elegante approvata: "disegno botanico minimale a linea sottile… un unico lungo ramo d'ulivo…
un solo colore bordeaux #8A1C2B su sfondo trasparente… entra dal bordo sinistro…". Incisione vintage piena = bocciata.

## Recuperare le immagini da ChatGPT (Chrome)
Chrome blocca i download multipli e la CSP blocca server localhost. Funziona:
- "Copia immagine" (o bottone iniettato che chiama `navigator.clipboard.write` su click reale) +
  `scripts/clip.sh <nome>` → salva gli appunti con `osascript … «class PNGf»` in `img/originali/<nome>.png`.
- Oppure download via blob → `~/Downloads/menu_<nome>.png` → `scripts/prep_foto.py` le sposta e scontorna.
- Immagini vecchie: `chatgpt.com/library?tab=images`.

## Scontorno
- **rembg** (gratis, locale): `tools/.venv_rembg/bin/python scripts/scontorna_foto.py foto.jpg out.png [--quadrata] [--senza-riflesso]`
  → piatto su bianco con ombra e riflesso "su vetro". Modello **birefnet-general** (l'unico che regge piatti
  bianchi su fondo bianco); `isnet-general-use` sbaglia sul bianco. Serve margine intorno al piatto.
  Ambiente: Python 3.12 via `uv` (con 3.14 non si installa), modello in `~/.rembg/models`.
- **Solo PIL** (se manca rembg): maschera pixel chiari poco saturi (`min≥190, max−min<16`) → `floodfill` dai
  bordi su una `.copy()` (senza copia non funziona) → `MinFilter(5)` + `GaussianBlur(1.4)`. Piatti tondi
  difficili: maschera a cerchio (`R=W*0.478`) o inviluppo convesso.
- **Piatti bianchi su pagina chiara**: rembg/flood-fill mangiano la ciotola → foto su bianco "moltiplicata"
  per il colore pagina (#FFFDF9) oppure maschera ellittica su PNG trasparente. Se la pagina è #FFFFFF niente moltiplica.
- Aggiunte: tondo pieno ritagliato quadrato 600-700 px, niente scontorno.
- Verifica lo scontorno su fondo scuro/colorato prima di impaginare ("scontorni fatti a caso" = bocciati).

## Formati file
- webp qualità 86: 900×900 px piatti, 420 px aggiunte/impasti; in pagina `object-fit:contain`, niente bordo/fondo.
- Negli artifact in base64 (limite 16 MB → usa webp).
- Accostamenti credibili (no gamberi + pistacchio se non è la ricetta).

