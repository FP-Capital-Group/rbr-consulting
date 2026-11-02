import json
import os; S=os.environ.get('MENU_DATI', '~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/')  # json di lavoro del cliente (esempio Luna Blu)
D=json.load(open(S+'stagioni.json')); M,FC=D['M'],D['FC']
FC.update({'ANOLINI IN BRODO':(1.6,'stima'),'RISO PORCINI':(2.6,'stima')})
W=['2025-10','2025-11','2025-12','2026-01','2026-02','2026-03','2026-04','2026-05']; E=['2026-07','2026-08/09']
def pzm(k,s): ms,nm=(W,8) if s=='W' else (E,2.6); return sum(M[m].get(k,[0,0])[0] for m in ms)/nm
# sezione, nome, chiave cassa, stagione dati, prezzo attuale, prezzo nuovo
C=[
('Antipasti','Gamberi al guazzetto con crostini','GAMB GUAZZETTO','W',18,19),
('Antipasti','Misto mare dello chef','MISTO MARE','W',25,27),
('Antipasti','Delizia di mare','DELIZIA DI MARE','W',18,19),
('Antipasti','Tentacolo di polpo in crema di patate','POLPO e CREM PAT','W',18,19),
('Antipasti','Crudo di Parma e Parmigiano Reggiano','CRUDO E PAR-REGG','W',15,16),
('Antipasti','Tagliere di salumi, giardiniera e torta fritta','AFFET GIARD TORT','W',15,16),
('Antipasti','Frittino all\'italiana','FRITTO ITALIANA','W',8,9),
('Primi d\'autore','Spaghettoni alle vongole veraci','SPAG VONGOLE','W',20,22),
('Primi d\'autore','Risotto ai frutti di mare','RISO MARE','W',18,21),
('Primi d\'autore','Tagliatelle all\'uovo ai funghi porcini','TAGLIAT. PORCINI','W',15,18),
('La pasta','Linguine allo scoglio','LINGUINE SCOGLIO','E',18,19),
('La pasta','Paccheri con polpo in crema di patate','PACCHERI POLPO','E',18,19),
('La pasta','Tris di tortelli','TRIS TORTEL','W',15,16),
('La pasta','Risotto ai funghi porcini','RISO PORCINI','W',10,18),
('La pasta','Gnocchi di patate al pomodoro','GNOCCO POMODORO','W',12,13),
('La pasta','Lasagne al forno','LASAGNA','W',10,12),
('La pasta','Anolini in brodo','ANOLINI IN BRODO','W',9,11),
('Grandi secondi','Grigliata mista di pesce','GRIG. MISTA PESC','W',25,28),
('Grandi secondi','Filetto di manzo alla griglia','FILETT MANZ GRIG','W',25,28),
('Grandi secondi','Spigola alla mediterranea','SPIGOLA MEDITERR','W',25,26),
('I secondi','Tagliata con rucola e Parmigiano','TAGLIA RUC PARMI','W',22,24),
('I secondi','Frittura mista con verdure','FRITTO PESC VERD','W',18,20),
('I secondi','Pesce spada alla griglia','SPADA GRIGLIA','W',18,19),
('I secondi','Grigliata di carne con chips','SPIEDI CARN CHIP','W',18,20),
('Contorni','Patatine fritte','PATATE FRITTE','W',6,6.5),
('Contorni','Verdure alla griglia','VERDURA GRIGLIA','W',6,6.5),
('Contorni','Insalata fresca mista','INS. FRESCA MIX','W',6,6.5),
('Contorni','Patate al forno','PATATE FORNO','W',4,6.5),
('Insalatone','Insalatona Italia','INS. ITALIA','W',12,13),
('Insalatone','Insalatona greca','INS. GRECA','W',12,13),
('Insalatone','Insalatona Brasile','INS. BRASILE','W',15,16),
('Pizze d\'autore','Bronte vs Mazara','PIZ BRONTEvsMAZ','W',18,19),
('Pizze d\'autore','Blue Moon','PIZ BLUE MOON','W',13,14),
('Pizze d\'autore','Mondiale','MONDIALE','W',13,14),
('Le classiche','Margherita','MARGHERITA','W',7,8),
('Le classiche','Napoli','NAPOLI','W',7.5,8.5),
('Le classiche','Diavola','DIAVOLA','W',8.5,9.5),
('Le classiche','Bufalina','BUFALINA','W',8,9),
('Le classiche','Quattro formaggi','4 FORMAGGI','W',8.5,9.5),
('Le classiche','Prosciutto cotto','PROSCIUTT COTTO','W',9,10),
('Le classiche','Prosciutto e funghi','PROSCIU e FUNGHI','W',9,10),
('Le tradizionali','Capricciosa','CAPRICCIOSA','W',10,11),
('Le tradizionali','Quattro stagioni','4 STAGIONI','W',9,10),
('Le tradizionali','Crudo di Parma','CRUDO DI PARMA','W',11,12),
('Le tradizionali','Verdure','VERDURE','W',9.5,10.5),
('Le tradizionali','Patatosa','PATATOSA','W',9,10),
('Le tradizionali','Parmigiana','PARMIGIANA','W',8.5,9.5),
('Le tradizionali','Tonno e cipolla','TONNO SAP SICILI','W',8,9),
('Le speciali','Crudo e stracciatella','CRUDO E STRACCIA','W',12,13),
('Le speciali','Pescatora','PESCATORA','W',11,12),
('Le speciali','Viennese','VIENNESE','W',10,11),
('Le speciali','Chip & chop','CHIP E CHOP','W',10,11),
('Le speciali','Gorgo calabrese','GORGO CALABRESE','W',10,11),
('Le speciali','Spiritosa','SPIRITOSA','W',10,11),
('Le speciali','Del maestro','DEL MAESTRO','W',10,11),
]
rows=[];tot=0
for sez,n,k,s,p0,p1 in C:
    q=pzm(k,s); fc=FC.get(k,(None,''))
    if k=='RISO PORCINI': p0=18
    d=(p1-p0)/1.1*q*12; tot+=d
    rows.append(dict(sez=sez,n=n,k=k,q=round(q,1),p0=p0,p1=p1,fc=fc[0],src=fc[1],mg=(p1/1.1-fc[0]) if fc[0] is not None else None,anno=round(d)))
json.dump(rows,open(S+'carta.json','w'),ensure_ascii=False)
from collections import defaultdict
bys=defaultdict(int)
for r in rows: bys[r['sez']]+=r['anno']
print(dict(bys),'TOT prezzi',round(tot))
for r in rows:
    if r['fc'] is None: print('NO FC',r['n'])

