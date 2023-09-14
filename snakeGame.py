#########################################
# Programmer: Ben Sadeh
# Date: 21/04/2020
# File Name: snakeGame.py
# Description: Snake Game
#########################################

import pygame
pygame.init()

from random import randint, randrange
from math import sqrt

#---------------------------------------#
# intro variables                       #
#---------------------------------------#
HEIGHT = 600
WIDTH  = 800
screen=pygame.display.set_mode((WIDTH,HEIGHT))

backgroundPic=pygame.image.load("Images/snakeBackground.png")
backgroundPic=pygame.transform.scale(backgroundPic,(WIDTH,HEIGHT))
bakgroundPic=backgroundPic.convert_alpha()

intBackgroundPic=pygame.image.load("Images/snakeGameIntro.png")
intBackgroundPic=pygame.transform.scale(intBackgroundPic,(WIDTH,HEIGHT))
intBakgroundPic=backgroundPic.convert_alpha()

gameOverPic=pygame.image.load("Images/gameOver.png")
gameOverPic=pygame.transform.scale(gameOverPic,(400,200))
gameOverPic=gameOverPic.convert_alpha()

apple=pygame.image.load("Images/apple.png")
apple=pygame.transform.scale(apple,(20,20))
apple=apple.convert_alpha()

#Colours
WHITE = (255,255,255)
BLACK = (0,0,0)
RED =(255,0,0)
GREEN =(0,255,0)
YELLOW = (255,255,0)
ORANGE = (255, 102, 0)
BLUE = (0,0,255)
BROWN = (26, 9, 0)
outline=0

#Time variables
timeDelay=90
counter=0
elapsed=0

#Text variables
font = pygame.font.SysFont("Ariel Black",60)
textX,textY=0,0
textX1,textY1=WIDTH/2,0

#Star power variables
starPower=False
resetTimeStar = pygame.time.get_ticks()//1000

#Intro screen buttons
rectX, rectY, rectW, rectH = WIDTH//2-100, 460, 200, 50
rectX1, rectY1, rectW1, rectH1 = WIDTH//2-100, 520, 200, 50

#---------------------------------------#
# snake's properties                    #
#---------------------------------------#
BODY_SIZE = 10
HSPEED = 20
VSPEED = 20

