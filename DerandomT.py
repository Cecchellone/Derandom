import math
import csv
import random
import os

random.seed()

def GetPercent(dice, peak, caos=0):
    bas = caos/len(dice)
    reverse = [peak-x for x in dice]
    tot = sum(reverse)
    percent = [(x*(1-bas) + bas*tot)/tot for x in reverse]
    return percent

def UpdateDice(dice, Pval, peak):
    if dice[Pval] >= peak:
        return dice
    
    tempD = dice
    tempD[Pval] += 1

    less = min(tempD)
    newdice = [x-less for x in tempD]
    return newdice

def RandomScan(dice, Rval, peak, caos=0):
    Lval = 0
    Hval = 0

    cake = GetPercent(dice, peak, caos)

    for x in range(len(dice)):
        Lval = Hval
        Hval += cake[x]
        if Lval <= Rval < Hval:
            return x, Rval < (Lval + caos/len(dice))
    return

def colorgen(color = None):
    if color == None:
        return '\033[0;37;40m'
    Colors = ["34", "36", "32", "33", "31", "35"]
    Colors = ["\033[1;"+ x +";40m" for x in Colors]
    return Colors[(color)%len(Colors)]

def printpercent(percent, multiplier):
    for x in range(len(percent)):
        print (colorgen(x+1) ,x+1, ' ', u"\u2587" * math.ceil(percent[x]*multiplier), '\t', round(percent[x]*100, 2), '\033[0;37;40m', sep='')
    return

def printdice(dice):
    for x in range(len(dice)):
        print (x+1, u"\u2587" * dice[x], '\t', dice[x])

#user
DICE_SIZE = 8
PEAK = 5
CAOS = 4 /100
playernum = 4

#start
Output = []
dice = [0 for x in range(DICE_SIZE)]
History = []
Play = True
i = 0

while Play:
    i+=1

    print("\nROUND", math.floor((i/playernum)+1), "\tPlayer", i%playernum+1, '\n')

    Rval = random.random()
    #print(Rval)

    Pond, Lucky = RandomScan(dice, Rval, PEAK, CAOS)
    
    if Lucky:
        print("\033[1;37;40m", Pond+1, "\t\033[1;30;47mLUCKY!!!\033[0;37;40m", sep='')
    else:
        print("\033[1;37;40m", Pond+1, "\033[0;37;40m", sep='')

    History.append(Pond)

    dice = UpdateDice(dice, Pond, PEAK)

    percent = GetPercent(dice, PEAK, CAOS)

    #print('')
    #printdice(dice)
    print('')
    printpercent(percent, 100)

    Play = input("premi Invio per proseguire ") != "exit"

print("Salvataggio storico in corso")

with open("DerandomT.csv","w+") as csv_out:
    csv_write = csv.writer(csv_out, delimiter=',')
    csv_write.writerow(History)

print("Salvataggio effettutato\nChiusura completata")
