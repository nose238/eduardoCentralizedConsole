# !/usr/bin/env python
# This code has been developed by Eduardo Marquez -- nose238@hotmail.com

##################Importing libraries#####################
import time
import commands
import os
from daemon import runner
###########Daemonization part starts######################
class App():
    def __init__(self):
        self.stdin_path = '/dev/null'
        self.stdout_path = '/dev/tty'
        self.stderr_path = '/dev/tty'
        self.pidfile_path =  '/tmp/foo.pid'
        self.pidfile_timeout = 5
    def run(self):
###########Daemonization part ends########################
#---------------------MAIN-------------------------------#
		i = 0
		while True:
			# The code is going to write ip addresses which have ssh connection and public key
			txt_ip_SSH= open("/var/www/html/centralizedConsole/web/centralizedConsole/ipListSSH.txt", "w")  
			txt_ip_SSH.write("")
			txt_ip_SSH.close()
			# Here is where code read passwd, user and port from
			file = open('/var/www/html/centralizedConsole/web/clients/clientsCredentials', 'r')
			ipStatus = open("/var/www/html/centralizedConsole/web/centralizedConsole/ipStatus.txt", "w")
			for line in file:
				txt_ip_SSH = open("/var/www/html/centralizedConsole/web/centralizedConsole/ipListSSH.txt", "a")   
				ipAdClient = line.partition("|")[0]
				temp       = line.partition("|")[2]
				userClient = temp.partition("|")[0]
				temp       = temp.partition("|")[2]
				passClient = temp.partition("|")[0]
				temp       = temp.partition("|")[2]
				portClient = temp.partition("|")[0]
				#print("IP: " + ipAdClient + "	USER: " +  userClient + "	PASS: " + passClient + "	PORT: " + portClient)
				ipStatus.write(ipAdClient+"|")
				# Try to connect by SSH. status get a value depending if there is an error or not
				status = commands.getstatusoutput("sshpass -p '' ssh -o 'KbdInteractiveDevices no' -o StrictHostKeyChecking=no " + 
				userClient + "@" + ipAdClient + " -p " + portClient) #it verifies if public key is on the Server  
				#print(status)
				if status[0] == 0: # return 0 whit no errors. Public key on in the Server
				#	print("Key found")
					ipStatus.write("yes\n")
					txt_ip_SSH.write(ipAdClient + "|" + userClient + "|" + portClient + "\n")
					txt_ip_SSH.close()
				elif status[0] == 1280: #Error server found but password does not match... somehow key is not on the Server
				#	print("Key not found... Trying to copy public key")
					ipStatus.write("no\n")
					#has public key been generated by client?
					key_status = commands.getoutput("ssh-keygen -b 2048 -t rsa -f /home/adminConsole/.ssh/id_rsa -q -N ''; echo '' ")
				#	print(key_status)
					key_status = commands.getoutput("echo 'Key generated... Trying to copy to the client'")
				#	print(key_status)
					#if public key doesn't exist this line creates it 
					key_status = commands.getoutput("sshpass -p '"+passClient+"' ssh-copy-id \
					    -o KbdInteractiveDevices=no  -o StrictHostKeyChecking=no "+userClient+"@"+ipAdClient+" -p "+portClient) 
				#	print(key_status) 
				else: #any other error
				#	print("Server not found")
					ipStatus.write("no\n")
				#print("***********************")
			file.close()
			i += 1
			ipStatus.close()
			time.sleep(10)
#---------------------MAIN-------------------------------#        
###########Daemonization part starts######################
app = App()
daemon_runner = runner.DaemonRunner(app)
daemon_runner.do_action()
###########Daemonization part ends########################