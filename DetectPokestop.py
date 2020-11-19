import cv2
import numpy as np


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