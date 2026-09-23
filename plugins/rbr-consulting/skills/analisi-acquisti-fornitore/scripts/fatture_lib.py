"""
Libreria di parsing per fatture elettroniche FatturaPA (XML/.p7m).
Uso: importata da estrai_fornitori.py e costruisci_analisi.py di questa stessa skill.

Non presuppone nulla sul fornitore: legge SEMPRE il P.IVA/Denominazione dal
contenuto della fattura, mai dal nome del file (vedi motivazione in SKILL.md,
sezione "Identificare il fornitore reale").
"""
import os
import re
import html
import subprocess

MESI_IT = ['Gen', 'Feb', 'Mar', 'Apr', 'Mag', 'Giu', 'Lug', 'Ago', 'Set', 'Ott', 'Nov', 'Dic']


def mese_label(data_str):
    """'2026-01-14' -> 'Gen-26'"""
    y, m, _d = data_str.split('-')
    return f"{MESI_IT[int(m) - 1]}-{y[2:]}"


def clean_text(s):
    """Le entità XML sono a volte doppiamente escappate (es. '&amp;apos;' invece di
    "'" ) da alcuni gestionali fornitore: due passate di html.unescape risolvono
    entrambi i casi senza rompere il testo normale."""
    for _ in range(2):
        s = html.unescape(s)
    return s


def dedup_descrizione(desc):
    """Alcuni fornitori duplicano — a volte troncando — la <Descrizione> nello
    stesso campo XML, es:
      'CASILLO FARINA 0 PIZZA L/LIEV.KG.25 CASILLO FARINA 0 PIZZA L/LIEV.KG.25'
      'DESANTIS POLPA POPIZZA B/BOX KG.5X2 DESANTIS POLPA POPI'  (troncata)
    Cerca il taglio più a destra tale per cui le parole successive siano un
    prefisso (anche troncato sull'ultima parola) delle prime, e tiene solo la
    prima metà. Se non trova nulla, ritorna il testo invariato."""
    words = desc.split()
    n = len(words)
    for j in range(n - 2, 0, -1):
        rest = words[j:]
        if len(rest) < 2 or len(rest) > j:
            continue
        ok = True
        for k in range(len(rest)):
            if k == len(rest) - 1:
                if not (words[k].startswith(rest[k]) or rest[k] == words[k]):
                    ok = False
            elif rest[k] != words[k]:
                ok = False
            if not ok:
                break
        if ok:
            return ' '.join(words[:j])
    return desc


def extract_xml_text(path):
    """Ritorna il testo XML di una fattura, gestendo sia .xml puro che .p7m
    (busta crittografica CAdES). Per i .p7m usa openssl (già presente su macOS/
    Linux, nessuna dipendenza python aggiuntiva)."""
    if path.endswith('.p7m'):
        try:
            r = subprocess.run(
                ['openssl', 'smime', '-verify', '-noverify', '-inform', 'DER', '-in', path],
                capture_output=True, timeout=20)
            data = r.stdout
            if b'FatturaElettronica' not in data:
                r2 = subprocess.run(
                    ['openssl', 'smime', '-verify', '-noverify', '-in', path],
                    capture_output=True, timeout=20)
                data = r2.stdout
            return data.decode('utf-8', errors='ignore')
        except Exception:
            return ''
    with open(path, 'rb') as fh:
        return fh.read().decode('utf-8', errors='ignore')


def _f(x):
    try:
        return float(x.strip().replace(',', '.'))
    except Exception:
        return None


def get_cedente(txt):
    """Estrae (piva, denominazione) del CedentePrestatore (il VERO mittente
    della fattura) dal contenuto XML. Il prefisso del nome file NON è
    affidabile: spesso è l'IdentificativoTrasmittente di un intermediario SDI
    condiviso da decine di mittenti diversi, non il fornitore."""
    m = re.search(r'<CedentePrestatore>.*?<IdCodice>(.*?)</IdCodice>', txt, re.S)
    piva = m.group(1).strip() if m else None
    m2 = re.search(r'<CedentePrestatore>.*?<Anagrafica>(.*?)</Anagrafica>', txt, re.S)
    denom = None
    if m2:
        block = m2.group(1)
        dm = re.search(r'<Denominazione>(.*?)</Denominazione>', block)
        if dm:
            denom = clean_text(dm.group(1).strip())
        else:
            nm = re.search(r'<Nome>(.*?)</Nome>', block)
            cm = re.search(r'<Cognome>(.*?)</Cognome>', block)
            if nm and cm:
                denom = clean_text((nm.group(1) + ' ' + cm.group(1)).strip())
    return piva, denom


