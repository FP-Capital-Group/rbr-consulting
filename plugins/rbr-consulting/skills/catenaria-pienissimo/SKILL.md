---
name: catenaria-pienissimo
description: Costruisce una catenaria email completa (funnel posizionamento + promo + remind) nel backoffice Pienissimo Pro, creando promozioni, tag e i nodi del workflow via API. Usa questa skill ogni volta che l'utente parla di catenaria, workflow o funnel email su Pienissimo, deve caricare in piattaforma un file di mail già scritte, chiede di creare promozioni o coupon su Pienissimo, o nomina un locale cliente insieme a Pienissimo — anche se non dice esplicitamente "catenaria".
---

# Catenaria su Pienissimo Pro

Carica un funnel email già scritto dentro Pienissimo come catenaria funzionante: crea le
promozioni, il tag di ingresso e i ~155 nodi del workflow.

Il funnel di partenza lo produce la skill `funnel-email-crm` (57 mail: 22 posizionamento,
5 promo, 30 remind). Questa skill è il passo successivo: dal file alla piattaforma.

**Leggi `playbook.md` prima di toccare qualsiasi cosa.** Contiene gli schemi JSON dei nodi,
gli endpoint e una serie di trappole dell'interfaccia che fanno perdere ore se le scopri
sul momento (la sessione che non si eredita tra schede, il tasto destro al posto del doppio
clic, il primo clic dopo ogni navigazione che viene ignorato).

## Prima di iniziare: 5 dati dall'utente

Senza questi il lavoro si blocca a metà. Chiedili tutti insieme in un solo messaggio.

1. **Il file con le mail** — percorso del `.txt` o `.pdf`
2. **Login fatto nella scheda giusta** — la sessione Pienissimo vive in `sessionStorage`,
   quindi una scheda nuova è sempre slogata. Fai accedere l'utente nella scheda che userai.
3. **URL del sito** del locale, per i link nelle mail di posizionamento
4. **Come configurare le 5 promozioni** — tipo di sconto e prodotti coinvolti
5. **Criterio della Condizione** — di norma "promozione utilizzata"

## Le 6 fasi

1. **Ricognizione** — apri Marketing → Catenaria, verifica il login, individua `id_multi` e
   `schema` del locale (compaiono nelle chiamate di rete)
2. **Promozioni** — creane una per ogni blocco promo del funnel, poi copia il link coupon
   di ciascuna dalla sezione "Links e collegamenti"
3. **Tag di ingresso** — un tag dedicato, che l'utente assegnerà poi ai contatti
4. **Testi** — carica le mail e sostituisci i segnaposto con URL reali
5. **Costruzione** — genera i nodi e salvali con una sola chiamata `saveWorkflow`
6. **Verifica e consegna** — controlla il grafo, apri l'editor, **lascia la catenaria non attiva**

## Due regole che non si negoziano

**Non attivare mai la catenaria.** Attivarla fa partire mail vere a clienti veri. L'utente
decide quando, dopo aver assegnato il tag ai contatti. Consegna sempre con Attivo = OFF e
dillo esplicitamente.

**Segnala gli scostamenti tra testo e listino.** Le mail sono scritte prima, il listino POS
cambia dopo: capita che una mail prometta "tutti e sei i burger" mentre a listino ce ne sono
dodici, o nomini un prodotto che non esiste più. Non correggere il testo di tua iniziativa e
non tirare a indovinare sul prodotto: configura quello che il cliente leggerà nella mail e
segnala la discrepanza all'utente, che è l'unico a sapere quale delle due fonti è aggiornata.
