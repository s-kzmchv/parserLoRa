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


fieldnames = ['timestamp', 'id device', 'error', 'num of message']
data = [' '] * 4
data_prev = [' '] * 4
res_list = []



f = open('syslog_dif_dB_SF11')


for line in f:

    if line.find("fcnt") != -1:
        numDevice = line.split(' ')[-2]

        data[1] = numDevice
        data[2] = '0'
        data[3] = line.split('=')[1][:-2]

        # if data[numDevice*4 + 1] == data_prev[numDevice*4 + 1] and data[numDevice*4 + 0] == data_prev[numDevice*4 + 0]:
        #     data [numDevice*4 + 1] = line.split('=')[1][:-2]
        # else:
        #     for i in range(2):
        #         for j in range(2):
        #             if data[j*4 + i] == data_prev[j*4 + i]:
        #                 data[j * 4 + i] = ' '
        #     if data[numDevice*4 + 1] == ' ':
        #         data[0] = data[numDevice*4 + 0]
        #         data[4] = data[0]
        #
        #     data_prev = data.copy()
        #     inner_dict = dict(zip(fieldnames, data))
        #     res_list.append(inner_dict)
        #     data[numDevice * 4 + 1] = line.split('=')[1][:-2]
        #
        #
        #
        # # devices[idDevice] = line.split('=')[1][:-2]
        # # if count_not_in_table == 0:
        # #     new_count = line.split('=')[1][:-2]
        # #     count_not_in_table = 1
        # # else:
        #
        print(line.split('=')[1][:-2])
        continue

    if line.find("JSON up: {\"rxpk\"") != -1:
        tmp = line.split('JSON up:')
        d = json.loads(tmp[1])

        if int(d['rxpk'][0]['tmst']) == 361757571:
            print('olololo')


        if (data[1] != data_prev[1] and data[1] != ' ') or (data[3] != data_prev[3] and data[3] != ' '):
            data[0] = d['rxpk'][0]['tmst']
            # data_prev = data.copy()
            # inner_dict = dict(zip(fieldnames, data))
            # res_list.append(inner_dict)
        else:
            data[1] = ' '
            data[2] = '1'
            data[3] = ' '
            data[0] = d['rxpk'][0]['tmst']
        data_prev = data.copy()
        inner_dict = dict(zip(fieldnames, data))
        res_list.append(inner_dict)


        #
        # # if int(d['rxpk'][0]['tmst']) == 1693903028:
        # #     print('olololo')
        #
        # if data[numDevice*4 + 0] == data_prev[numDevice*4 + 0]:
        #     data [numDevice*4 + 0] = d['rxpk'][0]['tmst']
        # else:
        #     for i in range(2):
        #         for j in range(2):
        #             if data[j*4 + i] == data_prev[j*4 + i]:
        #                 data[j * 4 + i] = ' '
        #
        #     if data[numDevice*4 + 1] == ' ':
        #         data[0] = data[numDevice*4 + 0]
        #         data[4] = data[0]
        #         inner_dict = dict(zip(fieldnames, data))
        #         res_list.append(inner_dict)
        #         data[0] = d['rxpk'][0]['tmst']
        #         data[4] = d['rxpk'][0]['tmst']
        #
        #
        #     data_prev = data.copy()
        #     inner_dict = dict(zip(fieldnames, data))
        #     res_list.append(inner_dict)
        #     data[numDevice * 4 + 0] = d['rxpk'][0]['tmst']

        # if time_not_in_table == 0:
        #     new_time = d['rxpk'][0]['tmst']
        #     time_not_in_table = 1

        print(d['rxpk'][0]['tmst'])
        continue


f.close()




path = "dict_output.csv"
csv_dict_writer(path, fieldnames, res_list)