from myParser import parse
from bisect import bisect_left
from itertools import chain, combinations, product
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random

# 1470482627
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

if __name__ == "__main__":
    devicesTimestampsSuccess = parse('syslog_22_SF7','out')
    # print(devicesTimestampsSuccess)
    begin = 845740083
    end = 2255666099
    step = 7000000
    e = 100000
    timeOnAir = 119000
    i = 9
    devicesTimestampsFail = {}
    for key in devicesTimestampsSuccess:
        # print(key)
        devicesTimestampsSuccess[key] = [int(entry) for entry in devicesTimestampsSuccess[key]]
        # print(devicesTimestampsSuccess[key])

        devicesTimestampsFail[key] = []
        nextTimestamp = devicesTimestampsSuccess[key][0] - step

        while nextTimestamp > begin:
            devicesTimestampsFail[key].append(nextTimestamp)
            nextTimestamp = nextTimestamp - step
        devicesTimestampsFail[key].reverse()
        nextTimestamp = devicesTimestampsSuccess[key][0] + step
        while nextTimestamp < end:
            if nextTimestamp - takeClosest(devicesTimestampsSuccess[key],nextTimestamp) > e:
                devicesTimestampsFail[key].append(nextTimestamp)
            nextTimestamp = nextTimestamp + step

        # print(devicesTimestampsFail[key])
    if devicesTimestampsFail.get('-1 SF7BW125') != None:
        devicesTimestampsFail.pop('-1 SF7BW125')


    f = open('outFailText.txt', 'w')
    for entry in devicesTimestampsFail:
        f.write(entry + ' ' + str(len(devicesTimestampsFail[entry])) + ' ' + str(devicesTimestampsFail[entry]) + '\n')
    f.close()


    m = sum(len(entry) for entry in devicesTimestampsSuccess)
    print(m)

    part = timeOnAir / i

    # test
    # timeOnAir = 10
    # devicesTimestampsSuccess ={'1': [100], '2': [400], '3': [0], '4':[20]}
    # devicesTimestampsFail ={'1': [], '2': [99], '3':[], '4':[]}
    # test

    for n in range(3):
        if n == 0:
            continue
        if n == 2:
            part = timeOnAir

        dict = {}
        listForEntry = [0]*n

        for key in devicesTimestampsSuccess:
            for entry in devicesTimestampsSuccess[key]:
                numberOfParticipant = 0
                listForEntry = [''] * n

                for currDevice in devicesTimestampsSuccess:
                    flag = False
                    if key == currDevice:
                        continue

                    nearestTimestamps = takeClosest(devicesTimestampsSuccess[currDevice],entry)
                    x = nearestTimestamps - entry

                    if x < 0 and abs(x) < timeOnAir:
                        # print("Attention " + str(entry) + " " + str(nearestTimestamps))
                        flag = True
                        # break

                    if abs(x) < timeOnAir :
                        numberOfParticipant = numberOfParticipant + 1

                        if numberOfParticipant > n:
                            # crossTimestaps.pop(entry)
                            break

                        j = 0
                        while abs(x) > part*(j+1):
                            j = j + 1
                        if flag:
                            listForEntry[numberOfParticipant - 1] = str(round((j + 1) * part * (-1),1))
                        else:
                            listForEntry[numberOfParticipant - 1] = str(round((j + 1) * part, 1))


                if numberOfParticipant > n:
                    continue

                for currDevice in devicesTimestampsFail:
                    flag = False
                    if key == currDevice:
                        continue

                    if len(devicesTimestampsFail[currDevice]) == 0:
                        continue

                    nearestTimestamps = takeClosest(devicesTimestampsFail[currDevice],entry)
                    x = nearestTimestamps - entry

                    if x < 0 and abs(x) < timeOnAir:
                        flag = True
                        # break

                    if abs(x) < timeOnAir :
                        numberOfParticipant = numberOfParticipant + 1

                        if numberOfParticipant > n:
                            break

                        j = 0
                        while abs(x) > part*(j+1):
                            j = j + 1
                        if flag:
                            listForEntry[numberOfParticipant - 1] = str(round((j + 1) * part * (-1),1))
                        else:
                            listForEntry[numberOfParticipant - 1] = str(round((j + 1) * part, 1))


                if numberOfParticipant < n:
                    continue
                if numberOfParticipant == n:
                    res = ' '.join(listForEntry)
                    if dict.get(res) == None:
                        dict[res] = [1, 0]
                    else:
                        dict[res][0] += 1

        for key in devicesTimestampsFail:
            for entry in devicesTimestampsFail[key]:
                numberOfParticipant = 0
                listForEntry = [''] * n

                for currDevice in devicesTimestampsSuccess:
                    flag = False
                    if key == currDevice:
                        continue

                    nearestTimestamps = takeClosest(devicesTimestampsSuccess[currDevice],entry)
                    x = nearestTimestamps - entry

                    if x < 0 and abs(x) < timeOnAir:
                        flag = True
                        # break

                    if abs(x) < timeOnAir :
                        numberOfParticipant = numberOfParticipant + 1

                        if numberOfParticipant > n:
                            break

                        j = 0
                        while abs(x) > part*(j+1):
                            j = j + 1
                        if flag:
                            listForEntry[numberOfParticipant - 1] = str(round((j + 1) * part * (-1),1))
                        else:
                            listForEntry[numberOfParticipant - 1] = str(round((j + 1) * part, 1))

                if numberOfParticipant > n:
                    continue
                for currDevice in devicesTimestampsFail:
                    flag = False
                    if key == currDevice:
                        continue

                    if len(devicesTimestampsFail[currDevice]) == 0:
                        continue

                    nearestTimestamps = takeClosest(devicesTimestampsFail[currDevice],entry)
                    x = nearestTimestamps - entry

                    if x < 0 and abs(x) < timeOnAir:
                        flag = True
                        # break

                    if abs(x) < timeOnAir :
                        numberOfParticipant = numberOfParticipant + 1

                        if numberOfParticipant > n:
                            break

                        j = 0
                        while abs(x) > part*(j+1):
                            j = j + 1
                        if flag:
                            listForEntry[numberOfParticipant - 1] = str(round((j + 1) * part * (-1),1))
                        else:
                            listForEntry[numberOfParticipant - 1] = str(round((j + 1) * part, 1))

                if numberOfParticipant < n:
                    continue
                if numberOfParticipant == n:
                    res = ' '.join(listForEntry)
                    if dict.get(res) == None:
                        dict[res] = [0, 1]
                    else:
                        dict[res][1] += 1

        print('n = ' + str(n))
        if n == 1:
            #вывод кол-ва в промежутке
            resStr = ''
            Pr = []
            Xi = []
            N_message = []
            for val in product(range(i*2), repeat=n):
                strVal = ''
                for j in range(len(val) - 1):
                    if val[j] < i:
                        strVal = strVal + str(round((i - val[j]) * part * (-1), 1)) + ' '
                    else:
                        strVal = strVal + str(round((val[j] - i + 1) * part , 1)) + ' '
                if val[-1] < i:
                     strVal = strVal + str(round((i - val[-1]) * part * (-1), 1))
                else:
                     strVal = strVal + str(round((val[-1] - i + 1) * part, 1))

                if dict.get(strVal) != None:
                    print(strVal + ' Success: ' + str(dict[strVal][0]) + ' Fail: ' + str(dict[strVal][1]))
                    resStr = resStr + 'Pr[success | ' + strVal + '] = ' + str(dict[strVal][0] / (dict[strVal][0] + dict[strVal][1])) +'\n'
                    Pr.append(dict[strVal][0] / (dict[strVal][0] + dict[strVal][1]))
                    N_message.append(dict[strVal][0] + dict[strVal][1])
                    Xi.append(float(strVal))
                    # Xi.append(strVal)
                else:
                    # print(strVal + ' Success: 0 Fail: 0')
                    # resStr = resStr + 'Pr[success | ' + strVal + '] = 0 \n'
                    Pr.append(0)
                    N_message.append(0)
                    Xi.append(float(strVal))
                    # Xi.append(strVal)
            print(resStr)

            plt.plot(Xi, Pr, color="g", label='probability')
            plt.xlabel('Xi')
            plt.ylabel('Pr[success]')
            plt.legend()
            plt.savefig("n={} probabilities.png".format(n))
            # plt.show()
            plt.clf()

            plt.plot(Xi, N_message, color="g", label='packet')
            plt.xlabel('Xi')
            plt.ylabel('NumOfMessage')
            plt.legend()
            plt.savefig("n={} packets.png".format(n))
            # plt.show()
            plt.clf()


