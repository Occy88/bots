import cv2
import numpy as np

from ImageProcessing.ImgTools import TfImageFinder
from ImageProcessing.conv import load_model
from ImageProcessing.conv import preprocess_images

POKESTOP_MODEL_PATH = '../models/PokestopDetect'
POKESTOP_IMAGES = 'images/Pokestop/*'
NOT_POKESTOP_IMAGES = 'images/Nothing/*'
POKESTOP_IMG_DIM = (100, 150, 3)
POKESTOP_RESIZE_DIM = (32, 32, 3)


def clean_img(img_list):
    """
    remove all unnecessary colours (conecntrate on blue pokestops only)

    :param img:
    :return:q
    """
    print("CLEANING N IMAGES: ", len(img_list))
    for i, img in enumerate(img_list):
        # print('CLEANING IMAGE: ', i)
        # print(img.shape)
        # print(type(img))
        # print(img[0][0])
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # Threshold of blue in HSV space
        lower_blue = np.array([35, 190, 130])
        upper_blue = np.array([170, 236, 255])

        # preparing the mask to overlay
        mask = cv2.inRange(hsv, lower_blue, upper_blue)

        # The black region in the mask has the value of 0,
        # so when multiplied with original image removes all non-blue regions
        img_list[i] = cv2.bitwise_and(img, img, mask=mask)
    return img_list


def preprocessor(X):
    return preprocess_images(X, (32, 32, 3), clean_img)


def get_detector():
    return TfImageFinder(
        load_model(POKESTOP_MODEL_PATH), preprocessor, POKESTOP_IMG_DIM)


POKESTOP_COLOR_CHANGE_PERCENT_AREA = ()
POKESTOP_TOO_FAR_PERCENT_AREA = ()
POKESTOP_TOO_FAR_IMAGE = ''
POKESTOP_AVAILABLE_IMAGE = ''
POKESTOP_NOT_AVAILABLE_IMAGE = ''


# two clicks registered:  [  23 1350] [  61 1374]
# (2,) (2,) (2,)
# purple
# x,y: [0.03194444 0.91216216]
# w,h: [0.05277778 0.01621622]
# =========== IMAGE SAVED========
# two clicks registered:  [  24 1353] [  66 1381]
# (2,) (2,) (2,)
# blue
# x,y: [0.03333333 0.91418919]
# w,h: [0.05833333 0.01891892]
# =========== IMAGE SAVED========
# two clicks registered:  [ 121 1169] [ 600 1200]
# (2,) (2,) (2,)
# words
# x,y: [0.16805556 0.78986486]
# w,h: [0.66527778 0.02094595]
# =========== IMAGE SAVED========
# two clicks registered:  [  94 1150] [ 633 1297]
# (2,) (2,) (2,)
#  area
# x,y: [0.13055556 0.77702703]
# w,h: [0.74861111 0.09932432]
# =========== IMAGE SAVED========
def test_pokestop_screen(screenshot):
    """
    returns state of pokestop
    :return: PokestopState:state.
    """
    # relevant screen area for checking if close enough
    # relevant screen area for spun/available section
    pass
