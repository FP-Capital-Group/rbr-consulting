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

### 2. Procurati i dati di acquisto
- CF popolati → usali direttamente.
- CF vuoti → estrai gli ordini dal POS o da un export del cliente. Per ogni cliente ti servono:
  data ultimo ordine, numero ordini nel periodo (12-24 mesi), spesa totale.
- Riconcilia POS↔GHL sulla chiave concordata. Elenca a parte i non matchabili (senza fidelity).

### 3. Scoring R-F-M in Python (locale)
Per ogni contatto matchato:
- **R** = giorni dall'ultimo ordine, **F** = numero ordini, **M** = spesa totale.
- Assegna a ciascuno un punteggio 1-5 per **quintili dinamici** calcolati sulla base clienti del
  locale (non bucket fissi: era il difetto del vecchio sistema Keap). R invertito: più recente = 5.
- `rfm_score` = concatenazione, es. "555".
- 🟡 Se il locale ha più punti vendita, calcola per punto vendita (piano: CF `preferred_pv`) —
  da validare con Marco.

### 4. Mappa i segmenti
Etichette dal piano RFM RBR (`rfm_segmentazione.md`): `champion`, `loyal`, `potential`, `new`,
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
- 🟡 Convenzione naming tag RFM non ancora standardizzata in RBR — proponi `rfm-<segmento>` e
  fai confermare a Marco.

### 6. Usa i segmenti per le campagne
- Smart list / filtri GHL sul tag segmento → destinatari campagna.
- 🟡 Il piano prevede workflow GHL triggerati sul **cambio** di segmento (`at_risk` → Win-back,
  `champion` → VIP invite): non esistono ancora nel blueprint, vanno creati col cliente.
- Per i testi: skill `funnel-email-crm` / `mail-funnel-ghl`.

## Regole RBR & trabocchetti
- ❌ Mai curl/script diretti sull'API GHL: sempre MCP `ghl2-<cliente>`.
- ⚠️ Quintili calcolati SUL locale, non su tutti i clienti RBR insieme.
- ⚠️ Senza dati POS non inventare M: un RFM solo su R (data creazione contatto) non è RFM.
- ⚠️ Snapshot dei conteggi per segmento PRIMA di taggare in massa; il tagging bulk è reversibile
  ma rumoroso — fallo confermare (🟡) se i contatti sono >1000.
- ❌ Mai lanciare la campagna: la skill si ferma ai segmenti taggati. L'invio lo decide il cliente.

## Definition of Done
- [ ] Fonte dati acquisti identificata (CF GHL popolati oppure POS/export) e riconciliata
- [ ] Scoring R-F-M a quintili dinamici calcolato per tutti i contatti matchabili
- [ ] Contatti non matchabili elencati a parte con motivo
- [ ] Segmenti mappati e conteggi per segmento mostrati a Marco/consulente
- [ ] Tag/CF scritti su GHL via MCP (dopo conferma 🟡 se bulk grande)
- [ ] Punti 🟡 (soglie segmenti, naming tag, workflow trigger) esplicitati e validati con Marco