speedX = 0
speedY = -VSPEED
segx = [WIDTH//2]*3
segy = [500, 500+VSPEED, 500+2*VSPEED]


#---------------------------------------#
# feature properties                    #
#---------------------------------------#
#Apple properties
appleX=randrange(20,WIDTH-20,20)
appleY=randrange(20,HEIGHT-20,20)

#Rotten apple properties
rAppleX=randrange(20,WIDTH-20,20)
rAppleY=randrange(20,HEIGHT-20,20)

#Star power properties
starPowerX=randrange(20,WIDTH-20,20)
starPowerY=randrange(20,HEIGHT-20,20)
mbyStarPwr=randint(1,5)

#---------------------------------------#
# functions                             #
#---------------------------------------#
def redraw():
    screen.blit(backgroundPic,(0,0))
    screen.blit(apple,(appleX,appleY))
    pygame.draw.circle(screen, YELLOW, (rAppleX, rAppleY), BODY_SIZE, outline)      #Draws rotten apples
    if mbyStarPwr==5:
        ranCLR=0,0,randint(150,255)
        pygame.draw.circle(screen, ranCLR, (starPowerX, starPowerY), BODY_SIZE, outline)    #Draws the star power blue circles
    if starPower:
        for i in range(len(segx)):
            pygame.draw.circle(screen, BLUE, (segx[i], segy[i]), BODY_SIZE, outline)    #Draws the snake with star feature
    else: 
        pygame.draw.circle(screen, GREEN, (segx[0], segy[0]), BODY_SIZE, outline)       #Draws the snake's head
        for i in range(1,len(segx)-1):
            pygame.draw.circle(screen, BLACK, (segx[i], segy[i]), BODY_SIZE, outline)       #Draws the snake's body
        pygame.draw.circle(screen, RED, (segx[-1], segy[-1]), BODY_SIZE, outline)       #Draws the snake's tail
    text = font.render("Counter: "+str(counter), 1, BLACK)      #Draws counter
    screen.blit(text,(textX, textY))
    text = font.render("Timer: "+str(20-elapsed), 1, BLACK)     #Draws timer
    screen.blit(text,(textX1, textY1))
    pygame.display.update()

def distance(x1, y1, x2, y2):
    return sqrt((x1-x2)**2 + (y1-y2)**2)        #Calculates distance between 2 points

def endGameScreen():        #Draws the end game screen
    screen.fill(BLACK)
    screen.blit(gameOverPic,(200,200))           
    pygame.display.update()

def startGameScreen():      #Draws the start game screen
    screen.blit(intBackgroundPic,(0,0))
    pygame.draw.rect(screen, GREEN, (rectX, rectY, rectW, rectH), 0)
    pygame.draw.rect(screen, GREEN, (rectX1, rectY1, rectW1, rectH1), 0)
    startTxt1=font.render('GUIDE',1,WHITE)
    startTxt2=font.render('START',1,WHITE)
    screen.blit(startTxt1,(WIDTH//2-70,465))
    screen.blit(startTxt2,(WIDTH//2-70,530))
    pygame.display.update()

def instructionsScreen():       #Draws the instructions screen
    screen.blit(backgroundPic,(0,0))
    instructionTxt=font.render('Press mouse to go back',1,WHITE)
    instructionTxt1=font.render('Use the arrow keys to move',0.5,WHITE)
    instructionTxt2=font.render('Apples:',0.5, WHITE)
    instructionTxt2a=font.render('Eat them to make the snake grow',0.5, WHITE)
    instructionTxt3=font.render('Yellow Balls = Rotten Apples,',0.5,WHITE)
    instructionTxt3a=font.render('They shrink the size of the snake',0.5,WHITE)
    instructionTxt4=font.render('Flashing Blue Balls = Star Bonus,',0.5,WHITE)
    instructionTxt4a=font.render('Snake is inivncible for 20 seconds',0.5,WHITE)
    screen.blit(instructionTxt,(20,20))
    screen.blit(instructionTxt1,(20,120))
    screen.blit(instructionTxt2,(20,220))
    screen.blit(instructionTxt2a,(20,255))
    screen.blit(instructionTxt3,(20,355))
    screen.blit(instructionTxt3a,(20,390))
    screen.blit(instructionTxt4,(20,490))
    screen.blit(instructionTxt4a,(20,525))
    pygame.display.update()

#---------------------------------------#
# main program                          #
#---------------------------------------#
#intro screen
introScreen = True
showRules=False
while introScreen:
    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            (mouseX,mouseY) = pygame.mouse.get_pos()
            if mouseX > rectX and mouseX < rectX+rectW and mouseY > rectY and mouseY < rectY+rectH:
                showRules=True
                while showRules:
                    for event in pygame.event.get():
                        if event.type == pygame.MOUSEBUTTONDOWN:
                            showRules = False
                    instructionsScreen()
            (mouseX,mouseY) = pygame.mouse.get_pos()
            if mouseX > rectX1 and mouseX < rectX1+rectW1 and mouseY > rectY1 and mouseY < rectY1+rectH1:
                introScreen = False
            starttime=pygame.time.get_ticks()//1000
    startGameScreen()
inPlay = True
while inPlay:

# check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            inPlay = False
    keys = pygame.key.get_pressed()

# act upon key events
    if keys[pygame.K_LEFT] and speedX==0:
        speedX = -HSPEED
        speedY = 0
        
    if keys[pygame.K_RIGHT] and speedX==0:
        speedX = HSPEED
        speedY = 0
        
    if keys[pygame.K_UP] and speedY==0:
        speedX = 0
        speedY = -VSPEED
        
    if keys[pygame.K_DOWN] and speedY==0:
        speedX = 0
        speedY = VSPEED
        
    for i in range(2,len(segy)):
        if segx[0]==segx[i] and segy[0]==segy[i] and not starPower:
            inPlay=False
            gameOver=True

# move all segments
    for i in range(len(segx)-1,0,-1):
        segx[i]=segx[i-1]
        segy[i]=segy[i-1]

# move the head
    segx[0] = segx[0] + speedX
    segy[0] = segy[0] + speedY

# star power feature
    if starPower:
        if segx[0]<0:
            segx[0]=WIDTH
        if segx[0]>WIDTH:
            segx[0]=0
        if segy[0]<0:
            segy[0]=HEIGHT
        if segy[0]>HEIGHT:
            segy[0]=0
    else:
        if segx[0]<0 or segx[0]>WIDTH or segy[0]<0 or segy[0]>HEIGHT:
            inPlay=False
            gameOver=True
    continuousTimeStar=pygame.time.get_ticks()//1000
    if distance(segx[0],segy[0],starPowerX,starPowerY)<10:
        mbyStarPwr=randint(1,5)
        starPowerX=randrange(20,WIDTH-20,20)
        starPowerY=randrange(20,HEIGHT-20,20)
        starPower=True
        resetTimeStar = pygame.time.get_ticks()//1000
    elapsedStar = resetTimeStar-continuousTimeStar
    if elapsedStar<=-20:
        starPower=False

# apple feature
    continuousTime=pygame.time.get_ticks()//1000

    if distance(segx[0],segy[0],appleX+10,appleY+10)<20:
        segx.append(segx[-1])
        segy.append(segy[-1])
        appleX=randrange(20,WIDTH-20,20)
        appleY=randrange(20,HEIGHT-20,20)
        counter+=1
        starttime = pygame.time.get_ticks()//1000
        mbyStarPwr=randint(1,5)
    elapsed = continuousTime - starttime

# rotten apple feature
    if distance(segx[0],segy[0],rAppleX,rAppleY)<10 and not starPower:
        segx.remove(segx[-1])
        segy.remove(segy[-1])
        rAppleX=randrange(20,WIDTH-20,20)
        rAppleY=randrange(20,HEIGHT-20,20)
        mbyStarPwr=randint(1,5)


# counter
    if counter==5:
        timeDelay=80
    if counter==10:
        timeDelay=70
    if counter==15:
        timeDelay=60

# end the game
    if elapsed>=20 or len(segx)<=2:
        inPlay=False
        gameOver=True

# update the screen     
    redraw()
    pygame.time.delay(timeDelay)

# game over screen
while gameOver:
    for event in pygame.event.get():    
        if event.type == pygame.QUIT:       
            gameOver = False

    endGameScreen()
    pygame.time.delay(60)
    
pygame.quit()
