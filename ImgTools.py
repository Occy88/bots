# Purpose of this file is to manage a screenshot that has been taken,
# make it easy to get a section of the specified section of the screenshot etc...
import cv2
import sys
import os
import win32gui
import win32ui
import win32con
import win32api
from Win32Wrapper import Win32Wrapper
import cv2 as cv
import numpy as np
from matplotlib import pyplot as plt

IMG_ROOT = os.path.abspath(os.curdir).split('bots')[0] + 'bots\\'


def crop_img(img, x, y, w, h):
    crop_img = img[y:y + h, x:x + w]
    return crop_img


def crop_img_percent(img, x, y, w, h):
    t_h = len(img)
    t_w = len(img[0])
    p_x = int(t_w * x)
    p_y = int(t_h * y)
    p_w = int(t_w * w)
    p_h = int(t_h * h)
    return crop_img(img, p_x, p_y, p_w, p_h)


def save_img(img, name):
    cv2.imwrite(IMG_ROOT + name, img, )


def load_img(name):
    print(IMG_ROOT + name)

    return cv2.imread(IMG_ROOT + name)


def get_cursor_location():
    flags, hcursor, (x, y) = win32gui.GetCursorInfo()

    return win32api.GetCursorPos()


def crop_center(img, x, y, width, height):
    return crop_img(img, int(x - width / 2), int(y - height / 2), width, height)


def template_match(template, test_img_path):
    img2 = template
    template = load_img(test_img_path)
    w2, h2 = img2.shape[0], img2.shape[1]
    w, h = template.shape[0], template.shape[1]

    img = img2.copy()
    method = cv.TM_CCOEFF
    # Apply template Matching
    res = cv.matchTemplate(img2,template,cv.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    return res
    # # print(w,h)
    # # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    # if method in [cv.TM_SQDIFF, cv.TM_SQDIFF_NORMED]:
    #     top_left = min_loc
    # else:
    #     top_left = max_loc
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv.rectangle(img, top_left, bottom_right, 255, 2)
    # plt.subplot(121), plt.imshow(res, cmap='gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(img, cmap='gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.show()
    # return min_val, max_val, np.array(max_loc) + np.array((w2 / 2, h2 / 2))
