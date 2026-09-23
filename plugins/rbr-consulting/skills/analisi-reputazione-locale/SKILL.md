---
name: analisi-reputazione-locale
description: Analizza le recensioni di un ristorante o locale su più fonti (TheFork, Google, Yelp, TripAdvisor), le legge in ordine di data e ne ricava punti forti, punti deboli e un piano operativo, consegnato come PDF. Usa questa skill quando l'utente chiede di analizzare o leggere le recensioni di un locale, chiede punti forti e punti deboli, vuole capire perché la media è scesa o come sta andando l'ultimo periodo, parla di reputazione online, voti, stelle, feedback dei clienti, recensioni negative da gestire, oppure nomina un locale cliente insieme a Google, TheFork, TripAdvisor, Yelp. Vale anche quando la richiesta sembra piccola ("che dicono le recensioni di X?") o riguarda una sola fonte: la risposta utile arriva quasi sempre incrociando più fonti e guardando il trend, non la media.
---

# Analisi reputazionale di un locale

> Skill condivisa da Luciano Purpi il 2026-09-03 (scansione skill).
> Nota dell'autore: analisi reputazionale su più fonti (Google, TheFork, TripAdvisor, Yelp) lette PER DATA e mai per rilevanza, contando gli incidenti invece di fare medie; consegna un PDF al cliente con `report_kit.py`. Usata su 4 locali RBR. Dentro ci sono anche le vie di estrazione che NON funzionano, già pagate a tentativi. Per superare il tetto di 200 recensioni del pannello Google vedi il metodo rpc `kAyvCf` (contributo di Luciano Purpi, 03/09/2026), che scavalca il limite indicato in `estrazione-fonti.md`.

La media delle recensioni è il dato meno utile che esista. È una fotografia di anni fa che
pesa sul presente, e un locale che oggi lavora benissimo può restare inchiodato a un 4,2
per colpa di com'era due estati fa.

Quello che serve al ristoratore è un'altra cosa: **cosa sta succedendo adesso, cosa sta
migliorando da solo e cosa no.** Questo si vede solo leggendo le recensioni in ordine di
data e contando gli incidenti, non facendo medie.

Leggi **`estrazione-fonti.md`** per come si tirano fuori i dati da ogni piattaforma — ci
sono dentro le vie che funzionano e quelle che sembrano funzionare e non funzionano, che
sono lezioni pagate su clienti veri. Leggi **`relazione.md`** quando arrivi a scrivere il
documento, e usa `report_kit.py` per impaginarlo invece di riscrivere il layout da zero.

## La regola che decide tutto: per data, mai per rilevanza

Ogni piattaforma di default ordina per "rilevanza" o "più utili". Quell'ordinamento è
inservibile per questo lavoro: sovrappesa le recensioni lunghe, con foto e con molti like,
e ti restituisce un campione che *sembra* rappresentativo e non lo è.

