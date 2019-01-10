import csv
import json


class Device:
    def __init__(self, lastTimestamp, numOfMessage):
        self.lastTimestamp = lastTimestamp
        self.numOfMessage = numOfMessage



def csv_dict_writer(path, fieldnames, data):
    """
    Writes a CSV file using DictWriter
    """
    with open(path, "w", newline='') as out_file:
        writer = csv.DictWriter(out_file, delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)


fieldnames = ['timestamp', 'id device', 'error', 'num of message', 'previous timestamp difference', 'previous timestamp difference for this device']
data = [' '] * 6
data_prev = [' '] * 6
res_list = []

devices = {}

messageCounter = 0
# todo не работает время между двумя сообщениями от одного узл


f = open('syslog_dif_dB_SF11')


for line in f:

    if line.find("fcnt") != -1:
        numDevice = line.split(' ')[-2]

        if devices.get(numDevice) == None:
            devices[numDevice] = Device(' ',0)

        data[1] = numDevice
        data[2] = '0'
        data[3] = line.split('=')[1][:-2]

        print(line.split('=')[1][:-2])
        continue

    if line.find("JSON up: {\"rxpk\"") != -1:
        messageCounter += 1
        tmp = line.split('JSON up:')
        d = json.loads(tmp[1])

        # if int(d['rxpk'][0]['tmst']) == 361757571:
        #     print('olololo')

        if (data[0] != ' '):
            data[4] = str(int( int(d['rxpk'][0]['tmst']  - data[0]) ))

        if (data[1] != data_prev[1] and data[1] != ' ') or (data[3] != data_prev[3] and data[3] != ' '):

            if data[1] != data_prev[1] and data[1] != ' ':
                if devices[data[1]].lastTimestamp != ' ':
                    # tmp1 = int(d['rxpk'][0]['tmst']) - int(devices[data[1]].lastTimestamp)
                    # tmp2 = (messageCounter-1) - int(devices[data[1]].numOfMessage)
                    # tmp3 = tmp1 / tmp2
                    data[5] = str((int(d['rxpk'][0]['tmst']) - int(devices[data[1]].lastTimestamp)) / ((messageCounter-1) - int(devices[data[1]].numOfMessage)) )
                else:
                    data[5] = ' '
            else:
                data[5] = ' '
            devices[data[1]].lastTimestamp = d['rxpk'][0]['tmst']
            devices[data[1]].numOfMessage = messageCounter
            data[0] = d['rxpk'][0]['tmst']
            # data_prev = data.copy()
            # inner_dict = dict(zip(fieldnames, data))
            # res_list.append(inner_dict)
        else:
            data[1] = ' '
            data[2] = '1'
            data[3] = ' '
            data[0] = d['rxpk'][0]['tmst']
            data[5] = ' '
        data_prev = data.copy()
        inner_dict = dict(zip(fieldnames, data))
        res_list.append(inner_dict)



        print(d['rxpk'][0]['tmst'])
        continue


f.close()




path = "dict_output.csv"
csv_dict_writer(path, fieldnames, res_list)