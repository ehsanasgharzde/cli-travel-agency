from modules import *
import pandas


class Handler:
    def __init__(self, agancy):
        self.agency = agancy

    def inputs(self):
        info = input()
        info = info.replace(" ?", "")
        info = info.split(" ")
        action, function, arguments = info[0], info[1], info[2:]

        parameters = {}
        for index in range(0, len(arguments), 2):
            try:
                integer = int(arguments[index + 1])
                double = float(arguments[index + 1])
                if integer == double:
                    arguments[index + 1] = int(arguments[index + 1])
                else:
                    arguments[index + 1] = float(arguments[index + 1])
            except:
                pass
            parameters.update({arguments[index]: arguments[index + 1]})

        return action, function, parameters

    def save(self):
        self.agency.airlines.to_csv("files/airlines.csv", index=False)
        self.agency.clients.to_csv("files/clients.csv", index=False)
        self.agency.etickets.to_csv("files/tickets.csv", index=False)

    def reset(self):
        tickets = pandas.DataFrame({
            "username": [],
            "ticket": [],
            "flight": [],
            "airline": [],
            "quantity": [],
            "origin": [],
            "destination": [],
            "departure_date": [],
            "departure_time": [],
            "arrival_date": [],
            "arrival_time": [],
            "class": [],
            "type": [],
            "cost": []
        })

        clients = pandas.DataFrame({
            "username": [],
            "password": [],
            "wallet": []
            })

        tickets.to_csv("files/tickets.csv", index=False)
        clients.to_csv("files/clients.csv", index=False)

    def main(self):
        while True:
            action, function, parameters = self.inputs()

            if action in ACTIONS:
                if function in FUNCTIONS:
                    if function == "signup":
                        self.agency.signup(action, parameters)
                    elif function == "login":
                        self.agency.login(action, parameters)
                    elif function == "logout":
                        self.agency.logout(action)
                        self.save()
                    elif function == "wallet":
                        self.agency.wallet(action, parameters)
                    elif function == "flights":
                        self.agency.flights(action, parameters)
                    elif function == "filters":
                        self.agency.filters(action, parameters)
                    elif function == "tickets":
                        self.agency.tickets(action, parameters)
                    elif function == "connecting_flights":
                        self.agency.connect(action, parameters)
                    elif function == "cheapest_flight":
                        self.agency.cheap(action, parameters)
                    elif function == "overall_report":
                        self.agency.report(action)
                    elif function == "reset":
                        self.reset()
                        error(200)
                    elif function == "exit":
                        self.save()
                        break
                else:
                    error(404)
            else:
                error(400)
