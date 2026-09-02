#!/usr/bin/env python3
"""
Estrae le fatture elettroniche passive (XML FatturaPA, anche .p7m) da una cartella
(con eventuali sottocartelle) e le divide in piu' FATTURE.xlsx in base al punto vendita
di destinazione (letto da CessionarioCommittente/Sede: Comune + Indirizzo), per clienti
multi-punto-vendita con UNICA partita IVA (dove il CSV Agenzia Entrate non basta perche'
mischia le fatture di tutti i punti vendita).

Uso:
    python3 estrai_fatture_xml.py "<cartella>" --store "PAROLA1=FATTURE_Store1.xlsx" \
                                                 --store "PAROLA2=FATTURE_Store2.xlsx"

- Cerca ricorsivamente tutti i .xml (esclusi *_metaDato.xml, che sono metadati SDI non fatture)
  e .xml.p7m (decodificati al volo con openssl, DER->verify->plaintext).
- Ogni fattura viene assegnata al PRIMO store la cui PAROLA (case-insensitive) e' contenuta nel
  Comune o nell'Indirizzo del CessionarioCommittente. Le fatture che non matchano nessuna parola
  finiscono in "<primo_nome_file>_NON_CLASSIFICATE.xlsx" — NON vengono indovinate, vanno
  controllate a mano.
- Nota di credito (TD04) -> Imponibile negativo (stessa convenzione di genera_fatture.py).
- Assegna la Categoria leggendo dal master condiviso (Google Sheet, via master_sheet.py);
  i fornitori non mappati vengono aggiunti come "Altro" (temporaneo, da ricategorizzare
  con conferma dell'utente prima di caricare sul foglio Google — mai lasciarli in "Altro").
- Deduplica fatture identiche (stesso fornitore + numero + data + importo) che possono
  comparire piu' volte (es. stessa fattura consegnata sia in chiaro che firmata .p7m).
"""
import base64
import glob
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

import pandas as pd

BASE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.environ.get('CDG_HOME') or BASE)
import master_sheet as ms


def ln(tag):
    """Local name di un tag XML, senza namespace Clark-notation {ns}tag."""
    return tag.split('}')[-1]


def testo(elem, nome):
    for child in elem.iter():
        if ln(child.tag) == nome:
            return (child.text or '').strip()
    return ''


def trova_figlio(elem, nome):
    for child in elem.iter():
        if ln(child.tag) == nome:
            return child
    return None


def _openssl_smime(args_extra, stdin_data=None, in_path=None):
    cmd = ['openssl', 'smime', '-verify', '-noverify', '-binary'] + args_extra
    if in_path:
        cmd += ['-in', in_path]
    return subprocess.run(cmd, input=stdin_data, capture_output=True)


def _sembra_xml(stdout):
    return bool(stdout) and b'<FatturaElettronica' in stdout[:2000]


def leggi_xml_bytes(path):
    if not path.endswith('.p7m'):
        with open(path, 'rb') as f:
            return f.read()

    # -noverify salta la verifica della catena di fiducia; il contenuto firmato viene
    # comunque estratto correttamente anche quando openssl segnala "Verification failure"
    # (firma non valida/non verificabile per motivi vari: cert scaduto, algoritmo non
    # supportato...) — non ci interessa l'autenticità crittografica, solo il contenuto,
    # che è già arrivato tramite il canale SDI legittimo. Quindi si ignora il returncode
    # e si valida solo che l'output sembri XML vero.

    # Caso 1: p7m binario DER standard (la maggioranza dei file).
    r = _openssl_smime(['-inform', 'DER'], in_path=path)
    if _sembra_xml(r.stdout):
        return r.stdout

    # Caso 2: alcuni file sono in realtà testo base64 grezzo (senza header PEM, tutto su
    # una riga) — DER fallisce con un errore ASN.1 di parsing (non di verifica). Li si
    # avvolge negli header PEM e si ritenta.
    with open(path, 'rb') as f:
        raw = f.read()
    wrapped = b'-----BEGIN PKCS7-----\n' + raw + b'\n-----END PKCS7-----\n'
    r2 = _openssl_smime(['-inform', 'PEM'], stdin_data=wrapped)
    if _sembra_xml(r2.stdout):
        return r2.stdout

    # Caso 3: fatture con allegati molto grandi (es. PDF incorporato in <Allegati>) in
    # DER a lunghezza indefinita — il parser ASN.1 "legacy" di `openssl smime` si rompe
    # su questa struttura, ma il parser CMS moderno la decodifica correttamente.
    r3 = subprocess.run(
        ['openssl', 'cms', '-verify', '-noverify', '-nosigs', '-no_content_verify', '-no_attr_verify',
         '-binary', '-inform', 'DER', '-in', path],
        capture_output=True,
    )
    if _sembra_xml(r3.stdout):
        return r3.stdout

    raise RuntimeError(
        f"openssl non ha estratto contenuto XML da {path}: "
        f"DER={r.stderr.decode(errors='replace')[:150]} | PEM={r2.stderr.decode(errors='replace')[:150]} | "
        f"CMS={r3.stderr.decode(errors='replace')[:150]}"
    )


