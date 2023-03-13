import datetime
f = open("spy1min-allyears.txt", "r").read().split("\n")
# unixtime, open, high, low, close
del f[0]
while '' in f:
    f.remove('')
for i in range(len(f)):
    f[i] = f[i].split(',')
    del f[i][-3:]
    f[i][0] = f[i][0][1:-1]
    for j in [1,2,3,4]:
        f[i][j] = float(f[i][j])

fCOPY = f.copy()
trailingStopR = 0 # Move Stop to Breakeven
activateTrailingStopAtR = 1 # Once 1R achieved

'''
for useTrailingStop in [ True, False ]:
    for orbSizeInMinutes in [3]):
        for SLPercent in [ 0.5, 0.7, 0.9, 1, 1.5, 2, 2.5 ]:
            for target in [ 1, 2, 3, 4, 5, 10, 20 ]:
'''
for outsideDayRequired in [True]:
    for useTrailingStop in [ False ]:
        for orbSizeInMinutes in [1,3,5,10,12,15]:
            for SLPercent in [ 1 ]:
                for target in [ 1, 2, 3, 4, 5, 10, 20 ]:
                    f = fCOPY.copy()

                    outcomes = []
                    reasons = []

                    #SLPercent = 1   # 1 = opposite end of candle, 0 = same as entry

                    for i in range(len(f)):
                        if f[i][0].endswith("09:30"):
                            
                            ''' Filter out INSIDE DAYS if required'''
                            if outsideDayRequired:                              # If outside day is required
                                prevdayhigh = 0
                                prevdaylow = 99999                              # Then we'll see if it is.
                                for q in range( i+1, i+391 ):
                                    try:
                                        if f[q][2] > prevdayhigh:
                                            prevdayhigh = f[q][2]
                                        if f[q][3] < prevdaylow:
                                            prevdaylow = f[q][3]
                                    except:
                                        break
                                if f[i][1] < prevdayhigh and f[i][1] > prevdaylow:   # and if it's an inside day
                                    continue                                     # Then skip that day and find next day

                            orblows = []
                            orbhighs = []
                            for x in range( orbSizeInMinutes ):
                                orblows.append(f[i-x][3])
                                orbhighs.append(f[i-x][2])
                            
                            barheight = max(orbhighs)-min(orblows)
                            risk = barheight*SLPercent
                            
                            n = orbSizeInMinutes
                            stillGoing = True
                            lockInProfits = False

                            while stillGoing:
                                
                                if f[i-n][3] < min(orblows):
                                    sl = min(orblows)+risk
                                    tsl = 999999  # Arbitrarily high Trailing Stop Loss to start
                                    x = orbSizeInMinutes+1
                                    while True:
                                        if f[i-x][0].endswith("09:30"):
                                            reward = min(orblows)-f[i-x+5][4]
                                            stillGoing = False
                                            reasons.append("eod")
                                            break
                                        if f[i-x][2] > sl:
                                            reward = -1*risk
                                            stillGoing = False
                                            reasons.append("sl")
                                            break
                                        if min(orblows)-f[i-x][3] > target*barheight:
                                            reward = target*barheight
                                            stillGoing = False
                                            reasons.append("targ")
                                            break
                                        if useTrailingStop:
                                            if min(orblows)-f[i-x][4] > risk:
                                                tsl = min(orblows)
                                            if f[i-x][2] > tsl:
                                                reward = 0
                                                stillGoing = False
                                                reasons.append("tsl")
                                                break
                                        x += 1
                                elif f[i-n][2] > max(orbhighs):
                                    sl = max(orbhighs)-risk
                                    x = orbSizeInMinutes+1
                                    tsl = 0 # Arbitrarily low Trailing Stop Loss to start
                                    while True:
                                        if f[i-x][0].endswith("09:30"):
                                            reward = f[i-x+5][4]-max(orbhighs)
                                            stillGoing = False
                                            reasons.append("eod")
                                            break
                                        if f[i-x][3] < sl:
                                            reward = -1*risk
                                            stillGoing = False
                                            reasons.append("sl")
                                            break
                                        if f[i-x][3]-max(orbhighs) > target*barheight:
                                            reward = target*barheight
                                            stillGoing = False
                                            reasons.append("targ")
                                            break
                                        if useTrailingStop:
                                            if f[i-x][3]-max(orbhighs) > risk:
                                                tsl = max(orbhighs)
                                            if f[i-x][4] < tsl:
                                                reward = 0
                                                stillGoing = False
                                                reasons.append("tsl")
                                                break
                                        x += 1
                                else:
                                    n = n + 1
                            outcomes.append( reward )
                                
                    print("Outside" if outsideDayRequired else "Inside", orbSizeInMinutes, "minORB", target, SLPercent, useTrailingStop, reasons.count("targ"),reasons.count("eod"),reasons.count("sl"), reasons.count("tsl"), len(outcomes), sum(outcomes))
#for x in outcomes:
#    print(x)