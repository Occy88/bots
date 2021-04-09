import logging
import signal
import sys
import threading
import time
import os
import cv2
import numpy as np
import atexit
from CardPrototyping.card_ADB.viewer import AndroidViewer
from CardPrototyping.GenericCard import GenericCardTemplate
from ImageProcessing.ImgTools import resize_img, crop_img
from settings import SCREEN_SCALE_FACTOR

logger = logging.getLogger(__name__)
logging.basicConfig(stream=sys.stdout, level=logging.INFO,
                    format='%(asctime)s.%(msecs)03d %(levelname)s:\t%(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')


class ADBManager(GenericCardTemplate()):
    def __init__(self):
        super().__init__()
        self.adjusted_resolution = None
        self.latest_frame = None
        logging.info('Bind methods generated')
        self.video_thread = None
        self.android = AndroidViewer()
        self.stop = True
        self.scale_factor = SCREEN_SCALE_FACTOR
        atexit.register(self._shutdown)
        try:
            signal.signal(signal.SIGINT, self._shutdown)
            signal.signal(signal.SIGTERM, self._shutdown)
            # signal.signal(signal.SIGKILL, self._shutdown)
            signal.signal(signal.SIGQUIT, self._shutdown)
            signal.signal(signal.SIGHUP, self._shutdown)
        except Exception as e:
            pass
        time.sleep(2)

    def set_resolution(self, res=np.array([1080, 1920])):
        # adb shell wm size reset
        # adb shell wm density resetpytho
        # adb shell wm size 1080x1920
        self.adjusted_resolution = res
        self.exec_adb_command(f'wm size ' + 'x'.join(res.astype(str)))
        time.sleep(2)

    def reset_resolution(self):
        self.exec_adb_command('wm size reset')

    def set_full_screen(self, app_ref='com.nianticlabs.pokemongo'):
        self.exec_adb_command(f'settings put global policy_control immersive.full={app_ref}')

    def exec_adb_command(self, cmd):
        os.popen(f'adb shell {cmd}')

    def do_mouse_event(self, x=0, y=0, flags=0, **kwargs):

        pass

    def do_frame_update(self, img: np.ndarray):
        pass

    def hold(self, xy: np.ndarray, as_percent=True):
        if as_percent:
            xy = self.to_percent(xy)
        self.android.hold(*xy)
        pass

    def release(self, xy, as_percent=True):
        if as_percent:
            xy = self.to_percent(xy)
        self.android.release(*xy)

    def to_percent(self, xy):
        return np.array([self.width, self.height]) * xy

    def swipe(self, xy_from: np.ndarray, xy_to: np.ndarray, as_percent=True, step_pixels=5, step_delay=0.05):
        """
        Swipe or click event
        (from==to -> click)
        :param xy_from:
        :param xy_to:
        :return:
        """

        if as_percent:
            xy_from = self.to_percent(xy_from)
            xy_to = self.to_percent(xy_to)
        logging.info("Adb Swipe message Recieved: " + str(xy_from) + str(xy_to))
        self.android.swipe(*xy_from, *xy_to, step_pixels=step_pixels, step_delay=step_delay)

    def _shutdown(self, *args):
        logging.info('Shutdown Signal Recieved: ', args)
        logging.info('Cleaning up')
        self.reset_resolution()

        self.stop = True
        self.android.close_all_sockets()
        logging.info("SHUTDOWN CALLED")
        logging.info("SLEEP COMPLETE")
        exit(0)
        return

    def _stop_all_threads(self):
        logging.info("STOPPING ALL THREADS")
        self.stop = True

    def _swipe(self, start_x, start_y, end_x, end_y):
        self.android.swipe(start_x, start_y, end_x, end_y)

    def _special_opencv_thread(self, window):
        logging.info("Video starting on:" + str(window))
        cv2.namedWindow(window)
        cv2.setMouseCallback(window, self.__sanitize_mouse_event)
        logging.info("Callbacks set")
        t = time.time()
        f = 0
        while not self.stop:

            dt = time.time() - t
            t = time.time()
            frames = self.android.get_next_frames()
            if frames is None:
                continue

            for frame in frames:
                f += 1
                if self.adjusted_resolution is not None:
                    frame = crop_img(frame, 0, 0, *self.adjusted_resolution)
                self.latest_frame = frame

                self._update_dim(self.latest_frame)
                self.do_frame_update(self.latest_frame)
                cv2.imshow(window, resize_img(frame, self.scale_factor, True))
                cv2.waitKey(1)
            if dt > 1:
                f = 0
        cv2.destroyWindow(window)
        cv2.waitKey(1)
        logging.info("Thread ended")

    def _update_dim(self, img):
        self.height = len(img)
        self.width = len(img[1])

    def _get_window_dim(self):
        return np.array([self.width, self.height])

    def __sanitize_mouse_event(self, event, x, y, flags, param):
        # logging.info(event, x, y, flags, param)
        self.mouse_x = x / self.scale_factor
        self.mouse_y = y / self.scale_factor
        kwargs = {'x': self.mouse_x, 'y': self.mouse_y, 'flags': flags, 'param': param, 'event': event}
        self.do_mouse_event(**kwargs)

    def _get_mouse_pos(self):
        return np.array([self.mouse_x, self.mouse_y])

    def start_capture(self, screen_name):
        self.stop = False
        self.video_thread = threading.Thread(target=self._special_opencv_thread,
                                             args=[screen_name])
        self.video_thread.daemon = True
        self.video_thread.start()

#
