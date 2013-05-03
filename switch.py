

#UDP switch program
import sys
from socket import *
from select import *
from getopt import *

ports=[];
src_port=10000
opts, args = getopt(sys.argv[1:], "s:p:", ["mysrcport","ports"])
for z,u in opts:
     try:
        if z == '-s':
		 
                 src_port = int(u)
        elif z == '-p':
		 print "port"
                 slist = u.split(",")
		 if len(slist)>8:
		  print "Max of 8 ports only"
		  raise Exception() 

		 for i in slist:
			
			if(int(i)<2000 or int(i)>65535):
			
			 raise Exception()
			
			ports.append(int(i))
			
			
 
        else: 
	
		exit()
     except:
	    print "ERROR!\nINVALID ARGUMENTS!!"
	    exit()


if src_port<2000 or src_port>65535:
	print "ERROR!\nINVALID ARGUMENTS!!"
	exit()

serverName = ''
socketList = []
print "done"
newsock = socket(AF_INET, SOCK_DGRAM)
newsock.bind(('127.0.0.1', src_port))
socketList.append(newsock)


switchTable=[];
ports=[4000,5000,6000];

def validateMessage(msg): 
 try:
  	int(msg[0])
  	if(int(msg[0])>65535 or int(msg[0])<2000):
   	 print "Please input a port number in the range 2000-65535"
   	 raise Exception()
 except:
  	return False
 
 return True


def checkSwitchTable(table,val):#to check if the passed port no is there in the switch table 
    
     for i in table:
        if i==val:           
            return True
        
     return False


count=0
flag=0

print "================UDP SERVER READY TO RECEIVE DATA==========(Press Ctrl+C to terminate)====================="
while 1:
    rlist, wlist, elist = select(socketList, [], socketList, 10)
    if not (rlist, wlist, elist):
        print "select() call timeout after ", timeout, " seconds"
    for rsock in rlist:
       message, clientAddr = rsock.recvfrom(2048)
       try:
        print "From ", clientAddr, ", Received data: ", message
        respMsg = message.split(",");
        
        if validateMessage(respMsg):
		if(checkSwitchTable(switchTable,int(clientAddr[1]))):
		 print ""
		else:	
		 switchTable.append(int(clientAddr[1]))
		 count+=1
		 print "Switch Table Updated"
		 print "---------------------"	
		 c=1
		 for k in switchTable:
			 print c," ",k,"\n" 
			 c+=1
		 print "---------------------"
		    
                
        	if(checkSwitchTable(switchTable,int(respMsg[0]))):#if switch table entry is already there, then switch can forward directly
                 print("direct sending")
        	 rsock.sendto(message,('127.0.0.1',int(respMsg[0])))
		else:
		 index=0#used to prevent switch from broadcasting to the sender
		 for i in ports:
		   if((i!=int(clientAddr[1]))):		  
                      print("sending broadcast message to ", ports[index]) 
                      rsock.sendto(message,('127.0.0.1',ports[index]))
		   index+=1
 
  
        else:
	 print("ERROR!\nPlease input in the format <dst port no>,<message>")
       except:print("ERROR!\nPlease input in the format <dst port no>,<message>")
				
     


