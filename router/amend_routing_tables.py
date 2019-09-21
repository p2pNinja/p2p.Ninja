


def amend_routing_tables (packet, returnaddr, unsigned_routing_dict, signed_routing_dict, unsigned_destination_list, signed_destination_list, settings):
    pass
    
    
    ''' this fucntion expects to recieve a packet (as defined in protocol documentation) as the first argument
    the source_address/connection information from where the packet came should be passed as the second argument.
         this function also accepts the 4 routing/destination sets. see protocol documentation
         this function then amends the 4 routing/desitnation sets accroding to information in the packet
         and return address and then return the 4 amended routing/destination sets/tables.
         this function serves to analayze the packet and addr and build the routing table.
         it may return false if the packet structure is not amenable analyses
    '''
    print ('you are in the amend_routing_tables function')
    input_args = (packet, returnaddr, unsigned_routing_dict, 
          signed_routing_dict, unsigned_destination_list, signed_destination_list)
    originid = packet['origin']['id']
    routingaid = packet['origin']['routingaid']
    time = packet['UTC']
    signature = packet['signaturebyorigin']
    if originid == settings['LOCALID']:
        print ('originid = local id, returning')
        return input_args

    if (packet['origin']['publickey'] is True) & (packet['type']=='broadcast') & (originid in signed_destination_list):
            print ('signed broadcast from known origin, will check if sufficient time has passed since last broadcast')
            if signed_routing_dict[originid]['time']-settings['MINIMUMINTERVALBETWEENBROADCASTS'] > time:
                print ('packet is sufficiently new')
                signed_routing_dict[originid] = {'time':time, 'peer': returnaddr}
                signed_destination_list.remove(originid)
                signed_destination_list.append(originid)
                print('signed destination list and signed_routing_dict updated, returngin to main loop now... ')
                return (packet, returnaddr, unsigned_routing_dict, 
                         signed_routing_dict, unsigned_destination_list, signed_destination_list)
            else:
                return input_args


    if (packet['origin']['publickey'] is True) & (packet['type']=='broadcast') : #new sender not known before
        print('signed broadcast from previously unknown sender')
        signed_routing_dict[originid] = {'time':time, 'peer': returnaddr}
        signed_destination_list.append(originid)
        print ('signed_destination_list and signed_routing_dict updated')
        if len(signed_destination_list)>settings['NUMBEROFKEYSTOSAVE']:
            print ('signed_destination_list is too long')
            del signed_routing_dict[signed_destination_list[0]]
            signed_destination_list.pop(0)
            print ('first element of signed_destination_list and corresponding entry from signed_routing_dict removed')
        print ('will return to main func now')
        return (packet, returnaddr, unsigned_routing_dict, 
                signed_routing_dict, unsigned_destination_list, signed_destination_list) 


    if packet['origin']['publickey'] is False:    # this always causes amending of the dictionary 
        print ('unsigned packet recieved, will update unsigned_routing_dict and unsigned_destination_list')
        
        if len(unsigned_destination_list)>settings['NUMBEROFKEYSTOSAVE']:
            print ('unsigned_destination_list too long, will trim along with unsigned_routing_dict')
            del unsigned_routing_dict[unsigned_destination_list[0]]
            unsigned_destination_list.pop(0)
            print ('successful')
        unsigned_routing_dict[originid] = {'peer':returnaddr}
        unsigned_destination_list.append(originid)
        print ('update successful')
        print ('return to main loop...')
        return (packet, returnaddr, unsigned_routing_dict, 
      signed_routing_dict, unsigned_destination_list, signed_destination_list) 

    if (packet['origin']['publickey'] is True) & (originid not in signed_destination_list):
        print('signed packet recieved , not broadcast type and previously not heard from')
        signed_routing_dict[originid] = {'time':time, 'peer': returnaddr}
        signed_destination_list.append(originid)
        print ('signed_destination_list and signed_routing_dict updated')
        if len(signed_destination_list)>settings['NUMBEROFKEYSTOSAVE']:
            print ('signed_destination_list is too long')
            del signed_routing_dict[signed_destination_list[0]]
            signed_destination_list.pop(0)
            print ('first element of signed_destination_list and corresponding entry from signed_routing_dict removed')
        print ('will return to main func now')
        return (packet, returnaddr, unsigned_routing_dict, 
                signed_routing_dict, unsigned_destination_list, signed_destination_list) 

    
    print ('amend routing tables, this packet did not meet any clause of ammending the tables')
    print ('final tables:\n', 'unsigned_routing_dict:\n', unsigned_routing_dict, 'signed_routing_dict:\n',signed_routing_dict, 
            'unsigned_destination_list:\n', unsigned_destination_list, 'signed_destination_list:\n ', signed_destination_list )

    return input_args































'''def learnfrom(packet, addr):
    packetorigin = packet.['origin'].['id']
    packettime=packet.['UTC']
    packetduration=(packettime-(time.time()))
    if packet.['origin'].['publickey'] & packet.['origin'].['id'] in signedroutingtable:
        myranking = signedroutingtable.[packetorigin].
        for (packettime,packetduration,nexthop) in myranking :
         
        myranking.append((packettime,packetduration,addr))
        
        rankingbyduration = sorted(myranking, key=itemgetter(2)) #longer duration last
        rankingbypackettime= sorted(rankingbyduration, key=itemgetter(1), reverse=True) #larger packet time first
        finalranking= rankingbypackettime
        while len(finalranking)>numberofconnectionstosave:
            finalranking.pop()
        signedroutingtable[packetorigin]=finalranking

    if packet.['isoriginidapublickey?'] & packetorigin is not in signedroutingtable:
        signedroutingtable[packetorigin]=[(packettime,packetduration,addr)]


'''
        






