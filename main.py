from myParser import parse
from bisect import bisect_left
from itertools import chain, combinations, product
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


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

    devicesTimestampsSuccess = parse('syslog_dif_dBm_SF7','out')
    # print(devicesTimestampsSuccess)
    begin = 539266819
    end = 1430876615
    step = 7000000
    e = 100000

    timeOnAir = 119000
    i = 3
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
    devicesTimestampsFail.pop('-1 SF7BW125')
    # for entry in devicesTimestampsSuccess['-1 SF7BW125']:
    #     flag = True
    #     for key in devicesTimestampsFalse:
    #         if key == '-1 SF7BW125':
    #             continue
    #         if len(devicesTimestampsFalse[key]) != 0 and abs(entry - takeClosest(devicesTimestampsFalse[key],entry)) < e:
    #             flag = False
    #     if flag:
    #         print(str(entry) + ' not find')

    f = open('outFailText.txt', 'w')
    for entry in devicesTimestampsFail:
        f.write(entry + ' ' + str(len(devicesTimestampsFail[entry])) + ' ' + str(devicesTimestampsFail[entry]) + '\n')
    f.close()


    m = sum(len(entry) for entry in devicesTimestampsSuccess)
    print(m)

    part = timeOnAir / i

    # test
    # timeOnAir = 10
    # devicesTimestampsSuccess ={'1': [100,200,300], '2': [400,500,600], '3': [399,695,797], '4':[300]}
    # devicesTimestampsFail ={'1': [430,540,640], '2': [700,800,900], '3':[], '4':[790]}
    # test




    for n in range(3):
        if n == 0:
            continue

        dict = {}
        listForEntry = [0]*n
        successX = [0] * i
        failX = [0] * i
        crossTimestapsSuccess = {}
        crossTimestapsFail = {}
        for key in devicesTimestampsSuccess:
            for entry in devicesTimestampsSuccess[key]:
                crossTimestapsSuccess[entry] = []
                numberOfParticipant = 0
                tmpSuccessX = [0]*i
                listForEntry = [''] * n

                flag = False

                for currDevice in devicesTimestampsSuccess:

                    if key == currDevice:
                        continue

                    nearestTimestamps = takeClosest(devicesTimestampsSuccess[currDevice],entry)
                    x = nearestTimestamps - entry

                    if x < 0 and abs(x) < timeOnAir:
                        # print("Attention " + str(entry) + " " + str(nearestTimestamps))
                        flag = True
                        break

                    if x < timeOnAir and x > 0:
                        numberOfParticipant = numberOfParticipant + 1

                        if numberOfParticipant > n:
                            # crossTimestaps.pop(entry)
                            break

                        j = 0
                        while x > part*(j+1):
                            j = j + 1
                        tmpSuccessX[j] = tmpSuccessX[j] + 1
                        listForEntry[numberOfParticipant - 1] = str(round((j+1)*part,1))
                        crossTimestapsSuccess[entry].append(nearestTimestamps)

                if numberOfParticipant > n or flag:
                    crossTimestapsSuccess.pop(entry)
                    continue

                for currDevice in devicesTimestampsFail:

                    if key == currDevice:
                        continue

                    if len(devicesTimestampsFail[currDevice]) == 0:
                        continue

                    nearestTimestamps = takeClosest(devicesTimestampsFail[currDevice],entry)
                    x = nearestTimestamps - entry

                    if x < 0 and abs(x) < timeOnAir:
                        flag = True
                        break

                    if x < timeOnAir and x > 0:
                        numberOfParticipant = numberOfParticipant + 1

                        if numberOfParticipant > n:
                            crossTimestapsSuccess.pop(entry)
                            break

                        j = 0
                        while x > part*(j+1):
                            j = j + 1
                        tmpSuccessX[j] = tmpSuccessX[j] + 1
                        listForEntry[numberOfParticipant - 1] = str(round((j+1)*part,1))
                        crossTimestapsSuccess[entry].append(nearestTimestamps)

                if numberOfParticipant < n or flag:
                    crossTimestapsSuccess.pop(entry)
                    continue
                if numberOfParticipant == n:
                    for j in range(i):
                        successX[j] = successX[j] + tmpSuccessX[j]

                    res = ' '.join(listForEntry)
                    if dict.get(res) == None:
                        dict[res] = [1, 0]
                    else:
                        dict[res][0] += 1

        for key in devicesTimestampsFail:
            for entry in devicesTimestampsFail[key]:
                crossTimestapsFail[entry] = []
                numberOfParticipant = 0
                tmpFailX = [0]*i
                listForEntry = [''] * n
                flag = False
                for currDevice in devicesTimestampsSuccess:

                    if key == currDevice:
                        continue

                    nearestTimestamps = takeClosest(devicesTimestampsSuccess[currDevice],entry)
                    x = nearestTimestamps - entry

                    if x < 0 and abs(x) < timeOnAir:
                        flag = True
                        break

                    if x < timeOnAir and x > 0:
                        numberOfParticipant = numberOfParticipant + 1

                        if numberOfParticipant > n:
                            break

                        j = 0
                        while x > part*(j+1):
                            j = j + 1
                        tmpFailX[j] = tmpFailX[j] + 1
                        listForEntry[numberOfParticipant - 1] = str(round((j+1)*part,1))
                        crossTimestapsFail[entry].append(nearestTimestamps)

                if numberOfParticipant > n or flag:
                    crossTimestapsFail.pop(entry)
                    continue
                for currDevice in devicesTimestampsFail:

                    if key == currDevice:
                        continue

                    if len(devicesTimestampsFail[currDevice]) == 0:
                        continue

                    nearestTimestamps = takeClosest(devicesTimestampsFail[currDevice],entry)
                    x = nearestTimestamps - entry

                    if x < 0 and abs(x) < timeOnAir:
                        flag = True
                        break

                    if x < timeOnAir and x > 0:
                        numberOfParticipant = numberOfParticipant + 1

                        if numberOfParticipant > n:
                            crossTimestapsFail.pop(entry)
                            break

                        j = 0
                        while x > part*(j+1):
                            j = j + 1
                        tmpFailX[j] = tmpFailX[j] + 1
                        listForEntry[numberOfParticipant - 1] = str(round((j+1)*part,1))
                        crossTimestapsFail[entry].append(nearestTimestamps)

                if numberOfParticipant < n or flag:
                    crossTimestapsFail.pop(entry)
                    continue
                if numberOfParticipant == n:
                    for j in range(i):
                        failX[j] = failX[j] + tmpFailX[j]

                    res = ' '.join(listForEntry)
                    if dict.get(res) == None:
                        dict[res] = [0, 1]
                    else:
                        dict[res][1] += 1

        print('n = ' + str(n))
        if n == 1:
            print('Success  = ' + str(successX))
            print('Fail     = ' + str(failX))

        # else:
        #     for j in dict:
        #         print(j + ' Success: ' + str(dict[j][0]) + ' Fail: ' + str(dict[j][1]))
        #
        # Pr = [0.0] * i
        # for j in range(i):
        #     if successX[j] + failX[j] != 0:
        #         Pr[j] = successX[j] / (successX[j] + failX[j])
        #         print('Pr[success | x = {}] = {}'.format((j+1)*part,float(Pr[j])))

        # print('success transfer')
        #for crossTimestap in crossTimestapsSuccess:
         #   if len(crossTimestapsSuccess[crossTimestap]) != 0:
          #      print(str(crossTimestap) + ': ' + str(crossTimestapsSuccess[crossTimestap]))

        # print('fail transfer')
        # for crossTimestap in crossTimestapsFail:
        #   if len(crossTimestapsFail[crossTimestap]) != 0:
        #       print(str(crossTimestap) + ': ' + str(crossTimestapsFail[crossTimestap]))

            Pr = []
            Xi = []
            for val in product(range(i), repeat=n):
                strVal = ''
                for j in range(len(val)-1):
                    strVal = strVal + str(round((val[j]+1)*part,1)) + ' '
                strVal = strVal +  str(round((val[-1]+1)*part,1))
                # print(strVal)
                # print(val + ' Success: ' + str(dict[j][0]) + ' Fail: ' + str(dict[j][1]))
                if dict.get(strVal) != None:
                    print('Pr[success | ' + strVal + '] = ' + str(dict[strVal][0] / (dict[strVal][0] + dict[strVal][1])))
                    Pr.append(dict[strVal][0] / (dict[strVal][0] + dict[strVal][1]))
                    Xi.append(strVal)

            plt.plot(Xi, Pr, color="g", label='something')
            plt.xlabel('Xi')
            plt.ylabel('Pr[success]')
            plt.legend()
            # plt.savefig("n={}.png".format(n))
            plt.show()
            plt.clf()

        if n == 2:
            count = 0
            for val in product(range(i), repeat=n):
                count += 1
                strVal = ''
                for j in range(len(val) - 1):
                    strVal = strVal + str(round((val[j] + 1) * part, 1)) + ' '
                strVal = strVal + str(round((val[-1] + 1) * part, 1))
                if dict.get(strVal) != None:
                #     print(dict[strVal][0], end=' ')
                # else:
                #     print('0', end=' '),
                #
                # if count == i:
                #     count = 0
                #     print('')
                    print(strVal +' ' + str(dict[strVal][0]) + ' ' + str(dict[strVal][1]))
                else:
                    print(strVal + ' 0 0')

            for val in product(range(i), repeat=n):
                strVal = ''
                for j in range(len(val)-1):
                    strVal = strVal + str(round((val[j]+1)*part,1)) + ' '
                strVal = strVal +  str(round((val[-1]+1)*part,1))
                # print(strVal)
                # print(val + ' Success: ' + str(dict[j][0]) + ' Fail: ' + str(dict[j][1]))
                if dict.get(strVal) != None:
                    print('Pr[success | ' + strVal + '] = ' + str(dict[strVal][0] / (dict[strVal][0] + dict[strVal][1])))
