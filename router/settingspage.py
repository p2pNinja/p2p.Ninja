
#the following function serves a webpage to allow settings to be changed. returns updated settings (with reference time diference if provided.)
def settingspage(packet_dict,returnaddr, sel, settings,listofpeers):
    print ('you are in settingspage module')
    import json
    import time
    import os
    import ast
    from threading import Thread
    
    
    
    
    returnaddr.sendall('<html>'.encode('utf-8'))

    url_bytes = ast.literal_eval(packet_dict['datastring'])
    url_str = str(url_bytes)
    print('str')
    
    
    
    
    
    try:
        step_one=url_str.split()[1]
        print('split')
        step_two = step_one.split('?')[1]
        print('split ?')
        list_of_parameters_and_settings = step_two.split('&')
        print('list_of_parameters_and_settings:', list_of_parameters_and_settings)

        url_dict ={}
        for parameter_value in list_of_parameters_and_settings:
            (parameter,value) = parameter_value.split('=')
            url_dict[parameter] = value
    except:
        url_dict = {'PASSWORD':''}
    print (url_dict)

    if url_dict['PASSWORD'] != settings['PASSWORD']:
        print('password did not match in settingspage')
        if 'PASSWORD=' in url_str:
            returnaddr.sendall('<html>The password you supplied is incorrect!'.encode('utf-8'))
            returnaddr.sendall(ast.literal_eval(packet_dict['datastring']))
        with open('./settingspagefiles/landingpage.html','r') as file:
            welcomemessage = file.read()
        returnaddr.sendall(welcomemessage.encode('utf-8'))
        #returnaddr.sendall('The password (if supplied) is inaccurate, connection will be terminated.'.encode('utf-8'))
        returnaddr.close()
        sel.unregister(returnaddr)
        return settings
    else:
        pass
    print ('passphrase found in url request')
 


   
    ##################################################################################################################
    try:
        if url_dict['PARAMETER'] == "current_settings":
            returnaddr.sendall(bytes('<br><br>settings file:<br>','utf-8'))
            try:
                os.chdir(os.path.dirname(os.getcwd()))
                with open('settings', 'r') as file:
                    settingsread = file.read()
                    file.close()
                returnaddr.sendall(settingsread.encode('utf-8'))
                os.chdir('./router') #come back to this directory
            except:
                returnaddr.sendall('settings file could not be read'.encode('utf-8'))
                returnaddr.sendall('<br>----------------------'.encode('utf-8'))

            
            returnaddr.sendall('<br><br> listofpeers file:<br>'.encode('utf-8'))
            try:
                os.chdir(os.path.dirname(os.getcwd()))
                with open('listofpeers', 'r') as file:
                    listofpeersread = file.read()
                    file.close()
                returnaddr.sendall(listofpeersread.encode('utf-8'))
                os.chdir('./router') #come back to this directory
            except:
                returnaddr.sendall('listofpeers file could not be read'.encode('utf-8'))
                #returnaddr.sendall('<br>----------------------'.encode('utf-8'))

            returnaddr.sendall('<br><br> list of peers per memory:<br>'.encode('utf-8'))
            returnaddr.sendall((json.dumps(listofpeers)).encode('utf-8'))



        elif url_dict['PARAMETER'] in [ 'LOCALID', 'LOCALIDPUBLICKEY', 'SELF_PORT_PEER',
                                'LOCALKEYEXPONENT', 'ACCEPTABLEHOPCOUNT', 'NUMBEROFKEYSTOSAVE', 'MINIMUMINTERVALBETWEENBROADCASTS',
                                'NUMBEROFCONNECTIONSTOSAVE', 'ACCEPTABLEROUTINGPACKETSIZE', 'ACCEPTABLEBROADCASTPACKETSIZE', 'TIMEDELAYACCEPTABLE']:
            returnaddr.sendall(('<br>Numeric change: set'+ url_dict['PARAMETER'] + ' to '+ url_dict['set_to']).encode('utf-8'))
            returnaddr.sendall('<br><br>this will now be attemtped to be changed and take effect on next reload'.encode('utf-8'))
            settingtemp = settings
            returnaddr.sendall('<br><br>this will now be attemtped to be changed and take effect on next reload1'.encode('utf-8'))
            settingtemp[url_dict['PARAMETER']] = int(url_dict['set_to'])
            returnaddr.sendall('<br><br>this will now be attemtped to be changed and take effect on next reload2'.encode('utf-8'))
            print('yoyo', json.dumps(settingtemp))
            print(settings)
            
            os.chdir(os.path.dirname(os.getcwd())) #step up one folder . and dont forget to comeback
            with open('settings', 'w+') as file:
                file.write(json.dumps(settingtemp))
                file.close()
                returnaddr.sendall('<br>write function sucessful'.encode('utf-8'))
            os.chdir('./router') #come back to this directory

        elif url_dict['PARAMETER'] in [ 'SELF_IP_PEER','LOCALROUTINGAID','PASSWORD']:
            
            returnaddr.sendall('<br><br>this will now be attemtped to be changed and take effect on next reload'.encode('utf-8'))
            settingtemp = settings
            #returnaddr.sendall('settings temp changed'.encode('utf-8'))
            settingtemp[url_dict['PARAMETER']] = url_dict['set_to']
            #returnaddr.sendall('settings temp changed'.encode('utf-8'))
            os.chdir(os.path.dirname(os.getcwd())) #step up one folder . and dont forget to comeback
            with open('settings', 'w+') as file:
                file.write(json.dumps(settingtemp))
                file.close()
                returnaddr.sendall('write function sucessful'.encode('utf-8'))
            os.chdir('./router') #come back to this directory

        elif url_dict['PARAMETER'] == 'ADD_PEER':
            returnaddr.sendall('you want to add peer'.encode('utf-8'))
            newpeer = (url_dict['set_to'], int(url_dict['set_to2']))
            listofpeers.append(newpeer)
            os.chdir(os.path.dirname(os.getcwd()))
            with open ('listofpeers','w+') as file:
                file.write(repr(listofpeers))
                file.close()
                returnaddr.sendall('operation successful'.encode('utf-8'))
            os.chdir('./router')

        elif url_dict['PARAMETER'] == 'REMOVE_PEER':
            returnaddr.sendall('you want to remove peer'.encode('utf-8'))
            peer = (url_dict['set_to'], int(url_dict['set_to2']))
            listofpeers.remove(peer)
            os.chdir(os.path.dirname(os.getcwd()))
            with open ('listofpeers','w+') as file:
                file.write(repr(listofpeers))
                file.close()
                returnaddr.sendall('operation successful'.encode('utf-8'))
            os.chdir('./router')

        elif url_dict['PARAMETER'] == 'TIME_SIGNAL':
            reference_time = int(url_dict['set_to'])/1000 #seconds since epoch
            local_time = time.time()
            referernce_minus_local_time = reference_time - local_time
            returnaddr.sendall('TIME_SIGNAL recieved. referernce_minus_local_time = '.encode('utf-8'))
            returnaddr.sendall(str(referernce_minus_local_time).encode('utf-8'))
            settings['referernce_minus_local_time'] = referernce_minus_local_time
            settingtemp = settings
            os.chdir(os.path.dirname(os.getcwd())) #step up one folder . and dont forget to comeback
            with open('settings', 'w+') as file:
                file.write(json.dumps(settingtemp))
                file.close()
                returnaddr.sendall('write function sucessful'.encode('utf-8'))
            os.chdir('./router') #come back to this directory


        elif url_dict['PARAMETER'] == 'start_server':
            os.chdir(os.path.dirname(os.getcwd())) #step up one folder . and dont forget to comeback
            os.chdir('./server')
            with open ('keep_alive', 'w+') as file:
                file.write('true')
            #import os
            try:
                os.remove("kill")
            except:
                pass
            time.sleep(2)

            def start_server():
                import subprocess
                subprocess.Popen("lxterminal -e sudo python3 server.py ", shell=True)
            thread = Thread(target = start_server)  
            thread.start()
            print('started server...')
            time.sleep(2)
            print ('moving on...')
            os.chdir(os.path.dirname(os.getcwd()))
            os.chdir('./router')
            returnaddr.sendall('start server command initiated without exception'.encode('utf-8'))
            pass

         
        elif url_dict['PARAMETER'] == 'stop_server':
            os.chdir(os.path.dirname(os.getcwd())) #step up one folder . and dont forget to comeback
            os.chdir('./server')
            with open ('kill', 'w+') as file:
                file.write('true')
                returnaddr.sendall('kill file written'.encode('utf-8'))
            #import os
            try:
                with open ('keep_alive', 'w+') as file:
                    file.write('false')
                    returnaddr.sendall('keep_alive file changed to false'.encode('utf-8'))
            except:
                pass
            thread = Thread(target = start_server)  
            thread.start()
            os.chdir(os.path.dirname(os.getcwd()))
            os.chdir('./router')
            


        elif url_dict['PARAMETER'] == 'serversetting_upload': #needs work!!!!
            os.chdir(os.path.dirname(os.getcwd())) #step up one folder . and dont forget to comeback
            os.chdir('./server')
            print ('serversettingupload')
            with open ('trialsettings', 'wb') as file:
                file.write(url_bytes)
                returnaddr.sendall('trialsettings file written'.encode('utf-8'))
            
            change_server_settings()
            print('did ti work??')
            #import os
            os.chdir(os.path.dirname(os.getcwd()))
            os.chdir('./router')
            
        elif url_dict['PARAMETER'] == 'website_upload': #needs work!!!!
            os.chdir(os.path.dirname(os.getcwd())) #step up one folder . and dont forget to comeback
            os.chdir('./server')
            print ('websiteupload')
            with open ('trialwebsite', 'wb') as file:
                file.write(url_bytes)
                returnaddr.sendall('trialwebsite file written'.encode('utf-8'))
            
            upload_website()
            print('did ti work??')
            #import os
            os.chdir(os.path.dirname(os.getcwd()))
            os.chdir('./router')
        




        else:
            returnaddr.sendall('<br><br><br><br>This is not available to be changed'.encode('utf-8'))
            #returnaddr.sendall('<br>Ethernet IP and TCP_PORT cannot be changed here. format to change setting is gateway.p2p/parameter/setting'.encode('utf-8'))
            #returnaddr.sendall('<br>parameter may be SELF_IP_PEER, SELF_PORT_PEER, LOCALID , LOCALROUTINGAID , LOCALIDPUBLICKEY , LOCALKEYEXPONENT , ACCEPTABLEHOPCOUNT , NUMBEROFKEYSTOSAVE , MINIMUMINTERVALBETWEENBROADCASTS , NUMBEROFCONNECTIONSTOSAVE , ACCEPTABLEROUTINGPACKETSIZE , ACCEPTABLEBROADCASTPACKETSIZE , TIMEDELAYACCEPTABLE'.encode('utf-8'))
    

    except:
        returnaddr.sendall('<br>no setting change request was received or the format was innacurate to be processed.'.encode('utf-8'))
        #returnaddr.sendall('<br>parameter may be SELF_PORT_PEER, LOCALID , LOCALROUTINGAID , LOCALIDPUBLICKEY , LOCALKEYEXPONENT , ACCEPTABLEHOPCOUNT , NUMBEROFKEYSTOSAVE , MINIMUMINTERVALBETWEENBROADCASTS , NUMBEROFCONNECTIONSTOSAVE , ACCEPTABLEROUTINGPACKETSIZE , ACCEPTABLEBROADCASTPACKETSIZE , TIMEDELAYACCEPTABLE'.encode('utf-8'))
    
    ###################################################################################################################
    statement = ('<br><br>####################################################<br>final settings follow at the conclusion of serving this page <br><br>')
    returnaddr.sendall(statement.encode('utf-8'))
    

    returnaddr.sendall(bytes('<br><br>settings file:<br>','utf-8'))
    try:
        os.chdir(os.path.dirname(os.getcwd()))
        with open('settings', 'r') as file:
            settingsread = file.read()
            file.close()
        os.chdir('./router')
        returnaddr.sendall(settingsread.encode('utf-8'))
    except:
        returnaddr.sendall('settings file could not be read'.encode('utf-8'))
        returnaddr.sendall('<br>----------------------'.encode('utf-8'))

    
    returnaddr.sendall('<br><br> listofpeers file:<br>'.encode('utf-8'))
    try:
        os.chdir(os.path.dirname(os.getcwd()))
        with open('listofpeers', 'r') as file:
            listofpeersread = file.read()
            file.close()
        os.chdir('./router')
        returnaddr.sendall(listofpeersread.encode('utf-8'))
    except:
        returnaddr.sendall('listofpeers file could not be read'.encode('utf-8'))
        #returnaddr.sendall('<br>----------------------'.encode('utf-8'))

    returnaddr.sendall('<br><br> list of peers per memory:<br>'.encode('utf-8'))
    returnaddr.sendall((repr(listofpeers)).encode('utf-8'))
    print (listofpeers)
    print (settings)

    returnaddr.sendall('<br>##############################<br><br><br>'.encode('utf-8'))
    '''
    returnaddr.sendall('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'.encode('utf-8'))
    returnaddr.sendall('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'.encode('utf-8'))
    returnaddr.sendall('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'.encode('utf-8'))
    returnaddr.sendall('<br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br><br>'.encode('utf-8'))
    with open('settingspage.py', 'r') as file:
        pageinfo = file.read()
        returnaddr.sendall(pageinfo.encode('utf-8'))
    '''
    returnaddr.close()
    sel.unregister(returnaddr)
    return settings





