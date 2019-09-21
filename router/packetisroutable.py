def packetisroutable(packet, addr, settings):
  import sys
  import hashlib
  def convert_to_byte (anything):
        import json
        #import hashlib
        anything_to_string = repr(anything)
        anything_to_bytes = (anything_to_string).encode('utf-8')
        return (anything_to_bytes)
  ''' analyzes the packet and returns either a True or False value
  based on wether is meets prespecified criteria
  '''

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
    return hashinteger

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
      hash_value = calculate_hash(packet['destination']['id'], packet['destination']['connection'], packet['datastring'], packet['UTC'])
      print('hash of message sucesffully calculated', hash_value)
      value_to_compare = hash_value%(packet['origin']['id'])
      hashthatwassigned = pow(packet['signaturebyorigin'], packet['origin']['exponent'],packet['origin']['id'])
      print ('hash that was signed :', hashthatwassigned)
      if value_to_compare!= hashthatwassigned :
        print ('signature not true')
        return True
      else:
        print('signature is true')


  except:
    return False

  pass
  return True



  

    


def hashsigned (RSA_e, RSA_public_key, signature  ):
    import hashlib
    import sys
    hashsigned = pow(signature, RSA_e, RSA_public_key)
    return hashsigned



'''
>>> m.digest_size
16
>>> m.block_size
64

More condensed:

>>> hashlib.sha224("Nobody inspects the spammish repetition").hexdigest()
'a4337bc45a8fc544c03f52dc550cd6e1e87021bc896588bd79e901e2'
>>> import hashlib
>>> m = hashlib.sha256()
>>> m.update(b"Nobody inspects")
>>> m.update(b" the spammish repetition")
>>> m.digest()
b'\x03\x1e\xdd}Ae\x15\x93\xc5\xfe\\\x00o\xa5u+7\xfd\xdf\xf7\xbcN\x84:\xa6\xaf\x0c\x95\x0fK\x94\x06'
>>> m.digest_size
32
>>> m.block_size
64

int.from_bytes(b'y\xcc\xa6\xbb', byteorder='little')
3148270713
'''
'''
def encrypt_int(message, ekey, n):
    """Encrypts a message using encryption key 'ekey', working modulo n"""

    assert_int(message, 'message')
    assert_int(ekey, 'ekey')
    assert_int(n, 'n')

    if message < 0:
        raise ValueError('Only non-negative numbers are supported')

    if message > n:
        raise OverflowError("The message %i is too long for n=%i" % (message, n))

return pow(message, ekey, n)'''
