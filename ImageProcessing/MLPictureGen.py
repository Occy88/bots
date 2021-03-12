import uuid

try:
    import keyboard
except:
    print("keyboard module not loaded")
from keyboard import KeyboardEvent
from CardPrototyping.card_ADB.instances_ADB import android_phone

from ImageProcessing.ImgTools import crop_center, save_img, crop_img, show_img, img_col_similarity, load_img
import json
import os


class MLPictureGen():
    def __init__(self, program_name):
        """

        :param program_name:
        :return:
        """
        print("initiating program controller")
        # android_phone = ProgramController(program_name)
        print(android_phone, " Initiation complete")
        self.width = 100
        self.height = 100
        self.name = 'default'

    def check_event_is_click(self, args):
        if not args['event'] == 1:
            return False
        return True

    def save_img(self, **kwargs):
        if self.check_event_is_click(kwargs):
            x, y = android_phone._get_mouse_pos()
            img = android_phone.get_latest_screenshot()
            img = crop_center(img, x, y, self.width, self.height)
            save_img(img, self.name, True)

    def set_img_attr(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height

    def capture_on_event(self, key, window_name, name='default', width=100, height=100):
        self.set_img_attr(name, width, height)
        android_phone.start_capture(window_name)

        def capture(e: KeyboardEvent):
            if e.name == key:
                self.save_img()

        keyboard.on_press(capture)

    def capture_on_click(self, window_name, name='default', width=100, height=100):
        self.set_img_attr(name, width, height)
        android_phone.start_capture(window_name)
        android_phone.add_click_callback(self.save_img)

    def test_image(self, path, img_name):
        """
        Image name should be in the format: name+ | + coord 1 + coord 2 +|+bool as percent
        """
        # print(path)
        # print(os.listdir(path))
        # print("-------------")
        img_name_with_coords = ''
        for a in os.listdir(path):
            if a.split("|")[0] == img_name:
                img_name_with_coords = a
                break
        if img_name_with_coords == '':
            raise Exception("Image Not Found: ", path, img_name)
        img = android_phone.latest_frame
        # show_img(img)
        details = json.loads(img_name_with_coords.split('|')[1].replace('.png', ''))
        img = crop_img(img, *details['xy'], *details['wh'], details['as_percentage'])
        # show_img(img)
        fp = path + img_name_with_coords
        # print(fp)
        img2 = load_img(fp)
        # show_img(img2)
        sim = img_col_similarity(img, img2)
        # print(sim)
        return sim

    def capture_on_two_click(self, name, path, as_percentage=True, with_coords=True, with_uuid=False, format='.png'):
        """
        Click first time for top left corner,
        Second for bottom right corner
        image is saved
        area_printed as percentage/as pixel.
        :return:
        """
        self.ctc_first = None
        print(android_phone)

        def process_click(**kwargs):
            if self.check_event_is_click(kwargs):
                if self.ctc_first is None:
                    self.ctc_first = android_phone._get_mouse_pos()
                else:
                    ctc_first = self.ctc_first
                    self.ctc_first = None
                    ctc_second = android_phone._get_mouse_pos()
                    print("two clicks registered: ", ctc_first, ctc_second)

                    win_dim = android_phone._get_window_dim()
                    print(ctc_first.shape, ctc_second.shape, win_dim.shape)

                    if as_percentage:
                        ctc_first = ctc_first / win_dim
                        ctc_second = ctc_second / win_dim
                    print("x,y:", ctc_first)
                    wh = ctc_second - ctc_first
                    print("w,h:", wh)
                    img = android_phone.latest_frame
                    nm = name
                    details = dict()
                    import numpy as np

                    details['xy'] = ctc_first.tolist()
                    details['wh'] = wh.tolist()
                    details['as_percentage'] = as_percentage
                    nm += '|' + json.dumps(details)
                    save_img(crop_img(img, *ctc_first, *wh, as_percentage), nm, with_uuid=with_uuid, format=format,
                             path=path)

                    print('=========== IMAGE SAVED========')

        android_phone.do_mouse_event_complete(process_click)

    def print_percentages(self, key):
        def print_val(e):
            if e.name == key:
                x, y = android_phone._get_mouse_pos()
                p_x = x / android_phone.width
                p_y = y / android_phone.height
                print(p_x, p_y)

        keyboard.on_press(print_val)
        pass
