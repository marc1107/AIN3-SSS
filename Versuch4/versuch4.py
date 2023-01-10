import numpy as np
from scipy import signal, stats
import matplotlib.pyplot as plt
import math
import cmath

sampleFreq = 20000 - 32  # -32 weil muss durch 256 teilbar sein


def main():
    # Teil 1 c)
    data = np.load("Recordings/Hoch1.npy")
    data = data[:100000]
    plt.title("Signal Hoch")
    plt.xlabel("Samples")
    plt.ylabel("Amplitude")
    plt.plot(data)
    plt.savefig("Hoch_Signal.png", dpi=900)
    plt.show()
    # plotAndSave(fourierAufg3("Recordings/Hoch1.npy"), data, "Hoch1_Sample")

    # Teil 1 b)
    data = np.load("Recordings/Hoch1.npy")[:sampleFreq]
    # plotAndSave(getSpectrum("Recordings/Hoch1.npy"), data, "Hoch1")

    # Teil 2 a)
    refHoch = getAndPrintReferenzspektrum("Hoch")
    refTief = getAndPrintReferenzspektrum("Tief")
    refRechts = getAndPrintReferenzspektrum("Rechts")
    refLinks = getAndPrintReferenzspektrum("Links")

    # Teil 2 c) + d)
    spracherkenner(refHoch, refTief, refLinks, refRechts)


def fourierAufg3(file):
    data = np.load(file)
    data = data[:100000]

    return np.fft.fft(data) * 0.00001


def getSpectrum(file):
    data = np.load(file)[:sampleFreq]

    window = np.array(list(getWindows(data, 512)))

    return np.fft.fft(window).mean(0)


def getWindows(arr, window_size):
    ret = []
    gauss_window = np.array(signal.gaussian(512, 512 / 4))

    for i in range(0, len(arr) - window_size + 1, math.floor(window_size / 2)):  # /2 weil zur Hälfte überlappen
        ret.append(np.concatenate(
            [[0] * i, list(gauss_window * (arr[i:i + window_size])), [0] * (len(arr) - (i + window_size))]))

    return ret


def plotAndSave(fourier, data, filename):
    print(len(fourier))

    f = []
    for index in range(0, len(data), 1):
        f.append(index / (len(data) * 0.00001))
    f = np.array(f)

    plt.title('Fouriertransformierte')
    plt.ylabel('Amplitude')
    plt.xlabel('Frequenz (Hz)')
    plt.grid(True)
    plt.xlim(0, 2000)
    plt.gcf().subplots_adjust(left=0.15)
    plt.plot(f[:len(f) // 2], np.abs(fourier[:len(fourier) // 2]))
    plt.savefig("PNG/" + filename + ".png", dpi=900)
    plt.show()


def getAndPrintReferenzspektrum(name):
    spektrum = getSpectrum("Recordings/" + name + "1.npy")
    spektrum += getSpectrum("Recordings/" + name + "2.npy")
    spektrum += getSpectrum("Recordings/" + name + "3.npy")
    spektrum += getSpectrum("Recordings/" + name + "4.npy")
    spektrum += getSpectrum("Recordings/" + name + "5.npy")

    spektrum = spektrum / 5

    # f = []
    # for index in range(0, len(spektrum), 1):
    #     f.append(index)
    # f = np.array(f)
    #
    # plt.title('Referenz ' + name)
    # plt.ylabel('Amplitude')
    # plt.xlabel('Frequenz (Hz)')
    # plt.grid(True)
    # plt.xlim(0, 1500)
    # plt.gcf().subplots_adjust(left=0.15)
    # plt.plot(f[:len(f) // 2], np.abs(spektrum[:len(spektrum) // 2])) # in getSpektrum() einbauen
    # plt.savefig("PNG/" + name + "_ref.png", dpi=900)
    # plt.show()

    return spektrum


# def bravais_pearson(x, y):
#     # Berechne den Mittelwert der Werte in x und y
#     x_mean = np.mean(x)
#     y_mean = np.mean(y)
#
#     # Berechnen Sie den Zähler der Bravais-Pearson-Formel
#     # Summenfunktion für jeden x- und jeden y-Wert in den Eingangsspektren
#     numerator = np.sum((x - x_mean) * (y - y_mean))
#
#     # Berechnen Sie den Nenner der Bravais-Pearson-Formel
#     # siehe formula_bravais_pearson.png
#     denominator = np.sqrt(np.sum((x - x_mean)**2) * np.sum((y - y_mean)**2))
#
#     # Berechne und returne den Korrelationskoeffizienten
#     return numerator / denominator


commands = ["Hoch", "Tief", "Links", "Rechts"]


def spracherkenner(refHoch, refTief, refLinks, refRechts):
    names = []
    refHoch = np.abs(refHoch)
    refTief = np.abs(refTief)
    refLinks = np.abs(refLinks)
    refRechts = np.abs(refRechts)

    for c in commands:
        for n in range(1, 6):
            names.append(c + str(n))

    treffer = [0, 0, 0, 0]

    for n in names:
        spec = np.load("Recordings/P" + n + ".npy")[:19968]
        spec = np.abs(np.fft.fft(spec))

        maximum = [stats.pearsonr(spec, refHoch)[0], stats.pearsonr(spec, refTief)[0],
                   stats.pearsonr(spec, refLinks)[0], stats.pearsonr(spec, refRechts)[0]]

        if np.max(maximum) == maximum[0]:
            print(n + " Phil: hoch")
            if n[0:4] == commands[0]:
                treffer[0] += 1
        elif np.max(maximum) == maximum[1]:
            print(n + " Phil: tief")
            if n[0:4] == commands[1]:
                treffer[1] += 1
        elif np.max(maximum) == maximum[2]:
            print(n + " Phil: Links")
            if n[0:5] == commands[2]:
                treffer[2] += 1
        elif np.max(maximum) == maximum[3]:
            print(n + " Phil: Rechts")
            if n[0:6] == commands[3]:
                treffer[3] += 1

    printHitrate(treffer, 'Phil')

    treffer = [0, 0, 0, 0]

    for n in names:
        spec = np.load("Recordings/M" + n + ".npy")[:19968]
        spec = np.abs(np.fft.fft(spec))

        maximum = [stats.pearsonr(spec, refHoch)[0], stats.pearsonr(spec, refTief)[0],
                   stats.pearsonr(spec, refLinks)[0], stats.pearsonr(spec, refRechts)[0]]

        if np.max(maximum) == maximum[0]:
            print(n + " Marc: hoch")
            if n[0:4] == 'Hoch':
                treffer[0] += 1
        elif np.max(maximum) == maximum[1]:
            print(n + " Marc: tief")
            if n[0:4] == 'Tief':
                treffer[1] += 1
        elif np.max(maximum) == maximum[2]:
            print(n + " Marc: Links")
            if n[0:5] == 'Links':
                treffer[2] += 1
        elif np.max(maximum) == maximum[3]:
            print(n + " Marc: Rechts")
            if n[0:6] == 'Rechts':
                treffer[3] += 1

    printHitrate(treffer, 'Marc')


def printHitrate(treffer, name):
    print("Hitrate von " + name + " Hoch: " + str(float(treffer[0]) / float(5) * 100) + "%")
    print("Hitrate von " + name + " Tief: " + str(float(treffer[1]) / float(5) * 100) + "%")
    print("Hitrate von " + name + " Links: " + str(float(treffer[2]) / float(5) * 100) + "%")
    print("Hitrate von " + name + " Rechts: " + str(float(treffer[3]) / float(5) * 100) + "%")


main()