Se una fonte non ti dà l'ordinamento per data, hai due strade oneste: trovarne un'altra che
lo dia (spesso il backoffice del locale ce l'ha nativo), oppure **usare quella fonte solo
come riscontro qualitativo, dichiarandolo, senza ricavarne una singola percentuale.**

Mai spacciare un campione ordinato per rilevanza per statistica. È l'errore che rende
sbagliata tutta l'analisi a valle, e nessuno se ne accorge finché il cliente non agisce
sulle conclusioni.

## Le due metriche, e perché sono indipendenti

Servono entrambe perché si muovono in modo diverso.

**La media** sale facilmente: basta che aumentino i voti alti. È l'indicatore che il
ristoratore guarda e quello che si muove per primo.

**La percentuale di esperienze rotte** — le recensioni sotto una soglia netta (sotto il 7
su 10, sotto le 3 stelle su 5) — non scende da sola. Rappresenta i clienti persi, e ogni
punto percentuale è un problema operativo che nessuno ha ancora chiuso.

Il caso più frequente e più istruttivo è questo: *la media sale e la percentuale di
incidenti resta ferma.* Vuol dire che il locale sta crescendo sui clienti che vanno bene e
non ha toccato le cause di quelli che vanno male. Il ristoratore vede il numero salire e
crede di aver risolto.

## Classificare le negative per causa, e leggerle nel tempo

Il passaggio che produce il valore vero. Leggi ogni recensione sotto soglia e assegnale
una causa — poche categorie, tre o quattro, ricavate dai testi e non decise a priori
(tipicamente: il prodotto, il servizio in sala, il conto, l'accoglienza). Le recensioni
senza testo vanno contate a parte e mai attribuite: sono rumore, non evidenza.

Poi disponi le cause per mese. **Quello che cerchi è la causa che non rientra.** Quasi
sempre uno o due temi calano da soli — la squadra si assesta, un problema viene notato e
chiuso — mentre uno resta piatto o cresce. Quello è l'unico su cui il locale non ha ancora
messo mano, ed è lì che va tutta la priorità.

Questa lettura vale più di qualsiasi elenco di lamentele, perché distingue i problemi che
si risolvono da soli da quelli che richiedono una decisione.

## Le positive vanno lette per contenuto, non contate

Un voto alto non dice niente su *cosa* il cliente ha apprezzato. Conta invece quante
recensioni citano ciascun tema: il prodotto, una persona dello staff per nome, il
posizionamento del locale, il prezzo, l'ambiente.

Il risultato più utile che questa analisi produce di solito è un'assenza. Se il locale è
costruito su una promessa — "leggera e digeribile", "senza glutine", "pesce del giorno" —
e quella parola compare nel 5% delle recensioni, la raccolta recensioni sta girando a
vuoto: riempie la scheda di complimenti generici invece che di posizionamento. È un
problema serio e completamente invisibile guardando la media.

Guarda anche la **forma** delle recensioni recenti: lunghezza dei testi, quota di autori
con zero recensioni precedenti, testi quasi identici fra loro. Un volume che esplode con
testi cortissimi da profili nuovi è il profilo tipico di una raccolta sollecitata, che le
piattaforme filtrano. Segnalalo come rischio, con i numeri — senza accusare nessuno.

## Triangolare, e poi uscire dalle recensioni

Due fonti indipendenti che indicano lo stesso mese di rottura sono una conferma solida.
Una fonte sola è un'ipotesi.

E la causa radice quasi mai sta dentro le recensioni. Sta nei dati che il locale ha già:
durate di prenotazione tarate sotto la permanenza reale che costringono la sala a far
alzare la gente (e producono recensioni furiose sul "tavolo tolto"), un menù nuovo che
sottrae tempi al forno, una coda in cassa che mescola asporto e verifiche promo. Se hai
accesso ai dati di cassa o di prenotazione, **incrociali**: è quello che trasforma un
elenco di lamentele in una diagnosi.

## Come si consegna

Il ristoratore non ha bisogno di sapere che il 12,4% dei clienti è insoddisfatto. Ha
bisogno di sapere *cosa fare lunedì mattina*.

Ogni punto debole va accompagnato dall'azione che lo chiude, da chi la fa e da come si
verifica che sia successo. E le azioni vanno ordinate per rapporto tra impatto e sforzo:
in questi locali le cose che spostano di più sono quasi sempre a costo zero — una frase
detta all'accoglienza, un foglio A4 in cassa, una procedura di trenta minuti — mentre
quelle costose spostano meno.

Chiudi sempre con un piccolo cruscotto: cinque o sei numeri con il valore di oggi,
l'obiettivo e dove si leggono. Senza quello la relazione è un documento; con quello
diventa uno strumento.

## Sequenza operativa

1. **Identifica il locale e le fonti.** Chiedi quali piattaforme usa e se hai accesso ai
   backoffice (TheFork Manager, Profilo dell'attività su Google). L'accesso cambia
   completamente la qualità del dato.
2. **Estrai per data.** Segui `estrazione-fonti.md`. Fissa la finestra temporale e dichiarala.
3. **Calcola le due metriche per mese** — media e percentuale sotto soglia — più le voci
   analitiche se la fonte le dà (cibo, servizio, ambiente, attesa).
4. **Classifica le negative per causa** e disponile nel tempo. Trova quella che non rientra.
5. **Conta i temi delle positive**, cercando soprattutto il posizionamento del locale.
6. **Triangola** fra le fonti e **incrocia** con i dati di cassa/prenotazioni se ci sono.
7. **Scrivi la relazione** seguendo `relazione.md` e impaginala con `report_kit.py`.
8. **Dichiara i limiti** in una nota metodologica: cosa hai potuto leggere per data, cosa no,
   e cosa resta fuori. È la parte che rende il documento affidabile.

## Due avvertenze che valgono per tutti i locali

**I nomi dello staff.** Compaiono spessissimo nelle recensioni positive ed è un ottimo
segnale — significa relazione, non servizio anonimo. Ma se un solo nome domina, segnalalo
come rischio: la reputazione recente sta poggiando su una persona.

**La stagionalità.** Nei locali turistici il mese di picco produce sia il massimo del
fatturato sia il massimo degli incidenti. Confronta un mese con l'altro sapendolo, e non
leggere come peggioramento quello che è solo volume.
