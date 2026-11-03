# -*- coding: utf-8 -*-
"""Carte ingegnerizzate Cartabianca: Tennis Club Sesto + Cartabianca Club (San Mauro).
Fonte piatti/descrizioni: menu stampati 08/09/2026 (~/Desktop/Menu Cartabianca/).
sale  = (categoria ks3, prodotto ks3)        -> venduto 6 mesi mar-ago 2026 + classe K-S
sheet = (categoria foglio, prodotto foglio)  -> prezzo approvato dal cliente (Confronto RISTORANTI)
card  = nome ricetta nel file 02             -> food cost se il piatto è nuovo o la ricetta è cambiata
"""

# ---------- abbinamenti ----------
def V(tipo, cantina, vino): return ('v', tipo, cantina, vino)
def B(tipo, nome): return ('b', tipo, '', nome)

T_CUVEE = V('bollicine', 'Cuvée', 'Millesimato')
T_PROS  = V('bollicine', 'Prosecco Superiore', 'DOCG Extra Dry')
T_PAS   = V('bianco', 'Tratturo', 'Passerina Terre di Chieti')
T_PEC   = V('bianco', 'Tratturo', 'Pecorino Terre di Chieti')
T_RIB   = V('bianco', 'Ribolla Gialla', 'delle Venezie')
T_FAL   = V('bianco', "Picco dell'Angelo", 'Falanghina')
T_TRA   = V('bianco', 'Vigna del Lauro', 'Traminer Isonzo')
T_CER   = V('rosato', "Cerasuolo d'Abruzzo", 'DOC')
T_ZIZ   = V('rosso', 'Zizzolo', 'Bolgheri')
T_HELL  = B('chiara', 'Hacker Hell')
T_WEIS  = B('bianca', 'Hacker Weisse')
T_KELL  = B('ambrata', 'Hacker Kellerbier')
T_BLON  = B('chiara', 'Lupulus Blonde')
T_BRUN  = B('scura', 'Lupulus Brune')
T_IPA   = B('ambrata', 'Punk IPA')

C_PAS, C_PEC, C_TRA, C_ZIZ = T_PAS, T_PEC, T_TRA, T_ZIZ
C_TRIP  = B('chiara', 'Lupulus Triple')
C_WEIS  = B('bianca', 'Ayinger Bräu-Weisse')
C_KELL  = B('ambrata', 'Ayinger Kellerbier')
C_BRUN  = B('scura', 'Lupulus Brune')
C_BLAN  = B('bianca', 'Lupulus Blanche')


def d(nome, desc, prezzo, sale=None, sheet=None, card=None, alg='', abb=None, **kw):
    x = dict(nome=nome, desc=desc, old=prezzo, sale=sale, sheet=sheet, card=card, alg=alg, abb=abb)
    x.update(kw)
    return x


# =====================================================================
#  TENNIS CLUB SESTO
# =====================================================================
AT, PT, ST, CT = 'Antipasti Tennis', 'Primi Tennis', 'Secondi Tennis', 'Contorni Tennis'
PCT, PGT, PST, CZT, DT = ('PIZZE CLASSICHE TENNIS', 'PIZZE GOURMET TENNIS', 'PIZZE SPECIALI TENNIS',
                          'CALZONI E COVACCINI TENNIS', 'Dessert Tennis')
sPCT, sPGT, sPST, sCZT = 'Pizze Classiche Tennis', 'Pizze Gourmet Tennis', 'Pizze Speciali Tennis', 'Calzoni E Covaccini Te'

TENNIS = dict(
  sigla='TENNIS', nome='Tennis Club Sesto', luogo='Sesto Fiorentino',
  pomodoro='pomodoro San Marzano dop',
  indirizzo='Via degli Scarpettini 39/A · 50019 Sesto Fiorentino · 055 0935001',
  coccoli_fc=2.91,
  premium_antipasti=[
    d('Selezione Cartabianca di terra', 'Un assaggio di tutti i nostri antipasti di terra', 15,
      card='Selezione CB Antipasti Terra', alg='1-3-7', abb=T_ZIZ),
    d('Selezione Cartabianca di mare', 'I nostri antipasti di mare, cotti', 16,
      card='Selezione CB Antipasti Mare', alg='1-2-4-14', abb=T_FAL),
    d('Selezione Cartabianca di mare con crudo', 'Il mare cotto più i crudi e i marinati del giorno', 17,
      card='Selezione CB Antipasti Mare + Crudo', alg='1-2-4-14', abb=T_CUVEE),
  ],
  antipasti=[
    d('Tris di cruditè', 'Tartare di tonno con teriyaki e frutti di bosco, salmone con chips e crema di topinambur, tartare di gamberi con burrata e pistacchi', 15,
      sale=(AT, 'Tris Tartare di Mare'), sheet=(AT, 'Tris Tartare di Mare'), alg='2-4-6-7-8', abb=T_CUVEE),
    d('Battuta di scottona', 'Tuorlo fritto, burrata e scaglie di tartufo', 15,
      sale=(AT, 'Degustazione Tartare di Manzo'), sheet=(AT, 'Degustazione Tartare di Manzo'), card='Battuta di Scottona', fc_da='card',
      alg='3-7', abb=T_CER, era='Degustazione tartare di manzo'),
    d('Zuppetta di moscardini alla Luciana', 'Con polentine fritte', 13,
      sale=(AT, 'Moscardini e Polenta'), sheet=(AT, 'Moscardini e Polenta'), card='Moscardini in Umido con Polentine Fritte', fc_da='card',
      alg='9-12-14', abb=T_PAS, era='Moscardini e polenta'),
    d('Bruschette Cartabianca', 'Pane toscano con salsiccia e stracchino, cavolo nero e pecorino; polentine fritte con fegatini e funghi trifolati', 10,
      sale=(AT, 'Bruschette del Club'), sheet=(AT, 'Bruschette del Club'), alg='1-7-9', abb=T_ZIZ),
    d('Polpo rosticciato', 'Cotto a bassa temperatura, su morbido di patate, terra di olive e capperi', 14,
      sale=(AT, 'Polpo Grigliato su Hummus'), sheet=(AT, 'Polpo Grigliato su Hummus'), card='Polpo CBT', fc_da='card',
      alg='14', abb=T_PEC, era='Polpo grigliato su hummus'),
    d('Tagliere CB', 'Salumi, pecorino di Seggiano, miele millefiori e pappa al pomodoro con burrata', 13,
      sale=(AT, 'Tagliere CB'), sheet=(AT, 'Tagliere CB'), alg='1-7', abb=T_ZIZ),
    d('Coccoli artigianali', 'Con prosciutto crudo e stracchino montato', 12,
      sale=(AT, 'Coccoli Crudo e Stracchino Montato'), sheet=(AT, 'Coccoli Crudo e Stracchino Montato'), alg='1-7', abb=T_PROS),
  ],
  fuori_antipasti=[
    d('Budino di polenta ripieno di brie', '', 12, card='Budino di Polenta', motivo='nuovo, mai venduto, margine sotto la media'),
    d('Crocchette di baccalà', '', 13, card='Crocchette Baccalà', motivo='nuovo, il margine più basso della sezione (8,68 €)'),
    d('Bistecchina di totano', '', 13, card='Bistecchina Totano', motivo='nuovo, mai venduto, margine sotto la media'),
  ],
  premium_primi=[
    d('Risotto mantecato al Castelmagno', 'Tartare e jus di manzo, zucca confit e scaglie di tartufo', 15,
      card='Risotto al Castelmagno', alg='7-9-12', abb=T_CER),
    d('Risotto al fondo di polpo', 'Tentacolo grigliato, cavolo nero e pomodorini confit', 15,
      card='Risotto POLPO', alg='9-12-14', abb=T_FAL),
    d('Chicche di patate su vellutata di mare', 'Crudo di gamberi al limone e chips di topinambur', 15,
      card='Chicche Mare', alg='1-2-3-4', abb=T_CUVEE),
  ],
  primi=[
    d('Spaghetti freschi alla carbonara', 'Pasta artigianale, guanciale, tuorlo, pecorino', 13,
      card='Spaghetti Carbonara', alg='1-3-7', abb=T_PEC),
    d('Pacchero al ragù di cinghiale', 'Crumble di cacao amaro e nocciole alle erbe', 14,
      card='Paccheri Ragù Cinghiale', alg='1-8-9-12', abb=T_ZIZ),
    d('Gnudi di ricotta e spinaci', 'Di nostra produzione, su vellutata di salvia, cialde di parmigiano e mais', 12,
      sale=(PT, 'Gnudi'), sheet=(PT, 'Gnudi'), alg='1-3-7', abb=T_TRA),
    d('Linguine alle vongole veraci', 'E bottarga di muggine', 14,
      sheet=(PT, 'Linguine Vongole e Bottarga'), card='Linguine Vongole Bottarga', q6=436, cls='PLOWHORSE',
      alg='1-4-14', abb=T_PAS),
    d('Fregola "in nero"', 'Stracotto di seppie e crema di burrata di Andria', 14,
      card='Fregola IN NERO', alg='1-7-14', abb=T_RIB),
  ],
  premium_secondi=[
    d('Bistecca alla fiorentina', 'Cotta sulla brace, al sangue come vuole la tradizione · al kg', 38,
      sale=(ST, 'Bistecca alla Fiorentina KG'), nuovo_prezzo=42, per2=True, alg='', abb=T_ZIZ,
      flag='fuori carta oggi: 50 kg in 6 mesi a 37,91 €/kg di media in cassa'),
    d('Tagliata di scottona alla griglia', 'Con cavolo nero e lardo', 18,
      sale=(ST, 'Tagliata di Manzo'), sheet=(ST, 'Tagliata di Manzo'), card='Tagliata di Scottona Cavolo e Lardo', fc_da='card',
      alg='', abb=T_ZIZ, era='Tagliata di manzo'),
    d('Tonno rosso marinato alla barbecue', 'In crosta di sesamo, su morbido di sedano rapa e cavolo nero', 18,
      sale=(ST, 'Tagliata di Tonno'), sheet=(ST, 'Tagliata di Tonno'), card='Tonno Rosso Marinato', fc_da='card',
      alg='4-6-9-11', abb=T_CER, era='Tagliata di tonno'),
  ],
  secondi=[
    d('Frittura di mare', 'Calamari e gamberi su letto di verdure croccanti', 16,
      sale=(ST, 'Frittura Mare'), sheet=(ST, 'Frittura Mare'), alg='1-2-14', abb=T_PROS),
    d('Galletto al mattone', 'Cotto a bassa temperatura, con verdure al forno', 16,
      sale=(ST, 'Galletto Mattone CBT + Contorno'), sheet=(ST, 'Galletto Mattone CBT + Contorno'), alg='', abb=T_CER),
    d('Goulash di mare', 'Polpo, seppia e totano gigante in cacciucco leggero, patate stufate', 18,
      card='Goulash Mare', alg='9-12-14', abb=T_ZIZ),
    d('Spiedino grigliato', 'Pancia, filetto, salsiccia e coppa di suino grigio del Casentino, fagioli all\'uccelletta', 15,
      card='Spiedino CBT', alg='', abb=T_ZIZ),
    d('Cartabianca Burger', 'Manzo 180 g, pane multicereali, bacon affumicato, scamorza, insalata, salsa Cartabianca e patate crispers', 15,
      sale=(ST, 'Cartabianca Burger'), sheet=(ST, 'Cartabianca Burger'), alg='1-3-7-10-11', abb=T_KELL),
    d('Filetto di baccalà in olio cottura', 'Su hummus di ceci al timo', 16,
      card='Filetto Baccalà', alg='4-11', abb=T_PAS),
  ],
  contorni=[
    d('Patatine fritte', '', 5, sale=(CT, 'Patate Fritte'), sheet=(CT, 'Patate Fritte')),
    d('Verdure al forno', '', 6, sale=(CT, 'Verdure Grigliate'), sheet=(CT, 'Verdure Grigliate')),
    d('Fagioli all\'uccelletta', '', 5, card='Fagioli Uccelletta'),
    d('Patate arrosto', '', 5, sale=(CT, 'Patate Arrosto'), sheet=(CT, 'Patate Arrosto')),
    d('Insalata di misticanza', '', 5, sale=(CT, 'Insalata Misticanza'), sheet=(CT, 'Insalata Misticanza')),
  ],
  classiche=[
    d('Margherita', 'Basilico fresco', 7.5, sale=(PCT, 'Margherita'), alg='1-7', abb=T_HELL),
    d('Marinara', 'Aglio, origano e basilico fresco. Senza mozzarella', 7, sale=(PCT, 'Marinara'), alg='1', abb=T_HELL),
    d('Napoli', 'Capperi, acciughe di Cetara, origano e basilico', 9, sale=(PCT, 'Napoli-'), alg='1-4-7', abb=T_WEIS),
    d('Bufala Dop', 'Bufala andriese dop al posto del fior di latte', 9, sale=(PCT, 'Bufala Dop'), alg='1-7', abb=T_WEIS),
    d('4 Formaggi', 'Gorgonzola, provola e stracchino', 9, sale=(PCT, '4 Formaggi-'), alg='1-7', abb=T_KELL),
    d('Vegetariana', 'Melanzane, zucchine e pomodorini', 8.5, sale=(PCT, 'Vegetariana-'), sheet=(sPCT, 'Vegetariana'), alg='1-7', abb=T_WEIS),
    d('Parmigiana', 'Melanzane e crema di parmigiano', 8.5, sale=(PCT, 'Parmigiana'), sheet=(sPCT, 'Parmigiana'), alg='1-7', abb=T_HELL),
  ],
  saporite=[
    d('Salamino', 'Salamino piccante', 8.5, sale=(PCT, 'Salamino-'), alg='1-7', abb=T_IPA),
    d('Würstel', 'Würstel', 8.5, sale=(PCT, 'Wurstel-'), sheet=(sPCT, 'Wurstel'), alg='1-7', abb=T_HELL),
    d('Prosciutto & funghi', 'Prosciutto cotto e champignon', 8.5, sale=(PCT, 'Prosciutto e Funghi-'), alg='1-7', abb=T_HELL),
    d('Capricciosa', 'Carciofi, olive, würstel, champignon e prosciutto cotto', 8.5, sale=(PCT, 'Capricciosa-'), sheet=(sPCT, 'Capricciosa'), alg='1-7', abb=T_KELL),
    d('Salsiccia & cipolla', 'Salsiccia e cipolla', 8.5, sale=(PCT, 'Salsiccia e Cipolla-'), sheet=(sPCT, 'Salsiccia e Cipolla'), alg='1-7', abb=T_KELL),
    d('Maialona', 'Prosciutto cotto, salsiccia, salamino e würstel', 9, sale=(PCT, 'Maialona-'), sheet=(sPCT, 'Maialona'), alg='1-7', abb=T_BRUN),
    d('Melanzane & provola', 'Melanzane al forno e provola', 8.5, sale=(PCT, 'Melanzane e Provola-'), sheet=(sPCT, 'Melanzane e Provola'), alg='1-7', abb=T_HELL),
  ],
  fuori_pizze=[
    d('Tonno & cipolla', '', 8.5, sale=(PCT, 'Tonno e Cipolla'), motivo='DOG: food cost 43%, il margine più basso delle pizze'),
    d('Zucchine & gamberetti', '', 9, sale=(PCT, 'Zucchine e Gamberetti-'), motivo='12 pezzi in 6 mesi'),
    d('La Piccante', '', 10, sale=(PST, 'La Piccante-'), motivo='DOG tra le speciali'),
    d('Pescatora', '', 12, sale=(PST, 'Pescatora-'), motivo='DOG: food cost 64%, 3,95 € di margine su 12 €'),
    d('Del Pizzaiolo', '', 9, sale=(PST, 'Del Pizzaiolo'), motivo='11 pezzi in 6 mesi'),
    d('Calzone bianco', '', 8.5, sale=(CZT, 'Calzone Bianco-'), motivo='15 pezzi in 6 mesi'),
  ],
  tartufate=[
    d('La Tartufina', 'Pomodoro San Marzano dop, bufala andriese e tartufo nero', 14,
      sale=(PST, 'La Tartufina-'), sheet=(sPST, 'La Tartufina'), alg='1-7', abb=T_CER),
    d('La Mortazza & Tartufo', 'Bianca con fior di latte, mortadella, scaglie di tartufo e crema di parmigiano', 14,
      sale=(PST, 'La Mortazza e Tartufo'), sheet=(sPST, 'La Mortazza e Tartufo'), alg='1-7-8', abb=T_CUVEE),
    d('La Porcina', 'Pomodoro San Marzano dop, fior di latte e porcini tartufati', 12,
      sale=(PST, 'La Porcina-'), sheet=(sPST, 'La Porcina'), alg='1-7', abb=T_ZIZ),
  ],
  gourmet=[
    d('Gialla di Cetara', 'Bianca, pomodorini gialli, burrata andriese e alici di Cetara', 11, sale=(PGT, 'Gialla di Cetara-'), sheet=(sPGT, 'Gialla di Cetara'), alg='1-4-7', abb=T_FAL),
    d('La Carbonara', 'Bianca, guanciale, tuorlo d\'uovo, pecorino e pepe', 11, sale=(PGT, 'Carbonara-'), sheet=(sPGT, 'Carbonara'), alg='1-3-7', abb=T_PEC),
    d('La Gustosa', 'Bianca, pacchetelle del Piennolo, burrata andriese e trito di noci', 11, sale=(PGT, 'La Gustosa'), sheet=(sPGT, 'La Gustosa'), alg='1-7-8', abb=T_PAS),
    d('La Fratoni', 'Bianca, zucca, provola e guanciale', 12, sale=(PGT, 'La Fratoni'), sheet=(sPGT, 'La Fratoni'), alg='1-7', abb=T_KELL),
    d('La Calabrese', 'Pomodoro, fior di latte, porcini e \'nduja', 12, sale=(PST, 'La Calabrese-'), sheet=(sPST, 'La Calabrese'), alg='1-7', abb=T_IPA),
    d('Del Contadino', 'Bianca, gorgonzola, pere e trito di noci', 11, sale=(PST, 'Del Contadino'), sheet=(sPST, 'Del Contadino'), alg='1-7-8', abb=T_TRA),
  ],
  speciali=[
    d('\'Nduja', 'Prosciutto crudo, burrata e \'nduja di Spilinga', 10, sale=(PST, 'Nduja-'), sheet=(sPST, 'Nduja'), alg='1-7', abb=T_IPA),
    d('Porcini & guanciale', 'Bianca, porcini e guanciale', 12, sale=(PST, 'Porcini e Guanciale'), sheet=(sPST, 'Porcini e Guanciale'), alg='1-7', abb=T_BRUN),
    d('Amatriciana', 'Guanciale, pecorino romano e pepe', 9, sale=(PST, 'Amatriciana-'), sheet=(sPST, 'Amatriciana'), alg='1-7', abb=T_KELL),
    d('La Tropea', 'Bianca, bufala andriese, olive taggiasche, pomodorini gialli e cipolla di Tropea', 11, sale=(PST, 'La Tropea-'), sheet=(sPST, 'La Tropea'), alg='1-7', abb=T_BLON),
    d('Salsiccia & friarielli', 'Bianca, fior di latte, salsiccia e friarielli', 10, sale=(PGT, 'Salsiccia e Friarielli'), alg='1-7', abb=T_KELL),
    d('Salamino & porcini', 'Salamino piccante e funghi porcini', 10, sale=(PCT, 'Salamino e Porcini-'), alg='1-7', abb=T_BRUN),
  ],
  calzoni=[
    d('Calzone classico', 'Mozzarella, prosciutto cotto e pomodoro', 8.5, sale=(CZT, 'Calzone Classico'), sheet=(sCZT, 'Calzone Classico'), alg='1-7', abb=T_HELL),
    d('Calzone farcito', 'Mozzarella, olive, carciofi, würstel, prosciutto cotto, funghi e pomodoro', 9, sale=(CZT, 'Calzone Farcito-'), sheet=(sCZT, 'Calzone Farcito'), alg='1-7', abb=T_KELL),
    d('Covaccino 2.0', 'Crudo, burrata e pomodorini confit', 10, sale=(CZT, 'Covaccino 2.0'), sheet=(sCZT, 'Covaccino 2.0'), alg='1-7', abb=T_BLON),
    d('Mascalzone', 'Metà pizza con salsiccia e stracchino, metà calzone con prosciutto cotto e provola', 9, sale=(PCT, 'Mascalzone-'), sheet=(sPCT, 'Mascalzone'), alg='1-7', abb=T_KELL),
  ],
  dolci=[
    d('Degustazione Cartabianca', 'I dolci della nostra pasticceria in assaggio, da dividere', 10, sale=(DT, 'Degustazione Cartabianca'), sheet=(DT, 'Degustazione Cartabianca'), alg='1-3-7-8', abb=T_PROS, foto=True),
    d('Sfogliatina di mele calda', 'Profumata alla cannella, con composta di frutti di bosco', 8, sale=(DT, 'Sfogliatina di Mele'), sheet=(DT, 'Sfogliatina di Mele'), alg='1-3-7', foto=True),
    d('Millefoglie', 'Sfoglia caramellata della nostra pasticceria, crema chantilly e frutti di bosco freschi', 7, sale=(DT, 'Millefoglie Scomposto'), sheet=(DT, 'Millefoglie Scomposto'), alg='1-3-7', foto=True),
    d('Crème brûlée', 'Profumata all\'arancia, zucchero caramellato', 7, sale=(DT, 'Creme Brulè'), sheet=(DT, 'Creme Brulè'), alg='3-7'),
    d('Calzoncino alla Nutella', 'Cotto a legna, zucchero a velo', 7, sale=(DT, 'Calzoncino Nutella'), sheet=(DT, 'Calzoncino Nutella'), alg='1-7-8'),
    d('Cheesecake', 'Di nostra produzione: frutti di bosco, cioccolato fondente o arance amare', 7, sale=(DT, 'Cheesecake'), sheet=(DT, 'Cheesecake'), alg='1-3-7'),
    d('Tiramisù', 'Mascarpone, caffè, savoiardi e cacao', 7, sale=(DT, 'Tiramisù'), sheet=(DT, 'Tiramisù'), alg='1-3-7'),
  ],
  fuori_dolci=[
    d('Delizia al cioccolato', '', 7, sale=(DT, 'Delizia Cioccolato'), motivo='food cost 31,6%: chi la sceglieva va su dolci che rendono 1-2 € in più'),
    d('Profiterole', '', 7, sale=(DT, 'Profiterole'), motivo='food cost 32,4%, il più alto dei dolci'),
    d('Selezione di mignon', '', 7, sale=(DT, 'Selezione Mignon'), motivo='DOG'),
    d('Bavarese al mascarpone', '', 7, sale=(DT, 'Bavarese'), motivo='17 pezzi in 6 mesi'),
    d('Crem caramel', '', 7, sale=(DT, 'Crem Caramel'), motivo='7 pezzi in 6 mesi'),
  ],
  sorbetto=d('Sorbetto al limone', 'Al naturale · con prosecco o vodka 7,50', 5, sale=(DT, 'Sorbetto Limone al Naturale'), sheet=(DT, 'Sorbetto Limone al Naturale')),
  amari=[('Amaro', 4, 4.5), ('Limoncello', 4, 4.5), ('Amaro Jefferson', 5, 5.5), ('Grappa Of Amarone barrique', 6, 7),
         ('Liquore Of Dorange', 6, 6), ('Whisky', 5, 5), ('Rhum Zacapa 23 anni', 7, 7)],
  amari_q6={'Amaro': 723, 'Limoncello': 237, 'Amaro Jefferson': 123, 'Grappa Of Amarone barrique': 235},
  caffe=[('Caffè Fiorenero 100% arabica', 2), ('Decaffeinato', 2.5), ('Caffè d\'orzo', 3), ('Ginseng', 2.5)],
  acque=[('Acqua 0,75', 2.5), ('Bibita in lattina', 3.5)],
  coperto_q6=1596, coperto_ric6=1446,
)

