# Template prompt per la ricerca di mercato (foglio "Confronto Mercato")

Usalo per lanciare un Task/agente di ricerca (uno per fornitore, o uno per
gruppo di 2-3 fornitori piccoli) in parallelo — mai in sequenza, altrimenti
il tempo totale si moltiplica per il numero di fornitori. Adatta le parti tra
`< >`.

```
Stai aiutando un consulente di ristorazione a costruire il foglio "Confronto
Mercato" di un'analisi acquisti fornitore per il cliente <NOME CLIENTE>. Il
fornitore analizzato è "<RAGIONE SOCIALE FORNITORE>" (<breve descrizione: tipo
di prodotti che vende>).

Per ciascuno dei seguenti prodotti, cerca online un prezzo di mercato/ingrosso
HORECA di riferimento (grossisti alimentari, cash & carry, distributori food
service, e-commerce B2B, quotazioni ufficiali tipo BMTI/ISMEA/Osservaprezzi
MIMIT dove pertinente) e confrontalo col prezzo pagato dal cliente. Prezzi in
EURO, IVA esclusa quando possibile.

Prodotti (descrizione originale fattura | unità di misura | prezzo pagato
dal cliente nell'ultimo mese disponibile):
1. <DESCRIZIONE COMPLETA CON GRAMMATURA/FORMATO> | <KG o PZ> | €X,XX/<unità>
2. ...

Per ogni prodotto restituisci in formato JSON (una lista di oggetti), con
questi campi esatti:
- "descrizione": la descrizione come sopra
- "prezzo_attuale": il prezzo pagato dal cliente (float, per l'unità indicata)
- "unita": "kg" o "pz"
- "prezzo_mercato": il prezzo di mercato/ingrosso trovato (float) o null se
  non hai trovato un riferimento affidabile — NON INVENTARE prezzi, meglio
  null che un numero a caso
- "valutazione": "SOPRA MERCATO" / "IN LINEA" / "SOTTO MERCATO" / null
- "fonte": nome della fonte
- "tipo_fonte": tipo (es. "Grossista HORECA", "Quotazione ufficiale ingrosso",
  "Cash & carry", "E-commerce B2B")
- "url": link della fonte se disponibile
- "data_rilevazione": mese-anno della rilevazione
- "affidabilita": "Alta" (prezzo diretto per prodotto/marca equivalente),
  "Media" (prodotto simile ma non identico, o prezzo al dettaglio invece che
  ingrosso), "Bassa" (stima indiretta)
- "note": eventuali limiti del confronto (formato diverso, marca diversa,
  prezzo al dettaglio vs ingrosso, ecc.)

Se per un prodotto non trovi NESSUN riferimento pubblico affidabile,
includilo comunque nella lista con prezzo_mercato: null e nota "Nessun
benchmark pubblico affidabile trovato" — non saltarlo, così sappiamo che è
stato cercato.

Rispondi SOLO con il JSON (array di oggetti), preceduto da "```json" e
seguito da "```", senza altro testo prima o dopo.
```

## Quali prodotti includere nella lista

Prendi i prodotti a maggiore spesa nel periodo dal foglio "Articoli" del
workbook già costruito (colonna "Importo acquisti €", ordinata
decrescente), escludendo righe di servizio che non sono prodotti veri:
trasporto, bolli, contributi, abbuoni/sconti commerciali registrati come
riga a parte. 8-12 articoli per fornitore è di solito un buon compromesso tra
copertura e tempo di ricerca — più fornitori nello stesso batch, meno
articoli a testa (l'obiettivo è dare al consulente segnali concreti, non
esaurire il 100% del listino).

Quando esprimi il prezzo al consulente/all'agente, usa l'unità più naturale
per il confronto: se il prodotto è fatturato "a sacco/scatola" ma il mercato
lo quota a peso (es. farina 25kg, formaggio a forma), normalizza tu prima a
€/kg (indicandolo tra parentesi) — è molto più facile per l'agente di ricerca
trovare un riscontro a peso che a "sacco da 25kg di marca X".

## Perché serve un JSON con schema fisso

Con l'output libero in prosa bisognerebbe rileggere e ritrascrivere a mano
ogni numero nel foglio Excel — lento e a rischio di errore di trascrizione.
Con lo schema fisso, `integra_mercato.py` legge il JSON direttamente e scrive
il foglio in automatico, incluso il calcolo di Diff €/%, Impatto sul periodo
e Valutazione.
