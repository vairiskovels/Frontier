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
screenSize = (screenWidth, screenHeight)
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
die = [pygame.image.load("images/character/D1.png"), pygame.image.load("images/character/D2.png"), pygame.image.load("images/character/D3.png"), pygame.image.load("images/character/D4.png"), pygame.image.load("images/character/D5.png"), pygame.image.load("images/character/D6.png"), pygame.image.load("images/character/D7.png")]


# ----------------------- Other ---------------------------

clock = pygame.time.Clock()

black = (0, 0, 0)
white = (255, 255, 255)
green1 = (0, 255, 64, 130)
green2 = (0, 255, 0, 130)
green3 = (64, 255, 0 , 130)
limeGreen = (128, 255, 0, 130)
greenYellow = (191, 255, 0, 130)
yellow = (255, 255, 0, 130)
orange = (255, 191, 0, 130)
darkOrange = (255, 128, 0, 130)
red1 = (255, 64, 0, 130)
red2 = (255, 0, 0, 130)


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
        self.dieCount = 0
        self.hp = 100
        self.hitbox = (self.x + 32,self.y + 10,45,70)

    def draw(self, display):
        global egx
        if self.hp > 0:
            healthBarWidth = self.hp * 1.6
        else:
            healthBarWidth = 1

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

        if self.hp > 90:
            player_health_color = green1
        elif self.hp > 80:
            player_health_color = green2
        elif self.hp > 70:
            player_health_color = green3
        elif self.hp > 60:
            player_health_color = limeGreen
        elif self.hp > 50:
            player_health_color = greenYellow
        elif self.hp > 40:
            player_health_color = yellow
        elif self.hp > 30:
            player_health_color = orange
        elif self.hp > 20:
            player_health_color = darkOrange
        elif self.hp > 10:
            player_health_color = red1
        elif self.hp > 1:
            player_health_color = red2
        else:
            player_health_color = black

        healthBar = pygame.Surface((healthBarWidth,healthBarHeight), pygame.SRCALPHA, 32)
        healthBar.fill(player_health_color)
        display.blit(healthBar, (20,20))

        pygame.draw.rect(display, yellow, (20, 20, healthOutWidth, healthOutHeight), 2)

    def handleKeys(self):
        global bg_x, bg_vel, egx
        keys = pygame.key.get_pressed()
    
        if keys[pygame.K_LEFT] and self.x > self.vel or keys[pygame.K_a] and self.x > self.vel: 
            self.x -= self.vel
            self.left = True
            self.right = False
            grassSound.play()
            if self.x <= 376:
                bg_x += bg_vel
                self.vel = 0
                en.x += bg_vel
                en1.x += bg_vel
                en2.x += bg_vel
                en3.x += bg_vel
                en4.x += bg_vel
                en5.x += bg_vel
                en6.x += bg_vel
                en7.x += bg_vel
                en8.x += bg_vel
                en9.x += bg_vel
                en10.x += bg_vel


        elif keys[pygame.K_RIGHT] and self.x < screenWidth - self.width - self.vel or keys[pygame.K_d] and self.x < screenWidth - self.width - self.vel:  
            self.x += self.vel
            self.left = False
            self.right = True
            grassSound.play()
            if self.x > screenWidth / 2.5:
                bg_x -= bg_vel 
                self.vel = 0
                en.x -= bg_vel
                en1.x -= bg_vel
                en2.x -= bg_vel
                en3.x -= bg_vel
                en4.x -= bg_vel
                en5.x -= bg_vel
                en6.x -= bg_vel
                en7.x -= bg_vel
                en8.x -= bg_vel
                en9.x -= bg_vel
                en10.x -= bg_vel

        else: 
            self.idle = True
            self.left = False
            self.right = False
            self.walkCount = 0
        
        if not(self.hit):
            if event.type == pygame.MOUSEBUTTONDOWN:
                swingSound.play()
                self.hit = True
                self.left = False
                self.right = False
                self.isJump = False

        else:
            if self.hitCount >= -18:
                self.hitCount -= 1
                self.left = False
                self.right = False
                self.isJump = False
            else:
                self.hitCount = 18
                self.hit = False

        if not(self.isJump):
            if keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]:
                self.isJump = True
                self.left = False
                self.right = False
                self.hit = False
                self.walkCount = 0
        else:
            if self.jumpCount >= -21:
                self.y -= (self.jumpCount * abs(self.jumpCount)) * 0.06
                self.jumpCount -= 1
                self.left = False
                self.right = False
                self.hit = False
            else: 
                self.jumpCount = 21
                self.isJump = False

            
