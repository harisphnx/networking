import json
import socket
import struct
import sys
print "NETWORKING ASSIGNMENT\n\n"

print "enter the number of routers"
n = int(input())

###extracting source and destination IP addresses###

fp = open("ipdump.txt", "r")
fp.seek(24,0)    #if ethernet dump then 52, if ipdump 24
source = fp.read(8)
dest = fp.read(8)
i = int(source, 16)
j = int(dest, 16)
source = str(socket.inet_ntoa(struct.pack(">L", i)))
dest = str(socket.inet_ntoa(struct.pack(">L", j)))
print "Source IP: %s" %source
print "Destination IP: %s" %dest
print "\n\n"

###finding the source router###
flag = 0
for x in range(n):
	exec('with open("router' + str(x) + '.json") as f:' + '\n' + '\t' + 'router' + str(x) + '= json.load(f)')
	exec('temp = router' + str(x))
	l = len(temp)
	for y in temp:
		if(y == source):
			flag = 1
			break
if(flag == 0):
	print "not a valid source address"
	sys.exit(1)

###startine with the routing process###

count = 0
##checking destination in local network##
while(1):
	if(count > n):
		print "sorry, destination not in the network"
		sys.exit(0)
	exec('with open("router' + str(x) + '.json") as f:' + '\n' + '\t' + 'router' + str(x) + '= json.load(f)')
	exec('temp = router' + str(x))
	for y in temp:
		if(y == dest):
			print "In router: %s" %x
			print "reached through interface: " + temp[y][1]
			sys.exit(0)

	##checking destination in foreign network##
	for x1 in temp:
		mask = temp[x1][0].split('.')
		dest1 = dest.split('.')
		net_id = ""
		for j in range(4):
			w = int(mask[j])
			z = int(dest1[j])
			net_id += str(w&z)+"."
		net_id = net_id[0:len(net_id)-1]
		if(net_id == x1):
			print "In router: %s" %x
			print "going through interface: " + temp[x1][1]
			x = int(temp[x1][2])
	count = count + 1

