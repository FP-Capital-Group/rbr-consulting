import json
import os; S=os.environ.get('MENU_DATI', '~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/')  # json di lavoro del cliente (esempio Luna Blu)
D=json.load(open(S+'stagioni.json')); M,CAT,FC=D['M'],D['CAT'],D['FC']
FC.update({k:(v,'stima') for k,v in {'PISTACCHINA':3.0,'DELICATA':1.6,'ALLEGRA':2.9,'PIZ BRONTEvsMAZ':5.0,'SORPRESA':2.5,'Biancaneve':1.4,'PUCARESE':2.2,'GIALLOBLU':2.2,'VERDURE COTTE VA':0.4}.items() if k not in FC})
W=['2025-10','2025-11','2025-12','2026-01','2026-02','2026-03','2026-04','2026-05']; E=['2026-07','2026-08/09']
def st(k,ms,nm):
    q=sum(M[m].get(k,[0,0])[0] for m in ms); v=sum(M[m].get(k,[0,0])[1] for m in ms)
    return q/nm, (v/q if q>0 else None)
CATS={
'Antipasti':[('Gamberi al guazzetto','GAMB GUAZZETTO',18,'W'),('Delizia di mare','DELIZIA DI MARE',18,'W'),('Tentacolo di polpo in crema di patate','POLPO e CREM PAT',18,'W'),('Impepata di cozze','IMPEPATA COZZE',15,'W'),('Misto mare dello chef (x2)','MISTO MARE',25,'W'),
  ('Crudo di Parma e Parmigiano','CRUDO E PAR-REGG',15,'W'),('Tagliere salumi, giardiniera, torta fritta (x2)','AFFET GIARD TORT',15,'W'),('Frittino all italiana','FRITTO ITALIANA',8,'W'),('Bruschetta fantasiosa','BRUSC FANTASI',8,'W'),
  ('[E] Carpaccio di polpo agli agrumi','CARPAC AGRU+RUCO',18,'E'),('[E] Corona di mazzancolle e avocado','MAZZANC AVO POMO',18,'E'),('[E] Crudo e melone','CRUDO E MELONE',15,'E')],
'Primi':[('Paccheri alla livornese','PACCH LIVORNESE',18,'W'),('Scialatielli allo scoglio','SCIALAT SCOGLIO',18,'W'),('Spaghettoni alle vongole','SPAG VONGOLE',20,'W'),('Risotto al profumo di mare','RISO MARE',18,'W'),
  ('Lasagne al forno','LASAGNA',10,'W'),('Tris di tortelli','TRIS TORTEL',15,'W'),('Gnocchi al pomodoro','GNOCCO POMODORO',12,'W'),('Tagliatelle ai porcini','TAGLIAT. PORCINI',15,'W'),
  ('[E] Linguine allo scoglio','LINGUINE SCOGLIO',18,'E'),('[E] Paccheri polpo e crema di patate','PACCHERI POLPO',18,'E'),('[E] Tortelli d erbetta','TORT. ERBETTA',12,'E'),('[E] Gnocchi alla sorrentina','GNOCCO SORRENTO',13,'E'),
  ('[E] Spaghetti pomodoro fresco e burrata','SPAGH POM E BURR',15,'E'),('[E] Orecchiette vongole e zucchine','ORECCH VONG ZUCC',20,'E'),('[E] Risotto gamberi calamari pistacchio','RIS GAMB CAL PIS',20,'E'),('[E] Trofie culatello e asparagi','TROFIE ASP CULAT',16,'E'),
  ('[fuori carta] Penne all arrabbiata','PENNE ARRABBIATA',None,'W')],
'Secondi':[('Frittura mista con verdure','FRITTO PESC VERD',18,'W'),('Spigola alla mediterranea','SPIGOLA MEDITERR',25,'W'),('Grigliata mista di pesce','GRIG. MISTA PESC',25,'W'),('Pesce spada alla griglia','SPADA GRIGLIA',18,'W'),
  ('Tagliata rucola e parmigiano','TAGLIA RUC PARMI',22,'W'),('Filetto alla griglia','FILETT MANZ GRIG',25,'W'),('Spiedino misto con chips','SPIEDI CARN CHIP',18,'W'),('[fuori carta] Spiedino di pesce','SPIEDINO PESCE',18,'W'),('[fuori carta] Cotoletta','COTOLETTA',None,'W')],
'Contorni e insalatone':[('Verdure alla griglia','VERDURA GRIGLIA',6,'W'),('Insalata fresca mista','INS. FRESCA MIX',6,'W'),('Patatine fritte','PATATE FRITTE',6,'W'),('Verdure al vapore','VERDURE COTTE VA',6,'W'),('[fuori carta] Patate al forno','PATATE FORNO',None,'W'),
  ('Insalatona greca','INS. GRECA',12,'W'),('Insalatona Brasile','INS. BRASILE',15,'W'),('Insalatona Italia','INS. ITALIA',12,'W'),('Insalatona del nonno','INS. DEL NONNO',12,'W')],
'Pizze':[(n,k,p,'W') for n,k,p in [('Margherita','MARGHERITA',7),('Napoli','NAPOLI',7.5),('Diavola','DIAVOLA',8.5),('Gorgo calabrese','GORGO CALABRESE',10),('Bufalina','BUFALINA',8),('Quattro stagioni','4 STAGIONI',9),('Capricciosa','CAPRICCIOSA',10),
  ('Tonno e sapore di Sicilia','TONNO SAP SICILI',8),('Prosciutto e funghi','PROSCIU e FUNGHI',9),('Funghi','FUNGHI',8),('Prosciutto cotto','PROSCIUTT COTTO',9),('Caprese','CAPRESE',9),('Speck & gorgo','SPECK e GORGO',10),('Viennese','VIENNESE',10),('Chip e chop','CHIP E CHOP',10),
  ('Patatosa','PATATOSA',9),('Parmigiana','PARMIGIANA',8.5),('Marinara','MARINARA',6.5),('Quattro formaggi','4 FORMAGGI',8.5),('Verdure','VERDURE',9.5),('Crudo di Parma','CRUDO DI PARMA',11),('Crudo e stracciatella','CRUDO E STRACCIA',12),('Wurstel','WURSTEL',8.5),
  ('Calzone Napoli','CALZONE NAPOLI',8.5),('Calzone farcito','CALZONE FARCITO',10),('Bronte vs Mazara','PIZ BRONTEvsMAZ',18),('Blue Moon','PIZ BLUE MOON',13),('Italia','ITALIA',10),('Mondiale','MONDIALE',13),('Estiva','ESTIVA',10),('Del carrozziere','CARROZIERE',10),
  ('Sorpresa','SORPRESA',10),('Del maestro','DEL MAESTRO',10),('Pescatora','PESCATORA',11),('Spiritosa','SPIRITOSA',10),('La norvegese','LA NORVEGESE',14),('Amalfi','AMALFI',14),('Pistacchina','PISTACCHINA',12),('Delicata','DELICATA',10),('Allegra','ALLEGRA',12)]]
  +[('[E] Patatosa special','PATATOSA SPECIAL',10.5,'E'),('[E] Parma gold','PARMA GOLD',13,'E'),('[E] Calabro-delizia','CALABRO-DELIZIA',11.5,'E'),('[fuori carta] Romana','ROMANA',None,'W'),('[fuori carta] Biancaneve','Biancaneve',None,'W'),('[fuori carta] Piada macchiata','PIADA MACCHIATA',None,'W'),('[fuori carta] Funghi porcini','FUNGHI PORCINI',8,'W')],
'Panuozzi':[(n,k,p,'W') for n,k,p in [('Del carrozziere','PAN. CARROZIERE',9.5),('Il norvegese','PAN. NORVEGESE',11),('Del maestro','PAN. DEL MAESTRO',9.5),('Rustico','PAN. RUSTICO',9.5),('Happy','PAN. HAPPY',9.5),('Vegetariano','PAN. VEGETARIANO',9.5),('Sfizioso','PAN. SFIZIOSO',9.5),
  ('Sbagliato','PAN. SBAGLIATO',9.5),('Classico','PAN. CLASSICO',10),('Contadino','PAN. CONTADINO',9.5),('Diavoletto','PAN. DIAVOLETTO',9.5),('Dello zio','PAN. DELLO ZIO',9.5),('Semplice','PAN. SEMPLICE',8),('Piccante e croccante','PAN. PICC e CROC',9.5)]]}
