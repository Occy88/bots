import os

print(os.getcwd())

from CardPrototyping.GenericCard import GenericCardTemplate
from CardPrototyping.card_ADB.instances_ADB import android_phone
from ImageProcessing.ImgTools import img_col_similarity
from ImageProcessing import MLPictureGen
import numpy as np

# path = '../PokemonGo/images/FriendGifting/'
path = 'PokemonGo/images/FriendGifting/'
gen = MLPictureGen.MLPictureGen()


def open_gift_page():
    open_page = gen.test_image(path, 'open_gift_page')
    print(open_page)
    return open_page > 0.8


def leave_page():
    print("LEAVINNG PAGE")
    btn = np.array([0.50462963, 0.87575])
    android_phone.swipe(btn, btn, True)
    time.sleep(1)


def gift_received():
    v = gen.test_image(path, 'gift_received_profile')
    print("checking recieved: ", v)

    return v > 0.8


def can_send():
    return gen.test_image(path, 'can_send_gift_profile') > 0.7


def change_profile():
    android_phone.swipe(np.array([0.93518519, 0.8]), np.array([0.1537037, 0.8]), True)
    time.sleep(2)
    pass


def open_gift():
    rand = np.array([0.16759259, 0.6225])
    print("Random Click")
    android_phone.swipe(rand, rand, True)
    time.sleep(3)
    print("Open Click")

    open = np.array([0.5, 0.75])

    android_phone.swipe(open, open, True)
    time.sleep(2)
    print("Open Click")
    time.sleep(1)
    if open_gift_page():
        print("GIFT LIMIT REACHED .....")
        leave_page()
        return False
    android_phone.swipe(open, open, True)
    time.sleep(0.3)
    android_phone.swipe(open, open, True)
    time.sleep(0.2)
    android_phone.swipe(open, open, True)
    time.sleep(0.2)
    android_phone.swipe(open, open, True)
    time.sleep(0.2)
    android_phone.swipe(open, open, True)
    time.sleep(3.5)
    return True


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


class SendGifts(GenericCardTemplate()):
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

    def do_send_gifts(self):
        print("initiating transfer routine in 10s")
        time.sleep(10)
        limit_reached = False

        while True:
            if gift_received():
                if limit_reached:
                    leave_page()
                else:
                    print("Gift Received")
                    print("Opening Gift")
                    limit_reached = not open_gift()

            if can_send():
                # break
                print("Sending gift")
                send_gift()
                print("Changing profile")
            change_profile()

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
