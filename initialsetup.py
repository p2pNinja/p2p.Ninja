#################### modify the chron tab and interface file
from time import sleep
import sys
import subprocess
import os

print ('Thank you for choosing p2p.Ninja')
print('Copyright (C) <2019>  <Hersh Goel> \n')
print('You should have received a copy of the GNU General Public License \nalong with this program.  If not, see <https://www.gnu.org/licenses/>')
print('This program comes with ABSOLUTELY NO WARRANTY')  
wait = input('If you would like to exit, press Ctrl+C, otherwise press Y and then ENTER')  

print ('We will attempt to install the p2p.Ninja Gateway on your') 
print ('computer. Please note that this program is for installation')
print ('on a new install of raspbian NOOBS_v2_9_0. p2p.Ninja is')
print ('experimental at this time and should only be installed and')
print ('executed in an environment where data confidentiality and')
print ('safety are dispensable. There is no warranty of any kind -')
print ('express or implied. p2p.Ninja network is not encrypted ')
print ('Proceeding with installation will delete')
print ('prior network settings and passwords. we do not warrant our')
print ('ability to restore your system settings afterwards. Superuser')
print('privileges are needed to complete this installation')
#print ( 'now.this will modify your network settings and schedule the p2p.Ninj')
#print ('this will modify your network settings and schedule the p2p.Ninja Gat\neway to start at each boot/reboot')
wait = input('Press Ctrl+C to exit, enter any key followed by ENTER to proceed: ')
sleep(1)
print ('thank you, will proceed')
sleep(1)
print ('...')

with open ('pathtohere', 'r') as file:
	pathtohere = file.read()
print('success in reading pathtohere')

with open('interfacesettings', 'r') as file:
	interface_settings = file.read()
print('success in reading interfacesettings')

sleep(1)


print('now attempting to create p2pninja.service in local directory')
sleep(1)
with open('p2pninja.service', 'w+') as file:
	file.close()
	pass

with open('p2pninja.service_template1of3', 'r') as file:
	service_template1of3 = file.read()

service_template2of3 = '\nWorkingDirectory=' + pathtohere

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


