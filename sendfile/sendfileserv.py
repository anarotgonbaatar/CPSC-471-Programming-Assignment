
# *****************************************************
# This file implements a server for receiving the file
# sent using sendfile(). The server receives a file and
# prints it's contents.
# *****************************************************

import socket
import os
from sendfile.ephemeral import get_ephemeral_port

# Control channel port
controlPort = 1234
# Create and bind control socket
controlSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
controlSocket.bind( ( '', controlPort ) )
controlSocket.listen(1)    # Listen for client connections

print( f"FTP server is listening on port {controlPort}" )

# ************************************************
# Receives the specified number of bytes
# from the specified socket
# @param sock - the socket from which to receive
# @param numBytes - the number of bytes to receive
# @return - the bytes received
# *************************************************
def recvAll(sock, numBytes):
	# Receive all bytes from a socket
	recvBuff = ""
	tmpBuff = ""
	
	# Keep receiving till all is received
	while len(recvBuff) < numBytes:
		
		# Attempt to receive bytes
		tmpBuff =  sock.recv(numBytes)
		
		# The other side has closed the socket
		if not tmpBuff:
			break
		
		# Add the received bytes to the buffer
		recvBuff += tmpBuff
	
	return recvBuff
		
# Accept connections forever
while True:
	print("Waiting for connections...")
	clientSocket, addr = controlSocket.accept()   # Accept connections
	print("Accepted connection from client: ", addr)
	print("\n")

	while True:
		command = clientSocket.recv( 1024 ).decode().strip()    # Receive FTP command
		if not command:
			break   # Cleint disconnected
		
		print( f"Received command: { command }" )
		
		if command == 'ls':
			# List all files in the directory
			files = '\n'.join( os.listdir( '.' ) )
			clientSocket.send( files.encode() )
			
		elif command.startswith( "get" ):
			filename = command.split()[1] # extract filename
			if os.path.exists( filename ):
				# Generate ephemeral port for the data channel
				dataPort = get_ephemeral_port()
				clientSocket.send( str( dataPort ).encode() )	# Send port to client
				
				# Open data channel
				dataSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
				dataSocket.bind( ( '', dataPort ) )
				dataSocket.listen(1)
				dataConn, _ = dataSocket.accept()
				
				# Send file over data channel
				with open( filename, 'rb' ) as f:
					dataConn.sendfile(f)
					
				dataConn.close()    # Close data connection
				dataSocket.close()
				print( f"Sent { filename } to client" )
			else:
				clientSocket.send( b"ERROR: File not found" )
		
		elif command.startswith( 'put' ):
			filename = command.split()[1]	# Extract filename
			
			# Generate ephemeral port for receiving data
			dataPort = get_ephemeral_port()
			clientSocket.send( str( dataPort ).encode() )	# Send port to clinet

			# Open data channel
			dataSocket = socket.socket( socket.AF_INET, socket.SOCK_STREAM )
			dataSocket.bind( ( '', dataPort ) )
			dataSocket.listen(1)
			dataConn, _ = dataSocket.accept()

			# Receive file over data channel
			with open( filename, 'wb' ) as f:
				while True:
					data = dataConn.recv( 1024 )
					if not data:
						break
					f.write( data )
			
			dataConn.close()
			dataSocket.close()
			print( f"Received { filename } from client" )

		elif command == "quit":
			print( "Closeing connection with client" )
			clientSocket.close()
			break

	print( "Waiting for new connection" )
	