MARCATORI_CLIENTE = ('TALPA', 'MISTER X')
ETICHETTE_FORTI = ('DESTINAZIONE MERCE', 'DEST MERCI', 'DEST.MERCE', 'INDIRIZZO DI FORNITURA',
                    'LUOGO DI CONSEGNA', 'UTENZA:', 'DEST.:', 'DEST :', 'DEST:')


def classifica_testo(testo_libero, regole):
    tu = (testo_libero or '').upper()
    for parole, _, etichetta in regole:
        if any(p.upper() in tu for p in parole):
            return etichetta
    return None


def classifica_testo_affidabile(testo_libero, regole):
    """Come classifica_testo, ma accetta il match SOLO se il testo e' riconoscibile come
    riferito alla consegna/destinazione del cliente — o perche' nomina il cliente stesso
    ('LA TALPA', 'MISTER X'), o perche' e' introdotto da un'etichetta esplicita e
    inequivocabile tipo 'DESTINAZIONE MERCE:'/'INDIRIZZO DI FORNITURA:'/'UTENZA:'. Necessario
    perche' alcuni fornitori scrivono nomi di luogo che NON sono la destinazione del cliente
    ma un proprio riferimento interno — es. il codice del proprio punto vendita di ritiro
    (visto realmente: 'Store: 62 - Trento') — che menzionerebbero una citta' senza riferirsi
    affatto a dove e' stata consegnata la merce del cliente."""
    tu = (testo_libero or '').upper()
    if not (any(m in tu for m in MARCATORI_CLIENTE) or any(e in tu for e in ETICHETTE_FORTI)):
        return None
    return classifica_testo(testo_libero, regole)


def estrai_testo_allegati(root):
    """Estrae il testo di eventuali PDF allegati alla fattura (es. bolletta utenza):
    alcuni fornitori (utenze, gas...) mettono l'indirizzo di fornitura SOLO nel PDF
    allegato, non in nessun campo strutturato dell'XML."""
    testi = []
    for att in root.iter():
        if ln(att.tag) != 'Attachment':
            continue
        b64 = (att.text or '').strip()
        if not b64:
            continue
        try:
            pdf_bytes = base64.b64decode(b64)
        except Exception:
            continue
        if not pdf_bytes.startswith(b'%PDF'):
            continue  # allegati non-PDF (es. .p7m, .xls) non gestiti
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=True) as tf:
            tf.write(pdf_bytes)
            tf.flush()
            r = subprocess.run(['pdftotext', '-layout', tf.name, '-'], capture_output=True)
        if r.returncode == 0:
            testi.append(r.stdout.decode('utf-8', errors='replace'))
    return ' '.join(testi)


