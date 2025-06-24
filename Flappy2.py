# Flappy 2
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

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # == means is equal to
            GameRunning = False       # = means Gets... GameRunning variable gets the value false

    screen.blit(Background.image, Background.rect)
    screen.blit(Base.image, Base.rect)

    pygame.display.update()
    clock.tick(fps) #for every second at most 60 frames (loops) can pass
    #print(clock.get_fps())

#out of the while loop
print("Game over")
pygame.quit()