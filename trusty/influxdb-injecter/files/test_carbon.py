#!/usr/bin/env python
import socket
import time
import random
import sys
 
CARBON_SERVER = sys.argv[1]
CARBON_PORT = long(sys.argv[2])
SERIES = sys.argv[3]
 
while True:
        message = '%s %d %d\n' % (SERIES, random.randint(1,20),int(time.time()))
        print 'sending message:\n%s' % message
        sock = socket.socket()
        sock.connect((CARBON_SERVER, CARBON_PORT))
        sock.sendall(message)
        time.sleep(1)
        sock.close()
