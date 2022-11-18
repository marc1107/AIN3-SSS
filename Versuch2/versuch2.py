import cv2
import numpy as np

image = cv2.imread('./Bilder/Grauwertkeil.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Aufbau der beiden Arrays: alle ungeraden Werte sind Startwerte eines Bereichs,
# die geraden die zugehörigen Endwerte
topRow = []
bottomRow = []

# erste Startwerte für oberste und unterste Reihe speichern
topRow.append(5)
bottomRow.append(5)

# topRow füllen
i = 80
while i < len(image[0]):
    if i + 10 < len(image[0]):
        if int(image[0][i + 10]) - int(image[0][i]) >= 20:
            topRow.append(i)  # Endwert speichern
            i += 15
            topRow.append(i)  # neuen Startwert speichern
    i += 1
topRow.append(len(image[0]) - 5)

# bottomRow füllen
i = 0
while i < len(image[len(image) - 1]):
    if i + 10 < len(image[len(image) - 1]):
        if int(image[len(image) - 1][i + 10]) - int(image[len(image) - 1][i]) >= 20:
            bottomRow.append(i)  # Endwert speichern
            i += 15
            bottomRow.append(i)  # neuen Startwert speichern
    i += 1
bottomRow.append(len(image[len(image) - 1]) - 5)

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
yBottom = len(image) - 5
subPicsMean = []
subPicsStd = []
i = 0
while i < len(xValues):
    ROI = image[yTop:yBottom, xValues[i]:xValues[i + 1]]
    subPicsMean.append(np.mean(ROI))
    subPicsStd.append(np.std(ROI, ddof=1))
    cv2.imwrite('SubPic_{}.png'.format(ROI_number), ROI)
    ROI_number += 1
    i += 2

print("Mittelwerte SubPics:\n{}".format(subPicsMean))
print("Standardabweichung SubPics:\n{}".format(subPicsStd))

# for i in range(len(image[0])):
#     print("Pixel {}: {}".format(i, image[0][i]))

# print("X-Wert: " + str(len(image[0])))
# print("Y-Wert: " + str(len(image)))

# cv2.imshow('image', image)
# cv2.waitKey(0)


# ---------------------------------------------------------
# Teil2
# ---------------------------------------------------------
darkImagesGray = []
for i in range(10):
    image = cv2.imread('./Bilder/Dunkelbild ({}).png'.format(i + 1))
    darkImagesGray.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))


def pixelwiseMean(arr):
    imageMean = np.zeros(shape=(len(arr[0]), len(arr[0][0])))

    for i in range(len(arr[0])):
        line = []
        for j in range(len(arr[0][0])):
            values = []
            for k in range(len(arr)):
                values.append(arr[k][i][j])
            line.append(np.mean(values))
        imageMean[i] = line

    return imageMean


darkImageMean = pixelwiseMean(darkImagesGray)
cv2.imwrite('Dunkelbild.png', darkImageMean)

print("DarkImageMean Array:\n{}".format(darkImageMean))
# print("DarkImage Y: {}".format(len(darkImageMean)))
# print("DarkImage X: {}".format(len(darkImageMean[0])))
