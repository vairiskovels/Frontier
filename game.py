# © 2019 Vairis Kovels All Rights Reserved

import time, random, math
import pygame
from pygame.locals import *
pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()

# ======================= Variables =======================

# ------------------------ Screen -------------------------

screenWidth = 928
screenHeight = 557
display = pygame.display.set_mode((screenWidth,screenHeight))
pygame.display.set_caption("Frontier")

bg = pygame.image.load('images/background.jpg').convert()
bgWidth, bgHeight = bg.get_rect().size
bg_x = 0



# ---------------------- Character ------------------------

walkRight = [pygame.image.load('images/character/R1.png'), pygame.image.load('images/character/R2.png'), pygame.image.load('images/character/R3.png'), pygame.image.load('images/character/R4.png'), pygame.image.load('images/character/R5.png'), pygame.image.load('images/character/R6.png')]
walkLeft = [pygame.image.load('images/character/L1.png'), pygame.image.load('images/character/L2.png'), pygame.image.load('images/character/L3.png'), pygame.image.load('images/character/L4.png'), pygame.image.load('images/character/L5.png'), pygame.image.load('images/character/L6.png')]
jump = [pygame.image.load('images/character/J1.png'), pygame.image.load('images/character/J2.png'), pygame.image.load('images/character/J3.png'), pygame.image.load('images/character/J4.png'), pygame.image.load('images/character/J5.png'), pygame.image.load('images/character/J6.png')]
char = [pygame.image.load('images/character/I1.png'), pygame.image.load('images/character/I2.png'), pygame.image.load('images/character/I3.png'), pygame.image.load('images/character/I4.png'), pygame.image.load('images/character/I5.png'), pygame.image.load('images/character/I6.png')]
attack = [pygame.image.load('images/character/A1.png'), pygame.image.load('images/character/A2.png'), pygame.image.load('images/character/A3.png'), pygame.image.load('images/character/A4.png'), pygame.image.load('images/character/A5.png'), pygame.image.load('images/character/A6.png')]

# ----------------------- Other ---------------------------

clock = pygame.time.Clock()

black = (0,0,0)
white = (255,255,255)
green = (0,255,0, 130)
greenyellow = (173,255,47)
yellow = (255,255,0,130)
red = (178,34,34,130) 
orange = (255,165,0,130)
darkorange = (255,140,0)


fps = 60

font = pygame.font.SysFont("font/Montserrat.ttf", 20)

music = pygame.mixer.music.load("music/soundtrack.mp3")
pygame.mixer.music.play(-1)

swingSound = pygame.mixer.Sound("music/swing.wav")
swingSound.set_volume(0.2)

impactSound = pygame.mixer.Sound("music/impact.wav")
impactSound.set_volume(0.05)

grassSound = pygame.mixer.Sound("music/grass_2.wav")
grassSound.set_volume(0.05)

introImage = pygame.image.load('images/main_menu.jpg')



# ======================= Functions =======================

    