####################################
def change_server_settings():
        print ('you are in change_server_settings.pyksdfjvndklfjfvnkdjsfvnkln')
        import ast

        with open('trialsettings', 'rb') as file:
            bytedata = file.read()
            stringdata = repr(bytedata)

        print('stringdate:',stringdata)


        print('\n\n\n\n\n\n')


        boundary = stringdata.split('boundary=')[1].split('\\r')[0]
        print('boundary:', boundary)

        multipartlist = stringdata.split(boundary)

        print('\n\n\n\n\n\n')
        print ('multipartlist')


        for part in multipartlist:
            print(part)
            print ('\n')



        for part in multipartlist:
            try:
                if part.index("\\r\\nContent-Disposition: form-data; name=\"myfile\"; filename=\"settings.txt\"") == 0:
                #
                    print('Yahoooooooooooooooooooooooo')
                    part_of_interest = part
                    break
                else:
                    print ('no')
            except:
                pass


        print ('part_of_interest', part_of_interest)

            

        header_removed = part_of_interest.split('\\r\\n\\r\\n', 1)[-1] 



        file_string = header_removed[:-6]
        print('\n\n'+'file_string', file_string)




        file_repr = "b\'"+file_string+"\'"
        print('\n\n','file_repr' , file_repr)


        file_bytes = ast.literal_eval(file_repr)
        print('\n\n', 'file_bytes',file_bytes)



        #print('\n\n\n', 'file', file)

        with open('settings.txt', 'wb+') as file:
            file.write(file_bytes)


