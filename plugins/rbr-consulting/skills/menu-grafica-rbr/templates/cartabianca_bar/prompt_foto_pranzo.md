# Foto del pranzo dei bar Cartabianca — prompt per ChatGPT (05/10/2026)

**Come si usa:** fate una foto vera del piatto in un bar (anche col telefono, a pranzo). In ChatGPT allegate la foto, incollate il prompt base e poi la riga del piatto. Salvate l'immagine col nome indicato in `data/cartabianca/carta_menu/bar/img/foto/`: entra da sola nella carta quando si rigenera (`python3 build_pranzo.py`).

Stesso stile delle carte di Tennis e Club: fatele tutte nella stessa chat, una dopo l'altra.

## Prompt base (da incollare sempre per primo)
> Fotografia professionale per il menu di un ristorante italiano di alto livello, stile Eataly. Usa la foto allegata come riferimento: mantieni ESATTAMENTE lo stesso piatto, gli stessi ingredienti, la stessa porzione e lo stesso piatto di servizio, non aggiungere e non togliere cibo. Piatto scontornato su sfondo bianco puro, appoggiato su una superficie di vetro bianco lucido con un riflesso morbido sotto. Luce naturale diffusa da sinistra, vista a 30 gradi, colori naturali e appetitosi, cibo a fuoco e nitido. Nessun testo, nessuna posata, nessun oggetto intorno. Formato orizzontale 4:3, alta risoluzione.

## Un prompt per ogni foto
| # | Dove va | Nome file | Da aggiungere al prompt base |
|---|---|---|---|
| 1 | La pasta (n.1) | `spaghettone_bottarga.png` | Spaghettone quadrato al burro con bottarga di muggine grattugiata sopra e scorza di limone, in un piatto fondo. |
| 2 | Insalate e freddi (n.1) | `crudo_bufala.png` | Piatto con fette sottili di prosciutto crudo, una mozzarella di bufala intera e rucola fresca. |
| 3 | I secondi (n.1) | `zuppetta_gamberetti.png` | Zuppetta di gamberetti in un sugo leggero di pomodoro, in una ciotola, con due crostoni di pane tostato appoggiati sul bordo. |
| 4 | Per finire (n.1) | `millefoglie.png` | Una monoporzione di millefoglie: strati di sfoglia croccante e crema chantilly, zucchero a velo sopra. Formato quadrato 1:1. |

## Aggiornamento 06/10 sera
Finché i 4 file non ci sono, nel riquadro del n.1 c'è un'illustrazione a tratto (`ILLU` in `build_pranzo.py`), mai la foto di un altro piatto.
Copertina: se arriva `img/foto/copertina_pranzo.png` sostituisce il disegno della tavola apparecchiata. Prompt da aggiungere al base:
> Vista dall'alto di un tavolo di legno chiaro apparecchiato per il pranzo: un piatto di spaghettone al burro e bottarga, un calice d'acqua, posate, un tovagliolo di lino crema. Luce naturale calda, atmosfera accogliente da bistrot italiano. Formato orizzontale 4:3.

