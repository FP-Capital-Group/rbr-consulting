---
name: checklist-marketing-rbr
description: >-
  La checklist master del sistema marketing RBR: dalla fonte di traffico al cliente che torna.
  Tre modi d'uso: (1) SETUP di un cliente nuovo (accessi → CRM GHL → servizio → tracciamento →
  coupon → fonti di traffico → recensioni → crescita → collaudo); (2) CONTROLLO RICORRENTE
  settimanale/mensile/trimestrale che chiude con max 3 azioni; (3) STATO: verifica cosa è attivo
  e cosa manca su un cliente e aggiorna il foglio "RBR - Stato marketing clienti". Mappa 21 fonti
  di traffico (Meta, Google Ads, Profilo Google, sito, telefono DeepAgent, bot WhatsApp/IG, TheFork,
  Wi-Fi con portale, QR in cassa, walk-in, database, gift card, partner, delivery, social…) con
  dove atterrano, come firmano il canale e cosa parte dopo. Usala quando il consulente dice
  "checklist marketing", "cosa manca a X", "fammi il giro di verifica di X", "controllo mensile",
  "setup marketing del cliente nuovo", "quali fonti di traffico attiviamo", "stato marketing
  clienti", "aggiorna il foglio di stato", "wi-fi marketing", "cosa compro per il wi-fi",
  "perché il cliente non ha contatti nel CRM". Richiama le skill operative invece di riscriverle.
---

# Checklist marketing RBR

> v1.0, 03/10/2026: bozza Claude (memorie + skill) fusa con la checklist di Luciano Purpi (verifiche sul
> campo su Mister Pizza, Dirigì, Barresi, Red Mike, Noolas, Duilio, Geb Garden, Love), approvata da Marco.
> Il documento completo è in `references/checklist-master.md`: **leggilo prima di lavorare**.
> Versione PDF impaginata RBR (da girare a colleghi o mostrare al cliente): `references/Sistema_Marketing_RBR_Checklist_v1.pdf`.

## La regola che tiene insieme tutto
Ogni fonte di traffico deve:
1. **atterrare** in un posto che cattura il contatto;
2. **lasciare la firma del canale** sulla prenotazione;
3. **far partire qualcosa dopo**.

Se una delle tre manca, quella è spesa, non marketing.

**Le 3 misure standard RBR:**
- **costo per prenotazione** (onorata);
- **% di coperti con un contatto nel CRM**;
- **imbuto del coupon**: consegnati → scaricati → riscattati.

CPC, CTR e like non sono risultati.

**L'ordine non si salta:** accessi → CRM → servizio → tracciamento → coupon provato → fonti gratuite → pubblicità. Mai comprare traffico prima che CRM e servizio reggano.

