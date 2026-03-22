import random
import os
import time
import json
from colorama import Fore, Style, init

# json yaratma - toxunma bura
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(BASE_DIR, 'balance.json')

def loadbal():
    # fayl yoxdusa 1000 coin ver
    if not os.path.exists(DATA_FILE):
        return 1000
    try:
        with open(DATA_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return 1000 # nese xarab olsa yene 1000 ver
    
def savebal(amount):
    with open(DATA_FILE, 'w') as f:
        json.dump(amount, f)

init(autoreset= True)
currentbal = loadbal()
# random suretli ilbizler listi
snails = {
    "Turbo": {"icon": "@$", "pos": 0, "speed": round(random.uniform(0.8, 1.3), 2), "color": Fore.CYAN},
    "Slime": {"icon": "@~", "pos": 0, "speed": round(random.uniform(0.8, 1.3), 2), "color": Fore.GREEN},
    "Shadow": {"icon": "@?", "pos": 0, "speed": round(random.uniform(0.8, 1.3), 2), "color": Fore.MAGENTA},
    "Silly": {"icon": "@!", "pos": 0, "speed": round(random.uniform(0.8, 1.3), 2), "color": Fore.RED}                                  
}

finishline = 70
logs = []

def drawtrack(bal, betname="none"):
    os.system('cls' if os.name == 'nt' else 'clear')
    print(Fore.YELLOW + Style.BRIGHT + "Snail market race") 
    print(Fore.CYAN + f"Balance: {bal} coins.")
    print(Fore.WHITE + '-' * (finishline + 15))

    for name,data in snails.items():
        space = " " * data["pos"]
        betmarker = (Fore.YELLOW +" <-- Your bet ") if name.lower() == betname.lower() else "" 
        print(f"{data['color']}{name:8} | {space}{data['icon']}{' ' * (finishline - data ['pos'])}{Fore.WHITE}🏁{betmarker}")

    print(Fore.WHITE + "-" * (finishline + 15)) 
    # son 3 event
    for log in logs[-3:]:
        print(log)

drawtrack(currentbal)
# izleyici ya da kredit hissesi
if currentbal <= 0:
    print(Fore.RED + "\n Insufficient funds!")
    print(Fore.WHITE + "1. Borrow 500 coins from the Snail Bank")
    print(Fore.WHITE + "2. Watch the race (Spectator Mode)")

    c = input("\n Your choice (1 or 2): ")

    if c == "1":
        currentbal = 500
        savebal(currentbal)
        print(Fore.GREEN + "The Bank granted you a 500 coin loan. Use it wisely!")
        print (Fore.RED + "\nWho are you betting on")
        for i,name in enumerate(snails.keys(), 1):
            print(f"{i}. {name}")

        betname = input("\nEnter snail name: ")
        betinput = input("Enter amount to bet (or type 'all'): ").lower()
        if betinput == 'all':
            betamount = currentbal
        else:
            try:
                betamount = int(betinput)
            except ValueError:
                print(Fore.RED + "Invalid ammount! Betting 0 coins...")
                betamount = 0
        if betamount < 0:
            print(Fore.RED + "Invalid bet amount! Betting 0 coins...")
            betamount = 0
    else:
        print(Fore.CYAN + "Spectator mode active. The race is about to start..")
        betname = "none"
        betamount = 0
        time.sleep(2)
else:
    betname = input("\nEnter which snail are you betting on: ").strip().lower()
    snailslw = {name.lower(): name for name in snails}
    if betname in snailslw:
        betname = snailslw[betname]

        betraw = input("Enter amount to bet (or type 'all'): ").lower()
        if betraw == 'all':
            betamount = currentbal
            print(Fore.MAGENTA + Style.BRIGHT + f"All in! Betting {betamount} coins!")
        else:
            try:
                betamount = int(betraw)
            except ValueError:
                print(Fore.RED + "Invalid input! Betting 0 coins...")
                betamount = 0
        if betamount < 0:
            print(Fore.RED + "Invalid bet amount! Betting 0 coins...")
            betamount = 0
    else:
        print(Fore.RED +"Invalid snail name! Switching to spectator mode.")
        betname = "none"
        betamount = 0
if betamount > currentbal:
    print(Fore.RED + "Not enough coins! Betting cancelled.")
    betamount = 0
    betname = "none"

temp_var = currentbal # daha sonra list ucun islet

print(Fore.YELLOW + f"\nRace is starting.. Betting {betamount} on {betname}...")
time.sleep(1.5)

raceon = True
while raceon:
    drawtrack(currentbal, betname)

    # events
    for name in snails:
        event = random.random()
        movemltp = 2

        if event < 0.03:
            movemltp = 0
            msg = f"{Fore.RED}! {name} got stuck in mud"
            logs.append(msg)
            if len(logs) > 5: # son 5 event
                logs.pop(0)
        elif event < 0.04:
            movemltp = 6
            msg = f"{Fore.CYAN}! {name} activated nitro"
            logs.append(msg)
            if len(logs) > 5:
                logs.pop(0)

        s = snails[name]["speed"]
        move = random.random() * s
        move = move * movemltp
        snails[name]["pos"] += int(move)

        if snails[name]["pos"] >= finishline:
            snails[name]["pos"] = finishline
            drawtrack(currentbal)
            winnername = name
            print (Fore.WHITE + "--------------------------------------")
            print(f"{Fore.YELLOW} Winner: {name.upper()}!")
            print(Fore.YELLOW + "\n Race Telemetry")
            for n, data in snails.items():
                print(f"{data['color']}{n:8}: {data['speed']} cm/sec")
            print (Fore.WHITE + "--------------------------------------")

            
            # balance
            if betamount > 0:
                if winnername.lower() == betname.lower():
                    gain = betamount * 2
                    currentbal += gain
                    print(Fore.YELLOW + f"You won! + {gain} coins!")
                else:
                    currentbal -= betamount
                    print(Fore.RED + f"You lost! -{betamount} coins.")
                savebal(currentbal)
                print(Fore.YELLOW + f"New balance: {currentbal} coins.")
            else:
                print(Fore.YELLOW + "No bet placed. Watching as a spectator.")
            
            raceon = False
            break
    time.sleep(0.2)