"""
In This file we showcase how to link and arm the ROV Device // This is only a test
*SSC ROV Research and Development*
This message is able to fully replace the joystick inputs.
"""

# Import mavutil
from pymavlink import mavutil
import time

# Create the connection
master = mavutil.mavlink_connection('udpin:192.168.2.1:14550')
# Wait a heartbeat before sending commands
master.wait_heartbeat()


# Arm
# master.arducopter_arm() or:
master.mav.command_long_send(
    master.target_system,
    master.target_component,
    mavutil.mavlink.MAV_CMD_COMPONENT_ARM_DISARM,
    0,
    1, 0, 0, 0, 0, 0, 0)

# wait until arming confirmed (can manually check with master.motors_armed())
print("Waiting for the vehicle to arm")
master.motors_armed_wait()
print('Armed!')



# Send a positive x value, negative y, negative z,
# positive rotation and no button.
# https://mavlink.io/en/messages/common.html#MANUAL_CONTROL
# Warning: Because of some legacy workaround, z will work between [0-1000]
# where 0 is full reverse, 500 is no output and 1000 is full throttle.
# x,y and r will be between [-1000 and 1000].
turn = 0
while True:
    if turn%9999 == 0:
        master.mav.manual_control_send(
                                master.target_system,
                                x=0, #throttle
                                y=0, #roll
                                z=500, #pitch
                                r=0, #yaw
                                buttons=0)
    else:
        master.mav.manual_control_send(
                                master.target_system,
                                x=0, #throttle
                                y=0, #roll
                                z=870, #pitch
                                r=0, #yaw
                                buttons=0)
    turn+=1
    #time.sleep(1)
    

# To active button 0 (first button), 3 (fourth button) and 7 (eighth button)
# It's possible to check and configure this buttons in the Joystick menu of QGC
'''buttons = 1<<3
master.mav.manual_control_send(
    master.target_system,
    0,
    -1000,
    500, # 500 means neutral throttle
    0,
    buttons)'''

print('Done')