# Conversation AI (bot di risposta) su GHL

Setup base dell'agente e knowledge base: `suite/quality/ghl_procedura_team_rbr.md` (sezione
Conversation AI). Qui le regole imparate sul campo.

## 1. Auto-Pilot NON basta: serve il Deploy

(contributo di Andrea, 10/09/2026)

Nel nuovo AI Agents (Conversation AI 2.0), Mode = Auto-Pilot + canali in "Contact Assignment
Channels" NON fa rispondere il bot: quella selezione vale solo per i bot assegnati via workflow.
Per l'auto-risposta serve la tab **Deploy** (in italiano "Implementa") dell'agente: **Configure** su
ogni canale (WhatsApp → numeri, IG/FB → pagine) e **Update**. Senza deploy il bot è un motore acceso
in folle.

- Nel Deploy per canale c'è "Doesn't have tags" = esclusione contatti per tag (whitelist staff).
  I tag creati solo via API non compaiono nel widget finché non esistono nel registro tag della
  location: creali prima da Impostazioni → Tag.
- "Sviluppa" e "Implementa" NON sono bozza/pubblicato: "Implementa" è solo l'elenco dei canali.
  **Il prompt salvato è GIÀ LIVE** sui canali deployati (contributo di Luciano Purpi, 19/09/2026).
  Non esiste una bozza: testa le modifiche al prompt prima di salvarle.

## 2. Prompt: mai offrire l'alternativa al self-service

(contributo di Andrea, 10/09/2026)

Nel prompt di un bot di prima risposta non far mai offrire proattivamente l'alternativa al link di
prenotazione ("se ha difficoltà ci scriva"): i clienti la usano come scappatoia e il self-service
muore. Il bot manda SOLO il link; la raccolta dati manuale scatta unicamente se è il cliente a
dichiarare che non riesce. Testato: con la regola nel prompt il comportamento è esatto in entrambi
gli scenari.

Link di prenotazione con source dedicato per canale (`?source=bot-whatsapp`, `bot-instagram`,
`bot-facebook`) per misurare cosa porta l'automazione.

## 3. Bot che prenota: attesa, svuotamento, controllo umano

(contributo di Luciano Purpi, 19/09/2026)

Far prendere una prenotazione al bot e farla finire sul gestionale richiede accorgimenti non ovvi:
se mancano si perdono tavoli in silenzio.

1. **Dove sta l'agente:** `/v2/location/<loc>/ai-agents/conversation-ai/agent/<id>`. La rotta
   `/settings/conversation_ai` NON esiste e risponde con body vuoto (sembra la pagina bianca da
   scheda nascosta, ma `document.hasFocus()` è true: non lo è). Il prompt è un editor ProseMirror:
   `querySelectorAll('textarea')` non lo trova, si legge da `.ai-prompt-editor__prosemirror`.
   Per sostituirlo: scrivi su file, metti in clipboard con
   `osascript -e 'set f to POSIX file "/percorso/prompt.txt"' -e 'set the clipboard to (read f as «class utf8»)'`,
   clic nell'editor, cmd+a, cmd+v, Salva.
2. **L'azione "Informazioni di contatto" aggiorna SOLO I CAMPI VUOTI.** Se non svuoti i campi a fine
   flusso, la seconda prenotazione dello stesso cliente riusa data e coperti della prima.
   Svuotamento in UN solo nodo: "Aggiorna il campo del contatto" → Tipo di azione "Cancella dati
   campo" → poi "Aggiungi campo" per ciascuno (il link non risponde finché non scegli il tipo di azione).
3. **Attesa di 1-2 minuti PRIMA del webhook.** Il bot può chiamare "Attiva un flusso di lavoro" nello
   stesso turno in cui "Informazioni di contatto" scrive i campi: senza attesa il webhook legge
   campi vuoti e la prenotazione si perde senza errori.
4. **Non esiste un ramo di fallimento:** il Se/Altrimenti di GHL non espone la risposta del webhook.
   La notifica allo staff deve dire "dovrebbe essere sul gestionale, se non la trovi inseriscila a
   mano", non "è stata inserita". Notifica via EMAIL, non SMS (vedi `suite/memory/gohighlevel.md`).
5. **URL del webhook:** copiandolo con cmd+c compare un `?` finto dopo ogni chip di variabile: è un
   artefatto della copia, non è nel valore salvato. Non "correggerlo" (cancellando distruggi un chip).
   La verità sta nel **registro di esecuzione**, che mostra richiesta e risposta per intero.
