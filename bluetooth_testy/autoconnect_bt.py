# import bluetooth
# import subprocess
#
# # Set the MAC address of the Bluetooth device you want to connect to
# target_address = 'A0:5A:5D:5B:6A:72'
#
# # Set the Bluetooth service UUID you want to connect to
# # This will depend on the type of device you're connecting to
# target_service = 'E0CBF06C-CD8B-4647-BB8A-263B43F0F974'
#                   # e0cbf06c-cd8b-4647-bb8a-263b43f0f974
# # Search for nearby Bluetooth devices
# nearby_devices = bluetooth.discover_devices()
#
#
# passkey = "0005" # passkey of the device you want to connect
#
# # Loop through the nearby devices and try to connect to the target device
# for address in nearby_devices:
#     print(address)
#     if address == target_address:
#         # Try to connect to the target device
#         print(f"Connecting to {target_address}...")
#         # Create a Bluetooth socket and connect to the target device
#         sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
#         sock.connect((target_address, 1))
#
#         # Receive some data from the target device
#         data = sock.recv(1024)
#         print(f"Received: {data}")
#
#         # Close the socket
#         sock.close()
import subprocess


bluetooth_address = 'A0:5A:5D:5B:6A:72'

# PowerShell commands to pair and connect to a Bluetooth device
powershell_commands = [
    'Import-Module DeviceManagement',
    f'Add-Device -Address {bluetooth_address}',
    f'Start-Device -Address {bluetooth_address}'
]

# Run PowerShell commands from Python
for command in powershell_commands:
    subprocess.run(['powershell.exe', '-Command', command], shell=True)