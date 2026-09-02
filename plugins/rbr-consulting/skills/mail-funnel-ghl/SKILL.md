---
name: mail-funnel-ghl
description: Crea in batch i template email del funnel catenaria su GoHighLevel via API (GHL v3, PIT + location ID) partendo dal PDF delle mail — shell HTML riutilizzabile, CTA per tipo mail, mail coupon post-form, test singolo prima del batch, verifica finale. Usa quando l'utente vuole caricare/creare le mail del funnel su GHL, replicare il lavoro Cipriano su un nuovo cliente, o creare template email GHL in massa. NB: le automazioni/workflow GHL non si creano via API — solo i template.
---

# Playbook: creazione template email funnel su GoHighLevel (GHL)

Prompt riutilizzabile da incollare a Claude per replicare il lavoro fatto per il funnel
Cipriano Pizzeria su un nuovo cliente. Copre solo la creazione dei **template email**
(non le automazioni: le API pubbliche di GHL non permettono di creare/modificare
workflow, solo di leggerli — l'automazione va montata a mano nell'editor GHL).

## Checklist: cosa dare a Claude prima di iniziare

1. Private Key API (Private Integration Token GHL, `pit-...`)
2. Location ID del sub-account GHL
3. PDF con i testi del funnel (catenaria)
4. Nome del template di base da usare come sample
5. Link alle promo (uno per ciascuna promo — usati come CTA "Scarica il coupon" e per
   capire quante promo/blocchi remind ci sono)

Le mail di consegna coupon post-form (`PROMOX - COUPON`) sono **sempre previste, una
per ogni promo** — è uno step standard della procedura, non va richiesto ogni volta.

## Dettaglio dei singoli input

1. PDF con le mail del funnel (struttura tipica: N mail di posizionamento, M promo,
   ognuna con 6 remind collegati).
2. Chiave API GHL (Private Integration Token, formato `pit-...`) — salvarla subito in
   un file `.env` locale (`GHL_PRIVATE_TOKEN=...`), mai in chiaro nei messaggi/file di progetto.
3. Location ID del sub-account GHL (stringa tipo `yvSGrxf03S7q85CuR0Bp`, si trova
   nell'URL del sub-account o in Impostazioni → Informazioni azienda).
4. Nome del template GHL esistente da usare come base grafica.
5. Convenzione di naming desiderata per i template (chiedere con esempio,
   es. `Posiz-1-Riassunto`, `Promo-1-Riassunto`, `Remind-1-Promo1-Riassunto`).
6. Link (form o landing page) per ciascuna promo. Le mail di "consegna coupon"
   post-form (`PROMOX - COUPON`) sono sempre incluse, una per ogni promo — non è
   uno step opzionale da chiedere, va sempre fatto.

## Procedura

1. **Leggere il PDF** (`Read` con `pages` a blocchi da max 20) ed estrarre tutte le mail
   con oggetto, corpo e tipo.
2. **Cercare il template base** via API:
   `GET /emails/locations/:locationId/templates?search=<nome>` → prendere `id`.
3. **Scaricare l'HTML del template base**:
   `GET /emails/locations/:locationId/templates/:templateId` → campo `editorContentUrl`
   → `curl` quell'URL per ottenere l'HTML compilato.
4. **Ispezionare le immagini incluse** (scaricarle e guardarle, non assumere): distinguere
   asset generici/brand (logo, foto ambientazione, footer) riutilizzabili in tutte le mail,
   da eventuali grafiche/coupon specifici di UNA promo che NON vanno riusati per le altre
   — se il contenuto di un'immagine non corrisponde all'offerta reale del PDF, fermarsi e
   chiedere come procedere prima di generare in massa.
5. **Costruire uno "shell" HTML riutilizzabile**: tenere intatte le sezioni fisse
   (logo, foto generiche, footer con indirizzo), sostituire con placeholder il blocco
   di testo del corpo e il bottone CTA (`__BODY_HTML__`, `__CTA_HREF__`, `__CTA_TEXT__`).
6. **Regola CTA per tipo mail**:
   - Posizionamento → bottone "Prenota il tuo tavolo" (link di prenotazione esistente).
   - Promo / Remind → bottone "Scarica il coupon" (link form/landing specifico di quella promo).
7. **Mail di consegna coupon** (`PROMOX - COUPON`, una per promo, sempre incluse):
   testo tipo "grazie per aver scaricato il coupon... presentalo in cassa" + requisiti
   di utilizzo + CTA prenotazione, con in fondo una card riepilogo offerta. Se non è
   disponibile un tool di generazione immagini, NON promettere una grafica identica —
   proporre esplicitamente una card in HTML/CSS (tabella con due pannelli, colori del
   brand, titolo offerta, dettaglio, dicitura "Mostra questo coupon in cassa") e far
   approvare lo stile prima di applicarlo a tutte le promo.
8. **Test prima della massa**: creare UN solo template di prova via
   `POST /emails/locations/:locationId/templates` (body: `name`, `editorType:"html"`,
   `editorContent`, `subjectLine`), poi aprire il `previewUrl`/`editorContentUrl`
   restituito nel browser e leggere il testo/verificare visivamente. Solo dopo conferma
   dell'utente, procedere con gli altri in batch.
9. **Batch**: script Python con `subprocess`+`curl` per l'HTTP (su alcune macchine
   `urllib`/`requests` falliscono per `CERTIFICATE_VERIFY_FAILED`: preferire `curl`).
   Loggare ogni risposta in un `results.json` con gli id creati, per poter poi correggere
   puntualmente con `PATCH` invece di ricreare tutto.
10. **Verifica finale**: `GET /emails/locations/:locationId/templates?limit=1` → campo
    `total`, e confrontare con `limit` alto per controllare nomi/duplicati. Il conteggio
    può includere template preesistenti nell'account: non è un errore.
11. **Modifiche successive** (es. l'utente chiede un aggiustamento su una parte comune):
    usare `PATCH /emails/locations/:locationId/templates/:templateId` con solo i campi
    da cambiare — non ricreare/duplicare i template già approvati.

## Riferimento API (GHL v3, header `Version: v3` sempre richiesto)

```
GET    /emails/locations/:locationId/templates?search=&limit=&offset=&folderId=
GET    /emails/locations/:locationId/templates/:templateId
POST   /emails/locations/:locationId/templates
PATCH  /emails/locations/:locationId/templates/:templateId
DELETE /emails/locations/:locationId/templates/:templateId
GET    /workflows/?locationId=        (sola lettura — nessuna creazione automazioni via API)
```

Base URL: `https://services.leadconnectorhq.com`
Header auth: `Authorization: Bearer <PIT>`

Body creazione minimo:
```json
{
  "name": "Posiz-1-Riassunto",
  "editorType": "html",
  "editorContent": "<html>...</html>",
  "subjectLine": "Oggetto della mail"
}
```

## Attenzione / limiti noti

- Le API pubbliche GHL **non permettono di creare o modificare workflow/automazioni**:
  solo lettura. Per costruire l'automazione serve l'editor grafico di GHL (manualmente,
  oppure guidando l'utente passo-passo, oppure — se l'utente si logga lui stesso nel
  pannello Browser — automatizzando i click, con i limiti di fragilità di un editor
  drag-and-drop).
- Mai riusare grafiche/coupon specifici di una promo per altre senza verificarne il
  contenuto reale (rischio di mostrare un'offerta sbagliata a un cliente finale).
- Attenzione ai comandi distruttivi in sequenza (es. DELETE su più id in un unico blocco
  bash): eseguire ed eyeball-checkare l'id giusto prima di ogni cancellazione.
