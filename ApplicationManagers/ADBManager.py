import signal
import threading
import time

import cv2
import numpy as np

from ApplicationManagers.viewer import AndroidViewer
from CardPrototyping.GenericCard import GenericCard


class ADBManager(GenericCard):
    def __init__(self):
        GenericCard.__init__(self, self.__class__)
        self.latest_frame = None
        print('window thread complete')
        self.video_thread = None
        self.android = AndroidViewer()
        self.stop = True
        signal.signal(signal.SIGINT, self._shutdown)
        signal.signal(signal.SIGTERM, self._shutdown)
        # signal.signal(signal.SIGKILL, self._shutdown)
        signal.signal(signal.SIGQUIT, self._shutdown)
        signal.signal(signal.SIGHUP, self._shutdown)

    def on_mouse_event(self, x=0, y=0, flags=0, **kwargs):
        pass

    def on_frame_update(self, img: np.ndarray):
        pass

    def swipe(self, xy_from, xy_to):
        """
        Swipe or click event
        (from==to -> click)
        :param xy_from:
        :param xy_to:
        :return:
        """
        self.android.swipe(*xy_from, *xy_to)

    def _shutdown(self,*args):
        print('signal received')
        self.stop = True
        self.android.close_all_sockets()
        print("SHUTDOWN CALLED")
        time.sleep(2)
        print("SLEEP COMPLETE")

    def _stop_all_threads(self):
        print("STOPPING ALL THREADS")
        self.stop = True

    def _swipe(self, start_x, start_y, end_x, end_y):
        self.android.swipe(start_x, start_y, end_x, end_y)

    def _special_opencv_thread(self, window):
        print("STARTED SPECIAL THREAD ON: ", window)
        cv2.namedWindow(window)
        print("window instantiated")
        cv2.setMouseCallback(window, self.__sanitize_mouse_event)
        print("callbacks set")
        t = time.time()
        f = 0
        self.stop = False
        while not self.stop:

            dt = time.time() - t
            t = time.time()
            frames = self.android.get_next_frames()
            if frames is None:
                continue

            for frame in frames:
                f += 1
                self.latest_frame = frame
                self._update_dim(self.latest_frame)
                self.on_frame_update(self.latest_frame)
                cv2.imshow(window, frame)
                cv2.waitKey(1)
            if dt > 1:
                f = 0
        cv2.destroyWindow(window)
        cv2.waitKey(1)
        print("Thread ended")

    def _update_dim(self, img):
        self.height = len(img)
        self.width = len(img[1])

    def _get_window_dim(self):
        return np.array([self.width, self.height])

    def __sanitize_mouse_event(self, event, x, y, flags, param):
        # print(event, x, y, flags, param)
        self.mouse_x = x
        self.mouse_y = y
        kwargs = {'x': x, 'y': y, 'flags': flags, 'param': param, 'event': event}
        self.on_mouse_event(**kwargs)

    def _get_mouse_pos(self):
        return np.array([self.mouse_x, self.mouse_y])

    def _start_capture(self, screen_name):
        self.stop = False
        self.video_thread = threading.Thread(target=self._special_opencv_thread,
                                             args=[screen_name])
        self.video_thread.daemon = True
        self.video_thread.start()


#
adb_manager = ADBManager()
adb_manager._start_capture('ADBManager')
