import os, sys
import Tkinter
import webbrowser

desktop_path = ‘/Users/username/Desktop’

def save():
cwd = os.getcwd()
root = Tkinter.Tk()
root.withdraw() # Hide the main window (optional)
text_in_clipboard = root.clipboard_get()
print text_in_clipboard
os.chdir(desktop_path)
with open(“temp.txt”, “w”) as text_file:
text_file.write(“%s” % text_in_clipboard)
os.chdir(cwd)

def reload():
cwd = os.getcwd()
os.chdir(desktop_path)
with open(“temp.txt”, “r”) as text_file:
for l in text_file:
webbrowser.get(‘chrome’).open_new_tab(l)
print l
os.chdir(cwd)

def func_switch(argument):
switcher = {
0: save,
1: reload,
}
# Get the function from switcher dictionary
func = switcher.get(argument, lambda: “nothing”)
# Execute the function
return func()

if __name__ == “__main__”:
argument = int(sys.argv[1])
func_switch(argument)