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

def getXiMostSign(keyDevice, packet, devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir):
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

def comparisonTwoDevice(d1name, d2name, devicesTimestampsSuccess, devicesTimestampsFail):
    d1 = devicesTimestampsSuccess[d1name].copy()
    d1.extend(devicesTimestampsFail[d1name])
    d1.sort()

    d2 = devicesTimestampsSuccess[d2name].copy()
    d2.extend(devicesTimestampsFail[d2name])
    d2.sort()

    for i in range(len(d1)-1):
        if (d1[i] in devicesTimestampsSuccess[d1name]) and (d2[i] in devicesTimestampsSuccess[d2name]):
            print(d1[i])
            print(d2[i])
            print(d1[i + 1] - d1[i])
            print(d2[i + 1] - d2[i])
            print("\t",d1[i] - d2[i])

def periodForDevice(dname, devicesTimestampsSuccess):
    d = devicesTimestampsSuccess[dname].copy()
    d.extend(devicesTimestampsFail[dname])
    d.sort()


    for i in range(len(d)-1):
        if (d[i + 1] - d[i] < 8000000):
            # print(d[i + 1])
            # print(d[i])
            print(d[i + 1] - d[i])
            print()


# выявить устройства которые не передают но и не пересекаются
# по сути пары устройств обнаружить

# посмотреть ошибку интерполяции
# увеличить время передачи на ошибку интерполяции
# вывести пересечение по устройству к устройству
# усреднениние
# фотки
# интерполяции + -
# пересечение в конце
# усреднить до 300

if __name__ == "__main__":

    namesOfLog = ['syslog_22_SF7',  'syslog_14_SF7', 'syslog_7_SF7']
    begins = [208178579, 113778867, 288014035]
    ends = [1271427251,  933773339, 1569561259]
    dict = {}

    # параметры
    timeOnAir = 119000
    # timeOnAir += 1000
    # step = 6999923
    # step = 6999440
    # step = 7000560
    step = 7000000
    i = 9
    part = timeOnAir / i

    # цикл по лог файлам
    for k in range(len(namesOfLog)):
        # begin = 208178579
        # end = 1271427251
        # nameOfLog = 'syslog_22_SF7'

        begin = begins[k]
        end = ends[k]
        nameOfLog = namesOfLog[k]

        print(nameOfLog)

        # парсинг
        devicesTimestampsSuccess, devicesTimestampsFail = parse(nameOfLog, 'out', step, begin, end)

        # преобразование к инту
        for key in devicesTimestampsSuccess:
            # print(key)
            devicesTimestampsSuccess[key] = [int(entry) for entry in devicesTimestampsSuccess[key]]
            devicesTimestampsFail[key] = [int(entry) for entry in devicesTimestampsFail[key]]

        # Подсчет утройст по имени файла
        numOfDevices = 0
        splitName = nameOfLog.split('_')
        for itmp in splitName:
            if itmp.isdigit():
                numOfDevices += int(itmp)

        # prob(devicesTimestampsSuccess, devicesTimestampsFail, numOfDevices)

        # comparisonTwoDevice("0160082E SF7BW125","01470B21 SF7BW125", devicesTimestampsSuccess, devicesTimestampsFail )

        # periodForDevice("0055013D SF7BW125",devicesTimestampsSuccess)

        # exit(0)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # для вывода всех пакетов без пересечения
        # общий список  TimeStamp'ов успешных и нет
        AllSuccessMessages = []
        AllFailMessages = []
        for key in devicesTimestampsSuccess:
            AllFailMessages.extend(devicesTimestampsFail[key])
            AllSuccessMessages.extend(devicesTimestampsSuccess[key])

        print("all message in success and fail")
        print(len(AllSuccessMessages), AllSuccessMessages)
        print(len(AllFailMessages), AllFailMessages)

        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

        # словари для записи Устройство - С каким утройствами пересекается
        ultimateDictionarySucces = {}
        ultimateDictionaryFail = {}

        for n in range(2):
            if n == 0:
                continue
            if n == 2:
                part = timeOnAir

            # цикл по устройствам
            for key in devicesTimestampsSuccess:
                ultimateDictionarySucces[key] = set()
                # цикл по успешным TimeStamp'ам
                for entry in devicesTimestampsSuccess[key]:
                    # получение точного значения Xi
                    currX, device = getXiMostSign(key, entry, devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir)
                    if currX != timeOnAir + 1:
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # добавление в список пересечений по утройствам
                        ultimateDictionarySucces[key].add(device)
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # удаление  TimeStamp'ов из общего списка  TimeStamp'ов
                        if entry in AllSuccessMessages:
                            AllSuccessMessages.remove(entry)

                        if entry in AllFailMessages:
                            AllFailMessages.remove(entry)
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # округление Xi до участка
                        j = 0
                        while abs(currX) > part * (j + 1):
                            j = j + 1
                        res = round((j + 1) * part, 1)
                        # увеличение событий для участка
                        if currX < 0:
                            res *= -1
                        if dict.get(res) == None:
                            dict[res] = [1, 0]
                        else:
                            dict[res][0] += 1

                ultimateDictionaryFail[key] = set()
                # цикл по пропушенным TimeStamp'ам
                for entry in devicesTimestampsFail[key]:
                    # получение точного значения Xi
                    currX, device = getXiMostSign(key, entry, devicesTimestampsSuccess, devicesTimestampsFail, timeOnAir)
                    if currX != timeOnAir + 1:
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # добавление в список пересечений по утройствам
                        ultimateDictionaryFail[key].add(device)
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # удаление  TimeStamp'ов из общего списка  TimeStamp'ов
                        if entry in AllSuccessMessages:
                            AllSuccessMessages.remove(entry)

                        if entry in AllFailMessages:
                            AllFailMessages.remove(entry)
                        # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
                        # округление Xi до участка
                        j = 0
                        while abs(currX) > part * (j + 1):
                            j = j + 1
                        res = round((j + 1) * part, 1)
                        if currX < 0:
                            res *= -1
                        # увеличение событий для участка
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
        # вывод таймстемпов по устройствам для которых не найдено пересечений
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





mu, sigma = 100, 15
x = mu + sigma * np.random.randn(10000)
bins = [0, 40, 60, 75, 90, 110, 125, 140, 160, 200]
hist, bins = np.histogram(x, bins=bins)
width = np.diff(bins)
center = (bins[:-1] + bins[1:]) / 2

fig, ax = plt.subplots(figsize=(8,3))
ax.bar(center, hist, align='center', width=width)
ax.set_xticks(bins)
fig.savefig("11111.png")