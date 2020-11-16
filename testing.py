from ProgramCotntroller import *
from ImgTools import crop_img_percent, save_img

p = ProgramController('scrcpy-noconsole.exe', WINDOW_TITLE, 0)
p.window.prepare_screenshot()
s = p.window.get_latest_screenshot()
s = crop_img_percent(s, 0, .3, 1, .5)
from DetectPokestop import clean_img

s = clean_img(s)
# print(s)
save_img(s, 'pokestop_detect' + str(1) + '.png')
