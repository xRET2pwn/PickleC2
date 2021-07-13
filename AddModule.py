#!/usr/bin/python3
import sqlite3
import argparse


def Add_Module(module_name, module_desc,module_path):

	try:
		database = "database.db"
		conn = sqlite3.connect(database)
		results = Check_Module(conn,module_name)
		if not results:
			conn.cursor()
			conn.execute("INSERT INTO modules(Module_Name,Module_Description,Module_Path) VALUES('%s','%s','%s')" % (module_name, module_desc,module_path))
			conn.commit()
			print ("Added successfully")
		else:

			print ("%s module name found!!" % module_name)
	except:
		print ("Can not add the script")


def Check_Module(conn,name):
	conn.cursor()
	results = conn.execute("SELECT Module_Name FROM modules WHERE Module_Name='%s'" % name )
	results = results.fetchall()
	return results

if __name__ == '__main__':
	parser = argparse.ArgumentParser()

	parser.add_argument('-n', '--name', type=str, help='Add the module name', required=True)
	parser.add_argument('-d', '--description', type=str, help='Add the module Description', required=True)
	parser.add_argument('-p', '--path', type=str, help='Add the module path.', required=True)

	args = parser.parse_args()

	Add_Module(args.name,args.description,args.path)


