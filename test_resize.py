from math import ceil
import cv2
import numpy as np
from skimage import io, feature, color, draw
from skimage.measure import CircleModel, ransac

img_original = cv2.imread('/home/leleo/Documents/BIR/computer-vision/sun.jpg',1)
edges = cv2.resize(img_original, (0,0), fx=0.2, fy=0.2, interpolation = cv2.INTER_LINEAR)
edges = cv2.resize(edges, (0,0), fx=5.0, fy=5.0, interpolation = cv2.INTER_LINEAR)

cv2.namedWindow('edges', cv2.WINDOW_NORMAL)    

cv2.imshow('edges',edges)
cv2.waitKey(0)
cv2.destroyAllWindows()