# =====================================================================
#  CARTABIANCA CLUB · SAN MAURO
# =====================================================================
AC, PC, SC, CC = 'ANTIPASTI MARZ25', 'PRIMI MARZ25', 'SECONDI MARZ25', 'CONTORNI OTTOBRE 2024'
PCC, PGC, PSC, CZC, DC = ('PIZZE CLASSICHE MARZ25', 'PIZZE GOURMET MARZ25', 'PIZZE SPECIALI MARZ25',
                          'CALZONI E COVACCINI MARZ25', 'Dessert Ristorante')
sAC, sPC, sSC, sCC = 'Antipasti Marz25', 'Primi Marz25', 'Secondi Marz25', 'Contorni Ottobre 2024'
sPCC, sPGC, sPSC, sCZC = 'Pizze Classiche Marz25', 'Pizze Gourmet Marz25', 'Pizze Speciali Marz25', 'Calzoni E Covaccini Ma'

CLUB = dict(
  sigla='CLUB', nome='Cartabianca Club', luogo='San Mauro a Signa',
  pomodoro='pomodoro 100% italiano',
  indirizzo='Via del Pozzo Rosso 2/V · 50058 San Mauro a Signa · 055 8737037',
  coccoli_fc=3.49,
  premium_antipasti=[],
  antipasti=[
    d('Tagliere del Club', 'Selezione di salumi, assaggi di pecorino stagionato e pesche caramellate', 12,
      sale=(AC, 'Tagliere del Club'), sheet=(sAC, 'Tagliere del Club'), alg='1-7', abb=C_ZIZ),
    d('Bruschette Cartabianca', 'Salsiccia e stracchino; pomodorini gialli, rossi e basilico; stracciatella e polvere di speck; lardo al rosmarino', 10,
      sale=(AC, 'Bruschette del Club'), sheet=(sAC, 'Bruschette del Club'), alg='1-7', abb=C_ZIZ),
    d('Coccoli artigianali', 'Con prosciutto crudo e stracchino montato', 11,
      sale=(AC, 'Coccoli Crudo e Stracchino'), sheet=(sAC, 'Coccoli Crudo e Stracchino'), alg='1-7', abb=C_TRIP),
    d('Tartare di tonno', 'Su mango, lime e terra di taralli al peperoncino', 15,
      sale=(AC, 'Tartare di Tonno'), alg='1-4', abb=C_TRA),
    d('Frittino di acciughe e fiori', 'Fritto al momento', 14,
      sale=(AC, 'Frittino Acciughe e Fiori'), alg='1-4', abb=C_PAS),
    d('Gamberoni in pasta kataifi', 'Fritti, con la mayo Cartabianca', 13,
      sale=(AC, 'Gamberi Kataifi'), sheet=(sAC, 'Gamberi Kataifi'), alg='1-2-3', abb=C_PEC),
  ],
  fuori_antipasti=[
    d('Carpaccio di manzo', '', 12, sale=(AC, 'Carpaccio di Manzo'), motivo='DOG: 13 pezzi in 6 mesi, food cost 43,5%'),
    d('Tiepido di mare', '', 14, sale=(AC, 'Tiepido di Mare'), motivo='DOG: food cost 48%, 6,59 € di margine su 14 €'),
  ],
  premium_primi=[
    d('Chicche di patate al sugo di scampi', 'Tartare di scampo crudo al naturale e stracciatella', 15,
      sale=(PC, 'Chicche Scampi'), sheet=(sPC, 'Chicche Scampi'), alg='1-2-3-7', abb=C_TRA),
    d('Risotto al Franciacorta', 'Zafferano e polvere di liquirizia', 15,
      sale=(PC, 'Risotto Franciacorta'), alg='7-9-12', abb=C_PEC),
    d('Linguine alle vongole veraci', 'E bottarga di muggine', 15,
      sheet=(sPC, 'Linguine Vongole Bottarga'), card='Linguine Vongole Bottarga', q6=217, cls='PLOWHORSE', alg='1-4-14', abb=C_PAS),
  ],
  primi=[
    d('Spaghettoni al datterino giallo', 'Crema di datterino giallo, stracciatella e crumble di taralli al rosmarino', 14,
      sale=(PC, 'Spaghettoni Datterino Giallo Stracciatel'), alg='1-7', abb=C_PAS),
    d('Paccheri alla carbonara di mare', 'Frutti di mare e bocconcini di tonno rosso', 14,
      sale=(PC, 'Paccheri Carbonara di Mare'), sheet=(sPC, 'Paccheri Carbonara di Mare'), alg='1-3-4-14', abb=C_TRA),
    d('Spaghetti quadrati allo scoglio', 'Lo scoglio Cartabianca', 14,
      sale=(PC, 'Spaghetti Scoglio'), sheet=(sPC, 'Spaghetti Scoglio'), alg='1-2-14', abb=C_PEC),
    d('Pici freschi cacio e pepe', 'Pecorino e pepe, niente altro', 13,
      sale=(PC, 'Pici Cacio e Pepe'), alg='1-7', abb=C_PAS),
  ],
  fuori_primi=[d('Trofie al pesto di zucchine', '', 13, sale=(PC, 'Trofie Zucchine e Crudo'), motivo='DOG: 21 pezzi, 6,88 € di margine')],
  premium_secondi=[
    d('Bistecca alla fiorentina', 'Polonia o Spagna, cotta sulla brace · al kg', 50,
      sale=(SC, 'Bistecca al kg'), per2=True, alg='', abb=C_ZIZ),
    d('Controfiletto di manzo', 'Battuta di pomodorini rossi e gialli, lardo di Colonnata e rucola', 17,
      sale=(SC, 'Controfiletto Manzo'), sheet=(sSC, 'Controfiletto Manzo'), alg='', abb=C_ZIZ),
    d('Tagliata di tonno', 'Salsa teriyaki e frutti di bosco', 17,
      sale=(SC, 'Tagliata di Tonno'), sheet=(sSC, 'Tagliata di Tonno'), alg='4-6', abb=C_TRA),
  ],
  secondi=[
    d('Frittura di mare', 'Calamari e gamberi su letto di verdure croccanti', 16,
      sale=(SC, 'Frittura Mare'), sheet=(sSC, 'Frittura Mare'), alg='1-2-14', abb=C_PAS),
    d('Tataki di pollo', 'In crosta di sesamo, caponatina di peperoni e olive taggiasche', 16,
      sale=(SC, 'Tataki di Pollo'), alg='11', abb=C_PEC),
    d('Spiedini di mazzancolle', 'Glassate al rum agricolo, insalatina di finocchi e arance', 16,
      sale=(SC, 'Spiedini di Mazzancolle'), alg='2', abb=C_TRA),
    d('Cartabianca Burger', 'Manzo 180 g, pane multicereali, bacon affumicato, scamorza, insalata, salsa Cartabianca e patate crispers', 15,
      sale=(SC, 'Cartabianca Burger'), sheet=(sSC, 'Cartabianca Burger'), alg='1-3-7-10-11', abb=C_KELL),
  ],
  contorni=[
    d('Patate fritte', '', 5, sale=(CC, 'Patate Fritte'), sheet=(sCC, 'Patate Fritte')),
    d('Verdure grigliate', '', 6, sale=(CC, 'Verdure Grigliate'), sheet=(sCC, 'Verdure Grigliate')),
    d('Patate arrosto', '', 5, sale=(CC, 'Patate arrosto'), sheet=(sCC, 'Patate arrosto')),
    d('Insalata mista', '', 5, sale=(CC, 'Insalata Mista')),
  ],
  fuori_contorni=[d('Insalata verde', '', 4, sale=(CC, 'Insalata Verde'), motivo='DOG')],
  classiche=[
    d('Margherita', 'Basilico fresco', 7.5, sale=(PCC, 'Margherita'), alg='1-7', abb=C_TRIP),
    d('Marinara', 'Aglio, origano e basilico fresco. Senza mozzarella', 7, sale=(PCC, 'Marinara'), alg='1', abb=C_TRIP),
    d('Napoli', 'Capperi, acciughe di Cetara, origano e basilico', 9, sale=(PCC, 'Napoli-'), alg='1-4-7', abb=C_WEIS),
    d('Bufala Dop', 'Bufala Barlotti dop al posto del fior di latte', 9, sale=(PCC, 'Bufala Dop'), alg='1-7', abb=C_WEIS),
    d('4 Formaggi', 'Gorgonzola, provola e stracchino', 9, sale=(PCC, '4 Formaggi-'), alg='1-7', abb=C_KELL),
    d('Vegetariana', 'Melanzane, zucchine e pomodorini', 9, sale=(PCC, 'Vegetariana-'), sheet=(sPCC, 'Vegetariana'), alg='1-7', abb=C_BLAN),
    d('Melanzane & provola', 'Melanzane al forno e provola', 9, sale=(PCC, 'Melanzane e Provola'), sheet=(sPCC, 'Melanzane e Provola'), alg='1-7', abb=C_TRIP),
  ],
  saporite=[
    d('Salamino', 'Salamino piccante', 8.5, sale=(PCC, 'Salamino-'), alg='1-7', abb=C_KELL),
    d('Würstel', 'Würstel', 8.5, sale=(PCC, 'Wurstel-'), sheet=(sPCC, 'Wurstel'), alg='1-7', abb=C_TRIP),
    d('Prosciutto & funghi', 'Prosciutto cotto e champignon', 9, sale=(PCC, 'Prosciutto e Funghi-'), alg='1-7', abb=C_TRIP),
    d('Capricciosa', 'Carciofi, olive, würstel, champignon e prosciutto cotto', 9, sale=(PCC, 'Capricciosa-'), sheet=(sPCC, 'Capricciosa'), alg='1-7', abb=C_KELL),
    d('4 Stagioni', 'Carciofi, olive, champignon e prosciutto cotto', 9, sale=(PCC, '4 Stagioni'), sheet=(sPCC, '4 Stagioni'), alg='1-7', abb=C_KELL),
    d('Salsiccia & cipolla', 'Salsiccia e cipolla', 9, sale=(PCC, 'Salsiccia e Cipolla-'), sheet=(sPCC, 'Salsiccia e Cipolla'), alg='1-7', abb=C_KELL),
    d('Maialona', 'Prosciutto cotto, salsiccia, salamino e würstel', 9, sale=(PCC, 'Maialona-'), sheet=(sPCC, 'Maialona'), alg='1-7', abb=C_BRUN),
  ],
  fuori_pizze=[
    d('Tonno & cipolla', '', 9, sale=(PCC, 'Tonno e Cipolla'), motivo='DOG: food cost 41%'),
    d('Parmigiana', '', 9, sale=(PCC, 'Parmigiana'), motivo='DOG'),
    d('Dolce Parma', '', 9, sale=(PGC, 'Dolce Parma'), motivo='DOG tra le gourmet'),
    d('Pescatora', '', 12, sale=(PSC, 'Pescatora-'), motivo='DOG: food cost 64%'),
    d('La Stracchina', '', 9, sale=(PSC, 'La Stracchina'), motivo='DOG: food cost 40%'),
  ],
  tartufate=[
    d('La Tartufina', 'Pomodoro 100% italiano, bufala Barlotti dop e tartufo nero', 14,
      sale=(PSC, 'Tartufina'), sheet=(sPSC, 'Tartufina'), alg='1-7', abb=C_ZIZ),
    d('La Mortazza & Tartufo', 'Bianca con fior di latte, mortadella, scaglie di tartufo e crema di parmigiano', 14,
      sale=(PSC, 'La Mortazza e Tartufo-'), sheet=(sPSC, 'La Mortazza e Tartufo'), alg='1-7-8', abb=C_PEC),
    d('La Porcina', 'Pomodoro 100% italiano, fior di latte e porcini tartufati', 12,
      sale=(PSC, 'La Porcina-'), sheet=(sPSC, 'La Porcina'), alg='1-7', abb=C_ZIZ),
  ],
  gourmet=[
    d('Gialla di Cetara', 'Bianca, pomodorini gialli, olive taggiasche, stracciatella Maldera e alici di Cetara', 11, sale=(PGC, 'Gialla di Cetara-'), sheet=(sPGC, 'Gialla di Cetara'), alg='1-4-7', abb=C_PAS),
    d('La Carbonara', 'Bianca, guanciale, tuorlo d\'uovo, pecorino e pepe', 11, sale=(PGC, 'Carbonara-'), sheet=(sPGC, 'Carbonara'), alg='1-3-7', abb=C_PEC),
    d('La Gustosa', 'Bianca, pomodorino giallo, stracciatella Maldera e trito di noci', 11, sale=(PGC, 'La Gustosa'), sheet=(sPGC, 'La Gustosa'), alg='1-7-8', abb=C_PAS),
    d('Gricia', 'Bianca, cipolla, guanciale, crema di pecorino e pepe', 10, sale=(PGC, 'Gricia'), sheet=(sPGC, 'Gricia'), alg='1-7', abb=C_KELL),
    d('Del Contadino', 'Bianca, gorgonzola, pere e trito di noci', 11, sale=(PSC, 'Del Contadino'), sheet=(sPSC, 'Del Contadino'), alg='1-7-8', abb=C_TRA),
  ],
  speciali=[
    d('\'Nduja', 'Prosciutto crudo, stracciatella Maldera e \'nduja di Spilinga', 10, sale=(PSC, 'Nduja-'), sheet=(sPSC, 'Nduja'), alg='1-7', abb=C_KELL),
    d('Porcini & guanciale', 'Bianca, porcini e guanciale', 12, sale=(PSC, 'Porcini e Guanciale'), sheet=(sPSC, 'Porcini e Guanciale'), alg='1-7', abb=C_BRUN),
    d('La Calabrese', 'Salamino e \'nduja', 12, sale=(PSC, 'Calabrese'), sheet=(sPSC, 'Calabrese'), alg='1-7', abb=C_KELL),
    d('La Tropea', 'Bianca, olive taggiasche, pomodorini gialli e cipolla di Tropea', 11, sale=(PSC, 'La Tropea-'), sheet=(sPSC, 'La Tropea'), alg='1-7', abb=C_BLAN),
    d('La Piccante', 'Salamino piccante e stracciatella Maldera', 10, sale=(PSC, 'La Piccante-'), sheet=(sPSC, 'La Piccante'), alg='1-7', abb=C_KELL),
    d('Amatriciana', 'Guanciale, pecorino romano e pepe', 9, sale=(PSC, 'Amatriciana-'), sheet=(sPSC, 'Amatriciana'), alg='1-7', abb=C_KELL),
    d('Salamino & porcini', 'Salamino piccante e funghi porcini', 10, sale=(PCC, 'Salamino e Porcini-'), alg='1-7', abb=C_BRUN),
  ],
  calzoni=[
    d('Calzone classico', 'Mozzarella, prosciutto cotto e pomodoro', 8.5, sale=(CZC, 'Calzone Classico'), sheet=(sCZC, 'Calzone Classico'), alg='1-7', abb=C_TRIP),
    d('Calzone farcito', 'Mozzarella, olive, carciofi, würstel, prosciutto cotto, funghi e pomodoro', 9, sale=(CZC, 'Calzone Farcito-'), sheet=(sCZC, 'Calzone Farcito'), alg='1-7', abb=C_KELL),
    d('Covaccino 2.0', 'Crudo, stracciatella Maldera e pomodorini gialli del Piennolo', 10, sale=(CZC, 'Covaccino 2.0'), sheet=(sCZC, 'Covaccino 2.0'), alg='1-7', abb=C_BLAN),
    d('Portafoglio', 'Bianca con fior di latte, rucola, crudo e crema di parmigiano', 10, sale=(CZC, 'Portafoglio'), sheet=(sCZC, 'Portafoglio'), alg='1-7', abb=C_TRIP),
    d('Mascalzone', 'Metà pizza con salsiccia e stracchino, metà calzone con prosciutto cotto e provola', 9, sale=(PCC, 'Mascalzone-'), sheet=(sPCC, 'Mascalzone'), alg='1-7', abb=C_KELL),
  ],
  dolci=[
    d('Sfogliatina di mele calda', 'Profumata alla cannella, con composta di frutti di bosco', 7.5, sale=(DC, 'Sfogliatina Mele'), sheet=(DC, 'Sfogliatina Mele'), alg='1-3-7', foto=True, era='venduta ma non scritta in carta'),
    d('Millefoglie', 'Sfoglia caramellata della nostra pasticceria, crema chantilly e frutti di bosco freschi', 7, sale=(DC, 'Millefoglie Scomposto'), sheet=(DC, 'Millefoglie Scomposto'), alg='1-3-7', foto=True),
    d('Crème brûlée', 'Profumata all\'arancia, zucchero caramellato', 7, sale=(DC, 'Creme Brulee'), sheet=(DC, 'Creme Brulee'), alg='3-7', foto=True),
    d('Calzoncino alla Nutella', 'Cotto a legna, zucchero a velo', 7, sale=(CZC, 'Calzoncino Nutella'), sheet=(sCZC, 'Calzoncino Nutella'), alg='1-7-8'),
    d('Tiramisù', 'Crema di mascarpone, caffè, savoiardi e cacao', 7, sale=(DC, 'Tiramisù'), sheet=(DC, 'Tiramisù'), alg='1-3-7'),
    d('Cheesecake', 'Di nostra produzione: frutti di bosco, cioccolato fondente o arance amare', 7, sale=(DC, 'Cheesecake'), sheet=(DC, 'Cheesecake'), alg='1-3-7'),
    d('Delizia al cioccolato', 'Tortino al cioccolato con cuore morbido', 7, sale=(DC, 'Delizia Cioccolato'), sheet=(DC, 'Delizia Cioccolato'), alg='1-3-7'),
  ],
  fuori_dolci=[
    d('La Contessa', '', 6, sale=(DC, 'La Contessa'), motivo='4,75 € di margine, sotto tutti gli altri'),
    d('Profiterole', '', 7, sale=(DC, 'Profiterole'), motivo='food cost 32,4%'),
    d('Selezione di mignon', '', 7, sale=(DC, 'Selezione Mignon'), motivo='DOG'),
  ],
  sorbetto=d('Sorbetto al limone', 'Al naturale · con prosecco o vodka 7,50', 5, sale=(DC, 'Sorbetto Limone'), sheet=(DC, 'Sorbetto Limone')),
  amari=[('Amaro', 4, 4.5), ('Limoncello', 4, 4.5), ('Grappa Of Amarone barrique', 6, 7),
         ('Liquore Of Dorange', 6, 6), ('Whisky', 5, 5), ('Rhum Zacapa 23 anni', 7, 7)],
  amari_q6={'Amaro': 342, 'Limoncello': 222, 'Grappa Of Amarone barrique': 99},
  caffe=[('Caffè Fiorenero 100% arabica', 2), ('Decaffeinato', 2.5), ('Caffè d\'orzo', 3), ('Ginseng', 2.5)],
  acque=[('Acqua 0,75', 2.5), ('Bibita in lattina', 3.5)],
  coperto_q6=3517, coperto_ric6=3220,
)