OUT={}
for c,items in CATS.items():
    rows=[]
    for n,k,p,s in items:
        q,avg=st(k,W,8) if s=='W' else st(k,E,2.6)
        price=p if p else (round(avg*2)/2 if avg else None)
        fc=FC.get(k,(None,''))
        mg=price/1.1-fc[0] if price and fc[0] is not None else None
        rows.append(dict(n=n,k=k,s=s,q=round(q,1),p=price,fc=fc[0],src=fc[1],mg=mg))
    base=[r for r in rows if r['s']=='W' and not r['n'].startswith('[fuori') and r['mg'] is not None]
    Q=sum(r['q'] for r in base); n=len(base)
    popT=Q/n*0.7; mgT=sum(r['q']*r['mg'] for r in base)/Q
    for r in rows:
        if r['mg'] is None: r['cl']='?'; continue
        hi_p=r['q']>=popT; hi_m=r['mg']>=mgT
        r['cl']={(1,1):'STAR',(1,0):'PLOWHORSE',(0,1):'PUZZLE',(0,0):'DOG'}[(hi_p,hi_m)]
    OUT[c]=dict(rows=rows,popT=popT,mgT=mgT)
    print(f'\n### {c}  soglia popolarità {popT:.1f} pz/mese · soglia margine {mgT:.2f} €')
    for r in sorted(rows,key=lambda r:-(r['mg'] or 0)):
        print(f"  {r['cl']:9} {r['n'][:44]:44} pz/m {r['q']:5.1f}  € {r['p']}  FC {r['fc'] if r['fc'] is None else round(r['fc'],2)} {r['src'][:1]}  marg {r['mg'] if r['mg'] is None else round(r['mg'],2)}")
json.dump(OUT,open(S+'matrici.json','w'),ensure_ascii=False)

