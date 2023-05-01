import pygame
import random
import math
from pygame import mixer

pygame.init()

screen = pygame.display.set_mode((800, 600))
icon = pygame.image.load('icon.png')
bg = pygame.image.load('space.jpg')

playerimage = pygame.image.load('rocket.png')
bul = pygame.image.load('bullet.png')

pygame.display.set_icon(icon)
title = pygame.display.set_caption("Game")

mixer.music.load('background.wav')
mixer.music.play(-1)

playerx = 370
playery = 480
playerxchange = 0

alienimage = []
alienx = []
alieny = []
alienxchange = []
alienychange = []
no_of_alien = 4

for i in range(no_of_alien):
    alienimage.append(pygame.image.load('alien.png'))
    alienx.append(random.randint(0, 736))
    alieny.append(random.randint(50, 150))
    alienxchange.append(1.5)
    alienychange.append(40)

bulletx = 0
bullety = 480
bulletychange = 5
bulletstate = 'ready'


def player(x, y):
    screen.blit(playerimage, (x, y))


def alien(x, y, i):
    screen.blit(alienimage[i], (x, y))


def bullet(x, y):
    global bulletstate
    bulletstate = 'fire'
    screen.blit(bul, (x + 16, y + 10))


def iscollission(x1, x2, y1, y2):
    DIS = math.sqrt((math.pow(x1 - x2, 2)) + (math.pow(y1 - y2, 2)))
    if DIS < 27:
        return True
    else:
        return False


go = pygame.font.Font('freesansbold.ttf', 64)


def gameover(x, y):
    gao = go.render('LOOSER..', True, (255, 255, 255))
    screen.blit(gao, (x, y))


score = 0
fnt = pygame.font.Font('freesansbold.ttf', 30)
tx = 10
ty = 10


def show_score(x, y):
    scr = fnt.render('SCORE: ' + str(score), True, (255, 255, 255))
    screen.blit(scr, (x, y))


rn = True
while rn:

    screen.fill((0, 0, 0))
    screen.blit(bg, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rn = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerxchange = - 1.5
            if event.key == pygame.K_RIGHT:
                playerxchange = 1.5
            if event.key == pygame.K_SPACE:
                bulletx = playerx
                bullet(bulletx, bullety)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerxchange = 0

    playerx += playerxchange
    if playerx <= 0:
        playerx = 0
    elif playerx >= 736:
        playerx = 736

    for i in range(no_of_alien):
        if alieny[i] > 400:
            for j in range(no_of_alien):
                alieny[j] = 2000
            gameover(250, 250)
            break
        alienx[i] += alienxchange[i]
        if alienx[i] <= 0:
            alienxchange[i] = +1.5
            alieny[i] += alienychange[i]
        elif alienx[i] >= 736:
            alienxchange[i] = -1.5
            alieny[i] += alienychange[i]

        collission = iscollission(alienx[i], bulletx, alieny[i], bullety)
        if collission:
            csound = mixer.Sound('explosion.wav')
            csound.play()
            bullety = 480
            bulletstate = 'ready'
            score += 1
            print(score)
            alienx[i] = random.randint(0, 736)
            alieny[i] = random.randint(50, 150)
        alien(alienx[i], alieny[i], i)
    # for bullet
    if bullety <= 0:
        bullety = 480
        bulletstate = 'ready'

    if bulletstate is 'fire':
        bsound = mixer.Sound('laser.wav')
        bsound.play()
        bullet(bulletx, bullety)
        bullety -= bulletychange
    show_score(tx, ty)
    player(playerx, playery)
    pygame.display.update()
