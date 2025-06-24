# Flappy 6
# Mr Wagner

# what this code does

import pygame
from pygame.locals import *
import os
import random
import math

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
        self.sibling = None

    def update(self):
        VertSpaceBetweenPipes = 150
        PipeHeight = 320
        self.rect.left -= 1
        if self.rect.right == 0 and self.sibling != None:
            self.rect.left = self.rect.width * 10
            self.sibling.rect.left = self.rect.width * 10
            rnd = random.randint(150, 350)
            self.sibling.rect.top = rnd #set the bottom pipe
            self.rect.top = rnd - VertSpaceBetweenPipes - PipeHeight

class Bird(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = self.image.convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.location = location
        self.waiting = True
        self.angle = 0.0

    def update(self):
        if self.waiting == True:
            self.rect.top = self.location[1] + math.sin(self.angle) * 10
            self.angle += 0.1
            if self.angle >= 6.28:  # 2 time pi
                self.angle = 0.0

def MakePipes(Pipes):
    global SpritesFolder
    global ScreenWidth
    VertSpaceBetweenPipes = 150
    HorizSpaceBetweenPipes = ScreenWidth // 1.5
    PipeHeight = 320
    StartDelay = ScreenWidth * 1.5
    for c in range (3):
        rnd = random.randint(150,350) #top of bottom pipe
        dn = Pipe(os.path.join(SpritesFolder, 'pipe-green-lower.png'), \
                  (StartDelay + HorizSpaceBetweenPipes*c, rnd))
        up = Pipe(os.path.join(SpritesFolder, 'pipe-green-upper.png'),
                  (StartDelay + HorizSpaceBetweenPipes*c, \
                  rnd - VertSpaceBetweenPipes - PipeHeight))
        Pipes.add(up)
        Pipes.add(dn)
        up.sibling = dn





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

Pipes = pygame.sprite.Group()
MakePipes(Pipes)

Faby = Bird(os.path.join(SpritesFolder, "yellowbird-midflap.png"), (100, ScreenHeight//3))

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # == means is equal to
            GameRunning = False       # = means Gets... GameRunning variable gets the value false

    screen.blit(Background.image, Background.rect)

    #draw our pipes
    for p in Pipes:
        screen.blit(p.image, p.rect)
        p.update()

    screen.blit(Faby.image, Faby.rect)
    Faby.update()

    screen.blit(Base.image, Base.rect1)
    screen.blit(Base.image, Base.rect2)
    Base.update()

    pygame.display.update()
    clock.tick(fps) #for every second at most 60 frames (loops) can pass
    #print(clock.get_fps())

#out of the while loop
print("Game over")
pygame.quit()