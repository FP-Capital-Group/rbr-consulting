---
name: contribuisci-conoscenza
description: Condivide col team RBR quello che questo Claude ha imparato — nuove procedure, fix, trucchi, pattern sui clienti — scrivendolo nello Sheet "RBR - Contributi conoscenza" su Drive (via service account). I contributi vengono fusi ogni lunedì nel plugin condiviso e distribuiti a tutti. Usa quando l'utente dice "condividi quello che ho imparato", "salva questa procedura per il team", "questo va nel cervello comune", quando risolvi qualcosa di non documentato nelle skill, e SEMPRE PRIMA di aggiornare il plugin a una nuova versione (per non perdere gli apprendimenti locali).
---

# Contribuisci conoscenza (il cervello condiviso RBR)

Il plugin è la memoria condivisa del team: quello che UN consulente impara deve
arrivare a TUTTI. Questa skill è il canale di andata; la routine settimanale fonde i
contributi nel plugin e il lunedì tutti ricevono l'aggiornamento.

## Quando attivarla (anche senza che l'utente lo chieda)

- Hai appena risolto qualcosa che le skill non documentavano (procedura, trappola,
  fix, pattern di un gestionale/piattaforma)
- L'utente ti corregge su un metodo e la correzione vale per tutto il team
- **Prima di aggiornare il plugin a una versione nuova**: chiedi all'utente "c'è
  qualcosa che abbiamo imparato e non ancora condiviso?" ed esporta prima di aggiornare
- L'utente lo chiede esplicitamente

## Procedura

1. **Distilla il contributo** (non un log di sessione — una procedura riutilizzabile):
   - Titolo (una riga)
   - Area: quale skill/tema tocca (es. foodcost-cliente, cdg-fatture, GHL, Pienissimo…)
   - Contenuto: il metodo in passi, con i dettagli concreti (ID, endpoint, formule,
     condizioni). Scrivi come se lo leggesse un collega che non c'era.
   - Se riservato/specifico di un cliente: anonimizza o segnala "solo per <cliente>".
2. **Mostra la bozza all'utente** e chiedi conferma (🟡) — è lui l'autore.
3. **Invia**: esegui `scripts/aggiungi_contributo.py` (nella cartella di questa skill):
   `python3 aggiungi_contributo.py "<autore>" "<area>" "<titolo>" "<contenuto>"`
   Lo script trova lo Sheet "RBR - Contributi conoscenza" su Drive via service account
   e aggiunge una riga con stato `nuovo`. Richiede `pip3 install gspread google-auth`.
4. **Conferma** all'utente: ✅ contributo inviato, verrà integrato nel plugin col
   prossimo aggiornamento del lunedì (report su Telegram a Marco).

## Regole

- Un contributo = un concetto. Tre cose imparate = tre righe separate.
- Niente segreti nuovi nel contenuto (token, password): quelli passano da Marco.
- Non modificare MAI le skill del plugin in locale: le modifiche si perdono
  all'aggiornamento successivo. Il canale è SOLO questo.
- Se lo Sheet non esiste o il service account non lo vede: segnala a Marco (⚠️) e
  salva il contributo in un file locale come backup da inviare a mano.
