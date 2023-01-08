import csv
import math

import matplotlib.pyplot as plt
import numpy as np
import scipy

muha_signal_ms = []
muha_signal_mV = []

with open("./first_tone.csv") as csvfile:
    messung = list(csv.reader(csvfile, delimiter=';'))

    for i in range(3, len(messung)):
        row = messung[i]
        row[0] = float(row[0].replace(",", "."))
        row[1] = float(row[1].replace(",", "."))
        if -20 > row[0] > -25:
            muha_signal_ms.append(row[0])
            muha_signal_mV.append(row[1])

# plt.plot(muha_signal_ms, muha_signal_mV)
# plt.grid()
# plt.show()

fourier = np.fft.fft(muha_signal_mV)

plt.title('Fouriertransform')
plt.ylabel('Amplitude')
plt.xlabel('Frequenz(kHz)')
plt.grid(True)

f = []
for index in range(0, len(fourier), 1):
    f.append(index / (len(fourier) * 0.000_005) / 1000)
f = np.array(f)

plt.xlim(0, len(fourier) / 1000)
# plt.ylim(0, 25_000)
plt.xticks(np.arange(0, 10, 0.7))

plt.plot(f[:len(f) // 2], np.abs(fourier[:len(fourier) // 2]))
plt.savefig('Transformed.png', dpi=900)
plt.show()

# -------------------------------
# Teil 2
# -------------------------------

# Frequenz, Amplitude in mV, Phasenverschiebung in ms
bigSpeaker = np.array([[100, 96.53, 5.451, 1.5], [200, 118.3, 4.988, 1.5], [300, 61.61, 0.281, 1.5], [400, 46.59, 0.376, 1.497],
                       [500, 37.32, 0.321, 1.494], [700, 30.61, 0.233, 1.5], [850, 29.75, 0.219, 1.523], [1000, 28.88, 0.185, 1.535],
                       [1200, 28.1, 0.192, 1.524], [1500, 26.89, 0.177, 1.5], [1700, 28.19, 0.162, 1.52], [2000, 26.8, 0.158, 1.5],
                       [3000, 19.92, 1.40, 1.5], [4000, 40.79, 0.143, 1.501], [5000, 27.84, 0.151, 1.503], [6000, 25.67, 0.131, 1.5],
                       [10000, 22.43, 0.048, 1.496]])

smallSpeaker = np.array([[100, 10.91, 4.007, 1.5], [200, 24.94, 3.163, 1.5], [300, 39.75, 2.34, 1.5], [400, 93.24, 1.986, 1.5],
                         [500, 126.4, 0.088, 1.5], [700, 57.54, 0.213, 1.5], [850, 45.42, 0.242, 1.5], [1000, 37.02, 0.223, 1.5],
                         [1200, 28.02, 0.199, 1.493], [1500, 36.85, 0.174, 1.5], [1700, 32.91, 0.174, 1.5], [2000, 33.6, 0.168, 1.5],
                         [3000, 27.97, 0.153, 1.5], [4000, 14.24, 0.132, 1.5], [5000, 33.34, 0.162, 1.5], [6000, 14.24, 0.114, 1.501],
                         [10000, 16.45, 0.046, 1.5]])


def plotBodeDiagramm(speaker, plotTitle, fileName):
    freq = speaker[:, :1]  # * 2 * np.pi
    phase = (speaker[:, 2:3] / -1000) * speaker[:, :1] * 360
    amp = speaker[:, 1:2] / 1000
    ampin = speaker[:, 3:4]
    # Amplitudengang berechnen
    ampdiv = amp / ampin

    plt.figure()
    plt.subplot(211)
    plt.title('Bode Diagram ' + plotTitle)
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude (dB)')
    plt.semilogx(freq, 20 * np.log10(abs(ampdiv)))
    # plt.xlim(speaker[0,0] * 2 * np.pi, speaker[16,0] * 2 * np.pi)
    plt.xlim(speaker[0, 0], speaker[16, 0])
    plt.grid()

    plt.subplot(212)
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Phasenwinkel')
    plt.semilogx(freq, phase)
    # plt.xlim(speaker[0,0] * 2 * np.pi, speaker[16,0] * 2 * np.pi)
    plt.xlim(speaker[0, 0], speaker[16, 0])
    plt.grid()

    plt.show
    plt.savefig('BodeDiagramm' + fileName + '.png', dpi=900)


def plotReadings(speaker, plotTitle, fileName):
    freq = speaker[:, :1]
    phase = speaker[:, 2:3]
    amp = speaker[:, 1:2]

    plt.figure()
    plt.subplot(211)
    plt.title('Messungen ' + plotTitle)
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Amplitude (mV)')
    plt.plot(freq, amp)
    plt.xlim(speaker[0, 0], speaker[16, 0])
    plt.grid()

    plt.subplot(212)
    plt.xlabel('Frequenz (Hz)')
    plt.ylabel('Phase (ms)')
    plt.plot(freq, phase)
    plt.xlim(speaker[0, 0], speaker[16, 0])
    plt.grid()

    plt.show
    plt.savefig('Messungen' + fileName + '.png', dpi=900)


plotBodeDiagramm(bigSpeaker, "Big Speaker", "BigSpeaker")
plotBodeDiagramm(smallSpeaker, "Small Speaker", "SmallSpeaker")
plotReadings(bigSpeaker, "Big Speaker", "BigSpeaker")
plotReadings(smallSpeaker, "Small Speaker", "SmallSpeaker")
