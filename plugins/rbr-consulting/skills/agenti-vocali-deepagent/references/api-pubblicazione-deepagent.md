# DeepAgent: leggere, salvare e pubblicare via API interna

Procedure dalla sessione già loggata su `platform.deepagent.app` (console del browser: le
chiamate ereditano i cookie). Utili perché l'editor dell'agent-builder è lento e i click
spesso non attecchiscono. (contributi di Luciano Purpi, 04/09, 09/09 e 12/09/2026)

## Elenco agenti e lettura di un prompt

- **Id e nomi di tutti gli agenti in una chiamata:** `GET /api/trpc/agent.list?input={"json":{}}`.
  Risponde `{items,total,page,pageSize,totalPages}`, non un array. `agentBuilder.getAll`
  risponde 404 e `agentBuilder.list` 500: quello buono è `agent.list`.
- **Configurazione di un agente:** `GET /api/trpc/agentBuilder.getById?batch=1&input={"0":{"json":{"id":"<id agente>"}}}`
  → leggi `configuration.personality.agentSystemPrompt`. È l'unica prova valida che un
  salvataggio è andato a buon fine (non la textarea, non il banner).
- **Il prompt esiste in tre copie**: `personality.agentSystemPrompt`,
  `personality.agentInstructions`, `llm.systemPrompt`. Una modifica via API le sostituisce tutte e tre.

## Backup prima di una modifica di massa

Scarica tutti i prompt in un JSON unico (`agentBuilder.getById` su ogni id di `agent.list`;
con 7 agenti ~190 KB, 30 secondi). Per portarlo fuori dal browser genera un `Blob` e clicca un
`<a download>` creato al volo: il click parte anche senza gesto dell'utente e il file finisce
nella cartella download.

## Salvare nel database

`POST /api/trpc/agentBuilder.update` con `{json:{id, configuration}}`, dove `configuration` è
quella letta con `getById` con le tre copie del prompt sostituite. Poi rileggi con `getById`.

**Salvare NON è pubblicare** (sotto). Se lavori dall'editor invece che via API: scrivi nella
textarea e premi Salva in una chiamata JS **separata** (vedi SKILL.md §2).

## Modifica di massa su prompt non identici

Le stesse regole hanno formulazioni diverse da agente ad agente: non cercare la stringa lunga
esatta, taglia **fra due marker** e controlla che la distanza fra i marker sia plausibile (per il
blocco telefono, sotto i 1500 caratteri). Se è più lunga il prompt è diverso e va guardato a
mano. Dopo, verifica sul comportamento (riascolto), non solo sulla stringa.

## Pubblicare su un agente già attivo: salvato non vuol dire in onda

Su un agente **ATTIVO** tutto quello che scrivi resta solo nel database: sul motore vocale gira
la configurazione del momento dell'attivazione. **Non propagano** né `agentBuilder.update`, né
il tasto Salva, né `POST /api/trpc/elevenlabs.updateAgent` lanciato a mano (che pure risponde
200 e crea un nuovo `version_id` a ogni giro — la sua risposta non è una prova di messa in onda).

L'unica cosa che pubblica è il flusso del tasto **"Attiva agente"**:

```
POST /api/agent-builder/deploy-simple/stream
body: {"deepAgentId": "<id agente>", "allowCreate": false}
```

Con `allowCreate:false` **aggiorna l'agente esistente** senza crearne uno nuovo: così si pubblica
in produzione senza il giro del duplicato. La risposta è uno stream di righe JSON con
l'avanzamento e, in coda, l'errore vero — quello che nella UI diventa il generico "La
configurazione dell'agente è stata rifiutata".

Quattro regole (nate da due giorni di guasto su un cliente in produzione):

1. **Gli errori sono intermittenti.** `provider_rejected` ha rifiutato la stessa configurazione
   per due giorni e poi è passata al secondo tentativo consecutivo, senza interventi del supporto.
   Vale anche `service_unavailable`. Prima di dire a un cliente che una modifica è impossibile,
   riprova a distanza di minuti e di ore.
2. **La chiamata dura fino a due minuti.** Dalla console va lanciata "fire and poll" (salva la
   promise su `window` e rileggila dopo): l'esecuzione JS scade a 45 s e sembra un blocco quando
   sta lavorando.
3. **Dopo ogni pubblicazione rileggi il prompt dal motore vocale.** Un deploy lanciato mentre
   stai ancora scrivendo la configurazione pubblica la versione VECCHIA e risponde "nessun
   errore". La prova è la lunghezza del prompt in onda: se non è cambiata, rilancia.
4. **Il deploy non rompe i tool**: lascia intatti `query_params_schema`, knowledge base e numeri
   di trasferimento (a differenza di `tools.update` via API, che azzera i parametri). Verificalo
   comunque.

**Una cosa passa senza deploy: il blocco audio** (voce, velocità, stabilità).
`elevenlabs.updateAgent` pubblica quello e solo quello, con qualche ora di ritardo. Se un agente
è bloccato in pubblicazione, la voce è l'unica leva che risponde in giornata.

## Prompt lunghi, entrata e uscita

L'output JS del browser è troncato a ~1000 caratteri: per leggere un prompt da 30-40k non andare
a pezzi, scaricalo con `Blob` + `<a download>` e leggilo dalla cartella download. In entrata
l'input non è troncato: passalo in 2-3 pezzi da ~15k salvati su `window` e concatenati.
