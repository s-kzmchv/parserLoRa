from myParser import *

from itertools import chain, combinations, product
import matplotlib.pyplot as plt
import random
import math

packetForPrint = -1

countMes1 = 0
countMes2 = 0
massOfLol1 = []
massOfLol2 = []

def prob(devicesTimestampsSuccess, devicesTimestampsFail,numOfDevices):
    # вычисление вероятности передачи
    max = 0
    numOfSuccessMessagesAll = 0
    numOfFailMessagesAll = 0
    for key in devicesTimestampsSuccess:
        numOfSuccessMessages = len(devicesTimestampsSuccess[key])
        numOfFailMessages = len(devicesTimestampsFail[key])
        if numOfSuccessMessages > max:
            max = numOfSuccessMessages
        numOfSuccessMessagesAll += numOfSuccessMessages
        numOfFailMessagesAll += numOfFailMessages
        print("P for {} = {}".format(key, numOfSuccessMessages / (numOfFailMessages + numOfSuccessMessages)))
    print()
    print("First way P = {} \n".format(numOfSuccessMessagesAll / (max * numOfDevices)))
    # print(max * numOfDevices)
    print("Second way P = {} \n".format(numOfSuccessMessagesAll / (numOfFailMessagesAll + numOfSuccessMessagesAll)))
    # print(numOfFailMessagesAll + numOfSuccessMessagesAll)
    # print(numOfSuccessMessagesAll)
    # print(numOfFailMessagesAll)

def getXiMostSign(keyDevice, packet,devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir):
    currX = timeOnAir + 1
    device = ' '
    for currDevice in devicesTimestampsSuccess:
        if keyDevice == currDevice:
            continue
        if len(devicesTimestampsSuccess[currDevice]) == 0:
            continue


        nearestTimestamps = takeClosest(devicesTimestampsSuccess[currDevice], packet)
        x = nearestTimestamps - packet

        if packet == packetForPrint:
            print(str(packet) +' + ' + str(x) + ' = ' + str(packet+x) + ' from '+ str(currDevice))

        if abs(x) < timeOnAir:
            if abs(x) < abs(currX):
                currX = x
                device = currDevice

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
                device = currDevice
    if currX != timeOnAir + 1 and packet == packetForPrint:
        print()
        print('YES ' + str(packet) +' + ' + str(currX) + ' = ' + str(packet+currX))
    return currX, device

def getXiOne(keyDevice, packet,devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir):
    currX = timeOnAir + 1
    numOfCross = 0
    device = ' '
    for currDevice in devicesTimestampsSuccess:
        if numOfCross > 1:
            return timeOnAir + 1, ' '
        if keyDevice == currDevice:
            continue
        if len(devicesTimestampsSuccess[currDevice]) == 0:
            continue


        nearestTimestamps = takeClosest(devicesTimestampsSuccess[currDevice], packet)
        x = nearestTimestamps - packet

        # if packet == packetForPrint:
        #     print(str(packet) +' + ' + str(x) + ' = ' + str(packet+x) + ' from '+ str(currDevice))

        if abs(x) < timeOnAir:
            currX = x
            numOfCross += 1
            device = currDevice

    if packet == packetForPrint:
        print()

    for currDevice in devicesTimestampsFail:
        if numOfCross > 1:
            return timeOnAir + 1, ' '
        if keyDevice == currDevice:
            continue
        if len(devicesTimestampsFail[currDevice]) == 0:
            continue


        nearestTimestamps = takeClosest(devicesTimestampsFail[currDevice], packet)
        x = nearestTimestamps - packet

        # if packet == packetForPrint:
        #     print(str(packet) +' + ' + str(x) + ' = ' + str(packet+x) + ' from '+ str(currDevice))

        if abs(x) < timeOnAir:
                currX = x
                numOfCross += 1
                device = currDevice

    if currX != timeOnAir + 1 and packet == packetForPrint:
        print()
        print('YES ' + str(packet) +' + ' + str(currX) + ' = ' + str(packet+currX))
    return currX, device

def comparisonTwoDevice(d1, d2):
    for i in range(len(d1)-1):
        print(d1[i])
        print(d2[i])
        print(d1[i + 1] - d1[i])
        print(d2[i + 1] - d2[i])
        print("\t",d1[i] - d2[i])



# выявить пересечения для определенного устройства

# счет вероятности передачи взять число передач и успешные поделить на общее число
# выявить устройства которые не передают но и не пересекаются
# по сути пары устройств обнаружить 

# вывести пакеты для которых найдено пересечение


