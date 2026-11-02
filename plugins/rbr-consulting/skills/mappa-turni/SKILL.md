---
name: mappa-turni
description: >-
  Metodo RBR per trasformare i cedolini mensili di un ristorante (PDF, un foglio per dipendente) in una mappa-colori cella-per-cella per la griglia turni settimanale "Turni del personale". Usala quando devi "ricostruire i turni del personale dai cedolini", "trasformare i cartellini in una griglia turni colorata", "capire chi lavora e quando in ogni reparto" o "preparare lo schema turni settimanale di un locale". Griglia a slot da 30 min, colori per reparto, regola staffing weekend RBR. Caso d'uso: gruppo Cartabianca, ma vale per qualsiasi ristorante.
---

# Mappa turni (cedolini → griglia turni settimanale colorata)

## Perché esiste
Il ristoratore vuole vedere a colpo d'occhio la copertura del locale: chi c'è, in che reparto, in che fascia oraria, giorno per giorno. I cedolini/cartellini mensili contengono gli orari reali ma sono illeggibili (un PDF per dipendente, orari diversi ogni giorno) e la griglia turni è settimanale. Questa skill traduce i cedolini in una **mappa colori cella-per-cella** su una griglia a slot da 30 minuti, uno schema pulito per reparto. Serve perché **il connettore Google Drive non sa colorare le celle di un Foglio Google esistente**: si genera un `.xlsx` colorato con openpyxl e lo si sincronizza su Drive.

## Quando usarla
- Un ristoratore ti manda i cedolini mensili di uno o più store e vuole la griglia turni settimanale.
- Devi ricostruire l'organico e la copertura oraria per reparto (cucina/pasticceria/bar).
- Vuoi verificare che lo staffing sia sensato (weekend coperto, riposi in settimana).

## Prerequisiti
- Cedolini/cartellini in PDF (un foglio per dipendente), con orari di ingresso/uscita per giorno.
- Python + `openpyxl` (colorazione celle con `PatternFill`).
- Se parti da un Foglio Google esistente: scaricane una copia `.xlsx` per replicarne la struttura (tab per store).
- Cartella Google Drive Desktop sincronizzata sul Mac, per far salire il file su Drive da solo.

## Procedura

### 1. Scegli la settimana e leggi gli organici
Default = **una settimana reale rappresentativa** (NON "settimana tipo": i locali variano troppo). Fai confermare al cliente quale settimana. Poi, dai cedolini, ricostruisci l'organico per reparto: quante persone in cucina, pasticceria/pizzeria, bar/sala, chi è in maternità/malattia/ferie.

### 2. Costruisci la griglia a slot da 30 minuti
Colonne = slot da 30 min (es. 05:00, 05:30, 06:00…). Righe = 7 blocchi-giorno (Lunedì→Domenica), ogni blocco con gli slot del reparto ("Cucina 1-3", "Pasticceria 1-4", "Pizzeria 1-2", "Bar 1-10").
**Regola di colorazione**: colora dall'ingresso fino alla **cella PRIMA dell'uscita** (il bordo destro della cella = fine slot). Es. 06:00→09:00 = celle 6,00 … 8,30.
Se ci sono turni che iniziano prima dell'inizio griglia (pasticceri notturni ~02:40, 03:50…), **aggiungi colonne a sinistra**: dai sempre gli orari REALI completi, niente taglio arbitrario alle 05:00.

### 3. Arrotonda alla mezz'ora
Minuti **00-14 → :00**, **15-44 → :30**, **45-59 → ora piena successiva**. Es. 06:20→06:30, 04:20→04:30, 06:47→07:00.

### 4. Applica i colori per reparto
- 🔴 **Cucina** = rosso `F4978E`
- 🔵 **Pasticceria / Pizzeria** = azzurro `9FE7F5`
- 🟢 **Bar / Sala** = verde `A9D08E`
Uno schema UNICO e pulito **per reparto** (non per persona, niente rotazioni dettagliate). Metti una "X" nelle celle lavorate + il colore. Segnala a parte solo le assenze/eccezioni (riposi, ferie, malattia, maternità).

### 5. Applica la regola staffing RBR (weekend pieno)
**REGOLA CHIAVE:** nei locali il WEEKEND è il picco → i riposi cadono quasi tutti in SETTIMANA (Lun-Ven), NON nel weekend.
- **WEEKEND = roster COMPLETO** (tutti lavorano)
- **FERIALE = stesso schema MA con 1-2 riposi a rotazione al giorno** → meno gente Lun-Ven
- **MAI presentare il weekend più scarico del feriale.**
Eccezioni reali ammesse: store chiusi nel weekend (es. cash&carry Lun-Ven, forno con domenica chiusa/sabato corto) e singoli che riposano nel weekend (raro, va verificato sul cedolino).

**Bar e locali con giorni lunghi** (venerdì, sabato, domenica con chiusura tarda): nessuno chiude da solo. Schema tipo: S1 14:00-17:00, stacco e rientro 20:00-chiusura; S2 17:00-chiusura; chiudono in due (turno spezzato disegnato con due range, vedi §6). Se lo schema chiede più turni di quelli che l'organico copre (es. 17 turni/settimana contro 16 disponibili), il turno in più è un extra **STRUTTURALE**: va scritto nel calendario col suo costo pieno (calcolato sul costo vero del cliente, non un parametro standard) con l'obiettivo che la serata lo ripaghi — incasso in più della fascia ≥ costo dell'extra, verificato dopo un numero dichiarato di serate. Vale per bar e locali con chiusura tarda nei giorni lunghi: non estenderla a ogni ristorante senza chiederlo. (contributo di Andrea Chirivì, Dolce Vita Cafè, 07/09/2026)

