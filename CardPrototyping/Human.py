from CardPrototyping.GenericCard import GenericCard


class Human(GenericCard):
    def __init__(self):
        super().__init__(Human)

    def move_update(self, x,y):
        print("MOVEMENT UPDATED :D")
        self.x = x
        self.y = y
        print(x, y)


def print_on_update(*args, **kwargs):
    print("I GOT UPDATED: ", args, kwargs)


def print_every_5(*args, **kwargs):
    print("===========================")
    print("IM BEING PRINTED EVERY 5 seconds: ", args, kwargs)


h = Human()
import inspect
import time

h.register_move_update(print_on_update)
h.register_move_update(print_every_5, 5)

for i in range(100):
    time.sleep(1)
    h.move_update(1,2)