# =====================================================================
#  REVISIONE 03/10/2026 sera (richieste Marco): libro da 8 facciate + carta dolci a parte,
#  sezioni che alzano il margine medio, descrizioni che valorizzano i piatti da spingere.
# =====================================================================
def _togli(L, da, nome, a, motivo):
    x = [p for p in L[da] if p['nome'] == nome][0]
    L[da].remove(x)
    if a:
        L.setdefault(a, []).append(dict(x, motivo=motivo))
    return x


def _sposta(L, da, nome, a):
    x = [p for p in L[da] if p['nome'] == nome][0]
    L[da].remove(x)
    L[a].append(x)


# calzoni e covaccini: sezione tolta (margine medio 6,5 €, il più basso delle pizze); il migliore va tra le speciali
for _L in (TENNIS, CLUB):
    for _n in ('Calzone classico', 'Calzone farcito', 'Mascalzone'):
        _togli(_L, 'calzoni', _n, 'fuori_pizze', 'sezione calzoni tolta: margine sotto la media delle pizze')
    _togli(_L, 'tartufate', 'La Mortazza & Tartufo', 'fuori_pizze', 'tartufata col margine più basso e meno venduta')
_sposta(TENNIS, 'calzoni', 'Covaccino 2.0', 'speciali')
_sposta(CLUB, 'calzoni', 'Portafoglio', 'speciali')
_togli(CLUB, 'calzoni', 'Covaccino 2.0', 'fuori_pizze', 'sezione calzoni tolta: tra le speciali resta il Portafoglio, che rende di più')
_togli(CLUB, 'speciali', 'Salamino & porcini', 'fuori_pizze', 'il margine più basso delle speciali (food cost 32%)')
_togli(TENNIS, 'gourmet', 'La Gustosa', 'fuori_pizze', 'DOG: margine e vendite sotto la media delle gourmet')
_togli(CLUB, 'dolci', 'Delizia al cioccolato', 'fuori_dolci', 'il margine più basso dei dolci (food cost 32%)')
# Club: le linguine (food cost 43%) escono dai primi della casa e vanno nella lista normale
_sposta(CLUB, 'premium_primi', 'Linguine alle vongole veraci', 'primi')

