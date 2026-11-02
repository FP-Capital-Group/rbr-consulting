# Il sistema marketing RBR: checklist master

> **v1.0, approvata da Marco il 03/10/2026.** Unisce la bozza di Claude (memorie e skill del plugin) con il PDF di Luciano «Sistema_Marketing_RBR_Checklist» (verifiche sul campo). Dove le due fonti si contraddicevano ha vinto la verifica sul campo.
> **12/10/2026:** integrate le migliorie di Andrea Chirivì dalla verifica completa su clienti e sistemi reali (con contributi di Roberto Falcon, Luciano Purpi e Leo).
> **Skill:** `checklist-marketing-rbr` (plugin rbr-consulting). **Foglio di stato:** [RBR - Stato marketing clienti](https://docs.google.com/spreadsheets/d/1CeZDWC3kyyof9N0bLuO0gaWghmWO8IgfMIHP82OoqGo/edit) (tab Stato, Controllo mensile, Prossime mosse).

**Come si usa.** Il documento ha tre pezzi:
- **Master Setup** (sez. 3): si fa una volta, quando il cliente entra. È uguale per tutti.
- **Master Controllo ricorrente** (sez. 4): settimana, mese, trimestre. È uguale per tutti.
- **Scheda cliente** (sez. 5): la parte personalizzata (posizionamento, offerte, testi, tempi, canali, lingue).

Ogni voce si segna con: ✅ attiva · 🟡 a metà · ⬜ da fare · ❓ mai verificata · ➖ non serve.

---

## 1. In una pagina

**La regola che tiene insieme tutto.** Ogni fonte di traffico deve:
1. **atterrare** in un posto che cattura il contatto;
2. **firmare** la prenotazione col canale da cui arriva;
3. **far partire qualcosa dopo**.

Se manca una delle tre, quella è spesa e non marketing.

**Il numero che giudica tutto** è il **costo per prenotazione** (onorata). Poi vengono la **% di coperti con un contatto nel CRM** e l'**imbuto del coupon** (consegnati → scaricati → riscattati → **tornati**, cioè chi rientra senza offerta entro una finestra fissa, es. il mese dopo o i 90 giorni del silenzio promozionale: è il numero che giudica davvero una promo). CPC, CTR e like non sono risultati.

**L'ordine conta.** Mai comprare traffico prima che CRM e servizio reggano: CRM → tracciamento → servizio → coupon provato → fonti gratuite → pubblicità.

**Il buco più grande non è la pubblicità, è quello che succede dopo:**
- richieste di recensione mai partite (Mister Pizza, Noolas);
- coupon scaricati a migliaia e riscattati in 60 (Noolas: 646 → 60);
- avvisi alla sala segnati «Eseguito» che non arrivavano a nessuno (Barresi);
- il 59% dei clienti seduti senza un contatto nel CRM (Barresi, settembre).

**Da chi si copia:**
- **Barresi** per il contenuto (il caso più completo);
- **Mister Pizza** per la struttura GHL;
- **Noolas** per il riscatto.

---

## 2. La mappa: le fonti di traffico e dove devono finire

Il CRM è un contenitore, non una strategia: senza un sistema di raccolta e un calendario di
invii, in tre mesi è solo un abbonamento (contributo di Roberto Falcon).

| # | Fonte | Dove atterra | Firma del canale | Cosa parte dopo |
|---|---|---|---|---|
| 1 | Meta Ads (locali + turisti per lingua) | landing `?code=X&source=Y` → widget Resmio (link diretto) | `source` + `comment code:X` | conferma, promemoria, coupon, catenaria |
| 2 | Meta sondaggio / Lead Ads | sondaggio o modulo GHL | Lead via API conversioni dal workflow | premio del sondaggio + catenaria |
| 3 | Meta Click-to-WhatsApp | conversazione WhatsApp in GHL | tag `fonte-ctwa` | bot/sala → prenotazione + consenso |
| 4 | Google Ads (IT, EN turisti, difesa del brand) | pagina prenota con `utm=` e `gclid` | gclid su Resmio | conversioni offline a Google |
| 5 | Prenota con Google / Profilo Google | widget Resmio | source `google_maps` / `google-business` | come le prenotazioni |
| 6 | Sito organico + SEO locale + popup | landing buono (**noindex**) | source `sito`, code `POPUP` | coupon + catenaria |
| 7 | Telefono | agente vocale DeepAgent | prenotazione scritta dal tool (`telefono-ai`) | conferma WhatsApp |
| 8 | WhatsApp / IG / FB in entrata | bot Conversation AI GHL | tag `prenotazione-da-confermare`, `?source=bot-<canale>` | avviso alla sala |
| 9 | TheFork | sync automatico verso Resmio | nota `THE FORK x%` | come le prenotazioni |
| 10 | **Wi-Fi del locale** | portale Omada → form GHL | `utm_source=wifi`, tag `fonte-wifi` | benvenuto (solo con consenso) + recensione |
| 11 | QR in cassa / sui tavoli / totem (club fedeltà) | modulo GHL | fonte `qr-cassa` | benvenuto + catenaria |
| 12 | Walk-in | Resmio come walk-in, col telefono | source `walk-in` | recensione + catenaria |
| 13 | Database vecchio (Keap, TheFork, Excel…) | campagna WhatsApp / email | `utm=riattivazione` | riaggancio |
| 14 | Liste fredde WhatsApp | primo messaggio = richiesta di consenso | tag `consenso-marketing` + `consenso_origine` | catenaria |
| 15 | Gift card | landing gift card | code `GIFTCARD` | consegna + promemoria a 7 e 17 giorni |
| 16 | Partner (hotel, B&B, concierge) ed eventi locali | link / QR per partner; guida al posto con QR, banchetto agli eventi | source `hotel-<nome>` / `evento-<nome>` | come le prenotazioni |
| 16b | Struttura ricettiva collegata | ogni ospite entra in lista al check-in | source `struttura-<nome>` | offerta cena |
| 17 | Porta un amico | codice personale (es. RAIAMICO) | code `<AMICO>` | coupon + catenaria |
| 17b | Vetrina con QR | visibile anche a locale chiuso | fonte `qr-vetrina` | come QR in cassa |
| 17c | Scontrino e menu con QR stampato | impostato una volta sul gestionale | fonte `qr-scontrino` / `qr-menu` | come QR in cassa |
| 18 | Delivery (Glovo / Deliveroo / Just Eat) | volantino nel sacchetto → QR | fonte `delivery` | porta il cliente in sala |
| 19 | Volantini / locandine / hostess / eventi | landing o modulo GHL | `source=volantino` / `hostess` / `evento` | coupon + catenaria; eventi → avviso allo store manager |
| 20 | Social organici (IG/TikTok, influencer locali) | link in bio → prenota | `utm=ig-bio` | come le prenotazioni |
| 21 | ChatGPT Ads (in test, Mister Pizza) | landing dedicata | `source=chatgpt-adv` | come Meta |

**Collaudo di ogni fonte accesa:**
1. Fai una prenotazione di prova.
2. Su Resmio arrivano il canale e il codice giusti?
3. In GHL il contatto nasce con la fonte?

**Percorso del contatto (smistamento):**
```
Fonte → link ?source/?code  ─┐       form GHL nativo (Wi-Fi, sito, Lead Ads, QR)
        Resmio/TheFork ──────┼→ webhook Make RBR-Clienti → Data Store rbr_clients
                             └→ GHL sub-account del cliente (match sul telefono +39)
   GHL: Smistamento → locale/turista/fidelity + fonte-<canale>
        consenso marketing? sì → catenaria · no → solo messaggi di servizio
   Cassa (iPratico / Cassa in Cloud): riscatto + spesa → tornano sul contatto
```
Nessun contatto resta solo su Make, su uno Sheet o in una piattaforma senza passare da GHL. Unica eccezione: i clienti su Pienissimo o Plateform, che vanno decisi uno per uno.

---

## 3. MASTER: il setup (una volta, all'ingresso del cliente)

### 3.0a Onboarding: foto di partenza e kickoff (prima degli accessi)
*(contributo di Roberto Falcon — guida v1.0)*

**Foto di partenza congelata**, prima di toccare qualsiasi cosa — senza non si dimostra il
risultato e non ci si fa pagare:
- [ ] MOLD diretto mese per mese, ultimi 12 mesi, dal CDG
- [ ] Coperti e incasso per servizio degli ultimi 3 mesi, scontrino medio, coperti per giorno della settimana
- [ ] Contatti in lista e da dove arrivano
- [ ] Recensioni (numero e media) su Google, TheFork e TripAdvisor
- [ ] Profilo Google a 90 giorni (visualizzazioni, chiamate, indicazioni)
- [ ] Spesa marketing e provvigioni
- [ ] Chi fa cosa oggi, agenzie e contratti

**Kickoff di un'ora col titolare** e con chi gestirà la sala, tre messaggi:
1. il marketing a pagamento non parte questa settimana (prima si ascoltano i clienti e si scrive la promessa);
2. il primo mese produce coperti da TheFork e decisioni, non campagne;
3. ci sono cose che deve fare lui (dare gli accessi, far consegnare il QR col conto, far dire la promessa al personale).

### 3.0 Accessi
- [ ] Accessi a GHL, Resmio, cassa (iPratico / Cassa in Cloud), Meta BM, Google Ads, Profilo Google, Search Console, GA4, sito, TheFork, TripAdvisor, DeepAgent, WhatsApp
- [ ] **Come si chiedono gli accessi**, non solo cosa:
  - accessi a nome del cliente, consulente come utente aggiunto o partner del Business Manager, doppio fattore sul telefono del titolare — mai credenziali dette a voce;
  - se il cliente manda in chat le sue credenziali personali (es. l'account Meta), non si usano: si chiede l'invito come partner e si consiglia il cambio password;
  - inventario degli accessi intestati alla società del cliente;
  - per ogni accesso, sapere quale mossa salta se manca;
  - senza accessi dopo 10 giorni è un problema di ingaggio, non di tempo: va portato in riunione col direttore tecnico;
  - Meta bloccata da un'agenzia precedente: il recupero lo fa il titolare (è il suo profilo), poi il consulente entra come partner del Business Manager e la vecchia agenzia viene tolta dagli accessi.
- [ ] **Foto del router** del locale: decide il Wi-Fi (porte libere, operatore)
- [ ] **Cellulare personale** di chi riceve gli avvisi (non il numero WhatsApp del locale)
- [ ] **Informativa privacy** con il locale come titolare + consenso marketing separato e facoltativo
- [ ] Carta del cliente sul sub-account GHL con ricarica automatica di $50 (senza carta non parte niente)
- [ ] **Stack diverso da Resmio/iPratico** (es. Cooperto, Cassa in Cloud): prima di proporre un
  cambio cassa, censisci cosa è collegato (es. una cassa automatica self-pay legata al software
  attuale) e fai una call a tre col referente del fornitore. Dati da chiedere per i preventivi
  (iPratico, Resmio, GHL): postazioni, marca e contratto della cassa automatica, stampanti
  comande, palmari per la sera, bilance del banco, tavoli e posti, numero WhatsApp, chi gestisce,
  mail dell'account. Se il cliente è su un prenotatore come Cooperto o Plateform, chiedi alla sala
  di segnare la nota del canale (es. "TF" per TheFork) e controlla serata per serata la cassa
  contro il CRM: senza nota, le prenotazioni di un canale esterno non si distinguono nel CRM.

### 3.0b Uscita da un'agenzia marketing esterna (se presente)
*(contributo di Andrea Chirivì + Roberto Falcon)*
- Griglia con le attività dell'agenzia e dove vanno: consulente, interno, fornitori locali.
- Sequenza: 1) inventario di proprietà e accessi, tutto intestato alla società del cliente; 2) lettura dell'accordo (durata, preavviso, proprietà degli asset, fatture mancanti); 3) ripresa del CRM e della misura; 4) convivenza; 5) chiusura ordinata.
- Prima della chiusura, i file originali degli shooting vanno nella cartella condivisa del cliente.
- Principio RBR: l'advertising non si delega a un'agenzia esterna, fuori si affida solo la produzione di foto e video.
- 🟡 Le cifre indicative di mercato per un'agenzia social (frequenza shooting, costo mensile) variano molto caso per caso: non prenderle come riferimento RBR, chiedile sempre al cliente.

