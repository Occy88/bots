"""
Simple card takes image from android,
displays it,
finds pokestops,
clicks on pokestop locations
"""

from CardPrototyping.GenericCard import GenericCardTemplate
from ImageProcessing.ImgTools import show_img, crop_img_percent
from PokemonGo.DetectPokestop import pokestop_detector

print("DECLARING CARD TEST CLASS")


class CardTest(GenericCardTemplate()):
    """
    An example class connecting with another one

    my fun bot recieves accepts an image and calls the swipe callback
    with the coordinates identified.
    """

    def __init__(self):
        super().__init__()

    def do_bot_recieve_img(self, img):
        """
        receives image, returns coordinates to swipe from and to
        :param img:
        :return:
        """
        print("DETECTING LOCATIONS")
        img = crop_img_percent(img, 0, .4, 1, .4)
        # show_img(img)
        img1, (img2, num_loc) = pokestop_detector.find_locations(img)
        # show_img(img1)
        # show_img(img2)
        # print(num_loc)
        print("SWIPING")
        return (50, 100), (50, 20)


print('DECLARED NOW INSTANTIATING')
card_test_card = CardTest()