#######

####################################
def upload_website():
        print ('you are uploading a website')
        import ast

        with open('trialwebsite', 'rb') as file:
            bytedata = file.read()
            stringdata = repr(bytedata)

        print('stringdate:',stringdata)


        print('\n\n\n\n\n\n')


        boundary = stringdata.split('boundary=')[1].split('\\r')[0]
        print('boundary:', boundary)

        multipartlist = stringdata.split(boundary)

        print('\n\n\n\n\n\n')
        print ('multipartlist')


        for part in multipartlist:
            print(part)
            print ('\n')



        for part in multipartlist:
            try:
                if part.index("\\r\\nContent-Disposition: form-data; name=\"myfile\"; filename=\"website.zip\"") == 0:
                #
                    print('Yahoooooooooooooooooooooooo')
                    part_of_interest = part
                    break
                else:
                    print ('no')
            except:
                pass


        print ('part_of_interest', part_of_interest)

            

        header_removed = part_of_interest.split('\\r\\n\\r\\n', 1)[-1] 



        file_string = header_removed[:-6]
        print('\n\n'+'file_string', file_string)




        file_repr = "b\'"+file_string+"\'"
        print('\n\n','file_repr' , file_repr)


        file_bytes = ast.literal_eval(file_repr)
        print('\n\n', 'file_bytes',file_bytes)



        #print('\n\n\n', 'file', file)

        with open('website.zip', 'wb+') as file:
            file.write(file_bytes)
        print('website.zip written')
        
        from zipfile import ZipFile
        print ('import done')
        with ZipFile('website.zip', 'r') as zip_ref:
            print('website.zip opened')
            zip_ref.extractall()
        print ('yelooooooooooooooooooooooooooooooo')
