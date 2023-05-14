
class Bullet:
    def __init__(self, img, x, y, x_change, y_change, state):
        self.img = img
        self.x = x
        self.y = y
        self.x_change = x_change
        self.y_change = y_change
        self.state = state

    def show(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def fire_bullet(self, screen):
        self.state = "fire"
        screen.blit(self.img, (self.x + 16, self.y + 10))