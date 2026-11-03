# Formati dei cedolini e fonti da cui scaricarli

Richiamato da SKILL.md §1 "Raccogli e ordina" e §2 "Estrai il testo grezzo". Le coordinate e i percorsi qui sotto sono tarati sui clienti verificati finora: **vanno ricontrollati a ogni layout nuovo dello studio paghe o del portale**, e le coordinate verificate a mano su una busta prima di un'estrazione in blocco (confronta sempre il totale dei netti estratti col riepilogo del PDF).

## Schede per software paghe

### TeamSystem / EPAGHE
File tipico: `PG<codice ditta><MM><AA>.PDF`. **Non è una busta singola**: è il libro paga completo del mese, con un cedolino per dipendente. Ogni cedolino è stampato **due volte** (il blocco si ripete) e in fondo ci sono pagine di riepilogo senza nome — in un caso reale, 98 pagine doppie su 196 totali. Si estrae solo il primo blocco di ogni nome.
- I file "speciali" possono essere la 14ª (si tengono, sono un mese a sé) o riemissioni (si escludono, altrimenti il mese si duplica).
- Lettura posizionale con `pdfplumber.extract_words`: il nome sta in alto, y ≈ 108-114, con x0 fra 293 e 443.
- Il **netto** è il valore allineato sotto la label `BUSTA` (stesso x0, ~14 punti più in basso). **Non è sotto `NETTO`**, che su questo layout porta sulla colonna ROL.

### Zucchetti
Testo estraibile normalmente. Il netto è l'importo isolato su una riga propria, subito prima della parola "Contatori". Controllo di coerenza: netto ≈ 80% del lordo.

### Centro Paghe
Il netto è in posizione fissa: x ≈ 500-575, y ≈ 715-735. Si estrae per coordinate.

## PDF cifrati da password
Si apre con `pikepdf(path, password=...)` e si salva una copia decrittata nella cartella privata del cliente (mai condivisa). La password dipende dallo studio paghe — non esiste una regola unica valida per tutti i clienti. Tentativi in ordine:
1. codice ditta (cifre dopo "PG" nel nome file TeamSystem);
2. codice fiscale / P.IVA della società datrice;
3. altre varianti note solo provando (capitato su almeno un cliente: una parola diversa, trovata per tentativi).

Se nessuna apre, si chiede UNA volta al consulente del lavoro o al cliente, invece di far sbloccare ogni file a mano. La password non si scrive mai nei file condivisi, nel plugin o nei report: solo nella memoria privata del cliente.

## Da dove arrivano i cedolini: portale paghe (es. Dipendenti in Cloud)

Se il cliente usa un portale paghe/presenze come Dipendenti in Cloud (`secure.dipendentincloud.it`), all'avvio della skill chiedi un accesso con ruolo **amministratore**: da quel momento cedolini e timbrature si scaricano direttamente, senza aspettare che il cliente li inoltri uno per uno. Il percorso nell'interfaccia va riverificato al primo uso su un cliente nuovo (può cambiare).

Percorso tipico: **Esporta → Buste paga → Richiedi esportazione**, con intervallo Da/A di un anno alla volta. Imposta "Seleziona tutti" sia sulle mensilità sia sui dipendenti.

**Trappola 1 — cessati esclusi di default**: l'export di default prende solo i dipendenti attivi e perde i cessati, sottostimando costo e turnover. L'export è asincrono: prima di richiederlo di nuovo controlla in "Download", spesso è già pronto.

**Trappola 2 — tredicesime assenti dall'export PDF**: anche se compaiono nel pannello, le tredicesime NON escono come PDF dall'export normale. Vanno lette dal pannello o chieste allo studio paghe. Prima di annualizzare, conta le mensilità per dipendente contro la "Lista buste paga" (xlsx) che esce con l'export, per accorgerti se mancano.

Altri elementi utili del portale:
- **Lista dipendenti** (gruppo, mansione, attivo/cessato): serve per fissare il perimetro per sede (SKILL.md §5) e per il turnover.
- **Timbrature**: export asincrono, un foglio per dipendente con ingressi e uscite — è la fonte delle ore lavorate e quindi del costo orario reale. Attenzione: la vista della settimana in corso può sembrare vuota o "in discrepanza" anche quando l'export completo restituisce mesi di dati pregressi corretti. Prima di scartarle o usarle, confronta sempre con le griglie turni del locale.
- **Modulo "Gestione turni"** del portale: spesso vuoto, perché i turni reali vivono altrove (Word, WhatsApp). Non usarlo come fonte senza averlo verificato.
- **Avvisi mail sui contratti a termine**: il portale manda avvisi a 30 giorni, 7 giorni e il giorno stesso della scadenza — il problema reale, quando succede, di solito non è la mancanza di avviso ma che nessuno decide in tempo.

(contributo di Andrea Chirivì, 2026-10-12 — confermato su un solo cliente, export del 02/09/2026 e timbrature del 28/09/2026)
