from pymavlink import mavutil
import os

# Set the MAVLINK20 environment variable to '1'
os.environ['MAVLINK20'] = '1'

# Create a MAVLink connection
master_send = mavutil.mavlink_connection('udpout:localhost:9000', dialect="ardupilotmega",source_system=1)
master_recv = mavutil.mavlink_connection('udp:localhost:9001', dialect ="ardupilotmega")

# Wait for the heartbeat message to find the system ID
master_recv.wait_heartbeat()

print("Received heartbeat! System ID: %d" % master_recv.target_system)
target_command_values = {
    "yRotationRelative": 0,
    "dockingRotationRelative": 0,
    "probXTransition": 0,
    "probYTransition": 0,
    "probZTransition": 0,
    "deployTransition": 0,
    "cameraRotationRelative": 0
}
# Receive and print messages
while True:
    msg = master_recv.recv_match(type="CUSTOM_PAYLOAD_CONTROL")
    if msg:
        print(target_command_values.keys())
        print(msg.command_target)
        print(msg.command_target in target_command_values.keys())
        if (msg.command_target in target_command_values.keys()):
            target_command_values[msg.command_target] += msg.command_value
            master_send.mav.custom_payload_control_send(msg.command_target.encode('utf-8'), target_command_values[msg.command_target])
        print(f"Received message:{msg}")

