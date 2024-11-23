# *****************************************************
# This file implements a client for sending and receiving
# files to/from the sendfileserv.py server. The client
# can upload, download, and list files on the server using cmds.py
# *****************************************************
import socket
import sys
from cmds import execute_command

# Validate command-line arguments
if len(sys.argv) != 3:
    print("Usage: python sendfilecli.py <server machine> <server port>")
    sys.exit(1)

# Set server details
server_name = sys.argv[1]
control_port = int(sys.argv[2])

# Connect to the server's control channel
control_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
control_socket.connect((server_name, control_port))
print(f"Connected to the FTP server at {server_name} on port {control_port}")

# Start command loop
while True:
    command = input("ftp> ").strip()
    if execute_command(control_socket, server_name, command) == "quit":
        break

print("Disconnected from the server.")