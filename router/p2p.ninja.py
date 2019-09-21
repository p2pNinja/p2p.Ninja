#inbuiltfunctions
import random
import selectors
import socket
import types
from operator import itemgetter, attrgetter #(for sorting through the routing table)
import hashlib #hashes
import pickle
import json
import time
import ast
import sys
#from zipfile import ZipFile

#myfunc
from broadcast import *
from settingspage import *
from amend_routing_tables import *
#from change_server_settings import *


import os
try:
    os.remove('kill')
except:
    pass

def keep_alive():
    try:
        with open('kill', 'r') as file:
            print ('kill file found , keep alive is now going to be false')
            return False
    except:
        return True
    


def openports(self_ip_peer,self_port_peer,TCP_IP,TCP_PORT,sel):
    '''first argument is an ip address, second argument is a port number, a UDP connection will be opened here
    third argument is ip address, forth argument is a port usually 80, a TCP IP connection will be opened here
    these connection will be registered with sel for reading. this function will change ip address over
    '''
    import selectors
    import socket
    from subprocess import call
    print ('you are in the openports module')
    try:
        call(["ifconfig", "wlan0", self_ip_peer]) #change ip address of wlan0
        print('there was success in changing wlan0 to self_ip_peer of your settings')
    except:
        print('there was an exception raised in the call ifconfig wlan0 command')
        pass


    #for other pi over adhoc network, establish UDP connection
    peersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        print ('Ref: UDP will try to bind to', (self_ip_peer, self_port_peer))
        peersock.bind((self_ip_peer, self_port_peer))
        print ('success in binding as above')
    except:
        peersock.bind(('127.0.0.1', 5005))
        print ('could not open port at requested ip addres and port for peers, default used :127.0.0.1, 5005 ')
    finally:
                peersock.setblocking(False)
                sel.register(peersock,selectors.EVENT_READ, data="peer")

    #for cilent facing ethernet port, open TCPIP port
    client=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.bind((TCP_IP, TCP_PORT))
    client.listen(100)
    client.setblocking(False)
    sel.register(client, selectors.EVENT_READ, data="client")
    print('TCPIP connection opened succesfully returning from openports')
    return (peersock, client, sel)

    # read the local id file for this pi's unique identifier.
    #with open(localid) as fp:
     #       localid= fp.readline() #reads the local id as the top line from the file localid
     #   print("local id from routing", localid)



    return True

####################################################################################
def str2int(s):
    chars = "".join(str(n) for n in range(10)) + "bcdfghjklmpqrvwxyz"
    # we have saved the five vowels and TNS for costumization
    i = 0
    print(chars)
    for c in (s):
        if c in chars:
            i *= len(chars)
            i += chars.index(c)
        else:
            pass
    return i

def int2str(i):
    chars = "".join(str(n) for n in range(10)) + "bcdfghjklmpqrvwxyz"
    # we have saved the five vowels and TNS for costumization
    s = ""
    while i:
        s += chars[i % len(chars)]
        i //= len(chars)
    string = s[::-1]
    return (string)


#chars = "".join(str(n) for n in range(10)) + "bcdfghjklmpqrvwxyz"

