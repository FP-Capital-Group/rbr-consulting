---
name: personale-oggi-domani
description: Trasforma una nuova organizzazione dei turni (griglia proposta per locale) in una tabella persona per persona «oggi → domani» da portare in riunione col titolare — accordo attuale stimato dai cedolini, ore pagate reali, turno di oggi, turno proposto, quanto cambia e cosa serve — e, se richiesto, ottimizza le ore togliendo SOLO le mezz'ore in perdita (incasso per ora lavorata sotto soglia). Usala quando il consulente dice "cosa cambia per ogni dipendente", "fammi la tabella persone oggi e domani", "incrocia i turni proposti con i cedolini", "chi resta scoperto con i nuovi turni", "togli le ore che non rendono", "arriva a X euro di costo del personale", "prepara il file per la riunione sul personale". Parte dopo mappa-turni e analisi-modello-business.
---

# Personale: oggi → domani

> Metodo nato su Cartabianca (catena di 11 locali, Firenze, 24/09/2026): 120 persone, file
> consegnato per la riunione col titolare, poi versione ottimizzata con −125 h/sett.
>
> (contributo di Andrea Chirivì, 12/10/2026)

## Perché esiste
Una griglia turni ottimizzata dice «servono 30 ore in meno al bar di X». Il titolare invece
pensa per nomi: «e Rossi cosa fa?». Finché il piano non diventa una riga per persona, la
riunione si blocca. Questa tabella rende il piano discutibile e applicabile.

## Prerequisiti (fonti)
1. **Cedolini** degli ultimi 4-5 mesi (per ore ordinarie, straordinari, tipo contratto).
2. **Griglia di oggi** (turni reali per locale, con i nomi).
3. **Griglia di domani** (turni proposti per locale: dal file di ottimizzazione o dal file del cliente).
4. Se si ottimizza: **incasso per mezz'ora** per locale (dal gestionale di cassa, `analisi-venduto-fasce`).
5. **Scadenze dei contratti a termine** (dalla tabella dello studio paghe o dal file monte ore del
   cliente) e presenze/timbrature dell'ultimo mese.

## Procedura
1. **Abbina i nomi** griglia → cedolino a mano, in un file di mapping: le griglie hanno nomi scritti
   male o solo il nome di battesimo (Bordoni = Mordoni, Solu = Tolu…). Chi non ha cedolino va segnato.
2. **Accordo attuale** per persona = ore da contratto **stimate**: 75° percentile delle ore ordinarie
   mensili ÷ 4,33. «CHIAMATA» nel nome del contratto = a chiamata. Dichiaralo come stima. Aggiungi la
   colonna **Scadenza** accanto all'accordo stimato.
3. Chi scade prima che parta lo schema nuovo è il primo punto in cui lo schema si adatta: non
   rinnovo, rinnovo con ore diverse o profilo nuovo da aprire — non va per forza rimpiazzato con una
   persona uguale. È la leva più forte perché si decide PRIMA dei rinnovi e non dopo: porta la
   tabella al titolare prima della prima scadenza.
4. **Assegna i turni di domani** in quest'ordine:
   chi è già nel locale fino alle sue ore di contratto → chi è in busta ma fuori griglia → chi oggi fa
   straordinario → rete (stesso reparto e tipo di locale, chi ha ore libere) → jolly → chiamata →
   posti DA ASSEGNARE. Chi c'è oggi ma non nelle schede di domani → posto DA ASSEGNARE/JOLLY più simile.
5. **Tabella** (tab nel file del cliente, non in un file nuovo): COGNOME Nome · locale · accordo ·
   turno oggi · turno domani · **Quanto cambia** (numero, per filtrare) · **Cosa cambia** (una frase
   semplice, leggibile dal titolare). Esiti con simboli: ✅ uguale 🔁 spostato 🟡 meno ore ➕ più ore
   🔴 da decidere ⚪ uscito ❔ senza cedolino · **⏳ in scadenza** (facoltativo).
6. **Sintesi per locale** in testa: ore di contratto vs ore proposte, scoperti, persone in eccesso.

