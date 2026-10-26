import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/syj/robot_workspace/robot/ros2_ws/src/my_arm_description/install/my_arm_description'
