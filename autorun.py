from __future__ import division
import os
import time
import sys
import shutil

#TO DO:
#	Time stamping with a variable interval determined by command timestamp <timeInterval>
#	Add repeat loop

class commander:
	updateTimeInterval = 5
	timestampInterval = 5*60
	cmdFile = os.getcwd() + "/cmd"
	initDir = os.getcwd()
	
	def __init__(this):
		print this.cmdFile
	
	def executeCommand(this, cmd):
		#Special commands
		split = [c.strip() for c in cmd.split(' ')]
		#Change working directory
		if(split[0] == "cd"):
			if(len(split) == 1):
				os.chdir(os.expanduser("~/"))
			else:
				if(os.path.isdir(split[1])):
					os.chdir(split[1])
			return
		#Execute file
		if(split[0] == "execute"):
			this.run(split[1])
			return
		#change update interval
		if(split[0] == "update"):
			#No number specified
			if(len(split) == 1):
				return
			try:
				this.updateTimeInterval = float(split[1])
			except ValueError:
				print "Error, %s not an integer."%split[1]
			return
		#Change cmd file
		if(split[0] == "cmd"):
			if(len(split) != 1):
				this.cmdFile = os.getcwd() + "/" + split[1]
			return
		#Execute bash command
		os.system(cmd)
	
	def executeLine(this, command):
		#Remove all comments
		command = command.split('#')[0]
		command = command.strip()
		#Splits line in different commands separated by a ';'
		commands = command.split(';')
		for cmd in commands:
			#Empty line
			if(command == ''):
				continue
			this.executeCommand(cmd)
	
	def run(this, filename = None):
		sleep = False
		if(filename == None):
			filename = this.cmdFile
			sleep = True
		#If not a file
		if(not os.path.exists(filename)):
			if(sleep):
				time.sleep(this.updateTimeInterval)
			return
		#Remove if a directory
		if(os.path.isdir(filename)):
			shutil.rmtree(filename)
			if(sleep):
				time.sleep(this.updateTimeInterval)
			return
		if(sleep):
			time.sleep(this.updateTimeInterval)
		#Run commands in file
		f = open(filename, 'r')
		for line in f:
			this.executeLine(line)
		f.close()
		if(os.path.exists(filename)):
			if(sleep):
				os.remove(filename)
		os.chdir(this.initDir)

cmd = commander()
while True:
	cmd.run()
