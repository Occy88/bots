import cv2
import numpy as np

def clean_img(img):
    """
    remove all unnecessary colours (conecntrate on blue pokestops only)

    :param img:
    :return:q
    """
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    print(hsv)
    # Threshold of blue in HSV space
    lower_blue = np.array([35,190,130])
    upper_blue = np.array([170, 236, 255])

    # preparing the mask to overlay
    mask = cv2.inRange(hsv, lower_blue, upper_blue)

    # The black region in the mask has the value of 0,
    # so when multiplied with original image removes all non-blue regions
    result = cv2.bitwise_and(img, img, mask=mask)
    return result
def scan_for_pokestops(img):
    """
    assumes image is  in correct size format.
    :param img:
    :return: locations of confirmed pokestops.
    """
    img=clean_img(img)
    return img
    # img=detect(img)

