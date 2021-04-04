import os

print(os.getcwd())

from CardPrototyping.GenericCard import GenericCardTemplate
from CardPrototyping.card_ADB.instances_ADB import android_phone
from ImageProcessing.ImgTools import img_col_similarity, find_circles
from ImageProcessing import MLPictureGen
import numpy as np

# path = '../PokemonGo/images/FriendGifting/'
path = 'PokemonGo/images/FriendGifting/'
gen = MLPictureGen.MLPictureGen()


def can_send():
    return gen.test_image(path, 'can_send_gift_profile') > 0.7


def catch():
    pokeball_select_location = np.array([0.43, 0.4]) * 2
    pokeball_master_location = np.array([0.415, 0.4]) * 2
    pokeball_hold = np.array([0.25, 0.42]) * 2
    # select master -> great ->pokeball
    print("SELECTING POKEBALL")
    android_phone.swipe(pokeball_select_location,pokeball_select_location)
    time.sleep(1)
    android_phone.swipe(pokeball_master_location,pokeball_master_location)
    time.sleep(1)
    print("SEARCHING")

    android_phone.hold(pokeball_hold, True)
    time.sleep(0.5)
    c1 = find_circles(android_phone.latest_frame, np.array([.05, .4]), np.array([0, 0.3, 1, .3]))
    while not len(c1) > 0:
        print("ATTEMPT, FIND")
        c1 = find_circles(android_phone.latest_frame, np.array([.05, .4]), np.array([0, 0.3, 1, .3]))
        time.sleep(1)
    print("FOUND, SWIPING")
    x, y, r = c1[0]
    android_phone.release(pokeball_hold, True)
    time.sleep(0.5)
    android_phone.swipe(pokeball_hold,
                        np.array([x, y]) / np.array(np.flip(android_phone.latest_frame.shape[:2])), as_percent=True,step_pixels=10,step_delay=0.001)
    # hold down
    # detect circle

    # throw ball into circle.
    pass


def send_gift():
    print("Send Click")
    send_button = np.array([0.185, 0.88])
    android_phone.swipe(send_button, send_button, True)
    time.sleep(3)
    print("Gift Click")

    gift_button = np.array([0.5, 0.35])
    android_phone.swipe(gift_button, gift_button, True)
    time.sleep(2)
    print("Send Confirm")
    send_confirm = np.array([0.5, 0.79625])

    android_phone.swipe(send_confirm, send_confirm, True)
    time.sleep(7)


import time


class CatchPokemon(GenericCardTemplate()):
    def __init__(self, name):
        super().__init__(self)
        android_phone.set_resolution()
        self.name = name

    def print_click(self, *args, **kwargs):
        if kwargs['event'] != 4:
            return
        p = np.array([kwargs['x'], kwargs['y']])
        t = np.array([android_phone.width, android_phone.height])
        p_percent = p / t
        print(p_percent)

    def next_profile(self):
        android_phone.swipe()

    def catch_pokemon(self):
        android_phone.do_mouse_event_complete(self.print_click)
        time.sleep(2)
        while True:
            catch()
            print("SLEEPING")
            time.sleep(10)

        # print("initiating for: ")
        # for i in range(num_pokemon):
        #     print(i / num_pokemon, '% left: ', num_pokemon - i)
        #
        #     android_phone.swipe(step1, step1)
        #     time.sleep(long_d)
        #     android_phone.swipe(step2, step2)
        #     time.sleep(short_d)
        #     android_phone.swipe(step3, step3)
        #     time.sleep(short_d)
        #     android_phone.swipe(step4, step4)
        #     time.sleep(med_d)
        #     android_phone.swipe(step5, step5)
        #     time.sleep(long_d)