## Il foglio di stato
[RBR - Stato marketing clienti](https://docs.google.com/spreadsheets/d/1CeZDWC3kyyof9N0bLuO0gaWghmWO8IgfMIHP82OoqGo/edit) (ID `1CeZDWC3kyyof9N0bLuO0gaWghmWO8IgfMIHP82OoqGo`). Ha tre tab:

- **Stato**: 39 voci × 12 clienti (colonne D–O, intestazioni in riga 3, voci nelle righe 4–42, percentuale in riga 43). Valori ammessi (menu a tendina):
  - `sì`, `a metà`, `da fare`;
  - `?` = mai verificato, NON vuol dire che manca;
  - `non serve`, `bloccato`.
- **Controllo mensile**: una riga per cliente per mese. Si compilano spesa ads, prenotazioni, coperti, coperti con contatto e coupon; costo per prenotazione, % copertura e % riscatto sono formule. Si chiude con le 3 azioni.
- **Prossime mosse**: cliente, mossa, sezione, responsabile, scadenza, stato (`da fare` / `in corso` / `fatto`).

Accesso: condiviso con Marco, Luciano e il service account `fp-cdg-service@fp-cdg-automation.iam.gserviceaccount.com` (vedi `cdg-fatture/google-accessi.md`).

Trappole del foglio:
- ⚠️ La lingua del foglio è **it_IT**: le formule si scrivono con il **punto e virgola** e i nomi italiani (`SE`, `CONTA.SE`, `CONTA.VALORI`, `LUNGHEZZA`). Con le virgole esce `#ERROR!`.
- Cliente nuovo = nuova colonna dopo l'ultima. Poi va estesa la riga 43, e con lei le convalide e i colori.
- Si scrive cella per cella, **mai sovrascrivere il foglio intero**.

## Modo 1: SETUP di un cliente nuovo
Segui `references/checklist-master.md` sez. 3 nell'ordine. Per ogni blocco usa la skill operativa:

| Blocco | Skill da usare |
|---|---|
| 3.0 Accessi (anche foto router, cellulare di chi riceve gli avvisi, informativa privacy) | — (chiedere al cliente in un solo messaggio) |
| 3.1 CRM: sub-account, ponte, campi, tag, flussi 01–09, dominio mail | `onboarding-cliente-ghl` |
| 3.1 WhatsApp + 3.2 Servizio: conferma, promemoria, orecchio, STOP | `whatsapp-ghl-locale` |
| 3.3 Tracciamento | `sistema-tracciamento-locale`, `google-ads-conversione-controllo`, `analytics-ristorante` |
| 3.4 Meta + Google Ads | `adv-ristorante` (strategia: `strategia-marketing-rbr`, mercato: `market-discovery-ristorante`) |
| 3.4 Profilo Google | `google-business-ristorante` |
| 3.4 Sito / SEO / landing | `sito-landing-ristorante`, `sito-wordpress-cliente-mcp`, `seo-local-ristorante` |
| 3.4 Agente vocale | `agenti-vocali-deepagent` |
| 3.4 Bot Conversation AI | `onboarding-cliente-ghl` → `references/conversation-ai.md` |
| 3.4 Wi-Fi con portale | `references/wifi-portale.md` (in questa skill) |
| 3.4 Coupon / QR / campagne | `campagna-locale` |
| 3.5 Reputazione | `risposte-recensioni-ai-ghl`, `analisi-reputazione-locale` |
| 3.6 Catenaria | `funnel-email-crm` (tre binari di default) + `mail-funnel-ghl`; Pienissimo: `catenaria-pienissimo` |
| 3.6 Segmentazione / riattivazione | `segmentazione-rfm` |
| Problemi tecnici | `diagnosi-suite` |

**Fine setup.** Per ogni fonte accesa:
1. fai una prenotazione di prova (contatto VERO, mai un numero inventato);
2. verifica su Resmio il canale e il codice;
3. verifica in GHL che il contatto sia nato con la fonte.

Poi compila la colonna del cliente nel foglio e la **Scheda cliente** (sez. 5 del master) nella memoria del cliente.

## Modo 2: CONTROLLO RICORRENTE
Sez. 4 del master.
- **Settimana**:
  - conversazioni senza risposta (devono essere zero);
  - richieste del bot inserite su Resmio;
  - chiamate DeepAgent fallite;
  - negative trattenute;
  - sync TheFork vivo;
  - errori nei flussi;
  - annunci bocciati e landing in 404.
- **Mese**: si riempie una riga in «Controllo mensile».
  - costo per prenotazione per canale;
  - % coperti con contatto;
  - imbuto coupon;
  - qualità del numero WhatsApp;
  - media delle recensioni in arrivo;
  - coerenza di orari, menu e prezzi su tutti i canali.
- **Trimestre**:
  - soglie della catenaria;
  - offerta d'ingresso che rende di più;
  - budget per stagione e per lingua;
  - pulizia degli accessi;
  - RFM;
  - analisi reputazione.

Ogni giro chiude con **massimo 3 azioni**, ognuna con il numero che la giustifica. Le azioni vanno in «Prossime mosse».

## Modo 3: STATO / giro di verifica
1. Leggi la colonna del cliente nel tab Stato.
2. Per ogni `?` e `a metà` verifica davvero, API-first:
   - GHL via `ghl2-<cliente>`;
   - Google Ads e Meta via MCP;
   - Resmio e iPratico via API;
   - il browser solo come ultima risorsa.
3. Prepara l'anteprima delle celle da cambiare (voce, valore vecchio → nuovo, prova) e mostrala al consulente.
4. Dopo l'ok scrivi solo quelle celle.
5. I buchi diventano righe in «Prossime mosse».

## Regole che valgono per tutti (sez. 6 del master)
**Offerte**
- Racconto a tutti, premio a chi viene spesso, offerta/sconto **solo a chi ha smesso di venire**.
- 90 giorni di silenzio promozionale dalla visita.
- Riaggancio in due tempi: giorno 91 un invito senza sconto (giovedì alle 11:30), giorno ~110 l'offerta.
- Al massimo 3 gesti all'anno a testa, di cui al massimo 1 sconto.
- Freno: chi torna 3 volte di fila solo con lo sconto esce dalle offerte per 12 mesi.

**Messaggi di prenotazione**
- Mai chiedere di confermare.
- Conferma e promemoria hanno **un solo pulsante, «Modifica o annulla»**, che porta al link di gestione Resmio.
- Mai messaggi di notte o mentre i clienti sono a tavola.

**Contenuti e destinatari**
- Nei messaggi automatici solo cose sempre vere.
- Il premio ai fedeli non è uno sconto e non nomina il numero di visite.
- Campagne solo a chi ha il `consenso-marketing`.
- Anteprima al cliente prima di qualunque invio.

## Trappole più care (sez. 8 del master, elenco completo lì)
- **Profilo Google:** orari sbagliati (Barresi, ~7–8k € persi).
- **Google Ads:** conversione = clic nel widget, invece della prenotazione onorata.
- **Meta:** pixel dentro l'iframe GHL.
- **Resmio:** `widget.js` riscrive il canale.
- **Flussi GHL:**
  - tag che si sommano, invece dell'innesco sul campo di stato;
  - bot senza azione «Attiva un flusso di lavoro»;
  - SMS alla sala senza sistema telefonico;
  - richiesta recensione mai partita.
- **Coupon:** riscatto senza meccanismo in sala (Noolas 646 → 60).
- **TheFork:** sync lanciato nel browser, invece che come attività programmata.

## Wi-Fi con portale
È la leva che porta la copertura dei contatti dal ~40% all'85–90% (insieme al QR in cassa).
- **Kit:** EAP650 (amazon.it/dp/B09TYX13F2, ~100 €) + controller OC200 (amazon.it/dp/B07GX6GVB6, ~110 €, **obbligatorio**) + switch se servono porte.
- **Cosa non funziona:** i router degli operatori (Vodafone Station, Optima ADB).
- **Setup completo, domini pre-accesso e trappole:** `references/wifi-portale.md`.
- **Privacy:** titolare è il locale, **RBR non è responsabile del trattamento**. Il consenso marketing è sempre facoltativo, il Wi-Fi non può dipendere da quello.

## Definition of Done
- [ ] Setup: ogni blocco 3.0–3.7 verde o segnato `non serve` con il motivo
- [ ] Una prenotazione di prova per ogni fonte accesa, verificata su Resmio e su GHL
- [ ] Colonna del cliente aggiornata nel foglio di stato (nessun `?` sulle voci toccate)
- [ ] Scheda cliente compilata nella memoria del cliente
- [ ] Prossime mosse scritte, con responsabile e scadenza
