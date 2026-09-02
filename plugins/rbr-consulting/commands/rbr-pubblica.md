---
description: Pubblica SUBITO una nuova versione del plugin RBR a tutti i consulenti (aggiornamento automatico entro ~1h30). Riservato a Marco / chi ha il repo rbr-suite e gh autenticato.
---

Sei l'addetto ai rilasci del plugin RBR. Questo comando fa arrivare a tutti i consulenti una
versione nuova del plugin, senza che loro facciano nulla. Argomenti: $ARGUMENTS
(vuoto o "veloce" = pubblica quello che c'è; "completo" = prima integra contributi e novità come il lunedì).

## 0. Prerequisiti (verifica, non chiedere)
- Clone del repo privato `rbr-suite` sul Mac: cerca `plugins/rbr-consulting/.claude-plugin/plugin.json`
  in `~/Desktop/AI/RBR AI/suite`, `~/Desktop/AI/rbr-suite`, `~/Documents`, `~/dev`. Se non c'è: questo
  comando è per Marco (o chi ha accesso al repo) → fermati e dillo.
- `gh auth status` deve essere autenticato (serve per PR e merge sul marketplace pubblico).
- `~/.claude/rbr/credentials.json` e `config.json` presenti (Conoscenza live + Telegram).

## 1. Modalità
- **veloce** (default): salta al punto 2. Serve quando Marco ha modificato skill/regole/`.mcp.json`
  a mano o vuole solo forzare l'aggiornamento di tutti.
- **completo**: esegui PRIMA le Fasi 1-4 della skill `aggiorna-conoscenza-rbr` in locale
  (contributi dal foglio → skill; ricerca novità → memory/skill; filtro). NON fare tu il bump di
  versione né il CHANGELOG: li fa lo script al punto 2. Usa `--minor` se hai creato skill nuove.

## 2. Rilascio (meccanica, tutta nello script)
Componi 1-4 righe di changelog scritte per chi lavora (cosa cambia, cosa deve fare), poi:
```
python3 <suite>/tools/rilascia.py --nota "riga 1" --nota "riga 2" [--minor] \
  --live "sintesi operativa 1-3 righe per il tab Conoscenza live" --telegram
```
Lo script: pull, bump, CHANGELOG, commit+push rbr-suite, build pubblico SENZA segreti
(la scansione anti-segreti blocca tutto se trova token: in quel caso togli il segreto e rilancia),
PR + merge sul marketplace (l'unico evento che fa aggiornare il server claude.ai), verifica su GitHub,
riga Conoscenza live, Telegram a Marco, puntatore submodule nel monorepo. Prima puoi fare `--dry-run`.

## 3. Cosa dire a Marco alla fine (2-4 righe)
Versione pubblicata, cosa contiene, e la regola dei tempi: server claude.ai entro 30 min dal merge,
app Cowork di ogni consulente entro l'ora successiva → ~1h30; alla prima chat nuova ognuno vede
"🆕 Plugin aggiornato alla vX". La Conoscenza live è già attiva alla prossima chat. Chi ha fretta:
Personalizza → Plugin → Rbr consulting → Aggiorna.
