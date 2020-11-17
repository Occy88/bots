import time

from ImgTools import crop_img_percent, save_img, show_img
from ProgramCotntroller import *

WINDOW_TITLE = ''
p = ProgramController(WINDOW_TITLE)
p.program.start_capture()
time.sleep(10)
s = p.program.get_latest_screenshot()

# print(s)
s = crop_img_percent(s, 0, .3, 1, .5)
from DetectPokestop import clean_img

s = clean_img(s)
show_img(s)
save_img(s, 'pokestop_detect' + str(1) + '.png')
