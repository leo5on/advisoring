#!/usr/bin/env python
from __future__ import print_function
import roslib
import sys
import rospy
import cv2 as cv
import cv2.aruco as aruco
import numpy as np
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError
import matplotlib.pyplot as plt
import matplotlib as mpl

class image_detection:

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
  
    # Converting the image to a grayscale
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)

    # Loading the aruco original dictionary for comparison
    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)

    # Specific Parameters generation
    parameters =  aruco.DetectorParameters_create()

    # Lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)

    # Function that displays the id and the corners to the image
    gray = aruco.drawDetectedMarkers(image, corners, ids)

    # show the images
    cv.imshow('feature',gray)
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