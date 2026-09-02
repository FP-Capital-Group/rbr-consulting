---
name: estrai-dati-ipratico
description: Estrae i numeri di un cliente da iPratico Cloud (incassi Z giornalieri, coperti, scontrino medio, prodotti venduti, margini, canali, fasce orarie) senza API key, usando il backend del portale con la sessione già loggata nel browser. Usala quando il consulente dice "tira giù gli incassi da iPratico", "estrai le chiusure di [cliente]", "quanto ha fatturato [cliente] a [mese] su iPratico", "prodotti venduti da iPratico per il menu engineering", "dati cassa iPratico nel CDG". Metodo verificato RBR (training=1, dedup per zNumber, cutoff 06:00).
---

# Estrarre i numeri da iPratico Cloud (metodo RBR verificato)

iPratico non dà API key, ma il portale web usa un backend interrogabile con la sessione del
cliente. Serve **Claude con accesso al browser** (Claude in Chrome o il browser tool della
sessione). Le credenziali dei clienti sono riservate: le inserisce il consulente, mai Claude.

## Prerequisiti (li fa il consulente)
1. Chrome loggato su `https://www.ipraticocloud.com` con l'account del cliente.
2. Aperta una pagina statistiche, es. *Chiusure alla cieca* (`/cloud-stats/blind-closure/eat`).
3. Chiedi in UN messaggio: cliente, periodo (dal → al, `YYYY-MM-DD`), e se ha più locali quale.

## Passo 1 — shopId del locale
Nella pagina attiva leggi il menu a tendina del locale: `select#location-0`. Il `value`
dell'opzione selezionata è lo **shopId** (numero, es. `23179`). Più locali → chiedi quale o
ripeti per ciascuno.

## Passo 2 — Token di sessione
Nel contesto JS della pagina leggi `window.idUsr` (stringa alfanumerica ~40 caratteri): è il
token del backend. Se manca, apri prima `.../cloud-stats/blind-closure/eat` e rileggi.
Il token **scade**: se una chiamata torna 401, ricarica una pagina del portale e rileggilo.

## Passo 3 — Chiusure (incassi + Z fiscali)
```
GET https://apiportal.ipraticocloud.com/statistics/closures
    ?channel=lct_<SHOPID>&training=1
    &dateFrom=<DAL> 00:00:00&dateTo=<AL> 23:59:00
    &application=eat&includeDeleted=true
```
Header obbligatori:
- `Authorization: <window.idUsr>` (token nudo, NON "Bearer")
- `Origin: https://www.ipraticocloud.com`
- `Referer: https://www.ipraticocloud.com/`
- `Accept: application/json, text/javascript, */*; q=0.01`

⚠️ **`training=1` è regola RBR**: include anche l'"extra" nel fatturato. Mai `0`.

Come eseguire, in ordine di preferenza:
- **A)** `fetch()` nel contesto della pagina (stessa origine autorizzata) → JSON.
- **B)** Se bloccato: pagina **Chiusure di giornata** (`/it/cloud-stats/chiusure/eat`) → imposta
  periodo → **Aggiorna** → leggi le richieste di rete → corpo della risposta `statistics/closures`.
- **C)** Fallback sempre valido: stessa pagina, *Mostra 100 righe*, leggi la tabella (o **Excel**).

## Passo 4 — Campi utili di ogni chiusura
| Campo | Significato |
|---|---|
| `DGFETotal` | **Incasso lordo Z** del giorno: è IL fatturato. Valorizzato anche per le manuali |
| `zNumber` | Numero Z progressivo (stringa). `null` = Z annullata |
| `referenceDate` | Data di competenza `YYYY-MM-DD` (trappola: vedi Passo 5) |
| `closureDate` | Momento della chiusura (UTC) |
| `firstClosedPaymentSessionDate` | Prima sessione: miglior proxy del giorno di servizio |
| `isDGFETotalManual` | `true` = totale inserito a mano (cassa giù). Da tenere |
| `nDocuments` | Numero documenti fiscali |

## Passo 5 — Pulizia (obbligatoria)
- **Deduplica per `zNumber`**: a volte arrivano 2 record con stesso `zNumber` e stesso
  `DGFETotal` (closureDate diverse, `deviceCode=null` o `isDGFETotalManual` diverso). Una sola
  entry per `zNumber`, altrimenti raddoppi il fatturato.
- **Escludi Z annullate**: `zNumber=null` o `DGFETotal<=0`.
- **Giorno di servizio**: NON usare `referenceDate` (le chiusure dopo mezzanotte finiscono sul
  giorno dopo). Cutoff alle **06:00 ora italiana** su `firstClosedPaymentSessionDate` (o
  `closureDate`).

## Passo 6 — Output
Tabella per giorno di servizio: data, incasso (`DGFETotal`), n. Z, n. documenti; **totale del
periodo**. Segnala giorni con chiusure manuali e duplicati risolti. Se il dato va nel CDG:
prima la skill `riconciliazione-dati-cliente`, poi `cdg-fatture` / `crea-cdg-cliente`.

## Altri numeri (stesso login, pagine report: menu Statistics — iPratico eat)
| Numero | Pagina |
|---|---|
| Prodotti venduti (mix, per `menu-engineering`) | Venduto e sconti — `/cloud-stats/report-prodotti-operatore/eat` |
| Margini / food cost per prodotto | Products profit margin — `/cloud-stats/stats-products-profit-margin/eat` |
| Sala / asporto / delivery | Totalizations — `/cloud-stats/totalizzazioni/eat` |
| Coperti e scontrino medio | Day-end closing (colonne Customers amount, Cover average) |
| Fasce orarie | Report timeslot — `/cloud-stats/report-per-fascia-oraria/eat` |
| Clienti / fidelity | Customer stats — `/cloud-stats/report-customer/1/eat` |

Per queste: naviga → periodo → **Aggiorna** → *Mostra 100 righe* → leggi la tabella o **Excel**.
Stesse cautele: deduplica, escludi resi/storni, normalizza nomi prodotto (abbreviazioni, doppi spazi).

## Note
- Nessuna API key né richiesta all'assistenza iPratico: si usa il backend del portale con la
  sessione del cliente.
- Vale per qualunque cliente su iPratico Cloud: cambia solo lo `shopId`.
- Se il consulente ha `mcp__claude-in-chrome__*` o il browser tool, è la via A/B; senza browser
  fai fare l'export Excel al consulente e leggi il file (via C).

(Procedura di Marco Cuccaro, 2026-09-02.)
