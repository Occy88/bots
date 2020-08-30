from utils import get_process_by_name
from utils import get_screenshot
import psutil
import subprocess
import pyautogui
import pygetwindow
HADES_STAR_PROGRAM_NAME = 'hadesstar.exe'
HADES_STAR_WINDOW_TITLE = "Hades' Star"
test='Device Manager'
def get_app(app_name):
    app = get_process_by_name(app_name)
    if not type(app) == psutil.Process:
        print("NO APP IDENTIFIED")
        exit(0)
    else:
        print("APP FOUND")
        return app


app = get_app(HADES_STAR_PROGRAM_NAME)

def prepare_window(w):
    # w.maximize()
    w.moveTo(2000, 2000)
import cv2
from time import time
loop_time = time()
window=pyautogui.getWindowsWithTitle(HADES_STAR_WINDOW_TITLE)
w=window[0]
prepare_window(w)
cv2.startWindowThread()
cv2.namedWindow("preview")
while app.is_running():

    img=get_screenshot(HADES_STAR_WINDOW_TITLE)
    k = cv2.waitKey(100) & 0XFF

    cv2.imshow("preview", img)    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()
    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv2.waitKey(1) == ord('q'):
        cv2.destroyAllWindows()
        break



