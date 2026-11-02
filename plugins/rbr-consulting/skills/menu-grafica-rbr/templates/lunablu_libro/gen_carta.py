import json,html
import os; S=os.environ.get('MENU_DATI', '~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/')  # json di lavoro del cliente (esempio Luna Blu)
D=json.load(open(S+'stagioni.json')); M,FC=D['M'],D['FC']
MX=json.load(open(S+'matrici.json'))
CL={}
for c in MX.values():
    for r in c['rows']: CL[r['k']]=r['cl']
FC.update({'PISTACCHINA':[3.0,'stima'],'ANOLINI IN BRODO':[1.6,'stima'],'RISO PORCINI':[2.6,'stima'],'PIZ BRONTEvsMAZ':[5.0,'stima'],'PROSCIU e FUNGHI':[1.95,'stima']})
CL.update({'RISO PORCINI':'fuori carta','ANOLINI IN BRODO':'fuori carta','LINGUINE SCOGLIO':'STAR','PACCHERI POLPO':'PUZZLE','SPIEDI CARN CHIP':'DOG → versione estiva'})
W=['2025-10','2025-11','2025-12','2026-01','2026-02','2026-03','2026-04','2026-05']; E=['2026-07','2026-08/09']
def pzm(k,s='W'):
    ms,nm=(W,8) if s=='W' else (E,2.6); return sum(M[m].get(k,[0,0])[0] for m in ms)/nm
def eur(x):
    s=f'{x:,.2f}'.replace(',','X').replace('.',',').replace('X','.')
    if s.endswith(',00'): return s[:-3]
    return s[:-1] if s.endswith('0') else s
VINI={'bianco':'#E4D08A','bolle':'#F2E7C4','rosso':'#7E1B33','rossofr':'#A3324F'}
BIRRE={'chiara':'#E8B93A','bianca':'#F3E3A0','nonfiltrata':'#D39A2E','rossa':'#A8401F','scura':'#4A2A18'}
W_={'falanghina':('bianco','Apicella','Falanghina'),'costab':('bianco','Apicella','Costa d\'Amalfi bianco'),'colle':('bianco','Apicella','Colle Santa Marina'),
'pinot':('bianco','Civa','Pinot grigio'),'passerina':('bianco','Umani Ronchi','Passerina'),'franciacorta':('bolle','Tenuta Ambrosini','Franciacorta brut'),
'malvasia':('bolle','della casa','Malvasia piacentina frizzante'),'gutturnio':('rossofr','Villa Rosa','Gutturnio frizzante'),'otello':('rossofr','Ceci','Otello nero di Lambrusco'),
'montepulciano':('rosso','Terre degli Eremi','Montepulciano d\'Abruzzo'),'costar':('rosso','Apicella','Costa d\'Amalfi rosso'),'scippata':('rosso','Apicella','A\' Scippata riserva'),'caranto':('rosso','Astoria','Caranto Pinot nero')}
B_={'hell':('chiara','Paulaner Hell'),'weiss':('bianca','Weissbier König Ludwig'),'ichnusa':('nonfiltrata','Ichnusa non filtrata'),'rossa':('rossa','Moretti rossa doppio malto'),'sixtus':('scura','Forst Sixtus')}
def vin(w):
    t,prod,n=W_[w]; return f'<span class="vin"><svg width="10" height="15" style="--w:{VINI[t]}"><use href="#calice"/></svg><span><b>{html.escape(n)}</b> {html.escape(prod)}</span></span>'
def abb(w,b):
    out=[]
    if w:
        t,prod,n=W_[w]; out.append(f'<span class="ab"><svg width="9" height="13" style="--w:{VINI[t]}"><use href="#calice"/></svg>{html.escape(n)}</span>')
    if b:
        t,n=B_[b]; out.append(f'<span class="ab"><svg width="11" height="13" style="--w:{BIRRE[t]}"><use href="#boccale"/></svg>{html.escape(n)}</span>')
    return '<span class="abb">'+'<span class="dot">·</span>'.join(out)+'</span>'
