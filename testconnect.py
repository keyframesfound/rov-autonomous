from pymavlink import mavutil

mavutil.set_dialect("ardupilotmega")

autopilot = mavutil.mavlink_connection('udpout:0.0.0.0:9000')
autopilot.wait_heartbeat()
autopilot.motors_armed_wait()
print('Armed!')