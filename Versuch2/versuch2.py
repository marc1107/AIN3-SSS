import cv2

img = cv2.imread('./Bilder/Grauwertkeil.png')

cv2.imshow('image', img)
cv2.waitKey(0)
