
# Wi-Fi Marketing RBR — Omada + GoHighLevel (metodo definitivo, testato 03/10/2026)

Fonte: `Guida-WiFi-Marketing-RBR.pdf` (Marco, 03/10/2026). Sostituisce l'ipotesi "Oscar WiFi" citata nell'inventario di luglio.

## Come funziona (1 riga)
Cliente si collega alla rete ospiti aperta → Omada apre la NOSTRA pagina portale → form GHL incorporato → contatto nasce in GHL (utm_source=wifi, utm_campaign=<locale>) + workflow "Form Submitted" → il redirect del form fa sbloccare il Wi-Fi dalla pagina (POST `/portal/auth`, authType 0).
Niente Make, niente webhook in entrata a pagamento.

## Materiale da acquistare (per locale)

| Cosa | Prezzo indicativo (ott 2026) | Dove comprarlo |
|---|---|---|
| Controller **TP-Link Omada OC200** | ~119–150 € | [Amazon.it B07GX6GVB6](https://www.amazon.it/dp/B07GX6GVB6) (link Luciano, ~110 €) · [PcComponentes](https://www.pccomponentes.it/controller-cloud-tp-link-oc200-omada) · [Yeppon](https://www.yeppon.it/products/tp-link-oc200-gateway-1053469) |
| Access point **TP-Link Omada EAP650** (Wi-Fi 6, soffitto) | ~95–120 € | [Amazon.it B09TYX13F2](https://www.amazon.it/dp/B09TYX13F2) (link Luciano, ~100 €, alimentatore incluso) · [MediaWorld](https://www.mediaworld.it/it/product/_access-point-tp-link-eap650-wifi-6-ieee-80211ax-gigabit-porte-eth-135053785.html) |
| Alimentazione OC200: cavetto micro-USB + caricatore 5V ≥1A (o PoE) | ~10 € | [Amazon.it](https://www.amazon.it/s?k=caricatore+5V+1A+micro+USB) — NON usare la porta USB del router |
| 2° cavo di rete Cat6 (8 contatti per lato, non telefonico) | ~5–10 € | [Amazon.it](https://www.amazon.it/s?k=cavo+ethernet+cat6) — lunghezza in base a router→soffitto |
| Switch PoE 5 porte **TP-Link TL-SG1005P** (consigliato se il router non ha 2 LAN libere; con PoE l'AP non usa l'alimentatore) | ~40–60 € | [Amazon.it](https://www.amazon.it/s?k=TP-Link+TL-SG1005P) · [Galaxus](https://galaxus.it/en/s1/product/tp-link-tl-sg1005p-5-ports-network-switches-7041992) |
| Account TP-Link (cloud) | gratis | omada.tplinkcloud.com |
| Sub-account GHL del locale con form + workflow | già nel canone GHL | — |

Totale kit: **~230–330 €** una tantum per locale (1 AP copre una sala media; sale grandi/dehors → 2° EAP650 o versione outdoor EAP650-Outdoor).
⚠️ Prezzi da ricontrollare all'acquisto: link Amazon = ricerca, non listing fisso.

## Perché (dati Luciano, set 2026)
- Barresi settembre: 96 clienti seduti, solo 39 con un contatto nel CRM (41%). Wi-Fi + QR in cassa → copertura stimata 85–90%; cattura anche gli altri al tavolo.
- **Controller OC200 obbligatorio**: il cloud Omada gratuito non espone il portale esterno → senza OC200 niente collegamento al CRM.
- **Router operatore inutili**: Vodafone Station e Optima ADB non hanno portale né raccolta dati (verificato).
- Kit ordinati: **Red Mike 16/09/2026**, **Barresi 25/09/2026**.
- In fase di accesso al cliente chiedere sempre la **foto del router**.

## Setup (sintesi — dettagli nel PDF)
1. **Fisico**: OC200 e EAP650 su due LAN del router del locale (router NON si tocca). Patch panel: mai spostare cavi senza sapere cosa c'è dall'altra parte (spegne altre stanze).
2. **App Omada** (telefono sul Wi-Fi del locale, ~10 min): Local Access → sito (Italia, UTC+1 Roma) → account dispositivo (password diversa per cliente, mai in foto) → adotta EAP650 → WAN Overrides OFF → SSID staff con password + SSID ospiti aperto e isolato ("NomeLocale Wi-Fi Gratis") → Accesso Cloud ON.
3. **Form GHL** "Wi-Fi Portale [Locale]": Nome, Cognome, Email, Telefono obbligatori; privacy obbligatoria; **marketing facoltativo**; pulsante "Accedi al Wi-Fi"; **On Submit = Redirect to URL** (mai messaggio di ringraziamento → Wi-Fi non si sblocca); captcha spento o domini Cloudflare in pre-accesso.
4. **Workflow GHL**: Form Submitted → tag `fonte-wifi` → benvenuto solo a chi ha consenso marketing → entra nella catenaria del locale.
5. **Zip portale** (`index.html`, `index.css`, `index.js`, `logo.png`): cambiare SOLO `GHL_FORM_URL`, `LOCALE`, `LANDING_URL`, `DEBUG:false`, `logo.png` (~256px quadrato), `--brand` in index.css.
6. **Omada web dal computer** (omada.tplinkcloud.com → Network Config → Authentication → Portal): SSID ospiti, **Authentication Type = No Authentication** (Hotspot = authType 11 = non sblocca), timeout 8–12 h, Landing = stessa URL, Import Customized Page (zip), Access Control → Pre-Authentication Access con i domini sotto (uno per riga, niente asterisco).

## Domini pre-accesso
```
api.leadconnectorhq.com
backend.leadconnectorhq.com
stcdn.leadconnectorhq.com
link.msgsndr.com
storage.googleapis.com
fonts.googleapis.com
fonts.gstatic.com
www.google.com
www.gstatic.com
challenges.cloudflare.com
brunhild.challenges.cloudflare.com
<dominio della pagina di destinazione>
```
Se GHL cambia servizi: Chrome → link form → Ispeziona → Network (Keep log) → invia → aggiungi i domini nuovi.

## Trappole
- Rotella che gira e torna, contatto non in GHL → mancano domini Cloudflare Turnstile.
- Contatto in GHL ma niente internet → portale non su No Authentication o form senza redirect.
- Pagina web Omada da telefono taglia i menu → portale sempre dal computer.
- I survey "Form Auth" nativi Omada non si modificano dopo la pubblicazione → non usarli.
- ⚠️ Lo `portale-rbr.zip` in Downloads di Marco (03/10 12:07) ha ancora `DEBUG: true` e NON contiene il controllo "internet risponde davvero 3–15 s" descritto nella guida → usare la versione finale (da archiviare in `suite/tools/wifi-portale/`).

## Privacy
Wi-Fi mai condizionato al consenso marketing (solo presa visione informativa). Campagne/catenaria solo a chi ha dato consenso marketing. Titolare = il locale. **RBR NON è responsabile del trattamento** (decisione Marco 03/10/2026). Ancora aperto: tempi di conservazione → validare col consulente privacy del locale.

## Collegamenti
- Destinazione contatto: sub-account GHL del locale (regola "lead sempre in GHL").
- Codice payload `LANDING_COUPON_REQUEST` in `rbr_payload_standard.md` (fonte wifi).
- Checklist marketing RBR: `quality/CHECKLIST_MARKETING_RBR.md`.
