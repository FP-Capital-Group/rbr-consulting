---
name: risposte-recensioni-ai-ghl
description: Attiva e calibra le risposte automatiche alle recensioni Google di un ristorante con Reviews AI di GoHighLevel (Reputation) — collegamento schede GBP, agente con prompt RBR multilingua e SEO, tono, attesa, blocco delle recensioni sensibili, smaltimento dell'arretrato in Drip Mode. Usala quando il consulente dice "rispondi in automatico alle recensioni", "attiva Reviews AI", "il cliente ha 1.500 recensioni senza risposta", "copia il risponditore di Mister Pizza su X", "le risposte alle recensioni sono tutte uguali", "sistema il prompt delle recensioni". Metodo nato su Mister Pizza e replicato su Raíces (set 2026).
---

# Risposte automatiche alle recensioni con Reviews AI (GHL)

## Perché esiste
Rispondere alle recensioni fa SEO locale (Google legge le risposte), mostra un locale vivo
e recupera i clienti scontenti. Quasi nessun ristoratore lo fa con costanza: su Raíces
c'erano ~1.600 recensioni, 1.576 senza risposta. Reviews AI di GHL lo fa da solo, ma con il
prompt di default risponde in inglese, sempre con la stessa frase, e a volte ammette colpe
che il locale non ha. Questa skill è il modo RBR di accenderlo senza rischi.

## Quando usarla
- Cliente con sub-account GHL e schede Google Business collegate (o da collegare).
- Arretrato di recensioni senza risposta, o risposte fatte a mano in modo irregolare.
- Per l'ANALISI delle recensioni (punti forti/deboli, piano) usa invece `analisi-reputazione-locale`.

## Prerequisiti
1. Sub-account GHL del cliente operativo (`onboarding-cliente-ghl`) e istanza MCP `ghl2-<cliente>`.
2. Schede GBP collegate in GHL (Settings → Integrations → Google). Le schede devono stare su un
   account Google a cui RBR ha accesso (di solito quello del consulente come gestore).
3. Dal cliente: nome con cui firmare (es. «Cesar - Raíces»), nomi ufficiali dei locali, piatti firma,
   mail per i problemi concreti. Chiedile tutte in un solo messaggio.

## Procedura
1. **Reputation → Settings → Reviews AI** → modalità **Auto Responses** (non «Suggestions»).
2. **Agente**: parti da quello di un cliente già calibrato (Mister Pizza) e ricalibralo; non
   partire dal prompt di default. Campi: nome agente («Risponditore Recensioni <Cliente>»),
   business name, tono **Friendly + Solution-Oriented**, voce «We», firma nel campo firma
   (NON nel prompt: il prompt vieta firme per evitare doppioni).
3. **Prompt** — struttura RBR (modello completo in `prompt-modello.md`):
   - LINGUA: quella della recensione; se è solo stelle, dedotta dal nome (nome italiano → italiano,
     nome chiaramente straniero → quella lingua, altro alfabeto latino → inglese). Una sola lingua per risposta.
   - REGISTRO: «tu» di default in IT/ES/FR/PT, formale solo con recensioni polemiche; tedesco sempre «Sie».
   - IDENTITÀ: nomi ufficiali dei locali (mai soprannomi di zona), cosa è il locale in una riga.
   - SEO: ripetere il piatto che il cliente ha lodato col nome giusto + al massimo 1-2 keyword
     locali («tacos de birria», «ristorante messicano a Firenze») solo se ci stanno. Zero keyword nelle negative.
   - VARIETÀ: aprire e chiudere in modo diverso, le risposte stanno una accanto all'altra.
   - NEGATIVE (≤3 stelle): ringraziare, dispiacersi per come è andata, MAI ripetere l'accusa come
     fatto («ci spiace che abbiate aspettato», non «ci spiace di aver dimenticato l'ordine»), mai
     promettere rimborsi/sconti/azioni, mai scuse operative inventate. Invito alla mail SOLO se c'è
     qualcosa di concreto da verificare (conto, ordine, allergia, prenotazione, persona dello staff).
   - DIVIETI: telefoni, indirizzi, promo, sconti, riferimenti all'automazione, frasi vuote
     («saremo più attenti», «lavoreremo per»).
4. **Sicurezza**: **Hold sensitive reviews = ON** (le risposte rischiose aspettano revisione umana).
   Attesa agente 1 min; attesa globale come Mister Pizza (15 min) — si imposta a mano.
5. **Arretrato**: crea una regola **Drip Mode** (es. tutti i giorni 9-17) per le recensioni vecchie,
   così non escono centinaia di risposte nello stesso minuto. Senza Drip l'arretrato non si smaltisce.
6. **Test**: fai generare 5 risposte di prova su recensioni reali (1 positiva con testo, 1 solo stelle,
   1 straniera, 1 negativa concreta, 1 negativa di gusto) e controllale contro le regole prima di attivare.
7. Salva il prompt finale nei file del cliente (`data/<cliente>/marketing/reviews_ai_prompt_<cliente>.txt`).

## Regole RBR & trabocchetti
- La tendina della **lingua di riserva** resta su English e non si cambia in automazione: falla a mano.
- Le risposte manuali restano possibili: da GBP, `google.com/local/business/<ID>/customers/reviews`
  (fuori dall'iframe della ricerca la tastiera funziona) → Rispondi → rientrare dalla lista dopo ogni invio.
- Mai frasi tipo «lascia una recensione e hai lo sconto»: vietato da Google.
- Il prompt copiato da un altro cliente va ripulito da TUTTI i nomi (locali, piatti, firma, mail).

## Definition of Done
- [ ] Auto Responses attivo, schede di tutti i locali collegate
- [ ] Prompt ricalibrato (lingua, registro, nomi locali, piatti, mail) e salvato nei file cliente
- [ ] Hold sensitive ON, firma nel campo firma, attese impostate
- [ ] Drip Mode per l'arretrato creato (o deciso con Marco di non farlo)
- [ ] 5 risposte di prova controllate e mostrate al consulente
