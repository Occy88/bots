"""
Simple card takes image from android,
displays it,
finds pokestops,
clicks on pokestop locations
"""
from ApplicationManagers.ADBManager import adb_manager
from ImageProcessing.ImgTools import show_img, crop_img_percent
from PokemonGo.DetectPokestop import get_detector

pokestop_detector = get_detector()


def my_fun_bot(img):
    print("DETECTING LOCATIONS")
    img = crop_img_percent(img, 0, .4, 1, .4)
    show_img(img)
    img1, (img2, num_loc) = pokestop_detector.find_locations(img)
    show_img(img1)
    show_img(img2)
    print(num_loc)
    print("SWIPING")
    adb_manager.swipe((50, 100), (50, 20))


adb_manager.bind_on_frame_update(my_fun_bot, 20)
import time

time.sleep(1000)