######################################################################
        if n == -1:

            for val in product(range(i), repeat=n):
                strVal = ''
                for j in range(len(val) - 1):
                    strVal = strVal + str(round((val[j] + 1) * part, 1)) + ' '
                strVal = strVal + str(round((val[-1] + 1) * part, 1))
                if dict.get(strVal) != None:
                    print(strVal +' Success: ' + str(dict[strVal][0]) + ' Fail: ' + str(dict[strVal][1]))
                else:
                    print(strVal + ' Success: 0 Fail: 0')

            dictX2 = {}
            for val in product(range(i), repeat=n):
                strVal = ''
                for j in range(len(val)-1):
                    strVal = strVal + str(round((val[j]+1)*part,1)) + ' '
                strVal = strVal +  str(round((val[-1]+1)*part,1))

                tmp = strVal.split(' ')

                if dictX2.get(tmp[1]) == None:
                    dictX2[tmp[1]] = []


                if dict.get(strVal) != None:
                    print('Pr[success | ' + strVal + '] = ' + str(dict[strVal][0] / (dict[strVal][0] + dict[strVal][1])))
                    dictX2[tmp[1]].append(dict[strVal][0] / (dict[strVal][0] + dict[strVal][1]))

                else:
                    print(
                        'Pr[success | ' + strVal + '] = 0')
                    dictX2[tmp[1]].append(0)


            keys = dictX2.keys()
            for entry in dictX2:
                tmp = np.random.rand(1,3)
                tmp = tmp[0]
                plt.plot(keys, dictX2[entry], color=tmp, label='x2 = {}'.format(entry))

            plt.xlabel('Xi')
            plt.ylabel('Pr[success]')
            plt.legend()
            plt.savefig("n={}.png".format(n))
            # plt.show()
            plt.clf()
######################################################################


        if n > 1:
            for val in product(range(i * 2), repeat=n):
                strVal = ''
                for j in range(len(val) - 1):
                    if val[j] < i:
                        strVal = strVal + str(round((i - val[j]) * part * (-1), 1)) + ' '
                    else:
                        strVal = strVal + str(round((val[j] - i + 1) * part, 1)) + ' '
                if val[-1] < i:
                    strVal = strVal + str(round((i - val[-1]) * part * (-1), 1))
                else:
                    strVal = strVal + str(round((val[-1] - i + 1) * part, 1))

                if dict.get(strVal) != None:
                    print(strVal +' Success: ' + str(dict[strVal][0]) + ' Fail: ' + str(dict[strVal][1]))
                    print(
                        'Pr[success | ' + strVal + '] = ' + str(dict[strVal][0] / (dict[strVal][0] + dict[strVal][1])))
                # else:
                #     print(strVal + ' Success: 0 Fail: 0')

