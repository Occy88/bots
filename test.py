from utils import get_process_by_name
from utils import get_screenshot
import psutil
import subprocess
import pyautogui
import pygetwindow
import numpy as np
import psutil
import win32gui
import win32ui
import win32con
import cv2
from ctypes import windll
from PIL import Image

import cv2
from time import time

PROGRAM_NAME = 'hadesstar.exe'
WINDOW_TITLE = "Hades' Star"
test = 'Device Manager'

import threading
class Win32Wrapper():
    def __init__(self, window_title):
        self.win_32_window = win32gui.FindWindow(None, window_title)
        self.update_properties()
        print('properties updated, starting thread')

        print('window thread complete')

    def update_properties(self):
        self.left, self.top, self.right, self.bottom = win32gui.GetWindowRect(self.win_32_window)
        self.height = self.bottom - self.top
        self.width = self.right - self.left
        print(self.width, self.height)
        cv2.namedWindow('preview')

    def prepare_screenshot(self):
        self.wDC = win32gui.GetWindowDC(self.win_32_window)
        self.dcObj = win32ui.CreateDCFromHandle(self.wDC)
        self.cDC = self.dcObj.CreateCompatibleDC()

        self.saveBitMap = win32ui.CreateBitmap()
        self.saveBitMap.CreateCompatibleBitmap(self.dcObj, self.width, self.height)
        self.cDC.SelectObject(self.saveBitMap)

    def show_image(self, screen_name, image):
        cv2.imshow(screen_name, image)
        if cv2.waitKey(1) == ord('q'):
            cv2.destroyAllWindows()

    def video(self):
        self.prepare_screenshot()

        t = time()
        f = 0
        while True:
            if cv2.waitKey(1) == ord('q'):
                cv2.destroyAllWindows()
                break
            if time() - t > 1:
                print(f)
                f = 0
                t = time()

            f += 1
            cv2.imshow('preview', self.capture_screenshot())
        self.release()

    def capture_screenshot(self):
        result = windll.user32.PrintWindow(self.win_32_window, self.cDC.GetSafeHdc(), 0)
        signedIntsArray = self.saveBitMap.GetBitmapBits(True)
        img = np.fromstring(signedIntsArray, dtype='uint8')
        img.shape = (self.height, self.width, 4)
        # release happens here...
        img = img[..., :3]
        img = np.ascontiguousarray(img)
        return img

    def release(self):
        self.cDC.DeleteDC()
        self.dcObj.DeleteDC()
        win32gui.ReleaseDC(self.win_32_window, self.wDC)
        win32gui.DeleteObject(self.saveBitMap.GetHandle())

    def screenshot(self):
        img = get_screenshot(self.win_32_window)
        self.show_image('preview', img)

    def kill_all_windows(self):
        cv2.destroyAllWindows()
    # def get_screenshot(self):
    #     wDC = win32gui.GetWindowDC(self.win_32_window)
    #     dcObj = win32ui.CreateDCFromHandle(wDC)
    #     cDC = dcObj.CreateCompatibleDC()
    #
    #     saveBitMap = win32ui.CreateBitmap()
    #     saveBitMap.CreateCompatibleBitmap(dcObj, self.width, self.height)
    #
    #     cDC.SelectObject(saveBitMap)
    #     result = windll.user32.PrintWindow(self.win_32_window, cDC.GetSafeHdc(), 0)
    #
    #     signedIntsArray = saveBitMap.GetBitmapBits(True)
    #     img = np.fromstring(signedIntsArray, dtype='uint8')
    #     img.shape = (self.height, self.width, 4)
    #
    #     dcObj.DeleteDC()
    #     cDC.DeleteDC()
    #     win32gui.ReleaseDC(self.win_32_window, wDC)
    #     win32gui.DeleteObject(saveBitMap.GetHandle())
    #     img = img[..., :3]
    #     img = np.ascontiguousarray(img)
    #     cv2.imshow("preview", img)  # debug the loop rate
    #
    #     return img


class ProgramController:
    def __init__(self, program_name, window_title, window_id):
        try:
            self.program = self.get_program(program_name)
            print('initiating win rapper')
            self.window = Win32Wrapper(window_title)
            self.options = {
                '0': ('quit', lambda: None),
                '1': ('start preview', self.window.video),

            }
            self.run()
        except Exception as e:
            print(e)

    def run(self):
        while True:
            val = self.control()
            if val == self.options['0']:
                break

    def control(self):
        for key, val in self.options.items():
            print(key, val)
        command = input('Please choose option: ')
        if command in self.options:
            self.options[command][1]()
        else:
            print("you chose an invalid option.")

    def get_program(self, program_name):
        program = get_process_by_name(program_name)
        if not type(program) == psutil.Process:
            raise Exception("Program not found")
        else:
            print("program FOUND")
            return program
ProgramController(PROGRAM_NAME,WINDOW_TITLE,0)