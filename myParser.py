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



def parse(inputFile, outputFile):
    fieldnames = ['id device',   'num of message', 'timestamps']
    data = [' '] * 3
    res_list = []
    devicesTimestamps = {}
    devicesMessage = {}
    messageCounter = 0
    currDevice = '-1'

    f = open(inputFile)
    for line in f:
        if line.find("fcnt") != -1:
            currDevice = line.split(' ')[-2]
            continue

        if line.find("JSON up: {\"rxpk\"") != -1:
            messageCounter += 1
            tmp = line.split('JSON up:')
            d = json.loads(tmp[1])

            currDevice = currDevice + ' ' + d['rxpk'][-1]['datr']

            if devicesTimestamps.get(currDevice) == None:
                devicesTimestamps[currDevice] = [str(d['rxpk'][-1]['tmst'])]
                devicesMessage[currDevice] = 1
            else:
                devicesTimestamps[currDevice].append(str(d['rxpk'][-1]['tmst']))
                devicesMessage[currDevice] += 1

            currDevice = '-1'
            continue
    f.close()

    for key in devicesMessage.keys():
        data[0] = key
        data[1] = str(devicesMessage[key])
        data[2] = ' '.join(devicesTimestamps[key])
        inner_dict = dict(zip(fieldnames, data))
        res_list.append(inner_dict)
    #csv_dict_writer(outputFile + 'Table.csv', fieldnames, res_list)

    f = open(outputFile + 'Text.txt', 'w')
    for entry in res_list:
        f.write(entry['id device'] + ' ' + entry['num of message'] + ' ' + entry['timestamps'] + '\n')
    f.close()
    return devicesTimestamps