class enemy(object):
    stayIdle = [pygame.image.load('images/enemy/t4.png'), pygame.image.load('images/enemy/t3.png'), pygame.image.load('images/enemy/t3.png'), pygame.image.load('images/enemy/t1.png'), pygame.image.load('images/enemy/t2.png'), pygame.image.load('images/enemy/t3.png'), pygame.image.load('images/enemy/t4.png')]
    enemyDie = [pygame.image.load("images/enemy/d1.png"), pygame.image.load("images/enemy/d2.png"), pygame.image.load("images/enemy/d3.png"), pygame.image.load("images/enemy/d4.png"), pygame.image.load("images/enemy/d5.png"), pygame.image.load("images/enemy/d6.png"), pygame.image.load("images/enemy/d7.png"), pygame.image.load("images/enemy/d8.png"), pygame.image.load("images/enemy/d9.png"), pygame.image.load("images/enemy/d10.png")]
    enemyAttack = [pygame.image.load("images/enemy/a1.png"), pygame.image.load("images/enemy/a2.png"), pygame.image.load("images/enemy/a3.png"), pygame.image.load("images/enemy/a4.png"), pygame.image.load("images/enemy/a5.png"), pygame.image.load("images/enemy/a6.png"), pygame.image.load("images/enemy/a7.png"), pygame.image.load("images/enemy/a8.png")]

    def __init__(self,x,y,width,height,hp):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        #self.end = end
        self.path = [self.x]
        self.idleCount = 0
        self.dieCount = 0
        self.killCount = 0
        self.attackCount = 0
        self.vel = 2
        self.hp = hp
        self.hitbox = (self.x + 12,self.y +5,45,70)

    def draw(self,display):
        global killCount
        if self.idleCount + 1 >= 56:
            self.idleCount = 0
        if self.attackCount + 1 >= 56:
            self.attackCount -= 25

        if man.x > self.x - 200 and man.x <= self.x:
            display.blit(self.enemyAttack[self.attackCount//7], (self.x, self.y))
            self.attackCount += 1
            man.hp -= 0.05
        else: 
            display.blit(self.stayIdle[self.idleCount//8], (self.x, self.y))
            self.idleCount += 1

        self.hitbox = (self.x + 12,self.y +5,45,70)
        #pygame.draw.rect(display, (255,0,0), self.hitbox, 2)
        
        if self.hp > 90:
            enemy_health_color = green1
        elif self.hp > 80:
            enemy_health_color = green2
        elif self.hp > 70:
            enemy_health_color = green3
        elif self.hp > 60:
            enemy_health_color = limeGreen
        elif self.hp > 50:
            enemy_health_color = greenYellow
        elif self.hp > 40:
            enemy_health_color = yellow
        elif self.hp > 30:
            enemy_health_color = orange
        elif self.hp > 20:
            enemy_health_color = darkOrange
        elif self.hp > 10:
            enemy_health_color = red1
        elif self.hp > 1:
            enemy_health_color = red2
        else:
            enemy_health_color = black

        if self.hp > 0:
            enemyHealthBarWidth = self.hp * .4
        else:
            enemyHealthBarWidth = 1

        enemyHealthBarHeight = 5

        enemyHealthOutWidth = 40
        enemyHealthOutHeight = 5

        #pygame.draw.rect(display, enemy_health_color, (self.x + 17, self.y, 40, 5))

        enemyHealthBar = pygame.Surface((enemyHealthBarWidth,enemyHealthBarHeight), pygame.SRCALPHA, 32)
        enemyHealthBar.fill(enemy_health_color)
        display.blit(enemyHealthBar, (self.x + 17, self.y))

        pygame.draw.rect(display, black, (self.x + 17, self.y, enemyHealthOutWidth,enemyHealthOutHeight), 1)



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



class projectiles(object):

    bulletImg = pygame.image.load('images/enemy/bullet2.png')

    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vel = 5

    def draw(self, display):
        if self.vel > 0: 
            display.blit(bulletImg, (self.x, self.y))




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
'''
        
def backgroundMoving():
    global bg_x
    bg_rel_x = bg_x % bg.get_rect().width
    display.blit(bg, (bg_rel_x - bg.get_rect().width,0))
    if bg_rel_x < screenWidth:
        display.blit(bg, (bg_rel_x,0))

def collision():
        global killCount
        col = 80

        if man.x >= en.x - col and man.x <= en.x and event.type == pygame.MOUSEBUTTONDOWN and en.hp > 0:
            en.hp -= 3
            #print("hit", en.hp)
            impactSound.play()

        if man.x >= en1.x - col and man.x <= en1.x and event.type == pygame.MOUSEBUTTONDOWN and en1.hp > 0:
            en1.hp -= 2
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en2.x - col and man.x <= en2.x and event.type == pygame.MOUSEBUTTONDOWN and en2.hp > 0:
            en2.hp -= 1
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en3.x - col and man.x <= en3.x and event.type == pygame.MOUSEBUTTONDOWN and en3.hp > 0:
            en3.hp -= 0.7
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en4.x - col and man.x <= en4.x and event.type == pygame.MOUSEBUTTONDOWN and en4.hp > 0:
            en4.hp -= 0.7
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en5.x - col and man.x <= en5.x and event.type == pygame.MOUSEBUTTONDOWN and en5.hp > 0:
            en5.hp -= 0.7
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en6.x - col and man.x <= en6.x and event.type == pygame.MOUSEBUTTONDOWN and en6.hp > 0:
            en6.hp -= 0.7
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en7.x - col and man.x <= en7.x and event.type == pygame.MOUSEBUTTONDOWN and en7.hp > 0:
            en7.hp -= 0.7
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en8.x - col and man.x <= en8.x and event.type == pygame.MOUSEBUTTONDOWN and en8.hp > 0:
            en8.hp -= 0.7
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en9.x - col and man.x <= en9.x and event.type == pygame.MOUSEBUTTONDOWN and en9.hp > 0:
            en9.hp -= 0.7
            #print("hit", en1.hp)
            impactSound.play()

        if man.x >= en10.x - col and man.x <= en10.x and event.type == pygame.MOUSEBUTTONDOWN and en10.hp > 0:
            en10.hp -= 0.7
            #print("hit", en1.hp)
            impactSound.play()

        elif en.hp > 1:
            pass
            #print("no hit",en.hp)
        else:
            pass
            #print("dead")



        if en.hp > 0:
            en.draw(display)
        else:
            if en.dieCount + 1 <= 100:
                display.blit(en.enemyDie[en.dieCount//10], (en.x, en.y))
                en.dieCount += 1
                if en.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if en1.hp > 0:
            en1.draw(display)
        else:
            if en1.dieCount + 1 <= 100:
                display.blit(en1.enemyDie[en1.dieCount//10], (en1.x, en1.y))
                en1.dieCount += 1
                if en1.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if en2.hp > 0:
            en2.draw(display)
        else:
            if en2.dieCount + 1 <= 100:
                display.blit(en2.enemyDie[en2.dieCount//10], (en2.x, en2.y))
                en2.dieCount += 1
                if en2.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if en3.hp > 0:
            en3.draw(display)
        else:
            if en3.dieCount + 1 <= 100:
                display.blit(en3.enemyDie[en3.dieCount//10], (en3.x, en3.y))
                en3.dieCount += 1
                if en3.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10


        if en4.hp > 0:
            en4.draw(display)
        else:
            if en4.dieCount + 1 <= 100:
                display.blit(en4.enemyDie[en4.dieCount//10], (en4.x, en4.y))
                en4.dieCount += 1
                if en4.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if en5.hp > 0:
            en5.draw(display)
        else:
            if en5.dieCount + 1 <= 100:
                display.blit(en5.enemyDie[en5.dieCount//10], (en5.x, en5.y))
                en5.dieCount += 1
                if en5.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10
         
        if en6.hp > 0:
            en6.draw(display)
        else:
            if en6.dieCount + 1 <= 100:
                display.blit(en6.enemyDie[en6.dieCount//10], (en6.x, en6.y))
                en6.dieCount += 1
                if en6.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if en7.hp > 0:
            en7.draw(display)
        else:
            if en7.dieCount + 1 <= 100:
                display.blit(en7.enemyDie[en7.dieCount//10], (en7.x, en7.y))
                en7.dieCount += 1
                if en7.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if en8.hp > 0:
            en8.draw(display)
        else:
            if en8.dieCount + 1 <= 100:
                display.blit(en8.enemyDie[en8.dieCount//10], (en8.x, en8.y))
                en8.dieCount += 1
                if en8.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if en9.hp > 0:
            en9.draw(display)
        else:
            if en9.dieCount + 1 <= 100:
                display.blit(en9.enemyDie[en9.dieCount//10], (en9.x, en9.y))
                en9.dieCount += 1
                if en9.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if en10.hp > 0:
            en10.draw(display)
        else:
            if en10.dieCount + 1 <= 100:
                display.blit(en10.enemyDie[en10.dieCount//10], (en10.x, en10.y))
                en10.dieCount += 1
                if en10.dieCount == 10:
                    en.killCount += 1
                    man.hp += 10

        if man.hp > 0:
            man.draw(display)
        else:
            if man.dieCount + 1 <= 56:
                display.blit(man.die[man.dieCount//8], (man.x, man.y))
                man.dieCount += 1

def redrawGameWindow():
    backgroundMoving()
    collision()
    playerx = font.render("player x : " + str(man.x), 1, white)
    playery = font.render("player y : " + str(man.y), 1, white)
    kill = font.render("Kills : " + str(en.killCount), 1, white)
    if man.hp >= 0:
        hp = font.render("HP : " + str(int(man.hp)), 1, white)
    else:
        hp = font.render("HP : " + str(0), 1, white)
    #display.blit(playerx, (780,10))
    #display.blit(playery, (780,30))
    display.blit(hp, (80,23))
    display.blit(kill, (77,45))
    #man.draw(display)
    pygame.display.update()
    
enemyLocations = [600, 900, 1000, 1200, 1250, 1400, 1700, 1800, 1950, 2100, 2200] 

run = True
man = player(100, 440, 110, 81)

en = enemy(enemyLocations[0], 435, 110, 81, 100)
en1 = enemy(enemyLocations[1], 435, 110, 81, 100)
en2 = enemy(enemyLocations[2], 435, 110, 81, 100)
en3 = enemy(enemyLocations[3], 435, 110, 81, 100)
en4 = enemy(enemyLocations[4], 435, 110, 81, 100)
en5 = enemy(enemyLocations[5], 435, 110, 81, 100)
en6 = enemy(enemyLocations[6], 435, 110, 81, 100)
en7 = enemy(enemyLocations[7], 435, 110, 81, 100)
en8 = enemy(enemyLocations[8], 435, 110, 81, 100)
en9 = enemy(enemyLocations[9], 435, 110, 81, 100)
en10 = enemy(enemyLocations[10], 435, 110, 81, 100)

bullet = projectiles
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

    player.handleKeys(man)
    redrawGameWindow()
    
  
pygame.quit()