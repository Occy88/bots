from CardPrototyping.GenericCard import GenericCardTemplate
from CardPrototyping.card_ADB.instances_ADB import android_phone
from ImageProcessing.ImgTools import img_col_similarity
from ImageProcessing import MLPictureGen
import numpy as np
# path = '../PokemonGo/images/FriendGifting/'
import os

path = '../../PokemonGo/images/FriendGifting/'
gen = MLPictureGen.MLPictureGen('adb')


def gift_received():
    return gen.test_image(path, 'gift_received_profile') > 0.98


def can_send():
    return gen.test_image(path, 'can_send_gift_profile') > 0.98


def change_profile():
    android_phone.swipe(np.array([0.93518519, 0.64333333]), np.array([0.1537037, 0.64458333]), True)
    time.sleep(5)
    pass


def open_gift():
    rand = np.array([0.16759259, 0.6225])
    print("Random Click")
    android_phone.swipe(rand, rand, True)
    time.sleep(5)
    print("Open Click")

    open = np.array([0.39259259, 0.77833333])

    android_phone.swipe(open, open, True)
    time.sleep(5)
    print("Open Click")

    android_phone.swipe(open, open, True)
    time.sleep(15)


def send_gift():
    print("Send Click")
    send_button = np.array([0.20185185, 0.71041667])
    android_phone.swipe(send_button, send_button, True)
    time.sleep(3)
    print("Gift Click")

    gift_button = np.array([0.20185185, 0.71041667])
    android_phone.swipe(gift_button, gift_button, True)
    time.sleep(2)
    print("Send Confirm")
    send_confirm = np.array([0.47037037, 0.79625])
    android_phone.swipe(send_confirm, send_confirm, True)
    time.sleep(7)
    pass


step1 = (130, 450)
step2 = (625, 1300)
step3 = (620, 1160)
step4 = (370, 800)
step5 = (370, 730)
extra_l_d = 2.2
long_d = 1.8
med_d = 1.3
short_d = 0.7
import time


class SendGifts(GenericCardTemplate()):
    def __init__(self, name):
        super().__init__(self)
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
        while True:
            if gift_received():
                print("Gift Received")
                print("Opening Gift")
                open_gift()
            if not can_send():
                print("Can't send")
                break
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


t = SendGifts("some name")

# android_phone.do_mouse_event_complete(t.print_click)
t.do_send_gifts()
# t.do_transfer(5)
time.sleep(100)
