# Flappy 4
# Mr Wagner

# what this code does

import pygame
from pygame.locals import *
import os

class Background(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

class Foreground(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.rect1 = self.rect.copy()
        self.rect2 = self.rect.copy()
        self.i = self.rect.w
        self.w = self.rect.w
        self.rect2.left = self.w

    def update(self):
        self.rect1.left = self.i - self.w
        self.rect2.left = self.i
        self.i -= 1
        if self.i == 0:
            self.i = self.w

class Pipe(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

    def update(self):
        self.rect.left -= 1
        if self.rect.right == 0:
            self.rect.left = self.rect.width * 10

pygame.init()
clock = pygame.time.Clock()
fps = 60

ScreenHeight = 512
ScreenWidth = 288

pygame.display.set_caption("Flappy Birds")
screen = pygame.display.set_mode ( (ScreenWidth, ScreenHeight) )

SpritesFolder = "sprites"
filename = os.path.join(SpritesFolder, "background-day.png")
Background = Background(filename, (0,0))

filename = os.path.join(SpritesFolder, "base.png")
Base = Foreground(filename, (0,400))

UpPipe = Pipe(os.path.join(SpritesFolder, "pipe-green-upper.png"), (200, -100))
DnPipe = Pipe(os.path.join(SpritesFolder, "pipe-green-lower.png"), (200, 300))

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # == means is equal to
            GameRunning = False       # = means Gets... GameRunning variable gets the value false

    screen.blit(Background.image, Background.rect)

    #draw our pipes
    screen.blit(UpPipe.image, UpPipe.rect)
    screen.blit(DnPipe.image, DnPipe.rect)
    UpPipe.update()
    DnPipe.update()

    screen.blit(Base.image, Base.rect1)
    screen.blit(Base.image, Base.rect2)
    Base.update()

    pygame.display.update()
    clock.tick(fps) #for every second at most 60 frames (loops) can pass
    #print(clock.get_fps())

#out of the while loop
print("Game over")
pygame.quit()