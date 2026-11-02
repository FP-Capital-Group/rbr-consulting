---
name: segmentazione-rfm
description: >-
  Segmenta i contatti di un locale cliente in GoHighLevel con il metodo RFM (Recency, Frequency,
  Monetary): calcola i punteggi R-F-M, costruisce i segmenti (champion/top spender, fedeli, nuovi,
  a rischio, dormienti, persi) e li tagga su GHL per campagne mirate. Usala quando l'utente dice
  "segmentazione RFM", "segmenta i clienti di X", "chi sono i top spender", "clienti dormienti",
  "campagna win-back sui clienti persi", "analisi RFM", "chi non ordina da mesi". Ogni operazione
  GoHighLevel passa dai tool MCP ghl2-[cliente], mai curl diretto.
---

# Segmentazione RFM su GoHighLevel

## Perché esiste
Un ristorante non deve parlare a tutti i clienti allo stesso modo: il cliente che spende 500€/anno
e quello che non ordina da 8 mesi vogliono messaggi diversi. RFM classifica ogni contatto su tre
assi — quanto è recente l'ultimo acquisto (R), quanto spesso compra (F), quanto spende (M) — e
produce segmenti azionabili su cui costruire campagne GHL mirate (VIP, win-back, benvenuto).

⚠️ **Stato del sistema RFM RBR**: il piano completo (sync POS notturno → CF GHL) è stato presentato
il 2026-05-08 e **rinviato da Marco** ("per il momento non lo facciamo"). Riferimento:
`mister-pizza/memory/rfm_segmentazione.md`. Questa skill applica il metodo RFM standard via MCP;
le parti marcate 🟡 vanno validate con Marco prima di eseguirle su un cliente vero.

## Quando usarla
- Il cliente vuole campagne mirate (VIP, riattivazione dormienti, benvenuto nuovi).
- Devi capire la base clienti di un locale: quanti attivi, quanti persi, chi spende di più.
- Prima di un funnel promo: scegliere A CHI mandarlo, non solo cosa scrivere.

## Prerequisiti
- Istanza MCP del cliente attiva: `ghl2-<cliente>` (misterpizza, personalg, democliente, dirigi,
  redmike, cipriano). Setup nuova istanza: `suite/memory/ghl_mcp_server.md`.
- **Dati di acquisto**. GHL da solo NON ha gli ordini: servono i dati POS. Nel blueprint RBR
  (`suite/memory/blueprint_monosede.md`) esistono già i Custom Field dedicati, previsti per un
  sync POS notturno:
  - RFM (3): `rfm_recenza`, `rfm_frequenza`, `rfm_monetario` (SINGLE_OPTIONS 1-5)
  - Statistiche (6): `spesa_totale`, `ordini_totali`, `giorni_dall_ultimo_ordine`,
    `data_ultimo_ordine`, `importo_ultimo_ordine`, `importo_primo_ordine`
  - ⚠️ Il sync POS→GHL **non è ancora implementato**: aspettati CF vuoti. In quel caso i dati
    vanno presi dal POS (iPratico: `lib/ipratico/` in `mister-pizza/`, oppure export ordini
    fornito dal cliente).
- **Chiave di aggancio POS↔GHL** (caso iPratico): `Ordini.fidelity` ↔ CF `fidelity_number`.
  Gli ordini iPratico non hanno email → **solo i contatti con tessera fidelity sono matchabili**.
  Per altri POS, concordare la chiave (email/telefono) con Marco.

## Procedura

### 1. Ricognizione su GHL (sempre via MCP)
Regola fissa: `search_operations` → `describe_operation` → `execute_operation` sull'istanza
`ghl2-<cliente>`. Mai curl diretto sull'API GHL.
- Cerca le operazioni contatti (`search_operations` con "contacts search") e custom field.
- Scarica i contatti con i CF RFM/statistiche e verifica se sono popolati.
- Per contare chi ha davvero un campo personalizzato valorizzato usa `contacts/search` con filtro `field: "customFields.<id>"` e operatore `exists` (oppure `eq` con un valore preciso, es. Consenso Marketing = 1) — l'operatore `not_empty` NON esiste per i campi personalizzati. Gli id dei campi si leggono una volta sola dai custom field della location. Per la paginazione servono `startAfter` e `startAfterId` insieme. Il conteggio va fatto prima di ogni campagna o pulizia, per sapere su quanti contatti si lavora davvero. *(contributo di Andrea Chirivì, 2026-10-12)*

