---
name: bot-risposte-ghl
description: Metodo RBR per costruire e accendere un bot AI di prima risposta su WhatsApp/Instagram/Facebook con Conversation AI 2.0 di GoHighLevel (AI Agents), per un ristorante che vuole rispondere a ogni messaggio senza vivere al telefono. Usala quando il cliente dice "voglio un'automazione di risposta ai messaggi", "un bot su WhatsApp", "rispondere in automatico ai social", "alleggerirmi dal telefono". Copre tutto il percorso verificato sul campo (Noolas, 04/09/2026): analisi delle chat reali, prompt nel tono del posizionamento, build dell'agente, LA TRAPPOLA DEL DEPLOY, Human Handover, spegnimento delle risposte automatiche Meta, avviso WhatsApp al responsabile di sala (ponte tag Make+workflow), collaudo e costi.
---

# Bot risposte GHL (Conversation AI 2.0) — il metodo

> Skill condivisa da Andrea Chirivì il 2026-10-12 (scansione skill).

Costruito e collaudato sul Noolas il 04/09/2026: bot vivo su 3 canali, prime risposte
in 15-16 secondi, handover al responsabile di sala in ~6 minuti. Questo file è la
strada completa, con ogni trappola pagata sul campo.

**Prerequisiti**: canale WhatsApp GHL attivo (skill `whatsapp-ghl-locale`: add-on 15$/mese,
coexistence, qualità Green), pagine FB/IG collegate a GHL, un sito del locale con
sitemap (per la knowledge base), posizionamento definito (skill `strategia-marketing-rbr`).

## Fase 0 — Analisi delle chat reali (MAI saltarla)

Prima di scrivere una riga di prompt, leggi 100-150 conversazioni vere (MCP GHL:
`conversations_search-conversation` + `get-messages`, per canale). Cerca:
- le **categorie di richiesta** e i volumi (sul Noolas: ~70% risposte "Confermo" alla
  catena prenotazioni, ~30% richieste operative: prenotare, modificare, disdire,
  richieste speciali, asporto, band, lamentele);
- i **buchi**: inbound mai risposti = coperti persi (il perché del progetto);
- il **tono dello staff** quando risponde a mano (è la voce da imitare);
- le categorie che DEVONO passare a un umano (decide il titolare, non tu);
- ⚠️ se il numero è usato anche per **chat personali/staff**: servirà l'esclusione.

Consegna al titolare la tabella categorie × canale e fatti dare le decisioni:
soglia gruppi grandi, chi riceve gli avvisi (nome+numero), a chi girare le band,
chat vietate al bot.

## Fase 1 — Il prompt (struttura in 5 blocchi)

Nel tono del posizionamento del locale. Struttura verificata:
1. **COME SCRIVI** — lingua, lei/tu, niente emoji/firma se lo staff non le usa, lessico
   e no-list del posizionamento. 🔴 **Cordialità obbligatoria**: mai risposte secche
   ("ecco il link" = antipatico); sempre un saluto o una parola di cortesia in apertura
   ("Buonasera!", "Certo!", "Volentieri!"). Breve ≠ freddo.
2. **I FATTI** — indirizzo, orari (piani, mai come vanto), reparti/piatti eroe,
   link di prenotazione **con source dedicato per canale** (es. `?source=bot-whatsapp`,
   `bot-instagram`, `bot-facebook`: così le provenienze dicono cosa porta il bot),
   eventi del mese, cose dismesse da spiegare (es. app morta).
3. **COSA FAI** — i casi che chiude da solo, con le frasi esatte tra virgolette.
   Regole d'oro: **mai offrire l'alternativa al link** ("se ha difficoltà ci scriva"
   è un invito a non usarlo — la raccolta dati scatta solo se è il cliente a dire che
   non riesce); 🔴 **mai dire "confermato"/"riceve la conferma"** per richieste che lo
   staff deve valutare (asporto, modifiche, gruppi): la formula è **"Mettiamo in
   lavorazione la sua richiesta e le rispondiamo a breve"** — la conferma è dell'umano.
4. **QUANDO PASSI LA MANO** — l'elenco handoff deciso col titolare, con la frase di
   passaggio ("Le faccio rispondere da un collega").
5. **MAI** — tavoli specifici, prezzi fuori menu, date alle band, invenzioni,
   insistere se il cliente vuole una persona, chat vietate.

## Fase 2 — Build dell'agente (AI Agents → Conversation AI)

