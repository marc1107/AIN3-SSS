# -*- coding: utf-8 -*-
"""
Created on Mon Jan  9 14:12:15 2023

@author: ds-05
"""

import redlab as rl
import numpy as np
import time
import matplotlib.pyplot as plt


def plotMessreihe(messreihe, filename):
    plt.title("Messreihe " + filename)
    plt.xlabel("Zeit (ms)")
    plt.ylabel("Volt (V)")
    
    plt.plot(messreihe)
    plt.savefig('PNG/plt' + filename + '.png', dpi=900)
    plt.show()
    

sin = []

for i in range(30):
    sin.append(np.sin(2*np.pi / 30 * i) + 1)

while(True):
    print("Wert eingeben")
    wert = input()
    
    if wert == -1:
        break;
    
    print("------- einzelne Werte -------------------------")
    #print("16 Bit Value: " + str(rl.cbAIn(0,0,1)))
    print("Voltage Value: " + str(rl.cbVIn(0,0,1)))
    print("------- Messreihe -------------------------")
    print("Messreihe: " + str(rl.cbAInScan(0,0,0,300,8000,1)))
    print("Messreihe: " + str(rl.cbVInScan(0,0,0,300,8000,1)))
    messreihe = rl.cbVInScan(0,0,0,1000,8000,1)
    print("------- Ausgabe -------------------------")
    #print("Voltage Value: " + str(rl.cbVOut(0,0,101,2.5)))
    #print("Voltage Value: " + str(rl.cbVOut(0,0,101,wert)))
    
    plotMessreihe(messreihe, wert)
    
while(True):
    for i in sin:
        rl.cbVOut(0,0,101,i)
        time.sleep(0.01)
