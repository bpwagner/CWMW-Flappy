# Flappy 14
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
        self.up_rect = self.rect.copy()
        self.up_rect.height = 1000000
        self.up_rect.bottom = self.rect.top
        self.sibling = None
        self.stopped = True
        self.score_counted  = False

    def update(self):
        if not self.stopped:
            VertSpaceBetweenPipes = 150
            PipeHeight = 320
            self.rect.left -= 1
            self.up_rect.left -= 1
            if self.rect.right == 0 and self.sibling != None:
                self.rect.left = self.rect.width * 10
                self.sibling.rect.left = self.rect.width * 10
                rnd = random.randint(150, 350)
                self.sibling.rect.top = rnd #set the bottom pipe
                self.rect.top = rnd - VertSpaceBetweenPipes - PipeHeight
                self.score_counted = False
                self.up_rect = self.rect.copy()
                self.up_rect.height = 1000000
                self.up_rect.bottom = self.rect.top

class Bird(pygame.sprite.Sprite):
    def __init__(self, image_file_list, location):
        pygame.sprite.Sprite.__init__(self)
        self.imgs = []
        self.imgs_index = 1 #state of flap during game
        self.imgs.append(pygame.image.load(image_file_list[0]).convert_alpha())#up
        self.imgs.append(pygame.image.load(image_file_list[1]).convert_alpha())#mid
        self.imgs.append(pygame.image.load(image_file_list[2]).convert_alpha())#down
        self.imgs.append(pygame.image.load(image_file_list[1]).convert_alpha())#mid
        self.image = self.imgs[self.imgs_index]
        #used to slow down the bird flapping
        self.frame_counter = 0
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
        self.frame_counter += 1
        if self.frame_counter == 7:
            self.imgs_index += 1
            if self.imgs_index == len(self.imgs):
                self.imgs_index = 0
            self.frame_counter = 0

        if self.waiting == True:
            self.rect.top = self.location[1] + math.sin(self.angle) * 10
            self.angle += 0.1
            if self.angle >= 6.28:  # 2 time pi
                self.angle = 0.0
            self.image = self.imgs[self.imgs_index]
        elif not self.stopped:
            self.grav += self.accel
            self.rect.y += self.grav
            if self.grav >= 7:
                self.image = pygame.transform.rotate(self.imgs[self.imgs_index], -90)
            elif self.grav >= 5:
                self.image = pygame.transform.rotate(self.imgs[self.imgs_index], -45)
            elif self.grav >= -2:
                self.image = self.imgs[self.imgs_index]
            else:
                self.image = pygame.transform.rotate(self.imgs[self.imgs_index], 45)
        else:
            pass

    def flap(self):
        self.grav += self.jump

class TextBox:
    def __init__(self, x,y, size, \
                 color = pygame.Color("white"), \
                 bg_color = pygame.Color("black")):
        self.x = x
        self.y = y
        self.font = pygame.font.Font(None, size)
        self.color = color
        self.bg_color = bg_color

    def draw(self, screen, text):
        text_bitmap = self.font.render(text, True, self.color, self.bg_color)
        screen.blit(text_bitmap, (self.x, self.y))

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

#sound stuff
pygame.mixer.init()
AudioFolder = "audio"
volume = 0.1 #0 - 1.0
swoosh = pygame.mixer.Sound(os.path.join(AudioFolder, "swoosh.ogg"))
swoosh.set_volume(volume)
wing = pygame.mixer.Sound(os.path.join(AudioFolder, "wing.ogg"))
wing.set_volume(volume)
point = pygame.mixer.Sound(os.path.join(AudioFolder, "point.ogg"))
point.set_volume(volume)
hit = pygame.mixer.Sound(os.path.join(AudioFolder, "hit.ogg"))
hit.set_volume(volume)
die = pygame.mixer.Sound(os.path.join(AudioFolder, "die.ogg"))
die.set_volume(volume)


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

FabyImgs = [os.path.join(SpritesFolder, "yellowbird-upflap.png"),\
            os.path.join(SpritesFolder, "yellowbird-midflap.png"),\
            os.path.join(SpritesFolder, "yellowbird-downflap.png")]

Faby = Bird(FabyImgs, (100, ScreenHeight//3))

Restart = Png(os.path.join(SpritesFolder, "restart.png"), (80,ScreenHeight//3))
Message = Png(os.path.join(SpritesFolder, "message.png"), (50,10))

Score = 0
HighScore = 0
txtScore = TextBox(80,430,40,(0,0,0), (221,216,157))
txtHighScore = TextBox(50,470,40,(0,0,0), (221,216,157))

GameRunning = True
while GameRunning:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: # == means is equal to
            GameRunning = False       # = means Gets... GameRunning variable gets the value false
        if event.type == KEYDOWN and event.key == pygame.K_SPACE \
                or event.type == pygame.MOUSEBUTTONDOWN:
                if Faby.waiting:
                    pygame.mixer.Sound.play(swoosh)
                    Faby.waiting = False
                    Faby.flap()
                    #start the pipes moving
                    for p in Pipes:
                        p.stopped = False
                elif Faby.stopped: #restart code
                    if Score > HighScore:
                        HighScore = Score
                    Score = 0
                    Faby.stopped = False
                    Faby.waiting = True
                    Faby.grav = 0.0
                    MakePipes(Pipes)
                    Base.stopped = False
                else:
                    if not Base.stopped:
                        pygame.mixer.Sound.play(wing)
                        Faby.flap()

    screen.blit(Background.image, Background.rect)

    #draw our pipes
    for p in Pipes:
        screen.blit(p.image, p.rect)
        p.update()

    screen.blit(Faby.image, Faby.rect)
    Faby.update()

    for p in Pipes:
        if Faby.rect.left >= p.rect.right and not p.score_counted and \
                p.sibling != None:
            pygame.mixer.Sound.play(point)
            Score += 1
            p.score_counted = True
            break

    if pygame.sprite.spritecollideany(Faby, Pipes) or \
        Faby.rect.bottom >= Base.rect1.top:
        if not Base.stopped:
            pygame.mixer.Sound.play(hit)
        #stop the base
        Base.stopped = True
        #stop the pipes
        for p in Pipes:
            p.stopped = True

    #collision with the invisible rectangle
    for p in Pipes:
        if pygame.Rect.colliderect(Faby.rect, p.up_rect) and p.sibling is not None:
            Faby.grav = 10.0
            Faby.accel = 0.20
            Faby.rect.bottom = 0
            if not Base.stopped:
                pygame.mixer.Sound.play(hit)
            # stop the base
            Base.stopped = True
            # stop the pipes
            for p in Pipes:
                p.stopped = True


    if Faby.rect.bottom + 10 >= Base.rect1.top:
        if not Faby.stopped:
            pygame.mixer.Sound.play(die)
        Faby.stopped = True
        #stop the base
        Base.stopped = True
        #stop the pipes
        for p in Pipes:
            p.stopped = True

    #show welcome message when waiting
    if Faby.waiting:
        screen.blit(Message.image, Message.rect)

    if Faby.stopped:
        screen.blit(Restart.image, Restart.rect)


    screen.blit(Base.image, Base.rect1)
    screen.blit(Base.image, Base.rect2)
    Base.update()

    txtScore.draw(screen, f"Score: {Score}")
    txtHighScore.draw(screen, f"High Score: {HighScore}")

    pygame.display.update()
    clock.tick(fps) #for every second at most 60 frames (loops) can pass
    #print(clock.get_fps())

#out of the while loop
print("Game over")
pygame.quit()