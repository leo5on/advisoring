#!/usr/bin/env python
import cv2
import numpy as np

img_original = cv2.imread('/home/leo5on/Documents/BIR/Advisoring/Sensor-calibratrion/teste.jpg',1)
img_bi = cv2.bilateralFilter(img_original,9,0.05,75)
img_gauss = cv2.GaussianBlur(img_original,(5,5),0)
edges = cv2.Canny(img_gauss,60,80)

cv2.imwrite('/home/leo5on/Pictures/ransac_test/test_' + '.jpg', edges)

cv2.namedWindow('edges', cv2.WINDOW_NORMAL)    

cv2.imshow('edges',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()