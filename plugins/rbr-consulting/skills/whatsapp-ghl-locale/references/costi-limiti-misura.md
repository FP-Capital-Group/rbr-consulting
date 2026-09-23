# Costi, limiti di invio e misura

> Contributo di Luciano Purpi (2026-09-04, aggiornato a set 2026), con i limiti a
> livello di portfolio osservati sui conti il 2026-09-13. Dati di costo del caso
> Noolas da Andrea Chirivì.
>
> **Fonte dei dati Meta**: developers.facebook.com, pagine pricing e messaging-limits,
> verificate il 4 set 2026. Vengono dalla documentazione, non dal campo: ricontrollale
> prima di un preventivo importante.

## Costi

- **Add-on GHL**: 15 $/mese per sub-account.
- **Meta, dal 1° luglio 2025**: NON si paga più a conversazione ma **a messaggio
  template consegnato**, con prezzo per categoria, paese e volume.
  - **Marketing**: circa 0,10 euro a messaggio in Europa occidentale.
  - **Utility**: molto meno, e cala col volume.
  - **Risposte libere dentro le 24 ore**: gratis **solo fino al 30 settembre 2026**,
    poi a pagamento. → **Rifare i preventivi degli assistenti conversazionali** (bot
    che rispondono in chat) che contavano su risposte gratuite.
- Caso reale Noolas, agosto 2026: circa 33 $ di sole conferme prenotazione (Utility).
- Dove si vede la spesa: Settings → Billing → Wallet & Transactions.

Al cliente si spiega: 15 $/mese + consumo a messaggio template consegnato, con le
Utility (servizio) che costano poco e le Marketing che si pagano a messaggio.

## Limiti di invio

A gradini: **250 → 2.000 → 10.000 → 100.000 → illimitato** contatti unici nelle 24 ore
(il gradino attuale si vede in Impostazioni → WhatsApp → Limiti di messaggistica).
- **Si sale** con qualità Media/Alta e usando almeno il **50% del limite negli ultimi
  7 giorni**; Meta controlla ogni 6 ore.
- ⚠️ **Attenzione agenzia**: dal 7 ottobre 2025 i limiti valgono a livello di
  **BUSINESS PORTFOLIO**, non per numero. Se più clienti stanno sotto lo stesso
  portfolio i volumi si sommano, e **un cliente che si comporta male abbassa i limiti
  agli altri**.
- Effetto pratico osservato (13 set 2026): Barresi è già a 100.000/24h pur avendo
  mandato pochissimo, perché eredita il gradino dagli altri clienti dell'agenzia.
  Quindi **il limite non è mai il collo di bottiglia per un locale: la qualità sì**
  (un numero nuovo va comunque scaldato, vedi `invio-di-massa.md`).

## Misura

- Ogni link nei template porta **`source=whatsapp-<campagna>`**: è così che nel
  report si distingue cosa ha portato WhatsApp rispetto a email e ads.
- Si misura in **persone che entrano** (prenotazioni, coupon/gift card riscattati),
  non in messaggi consegnati.
- Per le liste fredde: tasso di sì al template di consenso (attesi 10-20%, vedi
  `consenso-e-liste.md`) e andamento della qualità del numero dopo ogni lotto.
