import json,html
from weasyprint import HTML
from pypdf import PdfReader,PdfWriter
import os; O=os.environ.get('MENU_OUT','./')
import os; S=os.environ.get('MENU_DATI', '~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/')  # json di lavoro del cliente (esempio Luna Blu)
MX=json.load(open(S+'matrici.json'))
C='file://'+O+'carta/h-'
IT={'STAR':'STELLE','PLOWHORSE':'CLIENTE FELICE','PUZZLE':'SFIDE','DOG':'STOP'}
COL={'STAR':'#2E7D4F','PLOWHORSE':'#3B4E9A','PUZZLE':'#C08A2B','DOG':'#B23A3A'}
def e(x): return f'{x:,.2f}'.replace(',','X').replace('.',',').replace('X','.').rstrip('0').rstrip(',')

def matrice(cat,titolo,W=1300,H=640,fs=13,sq=True):
    c=MX[cat]; rows=[r for r in c['rows'] if not r['n'].startswith('[fuori')]
    popT,mgT=c['popT'],c['mgT']
    qs=[r['q'] for r in rows]; ms=[r['mg'] for r in rows]
    qmax=max(qs)*1.4; mmin=min(ms)-1; mmax=max(ms)+1.2
    L,T,R,B=80,20,W-30,H-50
    X=lambda v:L+(v-mmin)/(mmax-mmin)*(R-L)
    Y=(lambda v:B-(v/qmax)**.5*(B-T)) if sq else (lambda v:B-(v/qmax)*(B-T))
    s=[f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" font-family="Montserrat">']
    q=[(L,T,X(mgT),Y(popT),'#E3E6F2','PLOWHORSE','tanti ordini, margine basso: alza il margine'),
       (X(mgT),T,R,Y(popT),'#E2EFE4','STAR','tanti ordini, margine alto: proteggili'),
       (L,Y(popT),X(mgT),B,'#F4E2E2','DOG','pochi ordini, margine basso: toglili'),
       (X(mgT),Y(popT),R,B,'#F3EAD8','PUZZLE','pochi ordini, margine alto: valorizzali')]
    for x0,y0,x1,y1,f,n,sub in q:
        s.append(f'<rect x="{x0}" y="{y0}" width="{x1-x0}" height="{y1-y0}" fill="{f}"/>')
        lft=x0==L; ax=x0+10 if lft else x1-10-len(IT[n])*16.5; sx=x0+10 if lft else x1-10-len(sub)*6.9
        top=y0==T
        s.append(f'<text x="{ax}" y="{y0+30 if top else y1-28}" font-size="22" font-weight="700" fill="{COL[n]}" opacity=".6">{IT[n]}</text>')
        s.append(f'<text x="{sx}" y="{y0+48 if top else y1-10}" font-size="13" font-style="italic" fill="#666">{sub}</text>')
    s.append(f'<line x1="{X(mgT)}" y1="{T}" x2="{X(mgT)}" y2="{B}" stroke="#555" stroke-dasharray="6 5" stroke-width="1.5"/>')
    s.append(f'<line x1="{L}" y1="{Y(popT)}" x2="{R}" y2="{Y(popT)}" stroke="#555" stroke-dasharray="6 5" stroke-width="1.5"/>')
    s.append(f'<text x="{(L+R)/2}" y="{H-12}" text-anchor="middle" font-size="15" fill="#333">profittabilità: margine per piatto € — media {e(round(mgT,2))}</text>')
    s.append(f'<text transform="translate(24 {(T+B)/2}) rotate(-90)" text-anchor="middle" font-size="15" fill="#333">popolarità: piatti venduti al mese — soglia {e(round(popT,1))}</text>')
    boxes=[]
    for r in sorted(rows,key=lambda r:-r['q']):
        x,y=X(r['mg']),Y(r['q']); est=r['s']=='E'
        s.append(f'<circle cx="{x}" cy="{y}" r="8" fill="{COL[r["cl"]]}" fill-opacity="{0.35 if est else 0.9}" stroke="{COL[r["cl"]]}" stroke-width="1.5"/>')
        n=r['n'].replace('[E] ','')+(' (estate)' if est else '')
        w=len(n)*fs*0.58; lx,ly=x+12,y+5
        if lx+w>R: lx=x-12-w
        for k in range(14):
            cand=ly+(k//2+1)*(fs+2)*(1 if k%2 else -1) if k else ly
            if not any(abs(cand-by)<fs+1 and lx<bx+bw and lx+w>bx for bx,by,bw in boxes): ly=cand;break
        boxes.append((lx,ly,w))
        s.append(f'<text x="{lx}" y="{ly}" font-size="{fs}" fill="#222">{html.escape(n)}</text>')
    s.append('</svg>')
    return f'<section class="s"><div class="kick">LUNA BLU · MATRICE MENU ENGINEERING</div><h2>{titolo}</h2><div class="chart">{"".join(s)}</div><div class="note">Dati: piatti venduti in cassa (Zucchetti) ott-2025 → mag-2026, food cost da ricette RBR. Cerchi chiari = piatti del menu estivo.</div></section>'

def kpi(n,l): return f'<div class="k"><b>{n}</b><span>{l}</span></div>'

slides={}
slides['partenza']=f'''<section class="s dark"><div class="kick g">LUNA BLU · PARMA · DAL 1980</div><h1>Da dove partiamo</h1>
<div class="kpis">{kpi('86','piatti in carta oggi<br>54 tra pizze e panuozzi, 32 di cucina')}{kpi('974','piatti alla carta venduti al mese')}{kpi('22,3%','food cost medio alla carta')}{kpi('7,59 €','margine medio per piatto')}</div>
<p class="big">Circa <b>7.400 € di margine al mese</b> dai piatti alla carta, <b>89.000 € l'anno</b>.<br>Quanto ne resta dipende da <b>quali piatti</b> vendiamo.</p>
<p class="foot">Dati: cassa Zucchetti ottobre 2025 → maggio 2026, solo piatti alla carta (esclusi convenzioni, bar, delivery). Food cost dalle ricette, prezzi IVA esclusa.</p></section>'''

def rep(nome,voci,pz,quota,ric,fc,mg,mm):
    return f'<div class="rep"><h3>{nome}</h3><div class="rr"><span>piatti in carta</span><b>{voci}</b></div><div class="rr"><span>piatti venduti al mese</span><b>{pz} <small>({quota})</small></b></div><div class="rr"><span>incasso netto al mese</span><b>{ric} €</b></div><div class="rr"><span>food cost</span><b>{fc}</b></div><div class="rr hi"><span>margine medio per piatto</span><b>{mg} €</b></div><div class="rr"><span>margine al mese</span><b>{mm} €</b></div></div>'
slides['reparti']=f'''<section class="s"><div class="kick">LUNA BLU · OGGI</div><h2>Margine per reparto: cucina e pizzeria</h2>
<div class="reps">{rep('Cucina','32','356','37%','4.480','17,1%','10,43','3.720')}{rep('Pizzeria','54','618','63%','5.030','26,9%','5,95','3.680')}</div>
<p class="big" style="margin-top:22pt">La pizzeria vende <b>quasi 2 piatti su 3</b>, ma ogni pizza lascia <b>5,95 €</b> contro i <b>10,43 €</b> di un piatto di cucina.<br>Con 54 voci, la pizzeria porta lo stesso margine della cucina che ne ha 32.</p></section>'''

slides['categorie']=f'''<section class="s"><div class="kick">LUNA BLU · OGGI</div><h2>Margine per categoria</h2>
{{TAB}}<p class="foot2">Margine = prezzo IVA esclusa meno food cost. Media pesata sui pezzi venduti.</p></section>'''
def tab(rows,head):
    return '<table><tr>'+''.join(f'<th>{h}</th>' for h in head)+'</tr>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</table>'
slides['limita']=f'''<section class="s"><div class="kick">LUNA BLU · STEP 1</div><h2>Da 87 a 52 voci: −40%</h2>
<div class="two"><div>{tab([['Antipasti','9','7'],['Primi','8','10*'],['Secondi','7','7'],['Insalate e contorni','8','7'],['Pizze','41','21'],['Panuozzi','14','0'],['<b>Totale</b>','<b>87</b>','<b>52</b>']],['Categoria','Oggi','Nuova carta'])}
<p class="small">* 3 primi d'autore + 7 paste: entrano i 2 primi estivi più venduti (linguine allo scoglio e paccheri col polpo).</p></div>
<div><p>Ogni categoria ha <b>al massimo 7 piatti</b> (il "magico numero 7").</p><p>Le pizze passano da 41 a 21, divise in <b>4 famiglie</b> facili da leggere:<br>d'autore (3) · speciali (6) · tradizionali (6) · classiche (6).</p><p>La <b>Margherita esce dalla carta</b> ma resta in cassa a 8: chi la vuole la chiede comunque.</p><p>I <b>panuozzi escono</b>: margine sotto i 6 €, rallentano il forno.</p><p>Meno voci = cucina più veloce, magazzino più piccolo, meno sprechi.</p></div></div></section>'''

slides['decisioni']='''<section class="s"><div class="kick">LUNA BLU · COSA ABBIAMO FATTO IN OGNI QUADRANTE</div><h2>Fai splendere ciò che brilla, elimina ciò che spegne</h2>
<div class="quad">
<div class="q star"><h3>★ STAR · proteggili</h3><p>Misto mare dello chef · Delizia di mare · Spaghettoni alle vongole · Risotto ai frutti di mare · Tris di tortelli · Grigliata di pesce · Tagliata · Capricciosa · Crudo e stracciatella · Pescatora · Crudo di Parma</p><p class="a">→ posizioni migliori, foto, riquadri. Prezzo +1/2 € solo dove regge.</p></div>
<div class="q plow"><h3>☺ PLOWHORSE · rialzali</h3><p>Margherita 7 → 8 (fuori carta) · Lasagne 10 → 12 · Frittura 18 → 20 · Tagliatelle ai porcini 15 → 18 · Diavola 8,5 → 9,5 · Frittino 8 → 9 · Patatine 6 → 6,5</p><p class="a">→ li vendiamo già tanto: piccoli aumenti, grande effetto.</p></div>
<div class="q puz"><h3>? PUZZLE · spingili</h3><p>Amalfi (14 → 16) e Santa Croce (ex Mondiale, 13 → 15) nelle pizze d'autore · Pistacchina · Filetto 25 → 28 e Spigola nei "grandi secondi" · Insalate in riga da 3</p><p class="a">→ box blu in cima alla pagina, nome nuovo, storia, foto.</p></div>
<div class="q dog"><h3>⦸ DOG · toglili</h3><p>14 panuozzi · Funghi · Caprese · Marinara · Wurstel · Calzoni · Estiva · Del carrozziere · Gorgo calabrese · Impepata di cozze · Bruschetta · Verdure al vapore · Spiedino di pesce · Cotoletta</p><p class="a">→ fuori dalla carta. Meno ingredienti in magazzino.</p></div>
</div></section>'''

slides['posto']=f'''<section class="s"><div class="kick">LUNA BLU · STEP 2</div><h2>Formato libro A4: ogni pagina ha il suo sweet spot</h2>
<div class="imgs3"><img src="{C}4.png"><img src="{C}5.png"><img src="{C}7.png"></div>
<ul class="side"><li>In <b>cima a ogni pagina</b> il box dei piatti a più alto margine: primi d'autore, grandi secondi, pizze d'autore.</li>
<li>In ogni gruppo il piatto n.1 per margine sta <b>in seconda posizione</b>: il primo lo leggono tutti, il secondo lo ricordano.</li>
<li>La Capricciosa (la più venduta) con l'etichetta <b>"la più amata dai nostri clienti"</b>.</li>
<li>Le classiche, che vendono da sole, <b>in fondo</b> e senza evidenza.</li></ul></section>'''

slides['conti']='''<section class="s"><div class="kick">LUNA BLU · STEP 3</div><h2>Prezzi: piccoli ritocchi, a parità di piatti venduti</h2>
<div class="two"><div>'''+tab([['Antipasti','850'],["Primi d'autore + pasta",'2.110'],['Secondi e grandi secondi','1.480'],['Insalate e contorni','490'],['Pizze (21 in carta)','3.530'],['Margherita 7 → 8 (fuori carta)','1.020'],['<b>Totale</b>','<b>≈ 9.500 €/anno</b>']],['Sezione','margine in più €/anno'])+'''<p class="small">Calcolo prudente: stessi pezzi venduti di oggi, IVA esclusa. Non conta l'effetto dello spostamento delle vendite verso i piatti che margina di più.</p></div>
<div><p><b>Prezzi senza simbolo €</b>, scritti piccoli <b>subito dopo la descrizione</b>: «…con burro e Parmigiano | 16».</p><p><b>Decimali corti</b>: 9,5 · 10,5 · 11,5. Mai ,99.</p><p>Niente colonna dei prezzi a destra: il cliente sceglie il piatto, non il prezzo.</p><p>Experience a <b>27 € a persona</b> (barrato 32): antipasto da dividere, una portata e un dolce.</p></div></div></section>'''

slides['estetica']=f'''<section class="s"><div class="kick">LUNA BLU · STEP 4</div><h2>Un'estetica che parla di Luna Blu</h2>
<div class="imgs3"><img src="{C}1.png"><img src="{C}2.png"><img src="{C}6.png"></div>
<ul class="side"><li><b>Blu notte</b>: il colore del nome, elegante e riconoscibile.</li><li>Font <b>Lora</b>, graziato e leggibile anche con poca luce.</li>
<li><b>Una o due foto per pagina</b>, solo sui piatti da spingere.</li><li><b>Riquadri e asticelle</b> solo sui piatti scelti, tanto spazio bianco attorno.</li>
<li>Abbinamento <b>vino e birra</b> accanto a ogni pizza: fa crescere lo scontrino.</li></ul></section>'''

slides['emoziona']='''<section class="s"><div class="kick">LUNA BLU · STEP 5</div><h2>Nomi e descrizioni che raccontano la vostra storia</h2>
'''+tab([['Mondiale','<b>Santa Croce</b> — «porta il nome della piazza dove nel 1970 Giovanni aprì il primo locale»'],
['Pizza Amalfi','«…il profumo della Costiera Amalfitana, da dove è partita la famiglia Buonocore»'],
['Tris di tortelli','«Tortelli fatti in casa da nonna Maria, d\'erbetta, di patate e di zucca…»'],
['Tagliatelle ai porcini','«Tagliatelle all\'uovo fatte in casa da nonna Maria… il primo dell\'autunno»'],
['Affettati, giardiniera, torta fritta','<b>Tagliere Luna Blu</b> — coppa piacentina, salame di Felino, crudo di Parma 24 mesi'],
['Pomodoro, mozzarella','«Pomodoro del nostro territorio, fior di latte 100% italiano»'],
['Insalatona greca','<b>Insalata greca</b> — nella categoria Insalate, non più «insalatona»']],['Prima','Nella nuova carta'])+'''
<p class="small">Asterisco su tutti i piatti con pesce o frutti di mare congelati: l'onestà è tutto.</p></section>'''

slides['risultato']='''<section class="s dark"><div class="kick g">LUNA BLU · IL RISULTATO</div><h1>Cosa cambia da domani</h1>
<div class="kpis">'''+kpi('−40%','voci in carta (87 → 52)')+kpi('≈ 9.500 €','di margine in più all\'anno, solo dai prezzi')+kpi('max 7','piatti per categoria')+kpi('21,6%','food cost sotto controllo')+'''</div>
<h3 class="g">Prossimi passi</h3><ol class="big2"><li>Ok sulla carta e stampa del libro A4</li><li>Aggiornare prezzi e tasti in cassa Zucchetti (Margherita 8)</li><li>Formare la sala: quali piatti consigliare e perché</li><li>Dopo 60 giorni: nuova matrice con le vendite reali e ritocchi</li></ol></section>'''

slides['categorie']=slides['categorie'].replace('{TAB}',tab([['Antipasti','9','82','21,4%','10,67','870'],['Primi','8','111','13,3%','11,87','1.320'],['Secondi','7','72','21,6%','14,18','1.020'],['Contorni e insalatone','8','92','8,6%','5,56','510'],['Pizze','40','554','26,2%','5,96','3.300'],['Panuozzi','14','64','32,0%','5,90','380'],['<b>Totale</b>','<b>86</b>','<b>974</b>','<b>22,3%</b>','<b>7,59</b>','<b>7.400</b>']],['Categoria','Piatti in carta','Venduti al mese','Food cost','Margine medio €','Margine al mese €']))

def col(t,righe,tot,mese,cop,cls=''):
    r=''.join(f'<div class="rr"><span>{a}</span><b>+{b} €</b></div>' for a,b in righe)
    return f'<div class="rep {cls}"><h3>{t}</h3>{r}<div class="big3"><div><b>+{tot} €</b><span>all\'anno</span></div><div><b>+{mese} €</b><span>al mese</span></div><div><b>+{cop} €</b><span>a coperto</span></div></div></div>'
slides['potenziale']='''<section class="s"><div class="kick">LUNA BLU · IL POTENZIALE DEL NUOVO MENU</div><h2>Obiettivo: +20.000 / 25.000 € di margine all'anno</h2>
<div class="leve">
<div class="lv"><span class="n">1</span><div><h3>Cambio mix di vendita</h3><p>Cucina e pizzeria da 37/63 a <b>50/50</b>: un piatto di cucina lascia 10,43 €, una pizza 5,95 €</p></div><b>+7.000 €</b></div>
<div class="lv"><span class="n">2</span><div><h3>Menu ingegnerizzato</h3><p>2 ordini su 10 si spostano da clienti felici e stop verso <b>stelle e sfide</b></p></div><b>+3.900 €</b></div>
<div class="lv"><span class="n">3</span><div><h3>Aumento leggero dei prezzi</h3><p>Prezzi riallineati, a parità di piatti venduti</p></div><b>+9.500 €</b></div>
</div>
<div class="big3 tot"><div><b>+20 / 25.000 €</b><span>all'anno</span></div><div><b>+1.700 / 2.100 €</b><span>al mese</span></div><div><b>+3,30 €</b><span>a coperto</span></div></div>
<p class="foot2" style="margin-top:22pt;font-size:15pt">Calcolato sui piatti battuti in cassa (+20.400 €). Con i coperti che oggi non vengono battuti si arriva verso i 25.000 €.<br>Margine = prezzo IVA esclusa meno food cost, solo piatti alla carta. Coperti in cassa: circa 520 al mese (gen-set 2026). Non conteggiati: meno sprechi e magazzino, vino e birra abbinati.</p></section>'''
slides['m_anti']=matrice('Antipasti','Antipasti')
slides['m_primi']=matrice('Primi','Primi')
slides['m_sec']=matrice('Secondi','Secondi')
slides['m_pizze']=matrice('Pizze','Pizze',H=680,fs=11,sq=True)
slides['m_cont']=matrice('Contorni e insalatone','Contorni e insalatone')

CSS='''@page{size:1583pt 891pt;margin:0}
body{margin:0;font-family:Montserrat;color:#111}
.s{width:1583pt;height:891pt;box-sizing:border-box;padding:46pt 80pt;page-break-after:always;position:relative;overflow:hidden}
.dark{background:#0E1A3F;color:#fff}
.kick{letter-spacing:.45em;font-size:14pt;color:#555;text-align:center}.dark .kick,.g{color:#C9A74A}
h1{font-size:62pt;font-weight:300;text-align:center;margin:18pt 0 30pt}
h2{font-size:38pt;font-weight:600;text-align:center;margin:10pt 0 22pt;letter-spacing:.02em}
h3{font-size:20pt;margin:0 0 8pt}
.kpis{display:flex;gap:24pt;justify-content:center;margin:20pt 0 36pt}
.k{flex:1;border:1.5pt solid #C9A74A;padding:22pt 14pt;text-align:center}.k b{display:block;font-size:46pt;color:#C9A74A;font-weight:600}.k span{font-size:15pt}
.big{font-size:23pt;text-align:center;line-height:1.5}
.big2{font-size:20pt;line-height:1.7;margin-left:300pt}
.chart{text-align:center}.chart svg{width:1360pt;height:auto}
.note{font-size:11pt;color:#777;text-align:center;margin-top:6pt}
.two{display:flex;gap:50pt}.two>div{flex:1;font-size:17pt;line-height:1.5}
table{border-collapse:collapse;width:100%;font-size:16pt}th{background:#111;color:#fff;text-align:left;padding:9pt 12pt;font-weight:500}
td{padding:8pt 12pt;border-bottom:1pt solid #ddd}tr:nth-child(odd) td{background:#f4f4f6}
.foot{position:absolute;bottom:30pt;left:80pt;right:80pt;font-size:12pt;color:#9AA3C0;text-align:center}.foot2{font-size:12pt;color:#777;text-align:center}.reps{display:flex;gap:40pt;margin:0 60pt}.rep{flex:1;border-top:4pt solid #C9A74A;background:#f6f6f8;padding:18pt 26pt}.rep h3{font-size:28pt;margin-bottom:10pt}.rr{display:flex;justify-content:space-between;font-size:18pt;padding:7pt 0;border-bottom:1pt solid #ddd}.rr b{font-weight:600}.rr.hi b{color:#B8902F;font-size:24pt}.pot{margin-top:30pt}.pot .rep{padding:28pt 34pt}.pot h3{font-size:34pt;margin-bottom:18pt}.pot .rr{font-size:21pt;padding:14pt 0;gap:20pt}.pot .rr b{white-space:nowrap}.leve{margin:6pt 80pt 0}.lv{display:flex;align-items:center;gap:26pt;border-bottom:1.5pt solid #ddd;padding:24pt 0}.lv .n{font-size:66pt;color:#C9A74A;font-family:Montserrat;font-weight:300;width:60pt}.lv div{flex:1}.lv h3{font-size:34pt;margin:0}.lv p{font-size:21pt;margin:8pt 0 0;color:#333}.lv>b{font-size:44pt;white-space:nowrap}.tot{margin:40pt 80pt 0}.big3.tot>div{padding:30pt 4pt}.big3.tot b{font-size:44pt;white-space:nowrap}.big3.tot span{font-size:20pt}.pot .big3{margin-top:30pt}.pot .big3>div{padding:26pt 4pt}.pot .big3 b{font-size:38pt;white-space:nowrap}.pot .big3 span{font-size:17pt}.big3{display:flex;gap:10pt;margin-top:16pt}.big3>div{flex:1;background:#111;color:#fff;text-align:center;padding:12pt 4pt}.big3 b{display:block;font-size:30pt;color:#C9A74A;font-weight:600}.big3 span{font-size:13pt}.obj{border-top-color:#2E7D4F}.small{font-size:12pt;color:#666;line-height:1.4}
.quad{display:grid;grid-template-columns:1fr 1fr;gap:18pt}
.q{padding:16pt 20pt;font-size:15pt;line-height:1.45}.q p{margin:4pt 0}.q .a{font-style:italic;color:#333}
.star{background:#E2EFE4}.star h3{color:#2E7D4F}.plow{background:#E3E6F2}.plow h3{color:#3B4E9A}.puz{background:#F3EAD8}.puz h3{color:#A06E16}.dog{background:#F4E2E2}.dog h3{color:#B23A3A}
.imgs3{position:absolute;left:60pt;top:150pt;display:flex;gap:16pt}.imgs3 img{height:540pt;box-shadow:0 0 8pt rgba(0,0,0,.25)}
.side{position:absolute;left:1430pt;width:0}
ul.side{left:auto;right:50pt;top:170pt;width:300pt;font-size:15.5pt;line-height:1.5;padding-left:18pt}ul.side li{margin-bottom:12pt}
'''
order=['partenza','reparti','categorie','m_anti','m_primi','m_sec','m_cont','m_pizze','potenziale']
doc='<html><head><meta charset="utf-8"><style>'+CSS+'</style></head><body>'+''.join(slides[k] for k in order)+'</body></html>'
open(O+'nuove.html','w').write(doc)
HTML(string=doc).write_pdf(O+'nuove.pdf')
N={k:i for i,k in enumerate(order)}
orig=PdfReader('~/Downloads/Presentazione Menu Engineering (1).pdf'); new=PdfReader(O+'nuove.pdf')
print('nuove pagine',len(new.pages))
# sequenza: o=pagina originale (1-based), n=slide nuova
seq=[('o',1),('o',2),('o',3),('n','partenza'),('n','reparti'),('n','categorie'),('o',4),('o',5),('o',6),('o',7),('o',8),('o',9),
 ('n','m_anti'),('n','m_primi'),('n','m_sec'),('n','m_cont'),('n','m_pizze')]+[('o',k) for k in range(13,30)]+[('n','potenziale'),('o',30)]
w=PdfWriter()
for t,v in seq:
    w.add_page(orig.pages[v-1] if t=='o' else new.pages[N[v]])
out='~/Desktop/AI/RBR AI/consegne/2026-10-09/Presentazione_Menu_Engineering_LunaBlu.pdf'
w.write(out); print(out,len(seq))