# descrizioni: più ricche sui piatti da spingere (n.1 per margine, premium, puzzle). Da far validare alla cucina.
DESCR = {
  'Selezione Cartabianca di terra': 'Il giro completo dei nostri antipasti di terra, al centro del tavolo',
  'Selezione Cartabianca di mare': 'Tutti i nostri antipasti di mare cotti, da dividere',
  'Selezione Cartabianca di mare con crudo': 'Il mare cotto insieme ai crudi e ai marinati del giorno',
  'Battuta di scottona': 'Scottona battuta al coltello, tuorlo d\'uovo fritto, burrata e scaglie di tartufo',
  'Tris di cruditè': 'Tartare di tonno con teriyaki e frutti di bosco, salmone con chips e crema di topinambur, tartare di gamberi con burrata e pistacchi',
  'Gamberoni in pasta kataifi': 'Avvolti nella pasta kataifi e fritti al momento, croccanti fuori e morbidi dentro, con la mayo Cartabianca',
  'Frittino di acciughe e fiori': 'Acciughe e fiori fritti al momento, leggeri e dorati',
  'Risotto mantecato al Castelmagno': 'Mantecato al Castelmagno, con tartare e jus di manzo, zucca confit e scaglie di tartufo',
  'Fregola "in nero"': 'Fregola con lo stracotto di seppie al loro nero e la crema di burrata di Andria',
  'Pacchero al ragù di cinghiale': 'Ragù di cinghiale, crumble di cacao amaro e nocciole alle erbe',
  'Paccheri alla carbonara di mare': 'La carbonara rifatta col mare: frutti di mare e bocconcini di tonno rosso',
  'Spaghettoni al datterino giallo': 'Crema di datterino giallo, stracciatella fresca e crumble di taralli al rosmarino',
  'Risotto al Franciacorta': 'Sfumato al Franciacorta, con zafferano e polvere di liquirizia',
  'Bistecca alla fiorentina': None,   # tenuta per locale (sotto)
  'Frittura di mare': 'Calamari e gamberi fritti al momento, su un letto di verdure croccanti',
  'Tataki di pollo': 'Petto di pollo in crosta di sesamo, scottato e affettato, con caponatina di peperoni e olive taggiasche',
  'Vegetariana': 'Melanzane, zucchine e pomodorini sul nostro impasto',
  'Maialona': 'Per chi ha fame: prosciutto cotto, salsiccia, salamino e würstel',
  'Capricciosa': 'Carciofi, olive, würstel, champignon e prosciutto cotto: la classica come si deve',
  'La Calabrese': 'Pomodoro, fior di latte, porcini e \'nduja piccante',
  'Gialla di Cetara': None,
  'La Tropea': None,
  'Covaccino 2.0': 'Il covaccino del forno a legna, con crudo, burrata e pomodorini confit',
  'Portafoglio': 'La pizza piegata a portafoglio: fior di latte, rucola, crudo e crema di parmigiano',
  'La Tartufina': None,
  'Degustazione Cartabianca': 'Un assaggio di tutti i dolci della nostra pasticceria, da dividere',
  'Sfogliatina di mele calda': 'Appena sfornata, profumata alla cannella, con composta di frutti di bosco',
  'Millefoglie': 'Sfoglia caramellata della nostra pasticceria, crema chantilly e frutti di bosco freschi',
}
for _L in (TENNIS, CLUB):
    for _k, _v in _L.items():
        if isinstance(_v, list):
            for _p in _v:
                if isinstance(_p, dict) and DESCR.get(_p.get('nome')):
                    _p['desc'] = DESCR[_p['nome']]
for _p in TENNIS['premium_secondi']:
    if _p['nome'] == 'Bistecca alla fiorentina':
        _p['desc'] = 'La regina della brace, al sangue come vuole la tradizione toscana · al kg'
for _p in TENNIS['speciali']:
    if _p['nome'] == 'La Tropea':
        _p['desc'] = 'Bianca con bufala andriese, olive taggiasche, pomodorini gialli e cipolla rossa di Tropea'
# ingredienti per la riga «perché la nostra pizza» (solo quelli già scritti nelle carte di oggi)
TENNIS['ingredienti'] = [('Forno', 'a legna'), ('Pomodoro', 'San Marzano dop'),
                         ('Mozzarella', 'fior di latte'), ('Bufala', 'andriese dop'), ('Alici', 'di Cetara')]
CLUB['ingredienti'] = [('Forno', 'a legna'), ('Pomodoro', '100% italiano'),
                       ('Mozzarella', 'fior di latte'), ('Bufala', 'Barlotti dop'), ('Stracciatella', 'Maldera')]


# =====================================================================
#  REVISIONE 2 (03/10 sera) — regole della presentazione «5 step per un menu wow»:
#  meno pizze classiche (una lista sola da 7), meno elementi di contorno.
# =====================================================================
TENIAMO_CLASSICHE = {
    'TENNIS': ['Maialona', 'Vegetariana', 'Würstel', 'Capricciosa', 'Melanzane & provola', 'Bufala Dop', 'Margherita'],
    'CLUB':   ['Vegetariana', 'Capricciosa', 'Melanzane & provola', 'Maialona', 'Würstel', 'Bufala Dop', 'Margherita'],
}
for _L in (TENNIS, CLUB):
    _tutte = _L['classiche'] + _L['saporite']
    _tieni = TENIAMO_CLASSICHE[_L['sigla']]
    _L['classiche'] = [p for p in _tutte if p['nome'] in _tieni]
    _L['saporite'] = []
    for p in _tutte:
        if p['nome'] not in _tieni:
            _L['fuori_pizze'].append(dict(p, motivo='classica tolta: una lista sola da 7, restano quelle che rendono di più + Margherita e Bufala che tutti cercano'))


# =====================================================================
#  REVISIONE 3 (03/10 sera) — prezzi premium veri sui piatti della casa (22-28),
#  costruiti con ingredienti che la cucina già compra (listino «Prezzi ingredienti» del file 02).
#  Food cost IVA esclusa, a porzione. Tutti «proposta RBR, da validare con la cucina».
# =====================================================================
def _prem(nome, desc, prezzo, fc, abb, alg, conto):
    return d(nome, desc, prezzo, alg=alg, abb=abb, fc=fc, cls='NUOVO', proposta=True, conto=conto)

P_CASTEL = _prem('Risotto al Castelmagno e tartufo nero', 'Mantecato al Castelmagno, tartare e jus di manzo, zucca confit e tartufo nero a lamelle', 22, 3.40, T_CER, '7-9-12',
                 'ricetta di oggi 1,94 + 8 g di tartufo nero 1,16 + jus 0,30')
P_TARTUFO = _prem('Tagliolini al tartufo nero', 'Tagliolini freschi in fonduta di grana, guanciale croccante e tartufo nero grattato al momento', 22, 3.20, T_CER, '1-3-7',
                  'tagliolini 0,60 + grana e fonduta 0,85 + guanciale 0,32 + 8 g tartufo 1,16 + altro 0,27')
P_SCAMPI_R = _prem('Risotto agli agrumi con scampi', 'Zafferano e agrumi, scampi interi scottati e la tartare di scampo crudo sopra', 23, 7.00, T_CUVEE, '2-7-9',
                   'ricetta di oggi 3,53 + 2 scampi interi 2,25 + 30 g tartare di scampo 1,24')
P_SCAMPI_C = _prem('Chicche di patate agli scampi', 'Chicche fatte da noi, sugo di scampi, scampi interi scottati, tartare di scampo e stracciatella', 22, 6.10, C_TRA, '1-2-3-7',
                   'ricetta di oggi 3,84 + 2 scampi interi 2,25')
S_CONTRO = _prem('Tagliata di controfiletto al sale Maldon', 'Controfiletto di manzo 250 g alla brace, sale Maldon, rosmarino e patate al forno', 26, 6.80, T_ZIZ, '',
                 'controfiletto 270 g lordi a 22,95 €/kg = 6,20 + patate e rosmarino 0,60')
S_GRIGLIA = _prem('Grigliata di mare', 'Scampi, gamberoni, calamaro e polpo alla griglia, con olio buono e limone', 28, 11.10, T_CUVEE, '2-14',
                  'scampi 150 g 3,38 + gamberi 120 g 1,44 + calamaro 3,04 + polpo 2,41 + altro 0,83')

# Tennis: primi della casa nuovi; i due di prima scendono nella lista della pasta
_vecchi = TENNIS['premium_primi']
TENNIS['premium_primi'] = [P_CASTEL, P_TARTUFO, P_SCAMPI_R]
TENNIS['primi'] += [p for p in _vecchi if 'Castelmagno' not in p['nome']]
# Tennis: grandi secondi = fiorentina + tagliata di controfiletto + grigliata; tagliata di scottona e tonno nella lista
_fior = [p for p in TENNIS['premium_secondi'] if 'fiorentina' in p['nome']]
TENNIS['secondi'] += [p for p in TENNIS['premium_secondi'] if 'fiorentina' not in p['nome']]
TENNIS['premium_secondi'] = _fior + [S_CONTRO, S_GRIGLIA]
_togli(TENNIS, 'secondi', 'Filetto di baccalà in olio cottura', 'fuori_contorni', 'nuovo, mai venduto, il margine più basso dei secondi (lista a 7)')
# Club
_vecchi = CLUB['premium_primi']
CLUB['premium_primi'] = [dict(P_CASTEL, abb=C_PEC), dict(P_TARTUFO, abb=C_ZIZ), P_SCAMPI_C]
CLUB['primi'] += [p for p in _vecchi if 'Chicche' not in p['nome']]
_fior = [p for p in CLUB['premium_secondi'] if 'fiorentina' in p['nome']]
CLUB['secondi'] += [p for p in CLUB['premium_secondi'] if 'Tagliata di tonno' in p['nome']]
CLUB['fuori_contorni'].append(dict([p for p in CLUB['premium_secondi'] if 'Controfiletto' in p['nome']][0],
                                   motivo='sostituito dalla Tagliata di controfiletto al sale Maldon (stessa carne, prezzo premium)'))
CLUB['premium_secondi'] = _fior + [dict(S_CONTRO, abb=C_ZIZ), dict(S_GRIGLIA, abb=C_PAS)]
# il percorso: nuovo nome e prezzo
for _L in (TENNIS, CLUB):
    _L['percorso'] = dict(nome='Fidatevi di noi', prezzo=29)
_togli(TENNIS, 'secondi', 'Tagliata di scottona alla griglia', 'fuori_contorni', 'doppione della Tagliata di controfiletto premium (26): chi la ordinava passa a quella, che rende 4 € in più')
_togli(TENNIS, 'contorni', "Fagioli all'uccelletta", 'fuori_contorni', 'il contorno che rende meno (3,75 €), mai venduto: contorni a 4, due colonne pulite')


# =====================================================================
#  REVISIONE 4 (03/10 sera) — richieste Marco v6
# =====================================================================
for _L in (TENNIS, CLUB):
    _L['percorso'] = dict(nome='Carta bianca allo chef', prezzo=29)
    for _p in _L['tartufate']:   # più valore alle tartufate: prezzo sopra il foglio definitivo (proposta RBR)
        if _p['nome'] == 'La Tartufina':
            _p['nuovo_prezzo'] = 17
        if _p['nome'] == 'La Porcina':
            _p['nuovo_prezzo'] = 15
TENNIS['tartufate'][0]['desc'] = 'Pomodoro San Marzano dop, bufala andriese dop e tartufo nero a lamelle'
TENNIS['tartufate'][1]['desc'] = 'Pomodoro San Marzano dop, fior di latte e porcini trifolati al tartufo nero'
CLUB['tartufate'][0]['desc'] = 'Pomodoro 100% italiano, bufala Barlotti dop e tartufo nero a lamelle'
CLUB['tartufate'][1]['desc'] = 'Pomodoro 100% italiano, fior di latte e porcini trifolati al tartufo nero'
TENNIS['nome_cop'], TENNIS['indirizzo_cop'] = 'Cartabianca Tennis Club', 'Via degli Scarpettini 39/A · Sesto Fiorentino'
CLUB['nome_cop'], CLUB['indirizzo_cop'] = 'Cartabianca Club', 'Via del Pozzo Rosso 2/V · San Mauro a Signa'
_togli(TENNIS, 'primi', 'Chicche di patate su vellutata di mare', 'fuori_primi', 'nuovo, mai venduto, doppione del Risotto agli agrumi con scampi tra i primi d’autore')


# =====================================================================
#  REVISIONE 5 (03/10 sera) — descrizioni che danno valore, corte e oneste (solo ingredienti già in ricetta)
# =====================================================================
DESCR2 = {
  'Selezione Cartabianca di terra': 'Il giro completo dei nostri antipasti di terra, da dividere',
  'Selezione Cartabianca di mare': 'Tutti i nostri antipasti di mare cotti, da dividere',
  'Selezione Cartabianca di mare con crudo': 'Il mare cotto e i crudi del giorno, da dividere',
  'Tris di cruditè': 'Tartare di tonno con teriyaki e frutti di bosco, salmone con crema di topinambur, tartare di gamberi con burrata e pistacchi',
  'Battuta di scottona': 'Scottona battuta al coltello, tuorlo fritto croccante, burrata e scaglie di tartufo',
  'Zuppetta di moscardini alla Luciana': 'Moscardini in umido alla luciana, con polentine fritte croccanti',
  'Coccoli artigianali': 'Pasta lievitata fritta al momento, con prosciutto crudo e stracchino montato',
  'Polpo rosticciato': 'Cotto a bassa temperatura e rosticciato, su morbido di patate, terra di olive e capperi',
  'Tagliere CB': 'Salumi scelti, pecorino di Seggiano, miele millefiori e pappa al pomodoro con burrata',
  'Risotto al Castelmagno e tartufo nero': 'Mantecato al Castelmagno, con tartare e jus di manzo, zucca confit e tartufo nero',
  'Risotto agli agrumi con scampi': 'Zafferano e agrumi, scampi interi scottati e tartare di scampo crudo',
  'Fregola "in nero"': 'Fregola sarda, stracotto di seppie al nero e crema di burrata di Andria',
  'Gnudi di ricotta e spinaci': 'Fatti a mano da noi, su vellutata di salvia, con cialde di parmigiano e mais',
  'Spaghetti freschi alla carbonara': 'Spaghetti freschi artigianali, guanciale croccante, tuorlo e pecorino',
  'Linguine alle vongole veraci': 'Vongole veraci e bottarga di muggine grattugiata',
  'Pacchero al ragù di cinghiale': 'Ragù di cinghiale, crumble di cacao amaro e nocciole alle erbe',
  'Tagliata di controfiletto al sale Maldon': '250 g di controfiletto alla brace, sale Maldon, rosmarino e patate al forno',
  'Grigliata di mare': 'Scampi, gamberoni, calamaro e polpo alla griglia, olio extravergine e limone',
  'Tonno rosso marinato alla barbecue': 'Marinato alla barbecue in crosta di sesamo, su morbido di sedano rapa e cavolo nero',
  'Frittura di mare': 'Calamari e gamberi f
ritti al momento, su verdure croccanti',
  'Galletto al mattone': 'Cotto a bassa temperatura e finito sotto il mattone, con verdure al forno',
  'Cartabianca Burger': 'Manzo 180 g, pane multicereali, bacon affumicato, scamorza e salsa Cartabianca, con patate crispers',
  'Goulash di mare': 'Polpo, seppia e totano gigante in cacciucco leggero, con patate stufate',
  'La Fratoni': 'Bianca con zucca, provola e guanciale croccante',
  'La Carbonara': 'Bianca con guanciale croccante, tuorlo, pecorino e pepe nero',
  'Del Contadino': 'Bianca con gorgonzola, pere e noci: dolce e salato',
  'Porcini & guanciale': 'Bianca con porcini e guanciale croccante',
  'Amatriciana': 'Pomodoro, guanciale, pecorino romano e pepe',
  "'Nduja": "Prosciutto crudo, burrata e 'nduja piccante di Spilinga",
  'Capricciosa': 'Carciofi, olive, würstel, funghi e prosciutto cotto',
  'Vegetariana': 'Melanzane, zucchine e pomodorini',
  'Würstel': 'Pomodoro, fior di latte e würstel',
  'Margherita': 'Pomodoro, fior di latte e basilico fresco',
  'Maialona': 'Prosciutto cotto, salsiccia, salamino e würstel',
  'Crème brûlée': 'Crema all’arancia con la crosta di zucchero caramellato',
  'Calzoncino alla Nutella': 'Cotto nel forno a legna, ripieno di Nutella e spolverato di zucchero a velo',
  'Tiramisù': 'Savoiardi al caffè, crema al mascarpone e cacao amaro',
  # Club
  'Gamberoni in pasta kataifi': 'Avvolti nella pasta kataifi e fritti al momento, con la mayo Cartabianca',
  'Tagliere del Club': 'Salumi scelti, pecorino stagionato e pesche caramellate',
  'Chicche di patate agli scampi': 'Chicche fatte da noi, sugo di scampi, scampi interi, tartare di scampo e stracciatella',
  'Pici freschi cacio e pepe': 'Pici freschi, pecorino e pepe: niente altro',
  'Tagliata di tonno': 'Tonno scottato e tagliato, salsa teriyaki e frutti di bosco',
  'Tataki di pollo': 'Pollo in crosta di sesamo, scottato, con caponatina di peperoni e olive taggiasche',
  'La Gustosa': 'Bianca con pomodorino giallo, stracciatella Maldera e noci',
  'Gricia': 'Bianca con cipolla, guanciale croccante, crema di pecorino e pepe',
}
for _L in (TENNIS, CLUB):
    for _k, _v in _L.items():
        if isinstance(_v, list):
            for _p in _v:
                if isinstance(_p, dict) and _p.get('nome') in DESCR2:
                    _p['desc'] = DESCR2[_p['nome']]
