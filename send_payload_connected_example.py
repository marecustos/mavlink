from pymavlink import mavutil
import os
import time

# Set the MAVLINK20 environment variable to '1'
os.environ['MAVLINK20'] = '1'

# Create a MAVLink connection
master_send = mavutil.mavlink_connection('udpout:localhost:9000', dialect="ardupilotmega",source_system=1)
master_recv = mavutil.mavlink_connection('udp:localhost:9001', dialect ="ardupilotmega")

# Wait for the heartbeat message to find the system ID
master_recv.wait_heartbeat()

print("Received heartbeat! System ID: %d" % master_recv.target_system)

# Receive and print messages
while True:
    msg = master_recv.recv_match(type="CONNECTED_PAYLOAD_ACK")
    if msg:
        if (msg.result == 0):
            master_send.mav.connected_payload_send(payload_id=112,payload_name="seabotX".encode('utf-8'),payload_state="connected".encode('utf-8'))
            print("sent message")
