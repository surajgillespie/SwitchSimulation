

#UDP pc program

import sys
from socket import *
from select import *
from getopt import *

sw_udp=5000
src_port=1000

opts, args = getopt(sys.argv[1:], "s:d:", ["mysrcport","switchudpport"])
for z,u in opts:
     try:
        if z == '-s':
                 src_port = int(u)
        elif z == '-d':
                 sw_udp = int(u)
        else:
                 exit()
     except:print "ERROR!\nINVALID ARGUMENTS!!"


if src_port<2000 or src_port>65535 or sw_udp < 2000 or sw_udp>65535:
        print "ERROR!\nINVALID ARGUMENTS!!"
        exit()


mysocket=src_port
switchSocket=sw_udp

# build a list of server address/port pairs


sockList = []
sockList.append(sys.stdin)

clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.bind(('127.0.0.1',mysocket));
sockList.append(clientSocket)

print "================PC READY TO RECEIVE AND SEND DATA ON PORT ",mysocket,"==========(Press Ctrl+C to terminate)====================="

print("Please input the message in the format <dst port no>,<message>\n")

def validateMessage(rmsg):
   
   try:
	msg=rmsg.split(",")
        int(msg[0])
        if(int(msg[0])>65535 or int(msg[0])<2000):
         print "Please input a port number in the range 2000-65535"
         raise Exception()
   except:
	print("ERROR!\nPlease input in the format <dst port no>,<message>")
    	return False
   print "true"
   return True


while True:
   rlist, wlist, elist = select(sockList, [], sockList)
   if not (rlist, wlist, elist):
        print "No socket ready for any operation\n"
     
    
 
   for rsock in rlist:
        if rsock == clientSocket:
            msg, serverAddr = rsock.recvfrom(2048)
	    
	    smsg=msg.split(",")
	    if(int(smsg[0])==mysocket):#discards packets if the destination is not the current listening socket
              print " received data: ", smsg[1]
	    
        if rsock == sys.stdin:
            message = raw_input('')
	    if validateMessage(message):
             clientSocket.sendto(message, ('127.0.0.1', switchSocket))
	    
	     
   

clientSocket.close()