for _p in TENNIS['classiche']:
    if _p['nome'] == 'Bufala Dop': _p['desc'] = 'Pomodoro San Marzano dop e bufala andriese dop'
for _p in CLUB['classiche']:
    if _p['nome'] == 'Bufala Dop': _p['desc'] = 'Pomodoro e bufala Barlotti dop'
for _p in TENNIS['premium_secondi']:
    if 'fiorentina' in _p['nome']: _p['desc'] = 'La regina della brace toscana, al sangue come vuole la tradizione · al kg'
for _p in CLUB['premium_secondi']:
    if 'fiorentina' in _p['nome']: _p['desc'] = 'Polonia o Spagna, sulla brace e al sangue · al kg'
for _p in TENNIS['gourmet']:
    if _p['nome'] == 'Gialla di Cetara': _p['desc'] = 'Bianca con pomodorini gialli, burrata andriese e alici di Cetara'
    if _p['nome'] == 'La Calabrese': _p['desc'] = "Pomodoro, fior di latte, porcini e 'nduja piccante"

for _L in (TENNIS, CLUB):
    _L['percorso'] = dict(nome='Cartabianca Experience', prezzo=45)


# =====================================================================
#  REVISIONE 6 (05/10) — MENU UNICO: Tennis e Club con esattamente gli stessi piatti (richiesta Marco).
#  Scelta su margine dei due locali insieme, max 7 per sezione. Se un piatto c'è in un solo locale,
#  nell'altro è «nuovo» (stesso food cost, venduto 0). Il prezzo si allinea in build.py (il più alto dei due).
# =====================================================================
import copy as _copy
UNICO = {
  'premium_antipasti': ['Selezione Cartabianca di terra', 'Selezione Cartabianca di mare', 'Selezione Cartabianca di mare con crudo'],
  'antipasti': ['Battuta di scottona', 'Gamberoni in pasta kataifi', 'Tris di cruditè', 'Tagliere CB',
                'Zuppetta di moscardini alla Luciana', 'Coccoli artigianali', 'Bruschette Cartabianca'],
  'premium_primi': ['Tagliolini al tartufo nero', 'Risotto al Castelmagno e tartufo nero', 'Risotto agli agrumi con scampi'],
  'primi': ['Linguine alle vongole veraci', 'Paccheri alla carbonara di mare', 'Spaghetti quadrati allo scoglio',
            'Pacchero al ragù di cinghiale', 'Fregola "in nero"', 'Gnudi di ricotta e spinaci', 'Spaghetti freschi alla carbonara'],
  'premium_secondi': ['Bistecca alla fiorentina', 'Tagliata di controfiletto al sale Maldon', 'Grigliata di mare'],
  'secondi': ['Frittura di mare', 'Tonno rosso marinato alla barbecue', 'Goulash di mare', 'Galletto al mattone',
              'Spiedino grigliato', 'Tataki di pollo', 'Cartabianca Burger'],
  'contorni': ['Patatine fritte', 'Verdure grigliate', 'Patate arrosto', 'Insalata di misticanza'],
  'classiche': ['Vegetariana', 'Capricciosa', 'Melanzane & provola', 'Maialona', 'Würstel', 'Bufala Dop', 'Margherita'],
  'tartufate': ['La Tartufina', 'La Porcina'],
  'gourmet': ['La Calabrese', 'La Fratoni', 'Gialla di Cetara', 'La Carbonara', 'Del Contadino', 'La Gustosa', 'Gricia'],
  'speciali': ['La Tropea', 'Porcini & guanciale', 'Portafoglio', "'Nduja", 'Covaccino 2.0', 'La Piccante', 'Amatriciana'],
  'dolci': ['Degustazione Cartabianca', 'Sfogliatina di mele calda', 'Millefoglie', 'Crème brûlée',
            'Calzoncino alla Nutella', 'Tiramisù', 'Cheesecake'],
}
SINONIMI = {'Tagliere del Club': 'Tagliere CB', 'Patate fritte': 'Patatine fritte', 'Verdure al forno': 'Verdure grigliate',
            'Insalata mista': 'Insalata di misticanza', 'Tagliata di tonno': 'Tonno rosso marinato alla barbecue',
            'Chicche di patate agli scampi': None}


def _tutti(L):
    out = {}
    for k, v in L.items():
        if isinstance(v, list):
            for p in v:
                if isinstance(p, dict) and 'nome' in p and 'old' in p:
                    out.setdefault(SINONIMI.get(p['nome'], p['nome']) or p['nome'], p)
    return out


_TT, _TC = _tutti(TENNIS), _tutti(CLUB)
for _L, _mio, _altro in ((TENNIS, _TT, _TC), (CLUB, _TC, _TT)):
    for _k, _nomi in UNICO.items():
        _vecchi = {p['nome'] for p in _L.get(_k, [])}
        _nuova = []
        for _n in _nomi:
            if _n in _mio:
                _p = dict(_mio[_n], nome=_n)
            else:
                _p = _copy.deepcopy(_altro[_n])
                if _p.get('sale'):
                    _p['q6'], _p['cls'] = 0, 'NUOVO'
                _p['nuovo_qui'] = True
            _nuova.append(_p)
        _L[_k] = _nuova
    _L['calzoni'], _L['saporite'] = [], []


# ---------- REVISIONE 7 (05/10): descrizioni più ricche (oneste: solo ingredienti già in ricetta) ----------
DESCR3 = {
  'Selezione Cartabianca di terra': 'Tutti i nostri antipasti di terra in un unico giro, da dividere al centro del tavolo',
  'Selezione Cartabianca di mare': 'Il meglio dei nostri antipasti di mare cotti, da condividere',
  'Selezione Cartabianca di mare con crudo': 'Il mare cotto insieme ai crudi e ai marinati del giorno, per chi vuole tutto',
  'Battuta di scottona': 'Scottona battuta al coltello, tuorlo fritto croccante, burrata cremosa e scaglie di tartufo',
  'Gamberoni in pasta kataifi': 'Gamberoni avvolti nella pasta kataifi e fritti al momento, croccanti fuori e succosi dentro, con la nostra mayo',
  'Tris di cruditè': 'Tartare di tonno con teriyaki e frutti di bosco, salmone con crema di topinambur, gamberi con burrata e pistacchi',
  'Tagliere CB': 'Salumi scelti, pecorino di Seggiano, miele millefiori e la nostra pappa al pomodoro con burrata',
  'Zuppetta di moscardini alla Luciana': 'Moscardini cotti in umido alla luciana, con polentine fritte croccanti da intingere',
  'Coccoli artigianali': 'Pasta lievitata fritta al momento, con prosciutto crudo e stracchino montato: si mangiano con le mani',
  'Bruschette Cartabianca': 'Pane toscano con salsiccia e stracchino, cavolo nero e pecorino; polentine con fegatini e funghi trifolati',
  'Tagliolini al tartufo nero': 'Tagliolini freschi in fonduta di grana, guanciale croccante e tartufo nero grattato al momento',
  'Risotto al Castelmagno e tartufo nero': 'Mantecato al Castelmagno, con tartare e jus di manzo, zucca confit e tartufo nero',
  'Risotto agli agrumi con scampi': 'Zafferano e agrumi, scampi interi appena scottati e tartare di scampo crudo',
  'Linguine alle vongole veraci': 'Vongole veraci aperte in padella e bottarga di muggine grattugiata al momento',
  'Paccheri alla carbonara di mare': 'La carbonara rifatta col mare: frutti di mare, tuorlo e bocconcini di tonno rosso',
  'Spaghetti quadrati allo scoglio': 'Spaghetti quadrati saltati con lo scoglio Cartabianca: i frutti di mare in un piatto solo',
  'Pacchero al ragù di cinghiale': 'Ragù di cinghiale cotto a lungo, crumble di cacao amaro e nocciole alle erbe',
  'Fregola "in nero"': 'Fregola sarda, stracotto di seppie al loro nero e crema di burrata di Andria',
  'Gnudi di ricotta e spinaci': 'Fatti a mano da noi con ricotta e spinaci, su vellutata di salvia, cialde di parmigiano e mais',
  'Spaghetti freschi alla carbonara': 'Spaghetti freschi artigianali, guanciale croccante, tuorlo e pecorino: la carbonara come si deve',
  'Tagliata di controfiletto al sale Maldon': '250 g di controfiletto di manzo alla brace, sale Maldon, rosmarino e patate al forno',
  'Grigliata di mare': 'Scampi, gamberoni, calamaro e polpo alla griglia, con olio extravergine e limone',
  'Frittura di mare': 'Calamari e gamberi fritti al momento, leggeri e dorati, su verdure croccanti',
  'Tonno rosso marinato alla barbecue': 'Tonno rosso marinato alla barbecue in crosta di sesamo, su morbido di sedano rapa e cavolo nero',
  'Goulash di mare': 'Polpo, seppia e totano gigante in un cacciucco leggero, con patate stufate',
  'Galletto al mattone': 'Cotto a bassa temperatura e finito sotto il mattone: pelle croccante, carne tenera, verdure al forno',
  'Spiedino grigliato': 'Pancia, filetto, salsiccia e coppa di suino grigio del Casentino alla griglia, con fagioli all’uccelletta',
  'Tataki di pollo': 'Pollo in crosta di sesamo, scottato e tagliato, con caponatina di peperoni e olive taggiasche',
  'Cartabianca Burger': 'Manzo 180 g, pane multicereali, bacon affumicato, scamorza e salsa Cartabianca, con patate crispers',
  'Vegetariana': 'Melanzane, zucchine e pomodorini sul nostro impasto, con fior di latte',
  'Capricciosa': 'Carciofi, olive, würstel, funghi e prosciutto cotto: la classica di sempre',
  'Melanzane & provola': 'Melanzane al forno e provola filante',
  'Maialona': 'Per chi ha fame: prosciutto cotto, salsiccia, salamino e würstel',
  'Würstel': 'Pomodoro, fior di latte e würstel',
  'Margherita': 'Pomodoro, fior di latte e basilico fresco: semplice e perfetta',
  'La Calabrese': "Pomodoro, fior di latte, porcini e 'nduja piccante: il sud in una pizza",
  'La Fratoni': 'Bianca con zucca, provola filante e guanciale croccante',
  'La Carbonara': 'Bianca con guanciale croccante, tuorlo, pecorino e pepe nero',
  'Del Contadino': 'Bianca con gorgonzola, pere e noci: dolce e salato insieme',
  'La Gustosa': 'Bianca con pomodorino giallo, stracciatella Maldera e noci',
  'Gricia': 'Bianca con cipolla, guanciale croccante, crema di pecorino e pepe',
  'Porcini & guanciale': 'Bianca con porcini e guanciale croccante: profumo di bosco',
  'Portafoglio': 'La pizza piegata a portafoglio, con fior di latte, rucola, crudo e crema di parmigiano',
  "'Nduja": "Prosciutto crudo, burrata e 'nduja piccante di Spilinga",
  'Covaccino 2.0': 'Il covaccino del forno a legna, con crudo, burrata e pomodorini confit',
  'La Piccante': 'Salamino piccante e stracciatella Maldera: fuoco e freschezza',
  'Amatriciana': 'Pomodoro, guanciale, pecorino romano e pepe',
  'Degustazione Cartabianca': 'Un assaggio di tutti i dolci della nostra pasticceria, da dividere',
  'Sfogliatina di mele calda': 'Appena sfornata, profumata alla cannella, con composta di frutti di bosco',
  'Millefoglie': 'Sfoglia caramellata della nostra pasticceria, crema chantilly e frutti di bosco freschi',
  'Crème brûlée': 'Crema all’arancia sotto una crosta di zucchero caramellato',
  'Calzoncino alla Nutella': 'Cotto nel forno a legna, ripieno di Nutella e spolverato di zucchero a velo',
  'Tiramisù': 'Savoiardi al caffè, crema al mascarpone e cacao amaro',
  'Cheesecake': 'Fatta da noi: frutti di bosco, cioccolato fondente o arance amare',
}
_PIZZE = ('classiche', 'tartufate', 'gourmet', 'speciali')
for _L in (TENNIS, CLUB):
    for _k in UNICO:
        for _p in _L[_k]:
            if _p['nome'] in DESCR3 and not (_k in _PIZZE and _L is CLUB and 'San Marzano' in DESCR3[_p['nome']]):
                _p['desc'] = DESCR3[_p['nome']]

# ---------- abbinamenti solo sulle pizze: un vino e una birra per OGNI pizza ----------
VINI = {'P': ('Tratturo', 'Passerina Terre di Chieti'), 'K': ('Tratturo', 'Pecorino Terre di Chieti'),
        'T': ('Vigna del Lauro', 'Traminer Isonzo'), 'Z': ('Zizzolo', 'Bolgheri')}
BIRRE = {'TENNIS': {'chiara': 'Hacker Hell', 'bianca': 'Hacker Weisse', 'ambrata': 'Hacker Kellerbier', 'scura': 'Lupulus Brune'},
         'CLUB': {'chiara': 'Lupulus Triple', 'bianca': 'Lupulus Blanche', 'ambrata': 'Ayinger Kellerbier', 'scura': 'Lupulus Brune'}}
