# La relazione

Due documenti diversi, a seconda di cosa ha chiesto l'utente.

**L'analisi** risponde a "cosa dicono le recensioni": numeri, trend, punti forti, punti
deboli. È il documento del dato.

**La relazione operativa** risponde a "cosa faccio": segue il viaggio del cliente momento
per momento e per ogni problema dà l'azione, chi la fa e come si verifica. È il documento
della decisione, e di solito è quello che il ristoratore usa davvero.

Se l'utente non specifica, comincia dall'analisi e proponi la relazione operativa come
passo successivo — soprattutto se ha anche appunti presi in sala, perché è lì che i due
mondi si incontrano.

---

## Struttura dell'analisi

1. **Copertina** con fascia di 4 numeri: il volume, la media, la percentuale sotto soglia,
   e un numero che dia il senso del movimento (la crescita della media, o il dato più
   recente disponibile).
2. **Perimetro, metodo e limiti.** Una tabella con, per ogni fonte: quante recensioni,
   con quale ordinamento, e a cosa serve in questo documento. Va per prima, non in fondo:
   è quello che dice al lettore quanto può fidarsi di ciò che segue.
3. **I numeri per data.** Medie del periodo, distribuzione dei voti, e soprattutto la
   **tabella per mese** con media, voci analitiche e percentuale sotto soglia. Sotto la
   tabella, due o tre frasi che dicono cosa si vede solo guardando in ordine di data.
4. **Il presente**, se una fonte ti ha dato una finestra molto recente e completa. È la
   sezione che il ristoratore legge per prima.
5. **Punti forti.** Uno per paragrafo, ciascuno con il conteggio che lo sostiene e una
   citazione. Un punto di forza senza numero è un complimento.
6. **Punti deboli**, ordinati per impatto e non per frequenza. Apri con la tabella delle
   cause per mese, perché è quella che orienta tutto il resto.
7. **La lettura d'insieme.** Poche righe che collegano i punti deboli in un unico tema.
   Se non riesci a scriverle, l'analisi non è finita.
8. **Piano di miglioramento**: tabella con azione, perché, impatto, sforzo.
9. **Come misurare**: 4-6 indicatori con valore di oggi e obiettivo.
10. **Nota metodologica.** Cosa hai letto per data, cosa no, e cosa resta fuori.

## Struttura della relazione operativa

Stessa apertura (numeri + tesi in tre righe), poi:

1. **Dove siamo** — i numeri di cassa se ci sono, il trend delle recensioni, le cause.
2. **La diagnosi** — il tema unico sotto ai sintomi. Nei locali ben gestiti quasi sempre
   non è competenza ma **varianza**: le cose giuste sono già scritte da qualche parte e
   non sono entrate nei comportamenti.
3. **Il viaggio del cliente**, un momento per volta: prima dell'arrivo, l'arrivo, l'ordine,
   il primo morso, il conto, il governo della sala, il dopo. Per ciascuno tre blocchi
   fissi — *cosa dicono le recensioni*, *cosa hai osservato tu*, *cosa fare* — più le
   frasi esatte da far dire allo staff.
4. **Il linguaggio** — una pagina sola con tre colonne: si dice così / non si dice / perché.
   È la pagina che il ristoratore appende.
5. **Il sistema che rende tutto verificabile** — i riti brevi (briefing, checklist,
   debrief) che trasformano il documento in comportamento.
6. **Piano a 14 giorni** con chi e entro quando.
7. **Cruscotto** e **cosa non è in questo documento**.

---

## Come scrivere

**Ogni affermazione porta il suo numero.** "Il servizio è buono" non serve; "72 recensioni
su 183 citano la gentilezza, e il voto servizio supera quello del cibo" sì.

**Le citazioni sono la prova.** Una per punto debole, testuale, con piattaforma, data e
voto. Non riportare i nomi degli autori.

**Le azioni sono comportamenti, non intenzioni.** "Migliorare la comunicazione in cassa"
non è un'azione. "Un foglio A4 affisso in cassa con tre righe: come si legge la
prenotazione, su cosa si applica lo sconto, verifica dello scontrino prima di consegnarlo"
lo è.

**Le frasi per lo staff vanno scritte alla lettera**, non descritte. Una frase che il
cameriere può imparare a memoria vale dieci righe di principio. E quando l'utente te ne
detta una sua, usala parola per parola: la conosce meglio di te.

**Dai la buona notizia per prima quando c'è.** Questi documenti finiscono in mano a chi ci
lavora dentro tutti i giorni. Se il locale sta migliorando, dirlo per primo non è
cortesia: è ciò che rende leggibile la parte critica.

---

## Impaginazione

Usa `report_kit.py` — ha già copertina, capitoli numerati, tabelle, riquadri, citazioni,
fascia dei numeroni e piè di pagina.

```python
import sys; sys.path.insert(0, "<cartella di questa skill>")
from report_kit import Report

doc = Report("/percorso/Analisi.pdf",
             kicker="ANALISI RECENSIONI · 16 MAGGIO – 16 AGOSTO 2026",
             titolo="Nome del locale — Città",
             sottotitolo="Punti forti, punti deboli e piano di miglioramento",
             footer="Nome locale · Analisi recensioni · agosto 2026")

doc.kpi([("265", "recensioni nel periodo<br/>ordinate per data"),
         ("8,79", "media /10<br/>agosto: 8,91"),
         ("27", "sotto il 7/10<br/>pari al 10,2%")])
doc.panel("<b>La tesi in tre righe.</b> …")
doc.h1("Perimetro, metodo e limiti", "1")
doc.table([["Fonte", "Nel periodo", "Ordinamento", "Uso"],
           ["<b>TheFork</b>", "265", "Per data", "Fonte di riferimento"]],
          [24, 30, 45, 62])
doc.quote("Tutto è crollato al momento del conto.", "TheFork · 11 luglio · 6/10")
doc.script("Il tavolo è vostro fino alle 21, va bene?")
doc.build()
```

Prima di consegnare, apri il PDF e guarda almeno tre pagine renderizzate: le colonne
strette spezzano le parole a metà e le mezze pagine bianche si vedono solo così.
Il PDF va consegnato **senza password né restrizioni**, e in `~/Downloads` se l'utente
non indica altro.
