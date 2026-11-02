import openpyxl,json
from openpyxl.utils import get_column_letter as L
wb=openpyxl.load_workbook('consegne/2026-10-07/02 - Food Cost - LunaBlu - PRECOMPILATO RBR.xlsx')
fc=wb['Food Cost']
nat=json.load(open('~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/native_fc_backup.json'))
def nv(r,c):
    try: return nat[r-1][c-1]
    except: return ''
CAFF=range(43,48)
STD={ # scarto % (maggiorazione sul peso in ricetta), motivo
 'rucola':(10,'pulizia'),'radicchio':(20,'pulizia'),'zucchine':(5,'pulizia'),'melanzane':(10,'pulizia'),
 'peperoni':(25,'torsolo e semi'),'cipolla':(10,'buccia'),'carote':(15,'pelatura'),'fagiolini':(10,'punte'),
 'cetrioli':(10,'pulizia'),'pomodorini':(3,'pulizia'),'datterini':(3,'pulizia'),'pomodori':(5,'pulizia'),
 'prezzemolo':(40,'gambi'),'basilico':(40,'gambi'),'rosmarino':(40,'rametti'),'aglio':(15,'buccia'),
 'melone':(80,'buccia e semi, resa 55%'),'avvocado':(50,'buccia e nocciolo, resa 67%'),
 'carciofi':(65,'latta: peso sgocciolato circa 60%'),
 'calamari':(40,'pulizia + glassatura del congelato, resa 70%'),'calamari (crudi)':(40,'pulizia + glassatura, resa 70%'),
 'calamari (puliti)':(40,'pulizia + glassatura, resa 70%'),
 'gamberi':(15,'glassatura del congelato'),'gamberi (cotti)':(35,'glassatura + calo cottura'),
 'gamberetti':(15,'glassatura del congelato'),'gamberetti(cotti)':(30,'glassatura + calo cottura'),
 'gamberoni':(15,'glassatura del congelato'),'mazzancolle':(15,'glassatura del congelato'),
 'seppie':(25,'pulizia'),'polipo':(10,'pulizia testa e becco'),'polpo':(10,'pulizia testa e becco'),
 'triglie':(20,'eviscerazione'),'alici':(50,'testa e lisca, resa 67%'),'vongole':(5,'spurgo e rotte'),
 'cozze':(10,'barba e rotte'),'cozze (crude)':(10,'barba e rotte'),'pesce spada (crudo)':(15,'pelle + glassatura'),
 'spada':(15,'pelle + glassatura'),'carne di manzo':(10,'rifilatura'),'petto di pollo':(5,'rifilatura'),
 'porcini (cotti)':(50,'calo cottura'),
 'crudo':(10,'cotenna e grasso al taglio'),'speck':(10,'cotenna al taglio'),'culatello':(15,'cotenna e legatura'),
 'cotto':(5,'sfrido affettatrice'),'salame':(5,'pelle'),'salame piccante':(5,'pelle'),'coppa':(5,'sfrido'),
 'bresaola':(5,'sfrido'),'pancetta':(5,'cotenna'),'parmigiano':(10,'crosta'),'parmigiano reggiano':(10,'crosta'),
 'scaglie di parmigiano':(10,'crosta'),'grattugia di parmigia':(10,'crosta'),'grana':(10,'crosta'),
 'bufala':(10,'siero'),'provola':(5,'crosta'),
}
writes={}  # a1 -> (value, color, note)
for r in range(1,fc.max_row+1):
  for c in range(1,62):
    if c in CAFF: continue
    x=fc.cell(r,c).value; y=nv(r,c)
    if x is None: x=''
    if str(x).strip()!=str(y).strip():
        cell=fc.cell(r,c); col=cell.fill.fgColor.rgb if isinstance(cell.fill.fgColor.rgb,str) else None
        writes[L(c)+str(r)]=[x,col,cell.comment.text if cell.comment else None]
# scarti standard
pc=[c for c in range(1,62) if fc.cell(4,c).value=='Prodotto' and c not in CAFF]
nstd=0
for c in pc:
  for r in range(5,fc.max_row+1):
    a=fc.cell(r,c).value; g=fc.cell(r,c+1).value
    if not isinstance(a,str) or not isinstance(g,(int,float)) or g<=0: continue
    k=a.strip().lower()
    if k in STD:
      s,why=STD[k]; a1=L(c+3)+str(r)
      cur=fc.cell(r,c+3).value or 0
      if cur!=s:
        writes[a1]=[s,'00FFD8A8',f'Scarto reale STIMA RBR ({why}) - standard di settore, da confermare con una pesata in cucina']; nstd+=1
json.dump(writes,open('~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/writes.json','w'),default=str)
print(len(writes),'celle; scarti standard nuovi',nstd)

