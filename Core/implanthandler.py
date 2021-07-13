import os



def RemoveTask(name):

	os.remove("listeners/implant/%s/tasks.enc" % name)
	print ("[+] Task is cleaned")

def ReceiveTask(result,name):

	print ("[+] %s Results" % name)
	dec_result =  DecryptString(result,key)
	print (dec_result)
