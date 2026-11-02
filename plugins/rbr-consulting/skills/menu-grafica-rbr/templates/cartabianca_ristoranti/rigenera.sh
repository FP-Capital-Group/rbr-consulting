#!/bin/zsh
# rigenera carte Tennis + Club (prezzi dal foglio definitivo) e i PDF + montaggi di controllo
cd "$(dirname "$0")"
python3 prezzi_live.py && python3 build.py | grep TOTALE
P=../../../suite/plugins/rbr-consulting/skills/carta-menu-rbr/scripts/pdf_menu.py
python3 $P libro carta_tennis.html Menu_Cartabianca_Tennis_2026.pdf --extra-css stampa_libro.css | tail -1
python3 $P libro carta_club.html Menu_Cartabianca_Club_2026.pdf --extra-css stampa_libro.css | tail -1
python3 perche_piatti.py
python3 extra_carte.py

