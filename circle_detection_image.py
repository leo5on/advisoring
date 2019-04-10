#!/usr/bin/env python
import cv2
import numpy as np
import roslib
import rospy
from std_msgs.msg import Int32



class ros_comp():

    def __init__(self):

        # starts publishers of joint controllers topics to control the Dynamixels
        self.center_pub = rospy.Publisher("center_coords", Int32, queue_size=10) 

    def pub_coords(self, x, y, r):
        self.center_pub.publish(x)
        self.center_pub.publish(y)
        self.center_pub.publish(r) 

class circle_detection():

    def __init__(self):

        self.img_original = cv2.imread('/home/leo5on/Documents/BIR/Advisoring/Sensor-calibratrion/teste.jpg',1)
        self.img_gray = cv2.imread('/home/leo5on/Documents/BIR/Advisoring/Sensor-calibratrion/teste.jpg',0)
        self.img_blur = cv2.medianBlur(self.img_gray,5)
        self.Xcenter = 0
        self.Ycenter = 0
        self.Radius = 0

    def image_treatment(self):

        # parameters: 1=dp ratio, 500=min distance btw centers, param1=higher threshold, param2= accumulator threshold
        circles = cv2.HoughCircles(self.img_blur,cv2.HOUGH_GRADIENT,1,500,param1=38,param2=30,minRadius=950,maxRadius=1000)

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(self.img_original,(i[0],i[1]),i[2],(0,0,255),5)
            # draw the center of the circle
            cv2.circle(self.img_original,(i[0],i[1]),15,(0,255,0),10)

        coord_center = circles[0]
        self.Xcenter = int(coord_center[0][0])
        self.Ycenter = int(coord_center[0][1])
        self.Radius = int(coord_center[0][2])

        cv2.namedWindow('detected circles', cv2.WINDOW_NORMAL)    

        cv2.imshow('detected circles',self.img_original)
        cv2.waitKey(3000)
        cv2.destroyAllWindows()

    def ret_Xcent(self):
        return self.Xcenter

    def ret_Ycent(self):
        return self.Ycenter

    def ret_Radius(self):
        return self.Radius

class every():

    def __init__(self):
        self.rp = ros_comp()
        self.cd = circle_detection()

    def execution(self):
        self.cd.image_treatment()
        xc = self.cd.ret_Xcent()
        yc = self.cd.ret_Ycent()
        r = self.cd.ret_Radius()
        self.rp.pub_coords(xc, yc, r)



def main():
    # starts the node
    rospy.init_node("ball_detection", anonymous=True)

    e = every()
    e.execution()

if __name__ == '__main__':
    main()