import hid
import time
import math
import threading

# Set up the gamepad
vendor_id = 0x18d1
product_id = 0x9400
device = hid.device()
device.open(vendor_id, product_id)

stopReport = [0]*5
stopReport[0] = 5

def getRumbleReport(intensity):
    report = [0]*5
    report[0] = 5
    report[2] = intensity

    index = -1
    value = -1

    if intensity <= 1:
        index = 3
        value = 255
    elif intensity <= 85:
        index = 1
        value = (intensity - 1)*255/84
    elif intensity <= 169:
        index = 2
        value = (intensity - 85)*255/84
    else:
        index = 4
        value = (intensity - 169)*255/86

    report[index] = int(value)

    return bytearray(report)

lastRValue = -1
currentRValue = 0

lastLValue = -1
currentLValue = 0

def sendReportLoop():
    while True:
        report = [0] * 5
        report[0] = 5

        report[2] = currentLValue
        report[4] = currentRValue

        device.write(bytearray(report))

threading.Thread(target=sendReportLoop).start()


while True:
    inReport = device.read(64)
    currentRValue = inReport[9]
    currentLValue = inReport[8]

    shouldPrint = False

    if lastRValue != currentRValue:
        lastRValue = currentRValue
        shouldPrint = True

    if lastLValue != currentLValue:
        lastLValue = currentLValue
        shouldPrint = True

    if shouldPrint:
        print(currentLValue, currentRValue)
