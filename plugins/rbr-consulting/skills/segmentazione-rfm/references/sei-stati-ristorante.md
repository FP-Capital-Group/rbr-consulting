# RFM per ristoranti: sei stati invece di 125 celle

*(contributo di Luciano Purpi, 2026-09-13 — metodo nato sul lavoro Barresi)*

Una matrice RFM 5×5×5 su un ristorante è sovradimensionata: 125 celle quasi tutte vuote, e
nessun ristoratore agisce su 125 segmenti. Serve una griglia piccola e azionabile: **sei stati**
con un nome che dice già cosa fare. Un contatto sta in UNO stato solo; il tag si **sostituisce**
(non si somma); chi cambia stato cambia trattamento la sera stessa.

## Gli stati
| Stato | Criterio (soglie = ipotesi da tarare) | Trattamento |
|---|---|---|
| **Non misurato** | zero visite registrate | Niente di automatico, una campagna sola a blocchi. Non è un segmento, è una lista: su un locale che ha appena acceso il gestionale è quasi tutto il database — va fatto passare per la porta almeno una volta |
| **Nuovo** | 1 visita, ultima ≤ 60 gg | Racconto completo + invito alla seconda visita **ENTRO 30 GIORNI** dalla prima, senza sconto (Roberto Falcon, Piano Marketing RBR v1.0, mossa 8 "riattivazioni per sempre"); l'offerta a sconto parte solo dal giorno 91, per restare compatibile col silenzio promozionale |
| **Abituale** | 2-3 visite, ultima ≤ 90 gg | Racconto, NIENTE offerte, un premio all'anno a sorpresa |
| **Affezionato** | 4+ visite, ultima ≤ 90 gg | Racconto + precedenza, due premi all'anno |
| **Abituale fermo** | 2+ visite, ultima 91-180 gg | **Qui stanno i soldi**: riaggancio in due tempi. Roberto: chi non viene da 90 giorni riceve un motivo concreto per tornare, non solo uno sconto (tempi del riaggancio: `funnel-email-crm/references/tre-binari.md`) |
| **Dormiente** | ultima 181-365 gg | Una sola offerta forte con scadenza vera, poi silenzio 6 mesi |
| **Perso** | ultima > 365 gg | Fuori dagli invii ricorrenti, solo le stagionali |

## Le soglie vanno tarate, e va detto al cliente
60/90/180/365 sono un'**ipotesi** ragionevole, non una misura: dipendono dal ritmo con cui si va
in quel tipo di locale (una steakhouse non è la pizzeria del venerdì). Taratura vera: a sei mesi
di gestionale si guarda l'**intervallo mediano fra prima e seconda visita** e si mette la soglia
dell'"abituale fermo" a circa **1,3 × quell'intervallo** (il punto in cui uno che di solito sarebbe
già tornato non è tornato). Finché quel dato non c'è, chiamale ipotesi anche nel documento che
consegni.

## L'asse dei soldi quando lo scontrino non c'è: i coperti
Nella quasi totalità dei locali la M non esiste: lo scontrino per cliente si ha solo da chi
riscatta un QR, cioè quasi nessuno. Il sostituto che c'è SEMPRE sono **i coperti**, che il
gestionale prenotazioni registra su ogni riga (un tavolo da sei vale il doppio di un tavolo da
due). Si usa come **bandierina dentro lo stato**, non come terza dimensione di un cubo: chi porta
in media 4+ persone riceve, al posto dell'offerta standard, quella costruita per lui (l'antipasto
per il tavolo, il menu di gruppo).

## Il tetto che nessun software supera (dirlo PRIMA di promettere)
Su Barresi 75 visite su 162 non avevano né telefono né email (walk-in segnati al volo,
prenotazioni prese a voce): **il 46% della sala era invisibile al CRM**. La griglia vede solo la
metà della sala che si è lasciata riconoscere. La leva non è tecnologica: è **chiedere il
contatto al tavolo**, e il QR di riscatto serve anche a questo perché dà al cliente un motivo per
lasciarlo. Ogni punto recuperato lì vale più di qualunque raffinamento della matrice.

