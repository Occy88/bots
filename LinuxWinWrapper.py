import numpy as np
import win32gui
import win32ui
from ctypes import windll
from WindowInterface import WindowInterface
import cv2
from time import time

import threading


class LinuxWinWrapper(WindowInterface):
    def __init__(self, window_title):
        WindowInterface.__init__(self,window_title)
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
            cv2.imshow('preview', self.get_latest_screenshot())
        self.release()

    def get_latest_screenshot(self):
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


    def kill_all_windows(self):
        cv2.destroyAllWindows()
