import uuid

try:
    import keyboard
except:
    print("keyboard module not loaded")
from keyboard import KeyboardEvent

from ImgTools import crop_center, save_img
from ProgramController import ProgramController


class MLPictureGen():
    def __iclean_imgnit__(self, program_name):
        self.app = ProgramController(program_name)
        self.width = 100
        self.height = 100
        self.name = 'default'

    def save_img(self, **kwargs):
        if not kwargs['event'] == 1:
            print("RECIEVED EVENT: ", kwargs['event'])
            return
        x, y = self.app.program.get_mouse_pos()
        img = self.app.program.get_latest_screenshot()
        img = crop_center(img, x, y, self.width, self.height)
        save_img(img, self.name + '_' + str(uuid.uuid4()) + '.jpg')

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

    def print_percentages(self, key):
        def print_val(e):
            if e.name == key:
                x, y = self.app.program.get_mouse_pos()
                p_x = x / self.app.program.width
                p_y = y / self.app.program.height
                print(p_x, p_y)

        keyboard.on_press(print_val)
        pass