## Completare l'anagrafica
Costa poco se lo fanno la sala o il cliente stesso.
1. Quando qualcuno prenota per un compleanno, chi risponde chiede la data (giorno e mese) e, già
   che c'è, controlla e aggiorna il cellulare: è il modo più economico per completare l'anagrafica,
   e il telefono giusto è anche la chiave che aggancia le visite al contatto (senza telefono un
   contatto non è agganciabile).
2. Il modulo d'iscrizione alla fidelity fa lo stesso lavoro da solo: con `contacts/upsert` GHL
   riconosce il contatto dal telefono e lo aggiorna invece di duplicarlo, quindi un cliente storico
   che si iscrive corregge nome/cognome/email (anche storpiati dall'assistente telefonico) e
   aggiunge il compleanno. La mail di compleanno a chi ha solo il mese può chiedere il giorno
   esatto col link al modulo, svuotando da sola la lista "solo mese".

⚠️ Nell'upsert ogni campo passato sovrascrive: mai passare `tags` (si aggiungono dopo con
`POST /contacts/{id}/tags`), mai passare contatori o saldi (si leggono prima e si scrivono solo se
mancano).

È una pratica di sala, non ancora un risultato misurato: quanti compleanni/telefoni recupera non è
stato ancora contato. *(contributo di Andrea Chirivì, 2026-10-12)*

## Ordine di lavoro
1. Collaudo di quello che esiste.
1-bis. **Stato ereditato = fotografia ferma.** Un database importato da un sistema precedente (Pienissimo, Cooperto, Keap, Excel) porta presenze, data dell'ultima presenza e tag di stato (inattivo, prima volta, già cliente) fermi al giorno dell'import, e nessun motore li aggiorna. Prima di qualunque riattivazione si incrociano quei tag con le visite registrate DOPO l'import (gestionale prenotazioni, stato arrivato). Caso reale: 339 contatti su 905 arrivati dopo l'import erano ancora segnati "inattivo" — una riattivazione avrebbe scritto "ci manchi" a gente venuta poche settimane prima. La pulizia si fa **una volta sola**: si agganciano per telefono (normalizzato +39) le prenotazioni arrivate, le presenze diventano il valore importato più le visite successive all'ultima presenza registrata, la data dell'ultima presenza diventa l'ultima visita (formato ISO — normalizza i formati misti), e sui tag si toglie inattivo/prima volta e si mette già cliente. Anteprima CSV mostrata e confermata prima, log riga per riga per il rollback. Subito dopo si accende il motore che tiene vivo lo stato (trigger sul cambio del campo di stato + timer che rimette inattivo dopo N giorni), prima che lo stato ripulito invecchi di nuovo. Le presenze contano solo le visite registrate: i walk-in non entrano (vedi "Il tetto che nessun software supera", sopra).
2. Il **ponte gestionale → CRM** coi quattro dati di visita (data ultima visita, numero visite,
   media coperti, esito ultima prenotazione). È il pezzo che sblocca tutto e di solito dipende da
   terzi: chiedilo per primo, scritto preciso.
3. Il flusso giornaliero che assegna lo stato.
4. La guardia in testa alla catenaria.
5. Il riaggancio.
6. Il contatto al tavolo (lavoro di sala, non di software).

## Se il ponte non arriva
Si può accendere lo stesso, purché il trigger sia **"tag aggiunto"**: entrano solo le
prenotazioni nuove, nessuno dello storico. Il primo momento in cui il freno mancante fa danno vero
è la **seconda promozione** (con cadenza settimanale e promo ogni 4ª: il giorno 35), e solo per
chi nel frattempo è già tornato. Quindi si accende **con una data di scadenza scritta**: se a
quella data il freno non c'è, il funnel va in pausa (chi è a metà catena si ferma e riprende
dopo). È reversibile, e il costo di restare spenti è certo mentre quello del freno mancante è
probabile e lontano. Metti un promemoria automatico per quella data, non un post-it.
