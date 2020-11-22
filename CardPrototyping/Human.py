from CardPrototyping.GenericCard import GenericCard


class Human(GenericCard):
    def __init__(self):
        super().__init__(Human)

    def move_update(self, x,y):
        print("MOVEMENT UPDATED :D")
        self.x = x
        self.y = y
        print(x, y)


