# Ponte "fatto in casa" Resmio → GHL

> Contributo di Andrea Chirivì, 2026-10-12. In produzione su un cliente dal
> 24/09/2026 (registro sotto lock e riprova delle righe `ko` dal 02/10/2026).
> Nessuna chiave o dato di un cliente specifico in questo file.

## Quando serve

Il ponte di terzi perde eventi o si ferma, e il cliente ha un hosting dove gira
PHP: in questi casi conviene un ponte "fatto in casa" invece di dipendere da un
servizio esterno che non controlliamo.

## Com'è fatto

Un webhook Resmio dedicato chiama un endpoint PHP sul dominio del cliente. Usa una
**Private Integration dedicata** con i soli scope contatti e calendari, e la
chiave sta **solo sul server del cliente** — mai nel repo, mai nel JS del browser
(vedi anche la regola gemella in `cdg-fatture/google-accessi.md` sulle chiavi che
non devono mai stare sul server di un cliente).

## Cosa deve fare

1. **Prima di spegnere il vecchio ponte**: inventario completo di cosa scriveva e
   replica di tutto — campi prenotazione, tag di stato, appuntamento sul
   calendario.
2. Scrivere il **codice di gestione prenotazione** sul contatto (link Resmio, vedi
   `template-pronti.md` n.1).
3. Riscrivere tag e campo di stato **solo quando lo stato cambia**: la decisione si
   legge da un registro sotto lock, così la conferma non parte mai due volte.
4. **Non scrivere sui campi che appartengono ad altri flussi** (es. campi coupon
   gestiti altrove).
5. Tenere un **registro di ogni evento** con riga `ok`/`ko`. Gli errori passeggeri
   di Resmio o GHL diventano righe `ko` che un giro riprova (ogni 10 minuti, al
   massimo 4 volte).
6. Avere un **replay manuale** con flag (es. `riaggancia`) che rimette a posto una
   prenotazione senza toccare campi e tag già corretti.
7. Se esiste già un appuntamento a ±20 minuti (lasciato dal ponte vecchio o da un
   terzo ancora attivo), **adottarlo** invece di crearne un doppione. Mai adottare
   però l'appuntamento di un'altra prenotazione attiva.
8. Prima di accendere: due giri di revisione e una modalità prova. Dopo
   l'accensione, collaudare il promemoria su una prenotazione nata col ponte
   **nuovo**, mai su una vecchia (vedi `toNotify` in SKILL.md Pattern A).

## Rimandi (non riscrivere qui)

- `toNotify` e promemoria 4 ore: SKILL.md Pattern A.
- Errore 400 sui doppioni e guardia sullo stato: SKILL.md Pattern A.
- Ora senza secondi: `template-pronti.md`, Regole comuni.
- Orologio del giro (ogni 10 minuti, max 4 tentativi): `make-scenario-dod/SKILL.md`.

## Nella checklist di consegna

Quando il ponte è nostro: aggiungere "registro ok/ko e giro di recupero delle righe
`ko`" al punto 6 della checklist in SKILL.md.
