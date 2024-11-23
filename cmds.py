# *************************************************************
# This file focuses on handling FTP commands and responses. 
# This includes ls, get, put, and quit commands
# *************************************************************

import os
import socket

def send_command(control_socket, command):
#Send a command to the server and receive the response
    control_socket.send(command.encode())
    response = control_socket.recv(1024).decode().strip()
    return response

def handle_data_channel(server_name, data_port, is_download, filename):
#Handle the data channel for file transfer.
    data_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    data_socket.connect((server_name, data_port))
    total_bytes = 0

    if is_download:
        # Receiving the file from the server
        with open(filename, 'wb') as f:
            while True:
                data = data_socket.recv(1024) #recieve data in chunks
                if not data:
                    break
                f.write(data) #writes data to local file
                total_bytes += len(data)
        print(f"Received {filename}, {total_bytes} bytes transferred")
    else:
        # Sending the file to the server
        with open(filename, 'rb') as f:
            while (data := f.read(1024)):
                data_socket.sendall(data)
                total_bytes += len(data)
        print(f"Sent {filename}, {total_bytes} bytes transferred")
    
    data_socket.close()

def execute_command(control_socket, server_name, command):
#Execute the given FTP command
    if command == "ls":
        response = send_command(control_socket, "ls")
        print("Files on server:")
        print(response)
    
    elif command.startswith("get"):
        #Downloads a file to server
        _, filename = command.split(maxsplit=1)
        response = send_command(control_socket, f"get {filename}")
        if response.startswith("ERROR"):
            print(response)
        else:
            data_port = int(response)
            handle_data_channel(server_name, data_port, is_download=True, filename=filename)
    
    elif command.startswith("put"):
        #uploading file to server
        _, filename = command.split(maxsplit=1)
        if not os.path.exists(filename):
            print(f"ERROR: File {filename} not found.")
            return

        response = send_command(control_socket, f"put {filename}")
        if response.startswith("ERROR"):
            print(response)
        else:
            data_port = int(response)
            handle_data_channel(server_name, data_port, is_download=False, filename=filename)
    
    elif command == "quit":
        #Closing connection
        send_command(control_socket, "quit")
        print("Closing connection.")
        control_socket.close()
        return "quit"
    
    else:
        #Handles invalid commands
        print("Invalid command. Please use 'ls', 'get <filename>', 'put <filename>', or 'quit'.")
