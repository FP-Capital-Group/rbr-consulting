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
| **Nuovo** | 1 visita, ultima ≤ 60 gg | Racconto completo + promo della seconda visita |
| **Abituale** | 2-3 visite, ultima ≤ 90 gg | Racconto, NIENTE offerte, un premio all'anno a sorpresa |
| **Affezionato** | 4+ visite, ultima ≤ 90 gg | Racconto + precedenza, due premi all'anno |
| **Abituale fermo** | 2+ visite, ultima 91-180 gg | **Qui stanno i soldi**: riaggancio in due tempi |
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

## Ordine di lavoro
1. Collaudo di quello che esiste.
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
