import json
import socket
import struct
import sys
from random import randint
print "NETWORKING ASSIGNMENT\n\n"

########################## input #########################

#n = int(input("enter the number of ports\n"))
#print router

##########################################################
#packet_number = randint(1,4)
#print "packet_number",packet_number

def crc(msg, div, code):
	msg = list(msg)
	div = list(div)
	for i in range(len(msg)-len(code)):
	        if msg[i] == '1':
			for j in range(len(div)):
				msg[i+j] = str((int(msg[i+j])+int(div[j]))%2)
	return ''.join(msg[-len(code):])	

def route_lookup(router, packet_number):
	#with open('ip_dump.json', 'r+') as f:
	#	ip_dump = json.load(f)

	eth_dump = "eth_dump" + str(packet_number) + ".txt"
	fp = open(eth_dump, "r")

	####extracting IP, ports, and flags####
	fp.seek(52 + 16,0)    #if ethernet dump then 52, if ipdump 24
	sip = fp.read(8)
	dip = fp.read(8)
	i = int(sip, 16)
	j = int(dip, 16)
	sip = str(socket.inet_ntoa(struct.pack(">L", i)))
	dip = str(socket.inet_ntoa(struct.pack(">L", j)))
	print "\n\nSource IP: %s" %sip
	print "Destination IP: %s" %dip

	if( sip == "0.0.0.0" or sip == "127.0.0.1" or sip[0:3] == "223"):
		return -1
	elif( dip == "0.0.0.0" or dip == "127.0.0.1" ):
		return -1

	with open(router, 'r+') as f:
		routing_table = json.load(f)

	routing_info = routing_table[dip]
	print "\nGoing out through port", routing_info[1],"\n"
	#### reading port numbers ####
	fp.seek(29 + 16,0)    #if ethernet dump then 29, if ipdump 1
	hlen = fp.read(1)
	dhlen = int(hlen, 16)
	dhlen=dhlen*4
	dhlen = dhlen*2

	fp.seek(dhlen + 28 + 16, 0)    #if ethernet dump then dhlen + 28, if ipdump then dhlen
	sprt=fp.read(4)
	dprt=fp.read(4)

	sprt=int(sprt, 16)
	dprt=int(dprt, 16)
	print "Source Port: %s" %sprt
	print "Destination Port: %s" %dprt
	fp.close()
	return routing_info[1]
	##############################


def packet_check(packet_number):
	eth_dump = "eth_dump" + str(packet_number) + ".txt"
	fp = open(eth_dump, "r")
	fp.seek(28 + 16,0)	
	version=int(fp.read(1),16)
	if version != 4:
		print "Invalid IP version"
		return -1
		#sys.exit()
		
	headerLen=int(fp.read(1),16)*4
	if headerLen < 20:
		print "Header length is less than 20 bytes"
		return -1
		#sys.exit()

	fp.seek(44 + 16,0)
	ttl=int(fp.read(2),16)
	if ttl < 1:
		print "Invalid packet. Discarding it"
		return -1
		#sys.exit()

	code = "00000000000000000000000000000000"
	div =  "100000000000000010000000100010111"
	fp.seek(16,0)
	msg = fp.read(116)
	msg = str(bin(int(msg, 16))[2:].zfill(116))
	crc_result = crc(msg, div, code)

	if( crc_result != "00000000000000000000000000000000" ):
		print "CRC not valid "
		return -1
	#print crc_result

	fp.close()


def classification(packet_number):
	print "\n\n"
	eth_dump = "eth_dump" + str(packet_number) + ".txt"
	fp = open(eth_dump, "r")
	fp.seek(24 + 16,0)
	ethType = int(fp.read(4))
	fp.seek(29 + 16,0)    #if ethernet dump then 29, if ipdump 1
	hlen = fp.read(1)
	dhlen = int(hlen, 16)
	dhlen=dhlen*4
	dhlen = dhlen*2
	fp.seek(dhlen + 28 + 16, 0)    #if ethernet dump then dhlen + 28, if ipdump then dhlen
	sourcePort=fp.read(4)
	sourcePort=int(sourcePort, 16)
	#print "ethtype",ethType
	if ethType == 800:
		fp.seek(46 + 16,0)
		protocol = int(fp.read(2),16)
	#	print "protocol",protocol
		if protocol == 6:
	#		print "source_port", sourcePort
			if sourcePort == 80:
				print "flow 1: IP TCP HTTP"
			elif sourcePort == 443:
				print "flow 2:IP TCP HTTPS"
			else:
				print "default flow"
		elif protocol == 11:
			if sourcePort == 80:
				print "flow 3:IP UDP HTTP"
			elif sourcePort == 443:
				print "flow 4:IP UDP HTTPS"
			else:
				print "default flow"

		elif protocol == 01:
			if sourcePort == 80:
				print "flow 5:ICMP echo reply"
			elif sourcePort == 443:
				print "flow 6:ICMP"
			else:
				print "default flow"
		else:
			print "default flow"	
	else:
		print "default flow"
	fp.close()

def init_func(packet_number, n):
	router = "router" + str(n) + ".json"

	interface_number = packet_check(packet_number)

	if(interface_number != -1):
		interface_number = route_lookup(router, packet_number)

	if( interface_number != -1):
		classification(packet_number)
	#print "interface_number", interface_number
	return interface_number

