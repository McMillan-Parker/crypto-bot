import csv
import multiprocessing as mp

# Using readlines()
file1 = open('btc2021.txt', 'r')
priceDataLines = file1.readlines()
file1.close()
risePercent = 0
fallPercent = 0


def function1():
    for x in range(0, 4):
        risePercent = x * 0.002  # 0.2% increase each loop
        # Intitial setup variables for each pair of x,y
        fallPercent = 0
        for y in range(0, 48):
            fallPercent = y * 0.002  # 0.2% increase each loop
            comparisonPrice = float(priceDataLines[0].strip())
            mode = 'buy'
            cashAvailable = 1000
            btcAvailable = 0
            minute = 0
            print('Now testing pair: Sell when rise ' + str(round(risePercent, 2)) + '% and buy when fall ' + str(
                round(fallPercent, 2)) + '%.')
            for line in priceDataLines:
                minute += 1
                currentMinutePrice = float(line.strip())
                print("minute " + str(minute))
                if mode == 'buy':
                    if (((currentMinutePrice - comparisonPrice) / comparisonPrice) <= -fallPercent):
                        btcAvailable = cashAvailable / currentMinutePrice
                        print("price has fallen " + str(
                            ((currentMinutePrice - comparisonPrice) / comparisonPrice) * 100) + "%")
                        print("bought " + str(cashAvailable / currentMinutePrice) + " btc.")
                        comparisonPrice = currentMinutePrice
                        cashAvailable = 0
                        mode = 'sell'
                elif mode == 'sell':
                    if (((currentMinutePrice - comparisonPrice) / comparisonPrice) >= risePercent):
                        cashAvailable = currentMinutePrice * btcAvailable
                        print("price has risen " + str(
                            ((currentMinutePrice - comparisonPrice) / comparisonPrice) * 100) + "%")
                        print("sold $" + str(currentMinutePrice * btcAvailable) + "worth of btc.")
                        comparisonPrice = currentMinutePrice
                        btcAvailable = 0
                        mode = 'buy'
            if btcAvailable != 0:
                cashAvailable += (btcAvailable * currentMinutePrice)
            with open('backtestData.csv', 'a', newline='') as file:
                f = csv.writer(file)
                f.writerow(
                    [str(round(fallPercent * 100, 2)), str(round(risePercent * 100, 2)), str(cashAvailable - 1000)])


def function2():
    for x in range(4, 8):
        risePercent = x * 0.002  # 0.1% increase each loop
        # Intitial setup variables for each pair of x,y
        fallPercent = 0
        for y in range(0, 48):
            fallPercent = y * 0.002  # 0.1% increase each loop
            comparisonPrice = float(priceDataLines[0].strip())
            mode = 'buy'
            cashAvailable = 1000
            btcAvailable = 0
            minute = 0
            print('Now testing pair: Sell when rise ' + str(round(risePercent, 2)) + '% and buy when fall ' + str(
                round(fallPercent, 2)) + '%.')
            for line in priceDataLines:
                minute += 1
                currentMinutePrice = float(line.strip())
                print("minute " + str(minute))
                if mode == 'buy':
                    if (((currentMinutePrice - comparisonPrice) / comparisonPrice) <= -fallPercent):
                        btcAvailable = cashAvailable / currentMinutePrice
                        print("price has fallen " + str(
                            ((currentMinutePrice - comparisonPrice) / comparisonPrice) * 100) + "%")
                        print("bought " + str(cashAvailable / currentMinutePrice) + " btc.")
                        comparisonPrice = currentMinutePrice
                        cashAvailable = 0
                        mode = 'sell'
                elif mode == 'sell':
                    if (((currentMinutePrice - comparisonPrice) / comparisonPrice) >= risePercent):
                        cashAvailable = currentMinutePrice * btcAvailable
                        print("price has risen " + str(
                            ((currentMinutePrice - comparisonPrice) / comparisonPrice) * 100) + "%")
                        print("sold $" + str(currentMinutePrice * btcAvailable) + "worth of btc.")
                        comparisonPrice = currentMinutePrice
                        btcAvailable = 0
                        mode = 'buy'
            if btcAvailable != 0:
                cashAvailable += (btcAvailable * currentMinutePrice)
            with open('backtestData.csv', 'a', newline='') as file:
                f = csv.writer(file)
                f.writerow(
                    [str(round(fallPercent * 100, 2)), str(round(risePercent * 100, 2)), str(cashAvailable - 1000)])


