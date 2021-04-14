# Purpose of this file is to manage a screenshot that has been taken,
# make it easy to get a section of the specified section of the screenshot etc...
import glob
import json
import math
import os
import sys
import uuid
from PIL import Image
import cv2
import matplotlib.pyplot as plt
import numpy as np
import scipy
from scipy.ndimage.filters import maximum_filter
from scipy.ndimage.morphology import generate_binary_structure, binary_erosion


def crop_img(img, x, y, w, h, as_percentage=False):
    if as_percentage:
        t_h = len(img)
        t_w = len(img[0])
        x = int(t_w * x)
        y = int(t_h * y)
        w = int(t_w * w)
        h = int(t_h * h)
    crop_img = img[y:y + h, x:x + w]
    return crop_img


# def crop_img_percent(img, x, y, w, h):
#     return crop_img(img, p_x, p_y, p_w, p_h)


def crop_img_two_coords(img, x1, y1, x2, y2, as_percentage=False):
    x = x1
    y = y1
    w = x2 - x1
    h = y2 - y1
    return crop_img(img, x, y, w, h, as_percentage)


def save_img(img, name, with_uuid=False, format='.png', path='images/'):
    """

    :param img:
    :param name:
    :param with_uuid:
    :return:
    """
    if not os.path.exists(path):
        os.makedirs(path)
    if with_uuid:
        name += '_' + uuid.uuid4().__str__()
    name += format
    print("writing to: ", path + name)
    cv2.imwrite(path + name, img, )


def load_img(name):
    return cv2.imread(name)


def resize_img(img, dim, percent=False):
    # print("resizeing")
    # print(img.shape,dim,percent)
    if percent:
        wh = np.array([img.shape[0], img.shape[1]]) * dim
        wh = np.round(wh).astype(int)
        dim = tuple(wh)
    # flip the dimension. for cv2 resize
    dim = tuple(np.flip(dim[:2]))
    n = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    # print(n.shape)
    # print("----------------------------")
    return n


def resize_images(img_list, dim):
    resized_arr = np.empty(shape=(len(img_list), *dim))
    for i, m in enumerate(img_list):
        resized_arr[i] = resize_img(m, dim)
    return resized_arr


def load_dir(file_regx, img_dim):
    filenames = glob.glob(file_regx)
    image_list = np.empty((len(filenames), *img_dim), dtype=np.uint8)
    for i, filename in enumerate(filenames):  # assuming gif
        image_list[i] = load_img(filename).astype(np.uint8)
    print('loaded: ', image_list.shape)
    return image_list


def show_img(img):
    plt.imshow(img)
    plt.show()


def crop_center(img, x, y, width, height):
    return crop_img(img, int(x - width / 2), int(y - height / 2), width, height)


def template_match_tfmodel(template, test_dim_np, preproces_func, predict_func, kx, ky):
    max_y, max_x = (np.array(template.shape) - np.array(test_dim_np))[:2]
    print(max_x, max_y)
    print(max_x * max_y)
    # check every k pixels
    max_x = math.floor(max_x / kx)
    max_y = math.floor(max_y / ky)
    X = np.empty((max_x * max_y, *test_dim_np), dtype=np.uint8)
    p = np.zeros((max_x * max_y, 2), dtype=np.uint8)
    crop_dim = np.flip(test_dim_np[:2])
    print("crop dimensions: ", crop_dim)
    index = 0
    for i in range(max_x):
        for j in range(max_y):
            x = i * kx
            y = j * ky
            p[index][0] = j
            p[index][1] = i
            X[index] = crop_img(template, x, y, *crop_dim)
            index += 1

    X = preproces_func(X)
    probs = predict_func(X)
    pict = np.zeros((max_y, max_x))
    for i, val in enumerate(probs):
        y, x = p[i]
        if (np.argmax(val) == 0):
            pict[y][x] = np.max(val)
        else:
            pict[y][x] = np.max(val)
    pict += np.min(pict)
    pict *= (1 / np.max(pict))
    return pict


