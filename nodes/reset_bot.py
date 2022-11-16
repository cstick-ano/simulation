#! /usr/bin/env python

import rospy
import numpy as np
from std_srvs.srv import Empty
from sensor_msgs.msg import LaserScan

def reset():
    rospy.init_node('reset_bot')
    reset_world = rospy.ServiceProxy('/gazebo/reset_world', Empty)
    scan_range = []
    rate = rospy.Rate(10) # 10hz

    while not rospy.is_shutdown():
        data = None
        while data is None:
            try:
                data = rospy.wait_for_message('laser/scan', LaserScan, timeout=5)
            except:
                pass

        for i in range(len(data.ranges)):
            if data.ranges[i] == float('Inf'):
                scan_range.append(3.5)
            elif np.isnan(data.ranges[i]):
                scan_range.append(0)
            else:
                scan_range.append(data.ranges[i])

        if 0.16 > min(scan_range) > 0:
            rospy.loginfo("Collision")
            rospy.wait_for_service('/gazebo/reset_world')
            try:
                reset_world()
                scan_range.clear()
                scan_range.append(20)
            except (rospy.ServiceException) as e:
                print("gazebo/reset_simulation service call failed")
            
        rate.sleep()

if __name__ == '__main__':
    reset()