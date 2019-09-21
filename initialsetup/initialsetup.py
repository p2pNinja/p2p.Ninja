#################### modify the chron tab and interface file
from time import sleep
import sys
import subprocess
import os
import random
import json

with open('Text1', 'r') as file:
	notice = file.read()
print (notice)

while True:
	wait = input('If you would like to exit, press Ctrl+C, otherwise press Y and then ENTER: ')
	if wait == ('y' or 'Y'):
		break
	else:
		pass
sleep(1)
print ('thank you, will proceed')
sleep(1)
print ('...')

import os
os.chdir(os.path.dirname(os.getcwd())) #step up one folder

installationfolder= os.getcwd()
print('installation folder', installationfolder)
os.chdir('./initialsetup') #come back to this directory



print ('will now randomize localID')
sleep(1)
os.chdir(os.path.dirname(os.getcwd())) #step up one folder
settings ={}
if True:
    with open ('settings', 'r') as file:
        settingsread = file.read()
        file.close()
        print('settings file was read, read parameters follow:')
    print(settingsread)
    settingsread = json.loads(settingsread)
    #and replaces key value pairs based on settingsread
    for key in settingsread:
        settings[key] = settingsread[key]
    settings['LOCALID'] = random.randint(1,9999999999999999)
    
    
else:
    pass

tempipaddress = "192.168.2." + str(random.randint(1,255))
settings['SELF_IP_PEER'] = tempipaddress


with open('settings', 'w+') as file:
                file.write(json.dumps(settings))
                file.close()
print ('LOCALID and SELF_IP_PEER randomized and new file written')        
print ('final settings: ', settings)


os.chdir('./initialsetup') #come back to this directory


with open('interfacesettings', 'r') as file:
	interface_settings = file.read()
	file.close()
print('success in reading interfacesettings')

sleep(1)


print('now attempting to create p2pninja.service in local directory')
sleep(1)
with open('p2pninja.service', 'w+') as file:
	file.close()
	pass

with open('p2pninja.service_template1of3', 'r') as file:
	service_template1of3 = file.read()

service_template2of3 = '\nWorkingDirectory=' + installationfolder +'/router'

print (service_template2of3)

with open('p2pninja.service_template3of3', 'r') as file:
	service_template3of3 = file.read()



with open('p2pninja.service','a') as file:
	file.write(service_template1of3)
	file.write(service_template2of3)
	file.write(service_template3of3)
	
with open('p2pninja.service','r') as file:	
	p2pninjaservice = file.read()
	file.close()
print('success!')
sleep(1)
print('now attempt to copy p2pninja.service to system folder')
sleep(1)
os.chdir('/etc/systemd/system')
with open('p2pninja.service','w+') as file:
	file.write(p2pninjaservice)
	file.close()
print('success')
sleep(1)
print('will attempt daemon-reload and enable p2pninja.service')
os.system('sudo systemctl daemon-reload')
os.system('sudo systemctl enable p2pninja.service')
#print ('success')
sleep(1)

print('now attempt to overwrite interface')
sleep(1)
os.chdir ('/etc/network')
with open('interfaces','w+') as file:
	file.write(interface_settings)
	file.close()
print('success!')
sleep(1)
print('p2p.Ninja successfully installed! Thank you for choosing p2p.Ninja!')
sleep(3)
print('p2p.Ninja should begin operation with the next system restart')
wait = input('enter any keyword to exit : ')


