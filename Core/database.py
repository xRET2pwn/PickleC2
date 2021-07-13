import sqlite3
import random
import string


def connect():

	try:
		conn = sqlite3.connect("database.db")
		return conn
	except:
		print ("[-] Cannot find the database!!")
		exit()


def start_listener(connector,listener_ip,listener_port,listener_name):

	letters = string.ascii_lowercase
	Token = ''.join(random.choice(letters) for i in range(32))

	try:
		connector.cursor()
		connector.execute("INSERT INTO Listener(Listener_Name,Listener_IP,Listener_Port,Listener_Token) VALUES('%s','%s','%s','%s')" % (listener_name, listener_ip, listener_port, Token))
		connector.commit()
		return True

	except sqlite3.Error as error:

		print ("[-] Cannot record the listener in the database!!")
		print (error)
		return False


def delete_listener(connector,listener_token):

	try:
		connector.cursor()
		connector.execute("DELETE FROM Listener WHERE Listener_Token='%s'" % listener_token)
		connector.commit()
		return True

	except:

		print ("[-] Cannont delete the listener!!")
		return False




def return_token(connector,listener_name):

        try:

                connector.cursor()
                results = connector.execute("SELECT Listener_Token, Listener_IP, Listener_Port FROM Listener WHERE Listener_Name='%s'" % listener_name)
                results = results.fetchall()

                return results

        except:

                print ("[-] Cannot retrieve the token!!")
                return False



def check_token(connector,listener_name,listener_token):


	try:

		connector.cursor()
		results = connector.execute("SELECT Listener_Token FROM Listener WHERE Listener_Name='%s'" % listener_name)
		results = results.fetchall()

		if results[0][0] == listener_token:
			return True

		return False

	except:

		print ("[-] Cannot retrieve the token!!")
		return False


def list_listener(connector):

	try:

		connector.cursor()
		results = connector.execute("SELECT Listener_Name, Listener_IP, Listener_Port FROM Listener")
		results = results.fetchall()

		return results

	except:

		print ("[-] Cannot retrieve the Active Listener")
		return False

def run_listener(connector):


	try:

		connector.cursor()
		results = connector.execute("SELECT Listener_IP,Listener_Port FROM Listener")
		results = results.fetchall()
		return results

	except:

		print ("[-] Cannot retrieve previous listeners!!")
		return False

def clear_database(connector):

	try:

		connector.cursor()
		connector.execute("DELETE FROM Listener")
		connector.commit()
		connector.execute("DELETE FROM Implant_Info")
		connector.commit()

		return True

	except:

		print ("[-] Cannot delete the old listeners")
		return False


def Save_Implant(name):


	try:
		connect = sqlite3.connect("database.db")

		connect.cursor()

		connect.execute("Update Implant_Info set Active = '1' where Implant_Name = '%s'" % name)

		connect.commit()

		return True

	except:
		print ("Error")

	return False

def list_implant(conn):

	conn.cursor()
	results = conn.execute("SELECT Implant_Name FROM Implant_Info WHERE Active='1'")
	results = results.fetchall()
	return results

def rec_implant(conn,implant_name,key,listener_name,listener_ip,listener_port):

	conn.cursor()
	conn.execute("INSERT INTO Implant_Info(Implant_Name,Implant_Key,Listener_Name,Listener_Port,Listener_IP) VALUES('%s','%s','%s','%s','%s')" % (implant_name,key,listener_name,listener_port,listener_ip))
	conn.commit()
	return True



def return_key(connect,name):


	connect.cursor()

	results = connect.execute("SELECT Implant_Key FROM Implant_Info WHERE Implant_Name='%s'" % (name))

	results = results.fetchall()

	return results


def ChangeImplantName(connect,old_name,name):


	try:
		connect.cursor()

		connect.execute("Update Implant_Info set Implant_OldName='%s' where Implant_Name = '%s'" % (old_name,old_name))

		connect.commit()

		connect.execute("Update Implant_Info set Implant_Name='%s' where Implant_OldName = '%s'" % (name,old_name))

		connect.commit()

		return True

	except:

		return False


def list_module(connect):

	try:

		connect.cursor()
		results = connect.execute("SELECT Module_Name,Module_Description,Module_Path FROM modules")
		results = results.fetchall()

		return results
	except:

		return False


def return_rename_key(connect,name):


	connect.cursor()

	results = connect.execute("SELECT Implant_Key FROM Implant_Info WHERE Implant_OldName='%s'" % (name))

	results = results.fetchall()

	return results

def Delete_Active_Implant(connect,name):

	connect.cursor()

	connect.execute("DELETE FROM Implant_Info WHERE Implant_Name='%s'" % name)
	connect.commit()

	return True
