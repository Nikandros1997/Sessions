import os, sys
import webbrowser
import pathlib
import clipboard
import psutil
import subprocess

current_directory = os.getcwd()

def save_tabs(session_name):
    text_in_clipboard = clipboard.paste()
    os.chdir(current_directory)
    with open(session_name + '-browser.txt', "w") as text_file:
        text_file.write("%s" % text_in_clipboard)
    os.chdir(current_directory)

def reload_tabs(session_name):
    os.chdir(current_directory)
    with open(session_name + '-browser.txt', "r") as text_file:
        for l in text_file:
            webbrowser.get('chrome').open_new_tab(l)
    os.chdir(current_directory)

def save_running_software(session_name):
    apps_location = '/Users/nikandrosmavroudakis'

    os.chdir(apps_location)

    application_folder = os.listdir('/Applications')

    # Clearing App Name From The Extension
    application_folder = [f.split('.')[0] for f in application_folder if '.app' in f] # might be useless

    os.chdir(current_directory)

    with open(session_name + '-software.txt', "w") as text_file:
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            running_app = proc.info['name']

            if running_app in application_folder:
                text_file.write("%s\n" % running_app)

def reload_running_software(session_name):
    apps_to_be_loaded = list()

    with open(session_name + '-software.txt', "r") as text_file:
        for application in text_file:
            apps_to_be_loaded.append(application.split('\n')[0] + '.app')
    
    apps_location = '/Users/nikandrosmavroudakis/Applications/'

    os.chdir(apps_location)

    for app in apps_to_be_loaded:
        open_app = 'open -a ' + app.replace(' ', r'\ ')
        os.system(open_app)
        # print(asdf) osascript -e 'quit app "Calendar"'



def save(session_name):

    if session_name == '':
        print('Error: session -s [name]')
        return

    save_tabs(session_name) # works
    save_running_software(session_name) # works

def reload(session_name):

    if session_name == '':
        print('Error: session -r [name]')
        return

    reload_tabs(session_name) # works
    reload_running_software(session_name) # works

def ignore(application):

    if application == '':
        running_apps()
        print('Choose an app of the above to ignore')
    else:
        # check in applications folder if app exists
        # add to ignore file if it is
        print('Ignore: ' + application)
        print('You can ignore only running apps.')

def running_apps(placeholder=None):
    apps_location = '/Users/nikandrosmavroudakis'

    os.chdir(apps_location)

    application_folder = os.listdir('/Applications')

    # Clearing App Name From The Extension
    application_folder = [f.split('.')[0] for f in application_folder if '.app' in f] # might be useless

    for proc in psutil.process_iter(attrs=['pid', 'name']):
        running_app = proc.info['name']
        if running_app in application_folder:
            print("%s" % running_app)

def list_active_sessions(placeholder=None):
    print('List all stored sessions')

def func_switch(argument, session_name):
    switcher = {
        '-s': save,
        '-r': reload,
        '-i': ignore,
        '-a': running_apps,
        '-la': list_active_sessions
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "nothing")
    # Execute the function
    return func(session_name)

if __name__ == "__main__":
    argument = sys.argv[1]

    session_name = ''

    print(len(sys.argv))

    if len(sys.argv) > 2:
        session_name = sys.argv[2]

    func_switch(argument, session_name)

    print()

# Commands:
# -s [name] -> saves a session with name [name]
# -r [name] -> reloads a session with name [name]
# -i [name] -> ignores from storing in sessions app with name [name], when no [name] is provided lists all running apps
# -a        -> shows all running apps
# -la       -> lists all active sessions