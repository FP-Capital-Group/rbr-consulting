"""
Accesso condiviso al database fornitori -> categoria, su Google Sheet
(sostituisce il vecchio Fornitori_Categorie_MASTER.xlsx locale).

Usato da genera_fatture.py, correggi_categoria_master.py, convert_osteria.py.
Il foglio va condiviso in Editor con lo stesso service account di credentials.json.
"""
import os
import re

import gspread
from oauth2client.service_account import ServiceAccountCredentials

BASE = os.path.dirname(os.path.abspath(__file__))


def _resolve(name):
    """Cerca il file in: $CDG_HOME, ~/.claude/rbr (chiavi installate da /rbr-setup),
    cartella dello script, cartella corrente."""
    for d in (os.environ.get('CDG_HOME'), os.path.expanduser('~/.claude/rbr'), BASE, os.getcwd()):
        if d and os.path.exists(os.path.join(d, name)):
            return os.path.join(d, name)
    return os.path.join(os.environ.get('CDG_HOME') or BASE, name)


CREDENTIALS = _resolve("credentials.json")
URL_FILE = _resolve("MASTER_SHEET_URL.txt")
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

CATEGORIE_VALIDE = {
    "fornitori", "servizi", "utenze", "piattaforme delivery",
    "pubblicità - marketing", "provvigioni", "materiali di consumo",
    "viaggi e trasferte",
}


def norm(s):
    return re.sub(r'\s+', ' ', str(s)).strip().lower()


def _worksheet():
    with open(URL_FILE, encoding='utf-8') as f:
        url = f.read().strip()
    scope = SCOPE
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS, scope)
    client = gspread.authorize(creds)
    return client.open_by_url(url).sheet1


def _righe(ws):
    """Righe dati (senza header), ciascuna garantita [nome, categoria]."""
    values = ws.get_values()[1:]
    out = []
    for row in values:
        nome = row[0] if len(row) > 0 else ''
        categoria = row[1] if len(row) > 1 else ''
        if nome:
            out.append([nome, categoria])
    return out


def load_master():
    """Ritorna (worksheet, righe[nome, categoria])."""
    ws = _worksheet()
    return ws, _righe(ws)


def load_master_map():
    """Dict {nome_normalizzato: categoria}, per il lookup dei fornitori durante la categorizzazione."""
    _, righe = load_master()
    return {norm(nome): categoria for nome, categoria in righe}


def append_new_suppliers(nomi, categoria='Altro'):
    """Aggiunge al master i fornitori non ancora presenti (confronto su nome normalizzato).
    Ritorna la lista [nome, categoria] effettivamente aggiunta (esclude duplicati/già presenti)."""
    ws, righe = load_master()
    esistenti = {norm(nome) for nome, _ in righe}
    da_aggiungere, visti = [], set()
    for nome in nomi:
        n = norm(nome)
        if n and n not in esistenti and n not in visti:
            da_aggiungere.append([str(nome).strip(), categoria])
            visti.add(n)
    if da_aggiungere:
        ws.append_rows(da_aggiungere, value_input_option='RAW')
    return da_aggiungere


def update_categoria(fornitore, nuova_categoria):
    """Corregge la Categoria di un fornitore già esistente (match su nome normalizzato).
    Ritorna {'aggiornati': [(nome, vecchia_categoria), ...], 'simili': [...]} — 'simili' e'
    popolato solo se il fornitore non viene trovato, per aiutare l'utente senza indovinare."""
    ws = _worksheet()
    values = ws.get_values()
    target = norm(fornitore)
    aggiornati = []
    for i, row in enumerate(values[1:], start=2):
        nome = row[0] if len(row) > 0 else ''
        categoria = row[1] if len(row) > 1 else ''
        if nome and norm(nome) == target:
            aggiornati.append((nome, categoria))
            ws.update_cell(i, 2, nuova_categoria)
    if aggiornati:
        return {'aggiornati': aggiornati, 'simili': []}

    parole = [p for p in target.split() if len(p) > 3]
    simili = []
    if parole:
        for row in values[1:]:
            nome = row[0] if len(row) > 0 else ''
            if nome and any(p in norm(nome) for p in parole):
                simili.append(nome)
    return {'aggiornati': [], 'simili': simili[:10]}
