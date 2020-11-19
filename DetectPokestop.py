import cv2
import numpy as np

from ImgTools import TfImageFinder
from conv import load_model
from conv import preprocess_images

POKESTOP_MODEL_PATH = 'models/PokestopDetect'
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
    for i, img in enumerate(img_list):
        print('CLEANING IMAGE: ', i)
        print(img.shape)
        print(type(img))
        print(img[0][0])
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
