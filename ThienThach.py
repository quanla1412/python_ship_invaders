import math

class ThienThach:
    def __init__(self, img, x, y, y_change):
        self.img = img
        self.x = x
        self.y = y
        self.y_change = y_change

    def show(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def isCollide(self, player):
        distance = math.sqrt(math.pow(self.x - player.x, 2) + (math.pow(self.y - player.y, 2)))
        if distance < 64:
            return True
        else:
            return False

