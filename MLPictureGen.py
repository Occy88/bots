from ProgramCotntroller import ProgramController
from ImgTools import crop_center, save_img
import uuid
import keyboard
from keyboard import KeyboardEvent


class MLPictureGen():
    def __init__(self, program_name, window_title):
        self.app = ProgramController(program_name, window_title, 0)

    def capture_on_event(self, key, name, width, height):
        self.app.window.prepare_screenshot()

        def capture(e: KeyboardEvent):
            if e.name == key:
                x, y = self.app.window.get_mouse_pos()
                img = self.app.window.get_latest_screenshot()
                img = crop_center(img, x, y, width, height)
                save_img(img, name + '_' + str(uuid.uuid4()) + '.jpg')

        keyboard.on_press(capture)

    def print_percentages(self, key):
        def print_val(e):
            if e.name == key:
                x, y = self.app.window.get_mouse_pos()
                p_x = x / self.app.window.width
                p_y = y / self.app.window.height
                print(p_x, p_y)

        keyboard.on_press(print_val)
        pass