TOT={}
def piatto(sez,n,desc,k,p0,p1,w=None,b=None,cls='',s='W',per2=False,pizza=False,foto=None,rank=None,tag=None):
    q=pzm(k,s) if k else 0
    fc=FC.get(k,[None,''])[0] if k else None; src=FC.get(k,[None,''])[1] if k else ''
    mg1=p1/1.1-fc if fc is not None else None; mg0=p0/1.1-fc if (fc is not None and p0) else None
    anno=(p1-p0)/1.1*q*12 if p0 else 0
    TOT[sez]=TOT.get(sez,0)+anno
    pz=f'{q:.0f} pz/mese' if q>=1 else (f'{q:.1f} pz/mese' if q>0 else 'nessuna vendita in cassa')
    mk=[]
    if mg1 is not None: mk.append(f'margine {eur(mg0)} → {eur(mg1)} €' if mg0 is not None and p0!=p1 else f'margine {eur(mg1)} €')
    if fc is not None: mk.append(f'FC {fc/(p1/1.1)*100:.0f}%'+(' stimato' if src=='stima' else ''))
    mk.append(pz)
    if k and CL.get(k): mk.append(CL[k])
    if p0 and p0!=p1: mk.append(f'era {eur(p0)} · +{eur(anno)} €/anno')
    if s=='E': mk.append('dal menu estivo')
    if per2: mk.append(f'per 2: margine {eur(mg1*2)} €' if mg1 else '')
    prezzo=f'<span class="prezzo">{eur(p1)}{" pp" if per2 else ""}</span>'
    extra=' · <span class="due">minimo 2</span>' if per2 else ''
    r=f'<span class="rank">{rank}°</span>' if rank else ''
    ast='*' if n.endswith('*') else ''
    n=n.rstrip('*')
    tg=f'<span class="tag">{html.escape(tag)}</span>' if tag else ''
    nome=f'<span class="nome">{r}{html.escape(n)}{abb(w,b) if pizza else ""}{tg}</span>'
    body=f'{nome}<span class="desc">{html.escape(desc).replace("|BR|","<br>")}{ast}{extra}<span class="sep">|</span>{prezzo}</span><span class="mk">{" · ".join(x for x in mk if x)}</span>'
    if foto and isinstance(foto,str):
        return f'<div class="p pfoto {cls}"><div>{body}</div><div class="foto img"><img src="{foto}" alt="{html.escape(n)}"></div></div>'
    if foto:
        return f'<div class="p pfoto {cls}"><div>{body}</div><div class="foto"><svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.2"><rect x="3" y="6" width="18" height="13" rx="2"/><circle cx="12" cy="12.5" r="3.4"/><path d="M8 6l1.4-2h5.2L16 6"/></svg><span>FOTO</span></div></div>'
    return f'<div class="p {cls}">{body}</div>'
def ordina(items):
    # items: list of dict with margin; n.1 in seconda posizione
    for it in items:
        fc=FC.get(it['k'],[None])[0]; it['mg']=it['p1']/1.1-fc if fc is not None else 0
    s=sorted(items,key=lambda x:-x['mg'])
    for i,it in enumerate(s,1): it['rank']=i
    if len(s)>1: s[0],s[1]=s[1],s[0]
    return s
def sezione(sez,items,bordo=True,pizza=False,foto_first=False,fisso=False):
    o=ordina(items); out=[]
    if fisso:
        rk={id(x):x['rank'] for x in o}; o=items
        for x in o: x['rank']=rk[id(x)]
    for i,it in enumerate(o):
        cls=it.pop('cls','')
        if bordo and it['rank']==1 and not cls: cls='bordo'
        it.pop('mg')
        out.append(piatto(sez,cls=cls,pizza=pizza,**it))
    return '\n'.join(out)
def I(n,desc,k,p0,p1,**kw): d=dict(n=n,desc=desc,k=k,p0=p0,p1=p1); d.update(kw); return d

