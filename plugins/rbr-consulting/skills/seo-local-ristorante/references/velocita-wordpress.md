# Velocità di un WordPress in hosting condiviso

Metodo per gli interventi di §6 "Core Web Vitals / velocità" — **tutti SOLO
supervisionati**: ogni modifica va verificata a schermo su mobile e desktop, prima e dopo.

*(contributo di Andrea Chirivì, 2026-10-12, misurato dall'esterno prima e dopo)*

1. **Misura dall'esterno prima e dopo**: TTFB, peso pagina, numero di asset e di JS.
2. **Cache di pagina**: spesso già installata ma spenta (es. WP-Optimize). Attivala col
   preload delle URL principali e aggiungi `Cache-Control` a 1 anno sui file statici.
   Esempio misurato: TTFB da 3,1s a 0,11s, caricamento da 5,8s a 0,39s.
3. **Plugin che caricano asset senza servire a nulla**: disattiva (senza disinstallare, e
   con l'ok del cliente) plugin e-commerce/social non usati che caricano comunque script.
4. **Immagini in WebP**: un ottimizzatore che converte in locale (GD/Imagick) senza
   account o API key va bene per siti piccoli. Attiva: conversione WebP, lazy load, bulk
   "solo WebP" (tieni gli originali), e la riscrittura automatica dell'HTML verso i
   `.webp` — su nginx è indispensabile, altrimenti i file WebP nascono ma non vengono
   serviti. Non quantizzare mai le foto a 256 colori (si vedono macchie): preferisci
   WebP. Attenzione: il lazy load applicato anche agli iframe imbarcati (es. un modulo
   GHL) può lasciarli bianchi per 1-2 secondi — non è un guasto.
5. **Sfondi CSS (hero, pop-up) non si convertono da soli**: serve una regola `!important`
   verso il file `.webp` già generato, che copra tutte le varianti del selettore (base,
   `:after`, `:hover`, `:hover:after`). Se ci sono regole diverse per larghezza, l'override
   va nella stessa media query, altrimenti su mobile esce un ritaglio sbagliato. Se il
   builder del sito rigenera la classe, si torna al JPG senza rompere nulla.
6. **Feed social (es. Instagram) sotto la piega**: solo se il feed è davvero sotto la
   piega, applica il lazy load alle sue immagini con uno snippet mirato (es. un
   MutationObserver che interviene prima che il plugin assegni lo `src`), aggiungendo
   l'alt mancante all'immagine del profilo.
7. Ogni override va riverificato a schermo su mobile e desktop, prima e dopo: è il motivo
   per cui questi interventi restano "supervisionati" e non automatici.
