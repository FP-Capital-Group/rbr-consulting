import html,sys
import os; S=os.environ.get('MENU_DATI', '~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/')  # json di lavoro del cliente (esempio Luna Blu)
OUT=os.environ.get('MENU_OUT_DIR','./')
src=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'..','lunablu_libro','gen_carta.py')).read().split('def premium')[0]
g={}; exec(src,g)
eur,ordina,I,FC=g['eur'],g['ordina'],g['I'],g['FC']
FC.update({'PAN. DEL MAESTRO':[2.61,'r'],'PAN. HAPPY':[2.62,'r'],'PAN. SBAGLIATO':[3.20,'r'],'PAN. CLASSICO':[3.62,'r']})
PAN=[I('Del maestro','Salsiccia, friarielli e provola affumicata','PAN. DEL MAESTRO',9.5,11),
I('Classico','Prosciutto crudo di Parma 24 mesi, mozzarella di bufala campana DOP e pomodorini','PAN. CLASSICO',10,12),
I('Happy','Salsiccia, patatine fritte e provola affumicata','PAN. HAPPY',9.5,11),
I('Sbagliato','Salsiccia, melanzane a funghetto e provola affumicata','PAN. SBAGLIATO',9.5,11)]
def p(it,cls=''):
    n=it['n']; ast='*' if n.endswith('*') else ''; n=n.rstrip('*')
    d=html.escape(it['desc']).replace('|BR|',' ')
    due=' · minimo 2' if it.get('per2') else ''
    pr=eur(it['p1'])+(' pp' if it.get('per2') else '')
    tag=f'<span class="tag">{html.escape(it["tag"])}</span>' if it.get('tag') else ''
    c=cls or it.get('cls','')
    c=c if c in ('asta','bordo','pin') else ''
    body=f'<div class="nm">{html.escape(n)}{tag}</div><div class="ds">{d}{ast}{due} <span class="pr">{pr}</span></div>'
    if it.get('foto') and isinstance(it['foto'],str) and c!='pin':
        return f'<div class="p {c} pf"><div class="tx">{body}</div><img src="{it["foto"]}" alt=""></div>'
    return f'<div class="p {c}">{body}</div>'
def sez(items,fisso=False,first_bordo=False):
    o=ordina([dict(x) for x in items])
    if fisso: o=[dict(x) for x in items]
    return ''.join(p(it) for it in o)
def premio(items,img,stile):
    o=ordina([dict(x) for x in items])
    return f'<div class="premio {stile}"><img class="big" src="{img}" alt="">{"".join(p(it,"pin") for it in o)}</div>'
ANTI=[dict(x) for x in g['ANTI']]
for x in ANTI:
    if x['k']=='MISTO MARE': x['cls']='bordo'
cont=''.join(f'<div class="c"><b>{n}</b> <span class="ds">{d} <span class="pr">{eur(p1)}</span></span></div>' for n,d,k,p0,p1 in g['CONT'])
V=dict(ANTI=sez(ANTI),INS=sez(g['INSAL']),PREMP=premio(g['PREMP'],'img/lb_spaghettoni_vongole.webp','bordo'),
PASTA=sez(g['PASTA']),PREMS=premio(g['PREMS'],'img/lb_grigliata_pesce.webp','pieno'),SEC=sez(g['SEC']),CONT=cont,
PAUT=premio(g['PAUT'],'img/lb_santa_croce.webp','pieno'),PSPE=sez(g['PSPE'],fisso=True),PTRA=sez(g['PTRA']),PCLA=sez(g['PCLA']),PAN=sez(PAN))
t=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tpl_esterno.html')).read()
for k,v in V.items(): t=t.replace('{{'+k+'}}',v)
open(OUT+'menu_esterno_lunablu_120x70.html','w').write(t)
for it in PAN: print(it['n'], 'margine', round(it['p1']/1.1-FC[it['k']][0],2), 'era', round(it['p0']/1.1-FC[it['k']][0],2))