ANTI=[I('Gamberi al guazzetto*','Gamberi in un sugo delicato al prezzemolo, con crostini croccanti da intingere','GAMB GUAZZETTO',18,19,w='costab'),
I('Misto mare dello chef*','La selezione di antipasti di mare, caldi e freddi, che lo chef prepara ogni giorno','MISTO MARE',25,27,w='franciacorta',per2=True,foto='img/lb_misto_mare.webp',cls='pienobox'),
I('Delizia di mare*','Insalata di mare con seppie, polpo, gamberi, cozze, salmone e alici marinate','DELIZIA DI MARE',18,19,w='falanghina'),
I('Tentacolo di polpo in crema di patate*','Tentacolo di polpo cotto piano e poi scottato, su una purea morbida di patate','POLPO e CREM PAT',18,19,w='pinot'),
I('Crudo di Parma e Parmigiano Reggiano','Prosciutto crudo di Parma DOP 24 mesi e scaglie di Parmigiano Reggiano DOP','CRUDO E PAR-REGG',15,16,w='malvasia'),
I('Tagliere Luna Blu','Coppa piacentina, salame di Felino e crudo di Parma 24 mesi, giardiniera e torta fritta','AFFET GIARD TORT',15,16,w='gutturnio',per2=True),
I('Frittino all\'italiana','Mozzarelline, alghette, crocchette di patate, olive all\'ascolana e patatine fritte','FRITTO ITALIANA',8,9,w='franciacorta')]
PREMP=[I('Risotto ai frutti di mare*','Riso Carnaroli mantecato con i frutti di mare aperti in padella, profumato alla scorza di limone e senza pomodoro, per sentire solo il sapore del mare','RISO MARE',18,21,w='costab',cls='in'),
I('Spaghettoni alle vongole veraci','Spaghettoni trafilati al bronzo e vongole veraci aperte in padella con aglio, olio extravergine e prezzemolo, mantecati nel loro sugo','SPAG VONGOLE',20,22,w='falanghina',cls='in',tag='il consiglio dello chef'),
I('Tagliatelle ai funghi porcini','Tagliatelle all\'uovo fatte in casa da nonna Maria, saltate con funghi porcini, aglio e prezzemolo: il primo dell\'autunno','TAGLIAT. PORCINI',15,18,w='caranto',cls='in')]
PASTA=[I('Paccheri con polpo in crema di patate*','Paccheri di semola con dadolata di polpo cotto lentamente, su una crema vellutata di patate','PACCHERI POLPO',18,19,w='pinot',s='E'),
I('Linguine allo scoglio*','Linguine saltate in padella con scampi, cozze, vongole, seppie e gamberi,|BR|che lasciano tutto il loro sapore nel sugo','LINGUINE SCOGLIO',18,19,w='costab',s='E',cls='nob'),
I('Risotto ai funghi porcini','Riso Carnaroli mantecato con funghi porcini e Parmigiano Reggiano','RISO PORCINI',None,18,w='montepulciano'),
I('Tris di tortelli','Tortelli fatti in casa da nonna Maria, d\'erbetta, di patate e di zucca, con burro e Parmigiano','TRIS TORTEL',15,16,w='malvasia'),
I('Gnocchi di patate al pomodoro','Gnocchi di patate fatti in casa da nonna Maria, con pomodoro e basilico','GNOCCO POMODORO',12,13,w='gutturnio'),
I('Lasagne al forno','Sfoglia all\'uovo, ragù di carne, mozzarella e besciamella','LASAGNA',10,12,w='gutturnio'),
I('Anolini in brodo','Gli anolini della tradizione parmigiana, serviti nel brodo di carne','ANOLINI IN BRODO',9,11,w='otello')]
PREMS=[I('Filetto di manzo alla griglia','Filetto di manzo tenero e magro, cotto alla griglia come lo preferite, con rosmarino e un filo di olio extravergine a crudo','FILETT MANZ GRIG',25,28,w='scippata',cls='in'),
I('Grigliata mista di pesce*','Il pesce migliore della giornata cotto alla griglia: gamberoni, scampi, pesce spada e filetto di spigola, con olio extravergine e limone','GRIG. MISTA PESC',25,28,w='colle',cls='in'),
I('Spigola alla mediterranea','Filetto di spigola cotto in padella con olive, capperi, pomodorini e patate, che si insaporiscono nel sugo del pesce','SPIGOLA MEDITERR',25,26,w='falanghina',cls='in')]
SEC=[I('Grigliata di carne con chips','Salsiccia, petto di pollo, braciola di maiale e manzo cotti alla griglia,|BR|serviti con patatine fritte al momento','SPIEDI CARN CHIP',18,20,w='montepulciano'),
I('Tagliata con rucola e Parmigiano','Manzo cotto alla griglia e tagliato a fette, servito su rucola fresca con petali di Parmigiano Reggiano e olio extravergine','TAGLIA RUC PARMI',22,24,w='costar',foto='img/lb_tagliata.webp',cls='asta'),
I('Pesce spada alla griglia*','Trancio di pesce spada cotto alla griglia, servito su un letto di insalatina|BR|con olio extravergine e limone','SPADA GRIGLIA',18,19,w='passerina'),
I('Frittura mista con verdure*','Calamari, gamberi e alici fritti al momento, leggeri e dorati, con verdurine in pastella croccante','FRITTO PESC VERD',18,20,w='franciacorta')]
CONT=[('Patatine fritte','Fritte al momento','PATATE FRITTE',6,6.5),('Verdure alla griglia','Melanzane, zucchine e peperoni','VERDURA GRIGLIA',6,6.5),
('Insalata fresca mista','Verdure fresche di stagione','INS. FRESCA MIX',6,6.5),('Patate al forno','Al rosmarino, croccanti fuori','PATATE FORNO',None,6.5)]
INSAL=[I('Insalata greca','Insalata, cetrioli, datterini, cipolla di Tropea, feta e olive nere','INS. GRECA',12,13),
I('Insalata Brasile','Insalata, datterini, rucola, gamberetti e scaglie di Parmigiano','INS. BRASILE',15,16),
I('Insalata Italia','Insalata, pomodori, carote, tonno, mozzarella di bufala DOP e mais','INS. ITALIA',12,13)]
PAUT=[I('Amalfi*','Fior di latte 100% italiano, gamberetti, rucola e scorza di limone:|BR|il profumo della Costiera Amalfitana, da dove è partita la famiglia Buonocore','AMALFI',14,16,w='falanghina',b='weiss',cls='in'),
I('La Pistacchina','Pomodoro del nostro territorio, fior di latte 100% italiano,|BR|mortadella, stracciatella cremosa e granella di pistacchio','PISTACCHINA',12,14,w='malvasia',b='hell',cls='in'),
I('Santa Croce','Pizza bianca con pomodorini, mozzarella di bufala campana DOP, prosciutto crudo di Parma, funghi porcini e scaglie di Parmigiano Reggiano. Porta il nome della piazza dove nel 1970 Giovanni aprì il primo locale','MONDIALE',13,15,w='costar',b='ichnusa',cls='in')]
PSPE=[I('Spiritosa','Pomodoro del nostro territorio, fior di latte 100% italiano, cipolla caramellata e pancetta','SPIRITOSA',10,11,w='otello',b='rossa'),
I('Crudo e stracciatella','Pomodoro del nostro territorio e fior di latte 100% italiano;|BR|a fine cottura prosciutto crudo di Parma 24 mesi e stracciatella cremosa','CRUDO E STRACCIA',12,13,w='malvasia',b='ichnusa',cls='asta',foto='img/lb_crudo_stracciatella.webp'),
I('Del maestro','Bianca con fior di latte 100% italiano, friarielli, salsiccia e scamorza affumicata','DEL MAESTRO',10,11,w='gutturnio',b='sixtus'),
I('Pescatora*','Pomodoro del nostro territorio, fior di latte 100% italiano, frutti di mare e origano','PESCATORA',11,12,w='falanghina',b='weiss',cls='nob'),
I('Patatosa special','Fior di latte 100% italiano, patate al forno, salsiccia e provola affumicata','PATATOSA SPECIAL',10.5,11.5,w='gutturnio',b='sixtus',s='E',cls='nob'),
I('Speck & gorgo','Pomodoro del nostro territorio, fior di latte 100% italiano, gorgonzola e speck all\'uscita','SPECK e GORGO',10,11,w='otello',b='rossa')]
PTRA=[I('Verdure','Pomodoro del nostro territorio, fior di latte 100% italiano, peperoni, melanzane e zucchine','VERDURE',9.5,10.5,w='passerina',b='weiss'),
I('Capricciosa','Pomodoro del nostro territorio, fior di latte 100% italiano, cotto, funghi, carciofi, salsiccia e olive','CAPRICCIOSA',10,11,w='gutturnio',b='ichnusa',cls='asta',tag='la più amata dai nostri clienti'),
I('Crudo di Parma','Pomodoro del nostro territorio, fior di latte 100% italiano e prosciutto crudo di Parma 24 mesi','CRUDO DI PARMA',11,12,w='malvasia',b='hell'),
I('Viennese','Pomodoro del nostro territorio, fior di latte 100% italiano, würstel e patatine fritte','VIENNESE',10,11,w='gutturnio',b='hell',cls='nob'),
I('Tonno e cipolla','Pomodoro del nostro territorio, fior di latte 100% italiano, tonno e cipolla','TONNO SAP SICILI',8,9,w='falanghina',b='hell'),
I('Parmigiana','Pomodoro del nostro territorio, fior di latte 100% italiano, salsiccia e origano','PARMIGIANA',8.5,9.5,w='otello',b='rossa')]
PCLA=[I('Quattro formaggi','Fior di latte 100% italiano, gorgonzola dolce, stracchino cremoso e provola affumicata','4 FORMAGGI',8.5,9.5,w='malvasia',b='weiss'),
I('Prosciutto cotto','Pomodoro del nostro territorio, fior di latte 100% italiano e prosciutto cotto','PROSCIUTT COTTO',9,10,w='gutturnio',b='hell'),
I('Diavola','Pomodoro del nostro territorio, fior di latte 100% italiano, salame piccante calabrese e origano','DIAVOLA',8.5,9.5,w='otello',b='rossa'),
I('Prosciutto e funghi','Pomodoro del nostro territorio, fior di latte 100% italiano, funghi champignon freschi e prosciutto cotto','PROSCIU e FUNGHI',9,10,w='gutturnio',b='hell'),
I('Napoli','Pomodoro del nostro territorio, fior di latte 100% italiano, filetti di acciughe e origano','NAPOLI',7.5,8.5,w='falanghina',b='ichnusa'),
I('Bufalina','Pomodoro del nostro territorio e mozzarella di bufala campana DOP spezzata a mano','BUFALINA',8,9,w='falanghina',b='weiss')]

