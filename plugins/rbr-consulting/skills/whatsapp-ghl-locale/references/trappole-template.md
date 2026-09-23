# Trappole di approvazione dei template WhatsApp — verificate sul campo

Caso reale: template "Benvenuto" del Noolas, **tre rifiuti nello stesso giorno**
(29/07/2026), causa trovata solo cambiando la struttura. Ecco cosa abbiamo imparato,
in ordine di probabilità quando un template ti torna Rejected.

## 1. Il codice personale in un template Marketing (la causa vera del caso Noolas)

Un template Marketing che consegna un codice personale — "Ecco il tuo codice:
NOOLAS-MARIO-4218" — ha esattamente la **forma di un OTP**, e Meta ammette i codici
solo in categoria **Authentication**. Il rifiuto arriva **in pochi secondi**: è una
validazione automatica strutturale, non una revisione umana. Nessuna riscrittura del
testo lo salva finché il codice resta dentro.

**Nota di onestà**: è l'ipotesi più forte perché è l'unica differenza strutturale
col template Marketing approvato dello stesso account, e spiega tutti e tre i
rifiuti — ma la controprova (la versione senza codice inviata in approvazione) sul
caso Noolas non è mai stata completata. Trattala come ipotesi di lavoro, non come
certezza.

**La soluzione da provare per prima**: togliere il codice del tutto. Il coupon
diventa nominale — "questo messaggio è il tuo Benvenuto, mostralo al tavolo" —
oppure il messaggio porta un **link** alla pagina coupon personale (costruita sui
merge field del contatto), e il codice/QR vive lì. Più semplice anche in cassa, e
il sistema di riscatto non ne ha comunque bisogno (il riconoscimento si fa sul
telefono o sull'ID contatto, non sul codice).

## 2. Alcol e categorie merceologiche vietate

La policy WhatsApp non ammette la promozione di bevande alcoliche. Indizio forte: i
template approvati dei fornitori scrivono esplicitamente "sconto solo sul food,
bevande escluse". Nel dubbio: **il template non nomina l'offerta**, il dettaglio sta
sulla landing e nell'email, dove Meta non ha voce. (Nota di onestà: sul Noolas
rimuovere l'alcol da solo NON è bastato — la causa era il codice — ma resta un
rischio reale da non sommare agli altri.)

## 3. Il template rifiutato non si "ripara"

Modificare un template già Rejected e reinviarlo spesso **non produce una nuova
valutazione**: si continua a leggere un verdetto vecchio. Procedura corretta: crearne
uno **nuovo, con nome nuovo**, con la struttura corretta.

**Poi togli il rifiutato dall'elenco** (contributo di Luciano Purpi, 2026-09-13): i
template Rifiutati lasciati lì confondono chi sceglie il template dentro il workflow
(su Noolas due `benvenuto_*` Rifiutati erano ancora in elenco). Per le versioni
successive usa un suffisso (su Barresi: `_consenso`, `_consenso_2`, `_consenso_3`).

## 4. Dove leggere il motivo (spoiler: da nessuna parte di utile)

- GoHighLevel mostra **solo lo stato** (Active/Rejected), mai il motivo.
- Il WhatsApp Manager (business.facebook.com → WhatsApp Manager → Modelli di
  messaggio) mostra una motivazione **generica**: "non rispetta una o più normative".
- L'unica via per una risposta specifica è il **controllo manuale** dal Centro
  assistenza Meta — giorni di attesa. Prima di arrivarci, cambia la struttura:
  codici fuori, pulsanti, testo più corto, categoria giusta.

## 5. Regole di forma che evitano problemi a monte

- **Corto.** Un template lungo è un template a rischio. Il "cosa ricevi" lo racconta
  la landing che il cliente ha appena letto; WhatsApp fa da chiave d'ingresso.
- **Pulsanti al posto delle domande aperte.** "Rispondi per confermare" produce testo
  libero da interpretare (a pagamento, con l'AI); Confermo · Disdico · Modifico
  produce un dato esatto, gratis.
- **Header**: se incolli il corpo, controlla che il tipo di intestazione non sia
  saltato su "Immagine" (succede nell'editor GHL) — chiederebbe una foto che non hai.
- **Variabili**: l'editor GHL **sgancia le variabili** ({{1}}, {{2}}) quando riscrivi
  il corpo. Ricablarle sempre prima di inviare in approvazione.
- **Opt-out** in ogni template Marketing: preferisci il **pulsante nativo "Marketing
  opt-out"** (Meta compila da sé piè di pagina ed etichetta, tradotti in automatico,
  nessuna riga nel corpo da riapprovare); in alternativa una riga nel testo.
- **Ogni `{{n}}` va mappato a una variabile E deve avere un "Contenuto di esempio"**,
  altrimenti Meta rifiuta (vedi punto 7).
- L'immagine di header è **uguale per tutti i destinatari**: mai promettere QR o
  contenuti personalizzati dentro il messaggio.

## 6. La trappola d'ambiente che ha inquinato tutto

La **traduzione automatica di Chrome** su GoHighLevel riscrive il DOM: l'anteprima
del template mostra parole che NON verranno inviate ("burger" → "hamburger",
"WhatsApp" → "Bomba" nel menu), i campi si sganciano, i salvataggi non attecchiscono.
Disattivarla prima di toccare l'editor: clic destro sulla pagina → *Mostra sempre
l'originale*.

## 7. La variabile sbagliata che produce il «Ciao ,» (contributo di Luciano Purpi, 2026-09-19)

Percorso: Impostazioni → WhatsApp → Modelli → Crea modello → Modello vuoto.

**La trappola**: se nel selettore variabili usi la **ricerca** e scrivi "first name",
escono sei voci quasi identiche (Utente/ First Name, Customer/ First Name, Recipient/
First Name, Contact/ First Name…). Quella etichettata "Contact/ First Name" inserisce
`{{paymentLink.contact.first_name}}`, che su un contatto normale resta **vuota**. È
così che nascono i template approvati che poi partono con "Ciao ,".

**Cosa fare**
- Non usare la ricerca: **naviga l'albero**. Contatto → Nome dà `{{contact.first_name}}`;
  Contatto → Nome completo dà `{{contact.name}}`.
- Il campo della variabile è di **sola lettura**: non si corregge scrivendoci dentro,
  va riselezionato.
- Le voci dell'albero spesso non rispondono al clic sintetico (automazione browser).
  Se succede, clic via JS: `document.querySelectorAll('a.dropdown-tree__item')` →
  trova la voce per testo → dispatch di `mousedown` + `mouseup` + `click`.
- **Verifica sempre** dopo aver selezionato, leggendo i `value` degli input della
  pagina. Non fidarti dell'anteprima: mostra il contenuto di esempio, non la variabile.
- I **campi personalizzati** invece si cercano tranquillamente col nome completo (i
  nomi sono unici) e danno `{{contact.<chiave>}}`.
