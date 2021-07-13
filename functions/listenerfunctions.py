import netifaces as ni
import requests


from tabulate import tabulate
from time import sleep


from Core import listener,color,database


def StartListener(command,conn):
	try:
		command = command.split()

		try:

			listener_name = command[2]
			listener_ip = ni.ifaddresses(command[3])[ni.AF_INET][0]['addr']
			listener_port = command[4]

			results = database.return_token(conn,listener_name)

			if not results:
				res = database.start_listener(conn,listener_ip,listener_port,listener_name)

				if (res):

					try:

						listener.start(listener_ip,listener_port)
						sleep(0.5)

					except:

						print ("[%s] Cannot start the listener on %s:%s" % (color.red("-"),listener_ip,listener_port))
			else:

				print ("[%s] %s Listener found!!" % (color.red("-"),listener_name))

		except:

			print ("[%s] Wrong interface" % color.red("-"))

	except:

		print ("[%s] There an error found!!" % color.red("-"))

def StopListener(command,conn):

	try:

		name = command.split()[2]

		results = database.return_token(conn,name)

		if results:

			for i in range(0,len(results)):
				try:
					url = "http://%s:%s/shutdown/%s/%s" % (results[i][1],results[i][2],name,results[i][0])
					req = requests.get(url)

					if int(req.status_code) == 200:

						print ("[%s] %s Listener stopped" % (color.green("+"),name))

						database.delete_listener(conn,results[i][0])

						print ("[%s] %s Listener deleted" % (color.green("+"),name))

				except:

					print ("[%s] %s Listener is not running, run the listener first." % (color.red("-"),name))
		else:

			print ("[%s] %s Listener found!!" % (color.red("-"),name))

	except:

			print ("[%s] There an error found!!" % color.red("-"))

def ReloadListener(conn):

	results = database.run_listener(conn)

	if (results):

		for i in range(0, len(results)):

			listener.start(results[i][0],results[i][1])
			sleep(0.5)

		print ("[%s] Listeners is up" % color.green("+"))

	else:

		print ("[%s] Database has no listeners yet!" % color.red("-"))

def ListListener(conn):


	results = database.list_listener(conn)
	data = []

	for i in range(0,len(results)):

		data.append([results[i][0],results[i][1],results[i][2]])

	print("\n",tabulate(data, headers=["Listener Name", "Listener IP","Listener Port"]),"\n")






