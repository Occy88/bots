from ImageProcessing import conv
from ImageProcessing import ImgTools
from ImageProcessing import MLPictureGen
from ApplicationManagers import ProgramController
import time

gen=MLPictureGen.MLPictureGen()
time.sleep(5)
gen.capture_on_two_click()
