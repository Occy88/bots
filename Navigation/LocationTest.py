from ImageProcessing.ImgTools import crop_img_percent
from ImageProcessing.ImgTools import template_match
from Navigation.configs import QUEST_BUTTON_LOCATION as qb
from Navigation.configs import HOME_BUTTON_LOCATION as hb


def test_home(img):
    """
    Current test is check if the orange spectacles are in the correct location
    and if the pokeball in the bottom center is there as well. (a double test
    for redundancy)
    :param img:
    :return:
    """
    home_b = crop_img_percent(img, **hb)
    quest_b = crop_img_percent(img, **qb)
    res= template_match(home_b, 'Navigation\\assets\\home_pokeball_button.PNG')
    res2 = template_match(quest_b, 'Navigation\\assets\\home_quest_button.PNG')
    thresh=0.7
    if res2.max()>thresh and res.max()>thresh:
        print("TRUE")
        return True
    print("False, ",res.max(),res2.max())
    return False
