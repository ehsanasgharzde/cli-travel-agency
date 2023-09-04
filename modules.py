ACTIONS = ["POST", "GET", "DELETE"]
FUNCTIONS = ["signup", "login", "logout", "wallet", "flights", "filters", "tickets", "connecting_flights", "cheapest_flight", "overall_report", "reset", "exit"]
CLOCK = []


H200 = "OK"
H204 = "Empty"
H400 = "Bad Request"
H403 = "Permission Denied"
H404 = "Not Found"


def clock():
    hour = 1
    minute = 0
    
    while not hour > 23:
        if minute > 59:
            hour += 1
            minute = 0

        H = f"{hour}"
        if hour < 10:
            H = f"0{hour}"
        M = f"{minute}"
        if minute < 10:
            M = f"0{minute}"

        CLOCK.append(f"{H}:{M}")
        minute += 1
        
    CLOCK[-1] = "00:00"
    return CLOCK

def red(text):
    print("\033[91m" + text + "\033[0m")

def green(text):
    print("\033[92m" + text + "\033[0m")

def yellow(text):
    print("\033[93m" + text + "\033[0m")

def error(code):
    if code == 200:
        green(H200)
    elif code == 204:
        yellow(H204)
    elif code == 400:
        red(H400)
    elif code == 403:
        red(H403)
    elif code == 404:
        yellow(H404)
