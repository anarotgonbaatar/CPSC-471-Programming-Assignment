
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import os
from ephemeral import get_ephemeral_port

# Control channel port
controlPort = 1234

# Create and bind control socket
control_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
control_socket.bind( ( '', controlPort ) )
control_socket.listen(1)    # Listen for client connections

print( f"FTP server is listening on port { controlPort }" )

# Accept connections forever
while True:
	print( "Waiting for connections..." )
	client_socket, addr = control_socket.accept()   # Accept connections
	print( "Accepted connection from client: ", addr )
	print( "\n" )

	while True:
		command = client_socket.recv( 1024 ).decode().strip()    # Receive FTP command, up to 1024 bytes
		if not command:
			break   # Cleint disconnected
		
		print( f"Received command: { command }" )
		
		if command == 'ls':
			# List all files in the directory
			files = '\n'.join( os.listdir( '.' ) )
			client_socket.send( files.encode() )
			
		elif command.startswith( "get" ):
			filename = command.split()[1] # extract filename
			if os.path.exists( filename ):
				# Generate ephemeral port for the data channel
				data_port = get_ephemeral_port()
				client_socket.send( str( data_port ).encode() )	# Send port to client
				
				# Open data channel
				data_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
				data_socket.bind( ( '', data_port ) )
				data_socket.listen(1)
				data_conn, _ = data_socket.accept()
				
				# Send file over data channel
				with open( filename, 'rb' ) as f:
					data_conn.sendfile(f)
					
				data_conn.close()    # Close data connection
				data_socket.close()
				print( f"Sent { filename } to client" )
			else:
				client_socket.send( b"ERROR: File not found" )
		
		elif command.startswith( 'put' ):
			filename = command.split()[1]	# Extract filename
			
			# Generate ephemeral port for receiving data
			data_port = get_ephemeral_port()
			client_socket.send( str( data_port ).encode() )	# Send port to clinet

			# Open data channel
			data_socket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			data_socket.bind( ( '', data_port ) )
			data_socket.listen(1)
			data_conn, _ = data_socket.accept()

			# Receive file over data channel
			with open( filename, 'wb' ) as f:
				while True:
					data = data_conn.recv( 1024 )
					if not data:
						break
					f.write( data )
			
			data_conn.close()
			data_socket.close()
			print( f"Received { filename } from client" )

		elif command == "quit":
			print( "Closeing connection with client" )
			client_socket.close()
			break

	print( "Waiting for new connection" )
	
