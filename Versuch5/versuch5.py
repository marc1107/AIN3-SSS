import math

import matplotlib.pyplot as plt
import pandas as pd
import csv
import numpy as np

df = pd.read_excel('daten.xlsx', header=None)
n = df.to_numpy()

voltage_ad = []
keithley_ad = []
multi_ad = []
wandler_ad = []
pico_ad = []

voltage_da = []
keithley_da = []
multi_da = []
pico_da = []

for i in range(1, len(n)):
    if i < len(n) - 1:
        voltage_ad.append(n[i][0])
        keithley_ad.append(n[i][1])
        multi_ad.append(n[i][2])
        wandler_ad.append(n[i][3])
        pico_ad.append(n[i][4])
    voltage_da.append(n[i][6])
    keithley_da.append(n[i][7])
    multi_da.append(n[i][8])
    pico_da.append(n[i][9])


def main():
    # Aufgabe 2 Messfehler berechnen AD-Wandlung
    messfehler_multi = get_messfehler(keithley_ad, multi_ad)
    messfehler_wandler = get_messfehler(keithley_ad, wandler_ad)
    std_multi = get_standardabweichung(messfehler_multi)
    std_wandler = get_standardabweichung(messfehler_wandler)

    print("AD-Wandlung")
    print("Theoretischer Quantisierungsfehler: " + str(theoretischer_quantisierungsfehler(-10, 10, 11)))
    print("Standardabweichung Multimeter Voltcraft: " + str(std_multi))
    print("Standardabweichung AD-Wandler: " + str(std_wandler) + "\n")

    # Aufgabe 3 Messfehler berechnen DA-Wandlung
    messfehler_multi = get_messfehler(keithley_da, multi_da)
    messfehler_pico = get_messfehler(keithley_da, pico_da)
    std_multi = get_standardabweichung(messfehler_multi)
    std_pico = get_standardabweichung(messfehler_pico)

    print("DA-Wandlung")
    print("Theoretischer Quantisierungsfehler: " + str(theoretischer_quantisierungsfehler(0, 5, 10)))
    print("Standardabweichung Multimeter Voltcraft: " + str(std_multi))
    print("Standardabweichung PicoScope: " + str(std_pico) + "\n")

    plot_sin()

    for i in range(2, 9):
        if i < 5:
            plot_kurve("plt" + str(i) + "000", 50)
        elif i < 8:
            plot_kurve("plt" + str(i) + "000", 100)
        else:
            plot_kurve("plt" + str(i) + "000", 1000)


def theoretischer_quantisierungsfehler(u_min, u_max, bit):
    return (u_max - u_min) / 2**bit


# Arrays übergeben, gibt Array mit den Messfehlern zurück
def get_messfehler(ref, arr):
    messfehler = []
    for i in range(0, len(ref)):
        messfehler.append(ref[i] - arr[i])

    return messfehler


def get_standardabweichung(messfehler):
    sum = 0.0
    for m in messfehler:
        sum += m**2

    return math.sqrt((1.0 / (len(messfehler) - 1.0)) * sum)


def plot_sin():
    values_x = []
    values_y = []
    with open('sinus_pico.csv', newline='') as csvfile:
        messung = list(csv.reader(csvfile, delimiter=';'))

        for i in range(3, len(messung)):
            values_x.append(float(messung[i][0].replace(",", ".")))
            values_y.append(float(messung[i][1].replace(",", ".")))

    plt.title("Sinus")
    plt.xlabel("ms")
    plt.ylabel("Volt")
    plt.plot(values_x, values_y)
    plt.savefig("Sinusschwingung.png", dpi=900)
    plt.show()


def plot_kurve(name, samples):
    arr = np.load('PltData/' + name + '.npy')

    plt.title(name)
    plt.xlabel("Samples")
    plt.ylabel("Spannung (V)")
    plt.plot(arr[:samples])
    plt.savefig(name + ".png", dpi=900)
    plt.show()


main()
