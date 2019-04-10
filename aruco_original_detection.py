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

      
    # Our operations on the image come here
    gray = cv.cvtColor(image, cv.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
    parameters =  aruco.DetectorParameters_create()

    # lists of ids and the corners beloning to each id
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)


    gray = aruco.drawDetectedMarkers(image, corners, ids)

    # show the images
    cv.imshow('tag_detection',gray)
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

