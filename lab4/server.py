import socket
import sys
from thread import *

HOST = '' #Symoblic name meaning all available interfaces
PORT = 8888 #Arbitrary non-priviledged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print 'Socket created'
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

try:
	s.bind((HOST, PORT))
except socket.error, msg:
	print 'Bind failed. Error code : ' + str(msg[0]) + ' Message ' + msg[1]
	sys.exit()

print 'Socket bind complete'	

s.listen(10)
print 'Socket now listening'

def sendtoconnections(reply):
	for c in connections:
		c.sendall(reply)
	

# Function for handling connections. This will be used to create threads.
def clientthread(conn):
	#Sending message to connected client
	conn.send('Welcome to the server. Type something and hit enter\n') #send only takes strings

	#infinite loop so that function ddoes not terminate and do not end
	while True:
		#Receiving from client
		data = conn.recv(1024)
		if data[0:2] == '!q':
			break
		elif data[0:8] == '!sendall':
			reply = data[9:]
			sendtoconnections(reply)
		else:
			reply = 'OK... ' + data
			if not data:
				break
			conn.sendall(reply)

	#came out of loop
	connections.remove(conn)
	conn.close()

connections = []

while 1:
	#wait to accept a connection - blocking call
	conn, addr = s.accept()
	connections.append(conn)
	#display client information
	print 'Connected with ' + addr[0] + ':' + str(addr[1])

	#start new thread takes 1st argument as a function name to be run, second is the tuple of arguments to the function.
	start_new_thread(clientthread, (conn,))

s.close()
