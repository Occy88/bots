import time

from ImageProcessing.ImgTools import crop_img_percent, save_img, show_img
from ApplicationManagers.ProgramController import *

WINDOW_TITLE = ''
p = ProgramController(WINDOW_TITLE)
p.program.start_capture('adb')
time.sleep(10)
s = p.program.get_latest_screenshot()

# print(s)
s = crop_img_percent(s, 0, .3, 1, .5)
from PokemonGo.DetectPokestop import clean_img

s = clean_img([s])[0]
show_img(s)
save_img(s, 'pokestop_detect', True)
p.program.stop_all_threads()
