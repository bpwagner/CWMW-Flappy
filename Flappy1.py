# Flappy 1
# Mr Wagner


# what this code does

import pygame
from pygame.locals import *

pygame.init()
clock = pygame.time.Clock()
fps = 60

ScreenHeight = 512
ScreenWidth = 288

pygame.display.set_caption("Flappy Birds")
screen = pygame.display.set_mode ( (ScreenWidth, ScreenHeight) )

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # == means is equal to
            GameRunning = False       # = means Gets... GameRunning variable gets the value false


    pygame.display.update()
    clock.tick(fps) #for every second at most 60 frames (loops) can pass
    #print(clock.get_fps())

#out of the while loop
print("Game over")
pygame.quit()