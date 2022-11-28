import cv2
import numpy
import numpy as np

image = cv2.imread('./Bilder/Grauwertkeil.png')
grauwertkeil = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
grauwertkeil = grauwertkeil.astype(numpy.float32)

# Aufbau der beiden Arrays: alle ungeraden Werte sind Startwerte eines Bereichs,
# die geraden die zugehörigen Endwerte
topRow = []
bottomRow = []

# erste Startwerte für oberste und unterste Reihe speichern
topRow.append(5)
bottomRow.append(5)

# topRow füllen
i = 80
while i < len(grauwertkeil[0]):
    if i + 10 < len(grauwertkeil[0]):
        if int(grauwertkeil[0][i + 10]) - int(grauwertkeil[0][i]) >= 20:
            topRow.append(i)  # Endwert speichern
            i += 15
            topRow.append(i)  # neuen Startwert speichern
    i += 1
topRow.append(len(grauwertkeil[0]) - 5)

# bottomRow füllen
i = 0
while i < len(grauwertkeil[len(grauwertkeil) - 1]):
    if i + 10 < len(grauwertkeil[len(grauwertkeil) - 1]):
        if int(grauwertkeil[len(grauwertkeil) - 1][i + 10]) - int(grauwertkeil[len(grauwertkeil) - 1][i]) >= 20:
            bottomRow.append(i)  # Endwert speichern
            i += 15
            bottomRow.append(i)  # neuen Startwert speichern
    i += 1
bottomRow.append(len(grauwertkeil[len(grauwertkeil) - 1]) - 5)

xValues = []
for i in range(len(topRow)):
    if i % 2 == 0:
        xValues.append(topRow[i] if topRow[i] > bottomRow[i] else bottomRow[i])
    else:
        xValues.append(topRow[i] if topRow[i] < bottomRow[i] else bottomRow[i])

# print("TopRow:\n{}".format(topRow))
# print("BottomRow:\n{}".format(bottomRow))
# print("xValues:\n{}".format(xValues))

ROI_number = 0
yTop = 5
yBottom = len(grauwertkeil) - 5
subPicsMean = []
subPicsStd = []
i = 0
while i < len(xValues):
    ROI = grauwertkeil[yTop:yBottom, xValues[i]:xValues[i + 1]]
    subPicsMean.append(np.mean(ROI))
    subPicsStd.append(np.std(ROI, ddof=1))
    cv2.imwrite('SubPic_{}.png'.format(ROI_number), ROI)
    ROI_number += 1
    i += 2

print("Mittelwerte SubPics:\n{}".format(subPicsMean))
print("Standardabweichung SubPics:\n{}".format(subPicsStd))


def bildKontrastMaximiert(img, filename):
    imgCorrected = np.zeros(shape=(len(img), len(img[0])))
    min = np.min(img)
    max = np.max(img)
    for i in range(480):
        for j in range(640):
            imgCorrected[i][j] = img[i][j] - min
            if max > min:
                imgCorrected[i][j] = imgCorrected[i][j] * (255 / (max - min))
            else:
                imgCorrected[i][j] = imgCorrected[i][j] * 255

    cv2.imwrite('{}.png'.format(filename), imgCorrected)
    print("{}.png gespeichert".format(filename))

    count = 0
    for i in range(len(img)):
        for j in range(len(img[0])):
            if img[i][j] == imgCorrected[i][j]:
                count += 1
    print("Counter: {}".format(count))
    return imgCorrected


# ---------------------------------------------------------
# Teil 2
# ---------------------------------------------------------
darkImagesGray = []
for i in range(10):
    image = cv2.imread('./Bilder/Dunkelbild ({}).png'.format(i + 1))
    darkImagesGray.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))


def pixelwiseMeanAndSave(arr, filename):
    imageMean = np.zeros(shape=(len(arr[0]), len(arr[0][0])))

    for i in range(len(arr[0])):
        line = []
        for j in range(len(arr[0][0])):
            values = []
            for k in range(len(arr)):
                values.append(arr[k][i][j])
            line.append(np.mean(values))
        imageMean[i] = line
    cv2.imwrite('{}.png'.format(filename), imageMean)
    print("{}.png gespeichert".format(filename))

    return imageMean


darkImageMean = pixelwiseMeanAndSave(darkImagesGray, "Dunkelbild")
bildKontrastMaximiert(darkImageMean, "Dunkelbild_kontrastmax")


# print("DarkImageMean Array:\n{}".format(darkImageMean))
# print("DarkImage Y: {}".format(len(darkImageMean)))
# print("DarkImage X: {}".format(len(darkImageMean[0])))

def subtractAndSaveAs(img, darkImg, filename):
    subImg = np.zeros(shape=(len(img), len(img[0])))

    for i in range(len(img)):
        for j in range(len(img[0])):
            subImg[i][j] = img[i][j] - darkImg[i][j]

    cv2.imwrite('{}.png'.format(filename), subImg)
    print("{}.png gespeichert".format(filename))
    return subImg


# Dunkelbild von Grauwertkeil subtrahieren und speichern
subtractAndSaveAs(grauwertkeil, darkImageMean, "NoBildrauschen")

# ---------------------------------------------------------
# Teil 3
# ---------------------------------------------------------
# Mittelwertbild von 10 Weißbildern
whiteImagesGray = []
for i in range(10):
    image = cv2.imread('./Bilder/Weissbild ({}).png'.format(i + 1))
    whiteImagesGray.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))

whiteImageMean = pixelwiseMeanAndSave(whiteImagesGray, "Weissbild")
whiteImageMean = subtractAndSaveAs(whiteImageMean, darkImageMean, "Weissbild")
bildKontrastMaximiert(whiteImageMean, "Weißbild_kontrastmax")


def weissbildNormieren(img):
    return img / np.mean(img)


def divideAndSaveAs(img, whiteImg, filename):
    divImg = np.zeros(shape=(len(img), len(img[0])))

    for i in range(len(img)):
        for j in range(len(img[0])):
            if whiteImg[i][j] > 0:
                divImg[i][j] = float(img[i][j]) / float(whiteImg[i][j])
            else:
                print("Deadpixel x/y: {}/{}".format(j, i))
                divImg[i][j] = float(img[i][j])

    cv2.imwrite('{}.png'.format(filename), divImg)
    print("{}.png gespeichert".format(filename))
    return divImg


whiteImageNormiert = weissbildNormieren(whiteImageMean)
divGrauwertkeil = divideAndSaveAs(grauwertkeil, whiteImageNormiert, "Dividiert")

# ---------------------------------------------------------
# Teil 4
# ---------------------------------------------------------
ROI_number = 0
yTop = 5
yBottom = len(grauwertkeil) - 5
subPicsMean = []
subPicsStd = []
i = 0
while i < len(xValues):
    ROI = divGrauwertkeil[yTop:yBottom, xValues[i]:xValues[i + 1]]
    subPicsMean.append(np.mean(ROI))
    subPicsStd.append(np.std(ROI, ddof=1))
    cv2.imwrite('SubPicCorrected_{}.png'.format(ROI_number), ROI)
    ROI_number += 1
    i += 2

print("Mittelwerte SubPics nach Korrektur:\n{}".format(subPicsMean))
print("Standardabweichung SubPics nach Korrektur:\n{}".format(subPicsStd))
