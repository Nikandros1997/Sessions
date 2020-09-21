import sys
from .App import App
import os, sys, webbrowser, pathlib, clipboard, psutil, subprocess

def main():
	argument = sys.argv[1]
	if not argument == '-i':
		session_name = ''

		if len(sys.argv) == 3:
			session_name = sys.argv[2]

		app = App(session_name)

		app.func_switch(argument)
	else:
		ignore_app_name = sys.argv[2]
		session_name = ''

		try:
			argument2 = sys.argv[3]
		except:
			print('Something is wrong with the command format')
			sys.exit(0)
		
		try:
			session_name = sys.argv[4]
		except:
			print('Session name has not been specified')
			sys.exit(0)

		app = App(session_name)

		app.func_switch(argument, ignore_app_name)

		print('')

if __name__ == '__main__':
    main()
