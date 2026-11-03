# Segnalare a Google/TripAdvisor le recensioni che non sono recensioni

(contributo di Andrea Chirivì e Luciano Purpi, 2026-10-12) Procedura, motivi che funzionano
davvero e aspettative oneste da dare al cliente — **mai promettere la rimozione di una
recensione negativa prima di averla letta con questi criteri** (vedi anche SKILL.md, Regole
RBR & trabocchetti).

## Google

- **Strumento**: `support.google.com/business/workflow/9945796`, con l'account
  **PROPRIETARIO** del profilo. L'`authuser` cambia quando cambiano gli account collegati a
  Chrome: va verificato ogni volta su `business.google.com/u/N/locations`, perché un
  `authuser` sbagliato può far atterrare su un profilo di un altro cliente.
- **Percorso**: Conferma → sede → "Segnala una nuova recensione da rimuovere" → tabella con
  il link Report (con molte righe conviene cercare via script sulle celle). Esiti e ricorso
  stanno sotto "Controllare lo stato".
- Il Report apre `google.com/local/content/rap/report?postId=…`; l'invio vuole `r=1` fuori
  tema, `r=2` spam o account falso, `r=6` bullismo, più `&authuser`. ⚠️ Questi codici
  dipendono dalla UI di Google e vanno ricontrollati a ogni uso.
- ⚠️ **Trappola**: i clic per riferimento (`ref`), o fatti subito dopo la navigazione, spesso
  **non inviano**. Si clicca per coordinate dopo uno screenshot e si verifica che compaia
  "Segnalazione ricevuta".
- **Il motivo che funziona davvero è "fuori tema"**: parla solo del parcheggio, locale
  sbagliato, mai entrato nel locale. Si possono segnalare anche le 1★ senza testo.
- L'esito si ricontrolla dopo **3 giorni lavorativi** (confronto per stella, vedi
  `scarico-recensioni.md`).
- **Aspettative da dare al cliente**: su un caso misurato, è stata rimossa 1 segnalazione su
  7, in circa 6 giorni — ed era una 5★ fuori tema. Le negative segnalate come spam o
  bullismo erano ancora lì dopo una settimana. Le recensioni circostanziate, anche da un
  nickname, **non si tolgono**: a quelle si risponde, non si segnalano. Quando una
  segnalazione viene accolta, arriva una mail di conferma al proprietario del profilo.

## TripAdvisor

- Percorso: Centro gestione → "Segnalate la recensione".
- Motivi usati: **"non ha avuto alcuna esperienza"** per un cliente che non si è mai
  seduto; **"qualcos'altro"** per una recensione che parla solo del parcheggio o di temi
  estranei al locale.
- I radio del modulo **non si scelgono per riferimento**: si clicca per coordinate **dopo lo
  scroll** della pagina.
- Il testo della segnalazione si scrive **dopo** aver scelto il motivo, altrimenti si perde.
- Le aspettative misurate restano quelle di Google qui sopra: su TripAdvisor **non c'è ancora
  un esito contato** con lo stesso dettaglio — procedura confermata alla fonte, da
  verificare ancora su un caso diretto.