### 3.1 Fondamenta CRM (modello base GHL)
- [ ] Sub-account con lo snapshot **RBR Blueprint v1**, fuso Europe/Amsterdam, valuta EUR. Il «Funnel RBR» del blueprint va **in bozza** finché non è personalizzato: cancella i turisti e manda mail segnaposto.
- [ ] Struttura copiata da Mister Pizza: dati di visita nel contatto, poche etichette. **L'etichetta dice uno stato, il campo contiene un dato.** Barresi e Noolas hanno più di mille etichette ciascuno per non averlo fatto.
- [ ] Campi standard:
  - visita: `nprenotazionicliente`, `data_ultima_presenza`, `statoprenotazione`;
  - riscatto: `coperti_riscatto`, `scontrino_riscatto`;
  - persona e stato: `compleanno_gg_mm`, `stato_cliente`;
  - consenso: `consenso_data`, `consenso_origine`.
- [ ] Tag standard:
  - consenso: `consenso-marketing`, `no-marketing`, `opt-out`, `whatsapp-stop`;
  - recapiti: `email-bounced`, `email-non-valida`;
  - coupon: `coupon-inviato`, `coupon-utilizzato`;
  - fonte: `fonte-<canale>`.
- [ ] 13 Custom Values compilati e istanza MCP `ghl2-<cliente>`
- [ ] **Ponte prenotazioni → GHL**: match sul telefono +39 normalizzato. **L'innesco va sul campo di stato e non sul tag**: i tag si sommano e scattano solo la prima volta.
- [ ] Flussi con nomi standard:
  - 01 Ponte · 02 Stato cliente · 03 Smistamento lead;
  - servizio: 04 Conferma · 05 Promemoria · 06 Cancellata · 07 Orecchio;
  - crescita: 08 Recensione · 09 Benvenuto e riscatto.
