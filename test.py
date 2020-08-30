from utils import get_process_by_name
import psutil
import subprocess
import pyautogui
import pygetwindow
HADES_STAR_PROGRAM_NAME = 'hadesstar.exe'

def get_app(app_name):
    app = get_process_by_name(app_name)
    if not type(app) == psutil.Process:
        print("NO APP IDENTIFIED")
        exit(0)
    else:
        "APP FOUND"
        return app


app = get_app(HADES_STAR_PROGRAM_NAME)
while app.is_running():
    print(dir(pyautogui))
    windows=pyautogui.getAllWindows
    for w in windows:
        print(dir(w))
    files = app.open_files()
    print(len(files))
    for f in files:
        print(f.path)
    print(dir(app))
    break