def premium(sez,items,photo_label,stile='pieno',img=None):
    o=ordina(items); rows=[]
    for it in o:
        it.pop('cls',None); it.pop('mg')
        rows.append(piatto(sez,cls='pin',**it) if sez!='pizze_autore' else piatto(sez,cls='pin',pizza=True,**it))
    foto=f'<div class="foto grande img"><img src="{img}" alt="{photo_label}"></div>' if img else f'<div class="foto grande"><span>FOTO · {photo_label}</span></div>'
    return f'<div class="premio {stile}"><div class="premio-l">{"".join(rows)}</div>{foto}</div>'

anti=sezione('antipasti',[dict(x) for x in ANTI])
pp=premium('primi_autore',[dict(x) for x in PREMP],'spaghettoni alle vongole','bordo','img/lb_spaghettoni_vongole.webp')
pasta=sezione('pasta',[dict(x) for x in PASTA])
ps=premium('grandi_secondi',[dict(x) for x in PREMS],'grigliata di pesce','pieno','img/lb_grigliata_pesce.webp')
sec=sezione('secondi',[dict(x) for x in SEC])
ins=sezione('insalatone',[dict(x) for x in INSAL],bordo=False)
cont=''.join(f'<div class="c"><span class="nome">{n}</span><span class="desc">{d}<span class="sep">|</span><span class="prezzo">{eur(p1)}</span></span><span class="mk">{pzm(k):.0f} pz/mese · margine {eur(p1/1.1-FC[k][0])} €{(" · era "+eur(p0)) if p0 else " · oggi fuori carta"}</span></div>' for n,d,k,p0,p1 in CONT)
for n,d,k,p0,p1 in CONT:
    if p0: TOT['contorni']=TOT.get('contorni',0)+(p1-p0)/1.1*pzm(k)*12