ABB_PIZZA = {
  'Vegetariana': ('P', 'bianca'), 'Capricciosa': ('K', 'ambrata'), 'Melanzane & provola': ('K', 'chiara'), 'Maialona': ('Z', 'scura'),
  'Würstel': ('Z', 'chiara'), 'Bufala Dop': ('P', 'bianca'), 'Margherita': ('P', 'chiara'),
  'La Tartufina': ('Z', 'scura'), 'La Porcina': ('Z', 'scura'),
  'La Calabrese': ('Z', 'ambrata'), 'La Fratoni': ('T', 'ambrata'), 'Gialla di Cetara': ('P', 'bianca'), 'La Carbonara': ('K', 'ambrata'),
  'Del Contadino': ('T', 'scura'), 'La Gustosa': ('P', 'bianca'), 'Gricia': ('K', 'ambrata'),
  'La Tropea': ('P', 'bianca'), 'Porcini & guanciale': ('Z', 'scura'), 'Portafoglio': ('P', 'chiara'), "'Nduja": ('Z', 'ambrata'),
  'Covaccino 2.0': ('P', 'chiara'), 'La Piccante': ('Z', 'ambrata'), 'Amatriciana': ('K', 'ambrata'),
}
for _L in (TENNIS, CLUB):
    for _k in UNICO:
        for _p in _L[_k]:
            if _k in _PIZZE:
                v, b = ABB_PIZZA[_p['nome']]
                _p['abb2'] = (VINI[v], (b, BIRRE[_L['sigla']][b]))
            _p['abb'] = None
# foto vere disponibili (per la presentazione: asset di altri menu RBR, da sostituire con le foto Cartabianca)
FOTO_VERE = {'Bistecca alla fiorentina': 'p_fiorentina.png', 'Frittura di mare': 'p_frittura.png',
             'La Calabrese': 'p_calabrese.png', 'La Tartufina': 'p_tartufina.png', 'Tiramisù': 'p_tiramisu.png'}


# ---------- REVISIONE 8 (05/10): niente marche nelle descrizioni (origini sì), stesse birre ovunque, fiorentina 50 ----------
DESCR4 = {
  'Bufala Dop': 'Pomodoro 100% italiano e mozzarella di bufala campana dop',
  'La Tartufina': 'Pomodoro 100% italiano, mozzarella di bufala campana dop e tartufo nero a lamelle',
  'La Porcina': 'Pomodoro 100% italiano, fior di latte e porcini trifolati al tartufo nero',
  'Margherita': 'Pomodoro 100% italiano, fior di latte e basilico fresco: semplice e perfetta',
  'Gialla di Cetara': 'Bianca con pomodorini gialli, olive taggiasche, stracciatella pugliese e alici di Cetara',
  'La Gustosa': 'Bianca con pomodorino giallo, stracciatella pugliese e noci',
  "'Nduja": "Prosciutto crudo, burrata pugliese e 'nduja calabrese piccante",
  'La Piccante': 'Salamino piccante e stracciatella pugliese: fuoco e freschezza',
  'La Tropea': 'Bianca con mozzarella di bufala campana, olive taggiasche, pomodorini gialli e cipolla rossa di Tropea',
  'Covaccino 2.0': 'Il covaccino del forno a legna, con crudo, burrata pugliese e pomodorini confit',
  'Tagliata di controfiletto al sale Maldon': '250 g di controfiletto di manzo alla brace, sale in fiocchi, rosmarino e patate al forno',
  'Bistecca alla fiorentina': 'La regina della brace toscana, al sangue come vuole la tradizione · al kg',
}
BIRRE_UNICHE = {'chiara': 'Bionda bavarese', 'bianca': 'Weiss di frumento', 'ambrata': 'Ambrata non filtrata', 'scura': 'Scura d’abbazia'}
for _L in (TENNIS, CLUB):
    for _k in UNICO:
        for _p in _L[_k]:
            if _p['nome'] in DESCR4:
                _p['desc'] = DESCR4[_p['nome']]
            if _p.get('abb2'):
                _v, (_t, _b) = _p['abb2']
                _p['abb2'] = (_v, (_t, BIRRE_UNICHE[_t]))
            if 'fiorentina' in _p['nome']:
                _p['nuovo_prezzo'] = 50
            if _p['nome'] == 'Tagliata di controfiletto al sale Maldon':
                _p['nome'] = 'Tagliata di controfiletto alla brace'
# foto vere: si leggono da img/foto/<nome-file>.png appena ci sono (vedi prompt_foto_chatgpt.md)
import os as _os
FOTO_FILE = {'Battuta di scottona': 'battuta_scottona', 'Tagliolini al tartufo nero': 'tagliolini_tartufo',
             'Paccheri alla carbonara di mare': 'paccheri_carbonara_mare', 'Bistecca alla fiorentina': 'fiorentina',
             'Frittura di mare': 'frittura_mare', 'La Tropea': 'pizza_tropea', 'La Tartufina': 'pizza_tartufina',
             'La Calabrese': 'pizza_calabrese', 'Degustazione Cartabianca': 'degustazione_dolci',
             'Sfogliatina di mele calda': 'sfogliatina_mele', 'Tartufo nero': 'agg_tartufo', 'Burrata': 'agg_burrata',
             'Crudo di Parma': 'agg_crudo'}
_DIR = _os.path.join(_os.path.dirname(_os.path.abspath(__file__)), 'img', 'foto')
FOTO_VERE = {}
for _n, _f in FOTO_FILE.items():
    for _ext in ('.png', '.jpg', '.jpeg', '.webp'):
        if _os.path.exists(_os.path.join(_DIR, _f + _ext)):
            FOTO_VERE[_n] = 'foto/' + _f + _ext
# REV 9 (05/10): Degustazione Cartabianca giustificata: 5 assaggi per due, 16 (= 8 a testa, come un dolce)
for _L in (TENNIS, CLUB):
    for _p in _L['dolci']:
        if _p['nome'] == 'Degustazione Cartabianca':
            _p['desc'] = ('Cinque assaggi della nostra pasticceria serviti insieme: sfogliatina di mele calda, crème brûlée, '
                          'tiramisù, cheesecake e millefoglie')
            _p['nuovo_prezzo'] = 16
            _p['fc_fisso'] = 4.2
# REV 10 (05/10): descrizioni lunghe (2 righe) che valorizzano gli ingredienti, senza aggiungerne (allergeni invariati);
# selezioni Cartabianca tolte dagli antipasti per il momento
DESCR5 = {
  'Gamberoni in pasta kataifi': 'Gamberoni interi avvolti in un nido di pasta kataifi e fritti al momento: croccanti fuori, dolci e succosi dentro, da intingere nella nostra mayo',
  'Battuta di scottona': 'Scottona battuta a punta di coltello e condita a crudo, con un tuorlo fritto che si rompe sulla carne, burrata cremosa e scaglie di tartufo nero',
  'Tagliere CB': 'I salumi che scegliamo uno a uno, pecorino di Seggiano con miele millefiori e la nostra pappa al pomodoro toscana servita con burrata fresca',
  'Zuppetta di moscardini alla Luciana': 'Moscardini cotti piano in umido, come si fa a Santa Lucia, con polentine fritte e croccanti da intingere fino all’ultima goccia',
  'Coccoli artigianali': 'Pasta lievitata fritta al momento, gonfia e dorata come nelle sagre toscane, da aprire con le mani e riempire di prosciutto crudo e stracchino montato',
  'Bruschette Cartabianca': 'Pane toscano con salsiccia e stracchino, cavolo nero e pecorino; polentine con fegatini e funghi trifolati: un giro di Toscana in un piatto',
  'Tris di cruditè': 'Tre crudi da assaggiare: tartare di tonno con teriyaki e frutti di bosco, salmone con crema di topinambur, gamberi con burrata e pistacchi',
  'Tagliolini al tartufo nero': 'Tagliolini freschi saltati in una fonduta di grana, guanciale croccante e tartufo nero grattato al momento: il profumo arriva prima del piatto',
  'Risotto al Castelmagno e tartufo nero': 'Mantecato al Castelmagno, il formaggio delle montagne piemontesi, con tartare e jus di manzo, zucca confit e tartufo nero',
  'Risotto agli agrumi con scampi': 'Zafferano e agrumi, scampi interi appena scottati e una tartare di scampo crudo che si scioglie sul risotto caldo',
  'Fregola "in nero"': 'Fregola sarda cotta nello stracotto di seppie al loro nero, con una crema di burrata di Andria che addolcisce il sapore del mare',
  'Paccheri alla carbonara di mare': 'La carbonara come non l’avete mai mangiata: paccheri, frutti di mare, crema di tuorlo e bocconcini di tonno rosso al posto del guanciale',
  'Spaghetti quadrati allo scoglio': 'Spaghetti quadrati che trattengono il sugo, saltati in padella con tutti i frutti di mare del nostro scoglio: il mare intero in un piatto solo',
  'Gnudi di ricotta e spinaci': 'Fatti a mano da noi con ricotta e spinaci, come la ricetta di casa, su vellutata di salvia, cialde croccanti di parmigiano e mais',
  'Spaghetti freschi alla carbonara': 'Spaghetti freschi artigianali, guanciale rosolato fino a diventare croccante, tuorlo e pecorino montati a crema: la carbonara come si deve',
  'Linguine alle vongole veraci': 'Vongole veraci aperte in padella all’ultimo momento, il loro sugo che lega le linguine e bottarga di muggine grattugiata sopra',
  'Pacchero al ragù di cinghiale': 'Ragù di cinghiale cotto a lungo come nella tradizione maremmana, con un crumble di cacao amaro e nocciole alle erbe',
  'Bistecca alla fiorentina': 'La regina della brace toscana: crosta scura fuori, cuore rosso dentro, al sangue come vuole la tradizione · al kg',
  'Tagliata di controfiletto alla brace': '250 g di controfiletto di manzo alla brace, tagliato al momento, con sale in fiocchi, rosmarino e patate al forno dorate',
  'Grigliata di mare': 'Scampi, gamberoni, calamaro e polpo alla griglia, appena scottati per restare morbidi, con olio extravergine e limone',
  'Tonno rosso marinato alla barbecue': 'Trancio di tonno rosso marinato alla barbecue in crosta di sesamo, rosato dentro, su un morbido di sedano rapa e cavolo nero',
  'Frittura di mare': 'Calamari e gamberi fritti al momento, leggeri e dorati come sul lungomare, su verdure croccanti',
  'Goulash di mare': 'Polpo, seppia e totano gigante cotti piano in un cacciucco leggero, con il sugo profumato che bagna le patate stufate',
  'Galletto al mattone': 'Cotto a bassa temperatura e finito sotto il mattone, come nelle trattorie toscane: pelle croccante, carne tenera e verdure al forno',
  'Spiedino grigliato': 'Pancia, filetto, salsiccia e coppa di suino grigio del Casentino, l’antica razza toscana, alla griglia con fagioli all’uccelletta',
  'Cartabianca Burger': 'Manzo 180 g, pane multicereali, bacon affumicato, scamorza filante e la nostra salsa Cartabianca, con patate crispers',
  'Tataki di pollo': 'Pollo in crosta di sesamo, scottato e tagliato alla giapponese, con caponatina di peperoni e olive taggiasche',
  'Capricciosa': 'Carciofi, olive, funghi, prosciutto cotto e würstel: la classica di sempre, ricca come piace a noi',
  'Vegetariana': 'Melanzane, zucchine e pomodorini sul nostro impasto, con fior di latte: l’orto cotto nel forno',
  'Würstel': 'Pomodoro, fior di latte e würstel: la preferita dei bambini, e non solo',
  'Melanzane & provola': 'Melanzane cotte al forno e provola che fila: morbida e saporita',
  'Bufala Dop': 'Pomodoro 100% italiano e mozzarella di bufala campana dop: il latte di bufala fa la differenza',
  'Margherita': 'Pomodoro 100% italiano, fior di latte e basilico fresco: semplice e perfetta, la prova di ogni pizzaiolo',
  'Maialona': 'Per chi ha fame davvero: prosciutto cotto, salsiccia, salamino e würstel',
  'La Tartufina': 'Pomodoro 100% italiano, mozzarella di bufala campana dop e tartufo nero a lamelle: il profumo del bosco su una pizza',
  'La Porcina': 'Pomodoro 100% italiano, fior di latte e porcini trifolati al tartufo nero: l’autunno toscano appena sfornato',
  'La Fratoni': 'Bianca con zucca, provola filante e guanciale croccante: dolce, sapida, autunnale',
  'La Calabrese': 'Pomodoro, fior di latte, porcini e ’nduja piccante che si scioglie in cottura: il sud più deciso in una pizza',
  'La Carbonara': 'Bianca con guanciale croccante, tuorlo, pecorino e pepe nero: la carbonara romana diventa pizza',
  'Del Contadino': 'Bianca con gorgonzola, pere e noci: dolce e salato insieme, come la merenda dei contadini',
  'La Gustosa': 'Bianca con pomodorino giallo, stracciatella pugliese e noci: il dolce del pomodoro, la crema e il croccante',
  'Gricia': 'Bianca con cipolla, guanciale croccante, crema di pecorino e pepe: la nonna della carbonara, sapida e decisa',
  'Gialla di Cetara': 'Bianca con pomodorini gialli, olive taggiasche, stracciatella pugliese e alici di Cetara, il borgo dei pescatori della Costiera',
  'Porcini & guanciale': 'Bianca con porcini e guanciale croccante: il profumo del bosco e la sapidità del guanciale',
  'La Tropea': 'Bianca con mozzarella di bufala campana, olive taggiasche, pomodorini gialli e la cipolla rossa di Tropea, dolce come nessun’altra',
  "'Nduja": "Prosciutto crudo, burrata pugliese e 'nduja calabrese piccante: la burrata fresca spegne il fuoco della 'nduja",
  'Covaccino 2.0': 'Il covaccino del forno a legna, sottile e croccante, con prosciutto crudo, burrata pugliese e pomodorini confit',
  'Amatriciana': 'Pomodoro, guanciale croccante, pecorino romano e pepe: il sugo di Amatrice diventa pizza',
  'La Piccante': 'Salamino piccante e stracciatella pugliese: fuoco e freschezza nello stesso morso',
  'Portafoglio': 'La pizza piegata a portafoglio come nei vicoli di Napoli, con fior di latte, rucola, crudo e crema di parmigiano',
  'Sfogliatina di mele calda': 'Sfoglia appena sfornata, mele profumate alla cannella e composta di frutti di bosco: calda, come la merenda della domenica',
  'Crème brûlée': 'Crema all’arancia sotto una crosta di zucchero caramellato, da rompere col cucchiaino',
  'Calzoncino alla Nutella': 'Cotto nel forno a legna, ripieno di crema alle nocciole calda e coperto da una nevicata di zucchero a velo',
  'Tiramisù': 'Savoiardi bagnati nel caffè, crema al mascarpone e cacao amaro: il dolce italiano per eccellenza',
  'Cheesecake': 'Fatta da noi, cremosa e fresca, da scegliere con frutti di bosco, cioccolato fondente o arance amare',
  'Millefoglie': 'Sfoglia caramellata della nostra pasticceria, crema chantilly e frutti di bosco freschi',
}
for _L in (TENNIS, CLUB):
    _L['premium_antipasti'] = []
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and _p.get('nome') in DESCR5:
                    _p['desc'] = DESCR5[_p['nome']]
