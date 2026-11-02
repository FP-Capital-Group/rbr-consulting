import json,pandas as pd,gspread
from collections import defaultdict
import os; S=os.environ.get('MENU_DATI', '~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/')  # json di lavoro del cliente (esempio Luna Blu)
d=json.load(open(S+'mesi.json')); d.pop('2026-08/09',None)
AL={'TIROLESE':'TONNO SAP SICILI','POLPO CROCCANT':'POLPO e CREM PAT','ZUPPA COZZE':'IMPEPATA COZZE','SAUTE COZZE':'IMPEPATA COZZE','CIP E CHOP':'CHIP E CHOP',
'ROAST BEEF RU PA':'ROASTBEEF INS PA','PICCAN e CROCCA':'PAN. PICC e CROC','CALABRISELLA':'DIAVOLA','PROSCIU e PORCIN':'PROSCIU e FUNGHI','PAN. MOZZICOTTO':'PAN. RUSTICO',
'TROFIE CULAT ASP':'TROFIE ASP CULAT','SPAGH POM FRESCO':'SPAGH POM E BURR','GRIGLI CARN CHIP':'SPIEDI CARN CHIP','PAN. NORDICO':'PAN. NORVEGESE','PAN. LEGGERO':'PAN. LEGGERO',
'COSTAT MANZ GRIG':'FILETT MANZ GRIG','STRAC.  RUCOLA':'STRAC. RUCOLA','BRES RUC CARC UO':'BRESA RUC. PAR.'}
A=lambda n: AL.get(n,n)
# mesi puliti
M=defaultdict(lambda:defaultdict(lambda:[0,0.0])); CAT={}
for m,rows in d.items():
    for c,n,q,v in rows: k=A(n); M[m][k][0]+=q; M[m][k][1]+=v; CAT[k]=c
x=pd.read_excel('data/lunablu/zucchetti/report_2026-09-18/drive_leo/VendutoArticoli.xls',header=None)
s=x[x[1].notna()&x[2].apply(lambda v:isinstance(v,(int,float)))]
xl=defaultdict(lambda:[0,0.0])
for _,r in s.iterrows(): k=A(str(r[3]).strip()); xl[k][0]+=int(r[2]); xl[k][1]+=float(r[4]); CAT.setdefault(k,r[1])
for k,(q,v) in xl.items():
    jq=sum(M[f'2026-0{i}'][k][0] for i in range(1,8)); jv=sum(M[f'2026-0{i}'][k][1] for i in range(1,8))
    if q-jq: M['2026-08/09'][k]=[q-jq,v-jv]
# food cost dal foglio
sh=gspread.service_account('shared/credentials/service_account.json').open_by_key('1VzXSs8kIp_j0h-pBORJXSwqghkgwkEtl_G5PVGlEkhA')
R=json.load(open(S+'riep.json')); KEY={r[1]:r[3] for r in R}
KEY.update({'Trofie culatello e asparagi':'TROFIE ASP CULAT','costata di manzo ai ferri':'COSTATA MANZ FER','Grigliata mista con chips':'SPIEDI CARN CHIP','Roast beef':'ROASTBEEF INS PA',
 'Calabrisella':'DIAVOLA','Prosciutto e porcini':'PROSCIU e FUNGHI','Funghi porcini':'FUNGHI PORCINI','Tonno Sapore di Sicilia':'TONNO SAP SICILI','Chip & Chop':'CHIP E CHOP',
 'Calabro-Delizia':'CALABRO-DELIZIA','IL LEGGERO':'PAN. LEGGERO','MOZZICOTTO':'PAN. RUSTICO','Corona di mazzancolle con pomodorini e avvocado':'MAZZANC AVO POMO','saute di cozze':'IMPEPATA COZZE',
 'Spaghetti al pomodoro fresco, burrata e basilico':'SPAGH POM E BURR','DEL CARROZIERE':'PAN. CARROZIERE','IL NORDICO':'PAN. NORVEGESE','Mondiale':'MONDIALE'})
FC={}
for t,col in [('Primi','D'),('Pizze e calzoni','D'),('Panuozzi','D'),('Secondi','D'),('Antipasti','D'),('Contorni, insalatone e dolci','D')]:
    ws=sh.worksheet(t); a=ws.col_values(1); f=ws.col_values(4,value_render_option='UNFORMATTED_VALUE')
    for i in range(5,len(a)):
        n=a[i].replace(' *','')
        if n in KEY and i<len(f) and isinstance(f[i],(int,float)): FC[A(KEY[n])]=(f[i],'ricetta')
EST={'SCIALAT SCOGLIO':2.5,'SPAG SCOGLIO':2.5,'PACCHERI SCOGLIO':2.5,'SPAG VONGOLE':2.4,'RISO MARE':2.3,'TRIS TORTEL':1.37,'GNOCCO POMODORO':0.36,'TAGLIAT. PORCINI':2.5,'LASAGNA':1.8,
'PACCH LIVORNESE':2.5,'GAMB GUAZZETTO':2.0,'POLPO e CREM PAT':3.6,'FILETT MANZ GRIG':6.3,'PENNE ARRABBIATA':0.4,'PENNE POMODORO':0.35,'PENNE CARBONARA':0.9,'ANOLINI IN BRODO':1.5,
'RISO PARMIGIANA':0.8,'RISO PORCINI':2.0,'COTOLETTA':1.8,'PETTO DI POLLO F':1.0,'PATATE FORNO':0.15,'PATATE SALTO':0.2,'INS. VERDE':0.2,'VERDURE COTTE VA':0.4,'VERDURA SALTO':0.4,
'PATATE LESSE':0.15,'INS. POMODORO':0.3,'CRUDO DI PARMA':1.9,'TORTA FRITTA 5P':0.35,'SPIGOLA FIL FER':5.0,'ORATA FIL FER':4.5,'FUNGHI':1.3,'PIZZA ROSSA':0.3,'PIADA ROSSA':0.3,
'PIADA BIANCA':0.25,'PIADA MACCHIATA':0.5,'ROMANA':1.8,'RUCOLA':1.6,'STRAC. RUCOLA':2.3,'ITALIA':2.5,'LA NORVEGESE':4.3,'PAN. RUSTICO':2.3,'PAN. CONTADINO':2.6,'PAN. PICC e CROC':2.6,'PANUOZZO':2.0}
for k,v in EST.items(): FC.setdefault(k,(v,'stima'))
FOOD={'ANTIPASTI MARE','ANTIPASTI TERRA','PIATTI FREDDI','INSALATONE','PRIMI MARE','PRIMI TERRA','SECONDI MARE','SECONDI TERRA','CONTORNI','PIZZERIA','PANUOZZI'}
json.dump({'M':{m:dict(v) for m,v in M.items()},'CAT':CAT,'FC':FC},open(S+'stagioni.json','w'))

