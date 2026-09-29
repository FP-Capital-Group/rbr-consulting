---
name: dati-delivery-portali
description: Estrae dai portali Deliveroo Partner Hub e Glovo Partner Portal il venduto, gli ordini e le commissioni delivery per locale e per mese (con la sessione già aperta nel browser), divide fatture e commissioni fra più locali della stessa partita IVA e li riconcilia con cassa e CDG — incluse le trappole dei numeri diversi fra pagine dello stesso portale. Usala quando il consulente dice "quanto fa il delivery di X", "dividi Deliveroo e Glovo per locale", "scarica il venduto dai portali delivery", "il delivery è dentro i corrispettivi?", "quanti ordini fa su Deliveroo", "le commissioni delivery nel CDG", "diagnosi delivery", "da quando ha alzato i prezzi sul delivery cosa è cambiato".
---

# Dati delivery dai portali (Deliveroo, Glovo)

> Metodo nato su Raíces (2 locali, stessa P.IVA, lug-set 2026).

## Perché esiste
Le fatture delivery arrivano intestate alla società, non al locale, e il «totale» del portale non
coincide con l'imponibile della fattura. Senza dividerle bene il CDG per store è sbagliato, e senza
ordini veri non si può dire se un rialzo prezzi ha funzionato.

## Prerequisiti
- Sessione del cliente aperta nel Chrome del consulente (login con 2FA: lo fa il cliente o il consulente).
- Export fatture SDI (per commissioni) e cassa per locale (per sapere se il delivery è nei corrispettivi).

## Deliveroo Partner Hub
- Più locali = spesso **più organizzazioni** (org + branch); un branch può essere un market senza vendite.
- **Pagina Ordini** con `?startDate&endDate` nell'URL per mese; per iterare i mesi senza ricaricare:
  `window.next.router.push(...)` (è un'app Next.js).
- ⚠️ Il report **Performance** e la **pagina Ordini** possono dare numeri diversi (su un locale −20%):
  prima di usare uno dei due nel CDG, apri una fattura e guarda su quale imponibile è calcolata la
  commissione (commissione ≈ % × valore giusto). Finché non è chiarito, NON toccare il CDG: segnalalo.
- Fatture con serie unica per tutta la società → split per locale: coppia di fatture della stessa
  settimana + ranking sul totale del portale per locale (la più alta al locale che ha venduto di più);
  segnala le settimane ambigue. Deve riconciliare al centesimo col totale.

## Glovo Partner Portal
- Report per vendor: `/reports/GV_IT;<vendor>?from&to&prevFrom&prevTo`, ma **prima** bisogna
  selezionare lo store dal selettore in UI (il vendor nell'URL da solo è ignorato); niente router JS,
  navigazioni piene.
- «Sales» = valore del cibo (esclusi sconti e fee).
- **Serie numero fattura Foodinho diversa per store** → split esatto delle fatture.
- ⚠️ Gli slug dei negozi possono essere **invertiti** rispetto al nome: verifica sempre dall'ID vendor
  nel sorgente della pagina.

## Nel CDG
- Chiedi (o verifica) se il delivery è dentro i corrispettivi di cassa. Se sì: ricavo ristorante =
  (POS − Deliveroo − Glovo) ÷ 1,1 e due righe delivery separate, con la formula visibile.
- Commissioni delivery nei costi variabili del locale, split esatto dove possibile, altrimenti % venduto
  del mese (dichiarato).

## Diagnosi delivery (rialzo prezzi, ordini)
- Trova la **data del rialzo** (storico menu o salto dello scontrino medio) e confronta mese per mese
  ordini, scontrino medio, venduto, commissioni prima/dopo.
- Se il portale non dà gli ordini per un periodo, stimali dal **rapporto carrelli** (venduto ÷ scontrino
  medio del periodo vicino) e scrivi la nota metodologica nel foglio.
- Controlla gli **articoli per ordine** prima di affermare che il food cost per ordine è rimasto uguale.
- Consegna: foglio a 2 tab (dati mese per mese + nota metodologica).

## Definition of Done
- [ ] Venduto e ordini per locale × mese salvati in json nei dati del cliente
- [ ] Fatture/commissioni divise per locale e riconciliate al centesimo col totale
- [ ] Discrepanze fra pagine del portale segnalate, non «scelte» in silenzio
- [ ] CDG aggiornato solo dopo la verifica, con formule visibili
