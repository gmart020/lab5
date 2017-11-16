import socket
import sys
from check import ip_checksum
from helper import make_packet, corrupt, isACK
from time import sleep

HOST = ''
PORT = 8888

sequence_num = 0
expected_ack = 0
message_count = 0

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print 'Socket created'
except socket.error, msg:
    print 'Failed to create socket. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

try:
    s.bind((HOST, PORT))
except socket.error, msg:
    print 'Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1]
    sys.exit()

print 'Socket bind complete'

while 1:
	d = s.recvfrom(1024)
	data = d[0]
	addr = d[1]

	if not data:
		break
	
	if message_count == 1:
		data = data + 'a'

	seq = data[0]
	message = data[1:len(data) - 2]
	checksum = data[len(data) - 2:]

	reply = 'OK...' + message
	#temp
	message_count += 1

	if (not corrupt(data)) and isACK(data, expected_ack):
		print 'Message[' + addr[0] + ':' + str(addr[1]) + '] - ' + '(SEQ: ' + str(seq) + ') '  + message.strip()
	
		if message_count == 4:
			sleep(4.5)

		packet = make_packet(sequence_num, reply)
		s.sendto(packet, addr)
		if sequence_num == 0:
			sequence_num = 1
			expected_ack = 1
		else:
			sequence_num = 0
			expected_ack = 0
			

	elif not isACK(data, expected_ack):
		print 'Incorrect packet recieved. Deleting'

	else:
		print 'Received packet corrupted. Deleting.'

s.close()
