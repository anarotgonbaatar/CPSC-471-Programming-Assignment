# *************************************************************
# This program provides a function to generate an ephemeral port
# *************************************************************

import socket

def get_ephemeral_port():
    # Create a temporary socket bound to port 0, which will choose an ephemeral port
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as temp_socket:
        temp_socket.bind(('', 0))  # Bind to port 0 to select an ephemeral port
        ephemeral_port = temp_socket.getsockname()[1]  # Retrieve the selected ephemeral port
    return ephemeral_port
