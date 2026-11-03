# Il denominatore vero del costo per prenotazione

(contributo di Luciano Purpi, 2026-09-03) Tutti i numeri sono misurati su un locale
stagionale ad agosto 2026, mese chiuso: 2.420 prenotazioni, 8.430 coperti.

## 1. Ogni attribuzione è un pavimento, mai una misura
- Il campo `source` di Resmio copriva il 38%: 1.500 prenotazioni su 2.420 l'avevano vuoto.
- Walk-in = 44% delle righe (3.519 coperti).
- L'agente vocale aveva fatto 170 prenotazioni, TUTTE senza source.
- La provenienza vera si ricostruisce incrociando `source` + `comment`/`notes` (+
  `booking_request_parameters` dove c'è `gclid`/`utm`). Nel report al cliente si dichiara la
  quota non attribuita invece di farla sparire.

**Schema di raggruppamento delle fonti Resmio** (contributo di Andrea Chirivì, 2026-10-12):
sala/cassa (source vuoto + "resmio Tables" + `app.resmio.com`) · telefono · sito (tutti i
codici) · TheFork · pulsante sui profili IG/FB · Google gratis (`google_maps` + `GoogleCTA`) ·
mail/CRM. Su un caso reale il 50,3% dei coperti prenotava parlando con una persona, senza
provenienza: la pubblicità riconosciuta (7,3%) è un pavimento, perché chi telefona dopo aver
visto l'annuncio non porta con sé il canale.

## 2. Il CPA si calcola sulle onorate
No-show (128) e cancellate (203) = 17-20% del totale, concentrate su TheFork (10,2%) e
agente vocale (14,1%). Consuntivo del mese:

| Canale | Spesa | Prenotazioni | Onorate | CPA (onorate) | ROAS | Margine netto |
|---|---|---|---|---|---|---|
| Google | 2.366 € | 96 | 69 | 34,30 € | 1,51 | +127 € |
| Meta | 1.912 € | 15 | 9 | 212 € | 0,24 | −1.587 € |

## 3. Prima di scalare si misura il marginale, non il medio
Il 13 agosto i budget Google sono saliti del 56% (clic +70%): prenotazioni Google +15%, Meta
−5%, mentre il totale del locale cresceva del 45% da solo. CPA marginale della spesa
aggiuntiva ≈ 74 € contro 24,65 € medio. Regola: confronta periodo prima/dopo l'aumento, isola
la crescita spontanea del locale, calcola (Δ spesa) ÷ (Δ prenotazioni onorate del canale).

## 4. La pubblicità segue la domanda
Correlazioni sui 30 giorni: r(spesa Google, prenotazioni Google) = 0,03; r(spesa Meta,
prenotazioni Meta) = −0,04; mentre i canali non pagati correlano tutti col totale (TheFork
0,66, agente vocale 0,63, sito 0,55). Metodo onesto: due soli livelli di spesa e un mese di
piena stagionalità → indizio convergente, non prova causale. Ma cambia la conversazione col
cliente sul budget: in alta stagione una parte delle prenotazioni "da ads" sarebbe arrivata
comunque.

## 5. Due trappole operative dallo stesso caso
- **Stesso URL per tutte le inserzioni** → attribuzione per annuncio azzerata (6 annunci su 8
  da un mese all'altro). Ogni annuncio col suo `?utm=<landing>-<canale>`.
- **Obiettivo Meta "Traffico"** compra clic, non tavoli: 23.017 clic a 0,08 € per 15
  prenotazioni.

## 6. Il costo a coperto seduto (contributo di Andrea Chirivì, 2026-10-12)
Il CPA sulle onorate non basta a confrontare canali che riempiono tavolate di taglia diversa:
accanto va sempre il **costo a coperto seduto**.

**Calcolo**: spesa del canale ÷ prenotazioni Resmio con quella `source` (contate per data di
**creazione**, walk-in esclusi) = costo a prenotazione; costo a prenotazione ÷ tasso di onorate
= costo a onorata; spesa del canale ÷ coperti seduti delle onorate = **costo a coperto**.

Esempio reale (Noolas, due finestre diverse — da citare sempre col periodo, mai mescolate):
- 9/9-8/10: Google 12,10 € a onorata ma 2,78 € a coperto; eventi 12,82 € a coperto.
- 4/9-3/10: Google 688,71 € → 83 prenotazioni, 66 onorate, 298 coperti = 10,43 € a onorata e
  2,31 € a coperto. Meta 2x1 12,69 € e 5,97 € a coperto; Meta eventi 24,38 € e 6,80 € a coperto.

Sono **pavimenti**: si dichiarano le prenotazioni senza fonte (in un caso 193 su 829). Sugli
eventi una quota alta di prenotazioni viene annullata (vista anche al 37% in un caso): si
calcola sempre sulle onorate. Nel filtrare le prove dal dataset, escludi solo i nomi esatti —
un filtro troppo largo (es. ogni riga che inizia per "test") può buttare via anche dati veri
(es. "testata-*").
