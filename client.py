import socket
import sys
import time
from check import ip_checksum
from threading import Timer
from helper import make_packet, corrupt, isACK

host = 'localhost'
port = 8888

def timeout(s, packet):
	print 'Packet ' + str(packet[0]) + ' timeout.'
	s.sendto(packet, (host, port))
	global t
	t = Timer(1.0, timeout, [s, packet])
	t.start()

# Creating UDP socket
try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
except socket.error:
    print 'Failed to create socket'
    sys.exit()

sequence_num = 0 # Holds sequence number of current packet being sent.
expected_ack = 0 # Stores the expected sequence number to be sent though ACK from receiver.

while 1:
	# Wait for user to enter message and create a packet to send.
	message = raw_input('Enter message to send : ')    
	send_packet = make_packet(sequence_num, message);
	try:
		s.sendto(send_packet, (host, port))

	except socket.error, msg:
		print 'Error code : ' + str(msg[0]) + ' Message ' + msg[1]
		sys.exit()

	# Packet has been sent. Wait for ACK to be received.
	# Start timer for recently sent packet.
	# timerOn = False

	t = Timer(1.0, timeout, [s, send_packet])
	t.start()
	while 1:
		d = s.recvfrom(1024)
		data = d[0]
		if not corrupt(data) and isACK(data, expected_ack):
			print '(ACK: ' + data[0] + ') ' + data[1:len(data) - 2]
			if (sequence_num == 0):
				sequence_num = 1
			else:
				sequence_num = 0

			if (expected_ack == 0):
				expected_ack = 1
			else:
				expected_ack = 0
			time.sleep(.1)
			t.cancel()
			break


