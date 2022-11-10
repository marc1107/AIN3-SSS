import csv
import math

import matplotlib.pyplot as plt
import numpy as np
import scipy


def linregress(arr1, arr2):
    # Convert to numpy array
    nparr1 = np.asarray(arr1)
    nparr2 = np.asarray(arr2)
    return scipy.stats.linregress(nparr1, nparr2)


def plotlinregress(narr1, narr2, lbl_x, lbl_y):
    # Convert to numpy array
    arr1 = np.asarray(narr1)
    arr2 = np.asarray(narr2)

    slope, intercept, r, p, stderr = linregress(arr1, arr2)
    line = f'lineare Regressionslinie: y={slope:.2f}x+{intercept:.2f}'

    # Punkte von Array und Reggressionslinie mit Legende plotten:
    fig, ax = plt.subplots()
    ax.plot(arr1, arr2, label='logarithmierte Daten')
    ax.plot(arr1, intercept + slope * arr1, label=line)
    ax.set_xlabel(lbl_x)
    ax.set_ylabel(lbl_y)
    ax.legend(facecolor='white')
    plt.savefig('lineareAuswertung.png', dpi=227)
    plt.show()


start = 10
steps = 3
end = 70
rng = 100

cm = []
avgarr = []
stdarr = []

i = start
while i <= end:
    file = "./Protokoll1/" + str(i) + ".csv"
    print("Reading file: " + file)
    with open(file) as csvfile:
        messung = list(csv.reader(csvfile, delimiter=';'))

        if len(messung) < rng + 1000:
            break

        values = []
        avg = 0
        for j in range(1000, 1000 + rng):
            row = messung[j]
            valuestr = row[1].replace(",", ".")
            avg += float(valuestr)
            values.append(float(valuestr))

        # Durchschnitt berechnen
        avg = avg / rng
        cm.append(i)
        # Durchschnitt und Standardabweichung in zugehörige Arrays schreiben
        avgarr.append(avg)
        stdarr.append(np.std(values, ddof=1))

    i = i + steps

# Lineare Kennlinie
cm_log = []
volt_log = []

for i in range(len(cm)):
    cm_log.append(np.log(cm[i]))
    volt_log.append(np.log(avgarr[i]))

# nichtlineare Kennlinie
y = []
for x in avgarr:
    y.append(pow(math.e, 2.87) * pow(x, -1.68))

# plot Daten und nichtlineare Kennlinie
fig, ax = plt.subplots()
ax.plot(avgarr, cm, label='Daten')
ax.plot(avgarr, y, label='nichtlineare Kennlinie')
ax.set_xlabel("Spannung (V)")
ax.set_ylabel("Distanz (cm)")
ax.legend(facecolor='white')
plt.savefig('auswertung.png', dpi=227)
plt.show()


# plot lineare Kennlinie und logged Daten
plotlinregress(volt_log, cm_log, "Spannung log (V)", "Distanz log (cm)")
