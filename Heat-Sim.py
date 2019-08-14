import numpy
import matplotlib.pyplot as plt
import time
import math


genDes = 0
peopleNum = 3
p1Changes = [-2, 4, 4, 15, 20, 20, 20]
p2Changes = []
p3Changes = [1, 8]
p1Intol = 0
p3Intol = 0
p2Intol = 0
rooms = 4
weeks = 2
p1Pref = 65
p2Pref = 70
p3Pref = 75
initTemp = 55
ambTemp = 30
intolSwayConst = .5  # the least tolerant has 2x the sway
timeStepNum = (24*7)
maxHeat = 28  # 28/hr
sqFt = 900
cubicHouseFeet = 9000
amp = 10
period = 24
powerThreshold = .05
wholeHouseTemp = 70
directSun = True
k = 1  # constant amplitude
f = 0.85  # rate of historical predict discount
# 1 cent to heat 12,103 cubic feet 1deg farenEHGIHEINT

#Establish starting variables


def intol(changes):
    output = 0
    for item in changes:
        # print(.3*(numpy.absolute(item)))
        add = ((-1)/(.3*(numpy.absolute(item))+1)+1)
        # print(add)
        output = output + add
        # print(item)
        # print(output)
    return output

#define each individuals pickiness as determined by the number of times they've changed the temperature

def intolNorm():
    intols = []
    normIntols = []
    intols.append(intol(p1Changes))
    intols.append(intol(p2Changes))
    intols.append(intol(p3Changes))
    maxI = max(intols)
    minI = min(intols)
    for i in intols:
        normIntols.append(intolSwayConst + ((1-intolSwayConst)*(i-minI))/(maxI-minI))
    return(normIntols)

#normalize the intolerance ratings

# print(intolNorm())

# 1 hour intervals, 24 hour chunks, 7 day weeks, starts at 12AM
#             0  1  2  3  4  5  6  7  8  9 10 11 12 13 14 15 16 17 18 19 20 21 22 23
p1SchedW1 = ((1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1))

p2SchedW1 = ((2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2))

p3SchedW1 = ((3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 3, 3, 3))

p1SchedW2 = ((1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1),
             (1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 1, 1, 1))

p2SchedW2 = ((2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2),
             (2, 2, 2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 4, 4, 2, 2, 2))

p3SchedW2 = ((3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 3),
             (3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 3, 4, 4, 4, 4, 4, 4, 3, 4, 4, 4, 3, 3, 3))

p1allTime = (p1SchedW1, p1SchedW2)
p2allTime = (p2SchedW1, p2SchedW2)
p3allTime = (p3SchedW1, p3SchedW2)

#Dummy schedule data for simulation


def locate(pastSched, t):
    Loc = []
    for week in pastSched:
        for day in week:
            Loc.append(day[t])
    return(Loc)


i = 0
limit = 0


def maxLim():
    i = 0
    limit = 0
    while i < weeks:
        limit = limit + 7*(f**i)
        i = i+1
    return limit

#function for determining the drop off value per week

print(maxLim())


def predict(location):
    discountedLoc = []
    count = 0
    weekNum = (len(location)/7)
    roomCt = rooms
    while count < weekNum:
        X = int(count*7)
        Y = int(count*7+7)
        for item in location[X:Y]:
            oneCt = (int(location[X:Y].count(1)))
            twoCt = location[X:Y].count(2)
            threeCt = location[X:Y].count(3)
            fourCt = location[X:Y].count(4)
            discountedLoc.append([(int(oneCt)*f**count), (int(twoCt)*f**count),
                                  (int(threeCt)*f**count), (int(fourCt)*f**count)])
        count = count + 1
    return(discountedLoc)

#guess where an individual will be based on the history of their presence

p1H1Count = (predict((locate(p1allTime, 0))))


def historicDiscOdds(predict):
    first = [item[0] for item in predict]
    second = [item[1] for item in predict]
    third = [item[2] for item in predict]
    fourth = [item[3] for item in predict]
    r1Odds = sum(first)/maxLim()/7
    r2Odds = sum(second)/maxLim()/7
    r3Odds = sum(third)/maxLim()/7
    r4Odds = sum(fourth)/maxLim()/7
    return(round(r1Odds, 4), round(r2Odds, 4), round(r3Odds, 4), round(r4Odds, 4))


r1Odds, r2Odds, r3Odds, r4Odds = historicDiscOdds(predict((locate(p1allTime, 0))))

#Determine the odds of an individual being in a given room

def fullPredict(fullSched, t):
    return(historicDiscOdds(predict((locate(fullSched, t)))))


