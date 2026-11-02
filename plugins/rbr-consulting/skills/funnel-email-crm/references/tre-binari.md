# Catenaria a tre binari: la promozione non è un premio per chi viene

(contributo di Luciano Purpi, 13/09/2026)

Variante da usare quando il CRM conosce le visite del contatto (data ultima visita, numero visite:
vedi skill `onboarding-cliente-ghl`, `references/modello-base-locale.md`). Senza quei dati resta il
funnel lineare a 57 mail della SKILL.md.

## La regola

La promozione non è un premio per chi viene, è uno strumento per chi non viene. Uno sconto a un
cliente affezionato gli fa pagare meno una cena che avrebbe pagato intera E gli insegna ad aspettare
l'offerta: due danni al prezzo di uno. Chi è venuto da poco riceve racconto SÌ / offerte NO; chi si
è fermato riceve entrambi.

## Montaggio: tre flussi separati, non un flusso con condizioni

1. **RACCONTO** — a tutti, sempre, mai sconti.
2. **PREMIO** — a chi viene, mai uno sconto: deve essere una COSA (il taglio scelto e messo da parte,
   il calice, l'assaggio del pezzo nuovo, la precedenza), perché una percentuale ha un prezzo
   confrontabile in testa al cliente, una cosa no. E non deve essere prevedibile (alla 5a visita, il
   primo del mese): va agganciato a un fatto vero, o in tre giri diventa un diritto.
   **Innesco**: sul CONTATORE visite (es. "campo visite_totali modificato in 5"), con rientro OFF
   (una volta sola) — agganciato al contatore e non allo stato più una condizione sul numero, così
   il valore è già scritto quando il flusso parte e non c'è corsa fra due eventi. Attesa di 1 giorno
   dentro la finestra lun-sab 11-19 (mai la domenica, mai mentre il cliente è a tavola), poi
   WhatsApp "premio" e tag `premio-inviato`. **Il testo non nomina mai il numero di visite**: il
   premio non deve sembrare una raccolta punti (es. "ti scrivo perché ti conosciamo… la prossima
   volta dimmelo prima e te lo metto da parte io. Non è un'offerta e non scade."). Il contatore
   visite parte da zero il giorno in cui si accende e non conta lo storico, a meno di una pulizia
   una tantum via API con anteprima prima di applicarla — va detto al titolare prima che lo chieda.
   *(contributo di Luciano Purpi, 2026-10-12)*
3. **RIAGGANCIO** — a chi si è fermato, l'unico binario che può contenere offerte.

Perché separati davvero: in GHL la catena è lineare, per saltare un nodo servono condizione + "Vai a"
= 2 nodi per ogni promo (su 28 email con 7 promo sono 14 nodi in più in un builder fragile).
Separare costa mezza giornata una volta sola; poi le offerte si accendono, spengono e contano in un
punto solo.

## I due tetti e il freno

- Max **3 gesti all'anno a persona**, di cui al massimo **1 sconto**.
- Freno anti-cliente-da-sconto: due contatori per persona (visite entro 2 settimane da una promo /
  visite spontanee). Dopo 3 ritorni di fila tutti agganciati a promo e zero spontanei, la persona
  esce dalla rotazione offerte per 12 mesi (le restano racconto e stagionali). Se torna da sola, il
  contatore si azzera.

## Tempi

- Il silenzio promozionale dura **90 giorni** e parte dalla VISITA (non dalla promo): vale uguale se
  è rientrato con l'offerta o da solo.
- Riaggancio in due tempi: **giorno 91** un MOTIVO senza sconto, **giorno ~110** l'offerta solo se non
  si è mosso. Chi torna al primo colpo non è costato niente ed è la metà migliore.
- **Giorno di invio: giovedì alle 11:30**, non venerdì. Il venerdì la casella è piena di ristoranti; il
  giovedì sei quasi solo, chi legge può prenotare sia per venerdì che per sabato, e la sala sistema
  meglio una prenotazione con un giorno di margine. (Come impostare l'attesa in GHL: skill
  `mail-funnel-ghl`, `references/builder-ghl.md`.)
- La stessa regola dell'orario vale a due livelli diversi: **giovedì 18:00** per newsletter/lancio
  a tutta la lista (sotto), **giovedì 11:30** per il riaggancio automatico al singolo contatto (qui
  sopra) — non vanno confusi.

## Montaggio in GHL (verificato su clienti veri)

- **Timer dello stato**: tag `stato-attivo` (rientro ON) → attendi 90 giorni → togli `stato-attivo`
  e metti `stato-abituale-fermo`. Ogni nuova visita toglie il contatto dal timer e rimette il tag
  `stato-attivo`.
- **Riaggancio**: trigger tag `stato-abituale-fermo` (rientro ON) → attendi giovedì 11:30 → guardia
  "è ancora fermo?" (il tag `stato-abituale-fermo` c'è ancora) → mail con un motivo, senza sconto →
  attendi 19 giorni → guardia "è tornato?" (tag `stato-attivo`) → se no, mail con l'offerta (intorno
  al giorno 110). **Perché serve la prima guardia**: fra il tag e il giovedì passano fino a 6 giorni
  — se nel frattempo il cliente ha già prenotato, la mail col motivo non deve partire lo stesso.
- Concentrare gli invii in un solo giorno/orario va bene per l'**email**. Su **WhatsApp** gli invii
  vanno spalmati a ondate, non tutti insieme (stessa regola del controllo settimanale Make/GHL).
- `{{custom_values.novita_del_mese}}` (vedi sotto) è un valore **facoltativo**: il testo deve reggere
  anche se è vuoto, senza riquadri o frasi a metà. Il flusso che lo usa non parte finché il titolare
  non lo riempie la prima volta.
*(contributo di Luciano Purpi — montaggio verificato su clienti RBR, 2026-10-12)*

## Invii a tutta la lista: newsletter settimanale

La newsletter settimanale è la forma concreta del binario RACCONTO, finora solo un principio
("a tutti, sempre, mai sconti"):

- Una mail a settimana, sempre, a tutta la lista con consenso marketing.
- Un'idea sola per mail: il processo, l'ingrediente, la persona, il territorio o il premio. Apre
  con la promessa (vedi SKILL.md, Regola della promessa d'oro) e non contiene sconti.
- Chiude sempre con l'invito a iscriversi alla fidelity e a ritirare il regalo di benvenuto.
- Vale la regola della verità qui sotto: i prodotti si citano come repertorio, mai come
  disponibilità del giorno.
- **Motivo**: senza le settimanali il lancio promozionale arriva su una lista fredda e rende la
  metà. Un'offerta mandata da sola parla di prezzo, e chi risponde al prezzo torna solo per il
  prezzo.
- Orario: **giovedì alle 18:00**, a tutta la lista (diverso dal giovedì 11:30 del riaggancio al
  singolo contatto, sopra).

⚠️ **Il lancio mensile con offerta a tutta la lista (mossa 9 del Piano Marketing di Roberto) NON è
ancora stato integrato**: confligge con i tetti di questa skill (max 3 gesti/anno a persona, di cui
1 solo sconto; silenzio 90 giorni; offerte solo a chi si è fermato). Va deciso con Roberto e
Luciano come conciliarlo prima di scriverlo come regola — non è una decisione che si può prendere
da soli compilando questo file.
*(contributo di Roberto/RBR — Piano Marketing RBR v1.0, mossa 9, settembre 2026)*

## Regola della verità

Il messaggio automatico dice solo cose sempre vere; il pezzo specifico lo manda il titolare a mano
quando c'è davvero. Nominare un prodotto in automatico è pericoloso (la disponibilità dipende dal
fornitore): "è arrivata la Rubia Gallega" mandato a 30 persone è una bugia il giorno in cui non c'è.
Forma sicura: l'automatico parla del banco/della cucina e cita i prodotti come REPERTORIO, non come
stock del giorno. Stessa regola sui premi: non promettere "ti ho messo da parte X" in automatico,
promettere un GESTO ("dimmelo prima e il taglio te lo scelgo io") che è vero sempre.

Trucco che tiene viva l'automazione per anni: una riga `{{custom_values.novita_del_mese}}` dentro
l'email, che il titolare aggiorna in un punto solo senza entrare nel funnel.
