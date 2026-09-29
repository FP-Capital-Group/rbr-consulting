---
name: cdg-gruppo-bilanci-commercialista
description: Compila e revisiona il conto economico (CDG) di un gruppo con più società e più punti vendita partendo dai bilanci di verifica del commercialista (non dalle fatture), con cassa e cedolini come riscontri — mensili ricavati dai progressivi, riparto dei costi condivisi per famiglia merceologica, regole su cosa sta fuori dall'EBITDA (investimenti, auto, affitto ramo d'azienda infragruppo), note di credito, controllo indipendente dell'EBITDA e tab «Fonti e logica». Usala quando il consulente dice "aggiorna il CDG del gruppo", "sono arrivati i bilanci del commercialista", "il CDG non torna col bilancio", "ricava agosto dai progressivi", "ripartisci i costi sui locali", "confronta quest'anno con l'anno scorso a parità di locali", "scrivi da dove vengono i numeri del CDG". Per crearlo da zero usa crea-cdg-cliente; prima dei dati nuovi sempre riconciliazione-dati-cliente.
---

# CDG di gruppo dai bilanci del commercialista

> Metodo nato su Cartabianca (4 società, 11 locali + forno, set 2026). Tutte le regole qui sotto
> sono state trovate sbagliando e correggendo: rispettale anche quando sembrano pignole.

## La fonte giusta
- **Il CDG si alimenta dai bilanci di verifica del commercialista** (un file per società per mese o
  progressivi), non dai CSV delle fatture: il piano dei conti è spesso già per punto vendita
  (ricavi, merce, affitti, alcune utenze per locale). Le fatture servono solo per il dettaglio fornitore.
- **Mensili dai progressivi**: mese = progressivo(fino al mese) − progressivo(fino al mese prima).
  Verifica: somma dei mensili = progressivo annuo al centesimo sui ricavi.
- **Personale sempre dai cedolini**: nei bilanci il personale è riclassificato e incompleto.
- **Ricavi per locale**: il commercialista = scontrini + FATTURE emesse dalla cassa, netto IVA.
  Dall'API della cassa le fatture vanno prese a parte (i report «riconciliazioni» di solito contengono
  solo gli scontrini). Netto IVA con le aliquote reali delle chiusure (10/22/4 %), mai «÷1,1» secco.

## Riparto dei costi condivisi
1. **Diretto** quando il fornitore è di un solo locale (mappa fornitori validata dal cliente).
2. **Per famiglia merceologica** (cucina, bibite, caffè, generici bar, consumo, utenze, generale) con
   le quote del commercialista, **mai a % di ricavi** (i profili dei locali sono diversi).
3. **Stagionali/nuovi senza storico**: intensità k = quota famiglia ÷ quota venduto, × venduto del mese.
4. Locali senza cassa collegata: attenzione, ricevono merce ma zero ricavi → margine illeggibile, segnalalo.

## Cosa sta fuori dall'EBITDA (decisioni Marco, set 2026)
- **Investimenti** (arredi, banchi, attrezzature, opere, consulenze di sviluppo) → riga «Investimenti
  (fuori gestione)» sotto l'EBITDA, mai nei costi.
- **Auto** (noleggi lungo termine, autostrade, telepass) fuori.
- **Affitto ramo d'azienda pagato fra società del gruppo** → fuori in tutti gli anni (vista di gruppo).
- Interessi/spese verso soci o società del gruppo → fuori (infragruppo).
- **Premi di fine anno dei fornitori** → spalmati come riduzione della merce su tutti i mesi, in
  proporzione alla merce locale-mese. **TARI** e canoni annui → spalmati sui 12 mesi.
- Rimanenze: solo se il cliente fa inventario davvero.

## Trappole verificate
- **Note di credito**: nell'export CSV dell'Agenzia delle Entrate l'imponibile delle «Nota di credito»
  è POSITIVO → vanno girate in negativo (`if "credito" in tipo and v > 0: v = -v`).
- **Fatture intestate ad altre società del gruppo** (luce, acqua, auto dei locali): vanno nel riparto,
  e controlla se l'anno prima c'erano (confronti falsati).
- Utenze del Q1 contabilizzate a feb-mar: non «stimare» gennaio, le conteresti due volte.
- Jolly/pasticceria/trasporto: se sono già dentro gli stipendi lordi, non riallocarli sopra (doppio conteggio).
- Commissioni POS: reali quando ci sono, altrimenti % media reale della rete (su Cartabianca 1,10%, non 0,68%).
- Chiudi il CDG a un mese (es. luglio) se il successivo non è completo: salva i valori del mese
  parziale in un json per rimetterli dopo.

## Controlli prima di consegnare
1. **Aggregato = Σ store** su tutte le righe e tutti i mesi (0 differenze).
2. **Controllo indipendente**: EBITDA ricostruito «solo bilanci + cedolini» vs EBITDA del CDG; se non
   coincidono comunica una **forchetta onesta** e dove sta lo scarto, non un numero finto preciso.
3. **Confronto anno su anno a parità di locali** («stessi locali» = esclusi solo quelli aperti o chiusi
   nel periodo; definiscilo per scritto). Il personale PER LOCALE spesso non è confrontabile fra anni:
   confronta i totali.
4. Backup del file prima di ogni scrittura (`_archivio/BACKUP_<file>_<data>_pre-<cosa>.xlsx`).

## Tab «Fonti e logica» (primo tab del CDG)
Perimetro, fonti per riga, metodo di riparto, decisioni del consulente con data, correzioni fatte,
quadrature, numeri chiave a formula, punti aperti. Si aggiorna a ogni revisione: è quello che
permette a un altro consulente (o al commercialista) di fidarsi dei numeri.

## Definition of Done
- [ ] Mensili ricavati dai progressivi e quadrati sui ricavi
- [ ] Regole «fuori EBITDA» applicate in tutti gli anni in modo simmetrico
- [ ] Aggregato = Σ store, controllo indipendente fatto, forchetta comunicata
- [ ] Confronto a parità di locali con perimetro scritto
- [ ] Tab «Fonti e logica» aggiornato, mail con le domande aperte preparata (la invia il consulente)