def tempPower(room, currentTemp, t):
    power = True
    normOddsP1 = 0
    normOddsP2 = 0
    normOddsP3 = 0
    room = room - 1
    intolP1, intolP2, intolP3 = intolNorm()
    OddsP1 = fullPredict(p1allTime, t)
    roomOddsP1 = OddsP1[room]
    OddsP2 = fullPredict(p2allTime, t)
    roomOddsP2 = OddsP2[room]
    OddsP3 = fullPredict(p3allTime, t)
    roomOddsP3 = OddsP3[room]
    try:
        normOddsP1 = roomOddsP1/sum([roomOddsP1, roomOddsP2, roomOddsP3])
    except:
        pass
    try:
        normOddsP2 = roomOddsP2/sum([roomOddsP1, roomOddsP2, roomOddsP3])
    except:
        pass
    try:
        normOddsP3 = roomOddsP3/sum([roomOddsP1, roomOddsP2, roomOddsP3])
    except:
        pass
    totalOdds = sum([normOddsP1, normOddsP2, normOddsP3])
    if totalOdds < powerThreshold:
        power = False

    return(power)

#Determine the temp of a room based on the odds of each individual being in the room and the pickiness of that individual

def changeTemp(room, currentTemp, t):
    power = True
    normOddsP1 = 0
    normOddsP2 = 0
    normOddsP3 = 0
    room = room - 1
    intolP1, intolP2, intolP3 = intolNorm()
    OddsP1 = fullPredict(p1allTime, t)
    roomOddsP1 = OddsP1[room]

    OddsP2 = fullPredict(p2allTime, t)
    roomOddsP2 = OddsP2[room]

    OddsP3 = fullPredict(p3allTime, t)
    roomOddsP3 = OddsP3[room]

    try:
        normOddsP1 = roomOddsP1/sum([roomOddsP1, roomOddsP2, roomOddsP3])
    except:
        pass
    try:
        normOddsP2 = roomOddsP2/sum([roomOddsP1, roomOddsP2, roomOddsP3])
    except:
        pass
    try:
        normOddsP3 = roomOddsP3/sum([roomOddsP1, roomOddsP2, roomOddsP3])
    except:
        pass
    totalOdds = sum([normOddsP1, normOddsP2, normOddsP3])
    if totalOdds < powerThreshold:
        power = False
    p1Weight = normOddsP1 * (p1Pref - currentTemp) * intolP1
    p2Weight = normOddsP2 * (p2Pref - currentTemp) * intolP2
    p3Weight = normOddsP3 * (p3Pref - currentTemp) * intolP3

    return((p1Weight+p2Weight+p3Weight))  # /peopleNum /(roomOddsP1+roomOddsP2+roomOddsP3)

#Adjust the temperature based on tempPower


initR1 = changeTemp(1, initTemp, 0)
initR2 = changeTemp(2, initTemp, 0)
initR3 = changeTemp(3, initTemp, 0)
initR4 = changeTemp(4, initTemp, 0)
j = timeStepNum
timeRecord = []

tempRecord = []
stepCounter = 0
stepCounter2 = 0

tempChangeTotalr1 = 0
tempChangeTotalr2 = 0
tempChangeTotalr3 = 0
tempChangeTotalr4 = 0
fixedTemp = 0
totTempLoss = []
weatherRecord = []
constTemp = []

#Set empty variables for loop

# def intolError():

