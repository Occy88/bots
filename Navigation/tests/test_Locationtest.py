from ProgramCotntroller import ProgramController

p = ProgramController('scrcpy.exe', 'SM-G9650', 0)
p.window.prepare_screenshot()
s = p.window.capture_screenshot()

from Navigation.LocationTest import test_home

test_home(s)
p.window.release()
