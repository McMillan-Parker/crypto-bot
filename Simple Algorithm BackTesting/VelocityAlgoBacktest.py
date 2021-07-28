import csv
import multiprocessing as mp
# Using readlines()
file1 = open('btc2021.txt', 'r')
priceDataLines = file1.readlines()
file1.close()
risePercent=0
fallPercent=0
#future variable specifications:
#risePercent is the rise percentage bound
#fallPercent is the fall percentage bound
#minutesRise is the minutes associated with buying velocity
#MinutesFall is the minutes associated with selling velocity

def function1():
    for x in range (0,5):
        risePercent = x*0.0025 #0.25% increase each loop
        for y in range (0,21):
            fallPercent =y*0.0025 #0.25% increase each loop
            for a in range(1,21):
                minutesRise = a
                for b in range(1,21):
                    minutesFall = b
                    mode = 'buy'
                    cashAvailable = 1000
                    btcAvailable = 0
                    minute = 0
                    priceTableBTC = [0]
                    for line in priceDataLines:
                        minute +=1
                        currentMinutePrice = float(line.strip())
                        priceTableBTC.append(currentMinutePrice)
                        if len(priceTableBTC) < 21:
                            pass
                        else:
                            if mode == 'buy':
                                for z in range(int(minutesRise), 0, -1):
                                    if float(priceTableBTC[minute - z]) != 0:
                                        if ((float(priceTableBTC[minute]) / float(priceTableBTC[minute - z])) - 1) >= risePercent:
                                            btcAvailable = cashAvailable / currentMinutePrice
                                            cashAvailable = 0
                                            mode = 'sell'
                                            break
                            elif mode == 'sell':
                                for z in range(int(minutesFall), 0, -1):
                                    if float(priceTableBTC[minute - z]) != 0:
                                        if ((float(priceTableBTC[minute]) / float(priceTableBTC[minute - z])) - 1) <= -fallPercent:
                                            cashAvailable = currentMinutePrice * btcAvailable
                                            btcAvailable = 0
                                            mode = 'buy'
                                            break
                    if btcAvailable != 0:
                        cashAvailable += (btcAvailable*currentMinutePrice)
                    with open('velocityBacktestData.csv', 'a', newline='') as file:
                        f = csv.writer(file)
                        f.writerow([str(round(fallPercent*100,2)), str(round(risePercent*100,2)), str(minutesFall), str(minutesRise), str(cashAvailable-1000)])

def function2():
    for x in range (5,10):
        risePercent = x*0.0025 #0.25% increase each loop
        for y in range (0,21):
            fallPercent =y*0.0025 #0.25% increase each loop
            for a in range(1,21):
                minutesRise = a
                for b in range(1,21):
                    minutesFall = b
                    mode = 'buy'
                    cashAvailable = 1000
                    btcAvailable = 0
                    minute = 0
                    priceTableBTC = [0]
                    for line in priceDataLines:
                        minute +=1
                        currentMinutePrice = float(line.strip())
                        priceTableBTC.append(currentMinutePrice)
                        if len(priceTableBTC) < 21:
                            pass
                        else:
                            if mode == 'buy':
                                for z in range(int(minutesRise), 0, -1):
                                    if float(priceTableBTC[minute - z]) != 0:
                                        if ((float(priceTableBTC[minute]) / float(priceTableBTC[minute - z])) - 1) >= risePercent:
                                            btcAvailable = cashAvailable / currentMinutePrice
                                            cashAvailable = 0
                                            mode = 'sell'
                                            break
                            elif mode == 'sell':
                                for z in range(int(minutesFall), 0, -1):
                                    if float(priceTableBTC[minute - z]) != 0:
                                        if ((float(priceTableBTC[minute]) / float(priceTableBTC[minute - z])) - 1) <= -fallPercent:
                                            cashAvailable = currentMinutePrice * btcAvailable
                                            btcAvailable = 0
                                            mode = 'buy'
                                            break
                    if btcAvailable != 0:
                        cashAvailable += (btcAvailable*currentMinutePrice)
                    with open('velocityBacktestData.csv', 'a', newline='') as file:
                        f = csv.writer(file)
                        f.writerow([str(round(fallPercent*100,2)), str(round(risePercent*100,2)), str(minutesFall), str(minutesRise), str(cashAvailable-1000)])

