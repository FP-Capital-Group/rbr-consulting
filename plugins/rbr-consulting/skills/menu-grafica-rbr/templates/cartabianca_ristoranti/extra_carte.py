# -*- coding: utf-8 -*-
"""Carta dei dolci A5 rossa + carta degli allergeni A4 (Tennis e Club), da stampare.
Uso: python3 extra_carte.py  → Carta_dolci_A5.pdf · Carta_allergeni.pdf (+ HTML)"""
import html, os
from weasyprint import HTML
import build as B
from dati import TENNIS, CLUB

E = html.escape
HERE = os.path.dirname(os.path.abspath(__file__))
FONT = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Lora:ital,wght@0,400;0,600;0,700;1,400&display=swap">'
ALG = ['Glutine', 'Crosta-<br>cei', 'Uova', 'Pesce', 'Arachidi', 'Soia', 'Latte', 'Frutta a<br>guscio', 'Sedano', 'Senape',
       'Sesamo', 'Solfiti', 'Lupini', 'Mollu-<br>schi']
LEG = ('I piatti che presentano l’asterisco potrebbero essere preparati con prodotti congelati o abbattuti in base alla disponibilità.<br>'
       'L’elenco completo degli allergeni presenti nei nostri piatti è disponibile su richiesta. Consulta il personale o richiedi il documento dedicato.<br>'
       'Prezzi espressi in euro. Coperto e Servizio | 2,5')
PIATTO = ('<svg viewBox="0 0 120 70"><ellipse cx="60" cy="38" rx="54" ry="24" fill="none" stroke="#F3C9C4" stroke-width=".8"/>'
          '<ellipse cx="60" cy="37" rx="36" ry="15" fill="rgba(255,255,255,.08)" stroke="#F3C9C4" stroke-width=".5"/>'
          '<text x="60" y="40" text-anchor="middle" font-size="6" letter-spacing="1.4" fill="#F3C9C4">FOTO</text></svg>')


def dolci(L):
    ctx = B.costruisci(L)
    D = ctx['C']['dolci']
    from dati import FOTO_VERE
    righe = ''
    for p in D:
        riga = f'<b>{E(p["nome"])}</b><span>{B.attacca_prezzo(E(p["desc"]), B.prz(p["new"]), B.AST(p)).replace(chr(10), "<br>")}</span>'
        if p.get('rank') == 1:
            f = FOTO_VERE.get(p['nome'])
            img = f'<img src="{B.img64(f)}">' if f else ''
            righe += f'<div class="d n1{" con-foto" if f else ""}"><div class="tx">{riga}</div>{img}</div>'
        else:
            righe += f'<div class="d">{riga}</div>'
    return f"""<section class="a5">
      <div class="top"><em>{E(L["nome_cop"])}</em></div>
      <h1>I dolci</h1><p class="sotto">tutti dalla nostra pasticceria, fatti ogni giorno</p>
      <div class="lista">{righe}</div>
      <p class="leg">{LEG}</p></section>""" + dopo(L, ctx)


def dopo(L, ctx):
    r = lambda n, v: f'<div class="r"><b>{E(n)}</b> <span class="sep">|</span> <span class="prezzo">{B.prz(v)}</span></div>'
    am = ''.join(r(n, nw) for (n, o, nw) in L['amari'])
    cf = ''.join(r(n, v) for n, v in L['caffe'] + L['acque'])
    sb = ctx['sorb']
    return f"""<section class="a5 retro">
      <div class="top"><em>{E(L["nome_cop"])}</em></div>
      <h1>Dopo cena</h1><p class="sotto">per chiudere in bellezza</p>
      <h2>Amari e distillati</h2><div class="col">{am}</div>
      <h2>Fresco</h2><div class="d"><b>{E(sb["nome"])}</b><span>Al naturale <span class="sep">|</span> <span class="prezzo">{B.prz(sb["new"])}</span> · con prosecco o vodka <span class="sep">|</span> <span class="prezzo">7,5</span></span></div>
      <h2>Caffetteria</h2><div class="col">{cf}</div>
      </section>"""


def allergeni(L):
    ctx = B.costruisci(L)
    C = ctx['C']
    sez = [('Antipasti', C['premium_antipasti'] + C['antipasti']), ('Primi', C['premium_primi'] + C['primi']),
           ('Secondi e contorni', C['premium_secondi'] + C['secondi'] + C['contorni']),
           ('Pizze', C['tartufate'] + C['classiche'] + C['gourmet'] + C['speciali']), ('Dolci', C['dolci'] + [ctx['sorb']])]
    th = ''.join(f'<th><div>{a}</div></th>' for a in ALG)
    body = ''
    for t, items in sez:
        body += f'<tr class="sez"><td colspan="15">{t}</td></tr>'
        for p in items:
            cod = {int(x) for x in str(p.get('alg') or '').split('-') if x.strip().isdigit()}
            body += f'<tr><td class="n">{E(p["nome"])}</td>' + ''.join(f'<td>{"●" if i in cod else ""}</td>' for i in range(1, 15)) + '</tr>'
    return f'''<section class="a4">
      <h1>Carta degli allergeni</h1><p class="sotto">{E(L["nome_cop"])} · Regolamento UE 1169/2011</p>
      <p class="nota">● = l’allergene è presente nella ricetta. In cucina usiamo tutti questi ingredienti: non possiamo escludere tracce.
      Per allergie o intolleranze parlate sempre con il personale prima di ordinare.</p>
      <table><thead><tr><th class="n"></th>{th}</tr></thead><tbody>{body}</tbody></table></section>'''


