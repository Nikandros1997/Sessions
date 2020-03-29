import os, sys, webbrowser, pathlib, clipboard, psutil, subprocess

current_directory = pathlib.Path(__file__).parent.absolute()

# print(pathlib.Path(__file__).parent.absolute())
class App():
	def __init__(self, session_name):
		self.session_name = session_name

	def save_tabs(self):

		if not self.can_store_tabs():
			return

		text_in_clipboard = clipboard.paste()
		os.chdir(current_directory)
		with open(self.session_name + '-browser.ses', "w") as text_file:
			text_file.write("%s" % text_in_clipboard)
		os.chdir(current_directory)

	def reload_tabs(self):
		if not self.can_store_tabs():
			return

		os.chdir(current_directory)
		with open(self.session_name + '-browser.ses', "r") as text_file:
			for l in text_file:
				webbrowser.get('chrome').open_new_tab(l)
		os.chdir(current_directory)

	def save_running_software(self):
		# Removing The Extension From The App Name
		# application_folder = [f.split('.')[0] for f in application_folder if '.app' in f]
		ignored_apps = list()
		print(current_directory)
		os.chdir(current_directory)

		if os.path.isfile('.ignore'):
			with open('.ignore', 'r') as text_file:
				for app in text_file:
					ignored_apps.append(app.replace('\n', ''))

		with open(self.session_name + '-software.ses', "w") as text_file:
			for app in self.running_apps():
				if not app in ignored_apps:
					text_file.write("%s\n" % app)

	def reload_running_software(self):
		apps_to_be_loaded = list()

		with open(self.session_name + '-software.ses', "r") as text_file:
			for application in text_file:
				apps_to_be_loaded.append(application.split('\n')[0] + '.app')
		
		apps_location = '/Users/nikandrosmavroudakis/Applications/'

		os.chdir(apps_location)

		for app in apps_to_be_loaded:
			open_app = 'open -a ' + app.replace(' ', r'\ ')
			os.system(open_app)

	def close_apps(self):

		os.chdir(current_directory)

		if os.path.isfile(self.session_name + '-software.ses'):
			print('closing all apps')
			with open(self.session_name + '-software.ses', "r") as text_file:
				for application in text_file:
					# print('osascript -e \'quit app "{0}"\''.format(application.split('\n')[0] + '.app'))
					os.system('osascript -e \'quit app "{0}"\''.format(application.split('\n')[0] + '.app'))
	
	def verify_clipboard(self):

		links = clipboard.paste()

		links = links.split('\n')

		for link in links[:-1]:
			if not (link.startswith('http://') or link.startswith('https://')):
				return False

		return len(links) > 3

	def can_store_tabs(self):
		os.chdir(current_directory)

		return os.path.isfile(self.session_name + '-software.ses') and os.path.isfile(self.session_name + '-browser.ses') or not os.path.isfile(self.session_name + '-software.ses') and not os.path.isfile(self.session_name + '-browser.ses')

	def save(self):
		if self.session_name == '':
			print('Error: session -s [name]')
			return
		elif self.can_store_tabs() and not self.verify_clipboard():
			# if not os.path.isfile(self.session_name + '-browser.ses') and 
			print('Please check your clipboard')
			return
		elif not os.path.isfile('.ignore'):
			print('Create an ignore file first by running: sh session -i ')
			return

		self.save_tabs() # works
		self.save_running_software() # works
		self.close_apps() # works

	def reload(self):
		if self.session_name == '':
			print('Error: session -r [name]')
			return
		elif not os.path.isfile(self.session_name + '-software.ses'):
			print('Not anything stored, yet.')
			return

		self.reload_tabs() # works
		self.reload_running_software() # works

	def load_file(self, file_name):
		loaded_from_file = list()
		os.chdir(current_directory)
		

		with open(file_name, "r") as text_file:
			for application in text_file:
				application = application.replace('\n', '')
				loaded_from_file.append(application)

		return loaded_from_file

	def save_file(self, file_name, data):
		with open(file_name, "w") as text_file:
			for application in data:
				text_file.write("%s\n" % application)

	def ignore(self, app_to_ignore):
		application_name = app_to_ignore

		if application_name == '':
			self.show_all_running_apps()
			print('Choose an app of the above to ignore')
		else:
			if application_name in self.running_apps():
				os.chdir(current_directory)

				if os.path.isfile(self.session_name + '-software.ses'):

					apps_to_be_ignored = list()

					if os.path.isfile('.ignore'):
						apps_to_be_ignored = self.load_file('.ignore')

					if not application_name in apps_to_be_ignored:
						print('Ignore: ' + application_name)
						apps_to_be_ignored.append(application_name)
					else:
						print(application_name + ' won\'t be ingored anymore.')
						apps_to_be_ignored.remove(application_name)

					self.save_file('.ignore', apps_to_be_ignored)

					old_software_list = self.load_file(self.session_name + '-software.ses')

					updated_software_list = [ app.strip() for app in old_software_list if not app.strip() in apps_to_be_ignored]

					self.save_file(self.session_name + '-software.ses', updated_software_list)
				else:
					print('Session not registered.')
			else:
				print('You can ignore apps that are currently running.')
				print(app_to_ignore)

	def running_apps(self):
		output = subprocess.check_output('ps aux|grep ^nikandrosmavroudakis | grep /Applications', shell=True)
		running_apps = []
		# print(output)
		for line in str(output).split('\\n'):
			x = line[line.find('/Applications'):]
			y = x[:x.find('.app')]
			z = y[y.rfind('/')+1:]
			if not z in running_apps and z != '' and z != 'Application':
				running_apps.append(z)

		return running_apps

	def show_all_running_apps(self, placeholder=None):
		apps_to_be_ignored = self.load_file('.ignore')

		for app in self.running_apps():
			print(app, '(Ignored)' if app in apps_to_be_ignored else '')

	def get_active_sessions(self):
		os.chdir(current_directory)

		application_folder = os.listdir()

		return list(set([f.split('-')[0] for f in application_folder if f.endswith('.ses')]))


	def list_active_sessions(self, placeholder=None):
		print('Active Sessions:')

		for session in self.get_active_sessions():
			print(session)

	def decouple_apps_from_tabs(self):

		os.chdir(current_directory)

		# if browser file exists
		if self.can_store_tabs():
			print('Are you sure that you don\'t want to store the browser\'s tabs anymore?')
			answer = input()
			if answer == 'y':
				if os.path.isfile(self.session_name + '-browser.ses'):
					os.remove(self.session_name + '-browser.ses')
				else:
					open(self.session_name + '-software.ses', 'w')
			else:
				print('no changes applied')
		# else if browser file does not exist
		else:
			print('Do you want to start being able to store the browser\'s tabs in the session?')
			answer = input()
			if answer == 'y':
				open(self.session_name + '-browser.ses', 'w')
			else:
				print('no changes applied')

	def show_only_apps_not_ignored(self):
		apps_to_be_ignored = self.load_file('.ignore')

		formatted_string = ''

		for app in self.running_apps():
			if not app in apps_to_be_ignored:
				formatted_string += app + ','
		print(formatted_string)

	def show_active_sessions(self):
		formatted_string = ''

		for session in self.get_active_sessions():
			formatted_string += session + ','
		print(formatted_string)

	def help(self):
		print('-s [ssn_n]\t: store a new or update an existing session')
		print('-r [ssn_n]\t: restores a stored session')
		print()
		print('-i [app_n] -n [ssn_n]\t: ignores an app for a specific session')
		print()
		print('-d\t: decouples storage of apps from browser tabs')
		print('-a\t: displays all the running applications')
		print('-la\t: displays all the active sessions')


	def func_switch(self, argument, passing=None):
		switcher = {
			'-s' : self.save,
			'-r' : self.reload,
			'-i' : self.ignore,
			'-a' : self.show_all_running_apps,
			'-k' : self.show_only_apps_not_ignored,
			'-n' : self.show_active_sessions,
			'-la': self.list_active_sessions,
			'-d' : self.decouple_apps_from_tabs,
			'-h' : self.help,
		}
		# Get the function from switcher dictionary
		func = switcher.get(argument, lambda: "nothing")
		# Execute the function

		if(func.__name__ == 'ignore'):
			return func(passing)
		else:
			return func()

if __name__ == "__main__":
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
