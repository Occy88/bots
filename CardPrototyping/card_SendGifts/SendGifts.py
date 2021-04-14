import os

print(os.getcwd())

from CardPrototyping.GenericCard import GenericCardTemplate
from CardPrototyping.card_ADB.instances_ADB import android_phone
from ImageProcessing.ImgTools import img_col_similarity, update_img_from_details
from ImageProcessing import MLPictureGen
import numpy as np

# path = '../PokemonGo/images/FriendGifting/'
path = 'PokemonGo/images/FriendGifting/'
gen = MLPictureGen.MLPictureGen()

dbg_btn=np.array([0,0.1])
def open_gift_page():
    print("============[ Checking gift can be opened ]===========")
    v = gen.test_image(path, 'open_gift_page')
    print("value: ", v)
    return v > 0.8


def leave_page():
    print("LEAVINNG PAGE")
    btn = np.array([0.5, 0.96])
    android_phone.swipe(btn, btn, True)
    time.sleep(1)


def gift_received():
    print("============[ Checking if gift was received ]===========")
    v = gen.test_image(path, 'gift_received_profile')
    print("value: ", v)
    return v > 0.8


def can_send():
    print("============[ Checking if gift can be sent ]===========")
    v = gen.test_image(path, 'can_send_gift_profile')
    print("value: ", v)

    return v > 0.7


def change_profile():
    print("============[ NEXT PROFILE ]===========")
    android_phone.swipe(np.array([0.93518519, 0.86]), np.array([0.1537037, 0.86]), True, step_pixels=10, step_delay=0.02)
    time.sleep(2)
    pass


def click_wabble_gift():
    rand = np.array([0.5, 0.5])
    print("Random Click")
    android_phone.swipe(rand, rand, True)
    time.sleep(3)


def open_gift():
    click_wabble_gift()
    print("Open Click")

    open = np.array([0.5, 0.86])


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
    time.sleep(5)
    return True


def send_gift():
    print("Send Click")
    send_button = np.array([0.20185185, 0.85])
    android_phone.swipe(send_button, send_button, True)
    time.sleep(3)
    print("Gift Click")

    gift_button = np.array([0.5, 0.35])
    android_phone.swipe(gift_button, gift_button, True)
    time.sleep(2)
    print("Send Confirm")
    send_confirm = np.array([0.5, 0.83])
    android_phone.swipe(send_confirm, send_confirm, True)

    android_phone.swipe(send_confirm, send_confirm, True)
    time.sleep(5)


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
        android_phone.set_resolution()
        android_phone.set_full_screen('com.nianticlabs.pokemongo')
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

    def calibrate(self):
        images_path = './PokemonGo/images/FriendGifting/'
        images = ['open_gift_page', 'gift_received_profile', 'can_send_gift_profile']
        print("CALIBRATING:")
        print("EXPECTED TO BE ON PAGE WHERE GIFT IS RECIEVED FROM FRIEND AND IT WOBBLES")
        update_img_from_details(android_phone.latest_frame, images[1], images_path)
        print("CAPTURED...")
        print("CLICKING TO ACCEPT GIFT...")
        click_wabble_gift()
        time.sleep(2)
        print("EXPECTED TO BE ON PAGE WHERE YOU CAN OPEN THE GIFT...")
        update_img_from_details(android_phone.latest_frame, images[0], images_path)
        print("IMAGE CAPTURED... LEAVING PAGE TO PROFILE PAGE")
        leave_page()
        time.sleep(1)
        print("EXPECTING TO BE ON PROFILE PAGE...")
        print("EXPECTING GIFT IS NOT SENT (COLOURFUL)")
        update_img_from_details(android_phone.latest_frame, images[2], images_path)
        print("CALIBRATION COMPLETE...")

    def do_send_gifts(self):
        print("initiating transfer routine in 10s")
        time.sleep(1)
        limit_reached = False

        while True:
            if gift_received():
                if limit_reached:
                    leave_page()
                else:
                    limit_reached = not open_gift()
            if can_send():
                # break
                send_gift()
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