def parse_invoice(path):
    """Ritorna dict con metadati documento + righe prodotto, o None se il file
    non è leggibile (p7m corrotto, xml vuoto, ecc — segnalalo all'utente, non
    ignorarlo silenziosamente su tutta la cartella)."""
    txt = extract_xml_text(path)
    if not txt:
        return None

    tipo_m = re.search(r'<TipoDocumento>(.*?)</TipoDocumento>', txt)
    data_m = re.search(r'<Data>(\d{4}-\d{2}-\d{2})</Data>', txt)
    num_m = re.search(r'<Numero>(.*?)</Numero>', txt)
    piva, denom = get_cedente(txt)

    # isola <DatiBeniServizi> prima di leggere le righe, per non intercettare
    # tag omonimi di altri blocchi (es. DatiPagamento)
    body_m = re.search(r'<DatiBeniServizi>(.*?)</DatiBeniServizi>', txt, re.S)
    body = body_m.group(1) if body_m else txt

    righe = []
    for lm in re.finditer(r'<DettaglioLinee>(.*?)</DettaglioLinee>', body, re.S):
        block = lm.group(1)
        qta_m = re.search(r'<Quantita>([\d.,\s]+)</Quantita>', block)
        if not qta_m:
            # riga senza quantità: riferimento ordine, oppure sconto
            # finanziario a livello fattura (es. "SC.CONTR.ART.15 P.2", Natura
            # N1) non attribuibile a un prodotto specifico — va scartata qui,
            # ma segnala in SKILL.md di controllare lo scarto vs
            # ImponibileImporto dichiarato in fattura
            continue
        qta = _f(qta_m.group(1))
        if not qta:
            continue
        desc_m = re.search(r'<Descrizione>(.*?)</Descrizione>', block, re.S)
        um_m = re.search(r'<UnitaMisura>(.*?)</UnitaMisura>', block)
        prezzo_tot_m = re.search(r'<PrezzoTotale>([\d.,\s\-]+)</PrezzoTotale>', block)
        iva_m = re.search(r'<AliquotaIVA>([\d.,\s]+)</AliquotaIVA>', block)
        cod_m = re.search(r'<CodiceValore>(.*?)</CodiceValore>', block)

        prezzo_tot = _f(prezzo_tot_m.group(1)) if prezzo_tot_m else None
        if prezzo_tot is None:
            continue

        raw_desc = clean_text(re.sub(r'\s+', ' ', desc_m.group(1)).strip()) if desc_m else ''
        righe.append({
            'codice': cod_m.group(1).strip() if cod_m else '',
            'descrizione': dedup_descrizione(raw_desc),
            'um': (um_m.group(1).strip() if um_m else ''),
            'quantita': qta,
            # PrezzoTotale è GIÀ scontato (include gli sconti a cascata di
            # ScontoMaggiorazione) — non ricalcolare da PrezzoUnitario
            'prezzo_totale': prezzo_tot,
            'iva': _f(iva_m.group(1)) if iva_m else None,
        })

    imponibile_dichiarato = sum(
        _f(x) or 0 for x in re.findall(r'<ImponibileImporto>([\-\d.,]+)</ImponibileImporto>', txt))
    imponibile_da_righe = sum(r['prezzo_totale'] for r in righe)

    return {
        'file': os.path.basename(path),
        'tipo_doc': tipo_m.group(1) if tipo_m else None,
        'data': data_m.group(1) if data_m else None,
        'numero': num_m.group(1).strip() if num_m else None,
        'piva_cedente': piva,
        'denominazione_cedente': denom,
        'righe': righe,
        'imponibile_dichiarato': round(imponibile_dichiarato, 2),
        'imponibile_da_righe': round(imponibile_da_righe, 2),
        'scostamento': round(imponibile_dichiarato - imponibile_da_righe, 2),
    }


def is_credito(tipo_doc):
    """TD04 = nota di credito (reso/accredito). TD01/TD24 (e altri TD0x/TD2x
    di fattura) restano 'fatture' ai fini di questa skill."""
    return tipo_doc == 'TD04'


def load_invoices(paths):
    """paths: lista di path assoluti (.xml o .p7m) da processare, GIÀ filtrati
    per il fornitore scelto (usa prima estrai_fornitori.py per la selezione).
    Ritorna la lista ordinata per data, e la lista di file non leggibili."""
    docs = []
    errori = []
    for p in paths:
        d = parse_invoice(p)
        if d and d['data']:
            docs.append(d)
        else:
            errori.append(p)
    docs.sort(key=lambda d: d['data'])
    return docs, errori