def resize_bigger_to_smaller_img(img1, img2):
    if img1.shape == img2.shape:
        return img1, img2
    if np.sum(img1.shape) > np.sum(img2.shape):
        return resize_img(img1, img2.shape), img2
    else:
        return img1, resize_img(img2, img1.shape)


def get_image_difference(image_1, image_2):
    first_image_hist = cv2.calcHist([image_1], [0], None, [256], [0, 256])
    second_image_hist = cv2.calcHist([image_2], [0], None, [256], [0, 256])

    img_hist_diff = cv2.compareHist(first_image_hist, second_image_hist, cv2.HISTCMP_BHATTACHARYYA)
    img_template_probability_match = \
        cv2.matchTemplate(first_image_hist, second_image_hist, cv2.TM_CCOEFF_NORMED)[0][0]
    img_template_diff = 1 - img_template_probability_match

    # taking only 10% of histogram diff, since it's less accurate than template method
    commutative_image_diff = (img_hist_diff / 10) + img_template_diff
    return commutative_image_diff


def find_circles(img, radius_range=np.array([0, 1]), area=np.array([0, 0, 0, 1]), as_percent=True):
    img2 = crop_img(img, *area, as_percentage=as_percent)
    # img2 = threshold(img2, np.array([200, 200, 200]), np.array([255, 255, 255]))

    gray = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)
    show_img(gray)
    try:
        circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 1.2, 100)[0]
    except Exception as e:
        print("None Found")
        return []
    min_r = radius_range[0] * img.shape[1]
    max_r = radius_range[1] * img.shape[1]

    circles = circles.astype(int)
    circles += np.array([area[0] * img.shape[1], area[1] * img.shape[0], 0]).astype(int)
    circles = circles.astype(int)
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(img, (x, y), r, (255, 0, 0), 4)
        cv2.rectangle(img, (x - 5, y - 5), (x + 5, y + 5), (255, 128, 0), -1)
    show_img(img)
    print("IMAGE SHOWN: ",len(circles))
    circles = circles[circles[:, 2] > min_r]
    circles = circles[circles[:, 2] < max_r]
    print(len(circles))
    for c in circles:
        print(c)
    return circles

def img_col_similarity(img1, img2):
    """
    returns similarity of two image by color:
    using mse for now/
    summ diff/total
    :param img1:
    :param img2:
    :return:
    """
    # print(get_image_difference(img1,img2))
    print("comp sim")
    print(img1.shape, img2.shape)
    img1, img2 = resize_bigger_to_smaller_img(img1, img2)
    print(img1.shape, img2.shape)
    err = np.sum((img1.astype("float") - img2.astype("float")) ** 2)
    err /= (255 * np.prod(img1.shape))
    # # show_img(img1)
    # # show_img(img2)
    # img3 = cv2.subtract(img1, img2)
    # # print(img3[0])
    # # show_img(img3)
    # tot = 125 * np.prod(img1.shape)
    # delta = np.sum(img3)
    print(1 - err)
    return 1 - err


def update_img_from_details(img_update_from, img_name, path, format='.png'):
    img = img_update_from

    # show_img(img)

    details = json.loads(open(path + img_name + '.json', 'r').read())
    img = crop_img(img, *details['xy'], *details['wh'], details['as_percentage'])
    save_img(img, img_name, format=format, path=path)


