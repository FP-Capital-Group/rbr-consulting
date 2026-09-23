# Collaudo di una catenaria email su GHL (nuova o ereditata)

(contributo di Luciano Purpi, 13/09/2026)

Su 28 email di una catenaria ereditata, già in bozza e pronta per l'accensione, 26 portavano a una
pagina inesistente: le landing non erano mai state create. Nessuno se n'era accorto perché nessuno
aveva cliccato. **Il controllo che nessuno fa è aprire i link: farlo per primo.**

## Come si collauda

Non si guardano le email a schermo (ore, e non trova niente): si scaricano i sorgenti e si passa
uno script.

1. Dalla **libreria modelli** (Marketing → Email, NON dal workflow): apri modello → clic dentro il
   codice → cmd+a, cmd+c → `pbpaste > audit/catNN.html`. In quell'editor il salvataggio automatico è
   acceso: **si copia e basta, non si digita mai.**
   ⚠️ Il nodo Email del workflow può avere una copia propria diversa dal modello: se la spunta
   "Sincronizza le modifiche al modello" è tolta, collauda la copia del nodo (vedi `builder-ghl.md`).
2. I file arrivano in Windows-1252 (accenti storpiati, per i link non conta): usare `LC_ALL=C grep -a`.

```bash
for u in $(LC_ALL=C grep -aoh 'https://[^"?]*' audit/*.html | sort -u); do
  printf '%s %s\n' "$(curl -s -o /dev/null -w '%{http_code}' -L "$u")" "$u"; done
LC_ALL=C grep -aL 'unsubscribe' audit/*.html   # chi non ha la disiscrizione
LC_ALL=C grep -aL 'href="http' audit/*.html     # chi non ha una via d'uscita
```

## Lista di controllo (10)

1. Le pagine di destinazione esistono (codice HTTP vero).
2. Ogni email ha almeno un link per prenotare.
3. La disiscrizione c'è in TUTTE.
4. Indirizzo e telefono giusti (a Barresi il civico era sbagliato).
5. Le foto mostrano persone che ci sono ancora (turnover alto: una squadra di due anni fa smentisce il testo).
6. Nessuna email o pagina linkata cita un dominio che il cliente non controlla più (quello storico
   di Barresi era stato ripreso da altri e riempito di spam: nominarlo trascina giù la reputazione del mittente).
7. La lingua è quella del destinatario (un ramo "turisti" in italiano non serve a niente).
8. Tracciamenti presenti e distinti, uno per email.
9. Condizioni dell'offerta scritte (durata, non cumulabile, una per tavolo, solo in sala).
10. I campi dinamici hanno un ripiego (`{{contact.first_name}}` vuoto produce "Ciao ,").

Più il controllo di coerenza: il testo di ogni email corrisponde al PUNTO del percorso in cui si
trova il cliente (i testi migrano fra flussi quando si duplicano i workflow — vedi `builder-ghl.md`).

## Le pagine mancanti si clonano, non si riscrivono (WordPress + Elementor)

Dalla sessione WordPress già autenticata:
- `GET /wp-json/wp/v2/pages/<id-modello>?context=edit` → `meta._elementor_data` (stringa JSON)
- `POST /wp-json/wp/v2/pages` con `{title, slug, status:'publish', meta:{_elementor_data}}`

Poi **noindex su tutte**: sono pagine di campagna, chi ci arriva da Google prende un'offerta non sua
e l'offerta perde valore.
- **Yoast:** il noindex NON è scrivibile via REST. Apri `post.php?post=<id>&action=edit`, metti a `1`
  l'input nascosto `#yoast_wpseo_meta-robots-noindex` CON IL SETTER NATIVO (altrimenti React lo
  ignora), poi `wp.data.dispatch('core/editor').savePost()`.
- **AIOSEO:** la via REST esiste ma vuole il `currentPost` intero.
- Se il frontend non cambia dopo una modifica via REST: cache elementi Elementor
  (`suite/memory/gohighlevel.md`, sezione Elementor).

## Tracciamento: sul sito, non nelle email

Le email sono decine e cambiano. Un solo pezzo di codice sul sito legge `?utm=<etichetta>` dal link,
mappa il percorso alla campagna e inietta la nota nel widget di prenotazione. La prenotazione arriva
in sala CON LA NOTA GIÀ SCRITTA ("Tartare in omaggio"): il cliente non esibisce niente, lo staff non
discute, i riscatti si contano dal gestionale senza integrazioni. Salva sempre una copia dello
snippet prima di toccarlo: è l'unico punto da cui passa tutto il tracciamento del locale.

## È pronto quando

I 10 controlli sono verdi **e** sai dire per iscritto cosa succede a un contatto che entra oggi,
giorno per giorno. Se non sai dirlo non è pronto, è solo salvato.