1. Create Bot → **Prompt Based** → **Start from Scratch**. Nome tipo "<Cliente> Risposte",
   Business Name compilato, prompt nel campo Personality (l'editor riformatta le liste:
   cosmetico, ok).
2. **Contact Assignment Channels**: SOLO i canali voluti (es. WhatsApp+IG+FB, 3 di 8).
3. **Response Behavior**: accendi **Images** e **Voice Notes** (nelle chat vere i vocali
   sono ovunque; funzionano solo in Auto-Pilot).
4. **Knowledge Base**: creane una nuova → Web crawler → "All URLs in this domain" sul
   sito del locale → seleziona tutte le pagine della sitemap → Train. Poi collegala al
   bot in "Knowledge Base Triggers" con istruzione ("usala per menu, piatti, prezzi,
   orari, eventi"). Verifica con una domanda su un piatto: deve dare descrizione e
   prezzo REALI del sito.
5. **Human Handover** (Actions): abilita i 3 scenari di default + uno custom con
   l'elenco handoff del cliente. Per OGNI scenario: utente assegnatario, **Final
   Message in italiano** (i default sono in inglese!), frasi di esempio in italiano,
   "Reactivate bot after" 8 ore, tag `human handover` (è il gancio per gli avvisi),
   task sul contatto.
6. Testa nel pannello "Test your agent". **⚠️ ATTENZIONE: esegue le azioni per
   davvero, non è un ambiente sandbox** — il 24/09/2026 un test ha creato una
   prenotazione VERA su Resmio. Prima di testare il ramo prenotazione/API Call,
   usa un orario/tavolo fuori servizio o avvisa chi gestisce Resmio per
   annullare subito dopo. Verifica comunque: prenotazione → link giusto; band
   → contatto direzione artistica; conferma+allergia → "Segnato"; domanda menu
   → dati dalla KB. (correzione da contributo di Andrea Chirivì, 2026-10-12)

## Fase 3 — 🔴 LA TRAPPOLA DEL DEPLOY (il motore in folle)

**Mode=Auto-Pilot + canali selezionati NON bastano: il bot resta muto.** La selezione
canali vale solo per bot assegnati via workflow. Per l'auto-risposta serve la tab
**Deploy** dell'agente: **Configure su ogni canale** (WhatsApp → numeri, IG/FB →
pagine) → Update, toggle verdi. Senza questo passo sembra tutto attivo e non risponde
nessuno (sul Noolas: 1h30 di buco scoperta solo dai messaggi senza risposta).

Bonus nel Deploy: **"Doesn't have tags"** = esclusione contatti per tag (staff, amici).
⚠️ I tag creati via API non compaiono nel widget finché non esistono nel registro
(Settings → Tags): registrali prima.

## Fase 4 — Una sola voce: spegnere le risposte automatiche Meta

Se i primi messaggi FB/IG ricevono già una risposta fotocopia, spesso NON sta in GHL:
sta in **Meta Business Suite → Posta → Automazioni** ("Risposta automatica" e
"Messaggio di assenza"). ⚠️ Business Suite apre il **portfolio sbagliato** di default:
seleziona quello del cliente. Spegnile entrambe il giorno dell'accensione, mai prima.
E d'ora in poi: **niente IA di pagina Meta** (Business Agent) sui clienti col bot GHL —
doppia voce garantita.

## Fase 5 — Avviso WhatsApp al responsabile (il ponte tag)

Fatti verificati che obbligano questo disegno: **l'API pubblica GHL non invia template
WhatsApp** (422 Template not found con qualsiasi id) **né testo libero fuori dalla
finestra 24h** (Meta rifiuta). I template partono SOLO da UI e da workflow GHL.
⚠️ E l'editor workflow è un iframe che l'automazione browser non può pilotare: i
workflow li monta il consulente/cliente a mano (2 minuti).

La catena (tutta collaudata):
1. **Contatto del responsabile** in GHL (tag `staff-interno`).
2. **Template Utility** `avviso_staff_<cliente>`: corto, SENZA variabili ("C'è una
   nuova richiesta da gestire nelle chat del <Locale>. Apri le Conversazioni per
   rispondere."), niente header. Approvazione Meta in minuti (trappole → skill
   `whatsapp-ghl-locale/references/trappole-template.md`).
