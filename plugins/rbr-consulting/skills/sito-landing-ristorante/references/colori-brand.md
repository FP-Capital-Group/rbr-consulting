# Colori veri del brand di un cliente (dal sito e dal logo) — e leggibili

(contributo di Luciano Purpi, 2026-09-08)

Serve ogni volta che un canale (sito, landing, mail, widget Resmio, coupon) deve avere i
colori del cliente. Non si scelgono a occhio e non si chiede il manuale di brand che nessun
ristoratore ha: si **leggono**.

## 1. Dal sito: colori calcolati, non stimati
Dalla console del sito del cliente:
```js
const c={};
document.querySelectorAll('*').forEach(e=>{const s=getComputedStyle(e);
  [s.color,s.backgroundColor].forEach(v=>{if(v&&!v.includes('rgba(0, 0, 0, 0)'))c[v]=(c[v]||0)+1})});
Object.entries(c).sort((a,b)=>b[1]-a[1]).slice(0,12)
```
Il colore del marchio è quello con molte occorrenze che NON è bianco/nero/grigio.
Rumore da scartare:
- tavolozza di default di Gutenberg (#ff6900 #fcb900 #0693e3 #00d084 #cf2e2e…): se in un grep
  dell'HTML escono TUTTI quei valori una volta sola a testa, è la tavolozza vuota di
  WordPress — il sito non dice niente;
- widget di terzi (Google #1a73e8/#fbbc04, Deliveroo #00ccbc).

## 2. Dal logo: PIL, scartando i pixel neutri
Altrimenti vince sempre il bianco o il nero:
```python
h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
if a < 200 or s*100 < 18 or v*100 < 12 or v*100 > 97: continue   # trasparente/neutro/estremi
cnt[(r//24*24, g//24*24, b//24*24)] += 1
```
Se i pixel cromatici sono ~0, il logo è solo bianco/nero: il colore va cercato altrove (sito,
insegna, foto). Il logo ORIGINALE a colori sta quasi sempre nel WordPress del cliente
(`/wp-content/uploads/...`, la versione senza "cropped-" e senza misure); quello caricato sui
gestionali è spesso monocromatico.

## 3. Controllo obbligatorio PRIMA di applicare: contrasto WCAG ≥ 4,5:1
Su OGNI accostamento testo/sfondo. Un giallo o un arancio di marca su bianco sta tipicamente a
2-3:1: bellissimo sull'insegna, illeggibile in una mail. Si tiene la tinta e la si scurisce
finché passa (es. #FFA600 → #9C6200 per il testo), lasciando #FFA600 al pulsante dove sopra
c'è testo scuro.
```python
def lum(hexc):
    r, g, b = (int(hexc.lstrip('#')[i:i+2], 16)/255 for i in (0, 2, 4))
    f = lambda c: c/12.92 if c <= 0.03928 else ((c+0.055)/1.055)**2.4
    return 0.2126*f(r) + 0.7152*f(g) + 0.0722*f(b)
def cr(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)
```
Su 10 clienti 6 palette non passavano al primo giro e sono state corrette prima di andare
online. È l'unica parte che il cliente nota subito se è sbagliata.

## Note RBR
- Sui siti generati col template siti-ristoranti resta la regola hard dei **toni caldi**: se il
  colore di marca letto è freddo (blu, viola…), segnalalo a Marco prima di applicarlo.
- Per mail e widget Resmio (dove stanno i 14 campi colore, i campi che mentono, l'anteprima
  senza toccare l'account) → `suite/memory/resmio.md`, sezione Branding.