def estrai_fatture(path, regole):
    """Ritorna una lista di dict (una riga per documento, o piu' righe se lo stesso documento
    contiene consegne per punti vendita diversi — vedi destinazione riga-per-riga sotto)."""
    raw = leggi_xml_bytes(path)
    root = ET.fromstring(raw)

    header = trova_figlio(root, 'FatturaElettronicaHeader')
    cedente = trova_figlio(header, 'CedentePrestatore')
    cessionario = trova_figlio(header, 'CessionarioCommittente')

    fornitore = testo(cedente, 'Denominazione')
    if not fornitore:
        fornitore = f"{testo(cedente, 'Nome')} {testo(cedente, 'Cognome')}".strip()

    comune_header = testo(cessionario, 'Comune')
    indirizzo_header = testo(cessionario, 'Indirizzo')
    denominazione_header = testo(cessionario, 'Denominazione')
    # L'intestazione (Sede del CessionarioCommittente) e' l'ULTIMA istanza, non la prima:
    # per un piccolo numero di fornitori (grandi distributori con un'unica anagrafica
    # cliente) riporta sempre la stessa sede legale fissa, indipendentemente dal punto
    # vendita di consegna reale — ma per la maggior parte dei fornitori la varia
    # correttamente fattura per fattura (a volte perfino nel nome stesso, es. "...AL
    # MISTER X"), quindi va comunque usata quando non c'e' nient'altro di piu' specifico.
    store_header = classifica_testo(f"{comune_header} {indirizzo_header} {denominazione_header}", regole)
    testo_allegati = None  # calcolato pigro, solo se serve (costoso: decodifica+pdftotext)

    righe = []
    for body in root.iter():
        if ln(body.tag) != 'FatturaElettronicaBody':
            continue
        dg = trova_figlio(body, 'DatiGeneraliDocumento')
        if dg is None:
            continue
        tipo = testo(dg, 'TipoDocumento')
        numero = testo(dg, 'Numero')
        data = testo(dg, 'Data')

        imponibile_tot, iva_tot = 0.0, 0.0
        for riep in body.iter():
            if ln(riep.tag) == 'DatiRiepilogo':
                imponibile_tot += float(testo(riep, 'ImponibileImporto') or 0)
                iva_tot += float(testo(riep, 'Imposta') or 0)

        def riga_base(store, imponibile, iva):
            imp = -abs(imponibile) if tipo.upper() == 'TD04' else imponibile
            return {
                'Data emissione': data, 'DenominazioneFornitore': fornitore,
                'NumeroDocumento': numero, 'TipoDocumento': tipo,
                'Imponibile': round(imp, 2), 'Iva': round(iva, 2), 'Lordo': '',
                '_store': store, '_comune_dest': comune_header, '_indirizzo_dest': indirizzo_header,
                '_file': os.path.basename(path),
            }

        # La destinazione vera puo' comparire in punti diversi a seconda del gestionale del
        # fornitore, in ordine di priorita' (dal piu' al meno specifico):
        #  1. riga per riga, in Descrizione o AltriDatiGestionali (Segafredo, PREGIS, RESS
        #     Multiservices, SU.CE., Enterprise...) — vale anche per le righe successive che
        #     non ne specificano una propria, fino al prossimo cambio (fatture/DDT con piu'
        #     consegne raggruppate);
        #  2. nella Causale del documento (es. A.I.A.: "DESTINAZIONE MERCE: ...", Partesa:
        #     "Codice cliente: ... LA TALPA...");
        #  3. nel testo di un eventuale PDF allegato alla fattura (es. bollette utenze/gas
        #     che riportano l'indirizzo di fornitura SOLO li', non in nessun campo XML —
        #     visto su Butangas);
        #  4. in ULTIMA istanza, l'intestazione (Sede/Denominazione del CessionarioCommittente):
        #     per un piccolo numero di grandi fornitori riporta sempre un'unica sede fissa
        #     indipendente dal punto vendita reale (da qui la necessita' dei punti 1-3 come
        #     priorita'), ma per la maggior parte la varia correttamente fattura per fattura
        #     (a volte perfino nel nome, es. "...AL MISTER X") quindi resta un fallback valido
        #     quando non c'e' nient'altro di piu' specifico.
        causale_txt = ' '.join(c.text or '' for c in dg.iter() if ln(c.tag) == 'Causale')
        store_causale = classifica_testo_affidabile(causale_txt, regole)

        dest_corrente = None
        subtotali = {}
        una_riga_ha_dest = False
        for linea in body.iter():
            if ln(linea.tag) != 'DettaglioLinee':
                continue
            pezzi = [testo(linea, 'Descrizione')]
            for adg in linea:
                if ln(adg.tag) == 'AltriDatiGestionali':
                    pezzi.append(testo(adg, 'RiferimentoTesto'))
            store_riga = classifica_testo_affidabile(' '.join(pezzi), regole)
            if store_riga:
                dest_corrente = store_riga
                una_riga_ha_dest = True
            try:
                prezzo = float(testo(linea, 'PrezzoTotale') or 0)
            except ValueError:
                prezzo = 0.0
            chiave = dest_corrente or '_SENZA_DEST_'
            subtotali[chiave] = subtotali.get(chiave, 0.0) + prezzo

        def fallback_finale():
            nonlocal testo_allegati
            if store_causale:
                return store_causale
            if testo_allegati is None:
                testo_allegati = estrai_testo_allegati(root)
            store_allegato = classifica_testo_affidabile(testo_allegati, regole)
            if store_allegato:
                return store_allegato
            return store_header

        if not una_riga_ha_dest:
            righe.append(riga_base(fallback_finale(), imponibile_tot, iva_tot))
            continue

        # righe iniziali prima del primo cambio di destinazione (dest_corrente ancora None
        # quando sono state lette): usano il fallback (causale/allegato/intestazione).
        if '_SENZA_DEST_' in subtotali:
            chiave_fallback = fallback_finale() or '_SENZA_DEST_'
            subtotali[chiave_fallback] = subtotali.get(chiave_fallback, 0.0) + subtotali.pop('_SENZA_DEST_')

        somma_righe = sum(subtotali.values())
        for store, imp_parziale in subtotali.items():
            quota = (imp_parziale / somma_righe) if somma_righe else 0.0
            # riproporziona sul totale IMPONIBILE ufficiale (da DatiRiepilogo, non dalla somma
            # delle righe che puo' differire per sconti/arrotondamenti a livello documento)
            righe.append(riga_base(
                None if store == '_SENZA_DEST_' else store,
                imponibile_tot * quota,
                iva_tot * quota,
            ))
    return righe


