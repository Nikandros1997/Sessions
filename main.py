import os, sys, webbrowser, pathlib, clipboard, psutil, subprocess

current_directory = os.getcwd()
class App():

    def __init__(self, session_name):
        self.session_name = session_name

    def save_tabs(self):
        text_in_clipboard = clipboard.paste()
        os.chdir(current_directory)
        with open(self.session_name + '-browser.txt', "w") as text_file:
            text_file.write("%s" % text_in_clipboard)
        os.chdir(current_directory)

    def reload_tabs(self):
        os.chdir(current_directory)
        with open(self.session_name + '-browser.txt', "r") as text_file:
            for l in text_file:
                webbrowser.get('chrome').open_new_tab(l)
        os.chdir(current_directory)

    def save_running_software(self):
        apps_location = '/Users/nikandrosmavroudakis'

        os.chdir(apps_location)

        application_folder = os.listdir('/Applications')

        # Removing The Extension From The App Name
        application_folder = [f.split('.')[0] for f in application_folder if '.app' in f]

        os.chdir(current_directory)

        with open(self.session_name + '-software.txt', "w") as text_file:
            for app in self.running_apps():
                text_file.write("%s\n" % app)

    def reload_running_software(self):
        apps_to_be_loaded = list()

        with open(self.session_name + '-software.txt', "r") as text_file:
            for application in text_file:
                apps_to_be_loaded.append(application.split('\n')[0] + '.app')
        
        apps_location = '/Users/nikandrosmavroudakis/Applications/'

        os.chdir(apps_location)

        for app in apps_to_be_loaded:
            open_app = 'open -a ' + app.replace(' ', r'\ ')
            os.system(open_app)

    def save(self):

        if self.session_name == '':
            print('Error: session -s [name]')
            return

        # TODO: before running overriding the files make sure that the clipboard contains links, minimum number 3

        self.save_tabs() # works
        self.save_running_software() # works

        # close all running apps other than the ignored
        # osascript -e 'quit app "Calendar"'

    def reload(self):

        if self.session_name == '':
            print('Error: session -r [name]')
            return

        self.reload_tabs() # works
        self.reload_running_software() # works

    def ignore(self):

        application_name = self.session_name

        if application_name == '':
            self.show_all_running_apps()
            print('Choose an app of the above to ignore')
        else:
            # check in applications folder if app exists
            # add to ignore file if it is

            print(self.running_apps())
            print(application_name)

            if application_name in self.running_apps():

                os.chdir(current_directory)

                load_from_file = list()

                print('Ignore: ' + application_name)
                # create ignore file
                if os.path.isfile('.ignore'):
                    with open('.ignore', "r") as text_file:
                        for application in text_file:
                            load_from_file.append(application)

                load_from_file.append(application_name)

                with open('.ignore', "w") as text_file:
                    for application in load_from_file:
                        text_file.write("%s\n" % application)
        
            else:
                print('You can ignore only running apps.')


    def running_apps(self, placeholder=None):
        apps_location = '/Users/nikandrosmavroudakis'

        os.chdir(apps_location)

        application_folder = os.listdir('/Applications')

        # Clearing App Name From The Extension
        application_folder = [f.split('.')[0] for f in application_folder if '.app' in f] # might be useless

        return [proc.info['name'] for proc in psutil.process_iter(attrs=['pid', 'name']) if proc.info['name'] in application_folder]

    def show_all_running_apps(self, placeholder=None):
        for app in self.running_apps():
            print(app)

    def list_active_sessions(self, placeholder=None):
        print('List all stored sessions')

    def func_switch(self, argument):
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
        return func()

if __name__ == "__main__":

    argument = sys.argv[1]

    session_name = ''

    print(len(sys.argv))

    if len(sys.argv) > 2:
        session_name = sys.argv[2]

    app = App(session_name)


    app.func_switch(argument)

    print()

# Commands:
# -s [name] -> saves a session with name [name]
# -r [name] -> reloads a session with name [name]
# -i [name] -> ignores from storing in sessions app with name [name], when no [name] is provided lists all running apps
# -a        -> shows all running apps
# -la       -> lists all active sessions