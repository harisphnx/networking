mport json
import socket
import struct
import sys
print "NETWORKING ASSIGNMENT\n\n"

print "enter the number of routers"
n = int(input())

fp = open("ipdump.txt", "r")
fp.seek(24,0) #skipping the dest and the source mac address
mac_type = fp.read(4)


