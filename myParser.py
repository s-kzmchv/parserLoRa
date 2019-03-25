import csv
import json
from bisect import bisect_left
import numpy as np

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

def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def parse(inputFile, outputFile,timePeriod,beginTimestamp,endTimestamp):
    fieldnames = ['id device',   'num of message', 'timestamps']
    data = [' '] * 3
    res_list = []


    devicesSuccesTimestamps = {} # словарь id устройства и список timeStamp'ов
    devicesFailTimestamps = {} # словарь id устройства и список интерполированных timeStamp'ов
    devicesLastGetNumOfMessage = {} # словарь id устройства и номер последнего сообщения

    lostDevicesSuccesTimestamps = {} # словарь id устройства которое не попало в промежуток и список его timeStamp'ов

    currDevice = [] # список id устройств под обработку
    numOfCurrMessage = [] # список номеров пакетов этих id устройств

    interpolError = [] # список ошибок интерполяции
    maxError = 0 # максимальная ошибка интерполяции по абс величине

    avrgPeriodForDevice = {} # словарь хранит каждое усреднение пропуска по устройтсвам

    f = open(inputFile)
    for line in f: # проходим весь файл по строчно
        if line.find("fcnt") != -1: # находим строки с указанием id устройства и номером
            # добавляем в списки номера и устройства для обработки
            currDevice.append(line.split(' ')[-2])
            numOfCurrMessage.append(int(line.split(' ')[-1].split('=')[-1][:-2]))
            continue

        if line.find("JSON up: {\"rxpk\"") != -1: # находим строки с пакетами

            tmp = line.split('JSON up:')
            d = json.loads(tmp[1])
            for packetNum in range(len(d['rxpk'])): # идем по timeStamp'ам найденым в пакете
                timeStamp = d['rxpk'][packetNum]['tmst']

                # проверяем только те timeStamp'ы для которых имеются устройства. TimeStamp'ы без устройств не рассматриваются!
                if len(currDevice) > packetNum:
                    currDeviceWithSF = currDevice[packetNum] + ' ' + d['rxpk'][packetNum]['datr']
                else:
                    break

                # проверяем что timeStamp находится в заданном промежутке, если нет добавляем устройство и таймстемп в lostDevicesSuccesTimestamps
                if timeStamp < beginTimestamp or timeStamp > endTimestamp:
                    if lostDevicesSuccesTimestamps.get(currDeviceWithSF) == None:
                        lostDevicesSuccesTimestamps[currDeviceWithSF] = [timeStamp]
                    else:
                        lostDevicesSuccesTimestamps[currDeviceWithSF].append(timeStamp)
                    continue

                tmpTimeStampInterpol = 0
                # проверка на пропущенные пакеты
                # если разница между текущим и последним пакетом больше 1 тогда
                # добавляем пропущенные пакеты в devicesFailTimestamps
                # считаем ошибку интерполяции между последним проинтерполированным  и текушим timeStamp'ом
                if devicesLastGetNumOfMessage.get(currDeviceWithSF) != None and numOfCurrMessage[packetNum] - devicesLastGetNumOfMessage[currDeviceWithSF] != 1:
                    # print(timeStamp)
                    # print(int(devicesSuccesTimestamps[currDeviceWithSF][-1]))
                    # print(numOfCurrMessage[packetNum] - devicesLastGetNumOfMessage[currDeviceWithSF])
                    currTimePeriod = int((timeStamp - int(devicesSuccesTimestamps[currDeviceWithSF][-1])) / (numOfCurrMessage[packetNum] - devicesLastGetNumOfMessage[currDeviceWithSF]))
                    if avrgPeriodForDevice.get(currDeviceWithSF) == None:
                        avrgPeriodForDevice[currDeviceWithSF] = [currTimePeriod]
                    else:
                        avrgPeriodForDevice[currDeviceWithSF].append(currTimePeriod)
                    for i in range(numOfCurrMessage[packetNum] - devicesLastGetNumOfMessage[currDeviceWithSF] - 1):
                        devicesFailTimestamps[currDeviceWithSF].append(str((int(devicesSuccesTimestamps[currDeviceWithSF][-1]) + (i+1)*currTimePeriod)))
                        tmpTimeStampInterpol = int(devicesSuccesTimestamps[currDeviceWithSF][-1]) + (i+1)*currTimePeriod
                        # print(i)

                # запись ошибки интерполяции и макс ошибки
                if tmpTimeStampInterpol != 0:
                    # if timePeriod - (timeStamp - tmpTimeStampInterpol) < 0:
                    #     print(timeStamp )
                    #     print(tmpTimeStampInterpol)
                    # print((7000000 - (timeStamp - tmpTimeStampInterpol))/(i+1))
                    interpolError.append((7000000 - (timeStamp - tmpTimeStampInterpol))/(i+1))
                    if maxError < abs((7000000 - (timeStamp - tmpTimeStampInterpol))):
                        maxError = abs((7000000 - (timeStamp - tmpTimeStampInterpol)))

                # запись найденного timeStamp'a
                # запись последнего номера
                if devicesSuccesTimestamps.get(currDeviceWithSF) == None:
                    devicesSuccesTimestamps[currDeviceWithSF] = [str(timeStamp)]
                    devicesLastGetNumOfMessage[currDeviceWithSF] = numOfCurrMessage[packetNum]
                    devicesFailTimestamps[currDeviceWithSF] = []
                else:
                    devicesSuccesTimestamps[currDeviceWithSF].append(str(timeStamp))
                    devicesLastGetNumOfMessage[currDeviceWithSF] = numOfCurrMessage[packetNum]

            currDevice = []
            numOfCurrMessage = []

    f.close()

    # Интерполяция по краям
    for key in devicesSuccesTimestamps.keys():
        currTimePeriod = timePeriod # стандартный период
        #  если слишком мало значений успешной передачи и по ним нельзя определить новый период
        if (len(devicesSuccesTimestamps[key]) == 1) or (len(devicesSuccesTimestamps[key]) == 2 and int(devicesSuccesTimestamps[key][1]) - int(devicesSuccesTimestamps[key][0]) < 6000000):
            # пытаемся определить новый период по таймстемпам за границей промежутку
            if lostDevicesSuccesTimestamps.get(key) != None:
                nearest = takeClosest(lostDevicesSuccesTimestamps[key],int(devicesSuccesTimestamps[key][0]))
                tmpPeriod = abs(nearest - int(devicesSuccesTimestamps[key][0]))
                if tmpPeriod> 6000000 and tmpPeriod < 80000000:
                    currTimePeriod = tmpPeriod
        else:
            # если достаточно значений успешной передачи
            currTimePeriods = []
            for i in range(len(devicesSuccesTimestamps[key]) - 1):
                if (int(devicesSuccesTimestamps[key][i + 1]) - int(devicesSuccesTimestamps[key][i]) < 8000000 and int(devicesSuccesTimestamps[key][i + 1]) - int(devicesSuccesTimestamps[key][i]) > 6000000):
                    currTimePeriods.append(int(devicesSuccesTimestamps[key][i + 1]) - int(devicesSuccesTimestamps[key][i]))
            # берем среднее между соседними успешно переданными таймстемпами или берем среднее по промежтукам промущенных пакетов
            if len(currTimePeriods) == 0:
                currTimePeriod = int(np.mean(avrgPeriodForDevice[key]))
            else:
                currTimePeriod = int(np.mean(currTimePeriods))
        # интерполируем края с полученным периодом
        if len(devicesSuccesTimestamps[key]) != 0:
            currDeviceFirstTimeStamp = int(devicesSuccesTimestamps[key][0])
            while currDeviceFirstTimeStamp - currTimePeriod > beginTimestamp:
                devicesFailTimestamps[key].insert(0, str(currDeviceFirstTimeStamp - currTimePeriod))
                currDeviceFirstTimeStamp = int(devicesFailTimestamps[key][0])

            currDeviceLastTimeStamp = int(devicesSuccesTimestamps[key][-1])
            while currDeviceLastTimeStamp + currTimePeriod < endTimestamp:
                devicesFailTimestamps[key].append(str(currDeviceLastTimeStamp + currTimePeriod))
                currDeviceLastTimeStamp = int(devicesFailTimestamps[key][-1])

    # добавление в devicesFailTimestamps устройств из lostDevicesSuccesTimestamps
    for key in lostDevicesSuccesTimestamps.keys():
        if key in devicesFailTimestamps.keys():
            continue
        currTimePeriod = timePeriod # стандартный период 7000000
        # print(lostDevicesSuccesTimestamps[key])
        # пытаемся получить преоид из таймстемпов выходящих за границы рассматриваемого промежутка
        if len(lostDevicesSuccesTimestamps[key]) > 1:
            currTimePeriods = []
            for i in range(len(lostDevicesSuccesTimestamps[key]) - 1):
                if (lostDevicesSuccesTimestamps[key][i + 1] - lostDevicesSuccesTimestamps[key][i] < 8000000 and lostDevicesSuccesTimestamps[key][i + 1] - lostDevicesSuccesTimestamps[key][i] > 6000000):
                    currTimePeriods.append(lostDevicesSuccesTimestamps[key][i + 1] - lostDevicesSuccesTimestamps[key][i])
                    # currTimePeriod = lostDevicesSuccesTimestamps[key][i + 1] - lostDevicesSuccesTimestamps[key][i]
                    # break
            if len(currTimePeriods) != 0:
                currTimePeriod = int(np.mean(currTimePeriods))

        devicesFailTimestamps[key] = []
        devicesSuccesTimestamps[key] = []
        nearestFromBegin = takeClosest(lostDevicesSuccesTimestamps[key], beginTimestamp)
        nearestFromEnd = takeClosest(lostDevicesSuccesTimestamps[key], endTimestamp)
        currTimeStamp = 0
        if abs(beginTimestamp - nearestFromBegin) < abs(endTimestamp - nearestFromEnd):
            currTimeStamp = nearestFromBegin
        else:
            currTimeStamp = nearestFromEnd

        if currTimeStamp < beginTimestamp:
            currTimeStamp += currTimePeriod
            while currTimeStamp < endTimestamp:
                if currTimeStamp > beginTimestamp:
                    devicesFailTimestamps[key].append(str(currTimeStamp))
                currTimeStamp += currTimePeriod
        else:
            while currTimeStamp > beginTimestamp:
                currTimeStamp -= currTimePeriod
                if currTimeStamp < endTimestamp:
                    devicesFailTimestamps[key].insert(0,str(currTimeStamp))

    # Запись в файл devicesSuccesTimestamps
    for key in devicesSuccesTimestamps.keys():
        data[0] = key
        data[1] = str(len(devicesSuccesTimestamps[key]))
        data[2] = ' '.join(devicesSuccesTimestamps[key])
        inner_dict = dict(zip(fieldnames, data))
        res_list.append(inner_dict)
    #csv_dict_writer(outputFile + 'Table.csv', fieldnames, res_list)
    # print(devicesLastGetNumOfMessage)
    f = open(outputFile + 'SuccessText.txt', 'w')
    for entry in res_list:
        f.write(entry['id device'] + ' ' + entry['num of message'] + ' ' + entry['timestamps'] + '\n')
    f.close()
    f = open(outputFile + 'FailText.txt', 'w')


    # Запись в файл devicesFailTimestamps
    for key in devicesFailTimestamps.keys():
        tmp = ' '.join(devicesFailTimestamps[key])
        f.write(key + ' ' + str(len(devicesFailTimestamps[key])) + ' ' + tmp + '\n')
    f.close()

    print(interpolError)
    print(np.mean(interpolError))
    print(maxError)

    return devicesSuccesTimestamps, devicesFailTimestamps