def function3():
    for x in range(8, 12):
        risePercent = x * 0.002  # 0.1% increase each loop
        # Intitial setup variables for each pair of x,y
        fallPercent = 0
        for y in range(0, 48):
            fallPercent = y * 0.002  # 0.1% increase each loop
            comparisonPrice = float(priceDataLines[0].strip())
            mode = 'buy'
            cashAvailable = 1000
            btcAvailable = 0
            minute = 0
            print('Now testing pair: Sell when rise ' + str(round(risePercent, 2)) + '% and buy when fall ' + str(
                round(fallPercent, 2)) + '%.')
            for line in priceDataLines:
                minute += 1
                currentMinutePrice = float(line.strip())
                print("minute " + str(minute))
                if mode == 'buy':
                    if (((currentMinutePrice - comparisonPrice) / comparisonPrice) <= -fallPercent):
                        btcAvailable = cashAvailable / currentMinutePrice
                        print("price has fallen " + str(
                            ((currentMinutePrice - comparisonPrice) / comparisonPrice) * 100) + "%")
                        print("bought " + str(cashAvailable / currentMinutePrice) + " btc.")
                        comparisonPrice = currentMinutePrice
                        cashAvailable = 0
                        mode = 'sell'
                elif mode == 'sell':
                    if (((currentMinutePrice - comparisonPrice) / comparisonPrice) >= risePercent):
                        cashAvailable = currentMinutePrice * btcAvailable
                        print("price has risen " + str(
                            ((currentMinutePrice - comparisonPrice) / comparisonPrice) * 100) + "%")
                        print("sold $" + str(currentMinutePrice * btcAvailable) + "worth of btc.")
                        comparisonPrice = currentMinutePrice
                        btcAvailable = 0
                        mode = 'buy'
            if btcAvailable != 0:
                cashAvailable += (btcAvailable * currentMinutePrice)
            with open('backtestData.csv', 'a', newline='') as file:
                f = csv.writer(file)
                f.writerow(
                    [str(round(fallPercent * 100, 2)), str(round(risePercent * 100, 2)), str(cashAvailable - 1000)])


def function4():
    for x in range(12, 16):
        risePercent = x * 0.002  # 0.1% increase each loop
        # Intitial setup variables for each pair of x,y
        fallPercent = 0
        for y in range(0, 48):
            fallPercent = y * 0.002  # 0.1% increase each loop
            comparisonPrice = float(priceDataLines[0].strip())
            mode = 'buy'
            cashAvailable = 1000
            btcAvailable = 0
            minute = 0
            print('Now testing pair: Sell when rise ' + str(round(risePercent, 2)) + '% and buy when fall ' + str(
                round(fallPercent, 2)) + '%.')
            for line in priceDataLines:
                minute += 1
                currentMinutePrice = float(line.strip())
                print("minute " + str(minute))
                if mode == 'buy':
                    if (((currentMinutePrice - comparisonPrice) / comparisonPrice) <= -fallPercent):
                        btcAvailable = cashAvailable / currentMinutePrice
                        print("price has fallen " + str(
                            ((currentMinutePrice - comparisonPrice) / comparisonPrice) * 100) + "%")
                        print("bought " + str(cashAvailable / currentMinutePrice) + " btc.")
                        comparisonPrice = currentMinutePrice
                        cashAvailable = 0
                        mode = 'sell'
                elif mode == 'sell':
                    if (((currentMinutePrice - comparisonPrice) / comparisonPrice) >= risePercent):
                        cashAvailable = currentMinutePrice * btcAvailable
                        print("price has risen " + str(
                            ((currentMinutePrice - comparisonPrice) / comparisonPrice) * 100) + "%")
                        print("sold $" + str(currentMinutePrice * btcAvailable) + "worth of btc.")
                        comparisonPrice = currentMinutePrice
                        btcAvailable = 0
                        mode = 'buy'
            if btcAvailable != 0:
                cashAvailable += (btcAvailable * currentMinutePrice)
            with open('backtestData.csv', 'a', newline='') as file:
                f = csv.writer(file)
                f.writerow(
                    [str(round(fallPercent * 100, 2)), str(round(risePercent * 100, 2)), str(cashAvailable - 1000)])


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