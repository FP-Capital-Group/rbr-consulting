# Deliveroo: API interna degli ordini

*(contributo di Andrea Chirivì, 2026-10-12)*

Per il dettaglio di ogni ordine (righe, modificatori, orari), oltre al Partner Hub c'è l'API
interna usata dalla pagina stessa. Serve per gli articoli per ordine nella Diagnosi delivery
(vedi `SKILL.md`, sezione Diagnosi).

- **Lista ordini**: `GET /api/restaurants/<restaurant_id>/orders?payment_type=all&limit=50&date=D&end_date=D+1`
- **Dettaglio ordine**: `GET /api/orders/<order_id>` — righe e modificatori, `timeline.prepare_for`
  (ora in cui l'ordine deve essere pronto per il rider), `delivery_picked_up_at`.
- **Header obbligatori**: `Authorization: Bearer <JWT>`, `X-Roo-Org-Id: <org>`,
  `X-Hub-Api-Caller: https://partner-hub.deliveroo.com`.
- Il JWT dura circa 44 minuti, sta in un cookie della pagina e NON si rinnova da solo. Per
  rinnovarlo, 5 minuti prima della scadenza carica `/orders` in un iframe nascosto della stessa
  origine.

## Trappole
- Mai `a.click()` via script: il renderer della scheda si blocca.
- Il tasto "Aggiorna" ricarica la pagina e uccide lo script.
- In background i `setTimeout` vanno a 1 al minuto.
- `restaurant_id` e `org` sono specifici di ogni cliente: mai riusare quelli di un altro cliente.
