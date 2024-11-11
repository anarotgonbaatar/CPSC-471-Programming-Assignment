# *****************************************************
# This file implements a client for sending and receiving
# files to/from the sendfileserv.py server. The client
# can upload, download, and list files on the server.
# *****************************************************

import socket
import sys
import os

# Validate command-line arguments
if len(sys.argv) != 3:
    print("Usage: py cli.py <server machine> <server port>")
    sys.exit(1)

# Set server details
serverName = sys.argv[1]
controlPort = int(sys.argv[2])

# Connect to the server's control channel
controlSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
controlSocket.connect((serverName, controlPort))
print(f"Connected to the FTP server at {serverName} on port {controlPort}")

def sendCommand(command):
    """Send a command to the server and receive the response."""
    controlSocket.send(command.encode())
    response = controlSocket.recv(1024).decode().strip()
    return response

def handleDataChannel(dataPort, is_download, filename):
    """Handle the data channel for file transfer."""
    # Open data channel
    dataSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Connect to the server's ephemeral data port
    dataSocket.connect((serverName, dataPort))
    total_bytes = 0
    
    if is_download:
        # Receiving the file from the server
        with open(filename, 'wb') as f:
            while True:
                data = dataSocket.recv(1024)
                if not data:
                    break
                f.write(data)
                total_bytes += len(data)
        print(f"Received {filename}, {total_bytes} bytes transferred")
    else:
        # Sending the file to the server
        with open(filename, 'rb') as f:
            while (data := f.read(1024)):
                dataSocket.sendall(data)
                total_bytes += len(data)
        print(f"Sent {filename}, {total_bytes} bytes transferred")
    
    dataSocket.close()


# Start command loop
while True:
    command = input("ftp> ").strip()
    
    if command == "quit":
        sendCommand("quit")
        print("Closing connection.")
        controlSocket.close()
        break

    elif command == "ls":
        response = sendCommand("ls")
        print("Files on server:")
        print(response)

    elif command.startswith("get"):
        _, filename = command.split(maxsplit=1)
        response = sendCommand(f"get {filename}")
        
        if response.startswith("ERROR"):
            print(response)
        else:
            dataPort = int(response)
            handleDataChannel(dataPort, is_download=True, filename=filename)

    elif command.startswith("put"):
        _, filename = command.split(maxsplit=1)
        
        if not os.path.exists(filename):
            print(f"ERROR: File {filename} not found.")
            continue

        response = sendCommand(f"put {filename}")
        if response.startswith("ERROR"):
            print(response)
        else:
            dataPort = int(response)
            handleDataChannel(dataPort, is_download=False, filename=filename)

    else:
        print("Invalid command. Please use 'ls', 'get <filename>', 'put <filename>', or 'quit'.")

print("Disconnected from the server.")
