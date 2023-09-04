from collections import OrderedDict
from datetime import datetime
from modules import *
import pandas


class Agency:
    def __init__(self, airlines, clients, tickets):
        self.airlines = airlines
        self.clients = clients
        self.etickets = tickets
        self.clock = clock()
        self.capacity = self.capacities()
        self.filter = dict()
        self.isLogged = False
        self.username = None

    def signup(self, mode, parameters):
        if mode in ["POST"]:
            username = parameters["username"]
            password = parameters["password"]

            if not username in self.clients.username.values.tolist():
                client = pandas.DataFrame({
                    "username": [username], 
                    "password": [password], 
                    "wallet": [0.0]})
                self.clients = pandas.concat([self.clients, client], ignore_index=True, sort=True)
                self.save()
                self.isLogged = True
                self.username = username
                error(200)
            else:
                error(400)
        else:
            error(400)

    def login(self, mode, parameters):
        if mode in ["POST"]:
            username = parameters["username"]
            password = parameters["password"]

            if username in self.clients.username.values.tolist():
                if str(password) == str(self.clients.loc[self.clients.username == username].password.item()):
                    self.isLogged = True
                    self.username = username
                    error(200)
                else:
                    error(400)
            else:
                error(400)
        else:
            error(400)

    def logout(self, mode):
        if mode in ["POST"]:
            if self.isLogged:
                self.isLogged = False
                self.filter = dict()
                error(200)
            else:
                error(403)
        else:
            error(400)

    def wallet(self, mode, parameters):
        if mode in ["POST"]:
            if self.isLogged:
                amount = float(parameters["amount"])
                if amount <= 0.0:
                    error(400)
                else:
                    credit = float(self.clients.loc[self.clients.username == self.username].wallet.item())
                    self.clients.loc[self.clients.username == self.username, "wallet"] = credit + amount
                    self.save()
                    error(200)
            else:
                error(403)
        else:
            error(400)

    def flights(self, mode, parameters):
        if mode in ["GET"]:
            if self.isLogged:
                str = ""
                proceed = False
                if len(parameters) == 0 and len(self.filter) == 0:
                    if len(self.airlines) != 0:
                        proceed = True
                        for index, airline in self.airlines.iterrows():
                            if int(airline.seats) > 0:
                                for info in airline.tolist():
                                    str += f"{info} "
                                str += "\n"

                elif len(parameters) == 0 and len(self.filter) != 0:
                    if len(self.airlines) != 0:
                        proceed = True
                        isValid = True
                        airlines = self.airlines
                        filters = self.filter
                        clock = self.clock
                        if "min_price" in filters.keys() and "max_price" in filters.keys():
                            if float(filters["min_price"]) >= float(filters["max_price"]) or float(filters["min_price"]) < 0 or float(filters["max_price"]) < 0:
                                filters.pop("min_price")
                                filters.pop("max_price")
                                proceed = False
                                isValid = False
                                error(400)

                        if "min_price" in filters.keys():
                            if float(filters["min_price"]) >= 0:
                                airlines = airlines.loc[airlines.cost >= float(filters["min_price"])]
                                filters.pop("min_price")
                            else:
                                proceed = False
                                isValid = False
                                error(400)
                        if "max_price" in filters.keys():
                            if float(filters["max_price"]) >= 0:
                                airlines = airlines.loc[airlines.cost <= float(filters["max_price"])]
                                filters.pop("max_price")
                            else:
                                proceed = False
                                isValid = False
                                error(400)

                        if "from" in filters.keys():
                            airlines = airlines.loc[airlines.origin == filters["from"]]
                            filters.pop("from")
                        if "to" in filters.keys():
                            airlines = airlines.loc[airlines.destination == filters["to"]]
                            filters.pop("to")
                        if "departure_date" in filters.keys():
                            airlines = airlines.loc[airlines.departure_date == int(filters["departure_date"])]
                            filters.pop("departure_date")
                            if "min_departure_time" in filters.keys():
                                clock = clock[clock.index(filters["min_departure_time"]):]
                                filters.pop("min_departure_time")
                            if "max_departure_time" in filters.keys():
                                clock = clock[:(clock.index(filters["max_departure_time"]) + 1)]
                                filters.pop("max_departure_time")
                        else:
                            if "min_departure_time" in filters.keys() or "max_departure_time" in filters.keys():
                                if "min_departure_time" in filters.keys():
                                    filters.pop("min_departure_time")
                                if "max_departure_time" in filters.keys():
                                    filters.pop("max_departure_time")
                                proceed = False
                                isValid = False
                                error(400)

                        for index, airline in airlines.iterrows():
                            isCorrect = True
                            for key, value in filters.items():
                                if isValid and isCorrect and airline[key] != value:
                                    isCorrect = False
                                    break
                            if isValid and isCorrect and int(airline.seats) > 0 and airline.departure_time in clock:
                                for info in airline.tolist():
                                    str += f"{info} "
                                str += "\n"
                else:
                    id = int(parameters["id"]) - 1
                    if id < len(self.airlines) and id >= 0:
                        proceed = True
                        airlines = self.airlines.iloc[[id]]
                        if len(airlines) != 0:
                            for index, airline in airlines.iterrows():
                                for info in airline.tolist():
                                    str += f"{info} "
                                str += "\n"
                    else:
                        error(404)
                if len(str) != 0:
                    print(str, end="")
                elif proceed:
                    error(204)
            else:
                error(403)
        else:
            error(400)

    def filters(self, mode, parameters):
        if mode in ["POST", "DELETE"]:
            if self.isLogged:
                if mode == "POST":
                    self.filter.update(parameters)
                    error(200)
                elif mode == "DELETE":
                    self.filter = dict()
                    error(200)
            else:
                error(403)
        else:
            error(400)

    def tickets(self, mode, parameters):
        if mode in ["POST", "GET", "DELETE"]:
            if self.isLogged:
                if mode == "POST":
                    flight = int(parameters["flight"]) - 1
                    quantity = int(parameters["quantity"])
                    flightclass = parameters["class"]
                    type = parameters["type"]
                    cost = float(self.airlines.iloc[flight].cost.item()) * quantity

                    if len(self.airlines) > flight:
                        isValid = False
                        if flightclass == "economy" and self.capacity[flight][1] >= quantity:
                            isValid = True
                            index = 1
                        elif flightclass == "business" and self.capacity[flight][2] >= quantity:
                            isValid = True
                            index = 2
                            cost *= 2.5
                        else:
                            error(400)
                        if isValid:
                            if float(self.clients.loc[self.clients.username == self.username].wallet) >= cost:
                                seats = int(self.capacity[flight][0])
                                credit = float(self.clients.loc[self.clients.username == self.username].wallet)
                                self.airlines.loc[[flight], "seats"] = seats - quantity
                                self.clients.loc[self.clients.username == self.username, "wallet"] = credit - cost
                                self.capacity[flight][0] = int(self.capacity[flight][0]) - quantity
                                self.capacity[flight][index] = int(self.capacity[flight][index]) - quantity
                                lastticket = self.etickets.loc[self.etickets.flight == flight].sort_values(by=["ticket"], ascending=False)
                                if len(lastticket) == 0:
                                    ticket = 1
                                else:
                                    ticket = int(lastticket.iloc[0].ticket) + 1
                                
                                eticket = pandas.DataFrame({
                                    "username": [self.username],
                                    "ticket": [ticket],
                                    "flight": [flight],
                                    "airline": [self.airlines.iloc[flight].airline],
                                    "quantity": [quantity],
                                    "origin": [self.airlines.iloc[flight].origin],
                                    "destination": [self.airlines.iloc[flight].destination],
                                    "departure_date": [self.airlines.iloc[flight].departure_date],
                                    "departure_time": [self.airlines.iloc[flight].departure_time],
                                    "arrival_date": [self.airlines.iloc[flight].arrival_date],
                                    "arrival_time": [self.airlines.iloc[flight].arrival_time],
                                    "class": [flightclass],
                                    "type": [type],
                                    "cost": [cost]
                                })
                                self.etickets = pandas.concat([self.etickets, eticket], ignore_index=True, sort=True)
                                self.save()
                                print(ticket)
                            else:
                                error(400)
                    else:
                        error(404)

                elif mode == "GET":
                    if len(parameters) == 0:
                        tickets = self.etickets.loc[self.etickets.username == self.username]
                        if len(tickets) != 0:
                            for index, ticket in tickets.iterrows():
                                str = f"{ticket.ticket} {ticket.flight + 1} "
                                str += f"{ticket.airline} {ticket.quantity} "
                                str += f"{ticket.origin} {ticket.destination} "
                                str += f"{ticket.departure_date} {ticket.departure_time} "
                                str += f"{ticket.arrival_date} {ticket.arrival_time} "
                                str += f"{ticket['class']} {ticket.type} {ticket.cost}"
                                print(str)
                        else:
                            error(204)
                    else:
                        id = int(parameters["id"])
                        tickets = self.etickets.loc[self.etickets.username == self.username]
                        if len(tickets) != 0:
                            if id in tickets.ticket.tolist():
                                eticket = tickets.loc[tickets.ticket == id]
                                for index, ticket in eticket.iterrows():
                                    str = f"{ticket.ticket} {ticket.flight + 1} "
                                    str += f"{ticket.airline} {ticket.quantity} "
                                    str += f"{ticket.origin} {ticket.destination} "
                                    str += f"{ticket.departure_date} {ticket.departure_time} "
                                    str += f"{ticket.arrival_date} {ticket.arrival_time} "
                                    str += f"{ticket['class']} {ticket.type} {ticket.cost}"
                                    print(str)
                            else:
                                error(404)
                        else:
                            error(204)
                elif mode == "DELETE":
                    id = int(parameters["id"])
                    tickets = self.etickets.loc[self.etickets.username == self.username]
                    if id in tickets.ticket.tolist():
                        ticket = tickets.loc[tickets.ticket == id]
                        if ticket.type.item() == "refundable":
                            index = self.etickets.loc[(self.etickets.username == self.username) & (self.etickets.ticket == id)].index
                            self.etickets.drop(index, inplace=True)
                            credit = float(self.clients.loc[self.clients.username == self.username].wallet)
                            cost = float(ticket.cost)
                            self.clients.loc[self.clients.username == self.username, "wallet"] = credit + cost
                            self.save()
                            error(200)
                        else:
                            error(400)
                    else:
                        error(404)
            else:
                error(403)
        else:
            error(400)

    def connect(self, mode, parameters):
        if mode in ["GET"]:
            if self.isLogged:
                origin = parameters["from"]
                destination = parameters["to"]
                
                origins = self.airlines.loc[self.airlines.origin == origin]
                destinations = self.airlines.loc[self.airlines.destination == destination]

                connections = dict()

                for index, first in origins.iterrows():
                    for index, second in destinations.iterrows():
                        if first.destination == second.origin:
                            str = ""
                            departure = datetime(2022, 2, int(second.departure_date), int(second.departure_time.split(":")[0]), int(second.departure_time.split(":")[1]), 0)
                            arrival = datetime(2022, 2, int(first.arrival_date), int(first.arrival_time.split(":")[0]), int(first.arrival_time.split(":")[1]), 0)
                            duration = arrival - departure
                            seconds = duration.seconds
                            hours = seconds // 3600
                            minutes = (seconds - (hours * 3600)) // 60
                            if hours <= 23:
                                cost = float(first.cost) + float(second.cost)
                                str += "Flight 1: "
                                for info in first.tolist():
                                    str += f"{info} "
                                str += "\n----------"
                                str += "\nFlight 2: "
                                for info in second.tolist():
                                    str += f"{info} "
                                str += f"\n* Cunnection duration: {hours}h {minutes}m, Total cost: {cost}"
                                str += "\n----------"

                                connections.update({cost: str})
                if len(connections) > 0:
                    connections = OrderedDict(sorted(connections.items()))
                    for key, value in connections.items():
                        print(value)
                else:
                    error(404)
            else:
                error(403)
        else:
            error(400)

    def cheap(self, mode, parameters):
        if mode in ["GET"]:
            if self.isLogged:
                origin = parameters["from"]
                destination = parameters["to"]
                departure = int(parameters["departure_date"])

                airlines = self.airlines.loc[(self.airlines.origin == origin) & (self.airlines.destination == destination)]
                if len(airlines) != 0:
                    airlines = airlines.loc[airlines.departure_date == departure].sort_values(by=["cost"], ascending=True)
                    airline = airlines.iloc[0]
                    for info in airline.tolist():
                        print(info, end=" ")
                    print(f"\nTotal cost: {airline.cost}")
                else:
                    origins = self.airlines.loc[self.airlines.origin == origin]
                    destinations = self.airlines.loc[self.airlines.destination == destination]
                    connections = dict()

                    for index, first in origins.iterrows():
                        for index, second in destinations.iterrows():
                            if first.destination == second.origin and int(first.departure_date) == departure:
                                str = ""
                                cost = float(first.cost) + \
                                    float(second.cost)
                                for info in first.tolist():
                                    str += f"{info} "
                                str += "\n"
                                for info in second.tolist():
                                    str += f"{info} "
                                str += f"\nTotal cost: {cost}"
                                connections.update({cost: str})

                    if len(connections) > 0:
                        connections = OrderedDict(sorted(connections.items()))
                        print(connections[list(connections.keys())[0]])
                    else:
                        error(404)
            else:
                error(403)
        else:
            error(400)

    def report(self, mode):
        if mode in ["GET"]:
            if self.isLogged:
                average = "{:.2f}".format(float(self.airlines.cost.mean()))
                min = "{:.2f}".format(float(self.airlines.cost.min()))
                max = "{:.2f}".format(float(self.airlines.cost.max()))

                airlines = dict()
                destinations = dict()

                for index, ticket in self.etickets.iterrows():
                    if ticket.airline in airlines.keys():
                        airlines[ticket.airline] += int(ticket.quantity)
                    else:
                        airlines.update({ticket.airline: 0})

                    if ticket.destination in destinations.keys():
                        destinations[ticket.destination] += int(ticket.quantity)
                    else:
                        destinations.update({ticket.destination: 0})
                
                airlines = dict(sorted(airlines.items(), key=lambda x:x[1]))
                destinations = dict(sorted(destinations.items(), key=lambda x:x[1]))

                most = list(destinations.keys())[-1]
                top = f"{list(airlines.keys())[-1]} {list(airlines.keys())[-2]} {list(airlines.keys())[-3]}"

                print(f"average_flight_cost: {average}")
                print(f"min_flight_cost: {min}")
                print(f"max_flight_cost: {max}")
                print(f"most_popular_destination: {most}")
                print(f"top_airlines: {top}")
            else:
                error(403)
        else:
            error(400)

    def capacities(self):
        airlines = {}
        for index, airline in self.airlines.iterrows():
            economic = int(airline.seats * 0.75)
            business = int(airline.seats - economic)
            airlines.update({index: [airline.seats, economic, business]})

        return airlines

    def save(self):
        self.airlines.to_csv("files/airlines.csv", index=False)
        self.clients.to_csv("files/clients.csv", index=False)
        self.etickets.to_csv("files/tickets.csv", index=False)
