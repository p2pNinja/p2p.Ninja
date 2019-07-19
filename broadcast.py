



def broadcast(packet_byte, returnaddr, listofpeers, peersock): 
    for peer in listofpeers:
        if peer != returnaddr:
        	    peersock.sendto(packet_byte, peer)
        	    

    
    return
     
    