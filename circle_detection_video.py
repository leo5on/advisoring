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

        self.rp = ros_comp()

        self.vid_original = cv2.VideoCapture('/home/leo5on/Videos/bouncing_ball.mp4')
        self.Xcenter = 0
        self.Ycenter = 0
        self.Radius = 0

    def image_treatment(self):

        # Check if camera opened successfully
        if (self.vid_original.isOpened()== False): 
            print("Error opening video stream or file")

        # Read until video is completed
        while(self.vid_original.isOpened()):
            # Capture frame-by-frame
            ret, frame = self.vid_original.read()
            if ret == True:

                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                frame_blur = cv2.medianBlur(frame_gray,5)

                # parameters: 1=dp ratio, 500=min distance btw centers, param1=higher threshold, param2= accumulator threshold
                circles = cv2.HoughCircles(frame_blur,cv2.HOUGH_GRADIENT,1,1000,param1=2,param2=1,minRadius=1,maxRadius=30)

                frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)


                circles = np.uint16(np.around(circles))
                for i in circles[0,:]:
                    # draw the outer circle 
                    cv2.circle(frame,(i[0],i[1]),i[2],(0,0,255),3)
                    # draw the center of the circle
                    cv2.circle(frame,(i[0],i[1]),15,(0,255,0),1)

                coord_center = circles[0]
                self.Xcenter = int(coord_center[0][0])
                self.Ycenter = int(coord_center[0][1])
                self.Radius = int(coord_center[0][2])

                self.rp.pub_coords(self.Xcenter, self.Ycenter, self.Radius)

                cv2.namedWindow('detected circles', cv2.WINDOW_NORMAL)
          
                # Display the resulting frame
                cv2.imshow('detected circles',frame)

                # Press Q on keyboard to  exit
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    break

            # Break the loop
            else: 
                break

        # When everything done, release the video capture object
        self.vid_original.release()    


    def ret_Xcent(self):
        return self.Xcenter

    def ret_Ycent(self):
        return self.Ycenter

    def ret_Radius(self):
        return self.Radius

def main():
    # starts the node
    rospy.init_node("ball_detection", anonymous=True)

    cd = circle_detection()
    cd.image_treatment()

if __name__ == '__main__':
    main()