def function3():
    for x in range (10,15):
        risePercent = x*0.0025 #0.25% increase each loop
        for y in range (0,21):
            fallPercent =y*0.0025 #0.25% increase each loop
            for a in range(1,21):
                minutesRise = a
                for b in range(1,21):
                    minutesFall = b
                    mode = 'buy'
                    cashAvailable = 1000
                    btcAvailable = 0
                    minute = 0
                    priceTableBTC = [0]
                    for line in priceDataLines:
                        minute +=1
                        currentMinutePrice = float(line.strip())
                        priceTableBTC.append(currentMinutePrice)
                        if len(priceTableBTC) < 21:
                            pass
                        else:
                            if mode == 'buy':
                                for z in range(int(minutesRise), 0, -1):
                                    if float(priceTableBTC[minute - z]) != 0:
                                        if ((float(priceTableBTC[minute]) / float(priceTableBTC[minute - z])) - 1) >= risePercent:
                                            btcAvailable = cashAvailable / currentMinutePrice
                                            cashAvailable = 0
                                            mode = 'sell'
                                            break
                            elif mode == 'sell':
                                for z in range(int(minutesFall), 0, -1):
                                    if float(priceTableBTC[minute - z]) != 0:
                                        if ((float(priceTableBTC[minute]) / float(priceTableBTC[minute - z])) - 1) <= -fallPercent:
                                            cashAvailable = currentMinutePrice * btcAvailable
                                            btcAvailable = 0
                                            mode = 'buy'
                                            break
                    if btcAvailable != 0:
                        cashAvailable += (btcAvailable*currentMinutePrice)
                    with open('velocityBacktestData.csv', 'a', newline='') as file:
                        f = csv.writer(file)
                        f.writerow([str(round(fallPercent*100,2)), str(round(risePercent*100,2)), str(minutesFall), str(minutesRise), str(cashAvailable-1000)])

def function4():
    for x in range (15,21):
        risePercent = x*0.0025 #0.25% increase each loop
        for y in range (0,21):
            fallPercent =y*0.0025 #0.25% increase each loop
            for a in range(1,21):
                minutesRise = a
                for b in range(1,21):
                    minutesFall = b
                    mode = 'buy'
                    cashAvailable = 1000
                    btcAvailable = 0
                    minute = 0
                    priceTableBTC = [0]
                    for line in priceDataLines:
                        minute +=1
                        currentMinutePrice = float(line.strip())
                        priceTableBTC.append(currentMinutePrice)
                        if len(priceTableBTC) < 21:
                            pass
                        else:
                            if mode == 'buy':
                                for z in range(int(minutesRise), 0, -1):
                                    if float(priceTableBTC[minute - z]) != 0:
                                        if ((float(priceTableBTC[minute]) / float(priceTableBTC[minute - z])) - 1) >= risePercent:
                                            btcAvailable = cashAvailable / currentMinutePrice
                                            cashAvailable = 0
                                            mode = 'sell'
                                            break
                            elif mode == 'sell':
                                for z in range(int(minutesFall), 0, -1):
                                    if float(priceTableBTC[minute - z]) != 0:
                                        if ((float(priceTableBTC[minute]) / float(priceTableBTC[minute - z])) - 1) <= -fallPercent:
                                            cashAvailable = currentMinutePrice * btcAvailable
                                            btcAvailable = 0
                                            mode = 'buy'
                                            break
                    if btcAvailable != 0:
                        cashAvailable += (btcAvailable*currentMinutePrice)
                    with open('velocityBacktestData.csv', 'a', newline='') as file:
                        f = csv.writer(file)
                        f.writerow([str(round(fallPercent*100,2)), str(round(risePercent*100,2)), str(minutesFall), str(minutesRise), str(cashAvailable-1000)])

if __name__ == '__main__':
    p1 = mp.Process(target=function1)
    p2 = mp.Process(target=function2)
    p3 = mp.Process(target=function3)
    p4 = mp.Process(target=function4)
    p1.start()
    p2.start()
    p3.start()
    p4.start()
    p1.join()
    p2.join()
    p3.join()
    p4.join()