### 2. Procurati i dati di acquisto
- CF popolati → usali direttamente.
- CF vuoti → estrai gli ordini dal POS o da un export del cliente. Per ogni cliente ti servono:
  data ultimo ordine, numero ordini nel periodo (12-24 mesi), spesa totale.
- Riconcilia POS↔GHL sulla chiave concordata. Elenca a parte i non matchabili (senza fidelity).
- Se i dati vengono da un import, controlla la data dell'import e cosa li ha aggiornati da allora (vedi `references/sei-stati-ristorante.md`, punto 1-bis: lo stato importato è una fotografia ferma).

### 3. Scoring R-F-M in Python (locale)
Per ogni contatto matchato:
- **R** = giorni dall'ultimo ordine, **F** = numero ordini, **M** = spesa totale.
- Assegna a ciascuno un punteggio 1-5 per **quintili dinamici** calcolati sulla base clienti del
  locale (non bucket fissi: era il difetto del vecchio sistema Keap). R invertito: più recente = 5.
- `rfm_score` = concatenazione, es. "555".
- 🟡 Se il locale ha più punti vendita, calcola per punto vendita (piano: CF `preferred_pv`) —
  da validare con Marco.

### 4. Mappa i segmenti
**Default RBR per i ristoranti: sei stati, non 125 celle** *(contributo di Luciano Purpi, 2026-09-13)*.
Una matrice 5×5×5 su un ristorante resta quasi vuota e nessuno agisce su 125 segmenti. Si usano
sei stati mutuamente esclusivi (il tag si sostituisce, non si somma) più "non misurato":
**Nuovo** (1 visita, ≤60 gg) · **Abituale** (2-3 visite, ≤90 gg) · **Affezionato** (4+, ≤90 gg) ·
**Abituale fermo** (2+, ultima 91-180 gg — qui stanno i soldi) · **Dormiente** (181-365 gg) ·
**Perso** (>365 gg). Le soglie sono **ipotesi** da tarare (≈1,3 × intervallo mediano fra 1ª e 2ª
visita, dopo 6 mesi di gestionale) e va detto al cliente. Al posto della M, quasi sempre assente,
si usano i **coperti** come bandierina dentro lo stato (media 4+ persone → offerta di gruppo).
Trattamento per stato, taratura, ordine di lavoro e accensione senza ponte gestionale→CRM:
`references/sei-stati-ristorante.md`.

**Variante a quintili** (solo quando la M per cliente esiste davvero, es. delivery/fidelity con
scontrino per cliente). Etichette dal piano RFM RBR (`rfm_segmentazione.md`): `champion`, `loyal`, `potential`, `new`,
`at_risk`, `hibernating`, `lost`. Mappatura standard di riferimento — 🟡 soglie da validare con
Marco prima dell'uso sui clienti:

| Segmento | Criterio indicativo | Uso campagna |
|---|---|---|
| champion (top spender) | R 4-5, F 4-5, M 4-5 | VIP invite, anteprime |
| loyal | R 3-5, F 4-5 | programma fedeltà, referral |
| potential | R 4-5, F 2-3 | spinta al secondo/terzo ordine |
| new | R 5, F 1 | funnel benvenuto |
| at_risk | R 2-3, F 3-5 | win-back leggero |
| hibernating (dormienti) | R 1-2, F 1-2 | win-back con offerta forte |
| lost | R 1, F 1-2 | ultima chiamata / pulizia lista |

### 5. Scrivi tag e CF su GHL (via MCP)
- Crea (se mancano) e applica i tag segmento, es. `rfm-champion`, `rfm-dormiente` — o aggiorna i
  CF `rfm_recenza`/`rfm_frequenza`/`rfm_monetario` se il cliente ha il blueprint.
- Operazioni: `search_operations` per "add tags to contact" / "update contact", poi
  `describe_operation` e `execute_operation` in batch.
