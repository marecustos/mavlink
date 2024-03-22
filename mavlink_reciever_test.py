from pymavlink import mavutil
import os

# Set the MAVLINK20 environment variable to '1'
os.environ['MAVLINK20'] = '1'

# Create a MAVLink connection
master = mavutil.mavlink_connection('udp:localhost:9000', dialect ="ardupilotmega")

# Wait for the heartbeat message to find the system ID
master.wait_heartbeat()

print("Received heartbeat! System ID: %d" % master.target_system)

# Receive and print messages
while True:
    msg = master.recv_match(type="CUSTOM_PAYLOAD_CONTROL")
    if msg:
        print("Received message: %s" % msg)