class player(object):
    def __init__(self,x,y,width,height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 8
        self.isJump = False
        self.left = False
        self.right = False
        self.idle = False
        self.hit = False
        self.walkCount = 0
        self.hitCount = 40
        self.jumpCount = 21
        self.idleCount = 6
        self.hp = 81
        self.hitbox = (self.x + 32,self.y + 10,45,70)

    def draw(self, display):

        healthBarWidth = self.hp * 1.6
        healthBarHeight = 20

        healthOutWidth = 160
        healthOutHeight = healthBarHeight

        if self.walkCount + 1 >= 30:
            self.walkCount = 0
        if self.idleCount + 1 >= 54:
            self.idleCount = 0
        

        if self.left:
            display.blit(walkLeft[self.walkCount//5], (self.x,self.y))
            self.walkCount += 1
        elif self.right:
            display.blit(walkRight[self.walkCount//5], (self.x,self.y))
            self.walkCount += 1
        elif self.hit:
            display.blit(attack[self.hitCount//10], (self.x, self.y))
            self.hitCount -= 1
        elif self.isJump:
            display.blit(jump[self.jumpCount//7], (self.x,self.y))
            self.jumpCount -= 1
        elif self.idle:
            display.blit(char[self.idleCount//9], (self.x,self.y))
            self.idleCount += 1
        
        self.hitbox = (self.x + 32,self.y + 10,45,70)
       #pygame.draw.rect(display, (255,0,0), self.hitbox, 2)

        if self.hp > 75:
            player_health_color = green
        elif self.hp > 50:
            player_health_color = yellow
        elif self.hp > 25:
            player_health_color = orange
        elif self.hp > 1:
            player_health_color = red
        else:
            player_health_color = black

        healthBar = pygame.Surface((healthBarWidth,healthBarHeight), pygame.SRCALPHA, 32)
        healthBar.fill(player_health_color)
        display.blit(healthBar, (20,20))

        pygame.draw.rect(display, yellow, (20, 20, healthOutWidth, healthOutHeight), 2)


            
class enemy(object):
    stayIdle = [pygame.image.load('images/enemy/t4.png'), pygame.image.load('images/enemy/t3.png'), pygame.image.load('images/enemy/t3.png'), pygame.image.load('images/enemy/t1.png'), pygame.image.load('images/enemy/t2.png'), pygame.image.load('images/enemy/t3.png'), pygame.image.load('images/enemy/t4.png')]
    enemyDie = [pygame.image.load("images/enemy/d1.png"), pygame.image.load("images/enemy/d2.png"), pygame.image.load("images/enemy/d3.png"), pygame.image.load("images/enemy/d4.png"), pygame.image.load("images/enemy/d5.png"), pygame.image.load("images/enemy/d6.png"), pygame.image.load("images/enemy/d7.png"), pygame.image.load("images/enemy/d8.png"), pygame.image.load("images/enemy/d9.png"), pygame.image.load("images/enemy/d10.png")]

    def __init__(self,x,y,width,height,hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.end = end
        self.path = [self.x]
        self.idleCount = 0
        self.dieCount = 0
        self.vel = 2
        self.hp = hp
        self.hitbox = (self.x + 12,self.y +5,45,70)

    def draw(self,display):
        if self.idleCount + 1 >= 56:
            self.idleCount = 0

        if self.vel > 0: 
            display.blit(self.stayIdle[self.idleCount//8], (self.x, self.y))
            self.idleCount += 1

        self.hitbox = (self.x + 12,self.y +5,45,70)
        #pygame.draw.rect(display, (255,0,0), self.hitbox, 2)
        
        if self.hp > 90:
            enemy_health_color = green
        elif self.hp > 75:
            enemy_health_color = greenyellow
        elif self.hp > 50:
            enemy_health_color = yellow
        elif self.hp > 25:
            enemy_health_color = orange
        elif self.hp > 10:
            enemy_health_color = darkorange
        elif self.hp > 1:
            enemy_health_color = red
        else:
            enemy_health_color = black
        
        pygame.draw.rect(display, enemy_health_color, (self.x + 15, self.y, 40, 5))


    '''def move(self):
        if self.vel > 0:
            if self.x + self.vel < self.path[1]:
                self.x += self.vel
            else:
                self.vel = self.vel * - 1
                self.walkCount = 0
        else:
            if self.x - self.vel > self.path[0]:
                self.x += self.vel 
            else:
                self.vel = self.vel * - 1
                self.walkCount = 0
                '''

def game_intro():
    intro = True

    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    intro = False
                    run = True

        display.blit(introImage, (0,0))
        pygame.display.update()

        
def backgroundMoving():
    global bg_x
    bg_rel_x = bg_x % bg.get_rect().width
    display.blit(bg, (bg_rel_x - bg.get_rect().width,0))
    if bg_rel_x < screenWidth:
        display.blit(bg, (bg_rel_x,0))

enemyLocations = [600, 900] 

def collision():
        col = 80
        if man.x >= en.x - col and man.x <= en.x and event.type == pygame.MOUSEBUTTONDOWN and en.hp != 0:
            en.hp -= 2
            print("hit", en.hp)
            impactSound.play()
        if man.x >= en1.x - col and man.x <= en1.x and event.type == pygame.MOUSEBUTTONDOWN and en1.hp != 0:
            en1.hp -= 1
            print("hit", en1.hp)
            impactSound.play()
        elif en.hp > 1:
            print("no hit",en.hp)
        else:
            print("dead")

def redrawGameWindow():
    backgroundMoving()
    collision()
    playerx = font.render("player x : " + str(man.x), 1, white)
    playery = font.render("player y : " + str(man.y), 1, white)
    hp = font.render("HP : " + str(man.hp), 1, white)
    display.blit(playerx, (780,10))
    display.blit(playery, (780,30))
    display.blit(hp, (80,23))
    if en.hp > 0:
        en.draw(display)
    else:
        if en.dieCount + 1 <= 100:
            display.blit(en.enemyDie[en.dieCount//10], (en.x, en.y))
            en.dieCount += 1
    if en1.hp > 0:
        en1.draw(display)
    else:
        if en1.dieCount + 1 <= 100:
            display.blit(en1.enemyDie[en1.dieCount//10], (en1.x, en1.y))
            en1.dieCount += 1
    man.draw(display)
    pygame.display.update()
    

run = True
man = player(100, 440, 110, 81)
en = enemy(enemyLocations[0], 435, 110, 81, 100)
en1 = enemy(enemyLocations[1], 435, 110, 81, 55)
player_health = man.hp
enemy_health = en.hp
bg_vel = man.vel

# ======================= Main loop =======================

while run:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == KEYDOWN:
               if event.key == K_ESCAPE:
                   pygame.quit()

    keys = pygame.key.get_pressed()
    
    if keys[pygame.K_LEFT] and man.x > man.vel or keys[pygame.K_a] and man.x > man.vel: 
        man.x -= man.vel
        man.left = True
        man.right = False
        grassSound.play()
        if man.x <= 376:
            bg_x += bg_vel
            man.vel = 0
            en.x += bg_vel
            en1.x += bg_vel
            


    elif keys[pygame.K_RIGHT] and man.x < screenWidth - man.width - man.vel or keys[pygame.K_d] and man.x < screenWidth - man.width - man.vel:  
        man.x += man.vel
        man.left = False
        man.right = True
        grassSound.play()
        if man.x > screenWidth / 2.5:
            bg_x -= bg_vel 
            man.vel = 0
            en.x -= bg_vel
            en1.x -= bg_vel
            

    else: 
        man.idle = True
        man.left = False
        man.right = False
        man.walkCount = 0
    
    if not(man.hit):
        if event.type == pygame.MOUSEBUTTONDOWN:
            swingSound.play()
            man.hit = True
            man.left = False
            man.right = False
            man.isJump = False

    else:
        if man.hitCount >= -18:
            man.hitCount -= 1
            man.left = False
            man.right = False
            man.isJump = False
        else:
            man.hitCount = 18
            man.hit = False

    if not(man.isJump):
        if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
            man.isJump = True
            man.left = False
            man.right = False
            man.hit = False
            man.walkCount = 0
    else:
        if man.jumpCount >= -21:
            man.y -= (man.jumpCount * abs(man.jumpCount)) * 0.06
            man.jumpCount -= 1
            man.left = False
            man.right = False
            man.hit = False
        else: 
            man.jumpCount = 21
            man.isJump = False



    redrawGameWindow()
    
  
pygame.quit()
