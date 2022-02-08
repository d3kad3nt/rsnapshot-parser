#!/usr/bin/env python3

import subprocess

encoding="UTF-8"

def printconfig(config):
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
	with open("/etc/rsnapshot.conf", 'r', encoding = encoding) as config:
		printconfig(config)

if __name__ == "__main__":
	main()