#####################################################################################
def packetisroutable(packet, addr, settings):
  '''import sys
  import hashlib
  def convert_to_byte (anything):
        import json
        #import hashlib
        anything_to_string = repr(anything)
        anything_to_bytes = (anything_to_string).encode('utf-8')
        return (anything_to_bytes)
  
  

  def calculate_hash(*message):
    def convert_to_byte (anything):
        import json
        #import hashlib
        anything_to_string = repr(anything)
        anything_to_bytes = (anything_to_string).encode('utf-8')
        return (anything_to_bytes)
    m = hashlib.sha256()
    for item in message:
        m.update(convert_to_byte(message))
    hashvalue = m.digest()
    hashinteger=int.from_bytes(hashvalue, byteorder=sys.byteorder) 
    print ('hashinteger', hashinteger)
    return hashinteger'''

  print ('packet recieved in packetisroutable to test for integrity')
  try:

    
    if packet['hopcount'] > settings['ACCEPTABLEHOPCOUNT'] :
      print('too much hops')
      return False
      
    if packet['hopcount'] < 0:
      print('too little hops')
      return False

    if sys.getsizeof(packet)>settings['ACCEPTABLEROUTINGPACKETSIZE']:
      print ('too big size')
      return False 

    if packet['type'] is 'broadcast':
      if sys.getsizeof(packet)>settings['ACCEPTABLEBROADCASTPACKETSIZE']:
        return False

    #if not packet.['destination'] & packet.['UTC'] & packet.['version'] & packet.['origin'] & packet.['type']:
     # return False

    #if packet.['UTC'] + TIMEDELAYACCEPTABLE < time.time:
     # pass

    print ('testing for signature follows:')


    if packet['origin']['publickey'] is True:
      hash_value = hash_of(packet)
      print('hash of message sucesffully calculated', hash_value)
      value_to_compare = hash_value%(packet['origin']['id'])
      hashthatwassigned = pow(packet['signaturebyorigin'], packet['origin']['exponent'],packet['origin']['id'])
      print ('hash that was signed :', hashthatwassigned)
      if value_to_compare!= hashthatwassigned :
        print ('signature not true')
        return False
      else:
        print('signature is true')


  except:
    return False

  pass
  return True



  


###############################################################################
def convert_to_byte (anything):
    anything_to_string = json.dumps(anything)
    anything_to_bytes = (anything_to_string).encode('utf-8')
    return (anything_to_bytes)

#######################################################################

def packet_dict_to_byte (packet_dict):
    packet_to_string = json.dumps(packet_dict)
    packet_byte = (packet_to_string).encode('utf-8')
    return (packet_byte) #data

def packet_byte_to_dict(packet_byte):
    data_to_string = packet_byte.decode('utf-8')
    packet_dict = json.loads(data_to_string)
    return (packet_dict) # data/bytes


def databyte_to_datastring(databyte):
    return (repr(databyte))


def datastring_to_databyte(datastring):
    return(ast.literal_eval(datastring))
#############################################################################



def hash_of(packet):
    
    def byte_of(anything):
        anything_to_string = json.dumps(anything, sort_keys=True)
        anything_to_bytes = (anything_to_string).encode('utf-8')
        return (anything_to_bytes)
    
    #import hashlib
    #import sys
    m = hashlib.sha256()
    parameters =['destination', 'UTC', 'origin', 'datastring', 'anyotherparametertosign']
    for parameter in parameters:
        m.update(byte_of(packet[parameter]))
    hashvalue = m.digest()
    hashinteger=int.from_bytes(hashvalue, byteorder=sys.byteorder) 
    print ('hashinteger reported from the hash_of function:', hashinteger)
    return hashinteger


#######################################################################################################


def datapacker (urlinfo, tcpipconn, settings): #urlinfo is bytes data type sent by the browser originally, tcpipconn is where responses can be sent to the browser back.
    '''this function converts the URL request from the client browser into a 'packet' that can be routed by p2p.Ninja'''
    print ("datapacker activated")
    urlinfobytes=urlinfo
    urlinfostr=urlinfobytes.decode(encoding='UTF-8', errors='backslashreplace')
    '''see protocol documentation'''
    print ('recieved the following url that was converted to a string', urlinfostr)
    urlbroken=urlinfostr.split('/')
    destination_type_routingaid_etc=urlbroken[1]
    print ("listof_destination_type_routingaid_etc:", destination_type_routingaid_etc)
    #[destinationid, routingaid, packettype] = destination_type_routingaid_etc.split(.)
    if destination_type_routingaid_etc.split('.')[0] == 'settings':
        destinationid = 'settings'
        print ('destination id is settings')
    else:
        destinationid = str2int(destination_type_routingaid_etc.split('.')[0])
        print ('destinationid succesfullyset', destinationid)

    try:
        packettype = destination_type_routingaid_etc.split('.')[1]
    except:
        print('no packet type, will set to request')
        packettype = 'request'

    try:
        routingaid = destination_type_routingaid_etc.split('.')[2]
    except:
        print ('no routing aid, will set to 0')
        routingaid = '0'
    
    if destination_type_routingaid_etc.split('.')[0][0] == '~': # if initial character in webadddress/destination string is ~, destination is a non cryptographic key
        publickey = False
    else:
        publickey = True

    #calculate senders signature if able
    packet_dict ={'destination': {'id':destinationid, 'routingaid' :routingaid , 'connection' : False , 'publickey': publickey}, 
    'hopcount':0, 
    'UTC' : time.time()+settings['referernce_minus_local_time'], 
    'version' : settings['VERSION'], 
    'origin':{'id':settings['LOCALID'], 'routingaid':settings['LOCALROUTINGAID'], 'connection':repr(tcpipconn), 'publickey':settings['LOCALIDPUBLICKEY'], 
                            'exponent':settings['LOCALKEYEXPONENT']}, 
    'signaturebyorigin' : 0, 
    'datastring':repr(urlinfo), 
    'type':packettype ,
    'anyotherparametertosign':{}
    }
    #print ('####################################################yellow there, trying to reprocess the tcipipconn!!!!!!')
    #connection = eval(repr(tcpipconn))
    #tcpipconn.sendall(b'serialisation works')

    
    print ('datapacking done, will return packet_dict as follows' , packet_dict)
    return (packet_dict, tcpipconn)
     
    
    
