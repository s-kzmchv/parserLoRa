import csv
import json
from bisect import bisect_left

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
    devicesSuccesTimestamps = {}
    lostDevicesSuccesTimestamps = {}
    devicesFailTimestamps = {}
    devicesLastGetNumOfMessage = {}
    currDevice = []
    numOfCurrMessage = []

    f = open(inputFile)
    for line in f:
        if line.find("fcnt") != -1:
            # currDevice = line.split(' ')[-2]
            # numOfCurrMessage = int(line.split(' ')[-1].split('=')[-1][:-2])
            currDevice.append(line.split(' ')[-2])
            numOfCurrMessage.append(int(line.split(' ')[-1].split('=')[-1][:-2]))
            continue

        if line.find("JSON up: {\"rxpk\"") != -1:

            tmp = line.split('JSON up:')
            d = json.loads(tmp[1])
            # numOfTimestamps = len(d['rxpk'])
            for packetNum in range(len(d['rxpk'])):
                # timeStamp = d['rxpk'][-1]['tmst']
                timeStamp = d['rxpk'][packetNum]['tmst']
                currDeviceWithSF = currDevice[packetNum] + ' ' + d['rxpk'][packetNum]['datr']

                if timeStamp < beginTimestamp or timeStamp > endTimestamp:
                    if devicesSuccesTimestamps.get(currDeviceWithSF) == None:
                        if lostDevicesSuccesTimestamps.get(currDeviceWithSF) == None:
                            lostDevicesSuccesTimestamps[currDeviceWithSF] = [timeStamp]
                        else:
                            lostDevicesSuccesTimestamps[currDeviceWithSF].append(timeStamp)
                    continue

                if devicesLastGetNumOfMessage.get(currDeviceWithSF) != None and numOfCurrMessage[packetNum] - devicesLastGetNumOfMessage[currDeviceWithSF] != 1:
                    for i in range(numOfCurrMessage[packetNum] - devicesLastGetNumOfMessage[currDeviceWithSF] - 1):
                        devicesFailTimestamps[currDeviceWithSF].append(str((int(devicesSuccesTimestamps[currDeviceWithSF][-1]) + (i+1)*timePeriod)))

                if devicesSuccesTimestamps.get(currDeviceWithSF) == None:
                    devicesSuccesTimestamps[currDeviceWithSF] = [str(timeStamp)]
                    devicesLastGetNumOfMessage[currDeviceWithSF] = numOfCurrMessage[packetNum]
                    devicesFailTimestamps[currDeviceWithSF] = []
                    if lostDevicesSuccesTimestamps.get(currDeviceWithSF) != None:
                        lostDevicesSuccesTimestamps.pop(currDeviceWithSF)
                else:
                    devicesSuccesTimestamps[currDeviceWithSF].append(str(timeStamp))
                    devicesLastGetNumOfMessage[currDeviceWithSF] = numOfCurrMessage[packetNum]

            currDevice = []
            numOfCurrMessage = []

    f.close()

    # print(lostDevicesSuccesTimestamps)
    for key in lostDevicesSuccesTimestamps.keys():
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
            currTimeStamp += timePeriod
            while currTimeStamp < endTimestamp:
                if currTimeStamp > beginTimestamp:
                    devicesFailTimestamps[key].append(str(currTimeStamp))
                currTimeStamp += timePeriod
        else:
            while currTimeStamp > beginTimestamp:
                currTimeStamp -= timePeriod
                if currTimeStamp < endTimestamp:
                    devicesFailTimestamps[key].insert(0,str(currTimeStamp))



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





    for key in devicesSuccesTimestamps.keys():
        if len(devicesSuccesTimestamps[key]) != 0:
            currDeviceFirstTimeStamp = int(devicesSuccesTimestamps[key][0])
            while currDeviceFirstTimeStamp - timePeriod > beginTimestamp:
                devicesFailTimestamps[key].insert(0,str(currDeviceFirstTimeStamp - timePeriod))
                currDeviceFirstTimeStamp = int(devicesFailTimestamps[key][0])

            currDeviceLastTimeStamp = int(devicesSuccesTimestamps[key][-1])
            while currDeviceLastTimeStamp + timePeriod < endTimestamp:
                devicesFailTimestamps[key].append(str(currDeviceLastTimeStamp + timePeriod))
                currDeviceLastTimeStamp = int(devicesFailTimestamps[key][-1])



    for key in devicesFailTimestamps.keys():
        tmp = ' '.join(devicesFailTimestamps[key])
        f.write(key + ' ' + str(len(devicesFailTimestamps[key])) + ' ' + tmp + '\n')
    f.close()
    return devicesSuccesTimestamps, devicesFailTimestamps
