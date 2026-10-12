# Normative — cosa deve avere un sito di ristorante in Italia (ott 2026)

> Promemoria operativo, non consulenza legale. Il **titolare** dei dati e del sito è il ristorante: è lui che
> firma informativa e scelte. RBR (o il consulente) è al massimo fornitore tecnico. Casi dubbi (e-commerce
> grande, concorsi, dati sanitari/allergie, minori) → avvocato o DPO del cliente.

## 1. Dati obbligatori nel footer (ogni pagina)
- **Ragione sociale, sede legale, Partita IVA** (art. 35 DPR 633/1972: la P.IVA va sulla home del sito di chi ha
  partita IVA).
- Società (srl, spa, sas…): anche **numero di iscrizione al Registro imprese/REA** e, per srl/spa, **capitale sociale
  versato** (art. 2250 c.c., esteso ai siti internet).
- Contatti diretti: telefono e un'email (D.Lgs 70/2003 sul commercio elettronico chiede di essere contattabili
  rapidamente).
- Link a **Privacy**, **Cookie** e «**Preferenze cookie**» (per cambiare il consenso in ogni momento).
- Se il marchio commerciale è diverso dalla società («Cartabianca» → Cartabianca S.r.l.; «Raíces» → ditta del
  titolare) scrivi entrambi.

## 2. Privacy (GDPR Reg. UE 2016/679 + Codice privacy D.Lgs 196/2003)
**Informativa** (pagina Privacy, linkata sotto ogni modulo) con: titolare e contatti · dati raccolti (solo quelli dei
moduli + provenienza/lingua) · finalità e base giuridica (gestire prenotazioni/richieste = misure precontrattuali
art. 6.1.b; novità e offerte = consenso art. 6.1.a) · conservazione (es. 24 mesi per il marketing) · chi vede i dati
(staff, fornitori tecnici: hosting, GoHighLevel, gestionale prenotazioni — nominati responsabili art. 28) ·
trasferimenti fuori UE (GoHighLevel è americano: indicarlo con la base del trasferimento, Data Privacy Framework o
clausole contrattuali standard — da verificare sul contratto del fornitore) · diritti (artt. 15-22) e reclamo al
Garante · ultimo aggiornamento. Modello già scritto: pagina Privacy di Cartabianca Ristoranti (7 punti, IT/EN).

**Moduli**:
- Casella «Ho letto l'informativa» obbligatoria; casella **marketing separata, facoltativa e mai pre-spuntata**;
  prenotare non può dipendere dal consenso marketing.
- Consenso per canale se si usano canali diversi (email ≠ WhatsApp ≠ SMS): nel CRM campi `gdpr_email`,
  `gdpr_whatsapp`, `marketing_consent`, `privacy_policy` (modello base GHL RBR).
- Registra data/ora del consenso e da quale modulo (il plugin lo scrive nella nota GHL).
- Chiedi solo i dati che servono (niente data di nascita completa se basta giorno/mese per il compleanno).
- Minori di 14 anni non possono iscriversi al marketing da soli: niente moduli club rivolti a ragazzini.
- Allergie/intolleranze scritte nelle note sono dati sanitari: usali solo per servire il cliente, mai per marketing.
- Il cliente deve poter disiscriversi da ogni messaggio (link/«STOP»).

**Adempimenti del ristorante** (ricordaglieli, non li fa il sito): registro dei trattamenti, nomine dei fornitori
(accetta i DPA di hosting, GHL, gestionale), istruzioni allo staff che legge le richieste.

## 3. Cookie (Linee guida Garante 10/06/2021)
- **Banner al primo accesso** con la **X di chiusura = rifiuto** (obbligo del Garante) e, come buona prassi
  (EDPB), «Accetta» e «Rifiuta» ugualmente visibili.
  Niente consenso con lo scroll, niente cookie wall («accetta o non entri»).
- Prima del consenso partono solo cookie tecnici. **Pixel Meta, Google Ads, GA4, Hotjar, mappe e video incorporati**
  partono solo dopo il consenso per quella categoria (script bloccati dal plugin cookie: `type="text/plain"` +
  categoria).
- Non riproporre il banner prima di 6 mesi (salvo cambi), link «Preferenze cookie» sempre nel footer.
- Cookie policy: elenco dei cookie/servizi per categoria, durata, link alle informative dei terzi (TheFork, Resmio,
  Google, Meta). Plugin gratuiti che fanno lo scanner e la policy: Complianz, CookieYes (free) o quello dell'hosting.
- **Google Consent Mode v2** attivo se c'è Google Ads/GA4: non è un obbligo di legge ma un requisito di Google (EU
  User Consent Policy) per misurare e fare remarketing sugli utenti UE.
- Font caricati dal sito stesso (non da Google Fonts), mappe con link «Indicazioni» o caricate dopo il clic: così molte
  pagine restano senza cookie di terzi.
- Il widget di prenotazione (iframe di terzi) usa i suoi cookie tecnici: citalo nella cookie policy; deve funzionare
  anche con cookie rifiutati.
- Il testo del banner va tradotto in ogni lingua del sito (su Raíces restava in italiano su `/en/`).

