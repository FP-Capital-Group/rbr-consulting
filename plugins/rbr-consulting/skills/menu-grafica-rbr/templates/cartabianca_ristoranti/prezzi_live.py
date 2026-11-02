# -*- coding: utf-8 -*-
"""Scarica i tab «Prezzi BAR» e «Prezzi RISTORANTI» del foglio «Prezzi e personale - Cartabianca»
(formato pulito del 03/10/2026) → prezzi_live.json. Lo leggono build.py e bar/build_pranzo.py.
Dal 03/10 sera il foglio si chiama «Prezzi definitivi - Cartabianca»: si usa la colonna PREZZO FINALE.
Uso: python3 prezzi_live.py   (dalla root del repo o da qui)"""
import json, os
from google.oauth2 import service_account
from googleapiclient.discovery import build

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
SID = '1CMhwMHHyh6SK0xFeLGSTVRuLNk7dGkbUsCZnsgEFjDE'

if __name__ == '__main__':
    c = service_account.Credentials.from_service_account_file(
        os.path.join(ROOT, 'shared/credentials/service_account.json'),
        scopes=['https://www.googleapis.com/auth/spreadsheets.readonly'])
    s = build('sheets', 'v4', credentials=c).spreadsheets()
    out = {}
    for t in ('Prezzi BAR', 'Prezzi RISTORANTI'):
        v = s.values().get(spreadsheetId=SID, range=f"'{t}'!A2:L",
                           valueRenderOption='UNFORMATTED_VALUE').execute().get('values', [])
        H = v[0]
        out[t] = [dict(zip(H, r + [''] * len(H))) for r in v[2:] if len(r) > 1]
    json.dump(out, open(os.path.join(HERE, 'prezzi_live.json'), 'w'), ensure_ascii=False, indent=0)
    print({k: len(v) for k, v in out.items()})

