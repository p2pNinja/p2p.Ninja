'''this function will establish connections on both wired and wireless IP addresses at ports as previously defined, read local id from file'''


'''Here's a way to get the IP address without using a python package:

import socket
import fcntl
import struct

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return socket.inet_ntoa(fcntl.ioctl(
        s.fileno(),
        0x8915,  # SIOCGIFADDR
        struct.pack('256s', ifname[:15])
    )[20:24])

get_ip_address('eth0')  # '192.168.0.110'
'''


def openports(self_ip_peer,self_port_peer,TCP_IP,TCP_PORT,sel):
	'''first argument is an ip address, second argument is a port number, a UDP connection will be opened here
	third argument is ip address, forth argument is a port usually 80, a TCP IP connection will be opened here
	these connection will be registered with sel for reading. this function will change ip address over
	'''
	import selectors
	import socket
	from subprocess import call
	try:
		call(["ifconfig", "wlan0", self_ip_peer]) #change ip address of wlan0
	except:
		pass


	#for other pi over adhoc network, establish UDP connection
	peersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	try:
		print ((self_ip_peer, self_port_peer))

		peersock.bind((self_ip_peer, self_port_peer))
	except:
		peersock.bind(('127.0.0.1', 5005))
		print ('could not open port at requested ip addres and port for peers, default used :192.168.2.40, 5005 ')
	finally:
                peersock.setblocking(False)
                sel.register(peersock,selectors.EVENT_READ, data="peer")

	#for cilent facing ethernet port, open TCPIP port
	client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	client.bind((TCP_IP, TCP_PORT))
	client.listen(100)
	client.setblocking(False)
	sel.register(client, selectors.EVENT_READ, data="client")
	return (peersock, client, sel)

	# read the local id file for this pi's unique identifier.
	#with open(localid) as fp:
	 #       localid= fp.readline() #reads the local id as the top line from the file localid
	 #   print("local id from routing", localid)



	return True