3. **Scenario Make** `RBR-Handover-Alert-<Cliente>` (modello: id 7237855, org Mister
   Pizza, cartella RBR): schedule 10 min → HTTP POST `contacts/search` con filtro
   `tags eq "human handover"` → (filtro: total>0) → POST tag `avvisa-<responsabile>`
   sul contatto del responsabile → iterator sui clienti trovati → POST tag
   `handover-avvisato` + DELETE tag `human handover`. Auth: Private Integration
   dedicata (scopes contacts r/w + conversations r/w). ⚠️ Trappola Make: `timeout`
   del modulo http è un NUMERO, non stringa. Segui `make-scenario-dod` (backup,
   validate, test con contatto finto `@rbr-test.local`, activate + isPaused/isinvalid).
4. **Workflow GHL 3 blocchi** (lo monta il cliente): trigger Contact Tag added
   `avvisa-<responsabile>` → azione WhatsApp template avviso (⚠️ "Enable branches"
   OFF: serve solo ai template con pulsanti) → Remove tag (riarma l'avviso).

Semantica: l'avviso è un **campanello, non il registro** — più handover ravvicinati =
un campanello solo, e va bene: le richieste vivono in GHL (assegnate + task), non nel
tag. Latenza massima = intervallo della vedetta.

## Fase 6 — Collaudo e accensione

Ordine di accensione: prima i canali SENZA autorisponditori legacy, poi il resto dopo
averli spenti. Collaudo dal telefono del titolare (3 messaggi):
1. "Avete posto stasera?" → solo link col source giusto (~15 sec)
2. domanda su un piatto → descrizione+prezzo dalla KB (~15 sec)
3. richiesta da handoff (es. "8 pizze d'asporto") → presa in carico + handover +
   campanello al responsabile entro l'intervallo vedetta.
Poi fai riprovare il titolare **da cliente**: le correzioni di tono vere escono solo lì.
Nota: dopo un handover il bot dorme 8h su quella chat (normale).

I messaggi arrivati PRIMA del deploy non vengono recuperati dal bot: chiudili a mano
(solo quelli inerenti a oggi/futuro).

## Fase 7 — Audit del primo giorno (obbligatorio)

A fine giornata rileggi TUTTE le conversazioni post-accensione (subagent con MCP GHL):
latenze, tono, handover, buchi. Lezioni dal primo giorno Noolas (42 conversazioni,
latenza media 11,7 sec, 12 handover — e 4 magagne trovate solo così):
- **Numero mittente ≠ numero in scheda**: se il cliente scrive da un numero diverso da
  quello salvato sul contatto, le risposte del bot partono verso il numero in scheda e
  risultano **failed** (mai consegnate). Non è risolvibile da prompt: va monitorato
  (filtrare i messaggi failed) e il contatto va riallineato a mano.
- **Il bot può contraddire lo staff**: se una persona risponde a mano nella chat e il
  cliente riscrive, il bot riparte e può smentire lo staff ("La aspettiamo!" dopo un
  "tutto pieno" umano). Mitigazione nel prompt (MAI contraddire lo staff), ma il
  monitoraggio resta umano.
- **Disdette narrative**: "purtroppo abbiamo avuto un lutto" È una disdetta anche senza
  la parola disdire — nel prompt la regola va scritta esplicita, o il bot fa le
  condoglianze e il tavolo resta occupato.
- **Messaggi ambigui/flirt**: senza una regola, il bot asseconda ("faremo il possibile
  per farla stare bene"). Regola: neutro, cortese, poi staff.
- **Invenzioni di stato**: senza divieto esplicito il bot può dire "il sistema risulta
  chiuso". Regola nel MAI: niente affermazioni non verificabili, manda il link.
- **Link copiati dalla storia**: se in chat circolano vecchi link con source sbagliato,
  il bot può copiarli — imporre "ESCLUSIVAMENTE il link del tuo canale".

## Costi (ordini di grandezza verificati)

Add-on WhatsApp 15 $/mese + conversazioni Meta (~0,03 $ a utility) + Conversation AI
a risposta (~0,02 $) + Make (~2-5k ops/mese la vedetta). Un locale da ~1.200
conversazioni WhatsApp/mese: **indicativamente 15-40 $/mese totali**. Si controlla in
Settings → Billing → Wallet & Transactions.

## Il criterio che sta sopra a tutto

Il bot non è un giocattolo AI: chiude il buco delle richieste senza risposta (sul
Noolas il 43% delle chat moriva così) e **si misura in persone che entrano** —
prenotazioni dal link col source del bot, disdette salvate, richieste che arrivano
alla sala. Ogni risposta deve finire lì.
