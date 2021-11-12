#!/usr/bin/env python3

import argparse

def getArgparser() -> argparse.ArgumentParser:
	parser = argparse.ArgumentParser(description='This program is used to format the output of rsnapshot and output it to different backends')
	parser.add_argument('-o', '--output', nargs='+', required=True)
	return parser

def main():
	argparser = getArgparser()
	args = argparser.parse_args()

if (__name__ == "__main__"):
	main()