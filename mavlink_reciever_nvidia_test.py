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
master = mavutil.mavlink_connection(f'udp:{target_ip}:14550', dialect ="ardupilotmega")

# Wait for the heartbeat message to find the system ID
master.wait_heartbeat()

print("Received heartbeat! System ID: %d" % master.target_system)
# Receive and print messages
while True:
    msg = master.recv_match(type="CUSTOM_PAYLOAD_CONTROL")
    if msg:
        print("Received message: %s" % msg)

