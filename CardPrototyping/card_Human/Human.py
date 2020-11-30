from CardPrototyping.GenericCard import GenericCardTemplate


class Human(GenericCardTemplate()):
    def __init__(self, name):
        super().__init__(self)
        self.name = name

    def on_say(self, words):
        print(self.name, " SAID: ", words)

    def on_move(self, x, y):
        self.x = x
        self.y = y
        print("HUMAN HAS MOVED: ", x, y)
