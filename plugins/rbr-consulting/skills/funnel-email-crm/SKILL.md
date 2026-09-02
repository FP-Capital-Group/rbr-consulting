---
name: funnel-email-crm
description: Genera il PDF completo del funnel email CRM (catenaria) per un cliente ristorante/pizzeria — 57 mail (posizionamento + 5 promo + 30 remind) con regole di scrittura RBR (IO→TU, posizionamento in ogni mail, remind a tono crescente) e PDF ReportLab con pagina di riepilogo. Usa quando l'utente chiede di scrivere la catenaria, il funnel email, le mail CRM di un locale, o "genera i testi catenaria". Il file prodotto è l'input delle skill mail-funnel-ghl (caricamento su GoHighLevel) e catenaria-pienissimo (caricamento su Pienissimo Pro).
---

# Prompt: Genera il PDF del Funnel Email CRM per un cliente ristorante

## ISTRUZIONI PER CLAUDE

Devi generare un PDF completo del funnel email CRM per un cliente ristorante/pizzeria.
Il PDF verrà salvato sul Desktop dell'utente.

---

## ✅ CHECKLIST — DATI DA FORNIRE A CLAUDE

Prima di procedere, fornisci questi 4 punti. Senza di essi Claude non può iniziare.

**1. Nome del locale**
> es. Pizzeria Cipriano

**2. URL Google Maps del locale**
> es. https://maps.app.goo.gl/...
> *(Claude cercherà autonomamente: indirizzo, telefono, orari, recensioni, premi/riconoscimenti)*

**3. Descrizione del posizionamento del cliente**
> Cosa lo rende unico: chef, tecnica, ingredienti, storia, premi, territorio…
> es. "Pizza napoletana con farine certificate Residuo Zero, Mario Cipriano pizzaiolo napoletano, 3 Spicchi Gambero Rosso, locale nel quartiere San Frediano a Firenze"

**4. Lista delle 5 promo**
> Per ognuna: cosa offre e condizioni principali
> es.
> 1. 2x1 su tutte le pizze
> 2. 30% di sconto su tutto il conto
> 3. Bottiglia di vino a scelta in omaggio
> 4. Padellino farcito in omaggio (3 gusti a scelta)
> 5. Dolce per tutto il tavolo in omaggio

---

## REGOLE FISSE DI SCRITTURA

