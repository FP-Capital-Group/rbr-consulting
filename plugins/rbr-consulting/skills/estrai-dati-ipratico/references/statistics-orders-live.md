# iPratico — `statistics/orders` in diretta (reparti, varianti, cottura, ordini fantasma)

Per chi legge gli ordini in corso (monitor reparti, pass cucina), non per l'estrazione storica —
vedi `ordini-preconto-magazzino.md` per quella.

## Struttura
Per ogni riga: `dateSend`, `course` e `saleItem.product.category` (da cui si ricava il reparto).
`productComponents` con quantità > 0 = aggiunta, 0 = "SENZA". La cottura sta in
`saleItem.productAttributes` (name "Cottura"; "media" è il default sempre presente e non dice
nulla da sola) o come attributo libero; gli impasti sono varianti. I piatti dei menu a formula
stanno in `children` senza categoria propria: serve il catalogo da `/products` e
`/product-categories`. L'asporto è in `toGoDetails.name`. Non c'è un campo per note libere.

## Tempi
Una comanda compare in 2-9 secondi (mediana ~4); l'API risponde in ~345 ms, che a tarda sera con
molti ordini contemporanei possono salire molto; la sessione dura oltre 2 ore.

## Ordini fantasma (letture che sembrano doppie o sbagliate, ma non sono un errore)
- Un tavolo **spostato** crea un ordine nuovo con stesso `dateSend` e stesse righe: il vecchio
  resta visibile. Un conto portato in cassa crea una copia senza tavolo con lo stesso `dateSend`,
  che può sembrare un take away.
- Una riga **stornata dopo l'invio** ha `dateCancelled` e un `dateSend` nuovo; una riga ritoccata
  ha il `dateSend` riscritto, mentre `printSuccessful.dateSend` resta la prima stampa.
- **Regola**: salta le righe con `dateCancelled` e lega ogni riga alla prima ora vista.

## Ora di stampa e ritardo
Ora di stampa = `printSuccessful.dateSend`; ritardo = stampa − invio. Oltre ~120 secondi
("avvisare stampante/palmare") è **da verificare** come soglia, non ancora validata su più
locali. Le take away senza tavolo hanno `printSuccessful` null anche quando la carta è uscita:
per loro niente avviso.

## Due versioni superate, da non riportare
- "La cottura non viene battuta": sbagliata, la cottura c'è in `saleItem.productAttributes`.
- "`statistics/orders` non contiene le serate chiuse": a volte sì e a volte no — va verificato
  ogni volta, non dato per vero o falso a priori.

(contributo di Andrea Chirivì, 2026-10-12)
