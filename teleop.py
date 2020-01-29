#!/usr/bin/env python

"""
Node converts joystick inputs into Twist type msgs for Gazebo use
"""

import rospy
from geometry_msgs.msg import Twist
from sensor_msgs.msg import Joy