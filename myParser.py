import csv
import json


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
    devicesFailTimestamps = {}
    devicesLastGetNumOfMessage = {}
    currDevice = []
    numOfCurrMessage = []
    currDeviceWithSF = ''


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

                if timeStamp < beginTimestamp or timeStamp > endTimestamp:
                    continue

                currDeviceWithSF = currDevice[packetNum] + ' ' + d['rxpk'][packetNum]['datr']

                if devicesLastGetNumOfMessage.get(currDeviceWithSF) != None and numOfCurrMessage[packetNum] - devicesLastGetNumOfMessage[currDeviceWithSF] != 1:
                    for i in range(numOfCurrMessage[packetNum] - devicesLastGetNumOfMessage[currDeviceWithSF] - 1):
                        devicesFailTimestamps[currDeviceWithSF].append(str((int(devicesSuccesTimestamps[currDeviceWithSF][-1]) + (i+1)*timePeriod)))

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
