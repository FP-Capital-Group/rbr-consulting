# Codici offerta: cosa fanno davvero Resmio, il middleware QR e iPratico

Dettagli tecnici richiamati da `SKILL.md`. Tutto verificato sul campo da Luciano Purpi
(agosto-settembre 2026). Riferimento Resmio completo: `suite/memory/resmio.md`.

## 1. Chi legge cosa nella catena (contratto, non convenzione)

| Anello | Cosa legge | Dove |
|---|---|---|
| Widget Resmio (embed classico `widget.js`) | riscrive `source` con l'hostname della pagina | iframe |
| Widget Resmio (link diretto o proxy PHP) | `source` e `comment` interi | `app.resmio.com/<slug>/widget?...` |
| Widget Resmio → prenotazione | solo le chiavi ESATTE `gclid` e `utm` dal referrer | `booking_request_parameters` |
| Middleware QR coupon (agenzia partner) | regex su `code:` nel TESTO del `comment` | nota ospite |
| Staff / cassa | `notes` (nota interna) e `comment` (nota ospite) | scheda prenotazione |
| Ospite | `comment` stampato nella mail di conferma | mail Resmio |
| iPratico | campo `Codice` del promo code (senza trattini, case-sensitive) | cassa |

(contributi di Luciano Purpi, 2026-09-03)

## 2. `code:CODICE` nel comment è un contratto col middleware
Il middleware che genera i QR non legge un campo strutturato: cerca la stringa `code:` nel
testo della nota e prende quello che segue. Niente `code:` = nessun codice = il CRM cerca un
QR che non trova e il flusso si ferma **in silenzio**.
- Costo reale (22-24/08/2026): spostare il codice dal `comment` al parametro invisibile `utm`
  — modifica corretta in sé — ha spento la generazione QR per due giorni su due clienti.
- Dopo `code:` va il CODICE (colonna D del foglio generatore = campo `Codice` di iPratico),
  mai la descrizione: `code:GIFTCARDCASSA`, non `code: buono 10 euro in regalo`.
- 🟡 **Decisione aperta**: il `comment` finisce nella mail di conferma, quindi l'ospite legge
  l'etichetta. Strade: (A) portare tutto nel parametro invisibile e adeguare il middleware,
  (B) tenere `code:` e togliere le note dal template mail di Resmio. Da decidere con chi
  mantiene il middleware — non toccare l'anello da soli.

## 3. Link diretto al widget con `&comment=` (contributo di Luciano Purpi, 2026-09-05)
`app.resmio.com/<slug>/widget?source=<canale-campagna>&comment=<offerta in chiaro + code:CODICE>`
- Funziona su qualsiasi locale Resmio, senza proxy PHP, anche se il modulo non mostra il campo
  note (Red Mike, 04/09/2026: `?source=TEST-nota&comment=code:RIAPERTURA10` → prenotazione con
  source e comment corretti). Usabile in mail, WhatsApp, QR, bio Instagram, bot.
- Testo url-encodato, **niente emoji** (il test con emoji è tornato 404).
- Rimedio se il link è già partito senza comment (capitato: 83 mail): leggere le ultime
  prenotazioni, filtrare per `source` della campagna con `comment` vuoto e scrivere la nota con
  `PATCH /v1/facility/<slug>/bookings/<id>` (header `X-CSRFToken` dal cookie, risposta 202 →
  rileggere).

## 4. `source` dell'embed classico = sempre l'hostname
Con `static.resmio.com/static/<lang>/widget.js` il loader fa
`source = hostname(param.source || location.href)`: il `source=` scritto nell'embed è lettera
morta (Barresi, 22/08/2026). Passa intero solo col proxy PHP (Mister Pizza, Dirigì) o col link
diretto. **Check di 30 secondi** prima di ogni piano di attribuzione: apri una landing, leggi
l'URL dell'iframe generato, guarda se `source` è sopravvissuto. Se no → canale con `?utm=`
(vedi skill `sito-landing-ristorante`, Tracciamento).

## 5. iPratico e i codici sconto (contributi di Luciano Purpi, 2026-09-03 e 2026-09-04)
1. **Mangia i trattini**: `amico-portato` → codice `AMICOPORTATO` (il trattino resta solo nel
   Nome). Ogni codice con trattino nel foglio generatore è sospetto.
2. **Distingue le maiuscole**: ha accettato `10wifiprenotazione` accanto a `10WIFIPRENOTAZIONE`.
   Due grafie = due codici; un link con la grafia sbagliata non trova nulla.
3. **`sourceApps` parte vuoto** nel modulo a mano: senza spuntare anche "API pubbliche" il
   codice è invisibile all'API → il QR non arriva mai. Il tipo sconto parte su "%": per i buoni
   in euro "€ - Valore sconto".
4. **HTTP 412 = codice già esistente** (si legge solo nel body, la UI non lo mostra), non un
   blocco d'account. L'unicità è più ampia del singolo account: un codice può risultare
   occupato senza essere visibile da nessuna parte → serve iPratico per liberarlo.
5. **Due viste, la prima può mentire**: `/anagrafiche-cloud/promo-codes/1` (anagrafiche
   condivise) può rispondere "Nessun codice promozionale trovato" mentre i codici del locale
   stanno in `/anagrafiche-cloud/promo-codes/0` (vista per locale). Guardarle entrambe prima di
   concludere che un codice non c'è (altrimenti lo crei doppio).
6. **Parametri veri dalla DataTable** della pagina, da confrontare col testo della campagna:
   valore sconto, `minPurchase`, `isReusable`, date di validità, canali (`app_user`/`eat`/
   `api_public`). `isReusable = 1` = lo stesso codice all'infinito, anche dalla stessa persona:
   per una campagna a lista deciderlo consapevolmente o usare un codice a uso singolo.
7. **Creazione via API** (dalla scheda loggata su `/it/anagrafiche-cloud/promo-codes/1`, che
   espone `window.idUsr` e jQuery): `POST https://apiportal.ipraticocloud.com/promo-codes`,
   header `Authorization: window.idUsr`. DEVE passare da `jQuery.ajax`
   (`application/x-www-form-urlencoded`), NON da `fetch` con JSON: il validatore JSON scarta i
   booleani `false` con un errore fuorviante ("finalUnitaryPriceVariation.isPercentage: campo
   obbligatorio"). `channel` = `frn_<id>` per un codice condiviso fra sedi, `lct_<id>` per una
   sede sola.
8. **Il salvataggio in UI** è il pulsante "Salva" in fondo, non "⟳ Aggiorna" in alto (vedi
   `diagnosi-suite` → `references/trappole-strumenti.md`).

## 6. Verifica dai codici DAVVERO usati, non dal foglio
`GET /v1/facility/<slug>/bookings?limit=1000&order_by=-created` su Resmio + regex
`code\s*:\s*([A-Za-z0-9_.-]+)` sul campo **`comment`** (MAI `notes`: è la nota dello staff —
cercare lì fa credere morto un tracciamento che ha 400+ prenotazioni in 3 mesi). Su un cliente
ha fatto emergere codici in circolazione che non esistevano né su iPratico né nel foglio.

## 7. Caso che salva la campagna (Red Mike, 3/9/2026)
Landing di riapertura e testi portavano `10EURORIAPERTURA`, che in cassa NON esiste: il codice
vero era `RIAPERTURA10`. Chi si fosse presentato non avrebbe avuto lo sconto — e la colpa
sarebbe caduta sul cameriere.
