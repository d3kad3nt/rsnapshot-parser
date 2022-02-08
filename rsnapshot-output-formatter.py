#!/usr/bin/env python3

import argparse
import os

UTF_8 = "UTF-8"

def getArgparser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description='This program is used to format the output of rsnapshot and output it to different backends')
	parser.add_argument('-o', '--output', nargs='+', required=True)
	parser.add_argument('-i', '--input', required=True)
	return parser

def getBackupFolder(rsnapshotLog):
	#The first action on the backup folder is to remove the oldest backup. This is used to detect the backup Folder
	backupFolder = os.path.dirname([ match for match in rsnapshotLog if "rm -rf" in match][0].strip().split(" ")[-1][:-1])
	return backupFolder

def findBackupPoints(rsnapshotLog, backupFolder):
	backupPoints = []
	backupPoint = []
	tempFolderCreation = "mkdir -m 0755 -p {}/tmp/".format(backupFolder) 
	for line in rsnapshotLog:
		if tempFolderCreation in line:
			backupPoints.append(backupPoint)
			backupPoint = []
		backupPoint.append(line)
	backupPoints.append(backupPoint)
	return backupPoints[1:]

class BackupPoint:
	pass

def parseBackupPoints(loggedBackupPoints, backupFolder):
	for loggedBackupPoint in loggedBackupPoints:
		pass

def parseRsnapshotLog(rsnapshotLog):
	backupFolder = getBackupFolder(rsnapshotLog)
	backupPoints = findBackupPoints(rsnapshotLog, backupFolder)
	print(len(backupPoints))

	parsedBackupPoints = parseBackupPoints(backupPoints, backupFolder)
	pass

def readFile(filename:str):
	with open(filename, 'r', encoding='utf8') as logfile:
		lines = logfile.readlines()
	return lines

def getConfig(args):
	configfile = ""
	if args.configfile:
		configfile = args.configfile
		if not os.path.isfile(configfile):
			Exception("The configfile {} doesn't exist.".format(configfile))
	else:
		configfile = "/etc/rsnapshot.conf"
	with open(configfile, 'r', encoding=UTF_8) as config:
		parseConfig(config)

def parseConfig(config):
	for line in config:
		if line.startswith("#"):
			continue
		elif "include_conf" in line:
			command = line.split("\t")[1].replace("`", "")
			out = subprocess.check_output(command.split(), shell=True, encoding = encoding)
			printconfig(out.split("\n"))
		else:
			strippedLine = line.strip()
			if strippedLine:
				print(strippedLine)

def main():
	argparser = getArgparser()
	args = argparser.parse_args()
	config = getConfig(args)
	rsnapshotLog = readFile(args.input)
	parsedLog = parseRsnapshotLog(rsnapshotLog)

if (__name__ == "__main__"):
	main()