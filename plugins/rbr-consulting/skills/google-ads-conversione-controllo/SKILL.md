---
name: google-ads-conversione-controllo
description: Chiude il cerchio di una campagna Google Ads di un ristorante — crea la conversione «Prenota» sul widget di prenotazione (TheFork, Resmio o simili dentro iframe), mette il tag sul sito rispettando il banner cookie, verifica che parta DOPO il consenso, lancia la campagna mettendo in pausa le Smart vecchie e imposta un controllo giornaliero automatico con riepilogo Telegram e un'unica regola di ritocco permessa. Usala quando il consulente dice "misura le prenotazioni da Google Ads", "metti il tag di conversione", "la campagna non registra conversioni", "lancia la Search e controlla ogni giorno", "il tag c'è ma non traccia", "fammi un controllo quotidiano delle ads". Il piano della campagna lo fa adv-ristorante; questa skill la rende misurabile e sorvegliata.
---

# Google Ads: conversione Prenota + controllo giornaliero

> Metodo nato su Raíces (24/09/2026). KPI nord RBR: **costo per prenotazione** — senza questa
> conversione la campagna ottimizza sui clic e il KPI non si può leggere.

## Prerequisiti
- Campagna Search pronta (`adv-ristorante`), MCP `google-ads` con accesso all'account del cliente.
- Accesso al sito (`sito-wordpress-cliente-mcp` o `sito-landing-ristorante`).
- Sapere quale banner cookie usa il sito e con che categoria blocca gli script.

## Procedura
1. **Conversione**: via MCP (`execute_google_ads_mutate`) crea una ConversionAction WEBPAGE,
   categoria BOOK_APPOINTMENT, **primaria**, conteggio una per clic, valore fisso 1 €.
   Prendi il `send_to` (`AW-<id>/<label>`).
2. **Evento sul widget** (il widget è un iframe cross-origin: i clic dentro non si vedono):
   - *blur trick*: su `window.blur`, se `document.activeElement` è un IFRAME con `thefork` (o `resmio`)
     nello `src` → conversione;
   - in più, clic su qualsiasi `a[href*="thefork"]` (tasti che aprono la pagina intera);
   - una sola conversione per pagina (flag `sent`).
   Modello pronto in `tag-modello.html`.
3. **Consenso**: il blocco va messo in modo che il banner cookie lo gestisca (es. `type="text/plain"` +
   categoria statistiche/marketing, come fa il banner del sito). Mai farlo partire prima del consenso.
4. **Inserimento** in coda al footer con un marker di versione (`<!-- cliente-gads-v1 -->`), idempotente.
5. **Verifica vera, non a vista** — due passaggi nel browser:
   - con cookie RIFIUTATI: nessuna chiamata `googletagmanager`/`doubleclick`;
   - dopo «Accetta tutti»: si caricano `gtag/js?id=AW-…`, esiste `google_tag_manager['AW-…']`, partono
     `google.com/ccm/collect` e `ad.doubleclick.net/ccm`. Controlla con l'ID REALE, non col nome della funzione.
6. **Lancio**: attiva la Search, metti in **pausa le Smart** dello stesso account (si cannibalizzano),
   controlla billing APPROVED e annunci APPROVED (il primo giorno possono stare in PENDING).
7. **Controllo giornaliero**: scheduled task (es. ogni giorno alle 9) che legge con GAQL spesa, impression,
   clic, CPC, conversioni per gruppo e manda il riepilogo su Telegram al consulente. **Unica modifica
   automatica permessa**: +0,20 € di CPC a un gruppo con 0 impression per 2 giorni di fila, con un tetto
   (es. 1,50 €). Tutto il resto (budget, keyword, pausa) solo su ok del consulente.

## Regole RBR & trabocchetti
- Il nome account nell'MCP può uscire «Unknown»: identifica sempre per customer ID.
- Il gruppo «conquest» sui competitor: il nome del concorrente mai nei testi degli annunci.
- Sitelink e callout coerenti col sito: se il sito non ha WhatsApp, nessun sitelink WhatsApp.
- Un tag «installato» ma mai verificato dopo il consenso vale zero: può restare muto per mesi.
- Se aggiungi Meta nello stesso footer, stesso metodo (evento `Schedule` sul widget) e stessa verifica.

## Definition of Done
- [ ] Conversione primaria creata, `send_to` salvato nella memoria cliente
- [ ] Tag online sotto consenso, verificato con cookie rifiutati E accettati
- [ ] Search attiva, Smart in pausa, annunci approvati
- [ ] Task giornaliero attivo con riepilogo Telegram, regola di ritocco scritta nella memoria cliente
