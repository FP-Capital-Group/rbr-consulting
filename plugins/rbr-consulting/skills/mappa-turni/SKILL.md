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

### 6. Gestisci i casi particolari
- **Turni spezzati** → due range separati nello stesso giorno (es. 07:00-08:00 + 16:00-20:00).
- **Cross-store**: un cedolino può avere giorni segnati ad altri punti vendita → contano SOLO i giorni di questo store (o secondo la regola del cliente).
- **Nota "+ Rimborso €"** sul cedolino = turno extra pagato a rimborso, NON incide sulle ore lavorate.
- Ruoli in maternità/malattia sostituiti → metti nella riga del reparto il sostituto, non lasciare la riga vuota.

### 7. Genera l'xlsx e sincronizza su Drive
Con openpyxl replica la struttura della griglia (una tab per store), applica `PatternFill` con i colori sopra e le "X", scrivi le eccezioni/legenda nella riga note. **Non passare dal connettore Drive per colorare** (non modifica celle): salva il file nella cartella Google Drive Desktop sincronizzata (es. `.../GoogleDrive-<account>/Il mio Drive/`) → sale su Drive da solo. Il ristoratore poi ricolora/aggiusta a mano il Foglio "Turni del personale" se preferisce.

## Regole RBR & trabocchetti
- **Schema per REPARTO, non per persona**: il cliente vuole pulizia, non la rotazione esatta di ogni barista. Bar/Sala vanno UNITI in un'unica categoria.
- **Bar con entrate scaglionate**: i baristi non entrano tutti all'apertura; ricostruisci apertura/centrale/chiusura dai cedolini reali.
- **Slot = cella PRIMA dell'uscita**: l'errore più comune è colorare una cella in più.
- **Arrotondamento sempre alla mezz'ora**: non lasciare orari tipo 06:20 nella griglia.
- **Weekend mai più scarico del feriale** (regola staffing): è il controllo finale su ogni schema.
- **Il connettore Drive non colora celle**: metodo openpyxl + copia nella cartella sincronizzata, sempre.
- Caso d'uso storico: gruppo **Cartabianca** (store Calenzano, Osmannoro, Prato, Ingromarket, Soffiano, Forno, Novoli, Panciatichi, San Mauro). Ma la skill vale per qualsiasi ristorante.
- Emoji di sistema RBR: ✅ ok · 🟡 conferma richiesta · ⚠️ attenzione · ❌ errore · 💭 memoria aggiornata.

## Definition of Done
- [ ] Settimana di riferimento (reale, rappresentativa) confermata col cliente
- [ ] Griglia a slot da 30 min, colorata dall'ingresso alla cella PRIMA dell'uscita
- [ ] Orari arrotondati alla mezz'ora (00-14→:00, 15-44→:30, 45-59→ora piena dopo)
- [ ] Colori reparto corretti: Cucina F4978E · Pasticceria/Pizzeria 9FE7F5 · Bar/Sala A9D08E
- [ ] Regola staffing verificata: weekend pieno, riposi in settimana, weekend MAI più scarico
- [ ] Schema unico per reparto; assenze/eccezioni segnalate a parte; turni spezzati = due range
- [ ] xlsx generato con openpyxl + PatternFill e copiato nella cartella Drive sincronizzata