## Ottimizzazione «solo ore in perdita»
### Ordine del lavoro
1. Prima si decide quante unità lavorative servono in ogni turno, reparto per reparto (dal File 03,
   vedi `analisi-modello-business` §3-4).
2. Solo a organico deciso si disegnano ingressi e uscite **a scalare**: tutti presenti solo nel
   momento di punta, chi fa la preparazione entra prima, chi fa chiusura e pulizie esce dopo.

Il taglio delle mezz'ore sotto soglia (sotto) viene DOPO questi due passi, non al loro posto.

Quando il cliente chiede un tetto di costo (es. «arriva a 500k»):
- Calcola per ogni mezz'ora l'**incasso per ora lavorata** (IVA esclusa: cassa ÷ 1,1); togli ore SOLO
  dove è sotto soglia (su Cartabianca < 18 €/h), prima dai posti vuoti, poi dai DA ASSEGNARE.
- Non copiare la soglia da un altro locale: su Cartabianca era 18 €/h, ma va ricalcolata caso per
  caso (criterio di calcolo da confermare con l'autore della skill prima di fissarlo come regola).
- Usa il numero anche al rialzo: dove l'incasso per ora è molto sopra la media con poche persone in
  schema, valuta di aggiungere, non solo di togliere (caso: media 18-19 €/h ma 101 €/h con 2 persone
  tra le 21 e le 22).
- Vincoli fissi: mai toccare apertura, chiusura, preparazione; turni ≥ 3 h; mai locale vuoto.
- Nessun contratto cambia: le ore tolte a chi ha un nome si recuperano dai posti DA ASSEGNARE.
- Lavora su una **copia** del file (backup intatto), celle cambiate in rosso con commento «Prima: …».
- Se il tetto richiede di tagliare ore che incassano bene (25-36 €/h), NON farlo: mostra il numero
  raggiungibile e cosa costerebbe andare oltre. Ricontrolla sempre che cosa comprendeva il «tetto»
  originale (su Cartabianca i «500k» includevano un locale stagionale).

## Regole RBR & trabocchetti
- Nomi SEMPRE COGNOME + nome dal cedolino, mai solo il nome della griglia.
- Le **teste** si contano dal payroll, la griglia serve per la % di taglio e per il «dove».
- Un FT da 40 h copre ~34,5 h/sett reali (ferie, festività, malattia): FTE ≠ persone.
- File .xlsx su Drive: riscaricalo subito prima di scrivere e confronta `modifiedTime` prima di
  ricaricarlo (vedi regola «mai sovrascrivere un xlsx aperto»). Backup in `_archivio/` ogni volta.
- Tieni il file semplice per il titolare (7 colonne); i dettagli di calcolo in un tab separato.
- Incrocia l'ultima presenza/timbratura con la data di scadenza o di cessazione. Se qualcuno
  risulta in turno dopo la scadenza, o è cessato ma risulta ancora pagato, segnalalo al titolare
  come rischio da chiarire con lo studio paghe (proroga non ancora registrata? lavoro senza
  contratto?), senza giudizi legali. Prendi le scadenze da UNA fonte sola e dichiarala: può
  succedere che la stessa persona abbia scadenze diverse in liste diverse.
- Prima di proporre di cambiare il mix fra contrattualizzati e a chiamata/extra, calcola il costo
  per turno per tipo di contratto nello stesso mese (pagato ÷ turni censiti), sulla STESSA base per
  tutti (dichiara se netti, netti+extra o costo pieno). Se i valori coincidono, cambiare il mix non
  fa risparmiare: la leva è quante persone ci sono in sala per sera, non il tipo di contratto.

## Definition of Done
- [ ] Ogni persona in busta ha una riga (o è segnata come uscita/senza cedolino)
- [ ] Mapping nomi salvato, stime dichiarate come stime
- [ ] Colonne «Quanto cambia» e «Cosa cambia» compilate, sintesi per locale in testa
- [ ] Scadenze incrociate con lo schema nuovo e con le presenze, anomalie segnalate
- [ ] Se ottimizzato: copia con celle in rosso + commento, backup, numero raggiunto vs richiesto spiegato
