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


fieldnames = ['time first', 'count first', 'difference with the previous for first', 'error first', 'time second',
              'count second', 'difference with the previous for second', 'error second',
              'difference between first and second', 'interval estimate']
data = [' '] * 10
data_prev = [' '] * 10
res_list = []

numDevice = 0


devices = {'00650827': 0, '0050013B': 1}



# new_time =0
# new_count =0
# old_time =0
# old_count =0
#
# time_not_in_table = 0
# count_not_in_table = 0
d =0

f = open('syslog_SF11_for2and4')

for line in f:

    if line.find("fcnt") != -1:
        numDevice = devices[line.split(' ')[-2]]

        if data[numDevice*4 + 1] == data_prev[numDevice*4 + 1] and data[numDevice*4 + 0] == data_prev[numDevice*4 + 0]:
            data [numDevice*4 + 1] = line.split('=')[1][:-2]
        else:
            for i in range(2):
                for j in range(2):
                    if data[j*4 + i] == data_prev[j*4 + i]:
                        data[j * 4 + i] = ' '
            if data[numDevice*4 + 1] == ' ':
                data[0] = data[numDevice*4 + 0]
                data[4] = data[0]

            data_prev = data.copy()
            inner_dict = dict(zip(fieldnames, data))
            res_list.append(inner_dict)
            data[numDevice * 4 + 1] = line.split('=')[1][:-2]



        # devices[idDevice] = line.split('=')[1][:-2]
        # if count_not_in_table == 0:
        #     new_count = line.split('=')[1][:-2]
        #     count_not_in_table = 1
        # else:

        print(line.split('=')[1][:-2])
        continue

    if line.find("JSON up: {\"rxpk\"") != -1:
        tmp = line.split(' ')
        d = json.loads(tmp[7])

        # if int(d['rxpk'][0]['tmst']) == 1693903028:
        #     print('olololo')

        if data[numDevice*4 + 0] == data_prev[numDevice*4 + 0]:
            data [numDevice*4 + 0] = d['rxpk'][0]['tmst']
        else:
            for i in range(2):
                for j in range(2):
                    if data[j*4 + i] == data_prev[j*4 + i]:
                        data[j * 4 + i] = ' '

            if data[numDevice*4 + 1] == ' ':
                data[0] = data[numDevice*4 + 0]
                data[4] = data[0]
                inner_dict = dict(zip(fieldnames, data))
                res_list.append(inner_dict)
                data[0] = d['rxpk'][0]['tmst']
                data[4] = d['rxpk'][0]['tmst']


            data_prev = data.copy()
            inner_dict = dict(zip(fieldnames, data))
            res_list.append(inner_dict)
            data[numDevice * 4 + 0] = d['rxpk'][0]['tmst']

        # if time_not_in_table == 0:
        #     new_time = d['rxpk'][0]['tmst']
        #     time_not_in_table = 1

        print(d['rxpk'][0]['tmst'])
        continue

    # if time_not_in_table == 1 and count_not_in_table == 1:
    #     if (int(new_count) > 100): #тут надо испрвавить
    #         data[0] = new_time
    #         data[1] = new_count
    #         data[2] = ' ' #исправить
    #         data[3] = '1'
    #         data[4] = ' '
    #         data[5] = ' '
    #         data[6] = ' '
    #         data[7] = ' '
    #         data[8] = ' '
    #
    #     else:
    #         data[0] = ' '
    #         data[1] = ' '
    #         data[2] = ' '  # исправить
    #         data[3] = '0'
    #         data[4] = new_time
    #         data[5] = new_count
    #         data[6] = ' '
    #         data[7] = '1'
    #         data[8] = ' '
    #
    #     data_prev = data
    #     inner_dict = dict(zip(fieldnames, data))
    #     res_list.append(inner_dict)
    #     time_not_in_table = 0
    #     count_not_in_table = 0




f.close()

for i in range(2):
    for j in range(2):
        if data[j * 4 + i] == data_prev[j * 4 + i]:
            data[j * 4 + i] = ' '

if data[numDevice * 4 + 1] == ' ':
    data[0] = data[numDevice * 4 + 0]
    data[4] = data[0]
    if (data[0] != d['rxpk'][0]['tmst']):
        inner_dict = dict(zip(fieldnames, data))
        res_list.append(inner_dict)
    data[0] = d['rxpk'][0]['tmst']
    data[4] = d['rxpk'][0]['tmst']

data_prev = data.copy()
inner_dict = dict(zip(fieldnames, data))
res_list.append(inner_dict)
data[numDevice * 4 + 0] = d['rxpk'][0]['tmst']

# data = ["first_name,last_name,city".split(","),
#         "Tyrese,Hirthe,Strackeport".split(","),
#         "Jules,Dicki,Lake Nickolasville".split(","),
#         "Dedric,Medhurst,Stiedemannberg".split(",")
#         ]

# my_list = []
# fieldnames = data[0]
# for values in data[1:]:
#     inner_dict = dict(zip(fieldnames, values))
#     my_list.append(inner_dict)

path = "dict_output.csv"
csv_dict_writer(path, fieldnames, res_list)