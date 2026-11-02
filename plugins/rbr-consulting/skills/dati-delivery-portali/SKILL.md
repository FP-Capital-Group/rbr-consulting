---
name: dati-delivery-portali
description: Estrae dai portali Deliveroo Partner Hub, Glovo Partner Portal e Just Eat Partner Hub il venduto, gli ordini e le commissioni delivery per locale e per mese (con la sessione già aperta nel browser), divide fatture e commissioni fra più locali della stessa partita IVA e li riconcilia con cassa e CDG — incluse le trappole dei numeri diversi fra pagine dello stesso portale. Usala quando il consulente dice "quanto fa il delivery di X", "dividi Deliveroo e Glovo per locale", "scarica il venduto dai portali delivery", "il delivery è dentro i corrispettivi?", "quanti ordini fa su Deliveroo", "quanto fa su Just Eat", "le commissioni delivery nel CDG", "diagnosi delivery", "da quando ha alzato i prezzi sul delivery cosa è cambiato".
---

# Dati delivery dai portali (Deliveroo, Glovo, Just Eat)

> Metodo nato su Raíces (2 locali, stessa P.IVA, lug-set 2026).

## Perché esiste
Le fatture delivery arrivano intestate alla società, non al locale, e il «totale» del portale non
coincide con l'imponibile della fattura. Senza dividerle bene il CDG per store è sbagliato, e senza
ordini veri non si può dire se un rialzo prezzi ha funzionato.