### 6. Gestisci i casi particolari
- **Turni spezzati** → due range separati nello stesso giorno (es. 07:00-08:00 + 16:00-20:00).
- **Cross-store**: un cedolino può avere giorni segnati ad altri punti vendita → contano SOLO i giorni di questo store (o secondo la regola del cliente).
- **Nota "+ Rimborso €"** sul cedolino = turno extra pagato a rimborso, NON incide sulle ore lavorate.
- Ruoli in maternità/malattia sostituiti → metti nella riga del reparto il sostituto, non lasciare la riga vuota.

### 7. Genera l'xlsx e sincronizza su Drive
Con openpyxl replica la struttura della griglia (una tab per store), applica `PatternFill` con i colori sopra e le "X", scrivi le eccezioni/legenda nella riga note. **Non passare dal connettore Drive per colorare** (non modifica celle): salva il file nella cartella Google Drive Desktop sincronizzata (es. `.../GoogleDrive-<account>/Il mio Drive/`) → sale su Drive da solo. Il ristoratore poi ricolora/aggiusta a mano il Foglio "Turni del personale" se preferisce.

### 8. Se dalla mappa si passa al calendario con i nomi
Prima di riempire un calendario con i nomi, conta periodo per periodo (settimana o decade) i turni richiesti (giorni aperti × turni al giorno × persone per turno) e quelli disponibili (persone × giorni − riposi minimi − ferie e assenze note). Rifai il conto separatamente prima e dopo ogni entrata o uscita a metà mese. Se il saldo è negativo non riempire le caselle: dichiaralo con i numeri (es. 33 turni richiesti in 11 giorni contro 31 disponibili → due giorni restano scoperti per forza; se per dieci giorni nessuno riposa servono 8 extra, non 2). Accanto ai numeri metti le due strade: extra pagati (n × costo turno) oppure un altro modello di copertura (es. sera feriale con 1 persona sola, che chiude lo stesso buco con 0-2 extra). Il buco non si vede finché non si conta.
*Esempio datato del metodo, non standard: pub serale, vecchio modello 1 mattina + 2 sera tutti i giorni → 8 extra; superato dalla chiusura alle 22 nei feriali e venerdì lungo, che fa tornare il conto senza extra.*

**Controllo di fragilità.** Per ogni calendario conta, per reparto e giorno, quanti nomi diversi possono coprirlo nel mese. Se è uno solo, scrivilo in testa al calendario (es. bancone coperto da un solo barista da lunedì a giovedì; nel suo riposo lo copre chi lascia la sala). Da qui nascono le regole sui riposi incrociati: A non riposa nello stesso giorno di B se B è il suo unico sostituto. Poi misura ogni reparto come % della disponibilità dichiarata (turni richiesti ÷ turni che le persone hanno detto di poter fare, es. sala 158/176 = 90%), letta per blocchi di giorni: se da lunedì a giovedì il margine è zero, la leva è UNA persona disponibile in settimana, non un'altra persona che c'è solo nel weekend. Chi non è fisso si carica in proporzione alla disponibilità dichiarata, non a parità di giorni. Il controllo usa i dati per persona dei cedolini; la griglia consegnata resta per reparto (vedi Regole RBR) — l'esito va nella riga note o in legenda, non nella griglia.
*Esempio anonimo e datato: pub serale, 5 reparti, 21 persone, agosto 2026.*

(contributo di Andrea Chirivì, 2026-10-12)

## Regole RBR & trabocchetti
- **Schema per REPARTO, non per persona**: il cliente vuole pulizia, non la rotazione esatta di ogni barista. Bar/Sala vanno UNITI in un'unica categoria.
- **Bar con entrate scaglionate**: i baristi non entrano tutti all'apertura; ricostruisci apertura/centrale/chiusura dai cedolini reali.
- **Slot = cella PRIMA dell'uscita**: l'errore più comune è colorare una cella in più.
- **Arrotondamento sempre alla mezz'ora**: non lasciare orari tipo 06:20 nella griglia.
- **Weekend mai più scarico del feriale** (regola staffing): è il controllo finale su ogni schema.
- **Il connettore Drive non colora celle**: metodo openpyxl + copia nella cartella sincronizzata, sempre.
- **Calendario**: prima il saldo dei turni richiesti/disponibili (e il controllo di fragilità per reparto/giorno), poi i nomi.
- **Giorni lunghi** (venerdì/sabato/domenica a chiusura tarda): mai una chiusura da soli; l'extra strutturale si dichiara col suo costo.
- Caso d'uso storico: gruppo **Cartabianca** (store Calenzano, Osmannoro, Prato, Ingromarket, Soffiano, Forno, Novoli, Panciatichi, San Mauro). Ma la skill vale per qualsiasi ristorante.
- Emoji di sistema RBR: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Settimana di riferimento (reale, rappresentativa) confermata col cliente
- [ ] Griglia a slot da 30 min, colorata dall'ingresso alla cella PRIMA dell'uscita
- [ ] Orari arrotondati alla mezz'ora (00-14→:00, 15-44→:30, 45-59→ora piena dopo)
- [ ] Colori reparto corretti: Cucina F4978E · Pasticceria/Pizzeria 9FE7F5 · Bar/Sala A9D08E
- [ ] Regola staffing verificata: weekend pieno, riposi in settimana, weekend MAI più scarico
- [ ] Schema unico per reparto; assenze/eccezioni segnalate a parte; turni spezzati = due range (incluse le chiusure dei giorni lunghi in due, per bar/locali con chiusura tarda)
- [ ] xlsx generato con openpyxl + PatternFill e copiato nella cartella Drive sincronizzata
- [ ] Se si passa al calendario con i nomi: saldo turni richiesti/disponibili contato per periodo (dichiarato con i numeri se negativo) e reparti/giorni coperti da un solo nome segnalati
