import keyboard
import threading
import time


class Keyboard:
    def __init__(self, screen, ):

        try:
            keyboard.hook(self.test_hook, suppress=True)
        except Exception as e:
            print("IF YOU WOULD LIKE TO USE MULTIPLE KEYS SIMULTANEOUSLY \nRUN ME WITH SUDO PERMISSIONS")
            print('THANK YOU')

            self.screen = screen
            self.keys_pressed_buff = []
            self.key_dict = {}
            self.cooldown = 0.25
            key_thread = threading.Thread(target=self.key_handler)
            key_thread.start()
            self.cooldowns = threading.Thread(target=self.decrease_cooldowns)
            self.cooldowns.start()
        self.on_press_callbacks = []
        self.on_release_callbacks = []
        self.remap_keys = {
            'KEY_UP': 'up',
            'KEY_DOWN': 'down',
            'KEY_LEFT': 'left',
            'KEY_RIGHT': 'right',
        }

    def on_press(self, callback):
        self.on_press_callbacks.append(callback)

    def on_release(self, callback):
        self.on_release_callbacks.append(callback)

    def test_hook(self, keyboard_event):
        self.events(keyboard_event.name, keyboard_event.event_type)

    def events(self, key, event):
        if key in self.remap_keys:
            key = self.remap_keys[key]
        if event == 'up':
            for c in self.on_release_callbacks:
                c(key)
        else:
            for c in self.on_press_callbacks:
                c(key)

    def key_handler(self, ):
        while True:
            key = self.screen.getkey()
            try:
                if self.key_dict[key] == 0:
                    self.events(key, 'down')
                self.key_dict[key] = self.cooldown
            except:
                self.events(key, 'down')
                self.key_dict[key] = self.cooldown

    def key_callback(self, key_pressed):
        self.keys_pressed_buff.append(key_pressed)

    def decrease_cooldowns(self):
        t = time.time()
        while True:
            time.sleep(0.05)
            elapsed = time.time() - t
            t = time.time()
            for key in self.key_dict:
                if self.key_dict[key] > 0:
                    self.key_dict[key] -= elapsed
                if self.key_dict[key] < 0:
                    self.events(key, 'up')
                    self.key_dict[key] = 0
