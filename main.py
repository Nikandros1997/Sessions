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
        ignored_apps = list()

        os.chdir(current_directory)

        if os.path.isfile('.ignore'):
            with open('.ignore', 'r') as text_file:
                for app in text_file:
                    ignored_apps.append(app.replace('\n', ''))

        with open(self.session_name + '-software.txt', "w") as text_file:
            for app in self.running_apps():
                if not app in ignored_apps:
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

    def close_apps(self):

        if os.path.isfile(self.session_name + '-software.txt'):
            with open(self.session_name + '-software.txt', "r") as text_file:
                for application in text_file:
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

        if os.path.isfile('.ignore'):
            print('Create an ignore file first by running: sh session -i ')

        # TODO: before running overriding the files make sure that the clipboard contains links, minimum number 3
        
        if(self.verify_clipboard()):
            self.save_tabs() # works
            self.save_running_software() # works
            self.close_apps()
        else:
            print('Please check your clipboard')

    def reload(self):

        if self.session_name == '':
            print('Error: session -r [name]')
            return

        self.reload_tabs() # works
        self.reload_running_software() # works

    def ignore(self, file_to_ignore):
        application_name = file_to_ignore

        if application_name == '':
            self.show_all_running_apps()
            print('Choose an app of the above to ignore')
        else:
            # check in applications folder if app exists
            # add to ignore file if it is

            if application_name in self.running_apps():

                os.chdir(current_directory)

                load_from_file = list()

                print('Ignore: ' + application_name)
                # create ignore file
                if os.path.isfile('.ignore'):
                    with open('.ignore', "r") as text_file:
                        for application in text_file:
                            load_from_file.append(application.replace('\n', ''))

                if not application_name in load_from_file:
                    load_from_file.append(application_name)
                else:
                    print('Application is already ignored')

                with open('.ignore', "w") as text_file:
                    for application in load_from_file:
                        text_file.write("%s\n" % application)

                # updated_software_list = list()

                '''with open(self.session_name + '-software.txt', 'r') as text_file:
                    for app in text_file:
                        print(app)'''
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

    print(len(sys.argv))
    argument = sys.argv[1]

    if not argument == '-i':
        print('UP')

        session_name = ''

        if len(sys.argv) == 3:
            session_name = sys.argv[2]

        app = App(session_name)

        app.func_switch(argument)
    else:
        ignore_app_name = ''
        session_name = ''

        print('down')

        if len(sys.argv) > 3:
            ignore_app_name = sys.argv[2]

            argument2 = sys.argv[3]

            if not argument2 == '-n':
                print('Something is wrong with the command format')
                sys.exit(0)
            else:
                session_name = sys.argv[4]

        app = App(session_name)

        app.func_switch(argument, ignore_app_name)


    print()

# Commands:
# -s [name]                         -> saves a session with name [name]
# -r [name]                         -> reloads a session with name [name]
# -i [app_name] -n [session_name]   -> ignores from storing in sessions app with name [name], when no [name] is provided lists all running apps
# -a                                -> shows all running apps
# -la                               -> lists all active sessions