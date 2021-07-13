#!/usr/bin/python3

from Core import color,database
from functions import banner,main




if __name__ == "__main__":


	print ("[%s] Strating database" % color.green("+"))
	conn = database.connect()


	clear_db = input("[%s] Do you to delete the old database (Y/N):: " % color.blue("*")).lower()

	if clear_db.replace(" ","") == "y":

			database.clear_database(conn)

	banner.print_banner()

	main.start(conn)
