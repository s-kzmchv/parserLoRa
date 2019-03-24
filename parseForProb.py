
import json


currDevice = []
numOfMessageByDevice1 = {}
numOfMessageByDevice2 = {}
numOfMessageByDevice2Fail = {}
lastNumOfMessage = {}


nameOfLog = 'syslog_13_SF8_23_SF7'
begin = 52706483
end = 17035491

flag = False

f = open(nameOfLog)
for line in f:
    if line.find("fcnt") != -1:
        currDeviceName = line.split(' ')[-2]
        numOfCurrMessage = int(line.split(' ')[-1].split('=')[-1][:-2])
        currDevice.append(currDeviceName)

        if not flag:
            continue

        if numOfMessageByDevice2.get(currDeviceName) == None:
            numOfMessageByDevice2[currDeviceName] = 1
            numOfMessageByDevice2Fail[currDeviceName] = 0
            lastNumOfMessage[currDeviceName] = numOfCurrMessage
        else:
            numOfMessageByDevice2[currDeviceName] += 1
            numOfMessageByDevice2Fail[currDeviceName] = numOfCurrMessage - lastNumOfMessage[currDeviceName] - 1
            lastNumOfMessage[currDeviceName] = numOfCurrMessage

        # numOfCurrMessage.append(int(line.split(' ')[-1].split('=')[-1][:-2]))
        continue

    if line.find("JSON up: {\"rxpk\"") != -1:

        tmp = line.split('JSON up:')
        d = json.loads(tmp[1])
        # numOfTimestamps = len(d['rxpk'])
        for packetNum in range(len(d['rxpk'])):
            # timeStamp = d['rxpk'][-1]['tmst']
            timeStamp = d['rxpk'][packetNum]['tmst']

            if timeStamp == begin:
                if flag == True:
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
                flag = True

            if timeStamp == end:
                if flag == False:
                    print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAaa")
                flag = False

            if not flag:
                continue


            if len(currDevice) > packetNum:
                currDeviceWithSF = currDevice[packetNum] + ' ' + d['rxpk'][packetNum]['datr']
            else:
                # currDeviceWithSF = '-1 ' + d['rxpk'][packetNum]['datr']
                break

            # if currDeviceWithSF == "0052013C SF8BW125":
            #     print(timeStamp)


            if numOfMessageByDevice1.get(currDeviceWithSF) == None:
                numOfMessageByDevice1[currDeviceWithSF] = 1
            else:
                numOfMessageByDevice1[currDeviceWithSF] += 1


        currDevice = []

f.close()


print(numOfMessageByDevice1)


numOfDevices = 0
for i in nameOfLog.split('_'):
    if i.isdigit():
        numOfDevices += int(i)

numOfSuccessMessagesAll = sum(numOfMessageByDevice1.values())
maxNumOfMessages = max(numOfMessageByDevice1.values())
print("First way P = {} \n".format(numOfSuccessMessagesAll / (maxNumOfMessages * numOfDevices)))

print(numOfMessageByDevice2)
print(numOfMessageByDevice2Fail)

for key in numOfMessageByDevice2Fail:
    numOfMessageByDevice2Fail[key] += maxNumOfMessages - numOfMessageByDevice2[key] - numOfMessageByDevice2Fail[key]

print(numOfMessageByDevice2Fail)


numOfSuccessMessagesAll = sum(numOfMessageByDevice2.values())
numOfFailMessagesAll = sum(numOfMessageByDevice2Fail.values())


print("Second way P = {} \n".format(numOfSuccessMessagesAll / (numOfFailMessagesAll + numOfSuccessMessagesAll + maxNumOfMessages*(numOfDevices-len(numOfMessageByDevice2)))))