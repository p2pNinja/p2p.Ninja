
#the following function serves a webpage to allow settings to be changed.
def settingspage(packet,returnaddr, sel, settings,listofpeers):
    print ('you are in settingspage module')
    import json
    import time
    #############################################################################################################
    returnaddr.sendall(bytes('<!DOCTYPE html> <title>p2p.Ninja settings</title>Thank you for choosing p2p.Ninja! <br>This is your local p2p.Ninja gateway<br><br>','utf-8'))
    returnaddr.sendall('<br>##########################<br> Following are the settings of the p2p.Ninja gateway prior to your request for this page'.encode('utf-8'))
    

    returnaddr.sendall(bytes('<br><br>settings file:<br>','utf-8'))
    try:
        with open('settings', 'r') as file:
            settingsread = file.read()
            file.close()
        returnaddr.sendall(settingsread.encode('utf-8'))
    except:
        returnaddr.sendall('settings file could not be read'.encode('utf-8'))
        returnaddr.sendall('<br>----------------------'.encode('utf-8'))

    
    returnaddr.sendall('<br><br> listofpeers file:<br>'.encode('utf-8'))
    try:
        with open('listofpeers', 'r') as file:
            listofpeersread = file.read()
            file.close()
        returnaddr.sendall(listofpeersread.encode('utf-8'))
    except:
        returnaddr.sendall('listofpeers file could not be read'.encode('utf-8'))
        #returnaddr.sendall('<br>----------------------'.encode('utf-8'))

    returnaddr.sendall('<br><br> list of peers per memory:<br>'.encode('utf-8'))
    returnaddr.sendall((json.dumps(listofpeers)).encode('utf-8'))

    returnaddr.sendall('<br>##############################<br><br><br>'.encode('utf-8'))

    ######################################################################################################################




    returnaddr.sendall('<br><br> How you may change your p2p.Ninja Gateway settings:'.encode('utf-8'))
    returnaddr.sendall('<br><br>VERSION, Ethernet IP and TCP_PORT cannot be changed here. Format to change setting is settings.p2p/parameter_to_be_changed/setting_desired/set'.encode('utf-8'))
    returnaddr.sendall('<br><br>parameter may be SELF_PORT_PEER, LOCALID , LOCALROUTINGAID , LOCALIDPUBLICKEY , LOCALKEYEXPONENT , ACCEPTABLEHOPCOUNT , NUMBEROFKEYSTOSAVE , MINIMUMINTERVALBETWEENBROADCASTS , NUMBEROFCONNECTIONSTOSAVE , ACCEPTABLEROUTINGPACKETSIZE , ACCEPTABLEBROADCASTPACKETSIZE , TIMEDELAYACCEPTABLE'.encode('utf-8'))
    returnaddr.sendall('<br><br>ADD_PEER and REMOVE_PEER are additional commands. please format as follows : settings.p2p/ADD_PEER/IP_address/port_number/set '.encode('utf-8'))
    returnaddr.sendall('<br><br>LOCALROUTINGAID can be alfanumeric. Make sure you give setting for IP address in the right format, other values must be integers'.encode('utf-8'))
    returnaddr.sendall('<br>############################################'.encode('utf-8'))
    ##################################################################################################################
    if True:
        urlstring = packet['datastring']#.decode(encoding='UTF-8',errors='strict')
        urlbroken=urlstring.split('/')
        print('pocessing url in settings page, urlbroken:',urlbroken,settings)
        #returnaddr.sendall(urlbytes)
        settingparameter = urlbroken[2]
        settingvaluedesired = urlbroken[3]
        settingvaluedesiredport = urlbroken[4]

        
        returnaddr.sendall(('<br>####################################<br>your url request was assesed and, you are requesting change of following: <br>parameter:'+ settingparameter+ ' <br>to: '+ settingvaluedesired).encode('utf-8'))
        #returnaddr.sendall('<br>this will now be attemtped to be changed and take effect on next reload'.encode('utf-8'))

        if settingparameter in [ 'LOCALID', 'LOCALIDPUBLICKEY', 'SELF_PORT_PEER',
                                'LOCALKEYEXPONENT', 'ACCEPTABLEHOPCOUNT', 'NUMBEROFKEYSTOSAVE', 'MINIMUMINTERVALBETWEENBROADCASTS',
                                'NUMBEROFCONNECTIONSTOSAVE', 'ACCEPTABLEROUTINGPACKETSIZE', 'ACCEPTABLEBROADCASTPACKETSIZE', 'TIMEDELAYACCEPTABLE']:
            returnaddr.sendall(('<br>Numeric change: set'+ settingparameter+ ' to '+ settingvaluedesired).encode('utf-8'))
            returnaddr.sendall('<br><br>this will now be attemtped to be changed and take effect on next reload'.encode('utf-8'))
            settingtemp = settings
            returnaddr.sendall('<br><br>this will now be attemtped to be changed and take effect on next reload1'.encode('utf-8'))
            settingtemp[settingparameter] = int(settingvaluedesired)
            returnaddr.sendall('<br><br>this will now be attemtped to be changed and take effect on next reload2'.encode('utf-8'))
            print('yoyo', json.dumps(settingtemp))
            print(settings)
            with open('settings', 'w+') as file:
                file.write(json.dumps(settingtemp))
                file.close()
                returnaddr.sendall('<br>write function sucessful'.encode('utf-8'))

        elif settingparameter in [ 'SELF_IP_PEER','LOCALROUTINGAID']:
            
            returnaddr.sendall('<br><br>this will now be attemtped to be changed and take effect on next reload'.encode('utf-8'))
            settingtemp = settings
            #returnaddr.sendall('settings temp changed'.encode('utf-8'))
            settingtemp[settingparameter] = settingvaluedesired
            #returnaddr.sendall('settings temp changed'.encode('utf-8'))
            with open('settings', 'w+') as file:
                file.write(json.dumps(settingtemp))
                file.close()
                returnaddr.sendall('write function sucessful'.encode('utf-8'))

        elif settingparameter == 'ADD_PEER':
            returnaddr.sendall('you want to add peer'.encode('utf-8'))
            newpeer = (settingvaluedesired, int(settingvaluedesiredport))
            listofpeers.append(newpeer)
            with open ('listofpeers','w+') as file:
                file.write(repr(listofpeers))
                file.close()
                returnaddr.sendall('operation successful'.encode('utf-8'))

        elif settingparameter == 'REMOVE_PEER':
            returnaddr.sendall('you want to remove peer'.encode('utf-8'))
            peer = (settingvaluedesired, int(settingvaluedesiredport))
            listofpeers.remove(peer)
            with open ('listofpeers','w+') as file:
                file.write(repr(listofpeers))
                file.close()
                returnaddr.sendall('operation successful'.encode('utf-8'))



        else:
            returnaddr.sendall('<br><br><br><br>This is not available to be changed'.encode('utf-8'))
            #returnaddr.sendall('<br>Ethernet IP and TCP_PORT cannot be changed here. format to change setting is gateway.p2p/parameter/setting'.encode('utf-8'))
            #returnaddr.sendall('<br>parameter may be SELF_IP_PEER, SELF_PORT_PEER, LOCALID , LOCALROUTINGAID , LOCALIDPUBLICKEY , LOCALKEYEXPONENT , ACCEPTABLEHOPCOUNT , NUMBEROFKEYSTOSAVE , MINIMUMINTERVALBETWEENBROADCASTS , NUMBEROFCONNECTIONSTOSAVE , ACCEPTABLEROUTINGPACKETSIZE , ACCEPTABLEBROADCASTPACKETSIZE , TIMEDELAYACCEPTABLE'.encode('utf-8'))
    

    else:
        returnaddr.sendall('<br>no setting change request was received or the format was innacurate to be processed.'.encode('utf-8'))
        #returnaddr.sendall('<br>parameter may be SELF_PORT_PEER, LOCALID , LOCALROUTINGAID , LOCALIDPUBLICKEY , LOCALKEYEXPONENT , ACCEPTABLEHOPCOUNT , NUMBEROFKEYSTOSAVE , MINIMUMINTERVALBETWEENBROADCASTS , NUMBEROFCONNECTIONSTOSAVE , ACCEPTABLEROUTINGPACKETSIZE , ACCEPTABLEBROADCASTPACKETSIZE , TIMEDELAYACCEPTABLE'.encode('utf-8'))
    
    ###################################################################################################################
    statement = ('<br><br>####################################################<br>final settings follow at the conclusion of serving this page <br><br>')
    returnaddr.sendall(statement.encode('utf-8'))
    

    returnaddr.sendall(bytes('<br><br>settings file:<br>','utf-8'))
    try:
        with open('settings', 'r') as file:
            settingsread = file.read()
            file.close()
        returnaddr.sendall(settingsread.encode('utf-8'))
    except:
        returnaddr.sendall('settings file could not be read'.encode('utf-8'))
        returnaddr.sendall('<br>----------------------'.encode('utf-8'))

    
    returnaddr.sendall('<br><br> listofpeers file:<br>'.encode('utf-8'))
    try:
        with open('listofpeers', 'r') as file:
            listofpeersread = file.read()
            file.close()
        returnaddr.sendall(listofpeersread.encode('utf-8'))
    except:
        returnaddr.sendall('listofpeers file could not be read'.encode('utf-8'))
        #returnaddr.sendall('<br>----------------------'.encode('utf-8'))

    returnaddr.sendall('<br><br> list of peers per memory:<br>'.encode('utf-8'))
    returnaddr.sendall((repr(listofpeers)).encode('utf-8'))
    print (listofpeers)
    print (settings)

    returnaddr.sendall('<br>##############################<br><br><br>'.encode('utf-8'))

    returnaddr.sendall('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'.encode('utf-8'))
    returnaddr.sendall('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'.encode('utf-8'))
    returnaddr.sendall('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'.encode('utf-8'))
    returnaddr.sendall('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'.encode('utf-8'))
    with open('settingspage.py', 'r') as file:
        pageinfo = file.read()
        returnaddr.sendall(pageinfo.encode('utf-8'))

    returnaddr.close()
    sel.unregister(returnaddr)
    return
