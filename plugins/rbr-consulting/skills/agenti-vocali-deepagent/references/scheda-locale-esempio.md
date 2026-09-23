# Scheda locale compilata — Red Mike (Alghero)

Esempio reale, messo in produzione il 20 agosto 2026 (numeri di telefono e id oscurati). Usalo come modello:
compila la stessa scheda per ogni locale nuovo **prima** di scrivere il prompt.

## Il locale

| Voce | Valore |
|---|---|
| Nome | Red Mike |
| Concept | pizza, burger e grill ad Alghero |
| Indirizzo | Via Galileo Galilei 4/6, Alghero (SS) |
| Apertura | tutti i giorni 19:00–24:00 |
| Turni prenotabili | solo cena, 19:00–23:30 |
| Soglia gruppo | 8 coperti (oltre → operatore) |
| Casi da girare subito | asporto, consegne a domicilio, eventi e feste private, modifiche a prenotazioni esistenti |
| Note menù | antipasti, pizze, grill, burger, contorni, dolci, birre e vini |
| Zona turistica | sì → blocco `language_handling` indispensabile |

## I numeri — tre, e vanno tenuti distinti

| Ruolo | Numero | Note |
|---|---|---|
| Pubblico, dove chiamano i clienti | **+39 3xx xxx xxxx** | va deviato su quello DeepAgent |
| DeepAgent, dove risponde l'agente | **+39 055 xxx xxxx** | non si pubblica |
| Operatore, per il trasferimento | **+39 3xx xxx xxxx** (cellulare del referente) | reperibile 10:00–24:00 |

Il fisso del locale che sta su iPratico e sul profilo Google **non** è
quello su cui arrivano le chiamate: non usarlo nel prompt.

Il primo numero DeepAgent scelto (prefisso 0881) è risultato
**inutilizzabile**: chiamandolo risponde il servizio clienti di una finanziaria.
Sostituito con un numero del blocco 055, lo stesso di un cliente già in
esercizio. → **chiamare sempre il numero prima di assegnarlo.**

## Gestionale — Resmio, slug `redmike`

Com'era all'inizio e com'è stato messo:

| | Prima | Dopo |
|---|---|---|
| Giorni | LUN–SAB | **LUN–DOM** |
| Fascia prenotabile | 14:00–22:00 | **19:00–23:30** |
| Capacità per fascia | 10 | **28** |
| Intervallo | 30 min | **15 min** |
| Durata prenotazione | — | **90 min** |
| Auto-conferma fino a | — | **8 persone** (= soglia agente) |
| Eccezione "Chiuso" | 18 ago → 1 set 2026 | rimossa |
| Limiti ora di punta | LUN–DOM 14:00–22:00, 15 | **LUN–DOM 19:00–23:30**, 15 |

Con la fascia sbagliata l'agente avrebbe proposto le 14:00 e negato le 20:30, e
con l'eccezione attiva avrebbe detto "non c'è posto" fino a settembre. Nessuno
dei due problemi si vedeva guardando il prompt.

Widget diretto: `https://app.resmio.com/redmike/widget`

## Agente DeepAgent

| Voce | Valore |
|---|---|
| Id agente | `<id agente>` (da `agent.list`) |
| Assistente / voce | **Roberta** |
| Slug tool | `redmike` |
| Tool disponibilità | `get_disponibilit_redmike` |
| Tool prenotazione | `set_prenotazione_redmike` |
| Campo di smistamento | `ResmioUtente: "redmike"` nel body |
| Stato | Attivato |

I due tool condividono l'endpoint con quelli di un altro locale: lo smistamento
avviene per `ResmioUtente`, che è scritto nel `<toolkit>` del prompt. Verificato
con una prenotazione di prova, arrivata nel Resmio giusto.

## Cronologia dei guasti trovati

Utile come lista di ciò che va cercato in ogni agente nato da una copia:

1. Prompt del locale precedente, con nome sbagliato dell'assistente e tre sedi
   che non esistono.
2. Tre nomi diversi per lo stesso agente: voce Roberta, primo messaggio Alice,
   prompt Sara.
3. `Trasferisci a Umano` con i tre numeri e le condizioni dell'altro locale.
4. Tool che puntano alle rotte dell'altro locale.
5. Gestionale con orari, giorni e capacità che non c'entravano col locale.
6. Chiusura programmata dimenticata nel gestionale.
7. Limiti dell'ora di punta rimasti sulla vecchia finestra oraria.
8. Numero di telefono che rispondeva a un terzo.
9. Deploy interrotto, con `Attiva` che falliva in silenzio.
