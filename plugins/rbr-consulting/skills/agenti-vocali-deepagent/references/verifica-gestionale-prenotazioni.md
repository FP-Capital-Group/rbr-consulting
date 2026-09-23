# Verifica del gestionale prenotazioni (Resmio)

**Da fare prima di scrivere il prompt.** L'agente non decide se c'è posto: lo
chiede al gestionale. Se il gestionale è configurato male, l'agente risponde
"non c'è posto" a ogni chiamata e sembra rotto lui.

Su Red Mike il gestionale diceva **14:00–22:00, sei giorni su sette**, mentre il
locale era aperto **tutti i giorni 19:00–24:00**, e per giunta c'era una
chiusura programmata di due settimane. Con quella configurazione nessuna
prenotazione sarebbe mai passata.

## Lettura veloce senza login

La scheda pubblica del locale si legge così:

```
https://app.resmio.com/v1/facility/<slug>
```

Restituisce JSON. I campi che contano subito: `name`, `slug`, `city`, `phone`,
`timezone`, `booking_enabled`, `opening_hours` (con `begins`, `ends`,
`capacity`, `weekdays`). Serve anche a **confermare lo slug** del locale, che è
il valore da mettere nel prompt per lo smistamento delle prenotazioni.

`weekdays` va da 0 a 6: se ne mancano, un giorno della settimana non è
prenotabile. Sette valori = tutti i giorni.

## I sei controlli

Nel pannello: `Impostazioni → Prenotazioni → Orari` e `→ Prenotazioni online`.

1. **Orari e capacità di prenotazione** — la fascia deve coincidere con gli
   orari in cui il locale accetta prenotazioni, e i giorni devono esserci
   tutti. È la riga tipo `LUN - DOM | 19:00 - 23:30 | 28`.

2. **Capacità per fascia** — quante persone possono essere prenotate in ogni
   intervallo. Va letta **insieme** alla durata della prenotazione: con durata
   90 minuti una capacità di 28 significa "28 coperti seduti insieme", non 28
   ogni intervallo. Una capacità troppo bassa fa dire "non c'è posto" con la
   sala vuota; troppo alta fa accettare più gente di quanta ne entri.

3. **Intervallo di prenotazione** — 15 o 30 minuti. Determina i passi degli
   orari proposti **e** l'unità su cui si conta la capacità.

4. **Durata della prenotazione** — quanto a lungo un tavolo resta occupato.
   Senza questo valore la capacità non ha senso.

5. **Vacanze ed eccezioni** — cerca chiusure programmate. Una riga "Chiuso" che
   copre le prossime settimane azzera la disponibilità e non lascia traccia
   negli orari. **Non cancellarla di tua iniziativa**: chiedi se il locale è
   davvero chiuso in quel periodo.

6. **Limiti dell'ora di punta** — un cap di ingressi per intervallo, con una
   sua finestra oraria indipendente. Quando si cambiano gli orari del locale
   questa finestra **resta quella vecchia**: riallineala o toglila.

## Coerenza con il prompt

Tre valori devono coincidere fra gestionale e prompt, o l'agente promette cose
che il sistema rifiuta:

| | Gestionale | Prompt |
|---|---|---|
| Fascia prenotabile | Orari di prenotazione | `{{ORARI_PRENOTAZIONE}}`, fase 2 |
| Giorni | `weekdays` | `{{ORARI_APERTURA}}` |
| Soglia gruppo | auto-conferma fino a N | `{{SOGLIA_GRUPPO}}` |

L'auto-conferma allineata alla soglia dell'agente è la configurazione giusta:
tutto ciò che l'agente prenota da solo risulta confermato, e ciò che supera la
soglia passa all'operatore.

## Attenzione alla mappa dei tavoli

Se il locale attiva l'organizzazione dei tavoli, la capacità **smette** di
venire dal numero impostato e viene calcolata dalle dimensioni dei tavoli.
L'agente vede disponibilità diverse da un giorno all'altro senza che nessuno
abbia toccato il prompt: dopo quel cambio, rifai il collaudo.

## Link diretto al widget

Per far prenotare online senza passare dal sito del locale (utile se il sito ha
popup o offerte che sporcano il percorso):

```
https://app.resmio.com/<slug>/widget
```

Con `?source=<canale>` il valore finisce nella prenotazione e permette di
attribuire il canale (whatsapp, instagram, menu-qr...).