## Prerequisiti
- Sessione del cliente aperta nel Chrome del consulente (login con 2FA: lo fa il cliente o il consulente).
- Export fatture SDI (per commissioni) e cassa per locale (per sapere se il delivery è nei corrispettivi).
- ⚠️ **Verifica l'account attivo prima di leggere o salvare qualunque numero**: nel profilo Chrome c'è una sola sessione per portale, e il Partner Hub del consulente può restare loggato sull'account di un ALTRO cliente (caso reale: Deliveroo aperto sull'account del cliente sbagliato). Prima di ogni lettura o salvataggio leggi organizzazione, branch e nome del locale nella pagina e confrontali col cliente atteso — se non coincidono, fermati, rientra col cliente giusto e scarta i dati letti fino a lì. Vale per Deliveroo, Glovo e Just Eat (compartimenti stagni fra clienti). *(contributo di Andrea Chirivì, 2026-10-12, regola gemella di Luciano Purpi su iPratico)*
- ⚠️ La mail `partner.support` di Deliveroo risponde in automatico "casella non monitorata": usa la Live Chat del Partner Hub (lun-ven 10-18:45) o il referente commerciale del locale. L'accesso ufficiale all'Order API e ai webhook di Deliveroo si chiede dal Developer Portal o al referente — esito non ancora noto (richiesta inviata il 25/09/2026, risposta solo automatica).

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
- Da una scheda in background il calendario del Partner Hub non si usa: metti un hook su `XMLHttpRequest`, cattura il POST `/api/reporting_platform/reports` e rilancialo via `fetch` cambiando le date (tecnica dell'hook in `catenaria-pienissimo/playbook.md:85-99`).
- Range massimo: ~14 giorni per Ordini, ~1 mese per Performance. Dopo ~10 creazioni scatta il rate limit Cloudflare (429): pausa, poi riprendi.
- Lo storico può fermarsi a una certa data per limite della piattaforma, non per dato mancante: verificalo prima di segnalarlo come buco.
- Nei mesi vecchi il punto vendita può comparire con un altro nome: può essere un cambio nome o un secondo locale — chiedi al cliente prima di sommare, non darlo per scontato.
- Ordini rigettati: segnalali come problema operativo (es. chiusura anticipata rispetto agli orari dichiarati).
- Via manuale da dare al cliente: Report → Performance → periodo personalizzato → General report, un file per mese.
- Per il dettaglio di ogni ordine (righe, modificatori, orari) c'è l'API interna degli ordini: vedi `references/deliveroo-api-ordini.md`.
*(contributo di Andrea Chirivì, 2026-10-12)*

## Glovo Partner Portal
- Report per vendor: `/reports/GV_IT;<vendor>?from&to&prevFrom&prevTo`, ma **prima** bisogna
  selezionare lo store dal selettore in UI (il vendor nell'URL da solo è ignorato); niente router JS,
  navigazioni piene.
- «Sales» = valore del cibo (esclusi sconti e fee).
- **Serie numero fattura Foodinho diversa per store** → split esatto delle fatture.
- ⚠️ Gli slug dei negozi possono essere **invertiti** rispetto al nome: verifica sempre dall'ID vendor
  nel sorgente della pagina.

## Just Eat Partner Hub
- `partner-hub.justeat.it` → Documenti di riepilogo quindicinali: lì si leggono vendite e commissioni (le commissioni sono il subtotale dei documenti).
- Il testo sta dentro uno **shadow DOM**: `document.body.innerText` non lo vede — serve una funzione che scende ricorsivamente negli `shadowRoot`.
- La sessione scade spesso: serve il login del consulente, da chiedere in un solo messaggio.

## Nel CDG
Prima di scrivere, guarda nei rapporti di cassa (colonna Operatori o reparto) quanto delivery è già battuto e sotto quale voce — non darlo per scontato (caso reale: si sospettava finisse nei "preventivi", la foto Operatori ha mostrato solo 14 scontrini delivery per 577 €).

Tre casi:
- **(a) Delivery nei corrispettivi**: resta la regola attuale — ricavo ristorante = (POS − Deliveroo − Glovo) ÷ 1,1, due righe delivery separate, formula visibile in cella.
- **(b) Delivery FUORI cassa**: una riga dedicata per portale, "delivery fuori cassa <portale>" = (vendite del portale − quota già battuta in cassa) ÷ 1,1, formula visibile. Senza queste righe l'EBITDA è sbagliato (caso reale: mancavano 11.968 € netti in 9 mesi).
- **(c) Ordini battuti in cassa come asporto** (numero d'ordine come nome, solo per mandare la comanda in cucina, non scontrinati perché incassa la piattaforma): non sono nei corrispettivi, trattali come il caso (b). Sembrano ordini spariti nel controllo cassa: si incrociano col Partner Hub del giorno per **numero d'ordine**, mai per ora o importo (vedi `estrai-dati-ipratico`).

⚠️ Nota fiscale: se il delivery vada scontrinato lo decide il commercialista, non il consulente. La skill registra il fatto e lo segnala al cliente come rischio (i bonifici delle piattaforme sono tracciati).

**Commissioni** nei costi variabili del locale, split esatto dove possibile, altrimenti per portale:
- **Deliveroo senza fatture nel gestionale**: stima = (vendite − pagamenti settimanali) ÷ 1,22, dichiarata in nota come "trattenute stimate" (non è solo commissione: comprende anche promo co-finanziate e rimborsi — caso reale 44%, è una trattenuta complessiva, non la sola commissione).
- **Glovo**: l'imponibile sta nel dettaglio della fattura (Finanza → Fatture).
- **Just Eat**: commissioni = subtotale dei Documenti di riepilogo quindicinali.
- Per i mesi scoperti da fattura, usa il rapporto commissioni/vendite REALE dei mesi che hanno la fattura (es. Glovo apr-set = 32%), dichiarato in nota — mai una percentuale generica.
- Regola IVA: lo scorporo /1,22 "a vista" si fa SOLO sugli importi del portale IVA inclusa. Con fattura SDI si usa l'imponibile, senza scorporo (`crea-cdg-cliente/SKILL.md`).
- Benchmark di un caso reale: commissioni delivery totali ≈ 38% dei ricavi delivery netti.

*(contributo di Andrea Chirivì, 2026-10-12)*

## Diagnosi delivery (rialzo prezzi, ordini)
- Trova la **data del rialzo** (storico menu o salto dello scontrino medio) e confronta mese per mese
  ordini, scontrino medio, venduto, commissioni prima/dopo.
- Se il portale non dà gli ordini per un periodo, stimali dal **rapporto carrelli** (venduto ÷ scontrino
  medio del periodo vicino) e scrivi la nota metodologica nel foglio.
- Controlla gli **articoli per ordine** prima di affermare che il food cost per ordine è rimasto uguale.
- **Mix per categoria del canale**: leggi cosa vende davvero il canale (caso reale: un locale vendeva su Glovo soprattutto schiacciate/panini/fritti e quasi nulla di pizza — il canale era una panineria, non una pizzeria, e il menu delivery si costruisce su quello che il canale compra).
- **Quota netta che resta al locale** = pagamenti ÷ lordo del portale, accanto all'ordine medio.
- **Ordini per fascia**: pochi ordini in una fascia (es. pranzo) bocciano le idee pensate per quella fascia, prima ancora di lanciarle.
- Consegna: foglio a 2 tab (dati mese per mese + nota metodologica).

## Definition of Done
- [ ] Venduto e ordini per locale × mese salvati in json nei dati del cliente
- [ ] Fatture/commissioni divise per locale e riconciliate al centesimo col totale
- [ ] Discrepanze fra pagine del portale segnalate, non «scelte» in silenzio
- [ ] CDG aggiornato solo dopo la verifica, con formule visibili
- [ ] Quota delivery già battuta in cassa verificata prima di scrivere (casi a/b/c)
- [ ] Account/organizzazione del portale verificato (cliente giusto) prima di leggere o salvare dati
