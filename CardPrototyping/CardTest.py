"""
Simple card takes image from android,
displays it,
finds pokestops,
clicks on pokestop locations
"""
from ApplicationManagers.ADBManager import adb_manager
from CardPrototyping import GenericCard
from ImageProcessing.ImgTools import show_img, crop_img_percent
from PokemonGo.DetectPokestop import pokestop_detector


class CardTest(GenericCard):
    """
    An example class connecting with another one

    my fun bot recieves accepts an image and calls the swipe callback
    with the coordinates identified.
    """

    def __init__(self):
        super().__init__(self.__class__)
        pass

    def on_swipe(self, xy_from, xy_to):
        pass

    def my_fun_bot(self, img):
        print("DETECTING LOCATIONS")
        img = crop_img_percent(img, 0, .4, 1, .4)
        show_img(img)
        img1, (img2, num_loc) = pokestop_detector.find_locations(img)
        show_img(img1)
        show_img(img2)
        print(num_loc)
        print("SWIPING")
        self.on_swipe((50, 100), (50, 20))


def example(run_time):
    inst = CardTest()
    adb_manager.bind_on_frame_update(inst.my_fun_bot, 20)
    inst.bind_on_sipe(adb_manager.swipe)

    # some random sleep to decide how long you want the above to run for :D
    import time
    time.sleep(run_time)