# посмотреть ошибку интерполяции
# увеличить время передачи на ошибку интерполяции
# вывести пересечение по устройству к устройству
# усреднениние
# фотки
# интерполяуия + -

if __name__ == "__main__":
    timeOnAir = 119000
    # timeOnAir += 560 * 212
    begin = 880237045
    end = 2364649075
    step = 6999440
    # step = 7000560
    # step = 7000000
    i = 9
    # nameOfLog = 'syslog_15_SF8_21_SF7_00'
    nameOfLog = 'syslog_22_SF7'
    devicesTimestampsSuccess, devicesTimestampsFail = parse(nameOfLog, 'out', step, begin, end)

    for key in devicesTimestampsSuccess:
        # print(key)
        devicesTimestampsSuccess[key] = [int(entry) for entry in devicesTimestampsSuccess[key]]
        devicesTimestampsFail[key] = [int(entry) for entry in devicesTimestampsFail[key]]

    numOfDevices = 0
    splitName = nameOfLog.split('_')
    for itmp in splitName:
        if itmp.isdigit():
            numOfDevices += int(itmp)

    # prob(devicesTimestampsSuccess, devicesTimestampsFail, numOfDevices)

    d1 = devicesTimestampsSuccess["005F0143 SF7BW125"]
    d1.extend(devicesTimestampsFail["005F0143 SF7BW125"])
    d1.sort()

    d2 = devicesTimestampsSuccess["01470B21 SF7BW125"]
    d2.extend(devicesTimestampsFail["01470B21 SF7BW125"])
    d2.sort()

    # comparisonTwoDevice(d1,d2)

    # exit(0)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # для вывода всех пакетов без пересечения
    AllSuccessMessages = []
    AllFailMessages = []
    for key in devicesTimestampsSuccess:
        AllFailMessages.extend(devicesTimestampsFail[key])
        AllSuccessMessages.extend(devicesTimestampsSuccess[key])

    print("all message in success and fail")
    print(len(AllSuccessMessages), AllSuccessMessages)
    print(len(AllFailMessages), AllFailMessages)

    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


    ultimateDictionarySucces = {}
    ultimateDictionaryFail = {}

    part = timeOnAir / i

    for n in range(2):
        if n == 0:
            continue
        if n == 2:
            part = timeOnAir
        dict = {}
        for key in devicesTimestampsSuccess:
            ultimateDictionarySucces[key] = set()
            for entry in devicesTimestampsSuccess[key]:
                currX, device = getXiMostSign(key, entry, devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir)
                if currX != timeOnAir + 1:
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    ultimateDictionarySucces[key].add(device)
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    if entry in AllSuccessMessages:
                        AllSuccessMessages.remove(entry)

                    if entry in AllFailMessages:
                        AllFailMessages.remove(entry)
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
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
            ultimateDictionaryFail[key] = set()
            for entry in devicesTimestampsFail[key]:
                currX, device = getXiMostSign(key, entry, devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir)
                if currX != timeOnAir + 1:
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    ultimateDictionaryFail[key].add(device)
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                    if entry in AllSuccessMessages:
                        AllSuccessMessages.remove(entry)

                    if entry in AllFailMessages:
                        AllFailMessages.remove(entry)
                    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

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

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print("message without cross in success and fail")
        print(len(AllSuccessMessages), AllSuccessMessages)
        print(len(AllFailMessages), AllFailMessages)
        print()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        print("Cross device with other!!!!!!!")
        for key in ultimateDictionaryFail:
            if len(ultimateDictionaryFail[key]) != 0:
                print(key, ultimateDictionaryFail[key])
        print()
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        devicesTimestampsFailNoCross = {}
        for item in AllFailMessages:
            for key in devicesTimestampsFail:
                if item in devicesTimestampsFail[key]:
                    if devicesTimestampsFailNoCross.get(key) == None:
                        devicesTimestampsFailNoCross[key] = [item]
                    else:
                        devicesTimestampsFailNoCross[key].append(item)
                    break
        print("message without cross in fail by device")
        for key in devicesTimestampsFailNoCross:
            print(key,len(devicesTimestampsFailNoCross[key]), devicesTimestampsFailNoCross[key])
        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        print('\nn = ' + str(n))
        if n == 1:
            # вывод кол-ва в промежутке
            resStr = ''
            Pr = []
            Xi = []
            N_message = []

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
                    countMes1 += dict[item][1]
                else:
                    Pr.append(0)
                    N_message.append(0)
                    # Xi.append(str(item))
                    Xi.append(item)
                    print('Pr[success | ' + str(item) + '] = 0 Success: 0 Fail: 0')
            print(countMes1)
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