- **Apertura di ogni mail:** `Ciao @@nome@@,`
- **In ogni mail va sempre incluso almeno un elemento di posizionamento del cliente** (un dato, un riconoscimento, un dettaglio sulla tecnica, sulla storia o sul prodotto che rafforza l'identità del locale)
- **Chiusura di ogni mail:** frase tipica associata al cliente — unica, non generica. Claude ne propone 3 opzioni e aspetta la scelta prima di generare il PDF
- **Formato frase di chiusura:** `[frase ad effetto]` + a capo + `Il team di [Nome Locale] [emoji]` — senza indirizzo, telefono o link
- **CTA delle mail promo:** `🎟️ Scarica il coupon` → variabile `@@link_coupon@@`
- **Variabili CRM:** `@@nome@@` · `@@link@@` · `@@link_coupon@@`
- **Tono:** narrativo, caldo, frasi brevi, paragrafi di 1-3 righe, storytelling emozionale che porta alla CTA

- **Persona grammaticale — regola fondamentale:**
  La comunicazione è sempre **IO → TU** (o **IO → LEI** per locali eleganti/lusso). Mai usare il plurale "noi/volevamo".
  - ❌ "Volevamo ricordarti che…" — impersonale, nessuno sa chi parla
  - ✅ "Voglio ricordarti che…" — diretto, personale, coinvolgente
  - ✅ "Le volevo ricordare che…" — tono distinto per locali di lusso
  Il "noi" è ammesso **solo** quando si fa riferimento esplicito allo staff/team del locale (es. "noi in cucina scegliamo ogni ingrediente con cura"). In tutti gli altri casi: prima persona singolare.

---

## TONO DEI REMIND (crescente per ogni promo)

| Remind | Tono |
|---|---|
| R1 | Soft reminder — l'offerta è ancora disponibile |
| R2 | Rinforzo del valore — qualità e benefici dell'offerta |
| R3 | Promemoria con urgenza lieve |
| R4 | Social proof — molti clienti stanno già approfittando |
| R5 | Ultimi giorni — la promo sta per terminare |
| R6 | 48 ore — ultima chiamata, scadenza imminente |

**Struttura obbligatoria di ogni remind:**
1. Frase di promemoria offerta (IO → TU, mai "volevamo")
2. **2-3 righe di posizionamento** — ricordano perché scegliere questo locale (ingredienti, tecnica, chef, premi, atmosfera…)
3. CTA: `🎟️ Scarica il coupon` + `@@link_coupon@@`

Un remind senza posizionamento è troppo scarno: con le 2 foto nel template la mail diventa quasi solo immagini, con rischio spam alto.

**Foto nei remind: solo 1 immagine in alto (header). Nessuna foto nel body o in fondo.**
Le mail di posizionamento e promo possono avere 2 foto se il testo è adeguato.
Ratio testo/immagine bassa = penalità antispam.

---

## STRUTTURA DEL FUNNEL (57 mail totali)

| Blocco | Tipo | Quantità |
|---|---|---|
| Apertura | Posizionamento | 4 mail |
| Promo 1 | Promo + 6 Remind | 7 mail |
| | Posizionamento | 3 mail |
| Promo 2 | Promo + 6 Remind | 7 mail |
| | Posizionamento | 3 mail |
| Promo 3 | Promo + 6 Remind | 7 mail |
| | Posizionamento | 3 mail |
| Promo 4 | Promo + 6 Remind | 7 mail |
| | Posizionamento | 3 mail |
| Promo 5 | Promo + 6 Remind | 7 mail |
| Chiusura | Posizionamento | 6 mail |
| **TOTALE** | | **57 mail** |

---

## PRIMA PAGINA DEL PDF (riepilogo automatico)

Il PDF inizia con una pagina di riepilogo:
1. **4 riquadri colorati** con i contatori: Posizionamento · Promozioni · Remind · Totale mail
2. **Tabella delle promo** (colonne: Promo, Tipo/Offerta, Descrizione)
3. **Schema dei 6 remind** con il tono crescente
4. **Frase di chiusura** scelta

Poi il funnel completo con label colorate:
- 🟡 Giallo = posizionamento
- 🟢 Verde = promo
- 🔵 Ciano = remind

---

## WORKFLOW PASSO-PASSO

1. L'utente fornisce i 4 dati della checklist
2. Claude cerca il locale sul web (indirizzo, telefono, orari, recensioni, riconoscimenti)
3. Claude propone 3 opzioni di frase di chiusura — **aspetta la scelta dell'utente**
4. Claude scrive ed esegue uno script Python con ReportLab
5. Il PDF viene salvato sul Desktop come: `Funnel_Email_[NomeLocale]_[Città].pdf`

---

## TECH: generazione PDF

Usa **ReportLab** (non WeasyPrint — non è disponibile su macOS senza librerie di sistema).

```python
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable, Table, TableStyle
from reportlab.lib.enums import TA_CENTER
```

Struttura dello script:
- Lambda `S(name, **kw)` per creare stili in modo compatto
- Funzione `add(tipo, label, oggetto, lista_paragrafi)` per ogni mail
- Funzione `section(titolo, tipo)` per i titoli di blocco
- Variabile globale `CHIUSURA` con la frase scelta
- Prima pagina: riepilogo con `Table` (riquadri contatori + tabella promo + schema remind) — **senza PageBreak**, separato dal funnel con `HRFlowable`

---

## ESEMPIO DI MESSAGGIO DA INVIARE A CLAUDE

```
Genera il funnel email CRM per questo cliente:

Nome: Pizzeria Da Mario
Google Maps: https://maps.app.goo.gl/...
Posizionamento: pizza napoletana con farine biologiche, forno a legna,
Mario Esposito pizzaiolo con 20 anni di esperienza, locale in zona Prati a Roma

Promo:
1. Antipasto della casa in omaggio
2. 2x1 su tutte le pizze
3. 20% di sconto su tutto il conto
4. Bottiglia di vino a scelta in omaggio
5. Dolce per tutto il tavolo in omaggio
```
