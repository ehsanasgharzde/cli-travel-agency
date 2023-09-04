import pandas
from agency import Agency
from handler import Handler


path = input("./utravel.out ")

airlines = pandas.read_csv(path)
clients = pandas.read_csv("files/clients.csv")
tickets = pandas.read_csv("files/tickets.csv")

try:
    airlines.drop(["Unnamed: 0"], axis=1, inplace=True)
except:
    pass

try:
    clients.drop(["Unnamed: 0"], axis=1, inplace=True)
except:
    pass

try:
    tickets.drop(["Unnamed: 0"], axis=1, inplace=True)
except:
    pass

agency = Agency(airlines, clients, tickets)
handler = Handler(agency)

if __name__ == "__main__":
    handler.main() 