################################################################################################



def listener(peersock, client, sel, settings, unsigned_routing_dict, 
                                                      signed_routing_dict, unsigned_destination_list, signed_destination_list):
    '''this function expects two open connections as input arguments. the first argument is expectd to be a UDP connection
    the second argument is a TCPIP connection
    this function listens on both these connections. sel is the selectors function to which these connections are already registered.
    
    output is of format (packet, addr, True/False)
    any data recieved from the first arugment connection is decoded and returned as packet.
    on the second (client) argument connection, it accepts connectsion and recieves URL requests. it then sends this URL request to 
    function 'datapacker' for conversion inot a packet and then returns the 'packet'.
    it also returns a second arguemnt (addr) which represents the connection from which this function recieved the packet/data
    the third parameter (true/False) advises if the packet was generated locally

    
    '''
    loopcounter = 0
    print (' in listener function. loopcounter set to 0...')
    while keep_alive():
        #loopc +=1

        events=sel.select(timeout=1)

        for key, mask in events:
            if key.data is "peer":
                # a peer is sending data over the adhoc network
                loopcounter +=1
                loopcounter = loopcounter%100000
                print (' in listener, key.data is peer____________________________________________________________________________________')
                print ('loop counter (resets after 100k):', loopcounter)
                print ("packet recieved from peer")
                print (key, mask)
                try:
                    packet_byte, addr = peersock.recvfrom(settings['ACCEPTABLEROUTINGPACKETSIZE']+100) # buffer size is 1024bytes
                    print ("received message:", packet_byte)
                except Exception as e:
                    print(e)
                    print("message was not reiceved exception raised when trying to read peersock")
                    continue
                #packetstring=data.decode(encoding='UTF-8',errors='strict')
                #packet = json.loads(packetstring)
                print ("sender:", addr)
                data_or_packet_processor (packet_byte, addr, False, unsigned_routing_dict, 
                                                     signed_routing_dict, unsigned_destination_list, signed_destination_list, settings) #false for foreign packet
                pass
            if key.data is "client":
                #client computer is requesting connection over http:
                loopcounter +=1
                loopcounter = loopcounter%100000
                print (' in listener, key.data is client____________________________________________________________________________________')
                print ('loop counter (resets after 100k):', loopcounter)
                print ("connection request on port 80 by client")
                print (key.fileobj)
                print (key, mask)
                conn, addr = key.fileobj.accept()
                conn.setblocking(False)
                print ("connection accepted follows",conn, addr)
                print (" ")
                print (" ")
                print (" ")
                data=types.SimpleNamespace(addr=addr, inb=b'',outb=b'')
                sel.register(conn, selectors.EVENT_READ, data="service")
            if key.data is "service":
                loopcounter +=1
                loopcounter = loopcounter%100000
                print (' in listener, key.data is service____________________________________________________________________________________')
                print ('loop counter (resets after 100k):', loopcounter)
                # client computer is sending url request
                data_byte=key.fileobj.recv(10480000) #url request
                #packet=data.decode(encoding='UTF-8', errors='strict') #just to keep term packet alwasy decoded as abvoe
                if data:
                    print ("received as follows (will forward to data_or_packet_processor:\n", data_byte, key.fileobj)
                    data_or_packet_processor (data_byte, key.fileobj, True, unsigned_routing_dict, 
                                                      signed_routing_dict, unsigned_destination_list, signed_destination_list, settings)
                    
                    #key.fileobj.sendall(data)
                    #key.fileobj.close()
                    #sel.unregister(key.fileobj)
                else:
                    # client has send a connection close request
                    key.fileobj.close()
                    sel.unregister(key.fileobj)
            else:
                pass
            
            
                #sel.register(conn, selectors.EVENT_READ, data="connected")
                
