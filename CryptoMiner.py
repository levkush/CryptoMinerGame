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

# Color init
fred = Fore.RED
fyellow = Fore.YELLOW
fgreen = Fore.GREEN
fcyan = Fore.CYAN
fblue = Fore.BLUE
fmagenta = Fore.MAGENTA
fwhite = Fore.WHITE
fblack = Fore.BLACK

# Language selection
lang = input("What is your language? / Какой у вас язык? [en/RU]: ").lower().strip()

if lang == "ru" or "en":
    pass
else:
    print("Unknown language.")
    sys.exit()

# Game Saving
def Save(money, multiplier, upgradeprice):
    print(money)
    if not os.path.exists(os.path.expanduser('~') + "/.CryptoMiner"):
        os.mkdir(os.path.expanduser('~') + "/.CryptoMiner")
        
    os.chdir(os.path.expanduser('~') + "/.CryptoMiner")
    
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
        if lang == "ru":
            print(f"{fgreen}Игра сохранена!")
        else:
            print(f"{fgreen}Game saved!")

# Game Loading
def Load():
    os.chdir(os.path.expanduser('~') + "/.CryptoMiner")    
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

# Rounding: Millions to M, Billions to B, Trillions to T.
def human_format(num, round_to=2):
    magnitude = 0
    while abs(num) >= 1000:
        magnitude += 1
        num = round(num / 1000.0, round_to)
    return '{:.{}f}{}'.format(num, round_to, ['', 'K', 'M', 'B', 'T', 'Q'][magnitude])


# Check for saves
def SaveCheck():
    if os.path.exists(os.path.expanduser('~') + "/.CryptoMiner"):
        Load()
        if lang == "ru":
            print("Прогресс восстановлен!")
        else:
            print("Progress backuped!")
        return None
    
    # If no saves defaulting
    global money
    global multiplier
    global upgradeprice
    
    money = 0
    multiplier = 1
    upgradeprice = 25

# Assign variables
btcprice = 10000
getbtc = 0
getmoney = 0


# Check the system type and clear console
if os.name == "nt":
    os.system("cls")
else:
    os.system("clear")

# Cool logo with cool font
print(fgreen, pyfiglet.figlet_format("CryptoMiner"))

# Main function
def main(): 
    SaveCheck()
    
    btcwatchdog = threading.Thread(target=bitcoinprice, daemon=True)
    btcwatchdog.start()
    
    CommandInterpreter()
    

# Bitcoin volatility and autosaves
def bitcoinprice():
    while True:
        time.sleep(60)
        
        global multiplier
        global btcprice
        global localprice
        global money
        global upgradeprice
        global lang
        
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
            if lang == "ru":
                print(f"\n\n{fgreen}:) {fyellow}Биткойн {fwhite}подорожал. Новая цена: {fgreen}{btcprice}${fwhite}.\n")
            else:
                print(f"\n\n{fgreen}:) {fyellow}Bitcoin {fwhite}has risen in price. New price: {fgreen}{btcprice}${fwhite}.\n")
            continue
            
        elif up == False:
            btcprice = round(btcprice - (percentage * btcprice))
            multiplier = round(multiplier - (percentage * multiplier), 1)
            
            if lang == "ru":
                print(f"\n\n{fred}:( {fyellow}Биткойн {fwhite}упал в цене. Новая цена: {fgreen}{btcprice}${fwhite}.\n")
            else:
                print(f"\n\n{fred}:( {fyellow}Bitcoin {fwhite}fell in price. New price: {fgreen}{btcprice}${fwhite}.\n")      
        


# Earn money by mining
def mine(mult):
    global money
    global getmoney
    global getbtc
    
    getmoney = 1 * mult
    getbtc = getmoney / 1000
    
    money = money + getmoney
    
    getmoney = human_format(getmoney)
    
    if lang == "ru":
        print(f"Вы добыли {fyellow}{getbtc} BTC{fwhite} и обменяли на {fgreen}{getmoney}${fwhite}.")
    else:
        print(f"You have mined {fyellow}{getbtc} BTC{fwhite} and exchanged for {fgreen}{getmoney}${fwhite}.")
    
def upgrade():
    global multiplier
    global upgradeprice
    global money
    if money > upgradeprice:
        money = money - upgradeprice
        multiplier = round(multiplier * 1.5, 1)
        upgradeprice = upgradeprice * 1.5
        upgradeprice_human = human_format(upgradeprice)
        
        if lang == "ru":
            print(f"Вы прокачали ваши мощности! Новая цена прокачки {upgradeprice_human}$.")
        else:
            print(f"You have upgraded your powers! The new upgrade price is {upgradeprice_human}$.")
           
    else:
        if lang == "ru":
            print(f"У вас недостаточно средств. Вам нужно {upgradeprice_human}")
        else:
            print(f"You don't have enough funds. You need {upgradeprice_human}")

# Function that returns balance of a player
def balance():
    global money
    money = round(money, 2)
    retmoney = human_format(money) + "$"
    return retmoney

# Help command
def CommandList():
    len_now = 0
    CommandList = ["help", "m", "upgrade", "money", "btc", "save"]
    if lang == "ru":
        DescriptionList = ["- Вывести это сообщение.", "- Добывает биткойн и увеличивает ваш баланс.", "- Обновляет ваши видеокарты. Дает прирост к заработку.", "- Выводит количиство ваших денег.", "- Курс биткойна сейчас.", "- Сохраняет игру."]
    else:
        DescriptionList = ["- Display this message.", "- Mines bitcoin and increases your balance.", "- Upgrades your video cards. Gives an increase in earnings.", "- Displays the amount of your money.", "- Bitcoin rate now.", "- Saves the game."]
    while len_now < len(DescriptionList) and len_now < len(CommandList):
        print(fyellow + CommandList[len_now] + fwhite + ' ' + DescriptionList[len_now])
        len_now = len_now + 1

# Command interpreter (Main control panel)
def CommandInterpreter():
    global money
    global multiplier
    global upgradeprice
    exitlist = ["exit", "leave", "q", "quit"]
    while True:
        try:
            command = input(fblue + "> " + fwhite).lower().split()
            
        except KeyboardInterrupt:
            if lang == "ru":
                print("Выходим...")
            else:
                print("Exiting...")
            sys.exit()
            
        if command == None or "":
            continue
        try:
            if command[0] == "help":
                if lang == "ru":
                    print("Все команды: \n")
                else:
                    print("All commands: \n")
                CommandList()
                continue
        except Exception:
            continue
        
        if command[0] == "m":
            mine(multiplier)
            
        elif command[0] == "money":
            print(balance())
        
        elif command[0] == "iusearchbtw":
            money = 1000000
            
        elif command[0] == "btc":
            if lang == "ru":
                print(f"Цена биткойна: {fyellow}{btcprice}$")
            else:
                print(f"Bitcoin price is: {fyellow}{btcprice}$")

        elif command[0] == "upgrade":
            upgrade()
        elif command[0] == "save":
            Save(money, multiplier, upgradeprice)
            if lang == "ru":
                print(f"{fgreen}Игра сохранена!")
            else:
                print(f"{fgreen}Game saved!")
            
        elif command[0] in exitlist:
            if lang == "ru":
                print("Выходим...")
            else:
                print("Exiting...")
            sys.exit()
            
        else:
            if lang == "ru":
                print("Неизвестная команда. Напишите 'help' для помощи.")
            else:
                print("Unknown command. Type 'help' for help.")

main()



