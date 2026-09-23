# Configurazione dell'agente su DeepAgent

Editor: `platform.deepagent.app` → Agenti → Opzioni → **Modifica**. Le schede
sono **Identità, Personalità, Voce, Azioni, Telefono, Istruzioni**.

## Baseline verificata

Questi valori sono identici su tutti gli agenti in produzione. **Allineati a
questa baseline** invece di improvvisare: se un agente nuovo se ne discosta,
deve esserci un motivo.

| Dove | Impostazione | Valore |
|---|---|---|
| Identità | Tipo di agente | **Inbound** |
| Identità | Lingua primaria | Italiano, + secondarie (inglese, spagnolo, francese…) |
| Personalità | Tono | Professionale e Formale |
| Personalità | Settore | Sales |
| Personalità | Competenze | Supporto Clienti + Fissare Appuntamenti |
| Azioni | Raccolta dati | nessun campo personalizzato |
| Azioni | Chiedi consenso alla registrazione | OFF |
| Azioni | Invio dati chiamata a webhook | OFF |
| Telefono | Abilita Registrazioni | ON |
| Telefono | Abilita Trascrizioni | ON |
| Telefono | Durata massima inattività | 21 secondi |
| Telefono | Limita durata chiamata | 15 minuti |
| Istruzioni | Modalità Avanzata | ON |
| Istruzioni | Primo messaggio non interrompibile | ON |

Con la Modalità Avanzata attiva, Tono e Competenze incidono poco: il
comportamento vero è tutto nel prompt. Restano allineati per non introdurre
differenze inspiegabili fra un agente e l'altro.

## 1. Identità

- **Nome Agente**: il nome del locale.
- **Descrizione**: personalizzala sul locale invece di lasciare quella generica
  ereditata dalla copia. Serve a te, non al cliente: deve dire cosa fa
  l'agente, su quale gestionale scrive, e cosa passa all'operatore. Esempio:
  *"Assistente per le prenotazioni dei tavoli di Red Mike, pizza burger e grill
  ad Alghero. Verifica la disponibilità su Resmio e registra la prenotazione;
  passa all'operatore i gruppi oltre 8 persone, l'asporto, le consegne, gli
  eventi e le modifiche."*

## 2. Voce

Scegli una voce coerente col posizionamento e con la clientela. **Attenzione
alle voci con accento marcato**: nel catalogo alcune sono etichettate col
carattere (per esempio "Roberta (Coatta)", romanesco) e stonano su un locale di
un'altra regione o con clientela internazionale.

**Il nome della voce nel catalogo e il nome che l'agente si dà sono due cose
diverse.** L'etichetta della voce (Lara, Roberta, Susi...) è interna, il cliente
non la sente mai: si può cambiare voce senza toccare il prompt. Quello che deve
coincidere sono i **nomi pronunciati**: il nome nel *primo messaggio* e quello
in `<identity>`. È l'incoerenza più frequente nelle copie — ne abbiamo trovata
una con tre nomi diversi nello stesso agente.

**Cambiare voce non salva al primo colpo.** Il tile della voce va cliccato sul
riquadro, non sull'immagine (l'immagine fa partire l'anteprima), e poi va
premuto Salva. Verifica sempre riaprendo la scheda **e** guardando la voce
riportata nella pagina di dettaglio dell'agente: capita di credere di aver
cambiato voce e trovare ancora quella vecchia.

## 3. Azioni — la parte critica

L'agente usa solo i tool collegati qui:

- `get_disponibilit_<slug>` — verifica disponibilità (data in formato AAAA-MM-GG).
- `set_prenotazione_<slug>` — registra la prenotazione.
- `transfer_to_human` — trasferimento all'operatore.
- `end_call`, `skip_turn` — chiusura e ascolto.

**Controlla sempre due cose:**

1. **Lo slug nei nomi dei tool** è quello del locale corrente, non ereditato da
   una copia.
2. **L'URL dei tool.** Se coincide con quello di un altro locale, le
   prenotazioni possono finire nel sistema sbagliato. Non modificarlo se
   l'integrazione l'ha fatta qualcun altro: fatti dire qual è il campo che
   smista e mettilo nel prompt.

**Trasferisci a Umano**: verifica numero e condizioni. In una copia trovi i
numeri e le condizioni del locale precedente — vanno sostituiti tutti. Il
numero deve essere **diverso** da quello che verrà deviato sull'agente.

Le sezioni *Raccolta dati*, *Consenso* e *Azioni post-chiamata* restano come da
baseline: non servono per un agente di prenotazione.

## 4. Telefono

Scegli il numero — **dopo averlo chiamato** (vedi `scheda-locale-esempio.md`: un numero scelto a catalogo rispondeva a un terzo) — e
verifica in *Telefonia* che, a deploy fatto, la colonna Agente riporti il nome
dell'agente. Finché l'agente è in bozza risulta "Non Assegnato" anche se
selezionato: è normale.

## 5. Istruzioni

- **Modalità Avanzata** attiva, prompt compilato incollato, nessun `{{...}}`.
- **Obiettivo principale**: elenca TUTTI gli esiti buoni (prenotazione registrata,
  operatore, ordine indirizzato al canale giusto, informazione data corretta) e i
  fallimenti — testo standard in SKILL.md §6. Con il solo "prenotazione oppure
  operatore" il tasso di successo misura la quota di chiamate che sono prenotazioni,
  non la qualità dell'agente.
- **Primo messaggio**: coerente col nome della voce.
  *"Ciao, sono {{NOME_ASSISTENTE}}, l'assistente virtuale AI di {{NOME_LOCALE}}.
  Come posso aiutarti?"* — la formula usata su tutti gli agenti.

## 6. Knowledge base

Opzionale. Un agente di prenotazione non recita il menù al telefono, quindi
serve solo se il locale vuole risposte su documenti specifici.

## 7. Collaudo

Dopo il deploy, chiamando il numero DeepAgent dal proprio cellulare.

1. **Prenotazione semplice** entro la soglia → verifica, riepiloga con giorno
   della settimana + data, registra, chiude.
   **→ Poi controlla il gestionale: la prenotazione deve essere lì.** È il test
   che conta. Se non c'è, cercala nel gestionale del locale da cui l'agente è
   stato copiato.
2. **Richiesta mista** (tavolo + qualcosa da operatore) → prima registra il
   tavolo, poi annuncia il trasferimento dicendo che la prenotazione è
   confermata.
3. **Gruppo oltre la soglia** → annuncia il trasferimento e passa all'operatore
   senza raccogliere i dati.
4. **Orario fuori turno** → lo dice subito e riporta il cliente in fascia,
   prima di chiedere qualunque dato.
5. **Slot non disponibile** → propone un'alternativa verificata.
6. **Cambio lingua a metà chiamata** → segue il cliente senza annunciarlo.

Solo quando tutti e sei si comportano come previsto si passa alla deviazione
del numero del locale.