# REV 11 (05/10): solo ingredienti valorizzati, niente frasi finali a effetto (Marco)
DESCR6 = {
  'Gamberoni in pasta kataifi': 'Gamberoni interi avvolti in pasta kataifi croccante, fritti al momento, con la nostra mayo fatta in casa',
  'Battuta di scottona': 'Scottona battuta a punta di coltello, tuorlo d’uovo fritto croccante, burrata cremosa e scaglie di tartufo nero',
  'Tagliere CB': 'Salumi selezionati, pecorino di Seggiano stagionato, miele millefiori e pappa al pomodoro con burrata fresca',
  'Zuppetta di moscardini alla Luciana': 'Moscardini cotti lentamente in umido alla luciana, con polentine fritte croccanti',
  'Coccoli artigianali': 'Pasta lievitata fritta al momento, prosciutto crudo stagionato e stracchino fresco montato',
  'Bruschette Cartabianca': 'Pane toscano con salsiccia e stracchino, cavolo nero e pecorino; polentine con fegatini e funghi trifolati',
  'Tris di cruditè': 'Tartare di tonno con teriyaki e frutti di bosco, salmone con crema di topinambur, gamberi crudi con burrata e pistacchi',
  'Tagliolini al tartufo nero': 'Tagliolini freschi, fonduta di grana stagionato, guanciale croccante e tartufo nero grattato al momento',
  'Risotto al Castelmagno e tartufo nero': 'Riso mantecato al Castelmagno di montagna, tartare e jus di manzo, zucca confit e tartufo nero',
  'Risotto agli agrumi con scampi': 'Riso allo zafferano e agrumi, scampi interi appena scottati e tartare di scampo crudo',
  'Fregola "in nero"': 'Fregola sarda tostata, stracotto di seppie al loro nero e crema di burrata di Andria',
  'Paccheri alla carbonara di mare': 'Paccheri, frutti di mare, crema di tuorlo d’uovo e bocconcini di tonno rosso scottati',
  'Spaghetti quadrati allo scoglio': 'Spaghetti quadrati saltati in padella con i frutti di mare freschi dello scoglio',
  'Gnudi di ricotta e spinaci': 'Gnudi fatti a mano con ricotta fresca e spinaci, vellutata di salvia, cialde di parmigiano e mais',
  'Spaghetti freschi alla carbonara': 'Spaghetti freschi artigianali, guanciale croccante, tuorlo d’uovo e pecorino romano',
  'Linguine alle vongole veraci': 'Linguine, vongole veraci aperte in padella e bottarga di muggine grattugiata al momento',
  'Pacchero al ragù di cinghiale': 'Paccheri, ragù di cinghiale cotto a lungo, crumble di cacao amaro e nocciole alle erbe',
  'Bistecca alla fiorentina': 'Costata di manzo con l’osso cotta alla brace, al sangue come vuole la tradizione toscana · al kg',
  'Tagliata di controfiletto alla brace': '250 g di controfiletto di manzo alla brace, sale in fiocchi, rosmarino e patate al forno',
  'Grigliata di mare': 'Scampi, gamberoni, calamaro e polpo alla griglia, olio extravergine e limone',
  'Tonno rosso marinato alla barbecue': 'Trancio di tonno rosso marinato alla barbecue in crosta di sesamo, morbido di sedano rapa e cavolo nero',
  'Frittura di mare': 'Calamari e gamberi fritti al momento, leggeri e dorati, su verdure croccanti',
  'Goulash di mare': 'Polpo, seppia e totano gigante in un cacciucco leggero, con patate stufate',
  'Galletto al mattone': 'Galletto cotto a bassa temperatura e finito sotto il mattone, con verdure al forno',
  'Spiedino grigliato': 'Pancia, filetto, salsiccia e coppa di suino grigio del Casentino alla griglia, fagioli all’uccelletta',
  'Cartabianca Burger': 'Manzo 180 g, pane multicereali, bacon affumicato, scamorza e salsa Cartabianca, patate crispers',
  'Tataki di pollo': 'Pollo in crosta di sesamo scottato e tagliato, caponatina di peperoni e olive taggiasche',
  'Capricciosa': 'Pomodoro, fior di latte, carciofi, olive, funghi, prosciutto cotto e würstel',
  'Vegetariana': 'Fior di latte, melanzane, zucchine e pomodorini',
  'Würstel': 'Pomodoro, fior di latte e würstel',
  'Melanzane & provola': 'Melanzane al forno e provola filante',
  'Bufala Dop': 'Pomodoro 100% italiano e mozzarella di bufala campana dop',
  'Margherita': 'Pomodoro 100% italiano, fior di latte e basilico fresco',
  'Maialona': 'Prosciutto cotto, salsiccia, salamino e würstel',
  'La Tartufina': 'Pomodoro 100% italiano, mozzarella di bufala campana dop e tartufo nero a lamelle',
  'La Porcina': 'Pomodoro 100% italiano, fior di latte e porcini trifolati al tartufo nero',
  'La Fratoni': 'Bianca con zucca, provola filante e guanciale croccante',
  'La Calabrese': 'Pomodoro, fior di latte, porcini e ’nduja calabrese piccante',
  'La Carbonara': 'Bianca con guanciale croccante, tuorlo d’uovo, pecorino romano e pepe nero',
  'Del Contadino': 'Bianca con gorgonzola, pere e noci',
  'La Gustosa': 'Bianca con pomodorino giallo, stracciatella pugliese e noci',
  'Gricia': 'Bianca con cipolla, guanciale croccante, crema di pecorino romano e pepe nero',
  'Gialla di Cetara': 'Bianca con pomodorini gialli, olive taggiasche, stracciatella pugliese e alici di Cetara',
  'Porcini & guanciale': 'Bianca con porcini e guanciale croccante',
  'La Tropea': 'Bianca con mozzarella di bufala campana, olive taggiasche, pomodorini gialli e cipolla rossa di Tropea',
  "'Nduja": "Prosciutto crudo, burrata pugliese e 'nduja calabrese piccante",
  'Covaccino 2.0': 'Covaccino del forno a legna con prosciutto crudo, burrata pugliese e pomodorini confit',
  'Amatriciana': 'Pomodoro, guanciale croccante, pecorino romano e pepe nero',
  'La Piccante': 'Salamino piccante e stracciatella pugliese',
  'Portafoglio': 'Pizza piegata a portafoglio con fior di latte, rucola, prosciutto crudo e crema di parmigiano',
  'Sfogliatina di mele calda': 'Sfoglia appena sfornata, mele alla cannella e composta di frutti di bosco',
  'Crème brûlée': 'Crema all’arancia e crosta di zucchero caramellato',
  'Calzoncino alla Nutella': 'Calzoncino cotto nel forno a legna, crema alle nocciole e zucchero a velo',
  'Tiramisù': 'Savoiardi al caffè, crema al mascarpone e cacao amaro',
  'Cheesecake': 'Fatta da noi, con frutti di bosco, cioccolato fondente o arance amare',
  'Millefoglie': 'Sfoglia caramellata, crema chantilly e frutti di bosco freschi',
}
for _L in (TENNIS, CLUB):
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and _p.get('nome') in DESCR6:
                    _p['desc'] = DESCR6[_p['nome']]
# REV 12 (05/10): le pizze non iniziano più con «Bianca»: si parte dall'ingrediente principale
DESCR7 = {
  'La Fratoni': 'Provola filante, zucca e guanciale croccante',
  'La Carbonara': 'Fior di latte, guanciale croccante, tuorlo d’uovo, pecorino romano e pepe nero',
  'Del Contadino': 'Gorgonzola cremoso, pere e noci',
  'La Gustosa': 'Stracciatella pugliese, pomodorino giallo e noci',
  'Gricia': 'Crema di pecorino romano, guanciale croccante, cipolla e pepe nero',
  'Gialla di Cetara': 'Stracciatella pugliese, pomodorini gialli, olive taggiasche e alici di Cetara',
  'Porcini & guanciale': 'Fior di latte, porcini e guanciale croccante',
  'La Tropea': 'Mozzarella di bufala campana, olive taggiasche, pomodorini gialli e\ncipolla rossa di Tropea',
  'La Calabrese': 'Pomodoro 100% italiano, fior di latte, porcini e ’nduja calabrese piccante',
  'Amatriciana': 'Pomodoro 100% italiano, guanciale croccante, pecorino romano e pepe nero',
  'Capricciosa': 'Pomodoro 100% italiano, fior di latte, carciofi, olive, funghi, prosciutto cotto e würstel',
  'Würstel': 'Pomodoro 100% italiano, fior di latte e würstel',
  'La Piccante': 'Stracciatella pugliese e salamino piccante',
}
for _L in (TENNIS, CLUB):
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and _p.get('nome') in DESCR7:
                    _p['desc'] = DESCR7[_p['nome']]
# REV 13 (05/10): confermato da Marco: fior di latte 100% italiano, pomodoro toscano
import re as _re
for _L in (TENNIS, CLUB):
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and isinstance(_p.get('desc'), str):
                    _d = _re.sub(r'\b[Pp]omodoro 100% italiano', lambda m: m.group(0)[0] + 'omodoro toscano', _p['desc'])
                    _d = _re.sub(r'^Pomodoro(?! toscano)', 'Pomodoro toscano', _d)
                    _d = _re.sub(r'([Ff]ior di latte)(?! 100%)', r'\1 100% italiano', _d)
                    _p['desc'] = _d
# REV 14 (05/10): descrizioni incrociate con le fatture di acquisto 2026 (articoli_aggregati.csv):
# solo provenienze verificate in fattura (pomodoro toscano, bufala dop, stracciatella/burrata di Andria,
# alici di Cetara, Castelmagno dop, gorgonzola dop, Fior di Seggiano, tartufo nero estivo, scampi scozzesi,
# vongole veraci italiane, calamari patagonici, gamberi argentini, salmone norvegese, salsiccia lucchese,
# hamburger di scottona 180 g, würstel di puro suino, spaghetti quadrati 100% grano italiano). Niente marchi.
DESCR8 = {
  'Battuta di scottona': 'Scottona battuta a coltello, tuorlo d’uovo fritto croccante, burrata di Andria e tartufo nero estivo',
  'Tagliere CB': 'Salumi selezionati, pecorino Fior di Seggiano con miele, pappa al pomodoro toscano e burrata di Andria',
  'Bruschette Cartabianca': 'Pane toscano con salsiccia lucchese e stracchino, cavolo nero e pecorino; polentine con fegatini e funghi trifolati',
  'Tris di cruditè': 'Tartare di tonno con teriyaki e frutti di bosco, salmone norvegese con crema di topinambur, gamberi con burrata di Andria e pistacchi',
  'Tagliolini al tartufo nero': 'Tagliolini di pasta fresca, fonduta di grana padano dop, guanciale croccante e tartufo nero estivo grattato al momento',
  'Risotto al Castelmagno e tartufo nero': 'Riso Carnaroli mantecato al Castelmagno dop, tartare e jus di manzo, zucca confit e tartufo nero estivo',
  'Risotto agli agrumi con scampi': 'Riso Carnaroli allo zafferano e agrumi, scampi scozzesi appena scottati e tartare di scampo crudo',
  'Fregola "in nero"': 'Fregola sarda, stracotto di seppie al loro nero e crema di burrata di Andria',
  'Paccheri alla carbonara di mare': 'Paccheri, frutti di mare, crema di tuorlo d’uovo e bocconcini di tonno scottati',
  'Spaghetti quadrati allo scoglio': 'Spaghetti quadrati di grano 100% italiano saltati con i frutti di mare dello scoglio',
  'Spaghetti freschi alla carbonara': 'Spaghetti di pasta fresca, guanciale croccante, tuorlo d’uovo e pecorino romano',
  'Linguine alle vongole veraci': 'Linguine, vongole veraci italiane aperte in padella e bottarga di muggine grattugiata al momento',
  'Gnudi di ricotta e spinaci': 'Gnudi fatti a mano con ricotta e spinaci, vellutata di salvia fresca, cialde di parmigiano e mais',
  'Grigliata di mare': 'Scampi scozzesi, gamberoni, calamaro patagonico e polpo alla griglia, olio extravergine e limone',
  'Tonno rosso marinato alla barbecue': 'Trancio di tonno marinato alla barbecue in crosta di sesamo, morbido di sedano rapa e cavolo nero',
  'Frittura di mare': 'Calamari patagonici e gamberi argentini fritti al momento, leggeri e dorati, su verdure croccanti',
  'Cartabianca Burger': 'Hamburger di scottona 180 g, pane ai cereali, bacon affumicato, scamorza affumicata e salsa Cartabianca, patate crispers',
  'La Tartufina': 'Polpa di pomodoro toscano, mozzarella di bufala campana dop e tartufo nero estivo a lamelle',
  'La Porcina': 'Polpa di pomodoro toscano, fior di latte 100% italiano e porcini trifolati al tartufo nero',
  'La Fratoni': 'Provola affumicata filante, zucca e guanciale croccante',
  'La Calabrese': 'Polpa di pomodoro toscano, fior di latte 100% italiano, porcini e ’nduja piccante',
  'Del Contadino': 'Gorgonzola dop, pere e noci',
  'La Gustosa': 'Stracciatella di Andria, datterini gialli e noci',
  'Gialla di Cetara': 'Stracciatella di Andria, datterini gialli, olive taggiasche e alici di Cetara',
  'La Tropea': 'Mozzarella di bufala campana dop, olive taggiasche, datterini gialli e\ncipolla rossa di Tropea',
  "'Nduja": "Prosciutto crudo, burrata di Andria e 'nduja piccante",
  'Covaccino 2.0': 'Covaccino del forno a legna con prosciutto crudo, burrata di Andria e pomodorini confit',
  'Amatriciana': 'Polpa di pomodoro toscano, guanciale croccante, pecorino romano e pepe nero',
  'La Piccante': 'Stracciatella di Andria e salamino piccante',
  'Capricciosa': 'Polpa di pomodoro toscano, fior di latte 100% italiano, carciofi, olive, funghi, prosciutto cotto e würstel',
  'Würstel': 'Polpa di pomodoro toscano, fior di latte 100% italiano e würstel di puro suino',
  'Melanzane & provola': 'Melanzane al forno e provola affumicata filante',
  'Bufala Dop': 'Polpa di pomodoro toscano e mozzarella di bufala campana dop',
  'Margherita': 'Polpa di pomodoro toscano, fior di latte 100% italiano e basilico fresco',
  'Maialona': 'Prosciutto cotto, salsiccia, salamino e würstel di puro suino',
  'Sfogliatina di mele calda': 'Pasta sfoglia appena sfornata, mele alla cannella e composta di frutti di bosco',
}
for _L in (TENNIS, CLUB):
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and _p.get('nome') in DESCR8:
                    _p['desc'] = DESCR8[_p['nome']]
# REV 15 (05/10): «pomodoro del nostro territorio» ovunque; Del Contadino più ricca
for _L in (TENNIS, CLUB):
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and isinstance(_p.get('desc'), str):
                    _d = _p['desc'].replace('Polpa di pomodoro toscano', 'Pomodoro del nostro territorio')
                    _d = _d.replace('pomodoro toscano', 'pomodoro del nostro territorio').replace('Pomodoro toscano', 'Pomodoro del nostro territorio')
                    if _p.get('nome') == 'Del Contadino':
                        _d = 'Gorgonzola dop dolce e cremoso, pere fresche tagliate a fettine sottili e gherigli di noce croccanti'
                    _p['desc'] = _d
# REV 16 (05/10): degustazione generica, senza elenco dolci né «per due»
for _L in (TENNIS, CLUB):
    for _p in _L['dolci']:
        if _p['nome'] == 'Degustazione Cartabianca':
            _p['desc'] = 'Piccoli assaggi dei dolci del giorno, scelti dalla nostra pasticceria e serviti insieme'
