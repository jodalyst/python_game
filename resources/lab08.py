import pygame, sys
from pygame.locals import *

import random
import time

last_shoot = time.time()
SHOOT_TIMEOUT = 0.25

just_hit = time.time()
HIT_TIMEOUT = 1.5


pygame.init()


##GLOBAL VARIABLES!!!
##THINGS LIKE CONSTANTS WE WILL USE ALL CAPS VARIABLE NAMES FOR
FPS = 30 # frames per second setting
SCREENWIDTH = 400
SCREENHEIGHT = 300

FOODSIZE = 5 #dimensions of food (pixels)
ENEMYSIZE = 10 #dimensions of enemy (squares so x by x)
MISSILEWIDTH=3 #missile width
MISSILEHEIGHT=8 #missile height


TYPESOFENEMIES = 5

CHARWIDTH = 10 #your width
CHARHEIGHT = 15 #your height

MISSILERATE = 3 #movement rate of missiles

fpsClock = pygame.time.Clock()

FALL_RATE = 3 #fall rate of objects/food (how many pixels per clock tick)

BASICFONT = pygame.font.Font('freesansbold.ttf', 18)
TITLEFONT = pygame.font.Font('freesansbold.ttf', 18)
INSFONT = pygame.font.Font('freesansbold.ttf', 12)

# set up the window
DISPLAYSURF = pygame.display.set_mode((400, 300), 0, 32)
pygame.display.set_caption('')


#make some colors with easy to understand names for use throughout game:
WHITE = (255,255,255)
GREY = (200, 200, 200)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,100)
LIGHTBLUE = (0,0,255)
PURPLE = (255,0,255)
ORANGE = (255,165,0)
PINK = (255,192,203)
YELLOW = (255,255,0)
BLACK = (0,0,0)


#max foods on screen at any point in time
FOOD_CAP = 15
ENEMY_CAP = 150

foods = [] #list to contain food instances
enemies = [] #list to contain enemy instances
missiles = [] #list to contain missile instances


###important variables for player/character run time
#starting character position:
char_posx = SCREENWIDTH/2
char_posy = SCREENHEIGHT-30
#how many missiles you've got left:
#score:
missile_stock = 10
score = 0
#lives:
lives =3

instructions = '''You are a dark grey rectangle.
The world is full of colored square which will hurt you.
You must avoid these squares or destroy them with missiles.
Fire missiles with the spacebar.
The small red things are food. Eat the food.'''


def main():
    global CLOCK, SURFACE
    pygame.init()
    CLOCK = pygame.time.Clock()
    SURFACE = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
    pygame.display.set_caption('Edutainment')
    startScreen()
    while True:
        instructionsScreen()
        gameRun()
        endScreen()



def gameRun():
    global char_posx
    global char_posy
    global missile_stock
    global foods
    global enemies
    global missiles
    global lives
    global score
    global last_shoot
    score = 0 #start score at zero
    lives = 3 #start lives at 3
    missile_stock =10 #start missile stock at 10
    move_command = 0 #initial move command
    char_posx = SCREENWIDTH/2 #starting character x pos
    char_posy = SCREENHEIGHT-30 #starting character y pos
    foods = []
    enemies = []
    missiles = []

    while True: #main game loop...get out of it by calling "break"
        move_command = 0
        shoot_command = False
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            elif event.type == KEYDOWN:
                if event.key == K_SPACE:
                    shoot_command = True
                if event.key == K_ESCAPE:
                    terminate()
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT] or pressed[pygame.K_a]:
            move_command-=1
        if pressed[pygame.K_RIGHT] or pressed[pygame.K_d]:
            move_command+=1
        if shoot_command:
            if missile_stock>0:
                missiles.append([char_posx + 0.5*CHARWIDTH-0.5*MISSILEWIDTH,char_posy])
                missile_stock-=1
        char_posx +=move_command*3
        char_posx = min(max(char_posx,20),SCREENWIDTH-20)
        updateFoods()
        updateEnemiesAndMissiles()
        if lives<=0:
            break
        DISPLAYSURF.fill(LIGHTBLUE)
        drawCharacter([char_posx,char_posy])
        for food in foods:
            drawFood(food)
        for enemy in enemies:
            drawEnemy(enemy)
        for missile in missiles:
            drawMissile(missile)
        drawScore()
        pygame.display.update()
        fpsClock.tick(FPS)

