import math
import csv
import random
import os
from urllib.request import urlopen, Request

random.seed()


def RandOrg(qta=1):
    output = []
    if qta <= 1:
        qta = 1
    try:
        response = urlopen(Request("https://www.random.org/decimal-fractions/?num=" +
                                   str(qta) + "&dec=20&col=1&format=plain&rnd=new"))
        html = response.read()
        response.close
        output = [float(x) for x in html.split()]
    except:
        print("impossibile connettersi a Random.org")
        output = [random.random() for x in range(qta)]
    if qta == 1:
        return output[0]
    else:
        return output

def GetPercent(dice, peak, caos=0):
    bas = caos/len(dice)
    reverse = [peak-x for x in dice]
    tot = sum(reverse)
    percent = [(x*(1-bas) + bas*tot)/tot for x in reverse]
    return percent

def UpdateDice(dice, Pval, peak):
    if dice[Pval] >= peak:
        return dice
    
    tempD = list(dice) 
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

def printpercent(percent, multiplier=1, Cenable= True):
    for x in range(len(percent)):
        if Cenable:
            print (colorgen(x+1) ,x+1, ' ', u"\u2587" * math.ceil(percent[x]*multiplier), '\t', round(percent[x]*100, 2), '\033[0;37;40m', sep='')
        else:
            print (x+1, u"\u2584" * math.ceil(percent[x]*multiplier), '\t', round(percent[x]*100, 2))
    return

def printdice(dice, Cenable= True):
    for x in range(len(dice)):
        if Cenable:
            print (x+1, u"\u2587" * dice[x], '\t', dice[x])
        else:
            print (x+1, u"\u2584" * dice[x], '\t', dice[x])


#debug
ShowRval = False
ShowDice = False
ShowPercent = True
Cenable = False
Fenable = False
Pname = True

if input("Benvenuto in DerandomT.py ") == "debug":
    ShowRval = input(
        "Vuoi che venga mostrato il numero casuale generato? (y/n) ") == "y"
    ShowDice = input(
        "Vuoi che venga mostrato il grafico del dado? (y/n) ") == "y"
    ShowPercent = input(
        "Vuoi che venga mostrato il grafico della probabilità? (y/n) ") == "y"
    Cenable = input("Vuoi attivare i colori? (y/n) ") == "y"
    Fenable = input("Vuoi abilitare le forzature? (y/n) ") == "y"
    Penable = input("Vuoi specificare i nomi dei giocatori? (y/n) ") == "y"

#user input
DICE_SIZE = int(input("inserire numero di facce del dado: "))
if DICE_SIZE <= 2:
    DICE_SIZE = 2
playernum = int(input("inserire numero di giocatori: "))
if playernum <=2:
    playernum = 2

Players = ["Player "+ str(x+1) for x in range(playernum)]

if Pname:
    print("inserisci i nomi dei giocatori")
    for i in range(playernum):
        Players[i] = input(Players[i] + ": ")
RandomDotOrg = input("vuoi usare Random.org per generare i numeri? (y/n) ") != "n"

PEAK = 5
CAOS = 16/100
FORCED = 2

if input("vuoi usare le impostazioni di default? (y/n)\nPEAK:\t" + str(PEAK) + "\nCAOS:\t" + str(int(CAOS*100)) + "%\n" + ("FORCED:\t" + str(FORCED) + '\n')* int(Fenable)) == "n":
    PEAK = int(input("inserire numero di picco: "))
    CAOS = int(input("inserire percentuale di caos: ")) /100
    if Fenable:
        FORCED = int(input("inserire quantita forzature: (0=infinite) "))

    if PEAK <= 1:
        PEAK = 1
    if CAOS < 0 or CAOS > 100:
        CAOS =0
    if FORCED <= 0:
        if FORCED==0:
            FORCED = -1
        else:
            FORCED = 0

#start
Output = []
dice = [0 for x in range(DICE_SIZE)]
History = []
Play = True
i = 0



if ShowDice:
    print('')
    printdice(dice, Cenable)
if ShowPercent:
    print('')
    printpercent([1/DICE_SIZE for x in range(DICE_SIZE)], 1, Cenable)

input("\nè tutto pronto! premi Invio per iniziare")

while Play:
    print("\nROUND", math.floor((i/playernum)+1), '\t', Players[i%playernum], '\n')
    Rval = 0

    if RandomDotOrg:
        Rval = RandOrg()
    else:
        Rval = random.random()
    
    if ShowRval:
        print(Rval)

    Pond, Lucky = RandomScan(dice, Rval, PEAK, CAOS)
    
    if Cenable:
        if Lucky:
            print("\033[1;37;40m", Pond+1, "\t\033[1;30;47mLUCKY!!!\033[0;37;40m", sep='')
        else:
            print("\033[1;37;40m", Pond+1, "\033[0;37;40m", sep='')
    else:
        print (Pond+1, "\tLUCKY!!!"*int(Lucky))

    

    while True:
        Tdice = UpdateDice(dice, Pond, PEAK)

        if ShowDice:
            print('')
            printdice(Tdice, Cenable)
        if ShowPercent:
            print('')
            printpercent(GetPercent(Tdice, PEAK, CAOS), 100, Cenable)

        command = input("\npremi Invio per proseguire o digita 'exit' per interrompere la partita ")

        if Fenable and (FORCED>=1 or FORCED == -1) and command != "" and command.split()[0] == "forza":
            try:
                Forzato = int(command.split()[1])-1
                if 0<= Forzato< DICE_SIZE:
                    Pond = Forzato
                    print("il numero è stato forzato")
                    if FORCED !=-1:
                        FORCED -= 1
            except:
                print("operazione non effettuata")
        else:
            dice = Tdice
            History.append(Pond)
            Play = command != "exit"
            break
    
    i += 1
    

if input("la partita è conclusa!\nvuoi salvare lo storico su un file CSV? (y/n) ") == "y":
    filename = input("digita il nome del file senza estensione: ") + ".csv"
    print("Salvataggio storico in corso")

    with open(filename,"w+") as csv_out:
        csv_write = csv.writer(csv_out, delimiter=',')
        csv_write.writerow([x+1 for x in History])

    print("Salvataggio effettutato")
print("Partita conclusa!")


"""
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

builder = Gtk.builder().new_from_file("file/path")
"""