## 4. Menu, prezzi e allergeni
- **Allergeni** (Reg. UE 1169/2011, D.Lgs 231/2017): in sala si danno per iscritto o a voce con cartello; sul sito
  metti in fondo al menu «Per allergie e intolleranze chiedi al personale: l'elenco degli allergeni è disponibile in
  sala» (o le icone dei 14 allergeni piatto per piatto se il cliente ha la mappatura). **Se si vende online** (asporto,
  torte, delivery dal sito) gli allergeni devono essere disponibili **prima dell'acquisto**.
- Coperto e servizio indicati chiaramente se applicati. Prezzi pubblicati = prezzi in cassa (conferma scritta del
  cliente): un prezzo online più basso del conto è un problema col cliente finale.
- Prodotti congelati/surgelati: se il menu stampato ha l'asterisco «prodotto congelato», anche quello online.
- Sconti: ogni annuncio di riduzione di prezzo su un bene (torte, prodotti da banco, online o in negozio) deve
  indicare il prezzo più basso dei 30 giorni precedenti (Codice del consumo art. 17-bis, Omnibus).

## 5. Recensioni, premi, foto, claim
- **Vietate le recensioni false** o selezionate in modo ingannevole (Omnibus, D.Lgs 26/2023; AGCM sanziona): solo
  stelle e numero reali con link alla fonte; se citi una recensione scrivi da dove viene. Se il sito mostra recensioni
  deve dire se e come verifica che vengano da clienti veri (art. 22 c. 4-bis Codice del consumo): es. «recensioni
  pubblicate su Google, non verificate da noi».
- Premi e riconoscimenti solo verificati, con anno e fonte giusti (link all'articolo).
- Claim («fatto in casa», «forno a legna», «km 0», «senza glutine») solo se veri e confermati: sono pratiche
  commerciali, e «senza glutine» ha regole sue (meglio «opzioni per celiaci, chiedi al personale»).
- Foto: solo del cliente o con licenza. Niente foto di clienti prese da Google/Instagram, niente persone riconoscibili
  senza consenso, niente loghi di testate scaricati senza permesso (meglio wordmark testuale + link).

## 6. Vendita online dal sito (asporto, torte, gift card)
- Condizioni di vendita (chi vende, prezzi IVA inclusa, consegna/ritiro, pagamenti, reclami), conferma d'ordine
  scritta al cliente.
- **Recesso**: escluso per beni deperibili e personalizzati (art. 59 Codice del consumo) e per servizi di ristorazione
  con data precisa (art. 59 lett. n, es. cena-evento prenotata e pagata) — scriverlo. Le **gift card** vendute online
  hanno invece il recesso di 14 giorni: scrivilo con validità e condizioni.
- Il link alla piattaforma europea ODR non serve più (piattaforma chiusa il 20/07/2025).
- Pagamenti: solo col conto del cliente (Stripe/SumUp/Satispay suo); più semplice e spesso sufficiente: pagamento al ritiro.
- **Accessibilità** (European Accessibility Act, D.Lgs 82/2022, dal 28/06/2025): i servizi di e-commerce verso i
  consumatori devono essere accessibili; esenti le microimprese (meno di 10 addetti e fatturato o bilancio ≤ 2 M€).
  Gruppi come Cartabianca non sono micro → se vendono online: WCAG 2.1 AA + dichiarazione di accessibilità.
  In ogni caso (anche senza vendita) progettiamo AA: contrasto, alt, tastiera, etichette dei campi, niente testo dentro
  le immagini.

## 7. Club, fidelity, concorsi
- Carta fedeltà con premi = **operazione a premio** (DPR 430/2001): regolamento scritto e conservato, condizioni chiare
  sul sito (cosa si riceve, quando, scadenze) e cauzione del 20% del valore dei premi previsti, salvo premi consegnati
  subito (es. caffè offerto al momento) → farlo verificare al commercialista. Premi = regali (strategia RBR), mai «sconti finti».
- **Concorsi a premio** (estrazioni, «vinci una cena») hanno obblighi pesanti (comunicazione al Ministero, cauzione,
  notaio/funzionario per l'estrazione): non lanciarli dal sito senza il commercialista/consulente del cliente.
- Compleanno: basta giorno e mese (`compleanno_gg_mm`).

## 8. Comunicazioni dopo il modulo (GHL)
- Messaggi di servizio (conferma ricezione, promemoria prenotazione) → base contrattuale, ok senza consenso marketing.
- Messaggi promozionali (offerte, newsletter, compleanno con regalo, riaggancio) → solo a chi ha il consenso marketing
  per quel canale. WhatsApp: template approvati da Meta, categoria giusta (utility vs marketing).
- Mittente email dal dominio del cliente verificato (SPF/DKIM/DMARC), mai da Gmail.

## 9. Checklist normativa (prima del go-live)
- [ ] Footer: ragione sociale, sede, P.IVA (+ REA e capitale per le società), telefono, email
- [ ] Privacy aggiornata (fornitori reali: hosting, GHL, gestionale, TheFork/Resmio), IT + EN
- [ ] Banner cookie a norma, tag bloccati prima del consenso (verificato con «Rifiuta»), Consent Mode v2 se c'è Google
- [ ] Cookie policy con i servizi realmente presenti, link «Preferenze cookie» nel footer
- [ ] Moduli: privacy obbligatoria + marketing facoltativo non pre-spuntato
- [ ] Menu con nota allergeni e coperto; prezzi confermati
- [ ] Nessuna recensione/premio/claim non verificato; foto con diritti
- [ ] Se vende online: condizioni di vendita, recesso, allergeni prima dell'acquisto, accessibilità se non micro
