## user may edit the settings on the following four lines
RSA_public_key = 3233
RSA_exponent = 17
RSA_d = 413
default_file_to_send = './website'+'/home' #default response file


import selectors
import socket
from subprocess import call
import time
import hashlib
import json
import ast
import sys



settings = {}
try:
    with open ('settings', 'r') as file:
        settingsread = file.read()
        file.close()
        print('settings file was read, read parameters follow:')
    print(settingsread)
    settingsread = ast.literal_eval(settingsread)
    #and replaces key value pairs based on settingsread
    for key in settingsread:
        settings[key] = settingsread[key]
    print ('final settings', settings)
except:
    print ('settings file reading failed, exiting after 5 seconds')
    time.sleep(5)
    sys.exit()
serverport =(settings['SELF_IP_PEER'], settings['SELF_PORT_PEER']+1)


listofpeers = [(settings['SELF_IP_PEER'], settings['SELF_PORT_PEER'])] #my peers in format [(ipaddres, port) , (ipaddres, port),...]
######################################################################################################

'''
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

print('finally list of peers', listofpeers)'''
##########################################################################################################
#timescheduled = time.time() # this is a global function called by listener
def time_elapse(interval):
    now = time.time()
    if (now - lastime) > interval:
        lastime = now
        return True
    else:
        return False


##########################################################################################################
def str2int(s):
    chars = "".join(str(n) for n in range(10)) + "bcdfghjklmpqrvwxyz"
    # we have saved the five vowels and TNS for costumization
    i = 0
    for c in reversed(s):
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
    return s


###########################################################################################################

def get_response_data_string(datastring):
    urlstring = (ast.literal_eval(datastring)).decode('utf-8')
    spliturl = urlstring.split()
    print ('\n\n\n\n spliturl', spliturl, '\n\n\n\n')
    _address_pathtofile = spliturl[1]    
    addressstring = _address_pathtofile.split('/')[1]
    print('destinationstring/addressstring', addressstring)
    
    print('we are the server!!')
    pathtofile = _address_pathtofile[len(addressstring)+1:] #(remove the starting \ from the url)
    print ('pathtofile:', pathtofile)
    print (type(pathtofile))
    try:
        with open('./website/'+pathtofile, 'r') as file:
            responsedatastring = repr(file.read().encode('utf-8'))
            file.close()
            #responsedatastring = repr(data_string.encode('utf-8'))
            print ('file read per path')
            return responsedatastring
    
    except:
        print ('could not open file requested')
        pass
    
    
    
    try:
        with open(default_file_to_send, 'r') as file:
            data_string = repr(file.read().encode('utf-8'))
            file.close()
            print('default_file_to_send being sent')
            return data_string
    except:
        data_string = 'that resource was not found on this server, even default response file could not be sent!! you should not see this message'
        responsedatastring = repr(data_string.encode('utf-8'))
        print ('default data being sent')
        return responsedatastring





    pass





def packet_to_byte (packet):
    packet_to_string = json.dumps(packet)
    packet_to_bytes = (packet_to_string).encode('utf-8')
    return (packet_to_bytes)


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



def create_signature (RSA_d, RSA_public_key, message  ):
    '''all input are integers'''
    signature = pow(message%RSA_public_key,RSA_d, RSA_public_key)
    return signature



def is_it_time(timescheduled, interval): #interval will cause the next time to be scuelded
    if timescheduled<(time.time()):
        return ((timescheduled+interval), True)
    else:
        return (timescheduled, False)

def sendbroadcast(listofpeers,peersock):
    print ('in sendbroadcast')
    broadcast_packet = {
    'destination': {'id': 0, 'routingaid' : 0 , 'connection': False, 'publickey': False}, 
    'hopcount':0 , 
    'UTC' : time.time(), 
    'version' : 1,
    'origin':{'id':RSA_public_key,'routingaid': 0, 'connection':False, 'publickey':True, 'exponent':RSA_exponent},
    'signaturebyorigin' : 0, 
    'datastring':repr('ello world'), 
    'type':'broadcast',
    'anyotherparametertosign':{}
    }
    broadcast_packet['signaturebyorigin'] = create_signature(RSA_d, RSA_public_key, hash_of(broadcast_packet))
    for peer in listofpeers:
        peersock.sendto(packet_to_byte(broadcast_packet), peer)
        print('broadcast sent')
    pass

def listener(peersock, sel):
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
    timescheduled = time.time()

    while True:

        (timescheduled, it_is_time) = is_it_time (timescheduled, 10)
        if it_is_time:
            print ('sending broadcast')
            sendbroadcast(listofpeers,peersock)

        events=sel.select(timeout=1)
        for key, mask in events:
            if key.data is "peer":
                # a peer is sending data over the adhoc network
                print ("data recieved from peer")
                print (key, mask)
                data, addr = peersock.recvfrom(1024) # buffer size is 1024bytes
                print ("received message:", data)
                packetstring=data.decode(encoding='UTF-8',errors='strict')
                packet = json.loads(packetstring)
                print ("sender:", addr)
                try:
                    if packet['destination']['id'] == RSA_public_key:
                        pass
                    else:
                        print('desinaion id is not the same as local id')
                        continue
                except:
                    print ('packet recieved was not of a format to process, no response being sent')
                    continue
                packet_processing (packet, addr) #false for foreign packet
            else:
                pass




#start listening and routing
def packet_processing(packet,addr):
     
    print (packet)




    responsetime = time.time()
    responsedestinationid = packet['origin']['id']
    responsedestinationport = packet['origin']['connection']
    
    get_response_data_string(packet['datastring'])

    try:
        responsedatastring = get_response_data_string(packet['datastring'])
    except:
        pass


    response = {
    'destination': {'id': responsedestinationid, 'routingaid' : packet['origin']['routingaid'] , 'connection': responsedestinationport, 'publickey': packet['origin']['publickey']}, 
    'hopcount':0 , 
    'UTC' : responsetime, 
    'version' : 1,
    'origin':{'id':RSA_public_key,'routingaid': 0, 'connection':False, 'publickey':True, 'exponent':RSA_exponent},
    'signaturebyorigin' : 0, 
    'datastring':responsedatastring, 
    'type':'request',
    'anyotherparametertosign':{}
    }

    hash_value = hash_of(response)
    print('hash_value', hash_value)
    calculated_signature = create_signature(RSA_d, RSA_public_key, hash_value)

    response['signaturebyorigin'] = calculated_signature

    print ('now sending response...')
    peersock.sendto(packet_to_byte(response), addr)
    print ('response sent')        

    pass





sel=selectors.DefaultSelector()
peersock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
peersock.bind(serverport)
sel.register(peersock,selectors.EVENT_READ, data="peer")

listener(peersock, sel)