- [ ] Dominio mail autenticato (SPF/DKIM/DMARC/Return-Path) + `offerta.<dominio>`. Warm-up da 1.000 mail al giorno.
- [ ] WhatsApp Business ufficiale in GHL (~15 $/mese + ~0,10 € per ogni template Marketing). In coexistence vanno spenti benvenuto e risposte automatiche nell'app; l'app va aperta almeno ogni 14 giorni.
- [ ] Social collegati (IG, FB, Profilo Google, TripAdvisor) per Conversations + Reputation
- [ ] Cassa → GHL (spesa e visite sul contatto). ⬜ Da costruire per tutti.

### 3.2 Servizio (il ciclo della prenotazione: messaggi di servizio, non serve il consenso marketing)
- [ ] **Conferma WhatsApp** con un **solo pulsante «Modifica o annulla»** che porta al link di gestione Resmio.
  - Mai chiedere «confermi?».
  - Mai i link di annullamento di GHL: annullano in GHL, ma il tavolo su Resmio resta occupato.
- [ ] **Promemoria 4 ore prima**: è il flusso che ripaga il canale (ogni disdetta anticipata è un tavolo rivenduto)
- [ ] **Cancellata** senza promo
- [ ] **«Orecchio»** (Customer Replied) per chi risponde a parole: ogni flusso con pulsanti ha il suo ramo «risposta a parole»
- [ ] Ramo **STOP** (`whatsapp-stop`, blocca solo il canale WhatsApp)
- [ ] **Avvisi alla sala** via email, notifica interna o template WhatsApp approvato.
  - ⚠️ Gli SMS partono solo se il sub-account ha il sistema telefonico.
  - Senza, il registro dice «Eseguito» e non arriva niente.
- [ ] Nessun messaggio di notte o mentre i clienti sono a tavola (finestre orarie nei workflow)

### 3.3 Tracciamento
- [ ] Ogni link esterno porta `?source=` (e `?code=` se c'è un'offerta)
- [ ] **Link diretto** al widget Resmio (`app.resmio.com/<slug>/widget?source=…&comment=code:…`), mai l'embed: `widget.js` riscrive il canale col nome del sito
- [ ] `rbr-track.js` sul sito: UTM e gclid nel `comment` della prenotazione
- [ ] Pixel Meta + tag Google **verificati con l'ID reale** (`fbq.getState`, cookie `_fbp`), caricati dopo il consenso cookie.
  - Il pixel **non** va dentro l'iframe GHL: dal 2/9 l'evento Lead di Barresi è morto in silenzio.
- [ ] API conversioni Meta dal workflow GHL, **senza doppio conteggio** col pixel
- [ ] Google: **obiettivo = prenotazione, non clic nel widget**.
  - Il blur-trick al massimo come conversione secondaria.
  - Primaria = import offline delle prenotazioni onorate col gclid.
- [ ] GA4 + Search Console con 5 eventi: `click_prenotazione`, `click_telefono`, `click_indicazioni`, `invio_form`, `click_menu`
- [ ] Anagrafica esistente **esclusa** dalle ads di acquisizione (Noolas: il 67% dei lead era già in rubrica)

### 3.4 Fonti di traffico (dettaglio di setup)
**Meta**
- [ ] Un set per i locali + un set per ogni lingua dei turisti.
- [ ] Stesso codice per offerta, canale diverso per ogni set.
- [ ] Pubblici di retargeting + lookalike 1% sui VIP + audience «GHL Dormienti».
- [ ] Campagna di presenza locale a bassa frequenza.
- [ ] Account in un portfolio con paese IT e valuta EUR (il paese non si cambia).
- [ ] Ripartizione indicativa: 30% freddo locale · 10% freddo turisti · 20% tiepido · 40% caldo.

**Google Ads**
- [ ] Search IT + EN turisti (presenza fisica, raggio 8–10 km) + **difesa del nome** (TheFork e Just Eat comprano il nostro brand).
- [ ] Concorrenti solo come keyword, mai nel testo.
- [ ] Smart campaign in pausa, `ONE_PER_CLICK`.
- [ ] gclid fino a Resmio.
- [ ] Controllo giornaliero su Telegram.

**Profilo Google**
- [ ] **Orari giusti giorno per giorno**: Barresi è rimasto «sabato chiuso» per 3 mesi, ~180 coperti e 7–8k € persi.
- [ ] Pulsanti Menu e Prenota al posto giusto, Prenota con Google attivo, categoria specifica, attributi, menu con prezzi.
- [ ] 1 post a settimana per sede, WhatsApp sulla scheda, Q&A.