def main():
    if len(sys.argv) < 2 or '--store' not in sys.argv:
        print('Uso: python3 estrai_fatture_xml.py "<cartella>" --store "PAROLA1,PAROLA2=Output.xlsx" [--store "PAROLA3=Output2.xlsx" ...]')
        sys.exit(1)

    cartella = sys.argv[1]
    regole = []  # (parole_chiave: list[str], outfile, etichetta)
    args = sys.argv[2:]
    for i, a in enumerate(args):
        if a == '--store' and i + 1 < len(args):
            chiavi, _, outfile = args[i + 1].partition('=')
            parole = [p.strip() for p in chiavi.split(',') if p.strip()]
            regole.append((parole, outfile, parole[0]))

    file_xml = [f for f in glob.glob(os.path.join(cartella, '**', '*.xml'), recursive=True)
                if not f.endswith('_metaDato.xml')]
    file_p7m = glob.glob(os.path.join(cartella, '**', '*.xml.p7m'), recursive=True)
    tutti = file_xml + file_p7m
    print(f"File fattura trovati: {len(file_xml)} .xml + {len(file_p7m)} .xml.p7m = {len(tutti)}")

    righe, errori = [], []
    for f in tutti:
        try:
            righe.extend(estrai_fatture(f, regole))
        except Exception as e:
            errori.append((f, str(e)))

    if errori:
        print(f"\n!! {len(errori)} file non decodificati/parsati:")
        for f, e in errori[:20]:
            print(f"   {f}: {e}")

    df = pd.DataFrame(righe)
    print(f"\nDocumenti estratti: {len(df)}")

    # --- deduplica: stessa fattura consegnata piu' volte (es. sia in chiaro sia .p7m) ---
    prima = len(df)
    df = df.drop_duplicates(subset=['DenominazioneFornitore', 'NumeroDocumento', 'Data emissione', 'Imponibile', '_store'])
    if prima != len(df):
        print(f"Duplicati rimossi: {prima - len(df)} (stesso fornitore+numero+data+importo+destinazione)")

    non_class = df[df['_store'].isna()]
    if len(non_class) > 0:
        out_nc = os.path.join(os.getcwd(), 'FATTURE_NON_CLASSIFICATE.xlsx')
        non_class.drop(columns=['_store']).to_excel(out_nc, index=False)
        print(f"\n!! {len(non_class)} fatture non classificate (nessuna parola combacia) -> {out_nc}")
        print("   Comuni destinazione trovati (non riconosciuti):")
        for c in sorted(non_class['_comune_dest'].unique()):
            print(f"   - {c!r}")

    # --- categorizzazione dal master condiviso ---
    for parole, outfile, etichetta in regole:
        sub = df[df['_store'] == etichetta].copy()
        if sub.empty:
            print(f"\n[{etichetta}] nessuna fattura.")
            continue

        cat_map = ms.load_master_map()  # ricaricato per ogni store: riflette gli "Altro" appena aggiunti dallo store precedente
        sub['Categoria'] = sub['DenominazioneFornitore'].apply(lambda f: cat_map.get(ms.norm(f)))
        nuovi = sub[sub['Categoria'].isna()]['DenominazioneFornitore'].unique()
        if len(nuovi) > 0:
            aggiunti = ms.append_new_suppliers(nuovi, categoria='Altro')
            sub['Categoria'] = sub['Categoria'].fillna('Altro')
            print(f"\n[{etichetta}] Fornitori non mappati ({len(nuovi)}), aggiunti al master come 'Altro' ({len(aggiunti)} nuovi su Sheet):")
            for f in sorted(nuovi):
                print(f"   {f}")

        sub = sub.drop(columns=['_comune_dest', '_indirizzo_dest', '_file', '_store'])
        sub['_sort'] = pd.to_datetime(sub['Data emissione'], errors='coerce')
        sub = sub.sort_values('_sort', ascending=False).drop(columns='_sort').reset_index(drop=True)
        sub['Data emissione'] = pd.to_datetime(sub['Data emissione']).dt.strftime('%d/%m/%Y')

        sub.to_excel(outfile, index=False)
        n_nc = int((sub['Imponibile'] < 0).sum())
        print(f"[{etichetta}] {outfile}: {len(sub)} righe, {n_nc} note di credito, imponibile totale {sub['Imponibile'].sum():.2f}")


if __name__ == '__main__':
    main()
