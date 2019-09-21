



def broadcast(packet_byte, returnaddr, listofpeers, peersock): 
    for peer in listofpeers:
        if peer != returnaddr:
        	    try:
        	    	peersock.sendto(packet_byte, peer)
        	    except:
        	    	pass
        	    

    
    return
     
    