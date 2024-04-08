from pymavlink import mavutil
import subprocess
import os

# Set the MAVLINK20 environment variable to '1'
os.environ['MAVLINK20'] = '1'

def get_ip_address(interface):
    result = subprocess.run(['ifconfig', interface], stdout=subprocess.PIPE)
    output = result.stdout.decode('utf-8')
    lines = output.split('\n')
    for line in lines:
        if 'inet ' in line:
            parts = line.split()
            return parts[1]
    return None

target_ip = get_ip_address('eth0')
if target_ip:
    print(f"Detected target IP address: {target_ip}")
else:
    print("Failed to detect target IP address")

# Create a MAVLink connection
master_send = mavutil.mavlink_connection(f'udpout:10.42.0.1:9000', dialect="ardupilotmega",source_system=1)
master_recv = mavutil.mavlink_connection(f'udp:{target_ip}:9001', dialect ="ardupilotmega")

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

