# Adesivi/cartelli porta con i nuovi orari (call 07/10/2026) — un foglio A5 verticale per sede che cambia orario.
# Stile carte bar Cartabianca (Cormorant Garamond + EB Garamond, marrone #4A2617, rosso #A6192E, logo Cartabianca Cafè).
# Orari = ORARI di build_v3.py (Foglio 006, call 07/10). Chrome headless → PDF unico.
import base64, pathlib, subprocess, time, html
HERE = pathlib.Path(__file__).parent
LOGO = pathlib.Path('~/Desktop/AI/RBR AI/data/cartabianca/carta_menu/bar/img/logo_hd_2400.png')
OUT = pathlib.Path('~/Desktop/AI/RBR AI/consegne/2026-10-08/Cartabianca_Adesivi_nuovi_orari.pdf')
CHROME = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome'
DAL = 'dal 12 ottobre 2026'
G = ['Lunedì', 'Martedì', 'Mercoledì', 'Giovedì', 'Venerdì', 'Sabato', 'Domenica']
# (sede, orari per giorno, giorni con orario nuovo)
SEDI = [
    ('Osmannoro', ['6:30 – 20:00'] * 6 + ['7:30 – 20:00'], {0, 1, 2, 3, 4, 5, 6}),
    ('Ingromarket', ['7:00 – 17:30'] * 5 + ['chiuso', 'chiuso'], {0, 1, 2, 3, 4}),
    ('Novoli', ['6:30 – 19:30'] * 5 + ['7:00 – 20:00', '8:00 – 13:00'], {0, 1, 2, 3, 4}),
    ('Prato', ['6:30 – 20:30'] * 6 + ['7:30 – 20:30'], {6}),
    ('Panciatichi', ['6:30 – 21:30'] * 6 + ['7:00 – 21:30'], {6}),
    ('Soffiano', ['7:00 – 20:30'] * 6 + ['7:30 – 20:30'], {6}),
]
logo = 'data:image/png;base64,' + base64.b64encode(LOGO.read_bytes()).decode()
CSS = '''
@page { size: 148mm 210mm; margin: 0; }
* { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
html, body { margin: 0; background: #fff; }
body { font-family: 'EB Garamond', Garamond, Georgia, serif; color: #4A3A2E; }
.pg { width: 148mm; height: 210mm; position: relative; overflow: hidden; page-break-after: always; background: #fff; }
.cornice { position: absolute; inset: 7mm; border: 0.4mm solid #4A2617; }
.cornice::after { content: ''; position: absolute; inset: 1.6mm; border: 0.2mm solid #E7DCCB; }
.logo { position: absolute; top: 19mm; left: 0; right: 0; text-align: center; }
.logo img { width: 92mm; }
.tit { position: absolute; top: 46mm; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', Georgia, serif;
  font-weight: 500; font-size: 30pt; letter-spacing: .14em; text-transform: uppercase; color: #4A2617; line-height: 1; }
.sede { position: absolute; top: 60mm; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', Georgia, serif;
  font-style: italic; font-size: 17pt; color: #8A5A2B; }
.fil { position: absolute; top: 72mm; left: 50%; width: 22mm; margin-left: -11mm; border-top: 0.5mm solid #A6192E; }
table { position: absolute; top: 80mm; left: 22mm; right: 22mm; width: 104mm; border-collapse: collapse; }
td { font-size: 15.5pt; padding: 2.6mm 0; border-bottom: 0.25mm solid #E7DCCB; }
td.g { font-family: 'Cormorant Garamond', Georgia, serif; font-size: 13pt; letter-spacing: .16em; text-transform: uppercase; color: #4A2617; }
td.o { text-align: right; font-variant-numeric: lining-nums; color: #4A3A2E; }
td.o.c { font-style: italic; color: #8C7A6A; }
tr:last-child td { border-bottom: 0; }
.dal { position: absolute; bottom: 21mm; left: 0; right: 0; text-align: center; font-family: 'Cormorant Garamond', Georgia, serif;
  font-size: 11pt; letter-spacing: .26em; text-transform: uppercase; color: #8A5A2B; font-variant-numeric: lining-nums; }
'''
def pagina(sede, orari, nuovi):
    rows = ''.join(f'<tr><td class="g">{g}</td><td class="o{" c" if o == "chiuso" else ""}">{html.escape(o)}</td></tr>' for g, o in zip(G, orari))
    return f'''<div class="pg"><div class="cornice"></div><div class="logo"><img src="{logo}"></div>
<div class="tit">Orari</div><div class="sede">Cartabianca Cafè {html.escape(sede)}</div><div class="fil"></div>
<table>{rows}</table><div class="dal">Nuovi orari {DAL}</div></div>'''

doc = f'''<!doctype html><html lang="it"><head><meta charset="utf-8"><title>Cartabianca - nuovi orari</title>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,500;0,600;1,500&family=EB+Garamond:ital,wght@0,400;0,600;1,400&display=swap">
<style>{CSS}</style></head><body>{''.join(pagina(*s) for s in SEDI)}</body></html>'''
f = HERE / '_adesivi_orari.html'
f.write_text(doc, encoding='utf-8')
if OUT.exists(): OUT.unlink()
p = subprocess.Popen([CHROME, '--headless', '--disable-gpu', '--user-data-dir=/tmp/cprof_ades', '--no-first-run', '--no-pdf-header-footer',
                      '--virtual-time-budget=5000', f'--print-to-pdf={OUT}', f.as_uri()], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
t = time.time(); last = -1
while time.time() - t < 90:
    if p.poll() is not None and OUT.exists(): break
    if OUT.exists():
        sz = OUT.stat().st_size
        if sz == last and sz > 0: break
        last = sz
    time.sleep(1.5)
if p.poll() is None: p.kill()
print('OK', OUT, OUT.stat().st_size)

