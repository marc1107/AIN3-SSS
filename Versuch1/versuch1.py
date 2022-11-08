import csv
import matplotlib.pyplot as plt
import numpy as np

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


fig, ax = plt.subplots(2, 1)
#x = np.linspace(0, 8, 1000)

#ax[0, 0].plot(x, np.sin(x), 'g') #row=0, col=0
#ax[1, 0].plot(x, np.tan(x), 'k') #row=1, col=0

# Plotten
plt.subplot(1, 3, 1)
plt.plot(avgarr, cm)
plt.title("unlogged")
plt.xlabel("Spannung (V)")
plt.ylabel("Distanz (cm)")
# plt.savefig('Unlogged.png', dpi=227)
# plt.show()

# Lineare Kennlinie
cm_log = []
volt_log = []

for i in range(len(cm)):
    cm_log.append(np.log(cm[i]))
    volt_log.append(np.log(avgarr[i]))

# Plotten
plt.subplot(1, 3, 3)
plt.plot(volt_log, cm_log)
plt.title("logged")
plt.xlabel("Spannung log (V)")
plt.ylabel("Distanz log (cm)")

plt.savefig('auswertung.png', dpi=227)
# plt.savefig('logged.png', dpi=227)
plt.show()

#fig.show()
