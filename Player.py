import pygame

class Player:
    def __init__(self, name, img_path='', x=0, y=0, x_change=0, hp=0, score=0):
        self.img = None
        self.x = x
        self.y = y
        self.x_change = x_change
        self.hp = hp
        # self.name = name
        # self.score = score
        self.isDead = False

        if img_path:
            self.img = pygame.image.load('resources/images/spaceship.png')

    def show(self, screen):
        if self.img:
            screen.blit(self.img, (self.x, self.y))

