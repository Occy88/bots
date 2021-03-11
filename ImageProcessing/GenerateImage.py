from ImageProcessing import conv
from ImageProcessing import ImgTools
from ImageProcessing import MLPictureGen
import time

gen=MLPictureGen.MLPictureGen('adb')
time.sleep(5)
img_name='can_send_gift_profile'
# img_name='gift_received_profile'
path='../PokemonGo/images/FriendGifting/'
# gen.capture_on_two_click(img_name,path)
gen.test_image(path,img_name)
time.sleep(100)