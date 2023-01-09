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
    plotAndSave(fourierAufg3("Recordings/Hoch1.npy"), data, "Hoch1_Sample")

    # Teil 1 b)
    data = np.load("Recordings/Hoch1.npy")[:sampleFreq]
    plotAndSave(getSpectrum("Recordings/Hoch1.npy"), data, "Hoch1")

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
    gauss_window = np.array(signal.gaussian(512, 512/4))

    for i in range(0, len(arr) - window_size + 1, math.floor(window_size / 2)): # /2 weil zur Hälfte überlappen
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

    f = []
    for index in range(0, len(spektrum), 1):
        f.append(index)
    f = np.array(f)

    plt.title('Referenz ' + name)
    plt.ylabel('Amplitude')
    plt.xlabel('Frequenz (Hz)')
    plt.grid(True)
    plt.xlim(0, 1500)
    plt.gcf().subplots_adjust(left=0.15)
    plt.plot(f[:len(f) // 2], np.abs(spektrum[:len(spektrum) // 2])) # in getSpektrum() einbauen
    plt.savefig("PNG/" + name + "_ref.png", dpi=900)
    plt.show()

    return spektrum


def bravais_pearson(x, y):
    # Berechne den Mittelwert der Werte in x und y
    x_mean = np.mean(x)
    y_mean = np.mean(y)

    # Berechnen Sie den Zähler der Bravais-Pearson-Formel
    # Summenfunktion für jeden x- und jeden y-Wert in den Eingangsspektren
    numerator = np.sum((x - x_mean) * (y - y_mean))

    # Berechnen Sie den Nenner der Bravais-Pearson-Formel
    # siehe formula_bravais_pearson.png
    denominator = np.sqrt(np.sum((x - x_mean)**2) * np.sum((y - y_mean)**2))

    # Berechne und returne den Korrelationskoeffizienten
    return numerator / denominator



commands = ["Hoch", "Tief", "Links", "Rechts"]


def spracherkenner(refHoch, refTief, refLinks, refRechts):
    names = []
    for c in commands:
        for n in range(1, 6):
            names.append(c + str(n))

    for n in names:
        spec = np.load("Recordings/P" + n + ".npy")[:19968]
        spec = np.abs(np.fft.fft(spec))

        maximum = []

        # arr = [5-1j, 4+2j, 6+3j, 7-4j, 6-5j]
        # arr = 5-1j
        #
        # for i in range(0, len(arr)):
        #     arr[i] = cmath.polar(arr[i])
        #arr = np.stack([np.real(arr), np.imag(arr)], axis=-1)

        # refHochPassend = []
        #
        # for i in range (0, len(refHoch)):
        #     test = complex(refHoch[i].real, refHoch[i].imag)
        #     refHochPassend.append(cmath.polar(test))

        # maximum.append(np.corrcoef(arr, arr))
        # maximum.append(stats.pearsonr(arr, arr)[0])
        # maximum.append(stats.pearsonr(refHochPassend, refHochPassend)[0])
        # maximum.append(stats.pearsonr(np.real(refHoch), np.real(refHoch))[0])
        # maximum.append(stats.pearsonr(np.real(refTief), np.real(refTief))[0])
        # maximum.append(stats.pearsonr(np.real(refLinks), np.real(refLinks))[0])
        # maximum.append(stats.pearsonr(np.real(refRechts), np.real(refRechts))[0])

        # maximum.append(bravais_pearson(spec, refHoch))
        # maximum.append(stats.pearsonr(np.real(spec), np.real(refTief))[0])
        # maximum.append(stats.pearsonr(np.real(spec), np.real(refLinks))[0])
        # maximum.append(stats.pearsonr(np.real(spec), np.real(refRechts))[0])

        maximum.append(stats.pearsonr(spec, refHoch)[0])
        maximum.append(stats.pearsonr(spec, refTief)[0])
        maximum.append(stats.pearsonr(spec, refLinks)[0])
        maximum.append(stats.pearsonr(spec, refRechts)[0])

        # print("maximum: " + str(np.max(maximum)))
        # print("maximum0: " + str(maximum[0]))
        # print("maximum1: " + str(maximum[1]))
        # print("maximum2: " + str(maximum[2]))
        # print("maximum3: " + str(maximum[3]))
        if (np.max(maximum) == maximum[0]):
            print(n + " Phil: hoch")
        elif (np.max(maximum) == maximum[1]):
            print(n + " Phil: tief")
        elif (np.max(maximum) == maximum[2]):
            print(n + " Phil: links")
        elif (np.max(maximum) == maximum[3]):
            print(n + " Phil: rechts")


    for n in names:
        spec = np.load("Recordings/M" + n + ".npy")[:19968]
        spec = np.abs(np.fft.fft(spec))

        maximum = []

        maximum.append(stats.pearsonr(spec, refHoch)[0])
        maximum.append(stats.pearsonr(spec, refTief)[0])
        maximum.append(stats.pearsonr(spec, refLinks)[0])
        maximum.append(stats.pearsonr(spec, refRechts)[0])

        if (np.max(maximum) == maximum[0]):
            print(n + " Marc: hoch")
        elif (np.max(maximum) == maximum[1]):
            print(n + " Marc: tief")
        elif (np.max(maximum) == maximum[2]):
            print(n + " Marc: links")
        elif (np.max(maximum) == maximum[3]):
            print(n + " Marc: rechts")


#def pearson(arg1, arg2):



main()