#start screen graphics
def startScreen():
    DISPLAYSURF.fill(LIGHTBLUE)
    TitleSurf = TITLEFONT.render('Video Game', True, WHITE)
    SubTitleSurf = TITLEFONT.render('Fun Times' , True, WHITE)
    InstructionSurf = TITLEFONT.render('PRESS ANY KEY TO START', True, WHITE)
    TitleRect = TitleSurf.get_rect()
    SubTitleRect = SubTitleSurf.get_rect()
    InstructionRect = InstructionSurf.get_rect()
    TitleRect.topleft = (SCREENWIDTH/2-80, 40)
    SubTitleRect.topleft = (SCREENWIDTH/2-30 , 80)
    InstructionRect.topleft = (SCREENWIDTH/2-80 , 120)
    DISPLAYSURF.blit(TitleSurf, TitleRect)
    DISPLAYSURF.blit(SubTitleSurf, SubTitleRect)
    DISPLAYSURF.blit(InstructionSurf, InstructionRect)
    pygame.display.update()
    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

#instruction screen graphics:
def instructionsScreen():
    DISPLAYSURF.fill(LIGHTBLUE)
    TitleSurf = TITLEFONT.render('Video Game', True, WHITE)
    TitleRect = TitleSurf.get_rect()
    TitleRect.topleft = (SCREENWIDTH/2-80, 40)
    DISPLAYSURF.blit(TitleSurf, TitleRect)
    spot = 80
    b = instructions.split('\n')
    for q in b:
        SubTitleSurf = INSFONT.render(q , True, WHITE)
        SubTitleRect = SubTitleSurf.get_rect()
        SubTitleRect.topleft = (SCREENWIDTH/2-80 , spot)
        spot+=20
        DISPLAYSURF.blit(SubTitleSurf, SubTitleRect)
    InstructionSurf = TITLEFONT.render('PRESS ANY KEY TO START', True, WHITE)
    InstructionRect = InstructionSurf.get_rect()
    InstructionRect.topleft = (SCREENWIDTH/2-80 , spot)
    DISPLAYSURF.blit(InstructionSurf, InstructionRect)
    pygame.display.update()
    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

#end Screen Graphics
def endScreen():
    DISPLAYSURF.fill(BLACK)
    TitleSurf = TITLEFONT.render('GAME OVER :(', True, WHITE)
    SubTitleSurf = TITLEFONT.render('SCORE: %s' %(score), True, WHITE)
    TitleRect = TitleSurf.get_rect()
    SubTitleRect = SubTitleSurf.get_rect()
    TitleRect.topleft = (SCREENWIDTH/2-30, 40)
    SubTitleRect.topleft = (SCREENWIDTH/2-30 , 80)
    DISPLAYSURF.blit(TitleSurf, TitleRect)
    DISPLAYSURF.blit(SubTitleSurf, SubTitleRect)
    pygame.display.update()
    time.sleep(3)
    pygame.event.get() #empty queue
    DISPLAYSURF.fill(BLACK)
    TitleSurf = TITLEFONT.render('GAME OVER :(', True, WHITE)
    SubTitleSurf = TITLEFONT.render('SCORE: %s' %(score), True, WHITE)
    InstructionSurf = TITLEFONT.render('PRESS ANY KEY TO RESTART', True, WHITE)
    TitleRect = TitleSurf.get_rect()
    SubTitleRect = SubTitleSurf.get_rect()
    InstructionRect = InstructionSurf.get_rect()
    TitleRect.topleft = (SCREENWIDTH/2-30, 40)
    SubTitleRect.topleft = (SCREENWIDTH/2-30 , 80)
    InstructionRect.topleft = (SCREENWIDTH/2-80 , 120)
    DISPLAYSURF.blit(TitleSurf, TitleRect)
    DISPLAYSURF.blit(SubTitleSurf, SubTitleRect)
    DISPLAYSURF.blit(InstructionSurf, InstructionRect)
    pygame.display.update()
    while True:
        if checkForKeyPress():
            pygame.event.get() # clear event queue
            return

def terminate():
    pygame.quit()
    sys.exit()

def randXSpot():
    return random.randint(0, SCREENWIDTH - 1)

def rand(prob):
    return random.random()<prob

def randtype():
    return random.randint(0,TYPESOFENEMIES-1)

def collision(coord1,w1,h1,coord2,w2,h2):
    cond1 = coord1[0]<coord2[0]+w2
    cond2 = coord1[0] + w1 > coord2[0]
    cond3 = coord1[1] <coord2[1]+h2
    cond4 = coord1[1]+h1 > coord2[1]
    if cond1 and cond2 and cond3 and cond4:
        return True
    else:
        return False

