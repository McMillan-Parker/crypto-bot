import robin_stocks as rs
import os
import datetime
import time

user = input("Username: ")
pswd = input("Password: ")

rs.robinhood.authentication.login(username=user,
         password = pswd,
         expiresIn=86400,
         by_sms=True)

#My portfolio only has 4 types of crypto, you could add more...
#Print crypto type and corresponding amounts present in portfolio:

def getCurrentPortfolio():
    #Retrieve list of lists from robinhood that contains data pertaining to crypto, eg type found in portfolio:
    currency_list=rs.robinhood.crypto.get_crypto_positions(info="currency")
    #Turn this list of lists into individual lists to make data retrieval possible:
    cvals = [list(currency_list[0].values()), list(currency_list[1].values()), list(currency_list[2].values()), list(currency_list[3].values())]
    #Retrieve list of quantity of cryptocurrency present in portfolio
    qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")

    print("Current portfolio:\n")
    for x in range (0,4):
        
        if 'BTC' in cvals[x]:
            print("BTC: ")
        elif 'DOGE' in cvals[x]:
            print("DOGE: ")
        elif 'ETH' in cvals[x]:
            print("ETH: ")
        elif 'LTC' in cvals[x]:
            print("LTC: ")
        else:
            print("unknown currency: ")
        print(qlist[x])

def checkBalance():
    cashBalance = rs.robinhood.profiles.load_account_profile(info="cash")
    print("Cash Balance: ")
    print("$" + cashBalance)

#buy crypto if it falls 5% in a day
def buyAlgo():
    file = open("config.txt")
    configdata = file.readlines()
    buyPercent = configdata[1]
    file.close()
    #initial setup:
    intialPriceBTC = rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")
    print("Intital BTC Price: $" + str(initalPriceBTC) + ".")
    now = datetime.datetime.now()
    currentminute = (now.hour * 60) + now.minute
    startMinute = currentminute
    #this var is used below:
    minuteLoop = 0
    #compare this current data point to all other data points in list. If it is differed by 5% or more, submit a buy order for BTC. Reset the price table.
    while True:
        now = datetime.datetime.now()
        currentminute = (now.hour * 60) + now.minute
        currentPriceBTC = rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")
        #the next three lines just check if I've already printed info about the current minute.
        if minuteLoop != currentminute:
            print(str(now.hour) + ":" + str(now.minute) + ". Current BTC Price: $" + str(currentPriceBTC) + ".")
        minuteLoop = currentminute
        percentage = float(currentPriceBTC)/float(initialPriceBTC) -1
        if (percentage <= (float(buyPercent)/(-100))):
            print("Price has fallen " + str(abs(percentage*100)) + "% within the last 24 hours. Buying BTC now.")
            buyCrypto()
        #wait 59 seconds so robinhood doesn't kick me for sending too many requests:
        time.sleep(59)

def sellAlgo():
    file = open("config.txt")
    configdata = file.readlines()
    sellPercent = configdata[3]
    file.close()
    #initial setup:
    initialPriceBTC = rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")
    print("Intital BTC Price: $" + str(initialPriceBTC) + ".")
    now = datetime.datetime.now()
    currentminute = (now.hour * 60) + now.minute
    startMinute = currentminute
    #this var is used below:
    minuteLoop = 0
    #compare this current data point to all other data points in list. If it is differed by 5% or more, submit a buy order for BTC. Reset the price table.
    while True:
        now = datetime.datetime.now()
        currentminute = (now.hour * 60) + now.minute
        currentPriceBTC = rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")
        #the next three lines just check if I've already printed info about the current minute.
        if minuteLoop != currentminute:
            print(str(now.hour) + ":" + str(now.minute) + ". Current BTC Price: $" + str(currentPriceBTC) + ".")
        minuteLoop = currentminute
        percentage = float(currentPriceBTC)/float(initialPriceBTC) -1
        if (percentage >= (float(sellPercent)/100)):
            print("Price has risen " + str(abs(percentage*100)) + "% within the last 24 hours. Selling BTC now.")
            sellCrypto()
        #wait 59 seconds so robinhood doesn't kick me for sending too many requests:
        time.sleep(59)

def buyCrypto():
    cashAvailable = rs.robinhood.profiles.load_account_profile(info="cash")
    amountInDollars = float(cashAvailable)
    rs.robinhood.orders.order_buy_crypto_by_price('BTC', amountInDollars, timeInForce='gtc')
    print("Sent request to purchase $" + str(amountInDollars) + " worth of BTC.")
    qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")
    while (float(qlist[0]) < 0.00013):
        qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")
        time.sleep(15)
    runAlgo()

def sellCrypto():
    qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")
    BTCquantity = float(qlist[0])
    rs.robinhood.orders.order_sell_crypto_by_quantity('BTC', BTCquantity, timeInForce='gtc')
    print("Sent request to sell " + str(BTCquantity) + " BTC at a price of $" + str(rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")) + " per BTC")
    cashAvailable = rs.robinhood.profiles.load_account_profile(info="cash")
    while (float(cashAvailable) < 5):
        cashAvailable = rs.robinhood.profiles.load_account_profile(info="cash")
        time.sleep(15)
    runAlgo()

#Chooses whether to buy or sell crypto, depending on available cash and whether or not you have BTC present.
def runAlgo():
    getCurrentPortfolio()
    print()
    checkBalance()
    print()
    cashAvailable = rs.robinhood.profiles.load_account_profile(info="cash")
    qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")
    #using $5 since sometimes there's residual cash that would be inefficient to play with/would cause problems due to tolerances.
    if float(cashAvailable) >= 5:
        print("More than $5 is in your account. Looking for an ideal time to buy crypto now.")
        buyAlgo()
    elif (float(cashAvailable) <= 5) and (float(qlist[0]) > 0):
        print("Less than $5 is in your account but you have cryptocurrency present. Looking for an ideal time to sell crypto now.")
        sellAlgo()
    else:
        print("You don't have money in your account and you don't have cryptocurrency in your account. Can't operate.")

#Prompts the user to call a function:
def prompt():
    choice = "DefaultXD"
    while choice != "Quit":
        choice = input("type function here: ")
        if choice == "getCurrentPortfolio()":
            getCurrentPortfolio()
        elif choice == "checkBalance()":
            checkBalance()
        elif choice == "runAlgo()":
            runAlgo()
        elif choice == "buyAlgo()":
            buyAlgo()
        elif choice == "sellAlgo()":
            sellAlgo()
        elif choice == "buyCrypto()":
            buyCrypto()
        elif choice == "sellCrypto()":
            sellCrypto()
        elif choice == "Quit":
            break
        else:
            print("invalid choice")

prompt()

#rs.robinhood.authentification.logout()
