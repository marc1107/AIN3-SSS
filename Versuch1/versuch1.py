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
voltavg = []
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
        voltavg.append(avg)
        stdarr.append(np.std(values, ddof=1))

    i = i + steps

# Lineare Kennlinie
cm_log = []
volt_log = []

for i in range(len(cm)):
    cm_log.append(np.log(cm[i]))
    volt_log.append(np.log(voltavg[i]))

# nichtlineare Kennlinie
a = -1.68
b = 2.87
y = []
for x in voltavg:
    y.append(pow(math.e, b) * pow(x, a))

# plot Daten und nichtlineare Kennlinie
fig, ax = plt.subplots()
ax.plot(voltavg, cm, label='Daten')
ax.plot(voltavg, y, label='nichtlineare Kennlinie')
ax.set_xlabel("Spannung (V)")
ax.set_ylabel("Distanz (cm)")
ax.legend(facecolor='white')
plt.savefig('auswertung.png', dpi=227)
plt.show()


# plot lineare Kennlinie und logged Daten
plotlinregress(volt_log, cm_log, "Spannung log (V)", "Distanz log (cm)")


# Berechnung Standardabweichung von a4_kurz und a4_lang
# kurz
cmA4Kurz = []
avgA4Kurz = 0.0
stdA4Kurz = 0.0
with open("./Protokoll1/a4_kurze.csv") as csvfile:
    messung = list(csv.reader(csvfile, delimiter=';'))

    values = []
    for j in range(1000, 1000 + rng):
        row = messung[j]
        valuestr = row[1].replace(",", ".")
        avgA4Kurz += float(valuestr)
        values.append(float(valuestr))

    # Durchschnitt berechnen
    avgA4Kurz = avgA4Kurz / rng
    cmA4Kurz.append(i)
    # Durchschnitt und Standardabweichung in zugehörige Arrays schreiben
    stdA4Kurz = np.std(values, ddof=1)

# lang
cmA4Lang = []
avgA4Lang = 0.0
stdA4Lang = 0.0
with open("./Protokoll1/a4_lange.csv") as csvfile:
    messung = list(csv.reader(csvfile, delimiter=';'))

    values = []
    for j in range(1000, 1000 + rng):
        row = messung[j]
        valuestr = row[1].replace(",", ".")
        avgA4Lang += float(valuestr)
        values.append(float(valuestr))

    # Durchschnitt berechnen
    avgA4Lang = avgA4Lang / rng
    cmA4Lang.append(i)
    # Durchschnitt und Standardabweichung in zugehörige Arrays schreiben
    stdA4Lang = np.std(values, ddof=1)

p95 = 1.98
p68 = 1

stdA4KurzRichtig = stdA4Kurz / math.sqrt(rng)
stdA4LangRichtig = stdA4Lang / math.sqrt(rng)

vertrA4Kurz95Max = p95 * stdA4KurzRichtig
vertrA4Kurz95Min = -p95 * stdA4KurzRichtig
vertrA4Kurz68Max = p68 * stdA4KurzRichtig
vertrA4Kurz68Min = -p68 * stdA4KurzRichtig

vertrA4Lang95Max = p95 * stdA4LangRichtig
vertrA4Lang95Min = -p95 * stdA4LangRichtig
vertrA4Lang68Max = p68 * stdA4LangRichtig
vertrA4Lang68Min = -p68 * stdA4LangRichtig

print("\n95% Vertrauensbereich A4 kurz: [" + str(vertrA4Kurz95Min) + ", " + str(vertrA4Kurz95Max) + "]")
print("68% Vertrauensbereich A4 kurz: [" + str(vertrA4Kurz68Min) + ", " + str(vertrA4Kurz68Max) + "]")
print("\n95% Vertrauensbereich A4 lang: [" + str(vertrA4Lang95Min) + ", " + str(vertrA4Lang95Max) + "]")
print("68% Vertrauensbereich A4 lang: [" + str(vertrA4Lang68Min) + ", " + str(vertrA4Lang68Max) + "]")

fehlerfortpflanzungKurz = (np.exp(b) * (a * np.power(avgA4Kurz, a-1))) * stdA4Kurz
fehlerfortpflanzungLang = (np.exp(b) * (a * np.power(avgA4Lang, a-1))) * stdA4Lang

kennlinieUmgedrehtKurz = np.exp(b) * np.power(avgA4Kurz, a)
kennlinieUmgedrehtLang = np.exp(b) * np.power(avgA4Lang, a)

print("\nFehler kurze Seite: " + str(kennlinieUmgedrehtKurz) + " cm +- " + str(np.abs(fehlerfortpflanzungKurz)) + " cm")
print("Fehler lange Seite: " + str(kennlinieUmgedrehtLang) + " cm +- " + str(np.abs(fehlerfortpflanzungLang)) + " cm")

# Fläche berechnen
flaeche = kennlinieUmgedrehtKurz * kennlinieUmgedrehtLang

# Fehlerfortpflanzung Fläche
fehlerfortpFlaeche = np.sqrt(
    np.power(fehlerfortpflanzungKurz * stdA4Lang, 2) + np.power(fehlerfortpflanzungLang * stdA4Kurz, 2))

print("\nFläche: " + str(flaeche) + " cm^2 +- " + str(fehlerfortpFlaeche) + " cm^2")
