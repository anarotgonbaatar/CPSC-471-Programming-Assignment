# *************************************************************
# This program provides a function to generate an ephemeral port
# *************************************************************

import socket

def get_ephemeral_port():
    # Create a temporary socket bound to port 0, which will choose an ephemeral port
    temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    temp_socket.bind(('', 0))
    ephemeral_port = temp_socket.getsockname()[1]
    temp_socket.close()
    return ephemeral_port