CSS_D = '''@page{size:148mm 210mm;margin:0}
body{margin:0;font-family:Lora,Georgia,serif;color:#2B2220}
.a5{width:148mm;height:210mm;background:#fff;padding:15mm 14mm 0;box-sizing:border-box;position:relative;page-break-after:always}
.top{display:flex;align-items:center;justify-content:center;gap:3mm;color:#8A1C2B}
.top span{width:14mm;height:.5pt;background:#8A1C2B}.top em{font-size:9pt;white-space:nowrap}
h1{font-weight:700;font-size:34pt;text-align:center;margin:5mm 0 0;line-height:1;color:#8A1C2B}
.sotto{font-style:italic;font-size:9pt;text-align:center;color:#6E6058;margin:1.5mm 0 8mm}
.d{margin-bottom:4mm}.d b{display:block;font-size:11pt;font-weight:700;color:#2B2220}
.d span{display:block;font-size:8.8pt;color:#4A3F3A;line-height:1.45}
.d.n1{background:#8A1C2B;color:#fff;padding:4.5mm 5mm;margin:1mm 0 5mm;display:flex;align-items:center;gap:3mm}
.d.n1 .tx{flex:1}
.d.n1 b{color:#fff;font-size:14pt;margin-bottom:1mm}.d.n1 span{color:#F6DCD9;font-size:9pt}
.d.n1 img{width:46mm;height:31mm;object-fit:contain;margin:-6mm -9mm -6mm 0}
.per2{display:block;font-style:normal;font-size:10pt;color:#fff;margin-top:1.6mm}
h2{font-size:13pt;font-weight:700;margin:6mm 0 2.4mm;color:#8A1C2B}
.col{columns:2;column-gap:8mm}
.col .r{font-size:9.6pt;margin-bottom:1.6mm;color:#4A3F3A;break-inside:avoid}.col .r b{font-weight:600;color:#2B2220}
.d:not(.n1){margin-bottom:6mm}.d:not(.n1) span{font-size:9.4pt}.d:not(.n1) b{font-size:12pt}.col .r{margin-bottom:2.4mm !important;font-size:10pt !important}h2{margin-top:8mm !important}
/* 06/10 Marco: prezzo discreto ovunque — più piccolo, mai bold, colore della descrizione o più chiaro */
.prezzo{display:inline !important;font-size:.88em;font-weight:400;color:#7A6C64}
.d:not(.n1) span.prezzo,.d span span.prezzo{font-size:8.3pt !important;color:#7A6C64 !important}
.d.n1 span.prezzo{font-size:8.3pt !important;color:#F3C9C4 !important}
.col .r .prezzo{font-size:8.8pt;color:#7A6C64}
.sep{opacity:.5}
.d span span{display:inline !important}
.leg{position:absolute;left:14mm;right:14mm;bottom:10mm;font-size:5.4pt;line-height:1.4;color:#8C7F78;margin:0}'''
CSS_A = '''@page{size:210mm 297mm;margin:9mm 12mm 8mm}
body{margin:0;font-family:Lora,Georgia,serif;color:#222}
.a4{page-break-after:always}
h1{font-size:17pt;margin:0;font-weight:700;color:#8A1C2B}
.sotto{font-style:italic;font-size:8.6pt;color:#666;margin:.6mm 0 2.4mm}
table{width:100%;border-collapse:collapse;font-size:7.4pt}
th{font-weight:600;font-size:5.6pt;line-height:1.15;vertical-align:bottom;padding:0 .3mm 1.2mm;border-bottom:.8pt solid #222}
th div{text-align:center}
th.n,td.n{text-align:left;width:62mm}
td{border-bottom:.4pt solid #ddd;text-align:center;padding:.05mm .4mm;font-size:6.4pt;line-height:1.18}
tr.sez td{font-weight:700;font-size:8pt;text-align:left;border-bottom:.8pt solid #222;padding-top:1.6mm;color:#8A1C2B}
.nota{font-size:7pt;color:#444;margin:0 0 2mm;line-height:1.4}'''


def pdf(body, css, out):
    doc = f'<!doctype html><html><head><meta charset="utf-8">{FONT}<style>{css}</style></head><body>{body}</body></html>'
    open(os.path.join(HERE, out.replace('.pdf', '.html')), 'w').write(doc)
    r = HTML(string=doc, base_url=HERE).render()
    r.write_pdf(os.path.join(HERE, out))
    print('OK', out, len(r.pages), 'pagine')


if __name__ == '__main__':
    pdf(dolci(TENNIS) + dolci(CLUB), CSS_D, 'Carta_dolci_A5.pdf')
    pdf(allergeni(TENNIS) + allergeni(CLUB), CSS_A, 'Carta_allergeni.pdf')

