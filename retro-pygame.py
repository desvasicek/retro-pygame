import pygame
from pygame.locals import *
import random
enemies = []
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.pos = [random.randint(1, 1000), 4]
        self.size = [random.randint(20, 900), 10]
        self.rect = pygame.Rect(self.pos, self.size)
        enemies.append(self)
    def movedown(self):
        self.pos[1] = self.pos[1] + 3
        self.rect = pygame.Rect(self.pos, self.size)
Enemy()
pygame.init()
game = pygame.display.set_mode((1000, 1000))
pygame.display.set_caption("The Life of the Rect")
running = True
x = 490
y = 990
height = 10
width = 10
player = pygame.Rect((x, y), (10, 10))
vel = 10
while running:
    pygame.display.flip()
    for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and x>0:
        x -= vel
    if keys[pygame.K_RIGHT] and x<1000-width:
        x += vel
    if keys[pygame.K_UP] and y>0:
        y -= vel
    if keys[pygame.K_DOWN] and y<1000-height:
        y += vel
    game.fill((0, 0, 0))
    pygame.draw.rect(game, (255, 255, 255), (x, y, 10, 10))
    for enemy in enemies:
        pygame.draw.rect(game, (200, 200, 200), enemy.rect)
        enemy.movedown()
        if enemy.pos[1] == 100:
            Enemy()
        if enemy.pos[1] == 1000:
            enemies.remove(enemy)
    pygame.display.update()