###########################################################################################################
            




def routing2peers (packet_dict, whereitcamefrom, unsigned_routing_dict, signed_routing_dict, 
                     unsigned_destination_list, signed_destination_list,listofpeers, peersock):

    #recieved packetforrouting should be a decoded dictionary of the format {'destinationid': destination, 'isdestinationidapublickey': 1, 'hopcount'=1, 'UTC' = 'time', 'version' = 1,
    # 'originid'= localid,'isoriginidapublickey?' = 0, 
                     #  'signaturebysender' = 0, 'data'=urlinfobytes, 'clientport'=tcpipconn}
                         #'data' is always bytes types. if the originid is a cryptographic public key, set isoriginidapublickey? to 1 and give signature value
    # destination can be a public key or random number by a previous sender to get responses. if destintionid is publick key address, isdestinationidapublickey is set to 1, else 0
    #router will use destination value to route
  print ('routing2peers')
  packet_byte = packet_dict_to_byte(packet_dict)
  destinationid = packet_dict['destination']['id']

  if packet_dict['destination']['publickey'] & (destinationid in signed_destination_list): #destination is in the routing table.
    peer_IP_PORT = signed_routing_dict[destinationid]['peer']
    peersock.sendto(packet_byte, peer_IP_PORT)
    print ('packet_dict sent to:', peer_IP_PORT)
    return

  if packet_dict['destination']['publickey'] == False and destinationid in unsigned_destination_list:
    peer_IP_PORT = unsigned_routing_dict[destinationid]['peer']
    peersock.sendto(packet_byte, peer_IP_PORT)
    print ('packet_dict sent to:', peer_IP_PORT)
    return

  # packet is unroutable
  templist=listofpeers
  try:
    templist.remove(whereitcamefrom) #dont send it back!
  except:
    pass
  print('you are in routing2peers and there was no routing table to help')
  print('templist',templist,'listofpeers',listofpeers)
  peer_IP_PORT = random.choice(listofpeers)   ################# needs fixing!!!!
  print ('peer_IP_PORT:', peer_IP_PORT)
  try:
    peersock.sendto(packet_byte, peer_IP_PORT)
    print ('packet_dict sent to:', peer_IP_PORT) 
  except:
    pass
  return
      
      
########################################################################################################


def route2client(packet_dict):
    #recieved packetforrouting should be a decoded dictionary of the format {'destinationid': destination, 'isdestinationidapublickey': 1, 'hopcount'=1, 'UTC' = 'time', 'version' = 1,
    # 'originid'= localid,'isoriginidapublickey?' = 0, 
                     #  'signaturebysender' = 0, 'data'=urlinfobytes, 'clientport'=tcpipconn , 'packettype'=somenumber to indicate what this is}
                         #'data' is always bytes types. if the originid is a cryptographic public key, set isoriginidapublickey? to 1 and give signature value
    # destination can be a public key or random number by a previous sender to get responses. if destintionid is publick key address, isdestinationidapublickey is set to 1, else 0
    #router will use destination value to route
    print ('route2client activated')
    if True:
        data_bytes = ast.literal_eval(packet_dict['datastring'])
        #this datapakcet is a response to our client's prior request
        #we will now snd the 'data' in the packetforouting to the 'clientport' and close the open connection
        (destination_port, expectedoriginid, public_key_expected) = dict_of_openconnectionsTCP_IP[packet_dict['destination']['connection']]  
        #list_of_openconnectionsTCP_IP.remove(destination_port)
        #dict_of_openconnectionsTCP_IP.pop(destination_port)
        destination_port.sendall(data_bytes) 
        destination_port.close()
        sel.unregister(destination_port)
        print (data_bytes, '\n\n were sent to \n\n ', destination_port)
    else:
        print ('in route2client function , the following was recieved \n\n', packet_dict, ' \n\n could not be converted to data_bytes or destination port could not be accessed will return' )
        #this data packet needs to be routed
        #routing2peers(packetforouting, wherewerecievedpacketfrom, unsigned_routing_dict, signed_routing_dict, unsigned_destination_list, signed_destination_list,listofpeers, peersock)
        pass
    
    return True
    #need to use signature infomratin to build routing table.


