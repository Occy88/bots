import base64
import os
import threading
import time

import cv2
import numpy as np
from viewer import AndroidViewer

from WindowInterface import WindowInterface


class АdbWrapper(WindowInterface):
    def __init__(self):
        WindowInterface.__init__(self)
        self.update_properties()
        self.frame_rate = 30
        self.latest_frame = None
        print('properties updated, starting thread')
        print('window thread complete')
        self.capture_thread = None
        self.video_thread = None
        self.lock = threading.Lock()
        self.android = AndroidViewer()

    def exec_every(self, function, rate, *args):
        while (1):
            threading.Thread(target=function, args=args).start()
            time.sleep(rate)

    def swipe(self, start_x, start_y, end_x, end_y):
        self.android.swipe(start_x, start_y, end_x, end_y)

    def special_opencv_thread(self, window):
        t = time.time()
        f = 0
        while True:
            frames = self.android.get_next_frames()
            if frames is None:
                continue

            for frame in frames:
                cv2.imshow(window, frame)
                cv2.waitKey(1)



    def get_mouse_pos(self):
        x, y = 1, 2
        print(self.left, self.right, self.bottom, self.top)
        x -= self.left
        y -= self.top
        return x, y



    def video(self, ):
        self.video_thread = threading.Thread(target=self.special_opencv_thread,
                                             args=['video'])
        self.video_thread.start()





    def update_properties(self):
        self.left, self.top, self.right, self.bottom = 1, 2, 3, 4
        self.height = self.bottom - self.top
        self.width = self.right - self.left
        print(self.width, self.height)

#
