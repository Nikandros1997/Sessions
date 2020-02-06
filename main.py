import os, sys, webbrowser, pathlib, clipboard, psutil, subprocess

current_directory = os.getcwd()
class App():
	def __init__(self, session_name):
		self.session_name = session_name

	def save_tabs(self):
		text_in_clipboard = clipboard.paste()
		os.chdir(current_directory)
		with open(self.session_name + '-browser.ses', "w") as text_file:
			text_file.write("%s" % text_in_clipboard)
		os.chdir(current_directory)

	def reload_tabs(self):
		os.chdir(current_directory)
		with open(self.session_name + '-browser.ses', "r") as text_file:
			for l in text_file:
				webbrowser.get('chrome').open_new_tab(l)
		os.chdir(current_directory)

	def save_running_software(self):
		apps_location = '/Users/nikandrosmavroudakis'

		os.chdir(apps_location)

		application_folder = os.listdir('/Applications')

		# Removing The Extension From The App Name
		application_folder = [f.split('.')[0] for f in application_folder if '.app' in f]
		ignored_apps = list()

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
			print('close apps')
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

	def save(self):
		if self.session_name == '':
			print('Error: session -s [name]')
			return

		# print(self.running_apps())
		# return

		if not os.path.isfile('.ignore'):
			print('Create an ignore file first by running: sh session -i ')

		if(self.verify_clipboard()):
			self.save_tabs() # works
			self.save_running_software() # works
			self.close_apps() # works
		else:
			print('Please check your clipboard')

	def reload(self):
		if self.session_name == '':
			print('Error: session -r [name]')
			return

		self.reload_tabs() # works
		self.reload_running_software() # works

	def reload_file(self, file_name):
		loaded_from_file = list()

		with open(file_name, "r") as text_file:
			for application in text_file:
				application = application.replace('\n', '')
				loaded_from_file.append(application)

		return loaded_from_file

	def save_file(self, file_name, data):
		print('save_file')
		with open(file_name, "w") as text_file:
			for application in data:
				text_file.write("%s\n" % application)

	def ignore(self, file_to_ignore):
		application_name = file_to_ignore

		print(file_to_ignore)

		if application_name == '':
			self.show_all_running_apps()
			print('Choose an app of the above to ignore')
		else:
			if application_name in self.running_apps():
				os.chdir(current_directory)

				if os.path.isfile(self.session_name + '-software.ses'):
					load_from_file = list()

					print('Ignore: ' + application_name)

					# create ignore file
					if os.path.isfile('.ignore'):
						load_from_file = self.reload_file('.ignore')

					if not application_name in load_from_file:
						load_from_file.append(application_name)
					else:
						print('Application is already ignored')

					self.save_file('.ignore', load_from_file)

					updated_software_list = list()

					updated_software_list = self.reload_file(self.session_name + '-software.ses')

					updated_software_list = [ app.strip() for app in updated_software_list if not app.strip() in load_from_file]

					self.save_file(self.session_name + '-software.ses', updated_software_list)
				else:
						print('Session name not registered.')
			else:
					print('You can ignore only running apps.')

	def running_apps(self, placeholder=None):
		apps_location = '/Users/nikandrosmavroudakis'

		os.chdir(apps_location)

		application_folder = os.listdir('/Applications')

		# Clearing App Name From The Extension
		application_folder = [f.split('.')[0].lower() for f in application_folder if '.app' in f] # might be useless

		return [proc.info['name'] for proc in psutil.process_iter(attrs=['pid', 'name']) if proc.info['name'].lower() in application_folder]
		# return [proc.info['name'].lower() for proc in psutil.process_iter(attrs=['pid', 'name'])]
	def show_all_running_apps(self, placeholder=None):
		for app in self.running_apps():
			print(app)

	def list_active_sessions(self, placeholder=None):
		print('Active Sessions:')
		os.chdir(current_directory)

		application_folder = os.listdir()

		application_folder = list(set([f.split('-')[0] for f in application_folder if f.endswith('.ses')]))

		for session in application_folder:
			print(session)

	def func_switch(self, argument, passing=None):
		switcher = {
			'-s': self.save,
			'-r': self.reload,
			'-i': self.ignore,
			'-a': self.show_all_running_apps,
			'-la': self.list_active_sessions
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


# Commands:
# -s [name]                         -> saves a session with name [name]
# -r [name]                         -> reloads a session with name [name]
# -i [app_name] -n [session_name]   -> ignores from storing in sessions app with name [name], when no [name] is provided lists all running apps
# -a                                -> shows all running apps
# -la                               -> lists all active sessions