- ⚠️ **Rileggi sempre il contatto dopo la prima scrittura**: GHL può rispondere ok anche quando non scrive davvero il campo personalizzato. Se l'operazione MCP non scrive, usa `PUT /contacts/{id}` con `customFields: [{"id": "<id campo>", "field_value": <valore>}]` e il token di integrazione privata (PIT) del sotto-account. Sull'upsert (`POST /contacts/upsert`) la forma che funziona è `{id, value}`; con `key` + `field_value` l'API risponde 200 e lascia i campi vuoti senza avvisare — mai `key`. Prima della scrittura serve il CSV di anteprima confermato, durante un log con valore vecchio/nuovo per il rollback, e User-Agent esplicito negli script. Un contatore che un workflow deve incrementare va in un campo NUMERICO, mai testo (l'azione Math non accetta testo). *(contributo di Andrea Chirivì, 2026-10-12 — verificato sul PUT, 13.529 contatti senza errori; ⚠️ da verificare se l'MCP `ghl2-<cliente>` del plugin passa già la forma giusta)*
- 🟡 Convenzione naming tag RFM non ancora standardizzata in RBR — proponi `rfm-<segmento>` e
  fai confermare a Marco.

### 6. Usa i segmenti per le campagne
- Smart list / filtri GHL sul tag segmento → destinatari campagna.
- 🟡 Il piano prevede workflow GHL triggerati sul **cambio** di segmento (`at_risk` → Win-back,
  `champion` → VIP invite): non esistono ancora nel blueprint, vanno creati col cliente.
- **Prima di proporre una campagna su un database ereditato**: conta SUBITO i contattabili per il canale scelto (email: indirizzo valido + Consenso Marketing=1 + nessun DND; WhatsApp: telefono + consenso, vedi `whatsapp-ghl-locale/references/consenso-e-liste.md`), mostrando anche gli esclusi e il motivo. Dividi poi i contattabili per numero di visite (0 · 1 · 2-3 · 4-9 · 10+) e per anno dell'ultima presenza: su un database ereditato il blocco più grosso e più economico è spesso "venuto una volta sola, ultima visita l'anno scorso" — va in una campagna una tantum a scaglioni (vedi `onboarding-cliente-ghl/SKILL.md`, warm-up), non nei flussi ricorrenti. Riconta SEMPRE dopo la pulizia dello stato ereditato (punto 1-bis di `references/sei-stati-ristorante.md`), mai sui tag grezzi dell'import.
- Per i testi: skill `funnel-email-crm` / `mail-funnel-ghl`.

### 7. Misura il ritorno
- Misura RBR del ritorno: clienti già conosciuti (almeno una visita prima del mese) che tornano nel mese ÷ clienti serviti nel mese.
- Trappole quando i numeri vengono da un CRM terzo (Cooperto, Pienissimo, TheFork): (a) leggi la definizione del KPI (tooltip o API) prima di sommare — un "clienti di ritorno" che conta solo chi ha ≥2 visite DENTRO la finestra scelta sottostima se sommi mesi separati invece di leggere la finestra intera; (b) un NPS non è la media dei mesi, si ricalcola sulle risposte (stessa fonte); (c) i coupon usati sono tavoli, non persone — per le persone servono i coperti; (d) separa sempre i lead caricati in blocco dalla parte organica prima di citare la dimensione del database. *(contributo di Andrea Chirivì, 2026-10-12)*

## Regole RBR & trabocchetti
- ❌ Mai curl/script diretti sull'API GHL: sempre MCP `ghl2-<cliente>`.
- ⚠️ Quintili calcolati SUL locale, non su tutti i clienti RBR insieme.
- ⚠️ I tag di stato importati sono la fotografia del giorno dell'import: non usarli mai come destinatari di una riattivazione senza averli incrociati prima con le visite registrate dopo l'import (`references/sei-stati-ristorante.md`, punto 1-bis).
- ⚠️ Senza dati POS non inventare M: un RFM solo su R (data creazione contatto) non è RFM. Sui ristoranti il sostituto della M sono i coperti (vedi step 4).
- ⚠️ **Il tetto da dire PRIMA di promettere**: su Barresi il 46% delle visite (75 su 162) non aveva né telefono né email → metà sala invisibile al CRM. La leva vera è chiedere il contatto al tavolo (il QR di riscatto dà un motivo per lasciarlo). *(contributo di Luciano Purpi, 2026-09-13)*
- ⚠️ Snapshot dei conteggi per segmento PRIMA di taggare in massa; il tagging bulk è reversibile
  ma rumoroso — fallo confermare (🟡) se i contatti sono >1000.
- ❌ Mai lanciare la campagna: la skill si ferma ai segmenti taggati. L'invio lo decide il cliente.

## Definition of Done
- [ ] Fonte dati acquisti identificata (CF GHL popolati oppure POS/export) e riconciliata
- [ ] Scoring R-F-M a quintili dinamici calcolato per tutti i contatti matchabili
- [ ] Contatti non matchabili elencati a parte con motivo
- [ ] Segmenti mappati e conteggi per segmento mostrati a Marco/consulente
- [ ] Tag/CF scritti su GHL via MCP (dopo conferma 🟡 se bulk grande), contatto riletto dopo la scrittura
- [ ] Contattabili per canale contati (consenso, email o telefono, DND) prima di proporre una campagna
- [ ] Punti 🟡 (soglie segmenti, naming tag, workflow trigger) esplicitati e validati con Marco