#########################################################################################################################################################
def data_or_packet_processor(data_or_packet_bytes, returnaddr, TCPIPcommunication, unsigned_routing_dict, 
                                                      signed_routing_dict, unsigned_destination_list, signed_destination_list, settings): #called by listening function
    #loopcounter +=1
    #loopcounter = loopcounter%100000
    print ('in data_or_packet_processor')
    #print ('loop counter (resets after 100k):', loopcounter)
    
    #(data_or_packet_bytes, returnaddr, TCPIPcommunication) = listener(peersock, clientsock, sel, settings) 
    if TCPIPcommunication: # packetordata is actually a byte type client request and not a preformed packet
        try:
            data_bytes = data_or_packet_bytes
            (packet_dict, returnaddr) = datapacker(data_bytes, returnaddr, settings)
            print('back in data_or_packet_processor, will attempt to append to list_of_openconnectionsTCP_IP')
            list_of_openconnectionsTCP_IP.append(repr(returnaddr))
            dict_of_openconnectionsTCP_IP[repr(returnaddr)] = (returnaddr, packet_dict['destination']['id'], packet_dict['destination']['publickey'])
            print('list of open TCIPIP connections:',list_of_openconnectionsTCP_IP,'dict of open TCPIP connections', dict_of_openconnectionsTCP_IP)
            packetislocal = True #packet was formed from data sent by our client
        except:
            print('packaging of data failed, or list_of_openconnectionsTCP_IP not amended',data_bytes, returnaddr)
            response = ('your URL request could not be processed by the p2p.Ninja router. please check your url:').encode(encoding='UTF-8')
            returnaddr.sendall(response)
            returnaddr.sendall(data_bytes)
            returnaddr.close()
            sel.unregister(returnaddr)
            return
    else: #data_or_packet_bytees is a packet in bytes format from a peer
        packet_byte = data_or_packet_bytes
        packet_dict = packet_byte_to_dict(packet_byte)
        packetislocal = False #packet came from the peer network over mesh
    print ('packetislocal', packetislocal)
        


    if not (packetislocal or packetisroutable(packet_dict,returnaddr, settings)):
        print('not (packetislocal or packetisroutable(packet_dict,returnaddr, settings)), return')
        return
    
    (packet_dict, returnaddr, unsigned_routing_dict, signed_routing_dict, unsigned_destination_list, signed_destination_list) = amend_routing_tables(packet_dict, returnaddr, unsigned_routing_dict, 
                                                      signed_routing_dict, unsigned_destination_list, signed_destination_list, settings) #builds the routing table

    print ('reporting from the data_or_packet_processor function final tables:\n', 'unsigned_routing_dict:\n', unsigned_routing_dict, 'signed_routing_dict:\n',signed_routing_dict, 
            'unsigned_destination_list:\n', unsigned_destination_list, 'signed_destination_list:\n ', signed_destination_list )

    packet_dict['hopcount'] += 1

    if packet_dict['destination']['id']==settings['LOCALID']: #this datapakcet is a response to our client's prior request
        print ('packet_dictdestinationid==settings[LOCALID]:this datapakcet is a response to our clients prior request')
        #check our dictionary to see if origin of packet is the same from whom data was initially requested
        try:
            (destination_port, expectedoriginid, public_key_expected) = dict_of_openconnectionsTCP_IP[packet_dict['destination']['connection']] 
            print ('expectedoriginid:  ',expectedoriginid)
            print (packet_dict['origin']['id'])
        except:
            print('although destination id ==settings[localid], packet_dict[destination][connection] was not found in dict_of_openconnectionsTCP_IP. this packet will be discarded. will return to listener from data_or_packet processor')
            return
        if expectedoriginid != packet_dict['origin']['id']:
            print ('there was an attempt to access a port by a service that was not requested')
            return
        if (packet_dict['origin']['publickey'] is not True) and (public_key_expected):
            print ('unsigned data recieved, only signed packet acceptable. will return')
            return
        route2client(packet_dict)
        destination_port = packet_dict['destination']['connection']
        print (destination_port, '- the preceding will be removed from TCPIP list and dict')
        list_of_openconnectionsTCP_IP.remove(destination_port)
        dict_of_openconnectionsTCP_IP.pop(destination_port)
        return
    
    
    
    if packet_dict['type'] == 'broadcast':
        print ('packet_dict[type] is broadcast')
        broadcast(packet_byte, returnaddr, listofpeers, peersock)
        return
    

    if not (packet_dict['destination']['id']=='settings'): #if the packet has not already been routed to client, it needs to be routed to peers unless it is for settings.
        print('packet destined for routing2peers')
        routing2peers(packet_dict,returnaddr,unsigned_routing_dict, signed_routing_dict, unsigned_destination_list, signed_destination_list, listofpeers, peersock)
        return


    if packetislocal & (packet_dict['destination']['id']=='settings'):
        print ('this packet is a local settings page request')
        try:
            settings = settingspage(packet_dict,returnaddr,sel,settings,listofpeers) #update settings based on packet data
        except Exception as e: 
            print(e)
            try:
                response = ('your settings request could not be processed by the settings module').encode('UTF-8')
                returnaddr.sendall(response)
                returnaddr.close()
                sel.unregister(returnaddr)
            except:
                returnaddr.close()
                sel.unregister(returnaddr)
        finally:
            os.chdir(cwd) # get back to current workin directory
        if True:
            return
