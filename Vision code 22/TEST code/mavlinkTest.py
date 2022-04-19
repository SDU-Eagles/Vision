from pymavlink import mavutil
from time import sleep, time
import os
import src.fligtController as flightController
import time
import csv
import numpy as np 
import pandas as pd  

# connection = mavutil.mavlink_connection("/dev/ttyACM0")

# connection.wait_heartbeat()
# connection.

# print("Heartbeat from system (system %u component %u)" % (connection.target_system, connection.target_component))


# while True:
#     try: 
#         message = connection.messages['GLOBAL_POSITION_INT']
#     except : 
#         print("failed")
#         continue
#     else:
#         print("lat: %u lon: %u" % (message.lat,message.lon))

# message = connection.messages['GLOBAL_POSITION_INT']



# fc = flightController.fligtController(port="/dev/ttyACM0")
# while True:
#     lat,lon,alt,angle,time_stamp = fc.getGPScords()
#     # print("lat: %i"%(lat))
#     # print("lon: %i"%(lon))
#     # print("alt: %i"%(alt))
#     print("angle: %f , time: %f"%(angle, time_stamp))
#     sleep(1)




connection_string = "/dev/ttyACM0" # sitl.connection_string()

# Import DroneKit-Python
from dronekit import connect, VehicleMode

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True,  baud=57600)

# Get some vehicle attributes (state)
print("Get some vehicle attribute values:")
print(" GPS: %s" % vehicle.gps_0)
print(" Battery: %s" % vehicle.battery)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Mode: %s" % vehicle.mode.name)    # settable

@vehicle.on_message("GLOBAL_POSITION_INT")
def pancake(self, name, message):
    print("time: %s" % message.time_boot_ms)
    print("system: %s"% time.time())
    print('angle: %s' % message.hdg)

sleep(10)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
print("Completed")

