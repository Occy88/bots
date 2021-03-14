from CardPrototyping.GenericCard import GenericCardTemplate
from CardPrototyping.card_ADB.instances_ADB import android_phone

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

...


class TransferPokemon(GenericCardTemplate()):
    def __init__(self, name):
        super().__init__(self)
        self.name = name

    def print_click(self, *args, **kwargs):
        print(args, kwargs)

    def do_transfer(self, num_pokemon):
        print("initiating transfer routine in 10s")
        time.sleep(10)
        print("initiating for: ")
        for i in range(num_pokemon):
            print(i / num_pokemon, '% left: ', num_pokemon - i)

            android_phone.swipe(step1, step1)
            time.sleep(long_d)
            android_phone.swipe(step2, step2)
            time.sleep(short_d)
            android_phone.swipe(step3, step3)
            time.sleep(short_d)
            android_phone.swipe(step4, step4)
            time.sleep(med_d)
            android_phone.swipe(step5, step5)
            time.sleep(long_d)


t = TransferPokemon("some name")
android_phone.do_mouse_event_complete(t.print_click)
# t.do_transfer(5)
time.sleep(100)