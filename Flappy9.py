# Flappy 9
# Mr Wagner

# what this code does

import pygame
from pygame.locals import *
import os
import random
import math

# class Background(pygame.sprite.Sprite):
#     def __init__(self, image_file, location):
#         pygame.sprite.Sprite.__init__(self)
#         self.image = pygame.image.load(image_file)
#         self.image = self.image.convert()
#         self.rect = self.image.get_rect()
#         self.rect.left, self.rect.top = location

class Png(pygame.sprite.Sprite):
    def __init__(self, image_file, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image_file)
        self.image = self.image.convert_alpha()
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
        self.stopped = False

    def update(self):
        if not self.stopped:
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
        self.stopped = True

    def update(self):
        if not self.stopped:
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
        self.stopped = False
        self.angle = 0.0
        #gravity variables
        self.grav = 0.0
        self.accel = 0.20
        self.jump = -7.0

        
    def update(self):
        if self.waiting == True:
            self.rect.top = self.location[1] + math.sin(self.angle) * 10
            self.angle += 0.1
            if self.angle >= 6.28:  # 2 time pi
                self.angle = 0.0
        elif not self.stopped:
            self.grav += self.accel
            self.rect.y += self.grav
        else:
            pass

    def flap(self):
        self.grav += self.jump

def MakePipes(Pipes):
    global SpritesFolder
    global ScreenWidth
    VertSpaceBetweenPipes = 150
    HorizSpaceBetweenPipes = ScreenWidth // 1.5
    PipeHeight = 320
    StartDelay = ScreenWidth * 1.5
    Pipes.empty()
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
Background = Png(filename, (0,0))

filename = os.path.join(SpritesFolder, "base.png")
Base = Foreground(filename, (0,400))

Pipes = pygame.sprite.Group()
MakePipes(Pipes)

Faby = Bird(os.path.join(SpritesFolder, "yellowbird-midflap.png"), (100, ScreenHeight//3))

Restart = Png(os.path.join(SpritesFolder, "restart.png"), (80,ScreenHeight//3))
Message = Png(os.path.join(SpritesFolder, "message.png"), (50,10))

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # == means is equal to
            GameRunning = False       # = means Gets... GameRunning variable gets the value false
        if event.type == KEYDOWN and event.key == pygame.K_SPACE \
                or event.type == pygame.MOUSEBUTTONDOWN:
                if Faby.waiting:
                    Faby.waiting = False
                    Faby.flap()
                    #start the pipes moving
                    for p in Pipes:
                        p.stopped = False
                elif Faby.stopped:
                    Faby.stopped = False
                    Faby.waiting = True
                    Faby.grav = 0.0
                    MakePipes(Pipes)
                else:
                    Faby.flap()

    screen.blit(Background.image, Background.rect)

    #draw our pipes
    for p in Pipes:
        screen.blit(p.image, p.rect)
        p.update()

    screen.blit(Faby.image, Faby.rect)
    Faby.update()

    if pygame.sprite.spritecollideany(Faby, Pipes) or \
        Faby.rect.bottom >= Base.rect1.top:
        #stop the base
        Base.stopped = True
        #stop the pipes
        for p in Pipes:
            p.stopped = True

    if Faby.rect.bottom + 10 >= Base.rect1.top:
        Faby.stopped = True

    #show welcome message when waiting
    if Faby.waiting:
        screen.blit(Message.image, Message.rect)

    if Faby.stopped:
        screen.blit(Restart.image, Restart.rect)


    screen.blit(Base.image, Base.rect1)
    screen.blit(Base.image, Base.rect2)
    Base.update()

    pygame.display.update()
    clock.tick(fps) #for every second at most 60 frames (loops) can pass
    #print(clock.get_fps())

#out of the while loop
print("Game over")
pygame.quit()