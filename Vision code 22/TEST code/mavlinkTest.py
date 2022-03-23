from pymavlink import mavutil

# Start a connection listening to a UDP port
the_connection = mavutil.mavlink_connection('/dev/ttyACM0')

# Wait for the first heartbeat 
#   This sets the system and component ID of remote system for the link
the_connection.wait_heartbeat()
# messages can be find at https://mavlink.io/en/messages/common.html#GLOBAL_POSITION_INT
message = the_connection.messages['GPS_RAW_INT']
lat = message.lat
lon = message.lon
numOfSatelites = the_connection.messages['GPS_RAW_INT'].satellites_visible
print("sats: %u lat: %u lon: %u" % (numOfSatelites,lat, lon))
message = the_connection.messages['GPS_RAW_INT']
lat = the_connection.messages['GLOBAL_POSITION_INT'].lat
lon = the_connection.messages['GLOBAL_POSITION_INT'].lon
print("lat: %u lon: %u" % (lat, lon))
print("Heartbeat from system (system %u component %u)" % (the_connection.target_system, the_connection.target_component))

# Once connected, use 'the_connection' to get and send messages