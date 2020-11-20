import uuid

try:
    import keyboard
except:
    print("keyboard module not loaded")
from keyboard import KeyboardEvent

from ImageProcessing.ImgTools import crop_center, save_img, crop_img_percent
from ApplicationManagers.ProgramController import ProgramController


class MLPictureGen():
    def __init__(self, program_name):
        """

        :param program_name:
        :return:
        """
        self.app = ProgramController(program_name)
        self.app.program.start_capture('ml_picture_gen: ' + program_name)
        self.width = 100
        self.height = 100
        self.name = 'default'

    def check_event_is_click(self, args):
        if not args['event'] == 1:
            return False
        return True

    def save_img(self, **kwargs):
        if self.check_event_is_click(kwargs):
            x, y = self.app.program.get_mouse_pos()
            img = self.app.program.get_latest_screenshot()
            img = crop_center(img, x, y, self.width, self.height)
            save_img(img, self.name, True)

    def set_img_attr(self, name, width, height):
        self.name = name
        self.width = width
        self.height = height

    def capture_on_event(self, key, window_name, name='default', width=100, height=100):
        self.set_img_attr(name, width, height)
        self.app.program.start_capture(window_name)

        def capture(e: KeyboardEvent):
            if e.name == key:
                self.save_img()

        keyboard.on_press(capture)

    def capture_on_click(self, window_name, name='default', width=100, height=100):
        self.set_img_attr(name, width, height)
        self.app.program.start_capture(window_name)
        self.app.program.add_click_callback(self.save_img)

    def capture_on_two_click(self, name, path, as_percentage=True, with_uuid=True, format='.png'):
        """
        Click first time for top left corner,
        Second for bottom right corner
        image is saved
        area_printed as percentage/as pixel.
        :return:
        """
        self.ctc_first = None

        def process_click(**kwargs):
            if self.check_event_is_click(kwargs):
                if self.ctc_first is None:
                    self.ctc_first = self.app.program.get_mouse_pos()
                else:
                    ctc_first = self.ctc_first
                    self.ctc_first = None
                    ctc_second = self.app.program.get_mouse_pos()
                    print("two clicks registered: ", ctc_first, ctc_second)

                    win_dim = self.app.program.get_window_dim()
                    print(ctc_first.shape, ctc_second.shape, win_dim.shape)

                    if as_percentage:
                        ctc_first = ctc_first / win_dim
                        ctc_second = ctc_second / win_dim
                    print("x,y:", ctc_first)
                    wh = ctc_second - ctc_first
                    print("w,h:", wh)
                    img = self.app.program.get_latest_screenshot()
                    uid = uuid.uuid4()
                    save_img(crop_img_percent(img, *ctc_first, *wh), name, with_uuid=with_uuid, format=format,
                             path=path)

                    print('=========== IMAGE SAVED========' )

        self.app.program.add_click_callback(process_click)

    def print_percentages(self, key):
        def print_val(e):
            if e.name == key:
                x, y = self.app.program.get_mouse_pos()
                p_x = x / self.app.program.width
                p_y = y / self.app.program.height
                print(p_x, p_y)

        keyboard.on_press(print_val)
        pass