def find_peaks(p_2d_arr, threshold):
    """
    Finds all the maximas which are above a threshold on a 2d probability plane.
    :param p_2d_arr:
    :param threshold:
    :return:
    """
    # make zero anything bellow threshold.
    p_2d_arr[p_2d_arr < threshold] = 0

    # define an 8-connected neighborhood
    neighborhood = generate_binary_structure(2, 2)

    # apply the local maximum filter; all pixel of maximal value
    # in their neighborhood are set to 1
    local_max = maximum_filter(p_2d_arr, footprint=neighborhood) == p_2d_arr
    # local_max is a mask that contains the peaks we are
    # looking for, but also the background.
    # In order to isolate the peaks we must remove the background from the mask.

    # we create the mask of the background
    background = (p_2d_arr == 0)

    # a little technicality: we must erode the background in order to
    # successfully subtract it form local_max, otherwise a line will
    # appear along the background border (artifact of the local maximum filter)
    eroded_background = binary_erosion(background, structure=neighborhood, border_value=1)

    # we obtain the final mask, containing only peaks,
    # by removing the background from the local_max mask (xor operation)
    detected_peaks = local_max ^ eroded_background

    return scipy.ndimage.measurements.label(detected_peaks)


def threshold(img, threshold_lower, threshold_upper):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    mask = cv2.inRange(img, threshold_lower, threshold_upper)
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    return img & mask_rgb


def template_match(small_img, large_img):
    w2, h2 = large_img.shape[0], large_img.shape[1]
    w, h = small_img.shape[0], small_img.shape[1]

    img = small_img.copy()
    method = cv2.TM_CCOEFF
    # Apply template Matching

    res = cv2.matchTemplate(small_img, large_img, cv2.TM_CCOEFF_NORMED)
    threshold = 0.8
    loc = np.where(res >= threshold)
    return res
    # # print(w,h)
    # # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
    # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #     top_left = min_loc
    # else:
    #     top_left = max_loc
    # bottom_right = (top_left[0] + w, top_left[1] + h)
    # cv2.rectangle(img, top_left, bottom_right, 255, 2)
    # plt.subplot(121), plt.imshow(res, cmap='gray')
    # plt.title('Matching Result'), plt.xticks([]), plt.yticks([])
    # plt.subplot(122), plt.imshow(img, cmap='gray')
    # plt.title('Detected Point'), plt.xticks([]), plt.yticks([])
    # plt.show()
    # return min_val, max_val, np.array(max_loc) + np.array((w2 / 2, h2 / 2))


class Image:
    """
    Image in this project is an image of some fictional/actual larger image
    we specify it's crop function (x,y,w,h) as a percentage of the larger image so it can b cropped out.
    The above is as a percentage

    The image has an associated json file to which the state is saved and loaded from.

    """

    def __init__(self, crop_percent_dim=(0, 0, 1, 1), img=np.array([]), name='default', img_path='images/'):
        self.name = name
        self.img_path = img_path
        self.img = img
        self.crop_percent_dim = crop_percent_dim
        self.js_name = name

    def to_json(self):
        return json.dumps(self.__dict__)

    @staticmethod
    def load(js):
        return Image(**js)


class TfImageFinder:
    def __init__(self, model, preprocessor, match_np_dim=(100, 150), divisor=(4, 4), threshold=0.8):
        """

        :param model:
        :param preprocessor:
        :param match_np_dim:
        :param divisor:
        :param threshold:
        """
        self.preprocessor = preprocessor
        self.model = model
        self.match_np_dim = np.array(match_np_dim)
        self.divisor = np.array(divisor)
        self.threshold = threshold

    def find_locations(self, test_img):
        pict = template_match_tfmodel(test_img, self.match_np_dim, self.preprocessor, self.model.predict, *self.divisor)
        pict_peaks = find_peaks(pict, self.threshold)
        print("===========================")
        peaks = np.where(pict_peaks[0] > self.threshold)
        peaks = np.array(peaks)
        peaks = peaks.T
        peaks *= self.divisor
        offset = self.match_np_dim / 2
        print(offset)
        peaks += offset.astype(int)[:-1]
        # show_img(test_img)
        # show_img(pict)
        # show_img(pict_peaks[0])
        return pict, peaks


def find_image_locations(model, test_img, match_np_dim=(100, 150), divisor=(10, 10), threshold=0.8):
    pass
