---
name: traduci-pdf
description: >-
  Traduce un PDF dall'inglese all'italiano e genera un PDF A4 tipografico pronto per la stampa
  (logica dell'agente RBR Translate: estrazione pdfplumber, traduzione a blocchi con Claude,
  reimpaginazione reportlab con frontespizio, capitoli e numerazione pagine). Usala quando
  l'utente dice "traduci questo PDF", "traduci il libro", "PDF in inglese da tradurre in
  italiano", "traduzione per la stampa". Solo PDF testuali: le scansioni (OCR) non sono
  supportate.
---

# Traduci PDF EN → IT (logica RBR Translate)

Replica in una sessione Claude Code quello che fa l'agente `rbr-translate`
(`RBR AI/agents/rbr-translate/`), senza bisogno del bot deployato.

⚠️ **Cosa produce davvero**: NON una copia grafica dell'originale. Il PDF viene **reimpaginato**
in formato libro A4 (frontespizio, corpo Times giustificato, titoli capitolo, numeri di pagina).
Immagini, tabelle e layout grafico dell'originale vanno persi — è pensato per libri/manuali di
testo da stampare. Dillo all'utente prima di partire se il PDF è ricco di grafica.

## Prerequisiti
- `ANTHROPIC_API_KEY` disponibile (in `.env` o ambiente).
- Python con: `pdfplumber`, `anthropic`, `reportlab`, `python-dotenv`.
- PDF **testuale**: se l'estrazione restituisce testo vuoto è una scansione → fermati e segnala
  (OCR non gestito, è nel backlog dell'agente).
- Lingue: EN → IT (hardcoded nell'agente; per altre coppie adatta il prompt e segnalalo).

## Procedura

### Via A — hai il monorepo RBR AI in locale
Usa direttamente il CLI dell'agente:
```bash
cd "/Users/marco/Desktop/AI/RBR AI/agents/rbr-translate"
pip install -r requirements.txt   # pdfplumber, anthropic, reportlab, python-dotenv
python translate_cli.py <input.pdf> [<output.pdf>]   # default: <input>_IT.pdf accanto all'input
```
Fine. Il resto della skill serve per la Via B.

### Via B — sessione standalone (senza monorepo)
Scrivi uno script Python che replica i 3 moduli `core/` dell'agente:

**1. Estrazione** (da `core/extractor.py`)
- `pdfplumber.open()` → per ogni pagina `page.extract_text()`, strip, unisci con `"\n\n"`.
- Se il testo totale è vuoto → ❌ scansione, stop.
- Stampa il conteggio parole estratte come sanity check.

**2. Traduzione a blocchi** (da `core/translator.py` + `config.py`)
- Spezza il testo in blocchi da **~3000 parole** (`CHUNK_WORDS`) rispettando i confini di
  paragrafo (split su `"\n\n"`, non a metà paragrafo).
- Per ogni blocco chiama Claude (modello dell'agente: `claude-sonnet-4-6`, `max_tokens=8192`)
  con questo system prompt (testuale dall'agente):
  - Sei un traduttore letterario esperto, EN → IT
  - Mantieni la struttura originale: paragrafi, titoli di capitolo, righe vuote
  - Stile naturale e scorrevole, adatto a un libro
  - Conserva i nomi propri (persone, luoghi, marchi) in originale
  - Titoli di capitolo su riga separata, stessa formattazione originale
  - Non aggiungere commenti/note — solo il testo tradotto; non omettere nulla
- **Contesto di continuità**: al messaggio di ogni blocco (tranne il primo) antepone le ultime
  **300 parole** del blocco tradotto precedente, marcate "NON tradurre, solo per coerenza
  stilistica". È questo che evita cambi di tono/terminologia tra blocchi.
- Mostra il progresso (blocco i/N, %). Unisci i blocchi tradotti con `"\n\n"`.

**3. Reimpaginazione PDF** (da `core/pdf_generator.py`)
- `reportlab.platypus.SimpleDocTemplate`, pagina A4, margini: sx/dx/alto 3 cm, basso 2,5 cm.
- **Frontespizio**: spacer 3 cm + titolo (Times-Bold 22, centrato) + sottotitolo "Traduzione in
  italiano" (Times-Italic 13, centrato) + `PageBreak`. Titolo = nome file ripulito
  (`_`/`-` → spazio, Title Case) o titolo dichiarato dall'utente.
- **Corpo**: Times-Roman 11pt, interlinea 17, giustificato, rientro prima riga 0,6 cm.
- **Titoli capitolo**: Times-Bold 14, `keepWithNext`. Una riga è capitolo se matcha
  `Chapter/Capitolo/Part/Parte/Prologue/Epilogue/Introduction/Preface` (+ varianti IT),
  `^\d+\.\s+[A-Z]`, oppure è tutta MAIUSCOLA, 4-79 caratteri e ≤8 parole.
- **Footer**: numero di pagina centrato, Times-Roman 9, grigio, a 1,2 cm dal bordo.
- Escapa `& < >` prima di passare le righe a `Paragraph`.

### Consegna
- Salva come `<nome>_IT.pdf`, apri/controlla frontespizio, un titolo capitolo e un paragrafo a
  campione contro l'originale.
- Condividi secondo la baseline RBR (Drive/al richiedente).

## Correggere traduzioni vecchie con accenti scritti come apostrofi
Le traduzioni prodotte da rbr-translate prima di ~maggio 2026 (chunk in
`agents/rbr-translate/chunks_it/`, monorepo RBR AI) hanno tutti gli accenti scritti come
apostrofo ASCII: `qualita'`, `perche'`, `e'`, `cosi'`, `piu'`. Riguarda potenzialmente anche
altri libri tradotti in quel periodo, non solo casi isolati. **Non serve ritradurre** (zero
costi API): si corregge con un passaggio deterministico sul testo.
- Regole di fix: (1) parola che finisce in vocale+apostrofo seguita da non-lettera → vocale
  accentata (`a'`→`à`, `i'`→`ì`, `o'`→`ò`, `u'`→`ù`); (2) `e'`→`è`, tranne le parole che
  finiscono in `-che` (perché, poiché, affinché, benché, finché...) e ne/se/ventitré → `é`;
  (3) whitelist da NON toccare: `po'`, `mo'`, `di'`, `fa'`, `va'`, `sta'`, `de'`, `co'`; (4)
  salta le parole tra virgolette singole (es. `'no'`, `'coraggiosa'`): si riconoscono perché
  l'apostrofo di apertura è preceduto da spazio/inizio riga, mentre nelle elisioni
  (`dell'universita'`) è preceduto da lettere; (5) preserva il maiuscolo (`E'`→`È`,
  `QUALITA'`→`QUALITÀ`).
- Verifica finale: grep dei residui vocale+apostrofo a fine parola — devono restare solo `po'`,
  citazioni e possessivi inglesi (`Americans'`).
- Poi rigenera il PDF A4 con la pipeline reportlab di questa skill (frontespizio, capitoli,
  numeri di pagina).
- **Prima di ritradurre un libro da zero, controlla sempre** `agents/rbr-translate/chunks_it/`
  e `progress_*.json` esistenti nel monorepo RBR AI: potrebbe essere già tradotto per intero e
  mancare solo la generazione del PDF finale. *(contributo di Marco Cuccaro, 2026-08-28)*

## Regole & trabocchetti
- ⚠️ Blocchi troppo grandi = risposta troncata da `max_tokens`: se un blocco tradotto sembra
  monco, riduci `CHUNK_WORDS` e ritraduci quel blocco.
- ⚠️ Non "migliorare" il testo: traduzione fedele, nessuna sintesi, nessuna nota del traduttore.
- ⚠️ PDF con molte tabelle/immagini: avvisa che verranno perse prima di consumare API.
- Segreti (`ANTHROPIC_API_KEY`) sempre da `.env`/ambiente, mai nel codice o nel repo.

## Definition of Done
- [ ] Testo estratto non vuoto e conteggio parole comunicato
- [ ] Tutti i blocchi tradotti con contesto di continuità, nessun blocco troncato
- [ ] PDF A4 generato: frontespizio, capitoli rilevati, corpo giustificato, pagine numerate
- [ ] Controllo a campione traduzione vs originale fatto
- [ ] Limiti comunicati all'utente (niente OCR, layout grafico non preservato)
