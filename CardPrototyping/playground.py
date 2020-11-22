from CardPrototyping.Human import Human
from ApplicationManagers.ProgramController import ProgramController
adb_interface=ProgramController('ADB')
adb_interface.program.start_capture()

def print_on_update(*args, **kwargs):
    print("I GOT UPDATED: ", args, kwargs)


def print_every_5(*args, **kwargs):
    print("===========================")
    print("IM BEING PRINTED EVERY 5 seconds: ", args, kwargs)


h = Human()
import time

h.register_move_update(print_on_update)
h.register_move_update(print_every_5, 5)

for i in range(100):
    time.sleep(1)
    h.move_update(1, 2)
