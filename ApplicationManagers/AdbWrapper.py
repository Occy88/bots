import threading
import time

import cv2

from ApplicationManagers.WindowInterface import WindowInterface
from ApplicationManagers.viewer import AndroidViewer


class АdbWrapper(WindowInterface):
    def __init__(self, *args):
        WindowInterface.__init__(self)
        self.update_properties()
        self.frame_rate = 30
        self.latest_frame = None
        print('properties updated, starting thread')
        print('window thread complete')
        self.video_thread = None
        self.android = AndroidViewer()
        self.stop = True
        self.click_callbacks = []

    def exec_every(self, function, rate, *args):
        self.stop = False
        while not self.stop:
            threading.Thread(target=function, args=args).start()
            time.sleep(rate)

    def stop_all_threads(self):
        self.stop = True

    def swipe(self, start_x, start_y, end_x, end_y):
        self.android.swipe(start_x, start_y, end_x, end_y)

    def add_click_callback(self, callback):
        self.click_callbacks.append(callback)

    def special_opencv_thread(self, window):
        print("STARTED SPECIAL THREAD ON: ", window)
        cv2.namedWindow(window)
        print("window instantiated")
        cv2.setMouseCallback(window, self.handle_mouse_event)
        print("callbacks set")
        t = time.time()
        f = 0
        self.stop = False
        while not self.stop:

            if time.time() - t > 1:
                print(f)
                t = time.time()
                f = 0
            frames = self.android.get_next_frames()
            if frames is None:
                continue

            for frame in frames:
                f += 1
                self.latest_frame = frame
                cv2.imshow(window, frame)
                cv2.waitKey(1)
        cv2.destroyWindow(window)
        cv2.waitKey(1)

        print("Thread ended")

    def get_latest_screenshot(self):
        return self.latest_frame

    def handle_mouse_event(self, event, x, y, flags, param):
        print(event, x, y, flags, param)
        self.mouse_x = x
        self.mouse_y = y
        kwargs = {'x': x, 'y': y, 'flags': flags, 'param': param, 'event': event}
        for c in self.click_callbacks:
            c(**kwargs)

    def get_mouse_pos(self):
        return self.mouse_x, self.mouse_y

    def start_capture(self, screen_name):
        self.stop = False
        self.video_thread = threading.Thread(target=self.special_opencv_thread,
                                             args=[screen_name])
        self.video_thread.start()

    def update_properties(self):
        self.left, self.top, self.right, self.bottom = 1, 2, 3, 4
        self.height = self.bottom - self.top
        self.width = self.right - self.left
        print(self.width, self.height)

#
