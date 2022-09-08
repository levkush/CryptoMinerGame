import os
import sys
import pyfiglet
from colorama import Fore
import random
import threading
import time

global money
global multiplier
global upgradeprice

money = 0
multiplier = 1
upgradeprice = 25
btcprice = 10000

os.system("cls")

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
    btcwatchdog = threading.Thread(target=bitcoinprice, daemon=True)
    btcwatchdog.start()
    
    CommandInterpreter()


def bitcoinprice():
    while True:
        time.sleep(5)
        
        global multiplier
        global btcprice
        global localprice
        
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
    retmoney = str(money) + " USDT"
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

