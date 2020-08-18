import math

import pygame
import random
from pygame import mixer

pygame.init()
# 9867158504
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
# icon = pygame.image.load("ufo.png")
# pygame.display.set_icon(icon)

playerImg = pygame.image.load("spaceship.png")
playerX = 370
playerY = 480
playerXChange = 0

enemyImg = []
enemyX = []
enemyY = []
enemyXChange = []
enemyYChange = []
num_of_enemies = 4

for i in range(num_of_enemies + 1):
    enemyImg.append(pygame.image.load("enemy.png"))
    enemyX.append(random.randint(0, 735))
    enemyY.append(random.randint(45, 150))
    enemyXChange.append(0.3)
    enemyYChange.append(38)

bulletImg = pygame.image.load("bullet.png")
bulletX = 0
bulletY = 480
bulletYChange = 1
bullet_state = "Ready"

score_val = 0
font = pygame.font.Font("freesansbold.ttf", 32)

scoreX = 10
scoreY = 10

gameover_font = pygame.font.Font("freesansbold.ttf", 64)


def get_game_over():

    gameovertext = font.render("GAME OVER", True, (255, 255, 255))
    screen.blit(gameovertext, (320, 300))


def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (255, 255, 255))
    screen.blit(score, (x, y))


def shoot_bullet(x, y):
    global bullet_state
    bullet_state = "Shoot"
    screen.blit(bulletImg, (x + 16, y + 10))


def player(x, y):
    screen.blit(playerImg, (x, y))


def enemy(x, y, i):
    screen.blit(enemyImg[i], (x, y))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 27:
        return True
    return False


running = True
while running:
    screen.fill((90, 20, 150))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                print("Left Arrow key pressed")
                playerXChange = -0.5
            if event.key == pygame.K_RIGHT:
                print("Right arrow key pressed")
                playerXChange = 0.5
            if event.key == pygame.K_SPACE:
                if bullet_state is "Ready":
                    bullet_sound = mixer.Sound("laser.wav")
                    bullet_sound.play()
                    bulletX = playerX
                    shoot_bullet(bulletX, playerY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                print("Keystroke released")
                playerXChange = 0
    playerX += playerXChange
    if playerX < 0:
        playerX = 0
    if playerX > 736:
        playerX = 736
    for i in range(num_of_enemies):
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            get_game_over()
            break

        enemyX[i] += enemyXChange[i]
        if enemyX[i] < 0:
            enemyXChange[i] = 0.2
            enemyY[i] += enemyYChange[i]
        elif enemyX[i] > 736:
            enemyXChange[i] = -0.2
            enemyY[i] += enemyYChange[i]

        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            collision_sound = mixer.Sound("explosion.wav")
            collision_sound.play()
            bulletY = 480
            bullet_state = "Ready"
            score_val += 1


            # print(score_val)
            enemyX[i] = random.randint(0, 735)
            enemyY[i] = random.randint(45, 150)
        enemy(enemyX[i], enemyY[i], i)

    if bulletY < 0:
        bulletY = 480
        bullet_state = "Ready"
    if bullet_state is "Shoot":
        shoot_bullet(bulletX, bulletY)
        bulletY -= bulletYChange

    player(playerX, playerY)
    show_score(scoreX, scoreY)

    pygame.display.update()
