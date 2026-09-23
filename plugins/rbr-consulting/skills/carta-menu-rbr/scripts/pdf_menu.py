# -*- coding: utf-8 -*-
"""PDF di stampa di una carta RBR partendo dall'HTML dell'artifact (vista cliente).

Uso:
  python3 pdf_menu.py soffietto <menu.html> <out.pdf> [--ante 100,100,100,66]
  python3 pdf_menu.py libro     <menu.html> <out.pdf>

- soffietto: ogni <div class="blocco"> (fronte, retro) = una pagina larga quanto la somma
  delle ante x 297 mm; le <section class="anta"> vengono piazzate a coordinate ASSOLUTE
  (il flex orizzontale in WeasyPrint le impila: errore già pagato su Giurges).
- libro: ogni <section class="pag"> = una facciata A4.

Cosa fa in entrambi i casi: toglie barra, script ed etichette dell'artifact, nasconde la
vista consulente (.nota .mk .rank), trasforma i tratteggi in linee continue (il dashed manda
WeasyPrint in overflow), risolve gli <use href="#simbolo"> inlineando i <symbol>, e converte
i flex VERTICALI in blocchi con margini (in WeasyPrint sballano). Dopo: controlla il numero
di pagine; se una facciata sfora, riduci corpi di ~1pt e foto (22→18 mm) nel CSS EXTRA.
"""
import re, sys, os, argparse
from weasyprint import HTML

NASCONDI = '.bar,.etichetta,.nota,.mk,.rank{display:none !important}\n'

BLOCCHI = '''
.sec,.piatti,.grossi,.rcards,.combos,.taglie,.lst,.misure,.testa,.banda,.chiudi,.portate,.manifesto{display:block !important}
.piatti > .p{margin-bottom:2.8mm} .piatti > .p:last-child{margin-bottom:0}
.sec{margin-bottom:5mm} .sec:last-child{margin-bottom:0}
.rcards > .rcard,.lst > .lr,.taglie > .taglia,.combos > .combo{margin-bottom:2.4mm}
/* righe orizzontali: restano flex */
.p .riga,.form,.aggiunte,.cop-riga,.flist,.bev{display:flex !important}
.p.pfoto,.gitem,.rcard,.lr,.taglia,.portata{display:flex !important;gap:3mm;align-items:flex-start}
.p.pfoto > div:first-child,.gitem > div:first-child,.lr .n{flex:1 1 auto}
.foto{display:flex !important;align-items:center;justify-content:center;
      border-style:solid !important;flex:0 0 18mm;width:18mm;height:18mm}
.vin,.p .birra{display:block !important;margin-top:1mm}
.vin svg,.p .birra svg{vertical-align:-2px;margin-right:1.2mm}
.f,.chip{display:inline-flex !important}
'''


def pulisci(s):
    s = re.sub(r'<div class="bar">.*?</div>\s*(?=<div class="piano">)', '', s, flags=re.S)
    s = re.sub(r'<script>.*?</script>', '', s, flags=re.S)
    s = s.replace('dashed', 'solid')
    simboli = {m.group(1): (m.group(2), m.group(3)) for m in
               re.finditer(r'<symbol id="([^"]+)" viewBox="([^"]+)">(.*?)</symbol>', s, re.S)}

    def _use(m):
        attrs, sid = m.group(1), m.group(2)
        if sid not in simboli:
            return m.group(0)
        vb, corpo = simboli[sid]
        a = attrs if 'viewBox' in attrs else attrs + f' viewBox="{vb}"'
        return f'<svg {a}>{corpo}</svg>'
    return re.sub(r'<svg\s([^>]*?)>\s*<use href="#([^"]+)"\s*/?>\s*</svg>', _use, s, flags=re.S)