**Sito**
- [ ] **Offerta di benvenuto su tre porte**, non solo il popup (chi lo chiude non la ritrova più): pagina dedicata, voce nel menu del sito, sitelink Google Ads a livello di ACCOUNT. Ognuna con la sua etichetta di provenienza riscritta nel modulo.
- [ ] **Popup con buono**, ma **non mostrato al traffico di marca**: l'annuncio di marca punta a `/?marca=1`, il popup ha condizioni "pagina = home" **e** "URL non contiene marca=1" con "display when all" (trappola: la tendina Match va su "Is not", non "Is" — altrimenti l'effetto si rovescia). Si verifica con due visite: la home normale mostra il popup, quella con `?marca=1` no.
- [ ] **Landing coupon sempre noindex**, altrimenti il buono lo usano i clienti già acquisiti. Stessa logica del popup escluso dal traffico di marca.
- [ ] PDF vecchi del menu fuori dall'indice.
- [ ] Pagine SEO per sede (`/<tipo>-<città>-<quartiere>/`, schema Restaurant), GTranslate.
- [ ] Form → GHL (FormSubmit vietato).

**DeepAgent (agente vocale)**
- [ ] Orari prenotabili = quelli di Resmio (apertura, ultima ordinazione in cucina, ultimo slot: scritti separati).
- [ ] Prima registra e poi trasferisce.
- [ ] Numeri di trasferimento confermati dal cliente e **puliti**: a Red Mike uno rispondeva a un'altra azienda.
- [ ] Non promette quello che non sa fare.
- [ ] «Attiva agente» premuto dopo il salvataggio.
- [ ] 6 test + 9 prove al telefono, mai negli orari di punta.
- [ ] Webhook verso GHL.

**Bot WhatsApp/social (Conversation AI)**
- [ ] Deploy su ogni canale.
- [ ] Senza l'azione **«Attiva un flusso di lavoro»** il bot non prenota niente (Barresi: 0 prenotazioni). Con quella, passa la richiesta alla sala.

