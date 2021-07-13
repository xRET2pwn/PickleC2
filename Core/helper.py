"""
This part to print the help menu
"""
from tabulate import tabulate

def help():
	data = [['help', 'That command will display the help menu.'],
	['help {option}', 'That command will display the help menu of the option.'],
	['listener', 'That command will start a listener'],
	['implant','That command will generate a implant.'],
	['interact','That command will interact with the implant.'],
	['list {options}','That command will display the list menu of the option ex: list implant - list listener'],
	['exit','Force Exit']]

	return (tabulate(data, headers=["Options", "Description"]))


def list_listener_option():

	data = [['http','This listener is running under http protocol']]

	return (tabulate(data, headers=["Options", "Description"]))



def list_implant_lang():

	data = [['powershell','This is a powershell implant'],
	['go','This is a go implant']]

	return (tabulate(data, headers=["Options", "Description"]))



def help_listener():


	data = [['Start','listener start <listener_name> <listener_Interface> <listener_Port>'],
	['Stop','listener stop <name>'],
	['load','listener load'],
	['Active', 'listener list']]

	return (tabulate(data, headers=["Action", "Example"]))


def help_implant():

	data = [['Generate','implant generate <listener_name> <Implant_Lang> <Implant_Name>'],
	['Active', 'implant list']]

	return (tabulate(data, headers=["Action", "Example"]))

def help_interact():

	data = [['Interact','interact <Implant_Name>']]

	return (tabulate(data, headers=["Action", "Example"]))



def help_interact2():


	data = [['help','That command will display the help menu.'],
	['powershell','Execute a powershell command ex: powershell whoami'],
	['cmd','Execute a cmd command ex: cmd whoami'],
	['module','Load a selected module'],
	['list module', 'That command will display a list of modules'],
	['back','Return back'],
	['sleep','Set a Delay in seconds'],
	['exit','Exit the Implant']]

	return (tabulate(data, headers=["Option", "Description"]))


