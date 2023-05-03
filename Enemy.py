import math
class Enemy:
    def __init__(self, img, x, y, x_change, y_change):
        self.img = img
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change

    def show(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def isCollision(self, bullet):
        distance = math.sqrt(math.pow(self.x - bullet.x, 2) + (math.pow(self.y - bullet.y, 2)))
        if distance < 27:
            return True
        else:
            return False
