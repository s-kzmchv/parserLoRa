from myParser import parse
from bisect import bisect_left
from itertools import chain, combinations, product
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random


def takeClosest(myList, myNumber):
    """
    Assumes myList is sorted. Returns closest value to myNumber.

    If two numbers are equally close, return the smallest number.
    """
    pos = bisect_left(myList, myNumber)
    if pos == 0:
        return myList[0]
    if pos == len(myList):
        return myList[-1]
    before = myList[pos - 1]
    after = myList[pos]
    if after - myNumber < myNumber - before:
       return after
    else:
       return before


def getXi(keyDevice, packet,devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir):
    packetForPrint = 937555131
    currX = timeOnAir + 1
    for currDevice in devicesTimestampsSuccess:
        if keyDevice == currDevice:
            continue

        nearestTimestamps = takeClosest(devicesTimestampsSuccess[currDevice], packet)
        x = nearestTimestamps - packet

        if packet == packetForPrint:
            print(str(packet) +' + ' + str(x) + ' = ' + str(packet+x) + ' from '+ str(currDevice))

        if abs(x) < timeOnAir:
            if abs(x) < abs(currX):
                currX = x

    if packet == packetForPrint:
        print()

    for currDevice in devicesTimestampsFail:
        if keyDevice == currDevice:
            continue
        if len(devicesTimestampsFail[currDevice]) == 0:
            continue

        nearestTimestamps = takeClosest(devicesTimestampsFail[currDevice], packet)
        x = nearestTimestamps - packet

        if packet == packetForPrint:
            print(str(packet) +' + ' + str(x) + ' = ' + str(packet+x) + ' from '+ str(currDevice))

        if abs(x) < timeOnAir:
            if abs(x) < abs(currX):
                currX = x
    if currX != timeOnAir + 1 and packet == packetForPrint:
        print()
        print('YES ' + str(packet) +' + ' + str(currX) + ' = ' + str(packet+currX))
    return currX


if __name__ == "__main__":
    timeOnAir = 119000
    begin = 881557851
    end = 2563801763
    step = 7000000
    i = 9
    devicesTimestampsSuccess, devicesTimestampsFail = parse('syslog_22_SF7', 'out', step, begin, end)

    for key in devicesTimestampsSuccess:
        # print(key)
        devicesTimestampsSuccess[key] = [int(entry) for entry in devicesTimestampsSuccess[key]]
        devicesTimestampsFail[key] = [int(entry) for entry in devicesTimestampsFail[key]]



    part = timeOnAir / i

    for n in range(2):
        if n == 0:
            continue
        if n == 2:
            part = timeOnAir

        dict = {}

        for key in devicesTimestampsSuccess:
            for entry in devicesTimestampsSuccess[key]:
                currX = getXi(key, entry, devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir)

                if currX != timeOnAir + 1:
                    j = 0
                    while abs(currX) > part * (j + 1):
                        j = j + 1

                    res = round((j + 1) * part, 1)
                    if currX < 0:
                        res *= -1

                    if dict.get(res) == None:
                        dict[res] = [1, 0]
                    else:
                        dict[res][0] += 1

        for key in devicesTimestampsFail:
            for entry in devicesTimestampsFail[key]:

                currX = getXi(key, entry, devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir)

                if currX != timeOnAir + 1:
                    j = 0
                    while abs(currX) > part * (j + 1):
                        j = j + 1

                    res = round((j + 1) * part, 1)
                    if currX < 0:
                        res *= -1

                    if dict.get(res) == None:
                        dict[res] = [0, 1]
                    else:
                        dict[res][1] += 1

        print('n = ' + str(n))
        if n == 1:
            # вывод кол-ва в промежутке
            resStr = ''
            Pr = []
            Xi = []
            N_message = []

            # Xi = sorted(dict.keys())

            for item in np.arange(-timeOnAir, timeOnAir + 1, part):
                item = round(item, 1)
                if item == 0:
                    continue
                if dict.get(item) != None:
                    PrCurr = dict[item][0] / (dict[item][0] + dict[item][1])
                    Pr.append(PrCurr)
                    N_message.append(dict[item][0] + dict[item][1])
                    # Xi.append(str(item))
                    Xi.append(item)
                    print('Pr[success | ' + str(item) + '] = ' + str(PrCurr) + ' Success: ' + str(
                        dict[item][0]) + ' Fail: ' + str(dict[item][1]))
                else:
                    Pr.append(0)
                    N_message.append(0)
                    # Xi.append(str(item))
                    Xi.append(item)
                    print('Pr[success | ' + str(item) + '] = 0 Success: 0 Fail: 0')

            plt.plot(Xi, Pr, color="g", label='probability')
            plt.xlabel('Xi')
            plt.ylabel('Pr[success]')
            plt.legend()
            plt.savefig("n={} probabilities new.png".format(n))
            # plt.show()
            plt.clf()

            plt.plot(Xi, N_message, color="g", label='packet')
            plt.xlabel('Xi')
            plt.ylabel('NumOfMessage')
            plt.legend()
            plt.savefig("n={} packets new.png".format(n))
            # plt.show()
            plt.clf()
