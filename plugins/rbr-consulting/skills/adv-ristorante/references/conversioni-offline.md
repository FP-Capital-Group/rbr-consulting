# Conversioni offline Google Ads: formato del file e cifratura

(contributo di Andrea Chirivì, 2026-10-12)

Per caricare come conversioni offline solo le prenotazioni **onorate** (escluse cancellate e
no-show), con identificativi cifrati quando il `gclid` da solo non basta.

## Formato del file
- Prima riga: `Parameters:TimeZone=+0200;`
- Intestazione: `Email, Phone Number, Conversion Name, Conversion Time, Conversion Value, Conversion Currency`
- **Email**: in minuscolo, poi SHA-256.
- **Telefono**: formato E.164 col `+`, poi SHA-256 (regola verificata riproducendo identici 19
  hash di un file esistente).
- Se il gestionale inventa email di appoggio per chi non la lascia, l'aggancio si fa sul telefono.
- Il nome della conversione deve combaciare **esattamente** con l'azione dichiarata in Google Ads.
- Valore e valuta vanno insieme: valuta piena con valore vuoto è un errore.

## Controlli prima del caricamento
- 6 colonne per riga
- nessun campo vuoto
- hash da 64 caratteri
- nessuna data futura

## Limite del metodo
Con identificativi cifrati Google aggancia la conversione solo se il suo tag ha visto il clic
sul dominio del locale (coerente con `sistema-tracciamento-locale/playbook.md`: su un caso reale,
27 righe caricate, 0 riconosciute — il caricamento da solo non basta se manca il clic tracciato
a monte).

**Sicurezza**: il file di hash non va mai pubblicato su un URL aperto.