**TheFork**
- [ ] Sync verso Resmio come **attività programmata** — routine cloud, cron sul server o GitHub Actions, mai come ciclo nel browser o task locale che parte solo ad app aperta: quando il Mac dorme (o l'app è chiusa) si ferma (Dirigì: 41 ore ferme, metà prenotazioni perse in un giorno).
- [ ] **Mossa d'ingresso** (contributo di Roberto Falcon), non solo il sync:
  - scheda controllata: categoria e tipo di cucina giusti, almeno 15 foto vere, menu completo coi prezzi, tutti gli slot aperti;
  - sconto di lancio al **50% su tutto, weekend compreso, di default** — si esclude il weekend solo quando i numeri del locale dicono che è già pieno;
  - risposta automatica alla conferma che invita a iscriversi alla lista CRM;
  - risposta a ogni recensione entro 48 ore.

**Wi-Fi con portale + QR in cassa**
- [ ] Sono le due leve che portano la copertura dei contatti dal ~40% all'**85–90%**. Vedi sez. 7.

**Delivery**
- [ ] Promo solo sul portale (es. 2x1), menu aggiornato, volantino con QR nel sacchetto.

### 3.5 Reputazione
- [ ] **Un solo WhatsApp alle 10:00 del mattino dopo**, a tutti gli entrati con nome e telefono su Resmio (i «Seduto» senza nome sono walk-in e restano fuori), con **link personale**: con un link statico tutte le risposte risultano dello stesso cliente (Mister Pizza). Modelli standard in `references/sondaggi-standard.md`.
- [ ] **Il sondaggio sostituisce la richiesta di recensione, non si aggiunge.** In fondo al sondaggio Google viene proposto a tutti, mai solo a chi ha dato un voto alto.
- [ ] **Al massimo un messaggio ogni 60 giorni**: rientro spento nel workflow e un If/Else sul tag della richiesta come secondo controllo. Va **verificato che parta davvero**: a Mister Pizza e Noolas il motore era configurato ma non è mai partita nessuna richiesta.
- [ ] La profilazione va **a parte**, con un premio (vedi `references/sondaggi-standard.md`).
- [ ] **Reviews AI** in auto-risposta:
  - **lingua di ripiego controllata** (Barresi: clienti palermitani con la risposta in inglese);
  - negative trattenute e scritte a mano (Hold sensitive ON);
  - keyword del piatto lodato solo nelle positive;
  - 5 prove prima di attivare.
- [ ] Mai «recensione in cambio di sconto», mai comprarle, mai filtrare chi può recensire.

### 3.6 Crescita
**Offerta d'ingresso** (skill `strategia-marketing-rbr`)
- [ ] Offerta concreta, motivo, scadenza vera, condizioni in 1 riga.
- [ ] Mai leve di povertà; prima di proporre un prezzo si guarda quello attuale.

**Coupon**
- [ ] Codice parlante identico in 3 posti: link `?code=`, Sheet master offerte, iPratico (spunta «API pubbliche», va messo su ogni installazione).
- [ ] Il codice va anche nel Data Store `rbr_coupons`.

**Riscatto in sala**, una strada sola, mai tutte e due al tavolo:
- **Strada A**: il QR è il codice della cassa iPratico e lo sconto è automatico.
- **Strada B**: il QR apre un modulo GHL con coperti e scontrino.
- [ ] Senza meccanismo in sala i riscatti non si vedono (Noolas: migliaia scaricati, 4 registrati).

**Consegna del coupon**
- [ ] Mail + WhatsApp col QR → sollecito al giorno 3 → ultimo giro al giorno 7.
- [ ] Cruscotto con i 5 stati: inviato → scaricato → riscattato → scaduto → **tornato** (chi rientra senza offerta entro la finestra del silenzio promozionale).

**Regole dell'offerta, da decidere prima del lancio**
- [ ] Regolamento scritto per la cassa (PDF con i casi limite e le parole da usare in sala): quale piatto è gratis nel 2x1 (proposta: il meno caro), QR che non si legge (si onora, si segnano nome ed email, il cliente non paga un guasto nostro), uno a persona o a tavolo, scadenza dei gettoni, non cumulabilità fra offerte. 🟡 Le regole proposte dal consulente si segnano **«da confermare»** dal titolare, non si danno per attive.
- [ ] Regalo di compleanno: varianti costate sul listino vero, scelte **prima** che parta il flusso automatico.
- [ ] Gift card stampate (se previste): formato, tagli, numerazione, card partner e registro di cassa. Prima della tipografia il titolare decide: quante copie, quali partner, la scadenza, se si dà il resto, come si batte lo scontrino.

**Catenaria**: di default si usano i **tre binari** (sez. 6).
- [ ] Le alternative per chi non ha ancora le visite nel CRM sono la standard da 28 mail (1 a settimana, 7 promo) e quella da 57 mail (skill `funnel-email-crm`). Su Pienissimo c'è la skill `catenaria-pienissimo`.
- [ ] Locali e turisti vanno separati: i turisti ricevono 4 mail ravvicinate e poi lo stop.

**Il resto**
- [ ] Segmentazione a 6 stati:
  - Nuovo, Abituale, Affezionato;
  - **Abituale fermo (91–180 gg)**, il segmento che conta di più;
  - Dormiente, Perso.
- [ ] Compleanno (mail + WhatsApp `_compleanno_it`).
- [ ] Club fedeltà / premio ai fedeli (Meat Club, Club Cartabianca).
- [ ] Gift card.
- [ ] WhatsApp marketing:
  - template per campagna, senza codici personali né QR (Meta li rifiuta) e niente alcol;
  - invii a ondate da ~50 con 48 ore di attesa;
  - fornitori esclusi.
- [ ] SMS solo come ripiego (~0,02 $).

### 3.7 Collaudo
- [ ] Contatto di prova **vero**: mai un numero inventato, perché il ponte aggancia il contatto sbagliato. Va cancellato a fine test.
- [ ] Ogni ramo percorso una volta, nessun loop, invii solo in orario consentito
- [ ] Collaudo mail in 10 punti (link a 200, disiscrizione, `first_name` con valore di riserva, lingua…). Sul nodo Email «Sincronizza le modifiche» va su ON.
- [ ] **Anteprima al cliente prima di qualunque invio**
- [ ] Una prenotazione di prova per ogni fonte accesa (sez. 2)
- [ ] **Prima di dire che un flusso funziona, controlla uno per uno** (contributo di Luciano Purpi + Andrea Chirivì):
  - un nodo SMS senza sistema telefonico non è partito anche se il registro dice «Eseguito»;
  - WhatsApp free form parte solo entro 24 ore dall'ultimo messaggio del cliente, con template parte sempre;
  - il template è Attivo e non «In sospeso»;
  - la variabile è mappata e ha un esempio, verificato nel DOM e non solo in anteprima (altrimenti esce «Ciao ,»);
  - il registro di esecuzione è stato letto;
  - per le mail, si sta guardando il MODELLO o la COPIA nel nodo;
  - il flusso è pubblicato e non in bozza;
  - il destinatario della notifica interna esiste come utente;
  - la finestra oraria del flusso è allineata al drip dell'invio.
- [ ] **Conta i tag via API prima di dire che un funnel funziona** (scaricato / utilizzato): un flusso pubblicato da settimane ma con solo poche prove e nessun cliente vero non è "partito".

---

## 4. MASTER: il controllo ricorrente

Non è un report di numeri: i numeri servono a trovare dove il cliente si ferma. **Ogni giro chiude con al massimo 3 azioni**, ognuna con il numero che la giustifica.

| Quando | Cosa si guarda |
|---|---|
| **Ogni settimana** | Conversazioni senza risposta (devono essere zero) · richieste del bot inserite su Resmio · chiamate DeepAgent fallite · negative trattenute · sync TheFork vivo · errori nei flussi · annunci bocciati o landing in 404 (Dirigì: campagna ferma senza avviso) · Google Ads: riepilogo giornaliero · **provenienze** (sotto) · cruscotto in 5 numeri: arrivati (tag `status_arrived`), coupon usati su scaricati, prenotazioni avviate da Google, % senza fonte, speso al giorno |
| **Ogni mese** | Costo per prenotazione per canale · % di coperti con un contatto nel CRM · imbuto coupon (consegnati → scaricati → riscattati → tornati) · qualità del numero WhatsApp · media delle recensioni in arrivo · coerenza di orari, menu e prezzi su tutti i canali · statistiche mail (open, click) · GA4 e insight del Profilo Google (pannello / card AI / AI Overview) · KPI settimanale del cliente · **% coperti prenotati** (prenotati ÷ coperti battuti in cassa + canale di inserimento) · **% prenotazioni senza fonte** · **tavoli aperti in cassa contro tavoli sul gestionale** (regola alla sala: l'accoglienza mette SEMPRE il tavolo sul gestionale, walk-in e sale interne compresi) · riunione mensile coi numeri contro la foto di partenza (sotto) |
| **Ogni 3 mesi** | Soglie della catenaria ritarate sui dati veri · quale offerta d'ingresso rende di più · budget per stagione e per lingua · accessi ai profili, con metodo (sotto) · segmentazione RFM · analisi reputazione (media + % negative per causa e mese) |

### Riunione mensile: numeri contro la foto di partenza
*(contributo di Roberto Falcon + Leo)*
- MOLD diretto contro lo stesso mese dell'anno prima
- coperti reali contro i due break-even (diretto e totale)
- spesa marketing e provvigioni sul fatturato
- contatti nuovi per fonte
- iscritti alla fidelity e visite per iscritto

Tre domande a cui rispondere senza aprire il file: quanto spende il cliente, quanto gli rientra in
MOLD, a che mossa siamo. Le **3 azioni** di chiusura si scrivono con lo schema **CHECK** (cosa
verifico) · **ACTION** (cosa attivo) · **CONTROL** (cosa misuro) · **NEXT** (cosa miglioro).

### Le prime settimane dopo ogni accensione
*(contributo di Luciano Purpi + Andrea Chirivì)*
Oltre al controllo settimanale standard:
- nodo WhatsApp → Statistiche (Delivered, Read, Failed) — **"Read" è un pavimento**: chi ha spento le conferme di lettura non conta, non fidarsi solo di quello;
- cruscotto dell'agente: azioni attivate = 0 vuol dire che l'agente parla e basta;
- contatori dei TAG, non degli iscritti (es. `giftcard-consegnata`, `giftcard-prenotata`, `whatsapp-stop`);
- registri di esecuzione;
- Conversazioni → Non letto;
- recensioni sul profilo pubblico, che possono non coincidere col CRM;
- Impostazioni → WhatsApp → Limiti.

Verifica di copertura di ogni flusso post-visita: confronta gli arrivati su Resmio coi messaggi
partiti. Ogni arrivato non raggiunto ha la sua spiegazione (walk-in senza nome, limite di 60
giorni, assente in GHL, due contatti con due numeri diversi — non è un bug). Misura anche il
ritardo fra orario prenotato e messaggio partito.

### Conversazioni non lette: chi presidia, e una sentinella
*(contributo di Luciano Purpi + Andrea Chirivì)*
Prima di ogni invio di massa: leggi Conversazioni → Non letto, onora gli opt-out già arrivati e
nomina una persona precisa che presidia la casella — una prenotazione o un opt-out mai visti sono
un rischio reale, non teorico. Dove le risorse lo permettono, rinforza il controllo settimanale
«conversazioni senza risposta = zero» con una sentinella: uno script programmato ogni 10 minuti
nelle ore di servizio che, se una conversazione resta senza risposta, manda una notifica e mette
il tag che avvisa lo staff (al massimo un avviso ogni 30 minuti). Estendila anche alle risposte a
parole alla richiesta di recensione.

### Controllo settimanale delle provenienze
*(contributo di Andrea Chirivì — confermato su un cliente, da estendere)*
- Quadro delle prenotazioni create nella settimana, raggruppate per canale.
- **Zero prenotazioni col dominio del sito come source**: se compare, `widget.js` di Resmio è tornato a riscrivere il canale (vedi trappole, sez. 8).
- Nessun ripiego anonimo nuovo e i codici di fonte previsti compaiono davvero.
- Se il gestionale non è accessibile, il controllo **avvisa e si ferma**: un controllo nato per scoprire guasti silenziosi non deve fallire in silenzio.
- Gira su un orologio che non dipende da un Mac acceso (routine cloud, cron sul server, Make), mai su un'attività programmata locale che parte solo ad app aperta (vedi skill `make-scenario-dod`).

### Pulizia trimestrale degli accessi: il metodo
*(contributo di Andrea Chirivì)*
- Meta Business → Persone: la colonna «Ultima attività» registra l'ACCESSO, non l'azione.
- Per le azioni: Gestione inserzioni → seleziona tutte le campagne → icona orologio (cronologia modifiche). Il filtro «Modifica di» non filtra per persona: i nomi stanno nella colonna.
- Controlla anche i partner collegati e gli account pubblicitari in cui il consulente non entra.
- Google Ads e GA4: utenti e MCC di agenzia.
- WordPress: amministratori, password applicazione e log `access_ssl_log` via FTP (circa 12 giorni), filtrando `/wp-admin/` ed escludendo `admin-ajax.php`.
- Restano da controllare Plesk, registrar, utenti GHL e password Instagram.
- Le impostazioni Meta chiedono la passkey del titolare.
- 🟡 Se nelle notifiche Instagram del cliente compaiono avvisi del Centro gestione account (account Facebook rimossi o aggiunti), segnalali subito al titolare perché confermi se sono modifiche sue — segnale visto su un caso solo, da verificare come regola generale.

---

## 5. Scheda cliente (la parte personalizzata)

| Voce | Da compilare |
|---|---|
| Posizionamento («il n.1 di…» nella zona) | |
| No-list: frasi vietate dal posizionamento di questo cliente | |
| Pubblico: % locali / turisti, lingue | |
| Offerta d'ingresso (codice, valore, scadenza, strada di riscatto A/B) | |
| Premio ai fedeli (oggetto, mai sconto) | |
| Racconto: temi del mese (`novita_del_mese`, aggiornato dal titolare) | |
| Catenaria scelta + tempi | |
| Canali accesi (dalla mappa della sez. 2) | |
| Gestionale prenotazioni / cassa / CRM | |
| Orari: apertura / ultima ordinazione in cucina / ultimo slot | |
| Chi riceve gli avvisi (nome + cellulare personale + mail) | |
| Budget ads per stagione e lingua | |
| Stagionalità ed eventi della città | |

---

## 6. Le regole che valgono per tutti

**Quando si manda un'offerta**

| | Racconto | Premio | Offerta / sconto |
|---|---|---|---|
| Esempio | la carne nuova, la storia, il menu | il taglio scelto, il calice offerto | 10 €, 20% |
| Chi lo riceve | tutti, sempre | chi viene spesso | solo chi ha smesso di venire |

- **Silenzio promozionale di 90 giorni dalla visita.** Chi è appena venuto torna da solo, e uno sconto gli insegna ad aspettare la promo. Il racconto continua.
- **Riaggancio in due tempi:**
  - giorno 91: un invito senza sconto (giovedì alle 11:30);
  - giorno ~110: l'offerta, solo se non si è mosso.
- **Tetto di 3 gesti all'anno a testa** (premio o offerta), di cui al massimo 1 sconto. Conferme, promemoria e racconto non contano.
- **Freno:** chi torna 3 volte di fila solo con lo sconto esce dalle offerte per 12 mesi.
- *La promozione non è un premio per chi viene, è lo strumento per chi non viene.*

**Le altre regole**
- Nei messaggi automatici solo cose sempre vere. Il prodotto del giorno lo manda il titolare a mano.
- Il premio ai fedeli non è uno sconto e non nomina il numero di visite: non deve sembrare una raccolta punti.
- Mai chiedere di confermare una prenotazione: il pulsante serve a chi disdice.
- Mai messaggi di notte o mentre i clienti sono a tavola.
- Le risposte alle negative:
  - sono in prima persona, senza mea culpa servile;
  - chiudono con l'invito a tornare chiedendo del titolare.
- Copy:
  - mai affermazioni non verificate (forno a legna, «fatto in casa»);
  - mai foto stock spacciate per piatti del locale;
  - tono asciutto, prima persona singolare;
  - rispetta la no-list per cliente (Scheda cliente, sez. 5): frasi che rafforzano un posizionamento da rompere restano fuori anche se usate altrove;
  - mai promettere quello che le operations non reggono — ogni fatto si verifica col menu o col fornitore prima di pubblicare.
- **Quando cambia un dato** (orari, grammatura, frequenza di una serata) si corregge nello stesso giro su landing, pagine del sito, descrizioni SEO, testi delle campagne, menu e CRM. Il controllo mensile di coerenza resta come rete, non come primo momento della correzione.
- Campagne e catenaria solo a chi ha il `consenso-marketing`; agli altri solo messaggi di servizio.

---

## 7. Il Wi-Fi con portale: perché e cosa comprare

**Perché.** A Barresi, a settembre, su 96 clienti seduti solo 39 avevano un contatto: tutto il lavoro su messaggi e recensioni tocca il 41% della sala.
- Il Wi-Fi è un servizio che il cliente vuole, e il dato è il prezzo dell'accesso.
- Certifica che il cliente era lì quella sera.
- Cattura anche gli altri al tavolo: oggi una tavolata da 6 lascia un solo contatto.
- Con QR in cassa + Wi-Fi la copertura stimata sale all'**85–90%**.

**Kit** (~230 € a locale; dettagli, setup e domini pre-accesso in `memory/wifi_marketing_omada_ghl.md` della suite, copia nella skill: `references/wifi-portale.md`):

| Pezzo | Link | Prezzo | Note |
|---|---|---|---|
| Access point TP-Link EAP650 | [amazon.it/dp/B09TYX13F2](https://www.amazon.it/dp/B09TYX13F2) | ~100 € | alimentatore incluso, va al soffitto al centro della sala |
| Controller TP-Link OC200 | [amazon.it/dp/B07GX6GVB6](https://www.amazon.it/dp/B07GX6GVB6) | ~110 € | senza alimentatore: PoE o caricatore micro-USB 5V ≥1A |
| Switch 5 porte (PoE consigliato, es. TL-SG1005P) | [Amazon.it](https://www.amazon.it/s?k=TP-Link+TL-SG1005P) | ~20–50 € | solo se le porte del router sono piene |
| 2° cavo di rete Cat6 | — | ~5–10 € | 8 contatti per lato |

- **Il controller non è opzionale.** Il cloud Omada gratuito non espone il portale esterno: senza OC200 non si collega al CRM.
- **I router degli operatori non lo fanno.** Vodafone Station e Optima ADB non hanno portale né raccolta dati (verificato).
- Sul form GHL «On Submit» va su **Redirect** (è il segnale che sblocca) e il portale Omada su **No Authentication**.
- Kit ordinato per **Red Mike (16/9)** e **Barresi (25/9)**. Testato con successo il 3/10.
- Privacy: **titolare è il locale, RBR non è responsabile del trattamento** (decisione Marco 03/10/2026). Informativa a nome del locale sul portale; il consenso marketing è facoltativo e il Wi-Fi non può dipendere da quello.

---

## 8. Le trappole che ci sono costate di più

| Trappola | Cosa succede | Dove |
|---|---|---|
| Orari sbagliati sul Profilo Google | «Sabato chiuso» per 3 mesi: ~180 coperti, 7–8k € persi | Barresi |
| Conversioni Google = clic nel widget | L'algoritmo ottimizza sui tocchi, non sulle prenotazioni | Barresi |
| Landing della pubblicità in 404 | Annuncio bocciato, campagna ferma senza avviso | Dirigì |
| Landing coupon indicizzate | Il buono per i nuovi clienti lo trova chiunque su Google | Dirigì |
| Pixel dentro l'iframe GHL | Dal 2/9 l'evento Lead di Meta è morto in silenzio | Barresi |
| Pixel con l'ID segnaposto | Resta live per mesi senza raccogliere niente | vari |
| Banner cookie che blocca il pixel | I volumi crollano | Barresi |
| `widget.js` di Resmio | Riscrive il canale col nome del sito: tracciamento perso | Barresi |
| Tag che si sommano | I flussi scattano solo alla prima visita | Barresi, Mister Pizza |
| Link statico nel sondaggio | Tutte le risposte risultano dello stesso cliente | Mister Pizza |
| Bot senza azioni | 0 prenotazioni: rispondeva ma non poteva fare niente | Barresi |
| Il pulsante WhatsApp ascolta solo il pulsante | Chi risponde «sì» a parole cade nel nulla (15 sì, 0 prenotazioni) | Barresi (gift card) |
| Lingua di ripiego delle risposte AI | Clienti palermitani con la risposta in inglese | Barresi |
| Richiesta recensione mai accesa | Motore configurato, zero richieste inviate | Mister Pizza, Noolas |
| Riscatto senza meccanismo in sala | Migliaia di coupon scaricati, 4 riscatti registrati | Noolas |
| Numeri DeepAgent non puliti | Uno rispondeva a un'altra azienda | Red Mike |
| Sync TheFork nel browser | Il Mac dorme e il ciclo si ferma per 41 ore | Dirigì |
| SMS senza sistema telefonico | Il registro dice «Eseguito», alla sala non arriva niente | Barresi |
| Funnel RBR del blueprint attivo | Cancella i turisti e manda mail segnaposto | Red Mike, Raíces |
| Nodo Email con copia propria | Le modifiche al template non arrivano al workflow | Red Mike |
| Account Meta con paese US | Le campagne non partono, il paese non si cambia | Red Mike |
| Codice personale nel template WhatsApp Marketing | Meta lo scambia per un codice di verifica e lo rifiuta | vari |
| Anagrafica non esclusa dalle ads | Il 67% dei «nuovi» lead era già in rubrica | Noolas |
| Workflow GHL | API in sola lettura, builder non automatizzabile: si montano a mano | tutti |

---

## 9. Dove sono oggi i nostri clienti

Fotografia ricostruita da sessioni e memorie, **non** da un controllo fatto oggi. «?» = mai guardato, non vuol dire che manca.

| Punto | MP | Dirigì | Barresi | Red Mike | Noolas | Duilio | Geb | Love | Raíces | Cartabianca | Zio Bibbi | Luna Blu |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CRM GHL + snapshot | sì | sì | sì | sì | sì | sì | ? | no (Plateform) | sì | no | no | no (Pienissimo) |
| Ponte prenotazioni → CRM | sì | sì | a metà | ? | sì | ? | ? | no | sì | no | no | ? |
| Dominio mail / WhatsApp GHL | a metà (IP warm-up, WA si scollega) | ? | sì | sì | ? | a metà (template) | ? | ? | a metà | no | no | no |
| Agente vocale | sì | sì | sì | sì | sì | sì | sì | no | no | no | no | no |
| Bot WhatsApp/social | ? (KB pronta) | ? | sì (senza azioni) | ? | sì | ? | ? | ? | ? | no | no | no |
| Meta Ads | sì | sì | sì | bloccato (US) | sì | bozze | ? | ? | sì | no | no | no |
| Google Ads | sì | a metà | a metà | sì | ? | sì | ? | a metà | a metà (pagamento) | no | no | no |
| Tracciamento canale | sì | a metà | a metà | sì | ? | sì | ? | no | a metà | no | no | no |
| Wi-Fi con portale | ? | ? | ordinato | ordinato | ? | ? | ? | ? | previsto | no | no | no |
| QR cassa / club | no | no | pronti, da stampare | no | ? | ? | ? | ? | no | progettato | no | no |
| Riscatto coupon | sì | sì | a metà | sì | no | ? | ? | ? | sì (trigger link) | no | no | no |
| Richiesta recensione | no | ? | sì | ? | no | ? | ? | ? | ? | no | no | no |
| Risposte recensioni (Reviews AI) | sì | sì | sì | ? | a metà | ? | ? | ? | sì | no | no | no |
| Catenaria tre binari | no (31 mail) | no | sì | no (28 mail) | bozza | no | no | no | no (28 mail) | no | no | no |
| Premio fedeli | no | no | sì (Meat Club) | no | no | no | no | no | no | progettato | no | no |

---

## 10. Cosa proponiamo di fare

### Prime mosse sui clienti (dove si ottiene di più con meno fatica)
- **Mister Pizza:**
  - accendere la richiesta di recensione, mai partita da GHL;
  - link personale anche nella mail del sondaggio;
  - catenaria a tre binari;
  - IP dedicato a regime, WhatsApp stabile.
- **Noolas:**
  - costruire il riscatto in sala;
  - accendere la richiesta di recensione;
  - riattivare i 28.000 contatti fermi;
  - chiudere il «Funnel RBR» rimasto in bozza con persone dentro.
- **Barresi:**
  - stampare i QR per la cassa (pronti dal 10/9);
  - montare il Wi-Fi;
  - ponte che sostituisce i tag invece di sommarli;
  - azione «Attiva un flusso» sul bot;
  - CAPI.
- **Dirigì:** sync TheFork come attività programmata, tracciamento del gclid, catenaria.
- **Red Mike:**
  - pulsanti Menu e Prenota sul Profilo Google;
  - Wi-Fi;
  - verifica completa di GHL;
  - account Meta nuovo in un portfolio IT/EUR.
- **Raíces:** riattivare Google Ads dopo il pagamento, primi lead dal coupon, Wi-Fi, richiesta recensione.
- **Duilio e Geb Garden:** giro di verifica completo (quasi tutto da guardare); per Duilio, approvazione del template WhatsApp.
- **Love:** decidere come tracciare i canali su Plateform prima di qualunque campagna.
- **Cartabianca:** sub-account GHL + collegamento Cassa in Cloud → GHL, poi il Club con QR in cassa.
- **Zio Bibbi:** accessi (Profilo Google), poi le fondamenta.
- **Luna Blu:** riattivare Pienissimo e le promo delivery.

### Per il cervellone
- **Skill `checklist-marketing-rbr`:**
  - contiene i due master + la scheda cliente;
  - **richiama le skill esistenti** invece di riscriverle: `onboarding-cliente-ghl`, `funnel-email-crm`, `whatsapp-ghl-locale`, `agenti-vocali-deepagent`, `sistema-tracciamento-locale`, `adv-ristorante`, `google-business-ristorante`, `risposte-recensioni-ai-ghl`, `segmentazione-rfm`, `campagna-locale`.
- **Foglio di stato** con una colonna per cliente (la matrice della sez. 9). Diventa il punto di partenza del controllo mensile.
- **Correzioni alle skill esistenti** (✅ approvate e applicate il 03/10/2026, escono con la prossima release del plugin):
  1. `whatsapp-ghl-locale`: conferma con pulsanti Confermo/Disdico/Modifica → **un solo pulsante «Modifica o annulla»** verso il link Resmio; ramo «risposta a parole» in ogni flusso con pulsanti.
  2. `whatsapp-ghl-locale` (Pattern A, innesco su tag aggiunto) → **innesco sul campo di stato**, come nel flusso 01 di `onboarding-cliente-ghl`.
  3. `google-ads-conversione-controllo`: blur-trick come conversione **primaria** → secondaria; primaria = prenotazione onorata (offline), come dicono già `adv-ristorante` e `analytics-ristorante`.
  4. Avvisi alla sala **mai via SMS** se manca il sistema telefonico (`onboarding-cliente-ghl`, `whatsapp-ghl-locale`).
  5. Sync TheFork solo come attività programmata.
  6. Kit Wi-Fi e scelta del controller: nuova sezione, o skill `wifi-marketing-locale`.
  7. Snapshot «Funnel RBR»: dichiarati 15 template, ma gli oggetti da impostare sono 13. Da allineare.

### Decisioni
- ✅ 03/10/2026 Marco: ok alla struttura (setup + controllo ricorrente + scheda cliente, in skill + foglio di stato), alle 3 misure standard (costo per prenotazione, copertura dei contatti, imbuto del coupon) e alle 7 correzioni alle skill.
- ✅ 03/10/2026 Marco: **RBR NON è responsabile del trattamento** dei dati Wi-Fi: titolare è il locale (informativa a nome del locale).
- ✅ 03/10/2026 Marco: il primo giro di verifica sui clienti con tanti «?» lo fanno **Marco e Luciano**.
- ✅ 03/10/2026 Marco: collegamento cassa → GHL **per ora non si pilota su nessun cliente** (resta ⬜ in tutte le colonne).
- 🟡 Ancora aperto: tempi di conservazione dei dati Wi-Fi (da validare col consulente privacy del locale).

*Marco Cuccaro · Luciano Purpi, Restaurant Business Revolution*