def css_soffietto(ante):
    tot = sum(ante)
    c = [f'@page{{size:{tot}mm 297mm;margin:0}}',
         'html,body{margin:0;padding:0;background:#fff}',
         '.piano{padding:0 !important;overflow:visible !important}',
         f'.blocco{{margin:0 !important;width:{tot}mm !important;page-break-after:always}}',
         '.blocco:last-child{page-break-after:auto}',
         f'.menu{{display:block !important;position:relative;width:{tot}mm;height:297mm;box-shadow:none !important;overflow:hidden}}',
         '.anta{position:absolute !important;top:0;height:297mm;padding:11mm 8mm 9mm !important;'
         'border-right:0 !important;overflow:hidden;display:block !important}']
    x = 0
    for i, w in enumerate(ante, 1):
        c.append(f'.anta:nth-of-type({i}){{left:{x}mm;width:{w}mm !important;flex:none !important}}')
        x += w
    return '\n'.join(c) + '\n'


CSS_LIBRO = '''
@page{size:210mm 297mm;margin:0}
html,body{margin:0;padding:0;background:#fff}
.piano{padding:0 !important;overflow:visible !important}
.spread,.doppia{display:block !important;margin:0 !important;width:210mm !important;box-shadow:none !important}
.pag{width:210mm !important;height:297mm;min-height:0 !important;overflow:hidden;
     page-break-after:always;border-left:0 !important;display:block !important}
.spread:last-child .pag:last-child{page-break-after:auto}
.pag.centrata{display:flex !important;flex-direction:column;justify-content:center;align-items:center}
'''


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('formato', choices=['soffietto', 'libro'])
    ap.add_argument('html'); ap.add_argument('out')
    ap.add_argument('--ante', default='100,100,100,66', help='larghezze ante in mm (soffietto)')
    ap.add_argument('--extra-css', default='', help='file CSS aggiuntivo (scala tipografica di stampa)')
    a = ap.parse_args()
    s = pulisci(open(a.html, encoding='utf-8').read())
    css = NASCONDI + BLOCCHI
    css += css_soffietto([float(x) for x in a.ante.split(',')]) if a.formato == 'soffietto' else CSS_LIBRO
    if a.extra_css:
        css += open(a.extra_css, encoding='utf-8').read()
    s = s.replace('</body>', f'<style>{css}</style></body>') if '</body>' in s else s + f'<style>{css}</style>'
    base = os.path.dirname(os.path.abspath(a.html))
    open(os.path.join(base, '_print_' + os.path.basename(a.html)), 'w', encoding='utf-8').write(s)
    attese = s.count('class="pag') if a.formato == 'libro' else s.count('class="blocco"')
    # auto-compattazione: se una facciata sfora (pagine > attese) stringe corpi, spazi e foto
    for livello in range(0, 5):
        k = 1 - 0.06 * livello
        comp = '' if not livello else f'''
.nome,.p .nome{{font-size:{10.2*k:.1f}pt !important}} .desc,.p .desc{{font-size:{8.4*k:.1f}pt !important}}
.vin,.p .birra,.form,.f{{font-size:{7.8*k:.1f}pt !important}}
.piatti > .p{{margin-bottom:{2.8*k:.1f}mm !important}} .sec{{margin-bottom:{5*k:.1f}mm !important}}
.foto{{flex-basis:{18*k:.0f}mm !important;width:{18*k:.0f}mm !important;height:{18*k:.0f}mm !important}}
.pag{{padding-top:{16*k:.0f}mm !important;padding-bottom:{12*k:.0f}mm !important}}
'''
        doc = HTML(string=s.replace('</body>', f'<style>{comp}</style></body>'), base_url=base).render()
        if len(doc.pages) <= attese:
            break
    doc.write_pdf(a.out)
    nota = f' (compattato livello {livello})' if livello else ''
    esito = 'OK' if len(doc.pages) == attese else f'⚠️ ATTESE {attese}'
    print(f'{esito} {a.out} — {len(doc.pages)} pagine{nota}')


if __name__ == '__main__':
    main()
