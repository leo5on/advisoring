#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2 as cv
import numpy as np
import argparse
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class image_detection():

  def __init__(self):
    self.image_pub = rospy.Publisher("image_topic_2",Image, queue_size=10)

    self.image_sub = rospy.Subscriber("/warthog/camera/image_raw",Image,self.callback)

    #Initial Variables
    self.bridge = CvBridge()

  def callback(self,data):
    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)
    
    # load the image
    image = cv_image

    #inverts the image
    inverted_image = cv.bitwise_not(cv_image)

    #convert RGB to HSV
    hsv_inverted = cv.cvtColor(inverted_image, cv.COLOR_BGR2HSV) 

    # define the list of boundaries
    boundaries_green = ([179, 255, 255], [160, 0, 0])
    boundaries_red = ([90, 255, 255], [80, 70, 50])

	# create NumPy arrays from the boundaries
    lower_green = np.array(boundaries_green[1])
    upper_green = np.array(boundaries_green[0])
    lower_red = np.array(boundaries_red[1])
    upper_red = np.array(boundaries_red[0])

	# find the colors within the specified boundaries and apply the mask
    mask_green = cv.inRange(hsv_inverted, lower_green, upper_green)
    mask_red = cv.inRange(hsv_inverted, lower_red, upper_red)
    mask_all = cv.add(mask_green, mask_red)

  # output images 
    output_green = cv.bitwise_and(image, image, mask = mask_green)
    output_red = cv.bitwise_and(image, image, mask = mask_red)
    output_all = cv.bitwise_or(image, image, mask = mask_all)

	# show the images
    cv.imshow('hsv_image',image)
    #cv.imshow('mask_green',mask_green)
    #cv.imshow('mask_red',mask_red)
    #cv.imshow('output_green',output_green)
    #cv.imshow('output_red',output_red)
    cv.imshow('output_all',output_all)
    cv.waitKey(3)

    try:
      self.image_pub.publish(self.bridge.cv2_to_imgmsg(cv_image, "bgr8"))
    except CvBridgeError as e:
      print(e)

def main(args):
  id = image_detection()
  rospy.init_node('image_detection', anonymous=True)
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
  cv.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)