from pymavlink import mavutil
from time import sleep, time
import os
import src.fligtController as flightController
import time
import csv
import numpy as np 
import pandas as pd  

import dronekit_sitl
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

#connection_string = "/dev/ttyACM0" # sitl.connection_string()

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

vehicle.lat = 0
vehicle.lon = 0
vehicle.alt = 0
vehicle.angle = 0

@vehicle.on_message("GLOBAL_POSITION_INT")
def pancake(self, name, message):
    print("time: %s" % message.time_boot_ms)
    print("system: %s"% time.time())
    print('angle: %s' % message.hdg)
    self.lat = message.lat
    self.lon = message.lon
    self.alt = message.alt
    self.angle = message.hdg/100

sleep(10)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
print("Completed cord resived: %i" % vehicle.lat)