paut=premium('pizze_autore',[dict(x) for x in PAUT],'Santa Croce','pieno','img/lb_santa_croce.webp')
pspe=sezione('speciali',[dict(x) for x in PSPE],pizza=True,fisso=True)
ptra=sezione('tradizionali',[dict(x) for x in PTRA],pizza=True)
pcla=sezione('classiche',[dict(x) for x in PCLA],bordo=False,pizza=True)
json.dump(TOT,open(S+'tot.json','w'))
T=lambda k:eur(round(TOT.get(k,0),-1))
pizze_tot=sum(TOT.get(k,0) for k in ['pizze_autore','speciali','tradizionali','classiche'])
tpl=open(os.path.join(os.path.dirname(os.path.abspath(__file__)),'tpl_carta.html')).read()
for k,v in dict(ANTI=anti,PREMP=pp,PASTA=pasta,PREMS=ps,SEC=sec,CONT=cont,INS=ins,PAUT=paut,PSPE=pspe,PTRA=ptra,PCLA=pcla).items(): tpl=tpl.replace('{{'+k+'}}',v)
for k in ['antipasti','primi_autore','pasta','grandi_secondi','secondi','contorni','insalatone','pizze_autore','speciali','tradizionali','classiche']: tpl=tpl.replace('{{T_'+k+'}}',T(k))
tpl=tpl.replace('{{T_pizze}}',eur(round(pizze_tot,-1))).replace('{{T_tutto}}',eur(round(sum(TOT.values()),-2)))
open(os.environ.get('MENU_OUT','carta.html'),'w').write(tpl)
print({k:round(v) for k,v in TOT.items()}, round(sum(TOT.values())))

