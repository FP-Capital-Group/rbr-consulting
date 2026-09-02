#!/usr/bin/env python3
"""
Converte 'fatture_output OSTERIA.xlsx' (formato gia' aggregato, colonne diverse)
nel formato FATTURE.xlsx atteso dal loader carica_google_sheet.py.

Mappatura colonne:
  Data Emissione        -> Data emissione (dd/mm/YYYY)
  Denominazione Fornitore -> DenominazioneFornitore
  Numero Documento      -> NumeroDocumento
  Tipo Documento (codice) -> TipoDocumento
  Imponibile (€)        -> Imponibile (NEGATIVO se TD04 = nota di credito)
  Imposta (€)           -> Iva
  (Punto Vendita ignorato)
  Categoria             -> dal master Fornitori_Categorie_MASTER.xlsx (norm match); non trovati -> 'Altro'
"""
import os
import re
import sys
import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
CDG = os.environ.get('CDG_HOME') or BASE
sys.path.insert(0, CDG)
import master_sheet as ms

SRC = sys.argv[1] if len(sys.argv) > 1 else os.path.join(BASE, "fatture_output OSTERIA.xlsx")
OUT = os.path.join(BASE, "FATTURE.xlsx")

def norm(s):
    return re.sub(r'\s+', ' ', str(s)).strip().lower()

df = pd.read_excel(SRC)
cat_map = ms.load_master_map()

def get_cat(f):
    return cat_map.get(norm(f), 'Altro')

imp = pd.to_numeric(df['Imponibile (€)'], errors='coerce').fillna(0.0)
# TD04 = nota di credito -> imponibile negativo
is_nc = df['Tipo Documento'].astype(str).str.upper().str.strip() == 'TD04'
imp = imp.where(~is_nc, -imp.abs())

out = pd.DataFrame({
    'Data emissione': pd.to_datetime(df['Data Emissione']).dt.strftime('%d/%m/%Y'),
    'DenominazioneFornitore': df['Denominazione Fornitore'].astype(str).str.strip(),
    'NumeroDocumento': df['Numero Documento'],
    'TipoDocumento': df['Tipo Documento'],
    'Imponibile': imp.round(2),
    'Iva': pd.to_numeric(df['Imposta (€)'], errors='coerce').fillna(0.0).round(2),
    'Lordo': '',
    'Categoria': df['Denominazione Fornitore'].apply(get_cat),
})

out.to_excel(OUT, index=False)
n_altro = (out['Categoria'] == 'Altro').sum()
print(f"FATTURE.xlsx: {len(out)} righe | note credito(TD04): {int(is_nc.sum())} | imponibile tot: {out['Imponibile'].sum():.2f}")
print(f"Righe in 'Altro': {n_altro} | fornitori distinti in Altro: {out[out['Categoria']=='Altro']['DenominazioneFornitore'].nunique()}")
print("Categorie:", out['Categoria'].value_counts().to_dict())