# REV 17 (05/10): sfogliatina, «composta…» sul secondo rigo
for _L in (TENNIS, CLUB):
    for _p in _L['dolci']:
        if _p['nome'] == 'Sfogliatina di mele calda':
            _p['desc'] = 'Pasta sfoglia appena sfornata e mele alla cannella,\ncomposta di frutti di bosco'
# REV 18 (05/10): descrizioni su due righe (il prezzo esce sulla seconda), contorni descritti,
# fiorentina «5 all'etto, per 2 persone»
DESCR9 = {
  'Gamberoni in pasta kataifi': 'Gamberoni interi avvolti a mano in pasta kataifi sottile, fritti al momento fino a renderli dorati e croccanti, serviti con la nostra mayo fatta in casa',
  'Battuta di scottona': 'Scottona battuta a coltello e condita a crudo, tuorlo d’uovo fritto croccante, burrata di Andria e lamelle di tartufo nero estivo',
  'Tagliere CB': 'Salumi selezionati affettati al momento, pecorino Fior di Seggiano con miele, pappa al pomodoro del nostro territorio con burrata di Andria',
  'Zuppetta di moscardini alla Luciana': 'Moscardini cotti lentamente in umido alla luciana nel loro sugo di pomodoro, serviti con polentine di mais fritte e croccanti da intingere',
  'Coccoli artigianali': 'Coccoli di pasta lievitata fritti al momento, caldi e soffici, da aprire e farcire con prosciutto crudo stagionato e stracchino fresco montato',
  'Fregola "in nero"': 'Fregola sarda tostata, stracotto di seppie cotte a lungo nel loro nero e una crema fresca di burrata di Andria a completare il piatto',
  'Paccheri alla carbonara di mare': 'Paccheri di semola, frutti di mare saltati in padella, crema di tuorlo d’uovo e bocconcini di tonno scottati al posto del guanciale',
  'Spaghetti quadrati allo scoglio': 'Spaghetti quadrati di grano 100% italiano saltati in padella con i frutti di mare dello scoglio, che rilasciano tutto il loro sapore nel sugo',
  'Gnudi di ricotta e spinaci': 'Gnudi morbidi fatti a mano con ricotta e spinaci, adagiati su una vellutata di salvia fresca, con cialde croccanti di parmigiano e mais',
  'Spaghetti freschi alla carbonara': 'Spaghetti di pasta fresca, guanciale rosolato fino a diventare croccante, crema di tuorlo d’uovo e pecorino romano grattugiato al momento',
  'Linguine alle vongole veraci': 'Linguine di semola, vongole veraci italiane aperte in padella con il loro sugo e bottarga di muggine grattugiata al momento sopra il piatto',
  'Pacchero al ragù di cinghiale': 'Paccheri di semola, ragù di cinghiale cotto lentamente a lungo, crumble croccante di cacao amaro e nocciole tostate alle erbe aromatiche',
  'Bistecca alla fiorentina': 'Costata di manzo con l’osso cotta alla brace, al sangue come vuole la tradizione toscana',
  'Tonno rosso marinato alla barbecue': 'Trancio di tonno marinato alla barbecue in crosta di sesamo, scottato fuori e rosato dentro, su un morbido di sedano rapa e cavolo nero',
  'Goulash di mare': 'Polpo, seppia e totano gigante cotti piano in un cacciucco leggero e profumato, serviti con patate stufate che ne raccolgono il sugo',
  'Galletto al mattone': 'Galletto cotto a bassa temperatura e poi rosolato sotto il mattone, con la pelle croccante e la carne tenera, servito con verdure al forno',
  'Spiedino grigliato': 'Pancia, filetto, salsiccia e coppa di suino grigio del Casentino cotti alla griglia, serviti con fagioli all’uccelletta al pomodoro',
  'Tataki di pollo': 'Pollo in crosta di sesamo scottato e tagliato a fette alla giapponese, con una caponatina agrodolce di peperoni e olive taggiasche',
  'Patatine fritte': 'Fritte al momento, dorate e croccanti',
  'Patate arrosto': 'Al forno con rosmarino, croccanti fuori e morbide dentro',
  'Verdure grigliate': 'Melanzane, zucchine e peperoni alla griglia con olio extravergine',
  'Insalata di misticanza': 'Misticanza di stagione con olio extravergine',
}
for _L in (TENNIS, CLUB):
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and _p.get('nome') in DESCR9:
                    _p['desc'] = DESCR9[_p['nome']]
                if isinstance(_p, dict) and _p.get('nome') == 'Bistecca alla fiorentina':
                    _p['prezzo_txt'] = '5 all’etto'
# REV 19 (05/10): via la Margherita; pizze descritte su due righe (solo ingredienti verificati in fattura)
for _L in (TENNIS, CLUB):
    _L['classiche'] = [_p for _p in _L['classiche'] if _p['nome'] != 'Margherita']
DESCR10 = {
  'Porcini & guanciale': 'Fior di latte 100% italiano, porcini trifolati in padella e guanciale tagliato a listarelle, cotto in forno fino a diventare croccante',
  'La Trop
ea': 'Mozzarella di bufala campana dop, olive taggiasche denocciolate, datterini gialli dolci e cipolla rossa di Tropea tagliata sottile',
  "'Nduja": "Prosciutto crudo stagionato, burrata di Andria cremosa aggiunta a crudo e 'nduja piccante che si scioglie sulla pizza in cottura",
  'Covaccino 2.0': 'Covaccino sottile cotto nel forno a legna, farcito con prosciutto crudo stagionato, burrata di Andria e pomodorini confit al forno',
  'La Piccante': 'Stracciatella di Andria fresca e cremosa, aggiunta in uscita dal forno, e salamino piccante tagliato a fette sottili',
  'Amatriciana': 'Pomodoro del nostro territorio, guanciale croccante tagliato a listarelle, pecorino romano grattugiato e pepe nero macinato al momento',
  'Portafoglio': 'Pizza piegata a portafoglio e farcita con fior di latte 100% italiano, rucola fresca, prosciutto crudo stagionato e crema di parmigiano',
  'Capricciosa': 'Pomodoro del nostro territorio, fior di latte 100% italiano, carciofi, olive, funghi champignon, prosciutto cotto e würstel di puro suino',
  'Vegetariana': 'Fior di latte 100% italiano, melanzane e zucchine a fette sottili e pomodorini freschi tagliati a metà, cotti nel forno con la pizza',
  'Maialona': 'Pomodoro del nostro territorio, fior di latte 100% italiano, prosciutto cotto, salsiccia sbriciolata, salamino e würstel di puro suino',
  'Würstel': 'Pomodoro del nostro territorio, fior di latte 100% italiano e würstel di puro suino tagliati a rondelle e dorati nel forno',
  'Melanzane & provola': 'Pomodoro del nostro territorio, melanzane cotte al forno a fette e provola affumicata che fila in cottura',
  'Bufala Dop': 'Pomodoro del nostro territorio e mozzarella di bufala campana dop spezzata a mano, morbida e ricca di latte',
  'La Fratoni': 'Provola affumicata filante, zucca gialla cotta al forno e guanciale tagliato a listarelle, rosolato fino a diventare croccante',
  'La Calabrese': 'Pomodoro del nostro territorio, fior di latte 100% italiano, porcini trifolati e ’nduja piccante che si scioglie sulla pizza in cottura',
  'La Carbonara': 'Fior di latte 100% italiano, guanciale croccante, tuorlo d’uovo cremoso, pecorino romano grattugiato e pepe nero macinato al momento',
  'Del Contadino': 'Gorgonzola dop dolce e cremoso, pere fresche tagliate a fettine sottili e un trito di noci croccanti sparso a fine cottura',
  'La Gustosa': 'Stracciatella di Andria fresca e cremosa, datterini gialli dolci tagliati a metà e noci sgusciate a quarti, croccanti sotto i denti',
  'Gricia': 'Crema di pecorino romano, guanciale tagliato a listarelle e rosolato fino a diventare croccante, cipolla dorata e pepe nero macinato al momento',
  'Gialla di Cetara': 'Stracciatella di Andria, datterini gialli, olive taggiasche denocciolate e alici di Cetara sott’olio, dalla Costiera Amalfitana',
  'La Tartufina': 'Pomodoro del nostro territorio, mozzarella di bufala campana dop e lamelle di tartufo nero estivo affettate sulla pizza al momento',
  'La Porcina': 'Pomodoro del nostro territorio, fior di latte 100% italiano e porcini trifolati, profumati al tartufo nero',
}
for _L in (TENNIS, CLUB):
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and _p.get('nome') in DESCR10:
                    _p['desc'] = DESCR10[_p['nome']]
# REV 20 (05/10): La Piccante su una riga; degustazione a capo dopo «giorno,»
for _L in (TENNIS, CLUB):
    for _k in list(_L):
        if isinstance(_L[_k], list):
            for _p in _L[_k]:
                if isinstance(_p, dict) and _p.get('nome') == 'La Piccante':
                    _p['desc'] = 'Stracciatella di Andria fresca e cremosa e salamino piccante tagliato a fette sottili'
                if isinstance(_p, dict) and _p.get('nome') == 'Degustazione Cartabianca':
                    _p['desc'] = 'Piccoli assaggi dei dolci del giorno,\nscelti dalla nostra pasticceria e serviti insieme'
# REV 21 (05/10): a capo scelti a mano dove l'automatico spezza male
_ACAPO = {
  'Bufala Dop': 'Pomodoro del nostro territorio e mozzarella di bufala campana dop\nspezzata a mano, morbida e ricca di latte',
  'Melanzane & provola': 'Pomodoro del nostro territorio, melanzane al forno a fette e provola affumicata che fila in cottura',
  'Würstel': 'Pomodoro del nostro territorio, fior di latte 100% italiano\ne würstel di puro suino tagliati a rondelle e dorati nel forno',
}
for _L in (TENNIS, CLUB):
    for _p in _L['classiche']:
        if _p['nome'] in _ACAPO:
            _p['desc'] = _ACAPO[_p['nome']]
# REV 22 (08/10, Marco): tagliolini al tartufo nero a 24 per dare movimento ai tre primi d'autore (22 · 24 · 23)
for _L in (TENNIS, CLUB):
    for _p in _L['premium_primi']:
        if _p['nome'] == 'Tagliolini al tartufo nero':
            _p['old'] = 24
# REV 23 (08/10, Marco + Emiliano): Experience per due (antipasto e dolce da dividere, un primo o secondo a testa) a 49, barrato ~58
for _L in (TENNIS, CLUB):
    _L['percorso'] = dict(nome='Cartabianca Experience', prezzo=49)
# REV 24 (08/10, Marco): Experience col prezzo A PERSONA (minimo 2 persone): 25 a persona = 50 per due
for _L in (TENNIS, CLUB):
    _L['percorso'] = dict(nome='Cartabianca Experience', prezzo=50)
# REV 25 (08/10, Marco): Experience 26 pp con 32 barrato (scelto da Marco), portata a testa solo tra pasta e secondi della carta
for _L in (TENNIS, CLUB):
    _L['percorso'] = dict(nome='Cartabianca Experience', prezzo=52, barrato=32)
# REV 26 (08/10, Aldo via Marco): abbinamenti vino nuovi sulle pizze (birra invariata): una bollicina e un rosato
_ALDO = {'La Carbonara': ('Franciacorta Brut', 'San Cristoforo'), 'Gricia': ('Franciacorta Brut', 'San Cristoforo'),
         'Bufala Dop': ("Cerasuolo d'Abruzzo", 'DOC'), 'Vegetariana': ("Cerasuolo d'Abruzzo", 'DOC')}
for _L in (TENNIS, CLUB):
    for _k, _lista in _L.items():
        if isinstance(_lista, list):
            for _p in _lista:
                if isinstance(_p, dict) and _p.get('nome') in _ALDO and _p.get('abb2'):
                    _p['abb2'] = (_ALDO[_p['nome']], _p['abb2'][1])
# REV 27 (09/10, Marco): fiorentina 60 al kg (6 all'etto) senza «per 2 persone»; spiedino grigliato 16; insalata di misticanza 6
_NP27 = {'Spiedino grigliato': 16, 'Insalata di misticanza': 6, 'Bistecca alla fiorentina': 60}
for _L in (TENNIS, CLUB):
    for _k, _lista in _L.items():
        if isinstance(_lista, list):
            for _p in _lista:
                if isinstance(_p, dict) and _p.get('nome') in _NP27:
                    _p['nuovo_prezzo'] = _NP27[_p['nome']]
                    if _p['nome'] == 'Bistecca alla fiorentina':
                        _p['per2'] = False
                        _p['prezzo_txt'] = '6 all’etto'
# REV 28 (09/10, Marco): asterisco sui piatti con prodotti congelati/abbattuti (nota legale già in fondo alle pagine).
# Lista da fatture lug-ago 2026 (Emme Gel, Iliopesca, MARR, Polo, Nova Food: IQF/congelato) + crudo di pesce (abbattuto per legge).
# DA CONFERMARE con Aldo: moscardini e funghi delle bruschette non trovati in fattura come congelati (messi per prudenza).
CONGELATI = {'Gamberoni in pasta kataifi', 'Tris di cruditè', 'Zuppetta di moscardini alla Luciana', 'Bruschette Cartabianca',
             'Paccheri alla carbonara di mare', 'Spaghetti quadrati allo scoglio', 'Fregola "in nero"', 'Risotto agli agrumi con scampi',
             'Frittura di mare', 'Tonno rosso marinato alla barbecue', 'Goulash di mare', 'Cartabianca Burger', 'Grigliata di mare',
             'Patatine fritte', 'La Calabrese', 'Porcini & guanciale', 'La Porcina', 'Sfogliatina di mele calda', 'Millefoglie'}
# REV 29 (09/10, Marco): battuta più lunga così il prezzo arriva a metà riga (ingredienti veri dalla foto della cucina)
for _L in (TENNIS, CLUB):
    for _p in _L['antipasti']:
        if _p['nome'] == 'Battuta di scottona':
            _p['desc'] = ('Scottona battuta a coltello e condita a crudo, tuorlo d’uovo fritto croccante, burrata di Andria '
                          'e lamelle di tartufo nero estivo, su un letto di songino con ribes rosso')
# REV 30 (09/10, Marco): asterisco anche sul pacchero al ragù di cinghiale (polpa di cinghiale congelata)
CONGELATI.add('Pacchero al ragù di cinghiale')
# REV 31 (09/10, check finale Marco): a capo scelti a mano nei contorni
_ACAPO_C = {'Patate arrosto': 'Al forno con rosmarino, croccanti fuori\ne morbide dentro',
            'Verdure grigliate': 'Melanzane, zucchine e peperoni alla griglia\ncon olio extravergine'}
for _L in (TENNIS, CLUB):
    for _p in _L['contorni']:
        if _p['nome'] in _ACAPO_C:
            _p['desc'] = _ACAPO_C[_p['nome']]
# REV 32 (09/10, check finale): allergeni — La Piccante era senza (impasto + stracciatella = 1-7); battuta: tuorlo fritto impanato → glutine
for _L in (TENNIS, CLUB):
    for _k, _lista in _L.items():
        if isinstance(_lista, list):
            for _p in _lista:
                if isinstance(_p, dict) and _p.get('nome') == 'La Piccante' and not _p.get('alg'):
                    _p['alg'] = '1-7'
                if isinstance(_p, dict) and _p.get('nome') == 'Battuta di scottona':
                    _p['alg'] = '1-3-7'

