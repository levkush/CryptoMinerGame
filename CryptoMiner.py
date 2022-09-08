# Imports
import os
import sys
import pyfiglet
from colorama import Fore
import random
import threading
import time
import json
import base64

# Saving
def Save(money, multiplier, upgradeprice):
    print(money)
    if not os.path.exists(os.environ['HOME'] + "/.CryptoMiner"):
        os.mkdir(os.environ['HOME'] + "/.CryptoMiner")
        
    os.chdir(os.environ['HOME'] + "/.CryptoMiner")
    
    # Data to be written
    dictionary = {
        "money" : money,
        "upgradeprice" : upgradeprice,
        "multiplier" : multiplier,
    }

    # Serializing json 
    json_object = json.dumps(dictionary, indent = 4)
    
    # Writing
    with open("save.json", "w", encoding="utf-8") as outfile:
        outfile.write(json_object)
        print("Saved!")

# Loading
def Load():
    os.chdir(os.environ['HOME'] + "/.CryptoMiner")    
    # Opening JSON file
    with open('save.json', 'r') as openfile:
        # Reading from json file
        save = json.load(openfile)

    global money
    global multiplier
    global upgradeprice
    
    money = save["money"]
    upgradeprice = save["upgradeprice"]
    multiplier = save["multiplier"]

# Check for saves
def SaveCheck():
    if os.path.exists(os.environ['HOME'] + "/.CryptoMiner"):
        Load()
        print("Progress backuped!")
        return None
    
    # If no saves defaulting
    global money
    global multiplier
    global upgradeprice
    
    money = 0
    multiplier = 1
    upgradeprice = 25
    
btcprice = 10000


# Check the system type and clear console
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

fred = Fore.RED
fyellow = Fore.YELLOW
fgreen = Fore.GREEN
fcyan = Fore.CYAN
fblue = Fore.BLUE
fmagenta = Fore.MAGENTA
fwhite = Fore.WHITE
fblack = Fore.BLACK

print(fgreen, pyfiglet.figlet_format("CryptoFarmer"))

def main(): 
    SaveCheck()
    
    btcwatchdog = threading.Thread(target=bitcoinprice, daemon=True)
    btcwatchdog.start()
    
    CommandInterpreter()

def bitcoinprice():
    while True:
        time.sleep(5)
        
        global multiplier
        global btcprice
        global localprice
        global money
        global upgradeprice
        
        Save(money, multiplier, upgradeprice)
        
        percentage = random.randint(10, 20)
        percentage = (percentage / 100)
        
        up = random.choice([True, False])
        
        if btcprice < 6000:
            up = True
            
        elif btcprice > 14000:
            up = False
        
        if up == True:
            btcprice = round(btcprice + (percentage * btcprice))
            multiplier = round(multiplier + (percentage * multiplier), 1)
            
            print(f"\n\n{fgreen}:) {fyellow}Биткойн {fwhite}подорожал. Новая цена: {fgreen}{btcprice}${fwhite}.\n")
            continue
            
        elif up == False:
            btcprice = round(btcprice - (percentage * btcprice))
            multiplier = round(multiplier - (percentage * multiplier), 1)
            
            print(f"\n\n{fred}:( {fyellow}Биткойн {fwhite}упал в цене. Новая цена: {fgreen}{btcprice}${fwhite}.\n")       
        



def mine(mult):
    global money
    getmoney = 1 * mult
    getbtc = getmoney / 1000
    money = money + getmoney
    print(f"Вы добыли {fyellow}{getbtc} BTC{fwhite} и обменяли на {fgreen}{getmoney}${fwhite}.")
    
def upgrade():
    global multiplier
    global upgradeprice
    global money
    if money > upgradeprice:
        money = money - upgradeprice
        multiplier = round(multiplier * 1.5, 1)
        upgradeprice = upgradeprice * 1.5
        
        print(f"Вы прокачали ваши мощности! Новая цена прокачки {upgradeprice}$.")
           
    else:
        print(f"У вас недостаточно средств. Вам нужно {upgradeprice}")
    
def balance():
    global money
    money = round(money, 2)
    retmoney = str(money) + "$"
    return retmoney

def CommandList():
    len_now = 0
    CommandList = ["help", "m", "upgrade", "money", "btc"]
    DescriptionList = ["- Вывести это сообщение.", "- Добывает биткойн и увеличивает ваш баланс.", "- Обновляет ваши видеокарты. Дает прирост к заработку.", "- Выводит количиство ваших денег.", "- Курс биткойна сейчас"]
    while len_now < len(DescriptionList) and len_now < len(CommandList):
        print(fyellow + CommandList[len_now] + fwhite + ' ' + DescriptionList[len_now])
        len_now = len_now + 1

def CommandInterpreter():
    exitlist = ["exit", "leave", "q", "quit"]
    while True:
        try:
            command = input(fblue + "> " + fwhite).lower().split()
            
        except KeyboardInterrupt:
            print("\nВыходим...")
            sys.exit()
            
        if command == None or "":
            continue
        try:
            if command[0] == "help":
                print("All commands: \n")
                CommandList()
        except Exception:
            continue
        
        if command[0] == "m":
            mine(multiplier)
            
        elif command[0] == "money":
            print(balance())
            
        elif command[0] == "btc":
            print(btcprice)

        elif command[0] == "upgrade":
            upgrade()
            
        elif command[0] in exitlist:
            print("Выходим...")
            sys.exit()
            
        else:
            print("Неизвестная команда.")

main()

