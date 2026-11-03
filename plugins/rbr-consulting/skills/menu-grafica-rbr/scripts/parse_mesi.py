import re,glob,json,os
import os; S=os.environ.get('MENU_DATI', '~/Desktop/AI/RBR AI/data/lunablu/menu_inverno_2026/')  # json di lavoro del cliente (esempio Luna Blu)
num=lambda s: float(s.replace('.','').replace(',','.'))
item=re.compile(r'^\s*\d+\s+(\S.*?\S)\s{2,}(-?\d+)\s+.*?(-?[\d.]+,\d\d)\s+(-?[\d.]+,\d\d)\s*$')
sub=re.compile(r'^\s+(-?\d+)\s{5,}([A-Z][A-Za-z&. ]+?)\s{3,}(-?[\d.]+,\d\d)\s*$')
data={}
for f in sorted(glob.glob(S+'mesi/vendite_20*-[01][0-9].txt')):
    m=os.path.basename(f)[8:15]; pend=[]; rows=[]
    for l in open(f):
        a=item.match(l)
        if a: pend.append([a.group(1).strip(),int(a.group(2)),num(a.group(3))]); continue
        b=sub.match(l)
        if b:
            cat=b.group(2).strip()
            for p in pend: rows.append([cat]+p)
            pend=[]
    data[m]=rows
json.dump(data,open(S+'mesi.json','w'))
for m,r in data.items():
    print(m,len(r),sum(x[2] for x in r if x[0]=='PIZZERIA'),round(sum(x[3] for x in r)))

