import cv2
import numpy as np

# Wczytanie obrazów
image_sp = cv2.imread('cboard_salt_pepper.tif', cv2.IMREAD_GRAYSCALE)
image_pepper = cv2.imread('cboard_pepper_only.tif', cv2.IMREAD_GRAYSCALE)
image_salt = cv2.imread('cboard_salt_only.tif', cv2.IMREAD_GRAYSCALE)

# a) Filtr liniowy średniej kwadratowej 3x3
kernel = np.ones((3,3), np.float32) / 9
blurred = cv2.filter2D(image_sp, -1, kernel)

# b) Filtr medianowy
median = cv2.medianBlur(image_sp, 3)

# c) Filtry minimum i maksimum
min_filter = cv2.erode(image_sp, np.ones((3, 3), np.uint8))
max_filter = cv2.dilate(image_sp, np.ones((3, 3), np.uint8))

# Zapisz wyniki
cv2.imwrite('blurred.tif', blurred)
cv2.imwrite('median.tif', median)
cv2.imwrite('min_filter.tif', min_filter)
cv2.imwrite('max_filter.tif', max_filter)

# Wyświetlanie wyników
cv2.imshow('Original', image_sp)
cv2.imshow('Blurred', blurred)
cv2.imshow('Median', median)
cv2.imshow('Min Filter', min_filter)
cv2.imshow('Max Filter', max_filter)
cv2.waitKey(0)
cv2.destroyAllWindows()
