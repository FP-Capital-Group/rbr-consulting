# Consenso e liste fredde

> Contributo di Luciano Purpi (2026-09-04), con il pattern "consenso prima
> dell'offerta" dal contributo del 2026-09-13.

Conferme e promemoria di una prenotazione sono legittimi di suo. **Tutto il Marketing
va solo a chi ha dato il consenso**, e il consenso deve essere registrato in GHL in
modo che i flussi lo possano leggere. Il motivo non è solo legale: chi riceve
marketing che non ha chiesto blocca e segnala, e la qualità del numero crolla.

## Dove si raccoglie l'opt-in

- **Form** (sito, landing, prenotazione) con casella di consenso marketing WhatsApp.
- **QR al tavolo** che apre una chat o una landing con il consenso.
- **Template di consenso** (`template-pronti.md` n. 4) verso chi è già cliente.

## Come si registra in GHL

- tag **`consenso-marketing`**;
- custom field **`consenso_data`** (quando);
- custom field **`consenso_origine`** (da dove: form, QR, template, …).

Chi scrive STOP perde il tag `consenso-marketing` (vedi `orecchio-e-stop.md`).

## Lista di soli numeri importata senza consenso: procedura in 5 passi

1. **Ricostruisci la provenienza col titolare**: da dove vengono questi numeri
   (rubrica del telefono, vecchio gestionale, prenotazioni)? Serve per dichiararla
   nel primo messaggio ("ho il tuo numero perché sei stato nostro cliente").
2. **Segmenta per recenza**: prima chi è venuto di recente.
3. **Lavora a blocchi di 50-100 al giorno**, dal più recente al più vecchio.
4. **Primo messaggio = template di consenso, NON l'offerta.** L'offerta arriva solo
   dopo il sì, dentro le 24 ore, in testo libero.
5. **Chi dice no esce e non si ricontatta.** Chi non risponde non va "rincorso" con
   un altro template.

Attendersi **10-20% di risposte positive**.

Prima di partire, ripulisci la lista da fornitori e contatti di prova: la rubrica del
ristoratore non contiene solo clienti (vedi `invio-di-massa.md`).

## Il pattern "consenso prima dell'offerta" (Barresi, funziona)

Il template che apre la relazione chiede se la persona vuole il regalo, invece di
mandarlo. Tre effetti insieme:
1. **dichiara perché hai il numero** ("sei stato nostro cliente");
2. **raccoglie un consenso esplicito e tracciabile** (il clic su "Sì");
3. **sposta il seguito dentro le 24 ore**, dove il testo è libero e non serve un
   altro template da far approvare.

"Se non ti interessa non fare niente: non ti scrivo più" è l'opt-out più gentile che
esista. Testo completo in `template-pronti.md` (n. 4).
