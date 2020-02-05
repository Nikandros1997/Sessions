import os, sys
import webbrowser
import pathlib
import clipboard
import psutil

current_directory = os.getcwd()

def save_tabs(session_name):
    text_in_clipboard = clipboard.paste()
    print(text_in_clipboard)
    os.chdir(current_directory)
    with open(session_name + '-browser.txt', "w") as text_file:
        text_file.write("%s" % text_in_clipboard)
    os.chdir(current_directory)

def reload_tabs(session_name):
    os.chdir(current_directory)
    with open(session_name + '-browser.txt', "r") as text_file:
        for l in text_file:
            webbrowser.get('chrome').open_new_tab(l)
            print(l)
    os.chdir(current_directory)

def save_running_software(session_name):
    print('save_running_software')

    apps_location = '/Users/nikandrosmavroudakis'

    os.chdir(apps_location)

    files = os.listdir('/Applications')

    # Clearing App Name From The Extension
    files = [f.split('.')[0] for f in files if '.app' in f]

    os.chdir(current_directory)

    with open(session_name + '-software.txt', "w") as text_file:
        for proc in psutil.process_iter(attrs=['pid', 'name']):
            running_app = proc.info['name']

            if running_app in files:
                text_file.write("%s\n" % running_app)



def reload_running_software(session_name):
    print('restore_running_software')

def save(session_name):
    # save_tabs(session_name)
    save_running_software(session_name)

def reload(session_name):
    reload_tabs(session_name)
    reload_running_software(session_name)

def func_switch(argument, session_name):
    switcher = {
        '-s': save,
        '-r': reload,
    }
    # Get the function from switcher dictionary
    func = switcher.get(argument, lambda: "nothing")
    # Execute the function
    return func(session_name)

if __name__ == "__main__":
    argument = sys.argv[1]
    session_name = sys.argv[2]
    func_switch(argument, session_name)


# https://olaraundeuord.wordpress.com/2017/08/04/save-and-reload-all-open-chrome-tabs-with-copyallurlspythonapplescript/