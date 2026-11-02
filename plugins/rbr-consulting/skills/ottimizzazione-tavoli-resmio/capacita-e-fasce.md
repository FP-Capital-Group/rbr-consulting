# Capacità di cucina e sala: da dove viene il tetto per fascia

`trappole.md` dice che il tetto per fascia è un limite di cucina, ma non come si calcola.
Metodo generale — i numeri che seguono come esempio sono di un locale specifico e vanno
rifatti su ogni cliente, non riusati.

## Reparto più lento, dal venduto
Si separano i reparti come li vive la cucina. Per ognuno si calcolano i pezzi per coperto e il
massimo di pezzi mai prodotti in 60 minuti sullo storico, cioè i coperti/ora al record. Il
valore più basso fra i reparti è il primo cancello della serata.

## Tetto al quarto d'ora dal reparto più lento
Capacità dichiarata del reparto ÷ pezzi per coperto del giorno ÷ 4 = tetto per fascia di 15
minuti. Si calcola giorno per giorno perché il mix cambia. Morde solo nei picchi: non frena
tutta la serata, smussa solo il momento più caricato.

## I limiti del venduto
Il venduto dice quanto si è prodotto, non quanto si potrebbe produrre. Un record basso non
prova da solo che un reparto sia più lento, e la permanenza ai tavoli non lo stana da sola. La
risposta più solida è il tempo fra comanda e uscita del piatto. Attribuire la comanda all'ora
di seduta dà picchi per eccesso: va letto come stima prudente, non come misura esatta.

## Quando il vincolo è la sala, non la cucina
Con la sala piena nessun riassetto di cucina aiuta: il totale della serata è "chi entra prima
del pieno" più "i rientri dopo le rotazioni". La capienza utile esclude i tavoli di palco e
quelli fuori uso — va ricalcolata ogni volta, non presa dal totale tavoli nominale. Sopra la
capienza utile la sala non chiude nemmeno con l'assegnazione ottimale: la mossa possibile è
riaprire tavoli fuori uso, non ottimizzare di più.

## Resa al posto-ora
Il ricavo per posto-ora (importo ÷ posti ÷ permanenza in ore) cambia molto per fascia e taglia
di tavolata: le comitive grandi rendono di più tardi che presto, perché la permanenza pesa
meno sul totale della serata. È un argomento utile per decidere quando accettare un gruppo
grande, non solo se accettarlo.

## Lettura prima del servizio
Poco prima dell'apertura (es. 19:15), si confrontano i piatti/ora stimati per fascia con la
soglia del reparto più lento. Se la fascia rischia di sforare, la leva sta in sala: sui tavoli
grandi si raccoglie l'ordine appena seduti, o anche prima (telefono), per non far slittare
tutto il reparto.

---

Punti **da verificare**, non ancora provati su una serata vera: un profilo di ingressi per
mezz'ora che non sfondi né sala né cucina, il caso "serata con live a turni" (fasce di
pubblico diverse sui tavoli liberati), e un modello di capienza basato su simulazione. Non
vanno presentati al cliente come metodo collaudato finché non sono testati.

(contributo di Andrea Chirivì, 2026-10-12)
