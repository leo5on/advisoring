#!/usr/bin/env python
from math import ceil
import cv2
import numpy as np
from skimage import io, feature, color, draw
from skimage.measure import CircleModel, ransac

def ixqleto(img):
    # fonte: http://opencvpython.blogspot.com/2012/05/skeletonization-using-opencv-python.html
    size = np.size(img)
    skel = np.zeros(img.shape,np.uint8)
    
    # _,img = cv2.threshold(img,127,255,0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS,(3,3))
    done = False
    
    while( not done):
        eroded = cv2.erode(img,element)
        temp = cv2.dilate(eroded,element)
        temp = cv2.subtract(img,temp)
        skel = cv2.bitwise_or(skel,temp)
        img = eroded.copy()
    
        zeros = size - cv2.countNonZero(img)
        if zeros==size:
            done = True


    return skel


def quanti(img, K=8):
    # fonte: https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_ml/py_kmeans/py_kmeans_opencv/py_kmeans_opencv.html
    Z = img.reshape((-1,3))

    # convert to np.float32
    Z = np.float32(Z)

    # define criteria, number of clusters(K) and apply kmeans()
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1.0)
    ret,label,center=cv2.kmeans(Z,K,None,criteria,10,cv2.KMEANS_RANDOM_CENTERS)

    # Now convert back into uint8, and make original image
    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img.shape))

    return res2

img_original = cv2.imread('/home/leleo/Documents/BIR/computer-vision/ball_2.jpeg',1)
img_k = quanti(img_original.copy(), 3)
# img_gray = cv2.imread('/home/leleo/Documents/BIR/computer-vision/BIR_basketball.jpeg',0)
img_bi = cv2.bilateralFilter(img_k,70,100,10)
img_gray = cv2.cvtColor(img_bi, cv2.COLOR_BGR2GRAY)
#img_gauss = cv2.GaussianBlur(img_bi,(5,5),0)
img_shrinked = cv2.resize(img_bi, (0,0), fx=0.2, fy=0.2, interpolation = cv2.INTER_LINEAR)

edges = cv2.Canny(img_shrinked,50,200)

kernel = np.ones((11,11),np.uint8)
img_morph = cv2.morphologyEx(edges, cv2.MORPH_CLOSE, kernel)
gradient = cv2.morphologyEx(img_morph, cv2.MORPH_GRADIENT, kernel)

skel_1 = ixqleto(gradient)
skel_normal_size = cv2.resize(skel_1, (0,0), fx=5.0, fy=5.0, interpolation = cv2.INTER_LINEAR)


points = np.array(np.nonzero(edges)).T
print(points)
model_robust, inliers = ransac(points, CircleModel, min_samples=100, residual_threshold=3, max_trials=1000)
cy, cx, r = model_robust.params
cy = ceil(cy)
cx = ceil(cx)
r = ceil(r)

detected_circle = cv2.circle(img_shrinked.copy(), (cx,cy), r, (0,255,0), 1)

cv2.namedWindow('original_image', cv2.WINDOW_NORMAL) 
cv2.namedWindow('bilateral', cv2.WINDOW_NORMAL)
cv2.namedWindow('edges', cv2.WINDOW_NORMAL)
cv2.namedWindow('morph', cv2.WINDOW_NORMAL)  
cv2.namedWindow('gradient', cv2.WINDOW_NORMAL) 
cv2.namedWindow('skel', cv2.WINDOW_NORMAL)
cv2.namedWindow('quanti', cv2.WINDOW_NORMAL)
cv2.namedWindow('detected_circles', cv2.WINDOW_NORMAL)      
cv2.imshow('original_image',img_original)
cv2.imshow('bilateral',img_bi)
cv2.imshow('edges',edges)
cv2.imshow('morph',img_morph)
cv2.imshow('gradient',gradient)
cv2.imshow('skel',skel_normal_size)
cv2.imshow('quanti',img_k)
cv2.imshow('detected_circles',detected_circle)
cv2.waitKey(0)
cv2.destroyAllWindows()