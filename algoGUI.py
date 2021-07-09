import PySimpleGUI as sg
import robin_stocks as rs
import os
import datetime
import time

'''
FUNCTIONS UTILIZED BY ALL
'''

def checkBalance():
    cashBalance = rs.robinhood.profiles.load_account_profile(info="cash")
    currency_list=rs.robinhood.crypto.get_crypto_positions(info="currency")
    #Turn this list of lists into individual lists to make data retrieval possible:
    cvals = [list(currency_list[0].values()), list(currency_list[1].values()), list(currency_list[2].values()), list(currency_list[3].values())]
    #Retrieve list of quantity of cryptocurrency present in portfolio
    qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")
    BTCbalance = qlist[0]
    return [cashBalance, BTCbalance]

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

def buyCrypto():
    cashAvailable = rs.robinhood.profiles.load_account_profile(info="cash")
    amountInDollars = float(cashAvailable)
    rs.robinhood.orders.order_buy_crypto_by_price('BTC', amountInDollars, timeInForce='gtc')
    print("Sent request to purchase $" + str(amountInDollars) + " worth of BTC.")
    chooseRunAlgo()

def sellCrypto():
    qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")
    BTCquantity = float(qlist[0])
    rs.robinhood.orders.order_sell_crypto_by_quantity('BTC', BTCquantity, timeInForce='gtc')
    print("Sent request to sell " + str(BTCquantity) + " BTC at a price of $" + str(rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")) + " per BTC")
    chooseRunAlgo()

def chooseRunAlgo():
    #determine whether to go to runSimpleAlgo, runVelAlgo, runAccelAlgo, or runfcAlgo
    if determineAlgo == 'simple':
        runSimpleAlgo()
    elif determineAlgo == 'velocity':
        runVelAlgo()

'''
START VELOCITY ALGO STUFF
'''

def velAlgoWindow():
    global determineAlgo
    determineAlgo = 'velocity'
    # All the stuff inside your window.
    layoutVelocity = [  [sg.Text('If BTC drops '), sg.InputText(size=(3,1)), sg.Text('% in a '), sg.InputText(size=(3,1)), sg.Text('minute period, buy.')],
                        [sg.Text('If BTC rises '), sg.InputText(size=(3,1)), sg.Text('% in a '), sg.InputText(size=(3,1)), sg.Text('minute period, sell.')],
                        [sg.Button('GO')],
                        [sg.Multiline(size=(50,6), key='multiline', disabled=True)]  ]
    # Create the Window
    windowVelocity = sg.Window('Velocity Algorithm', layoutVelocity)
    windowVelocity.finalize()
    windowVelocity.BringToFront()
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = windowVelocity.read()
        if event == 'GO':
            BTCdrop = values[0]
            minutesDrop = values[1]
            BTCrise = values[2]
            minutesRise = values[3]
            #pass values[0-3] (percentiles, minutes) through... 
            runVelAlgo(BTCdrop, minutesDrop, BTCrise, minutesRise, windowVelocity)
        elif event == sg.WIN_CLOSED: # if user closes window
            break
        
def runVelAlgo(BTCdrop, minutesDrop, BTCrise, minutesRise, windowVelocity):
    #Startup stuff displayed in multiline textbox
    windowVelocity.refresh()
    windowVelocity['multiline'].update(value=('Start time: ' + str(datetime.datetime.now()) + '\n'), append=True)
    windowVelocity.refresh()
    balance = checkBalance()
    cashBalance = balance[0]
    BTCbalance = balance[1]
    windowVelocity['multiline'].update(value=('Current Cash balance: $' + str(cashBalance) + '\n'), append=True)
    windowVelocity['multiline'].update(value=('Current BTC balance: ' + str(BTCbalance) + 'BTC \n'), append=True)
    windowVelocity.refresh()
    
    cashAvailable = rs.robinhood.profiles.load_account_profile(info="cash")
    qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")
    #using $5 since sometimes there's residual cash that would be inefficient to play with/would cause problems due to tolerances.
    if float(cashAvailable) > 5:
        windowVelocity['multiline'].update(value=('More than $5 is in your account. Looking for an ideal time to buy crypto now.' + '\n'), append=True)
        windowVelocity.refresh()
        buyVelAlgo(BTCdrop, minutesDrop, windowVelocity)
    elif (float(cashAvailable) <= 5) and (float(qlist[0]) > 0):
        windowVelocity['multiline'].update(value=('Less than $5 is in your account but you have cryptocurrency present. Looking for an ideal time to sell crypto now.' + '\n'), append=True)
        windowVelocity.refresh()
        sellVelAlgo(BTCrise, minutesRise, windowVelocity)
    else:
        windowVelocity['multiline'].update(value=("You don't have money in your account and you don't have cryptocurrency in your account. Can't operate." + '\n'), append=True)
        windowVelocity.refresh()

def buyVelAlgo(BTCdrop, minutesDrop, windowVelocity):
    buyPercent = float(BTCdrop) / 100
    #initial list setup:
    pricetableBTC = list(range(1440))
    for x in range(0,1440):
        pricetableBTC[x] = 0
    now = datetime.datetime.now()
    currentminute = (now.hour * 60) + now.minute
    startMinute = currentminute
    #this var is used below:
    minuteLoop = 0
    #compare this current data point to all other data points in list. If it is differed by 5% or more, submit a buy order for BTC. Reset the price table.
    while True:
        now = datetime.datetime.now()
        currentminute = (now.hour * 60) + now.minute
        pricetableBTC[currentminute] = rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")
        #the next three lines just check if I've already printed info about the current minute.
        if minuteLoop != currentminute:
            windowVelocity['multiline'].update(value=(str(now.hour) + ":" + str(now.minute) + ": $" + str(pricetableBTC[currentminute]) + " per BTC." + '\n'), append=True)
            windowVelocity.refresh()
        minuteLoop = currentminute
        for x in range (int(minutesDrop), 0, -1):
            if (float(pricetableBTC[currentminute - x]) != 0):
                if ((((float(pricetableBTC[currentminute])/float(pricetableBTC[currentminute - x])) -1) >= buyPercent)):
                    windowVelocity['multiline'].update(value=("Price has fallen " + str((abs(float(prictableBTC[currentminute])/float(pricetableBTC[currentminute - x])) -1)*100)
                                                              + "% in the last " + str(x) + " minutes. Buying BTC now." + '\n'), append=True)
                    windowVelocity.refresh()
                    buyCrypto()
        #wait 59 seconds so robinhood doesn't kick me for sending too many requests:
        windowVelocity.read(timeout=59000)

def sellVelAlgo(BTCrise, minutesRise, windowVelocity):
    sellPercent = float(BTCrise) / 100
    #initial list setup:
    pricetableBTC = list(range(1440))
    for x in range(0,1440):
        pricetableBTC[x] = 0
    now = datetime.datetime.now()
    currentminute = (now.hour * 60) + now.minute
    startMinute = currentminute
    #this var is used below:
    minuteLoop = 0
    #compare this current data point to all other data points in list. If it is differed by 5% or more, submit a buy order for BTC. Reset the price table.
    while True:
        now = datetime.datetime.now()
        currentminute = (now.hour * 60) + now.minute
        pricetableBTC[currentminute] = rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")
        #the next three lines just check if I've already printed info about the current minute.
        if minuteLoop != currentminute:
            windowVelocity['multiline'].update(value=(str(now.hour) + ":" + str(now.minute) + ": $" + str(pricetableBTC[currentminute]) + " per BTC." + '\n'), append=True)
            windowVelocity.refresh()
        minuteLoop = currentminute
        for x in range (int(minutesRise), 0, -1):
            if (float(pricetableBTC[currentminute - x]) != 0): 
                if ((((float(pricetableBTC[currentminute])/float(pricetableBTC[currentminute - x])) -1) <= -sellPercent)):
                    windowVelocity['multiline'].update(value=("Price has risen " + str(abs(float(prictableBTC[currentminute])/float(pricetableBTC[currentminute - x]))*100)
                                                              + "% in the last "+str(x)+" minutes. Buying BTC now." + '\n'), append=True)
                    windowVelocity.refresh()
                    sellCrypto()
        #wait 59 seconds so robinhood doesn't kick me for sending too many requests:
        windowVelocity.read(timeout=59000)    

'''
END VELOCITY ALGO STUFF
'''



'''
START SIMPLE ALGO STUFF
'''

def simpleAlgoWindow():
    # All the stuff inside your window.
    layoutSimple = [  [sg.Text('If BTC drops '), sg.InputText(size=(3,1)), sg.Text('%, buy.')],
                        [sg.Text('If BTC rises '), sg.InputText(size=(3,1)), sg.Text('%, sell.')],
                        [sg.Button('GO')],
                        [sg.Multiline(size=(50,6), key='multiline', disabled=True)]  ]
    # Create the Window
    windowSimple = sg.Window('Simple Algorithm', layoutSimple)
    windowSimple.finalize()
    windowSimple.BringToFront()
    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = windowSimple.read()
        if event == 'GO':
            BTCdrop = values[0]
            BTCrise = values[1]
            #pass values[0-1] (percentiles) through... 
            runSimpleAlgo(BTCdrop, BTCrise, windowSimple)
        elif event == sg.WIN_CLOSED: # if user closes window
            break  

def runSimpleAlgo(BTCdrop, BTCrise, windowSimple):

    #Startup stuff displayed in multiline textbox
    windowSimple.refresh()
    windowSimple['multiline'].update(value=('Start time: ' + str(datetime.datetime.now()) + '\n'), append=True)
    windowSimple.refresh()
    balance = checkBalance()
    cashBalance = balance[0]
    BTCbalance = balance[1]
    windowSimple['multiline'].update(value=('Current Cash balance: $' + str(cashBalance) + '\n'), append=True)
    windowSimple['multiline'].update(value=('Current BTC balance: ' + str(BTCbalance) + 'BTC \n'), append=True)
    windowSimple.refresh()
    
    cashAvailable = rs.robinhood.profiles.load_account_profile(info="cash")
    qlist = rs.robinhood.crypto.get_crypto_positions(info="quantity_available")
    #using $5 since sometimes there's residual cash that would be inefficient to play with/would cause problems due to tolerances.
    if float(cashAvailable) > 5:
        windowSimple['multiline'].update(value=('More than $5 is in your account. Looking for an ideal time to buy crypto now.' + '\n'), append=True)
        windowSimple.refresh()
        buySimpleAlgo(BTCdrop, windowSimple)
    elif (float(cashAvailable) <= 5) and (float(qlist[0]) > 0):
        windowSimple['multiline'].update(value=('Less than $5 is in your account but you have cryptocurrency present. Looking for an ideal time to sell crypto now.' + '\n'), append=True)
        windowSimple.refresh()
        sellSimpleAlgo(BTCrise, windowSimple)
    else:
        windowSimple['multiline'].update(value=("You don't have money in your account and you don't have cryptocurrency in your account. Can't operate." + '\n'), append=True)
        windowSimple.refresh() 

def buySimpleAlgo(BTCdrop, windowSimple):
    buyPercent = BTCdrop
    #initial list setup:
    pricetableBTC = list(range(1440))
    for x in range(0,1440):
        pricetableBTC[x] = 0
    now = datetime.datetime.now()
    currentminute = (now.hour * 60) + now.minute
    startMinute = currentminute
    #this var is used below:
    minuteLoop = 0
    #compare this current data point to all other data points in list. If it is differed by 5% or more, submit a buy order for BTC. Reset the price table.
    while True:
        now = datetime.datetime.now()
        currentminute = (now.hour * 60) + now.minute
        pricetableBTC[currentminute] = rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")
        #the next three lines just check if I've already printed info about the current minute.
        if minuteLoop != currentminute:
            windowSimple['multiline'].update(value=(str(now.hour) + ":" + str(now.minute) + ": $" + str(pricetableBTC[currentminute]) + " per BTC." + '\n'), append=True)
            windowSimple.refresh()
        minuteLoop = currentminute
        percentage = float(pricetableBTC[currentminute])/float(pricetableBTC[startMinute]) -1
        if (percentage <= (float(buyPercent)/(-100))):
            windowSimple['multiline'].update(value=("Price has fallen " + str(abs(percentage*100)) + "% since algorithm startup. Buying BTC now." + '\n'), append=True)
            windowSimple.refresh()
            buyCrypto()
        #wait 59 seconds so robinhood doesn't kick me for sending too many requests:
        windowSimple.read(timeout=59000)

def sellSimpleAlgo(BTCrise, windowSimple):
    sellPercent = BTCrise
    #initial list setup:
    pricetableBTC = list(range(1440))
    for x in range(0,1440):
        pricetableBTC[x] = 0
    now = datetime.datetime.now()
    currentminute = (now.hour * 60) + now.minute
    startMinute = currentminute
    #this var is used below:
    minuteLoop = 0
    #compare this current data point to all other data points in list. If it is differed by 5% or more, submit a buy order for BTC. Reset the price table.
    while True:
        now = datetime.datetime.now()
        currentminute = (now.hour * 60) + now.minute
        pricetableBTC[currentminute] = rs.robinhood.crypto.get_crypto_quote("BTC", info="ask_price")
        #the next three lines just check if I've already printed info about the current minute.
        if minuteLoop != currentminute:
            windowSimple['multiline'].update(value=(str(now.hour) + ":" + str(now.minute) + ": $" + str(pricetableBTC[currentminute]) + " per BTC." + '\n'), append=True)
            windowSimple.refresh()
        minuteLoop = currentminute
        percentage = float(pricetableBTC[currentminute])/float(pricetableBTC[startMinute]) -1
        if (percentage >= (float(sellPercent)/100)):
            windowSimple['multiline'].update(value=("Price has risen " + str(abs(percentage*100)) + "% since algorithm startup. Selling BTC now." + '\n'), append=True)
            windowSimple.refresh()
            sellCrypto()
        #wait 59 seconds so robinhood doesn't kick me for sending too many requests:
        windowSimple.read(timeout=59000)
 

'''
END SIMPLE ALGO STUFF
'''


'''
START PROGRAM
'''
    
sg.theme('Dark Blue 3')   # Add a touch of color

layoutLogin = [  [sg.Text('Login Info:')],
                 [sg.Text('username: ', size=(7,1)), sg.InputText()],
                 [sg.Text('password: ', size=(7,1)), sg.InputText(password_char='*')],
                 [sg.Button('GO')]  ]
windowLogin = sg.Window('Login', layoutLogin)
windowLogin.finalize()
while True:
    event, values = windowLogin.read()
    if event == 'GO':
        sg.Popup('Attempting to log you in. After closing this, check the command prompt and enter the SMS code sent to your device.')
        username = values[0]
        password = values[1]
        #pass values[1-3] through... percentiles and login info
        rs.robinhood.authentication.login(username=username,
         password = password)
        layoutAlgoChoice = [  [sg.Button('Simple')],
                              [sg.Button('Velocity')],
                              [sg.Button('Acceleration')],
                              [sg.Button('Floor/Ceiling')] ]
        windowAlgoChoice = sg.Window('Choice', layoutAlgoChoice)
        windowAlgoChoice.finalize()
        windowLogin.close()
        del windowLogin
        windowAlgoChoice.BringToFront()
        while True:
            event, values = windowAlgoChoice.read()
            if event == 'Simple':
                #go to Simple algorithm window
                windowAlgoChoice.close()
                del windowAlgoChoice
                simpleAlgoWindow()
            elif event == 'Velocity':
                #Go to Velocity algo window
                windowAlgoChoice.close()
                del windowAlgoChoice
                velAlgoWindow()
            elif event == 'Acceleration':
                #go to acceleration algo Window
                windowAlgoChoice.close()
                del windowAlgoChoice
                accelAlgoWindow()
            elif event == 'Floor/Ceiling':
                #go to Floor/Ceiling algo Window
                windowAlgoChoice.close()
                del windowAlgoChoice
                fcAlgoWindow()
            elif event == sg.WIN_CLOSED: # if user closes window
                break

windowLogin.close()
