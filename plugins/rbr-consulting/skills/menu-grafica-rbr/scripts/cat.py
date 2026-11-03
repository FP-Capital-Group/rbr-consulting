import gspread,json,re
from gspread.utils import rowcol_to_a1 as A
sh=gspread.service_account('shared/credentials/service_account.json').open_by_key('1VzXSs8kIp_j0h-pBORJXSwqghkgwkEtl_G5PVGlEkhA')
R=json.load(open('~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/riep.json'))
FC={r[1]:r[2] for r in R}; UN={r[1]:(r[4] or 0) for r in R}
FC['crostata marmellata']="='Food Cost'!W18"
MENU={ # prezzo menu estivo giu-26 IVA incl.; None = non in menu -> prezzo medio cassa
'Paccheri con polpo in crema di patate':18,'linguine allo scoglio':18,'Orecchiette con vongole e zucchine':20,'Riso gamberi, calamari, pistacchi di Bronte':20,
"Tortelli d'erbetta":12,'Gnocchi di patate alla sorrentina':13,'Trofie culatello e asparagi':16,'Spaghetti al pomodoro fresco, burrata e basilico':15,'spaghetto aglio olio e peperoncino':None,
'Frittura mista con verdure':18,'Spigola alla mediterranea':25,'Grigliata mista di pesce (tutto crudo)':25,'Pesce spada alla griglia':18,'Tagliata con rucola e petali di parmigiano':22,
'costata di manzo ai ferri':25,'Grigliata mista con chips':20,'Roast beef':12,'Spiedini di pesce':None,
'Verdure alla griglia':6,'Insalata mista':6,'Patatine fritte':6,'Insalatona Greca':12,'Insalatona Brasile':15,'Insalatona Italia':12,'Insalatona del nonno':12,'crostata marmellata':None,
'Margherita':7,'Napoli':7.5,'Prosciutto Cotto':9,'Prosciutto e porcini':9,'Caprese':9,'Estiva':10,'Capricciosa stellante':10,'Armonia delle quattro stagioni':9,'Quattro Formaggi':8.5,
'Funghi porcini':8,'Calabrisella':8.5,'Bufalina':8,'Patatosa':9,'Crudo di parma':11,'Marinara':6.5,'Verdure':9.5,'Calzone Napoli':8.5,'Calzone Farcito':10,
'Del Maestro':10,'Spiritosa':10,'Del carrozziere':10,'Crudo e Straccia':12,'Tonno Sapore di Sicilia':8,'Parmigiana':8.5,'Mondiale':13,'Viennese':10,'Chip & Chop':10,'Speck & gorgo':10,
'Amalfi':14,'Gorgo Calabrese':10,'Blue Moon':13,'Pescatora':11,'Calabro-Delizia':11.5,'Parma Gold':13,'Patatosa Special':10.5,'Mediterranea':11,'La carbonara 2.0':11,'wurstel':None,
'DEL CARROZIERE':9.5,'IL NORDICO':11,'DEL MAESTRO':9.5,'HAPPY':9.5,'VEGETARIANO':9.5,'SFIZIOSO':9.5,'SBAGLIATO':9.5,'CLASSICO':10,'DIAVOLETTO':9.5,'DELLO ZIO':9.5,'SEMPLICE':8,'IL LEGGERO':12,'MOZZICOTTO':8,
'Corona di mazzancolle con pomodorini e avvocado':18,'Delizia di mare':18,'Carpaccio di polpo':18,'saute di cozze':15,'Misto mare dello chef':25,'crudo e melone':15,
'tagliere di salume con giardiniera e torta fritta':15,"frittino all'italiana":8,'fantasia di bruschette':8,'Crudo e Parmigiano Reggiano':None}
CASSA={r[1]:r[5] for r in R}
def price(n): return MENU[n] if MENU.get(n) is not None else CASSA.get(n)
cats=lambda c:[r[1] for r in R if r[0]==c]
LAY={'A':dict(price='C',net='D',fc='E',pct='F',marg='G',units='H',mix='I',tot='J',new='B',last='J'),
     'B':dict(price='B',net='C',fc='D',pct='E',marg='F',units='G',mix='H',tot='I',last='I'),
     'F':dict(price='B',net='C',fc='D',pct='E',marg='F',units='H',mix='I',tot='J',blank='G',last='J')}
PER='01/01/2026 - 30/07/2026 (pezzi venduti: cassa Zucchetti) · prezzi: menù estivo giugno 2026 IVA inclusa (* = non in menù, prezzo medio di cassa)'
def fill(tab,lay,title,items,end):
    ws=sh.worksheet(tab); L=LAY[lay]; s,e=6,end
    up=[{'range':'A1','values':[[title]]},{'range':'B3','values':[[PER]]}]
    if lay=='F': up.append({'range':'G5','values':[['']]})
    rows=[]
    cols=[chr(c) for c in range(ord('A'),ord(L['last'])+1)]
    for i in range(s,e+1):
        row={c:'' for c in cols}
        k=i-s
        if k<len(items):
            n=items[k]; p=price(n)
            row['A']=n+('' if MENU.get(n) is not None else ' *')
            row[L['price']]=p if p is not None else ''
            row[L['net']]=f"={L['price']}{i}/1,1"
            row[L['fc']]=FC[n]
            row[L['pct']]=f"={L['fc']}{i}/{L['net']}{i}"
            row[L['marg']]=f"={L['net']}{i}-{L['fc']}{i}"
            row[L['units']]=UN.get(n,0) or 0
            row[L['mix']]=f"={L['units']}{i}/SUM(${L['units']}${s}:${L['units']}${e})"
            row[L['tot']]=f"={L['marg']}{i}*{L['units']}{i}"
        rows.append([row[c] for c in cols])
    up.append({'range':f'A{s}:{L["last"]}{e}','values':rows})
    t=e+1
    tot={c:'' for c in cols}
    tot['A']='TOTALE / margine medio per piatto venduto'
    tot[L['units']]=f"=SUM({L['units']}{s}:{L['units']}{e})"
    tot[L['tot']]=f"=SUM({L['tot']}{s}:{L['tot']}{e})"
    tot[L['mix']]=f"={L['tot']}{t}/{L['units']}{t}"
    up.append({'range':f'A{t}:{L["last"]}{t}','values':[[tot[c] for c in cols]]})
    up.append({'range':f'A{t+1}:{L["last"]}{t+1}','values':[['']*len(cols)]})
    # medie pareto / troncata
    f=ws.get('K1:Z80',value_render_option='FORMULA')
    for ri,r in enumerate(f):
        for ci,x in enumerate(r):
            if isinstance(x,str) and x.startswith('='):
                col=chr(ord('K')+ci); lbl=r[ci-2] if ci>=2 else ''
                isu='ordinato' in str(lbl).lower()
                rng=(L['units'] if isu else L['marg'])+f'{s}:'+(L['units'] if isu else L['marg'])+f'{e}'
                nf=f'=TRIMMEAN({rng};20%)' if 'TRIMMEAN' in x else f'=SUM({rng})/COUNTA(A{s}:A{e})*80%'
                up.append({'range':f'{col}{ri+1}','values':[[nf]]})
    ws.batch_update(up,value_input_option='USER_ENTERED')
    print(tab,title,len(items),'righe',s,e)