while timeStepNum > 0:
    if stepCounter2 > 23:
        stepCounter2 = stepCounter2 - 23
    if directSun == True:
        day = True
    else:
        day = False
    if stepCounter2 > 8 and stepCounter2 < 20:
        day = False
    if timeStepNum == j:
        prevTempR1 = initTemp
        prevTempR2 = initTemp
        prevTempR3 = initTemp
        prevTempR4 = initTemp
    else:
        pass
    minute = 0
    while minute < 60:
        r1Temp = (1/10)*changeTemp(1, prevTempR1, (stepCounter2)) - (.0115*(prevTempR2-prevTempR1) + .0118*(prevTempR3 -
                                                                                                            prevTempR1) + .02*(ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-8)+(minute/60))) - prevTempR1))
        r2Temp = (1/10)*changeTemp(2, prevTempR2, (stepCounter2)) - (.0115*(prevTempR1-prevTempR2) + .0118*(prevTempR4 -
                                                                                                            prevTempR2) + .0192*(ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-8)+(minute/60))) - prevTempR2))
        r3Temp = (1/10)*changeTemp(3, prevTempR3, (stepCounter2)) - (.0118*(prevTempR1-prevTempR3) + .0118*(prevTempR4 -
                                                                                                            prevTempR3) + .0192*(ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-8)+(minute/60))) - prevTempR3))
        r4Temp = (1/10)*changeTemp(4, prevTempR4, (stepCounter2)) - (.0118*(prevTempR3-prevTempR4) + .0118*(prevTempR2 -
                                                                                                            prevTempR4) + .02*(ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-8)+(minute/60))) - prevTempR4))
        sub = 0
        if day == True:
            r1Temp = r1Temp + .0216
            r2Temp = r2Temp + .0216
            r3Temp = r3Temp + .0216
            r4Temp = r4Temp + .0216
            sub = .0216

        powerR1 = tempPower(1, prevTempR1, (stepCounter2))
        if powerR1 == False:
            r1Temp = 0
        powerR2 = tempPower(2, prevTempR2, (stepCounter2))
        if powerR2 == False:
            r2Temp = 0
        powerR3 = tempPower(3, prevTempR3, (stepCounter2))
        if powerR3 == False:
            r3Temp = 0
        powerR4 = tempPower(4, prevTempR4, (stepCounter2))
        if powerR4 == False:
            r4Temp = 0
        tempChangeTotalr1 = tempChangeTotalr1 + numpy.absolute(r1Temp)
        tempChangeTotalr2 = tempChangeTotalr2 + numpy.absolute(r2Temp)
        tempChangeTotalr3 = tempChangeTotalr3 + numpy.absolute(r3Temp)
        tempChangeTotalr4 = tempChangeTotalr4 + numpy.absolute(r4Temp)
        prevTempR1 = r1Temp * (1) + prevTempR1 + ((.0115*(prevTempR2-prevTempR1) + .0118*(prevTempR3-prevTempR1) + .02*(
            ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-8)+(minute/60))) - prevTempR1))) - sub
        prevTempR2 = r2Temp * (1) + prevTempR2 + ((.0115*(prevTempR1-prevTempR2) + .0118*(prevTempR4-prevTempR2) + .0192*(
            ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-8)+(minute/60))) - prevTempR2))) - sub
        prevTempR3 = r3Temp * (1) + prevTempR3 + ((.0118*(prevTempR1-prevTempR3) + .0118*(prevTempR4-prevTempR3) + .0192*(
            ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-8)+(minute/60))) - prevTempR3))) - sub
        prevTempR4 = r4Temp * (1) + prevTempR4 + ((.0118*(prevTempR3-prevTempR4) + .0118*(prevTempR2-prevTempR4) + .02*(
            ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-8)+(minute/60))) - prevTempR4))) - sub
        timeNow = round(stepCounter + (minute/60), 3)
        timeRecord.append(timeNow)
        tempRecord.append([prevTempR1, prevTempR2, prevTempR3, prevTempR4])
        weatherRecord.append(
            float(.0181*(ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-9)+(minute/60))))))
        # print(len(weatherRecord))
        #print(float(.0181*(ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter-9)+(minute/60))))))
        constTemp.append(75)
        totTempLoss.append(numpy.absolute((.0115*(prevTempR3-prevTempR4) + .0115*(prevTempR2-prevTempR4) + .0181 *
                                           (ambTemp + amp*math.sin((3.1415*2/period)*((stepCounter2-9)+(minute/60))) - prevTempR4))))
        minute = minute + 1

    timeStepNum = timeStepNum - 1
    stepCounter = stepCounter + 1
    stepCounter2 = stepCounter2 + 1

#Initiate time step sequence to model the temperature change over time.
#This step accounts for seasonal temperature change, as well as heat loss from
#solar radiation, conduction of heat through walls, and a sinusoidal graph of
#the ambient temperature of the outside of the house.
    
# Loss for R1 per min = (.0115*(TR2- TR1) + .0115*(TR3- TR1) + .0181*(Ambient - TR1))
# Loss for R2 ^= (.0115*(TR1- TR2) + .0115*(TR4- TR2) + .0181*(Ambient - TR2))
# Loss for R3 ^= (.0115*(TR1- TR3) + .0115*(TR4- TR3) + .0181*(Ambient - TR3))
# Loss for R4 ^= (.0115*(TR3- TR4) + .0115*(TR2- TR4) + .0181*(Ambient - TR4))


#print(changeTemp(4, 74, 19))

r1Temps = [item[0] for item in tempRecord]
r2Temps = [item[1] for item in tempRecord]
r3Temps = [item[2] for item in tempRecord]
r4Temps = [item[3] for item in tempRecord]

#count the total temperature change over time

print((2250/12103) *
      (sum([tempChangeTotalr1, tempChangeTotalr2, tempChangeTotalr3, tempChangeTotalr4])))
print('multi therm^')
print((2250/12103) * (tempChangeTotalr4*4))
print('single therm^')
# 1 cent to heat 12,103 1 deg

#calculate the cost based on the total temp change


# plt.plot(timeRecord, weatherRecord)
# plt.show()
plt.plot(timeRecord, r1Temps)
plt.title('r1temps')
plt.show()
plt.plot(timeRecord, r2Temps)
plt.title('r2temps')
plt.show()
plt.plot(timeRecord, r3Temps)
plt.title('r3temps')
plt.show()
plt.plot(timeRecord, r4Temps)
plt.title('r4temps')
plt.show()

#graph the temperature over time