#####################################################################################################################################
     


###############################################################################################################
# FOLLOWING IS THE LOADING OF SETTINGS, AND ROUTING TABLES

import os
cwd = os.getcwd()


print('Thank you for using p2p.Ninja for your peer to peer networking needs')
print('will load default settings...')








#default settngs
settings = {'SELF_IP_PEER':"192.168.2.40", 
    'SELF_PORT_PEER' : 5005,
    'TCP_IP' : "192.168.1.40", 
    'TCP_PORT' : 80,
    'LOCALID' : 349845934857984923840, 
    'LOCALROUTINGAID' : '100as701' ,
    'LOCALIDPUBLICKEY':0,
    'LOCALKEYEXPONENT':0,
    'ACCEPTABLEHOPCOUNT':4,
    'NUMBEROFKEYSTOSAVE':1000,
    'MINIMUMINTERVALBETWEENBROADCASTS' : 10,
    'NUMBEROFCONNECTIONSTOSAVE':10,
    'ACCEPTABLEROUTINGPACKETSIZE':2000,
    'ACCEPTABLEBROADCASTPACKETSIZE' : 100,
    'TIMEDELAYACCEPTABLE' : 20,
    'VERSION' : 1,
    'referernce_minus_local_time': 0}



print ('will read settings file for additional/revised settings')
#following reads the settings from file settings
import os
os.chdir(os.path.dirname(os.getcwd())) #step up one folder . and dont forget to comeback
try:
    with open ('settings', 'r') as file:
        settingsread = file.read()
        file.close()
        print('settings file was read, read parameters follow:')
    print(settingsread)
    settingsread = json.loads(settingsread)
    #and replaces key value pairs based on settingsread
    for key in settingsread:
        settings[key] = settingsread[key]
    print ('final settings: ', settings)
except:
    print ('settings file reading failed')
    settings = {'SELF_IP_PEER':"192.168.2.40",
    'SELF_PORT_PEER' : 5005, 
    'TCP_IP' : "192.168.1.40", 
    'TCP_PORT' : 80,
    'LOCALID' : 349845934857984923840, 
    'LOCALROUTINGAID' : '100as701' ,
    'LOCALIDPUBLICKEY':0,
    'LOCALKEYEXPONENT':0,
    'ACCEPTABLEHOPCOUNT':4,
    'NUMBEROFKEYSTOSAVE':1000,
    'MINIMUMINTERVALBETWEENBROADCASTS' : 10,
    'NUMBEROFCONNECTIONSTOSAVE':10,
    'ACCEPTABLEROUTINGPACKETSIZE':2000,
    'ACCEPTABLEBROADCASTPACKETSIZE' : 100,
    'TIMEDELAYACCEPTABLE' : 20,
    'VERSION' : 1}
    print('settings:',settings)




