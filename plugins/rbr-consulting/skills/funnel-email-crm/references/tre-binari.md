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

## Regola della verità

Il messaggio automatico dice solo cose sempre vere; il pezzo specifico lo manda il titolare a mano
quando c'è davvero. Nominare un prodotto in automatico è pericoloso (la disponibilità dipende dal
fornitore): "è arrivata la Rubia Gallega" mandato a 30 persone è una bugia il giorno in cui non c'è.
Forma sicura: l'automatico parla del banco/della cucina e cita i prodotti come REPERTORIO, non come
stock del giorno. Stessa regola sui premi: non promettere "ti ho messo da parte X" in automatico,
promettere un GESTO ("dimmelo prima e il taglio te lo scelgo io") che è vero sempre.

Trucco che tiene viva l'automazione per anni: una riga `{{custom_values.novita_del_mese}}` dentro
l'email, che il titolare aggiorna in un punto solo senza entrare nel funnel.