def updateFoods():
    global foods
    global score
    new_foods=[]
    global missile_stock
    for food in foods:
        candidate = [food[0],food[1]+FALL_RATE]
        if collision(candidate,FOODSIZE,FOODSIZE,[char_posx,char_posy],CHARWIDTH,CHARHEIGHT):
            missile_stock+=1
            score +=1
        elif candidate[1]<SCREENHEIGHT:
            new_foods.append(candidate)
    if len(new_foods)< FOOD_CAP and rand(0.05):
        new_foods.append([randXSpot(),0])
    foods = new_foods

def AI(charx,enemyx,type):
    return enemyx #doesn't move

def enemy_release(score):
    return 0.05
    

def updateEnemiesAndMissiles():
    global enemies
    global missiles
    global missile_stock
    global lives
    global score
    global just_hit
    new_enemies=[]
    new_missiles=[]
    for missile in missiles:
        candidate = [missile[0],missile[1]-MISSILERATE]
        if candidate[1] >0:
            new_missiles.append(candidate)
    for enemy in enemies:
        newx = AI(char_posx,enemy[0],enemy[2])
        candidate = [newx,enemy[1]+FALL_RATE,enemy[2]]
        hit = False
        for m in range(len(new_missiles)):
            if collision(candidate[:2],ENEMYSIZE,ENEMYSIZE,new_missiles[m],MISSILEWIDTH,MISSILEHEIGHT):
                new_missiles.pop(m)
                hit=True
                score +=1
                print("HITHIT")
                break #enemy hit and blown up!
        if hit:
            pass
        elif collision(candidate[:2],ENEMYSIZE,ENEMYSIZE,[char_posx,char_posy],CHARWIDTH,CHARHEIGHT):
            lives-=1
            just_hit = time.time()
        elif candidate[1]<SCREENHEIGHT:
            new_enemies.append(candidate)
    if len(new_enemies)< ENEMY_CAP and rand(enemy_release(score)):
        new_enemies.append([randXSpot(),0,randtype()])
    missiles = new_missiles
    enemies = new_enemies


def drawCharacter(coordinates):
    charRect = pygame.Rect(coordinates[0],coordinates[1],CHARWIDTH,CHARHEIGHT)
    if time.time()-just_hit >HIT_TIMEOUT:
        pygame.draw.rect(DISPLAYSURF,BLUE,charRect)
    else:
        pygame.draw.rect(DISPLAYSURF,RED,charRect)

def drawFood(coordinates):
    appleRect = pygame.Rect(coordinates[0], coordinates[1], FOODSIZE, FOODSIZE)
    pygame.draw.rect(DISPLAYSURF, RED, appleRect)
    
def drawEnemy(coordinates):
    enemyRect = pygame.Rect(coordinates[0],coordinates[1], ENEMYSIZE, ENEMYSIZE)
    if coordinates[2]==0:
        pygame.draw.rect(DISPLAYSURF,GREEN,enemyRect)
    elif coordinates[2]==1:
        pygame.draw.rect(DISPLAYSURF,YELLOW,enemyRect)
    elif coordinates[2]==2:
        pygame.draw.rect(DISPLAYSURF,PURPLE,enemyRect)
    elif coordinates[2]==3:
        pygame.draw.rect(DISPLAYSURF,PINK,enemyRect)
    elif coordinates[2]==4:
        pygame.draw.rect(DISPLAYSURF,ORANGE,enemyRect)

def drawMissile(coordinates):
    missile = pygame.Rect(coordinates[0],coordinates[1], MISSILEWIDTH,MISSILEHEIGHT)
    pygame.draw.rect(DISPLAYSURF, GREY,missile)

def checkForKeyPress():
    if len(pygame.event.get(QUIT)) > 0:
        terminate()
    keyUpEvents = pygame.event.get(KEYUP)
    if len(keyUpEvents) == 0:
        return None
    if keyUpEvents[0].key == K_ESCAPE:
        terminate()
    return keyUpEvents[0].key

def drawScore():
    scoreSurf = BASICFONT.render('Score: %s' % (score), True, WHITE)
    missilesSurf = BASICFONT.render('Missiles: %s' % (missile_stock), True, WHITE)
    livesSurf = BASICFONT.render('Lives: %s' % (lives), True, WHITE)
    scoreRect = scoreSurf.get_rect()
    missilesRect = missilesSurf.get_rect()
    livesRect = livesSurf.get_rect()
    scoreRect.topleft = (SCREENWIDTH - 120, 10)
    missilesRect.topleft = (SCREENWIDTH - 120, 25)
    livesRect.topleft = (SCREENWIDTH - 120, 40)
    DISPLAYSURF.blit(scoreSurf, scoreRect)
    DISPLAYSURF.blit(livesSurf, livesRect)
    DISPLAYSURF.blit(missilesSurf, missilesRect)

#code below runs the main function when you just call python3 lab08.py in terminal
if __name__ == '__main__':
    main()