#######


###########

listofpeers = [('127.0.0.1', 5700)] #my peers in format [(ipaddres, port) , (ipaddres, port),...]

print('will try to read file listofpeers')
try:
    with open ('listofpeers', 'r') as file:
        peersread = file.read()
        file.close()
    print('list of peers file read as follows',peersread)
    listofpeers.extend(ast.literal_eval(peersread))
except:
    print ('peers file not loaded. only default peer exists')
    #print ('list of peers', listofpeers)

print('finally list of peers', listofpeers)


os.chdir('./router') #come back to this directory
#########################

unsigned_routing_dict={}
print('attempting to read unsigned_routing_dict...')
try:
    with open ('unsigned_routing_dict', 'r') as file:
        unsigned_routing_dictread = file.read()
        file.close()
    print('unsigned_routing_dict read as follows:',unsigned_routing_dictread)
    print('attempting to load unsigned_routing_dict')
    unsigned_routing_dict = ast.literal_eval(unsigned_routing_dictread)
except:
    unsigned_routing_dict={}
    print ('unsigned_routing_dict file not loaded. only default dict exists')
    
print('final unsigned_routing_dict', unsigned_routing_dict)


######################################

signed_routing_dict = {}
print('attempting to read signed_routing_dict...')

try:
    with open ('signed_routing_dict', 'r') as file:
        signed_routing_dictread = file.read()
        file.close()
    print('signed_routing_dict read as follows:', signed_routing_dictread)
    print('attempting to load signed_routing_dict..')
    signed_routing_dict = ast.literal_eval(signed_routing_dictread)
except:
    print ('signed_routing_dict file not loaded. only default dict exists')
    signed_routing_dict={}

print('final signed_routing_dict', signed_routing_dict)
###########################

unsigned_destination_list = []
print('attempting to read unsigned_destination_list...')
try:
    with open ('unsigned_destination_list', 'r') as file:
        unsigned_destination_listread = file.read()
        file.close()
    print('unsigned_destination_list was read as follows', unsigned_destination_listread, 'attempt to load unsigned_destination_list')
    unsigned_destination_list = ast.literal_eval(unsigned_destination_listread)
except:
    print ('unsigned_destination_list file not loaded. only default list exists')
    
print('final unsigned_routing_dict', unsigned_routing_dict)

##########################
signed_destination_list = []
print('attempting to read signed_destination_list')
try:
    with open ('signed_destination_list', 'r') as file:
        signed_destination_listread = file.read()
        file.close()
    print('signed_destination_list read as follows:', signed_destination_listread)
    print ('attempting to load signed_destination_list')
    signed_destination_list = ast.literal_eval(signed_destination_listread)
    print('success')
except:
    print ('signed_destination_list file not loaded. only default list exists')
    
print('final signed_routing_dict', signed_routing_dict)

########################

savedhashes = []

# the following are for use in the datapacker and route functions.
list_of_openconnectionsTCP_IP = [] #list of connections that have been opened with the clients
dict_of_openconnectionsTCP_IP = {}

########

#THE MAIN LOOP FOLLOWS SHORTLY


#open connections and routing tables:
sel=selectors.DefaultSelector()
print('will attmept to open connections, initiating openports function')
(peersock, clientsock, sel)=openports(settings['SELF_IP_PEER'],settings['SELF_PORT_PEER'],settings['TCP_IP'],settings['TCP_PORT'], sel) 
print('ports opened succesfully , entering main loop of p2p.Ninja, Thank you again.')

loopcounter=0
#start listening and routpng


    
listener(peersock, clientsock, sel, settings, unsigned_routing_dict, 
                                                      signed_routing_dict, unsigned_destination_list, signed_destination_list)

peersock.close()
clientsock.close()

