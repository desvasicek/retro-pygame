import pygame
from pygame.locals import *
import random
import time
from pygame import mixer
import colorama
from colorama import Fore
import psutil, os
import math
def load():
    other = False
    game_loop(other)
def game_loop(other):
    if other:
        other = False
    else:
        other = True
    health = 3
    enemies = []
    game_over = False
    points = 0.0
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.pos = [random.randint(-200, 1000), 0]
            self.size = [10, 10]
            self.rect = pygame.Rect(self.pos, self.size)
            self.no = random.randint(10000, 99999)
            self.image = "/home/pi/retro-pygame/images/PNG/Meteors/meteorGrey_big3.png"
            self.size = [89, 82]
            enemies.append(self)
        def movedown(self):
            if not game_over:
                self.pos[1] = self.pos[1] + 4
                self.rect = pygame.Rect(self.pos, self.size)
            else:
                enemies.remove(self)
        def destroy(self):
            enemies.remove(self)
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.pos = [490, 990]
            self.size = [10, 10]
            self.rect = pygame.Rect(self.pos, self.size)
            self.color = (230, 230, 230)
        def move(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.pos[0] > 10:
                self.pos[0] -= 15
            if keys[pygame.K_RIGHT] and self.pos[0] < 990 - self.size[0]:
                self.pos[0] += 15
            if keys[pygame.K_UP] and self.pos[1] > 10:
                self.pos[1] -= 4
            if keys[pygame.K_DOWN] and self.pos[1] < 990 - self.size[1]:
                self.pos[1] += 4
            self.rect = pygame.Rect(self.pos, self.size)
        def draw(self):
            self.image = pygame.transform.scale(pygame.image.load("/home/pi/retro-pygame/images/PNG/playerShip2_orange.png"), [20, 20])
            game.blit(self.image, self.rect)
        def collide(self):
            for enemy in enemies:
                if self.pos[0] >= enemy.pos[0] and self.pos[0] <= enemy.pos[0] + enemy.size[0] and self.pos[1] >= enemy.pos[1] and self.pos[1] <= enemy.pos[1] + enemy.size[1]:
                    return enemy
    Enemy()
    pygame.init()
    mixer.init()
    pygame.font.init()
    mixer.music.load("/home/pi/retro-pygame/8-bit.ogg")
    mixer.music.play(loops=-1)
    def gameover():
        font = pygame.font.SysFont('Press Start 2P', 30)
        over = font.render('Game Over', False, (255, 0, 0))
        endscore = font.render('Score: ' + str(points), False, (255, 0, 0))
        press = font.render('Press SPACE to Restart', False, (255, 255, 0))
        game.blit(over, (410, 450))
        game.blit(endscore, (410, 500))
        game.blit(press, (250, 940))
    game = pygame.display.set_mode((1000, 1000))
    pygame.display.set_caption("Retro Pygame By Desmond Vasicek")
    running = True
    x = 490
    y = 990
    height = 10
    width = 10
    player = Player()
    vel = 10
    while running:
        try:
            pygame.display.flip()
            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        try:
                            pygame.quit()
                        except:
                            pass
                        if other:
                            print(f"Player 1 Score: {points}")
                        else:
                            print(f"Player 2 score: {points}")
            game.fill((0, 0, 12))
            if player.collide():
                health -= 1
                player.collide().destroy()
                if health == 0:
                    game_over = True
            for enemy in enemies:
                game.blit(pygame.image.load(enemy.image), enemy.rect)
                enemy.movedown()
                if enemy.pos[1] == 100:
                    Enemy()
                if enemy.pos[1] >= 1000:
                    enemy.destroy()
            if game_over:
                gameover()
                player.draw()
            else:
                points += 1.5
                player.draw()
                player.move()
            if game_over:
                keys = pygame.key.get_pressed()
                if keys[pygame.K_SPACE]:
                    pygame.quit()
                    if other:
                            print(f"Player 1 Score: {points}")
                    else:
                            print(f"Player 2 score: {points}") 
                    game_loop(other)
                    break
            pygame.display.update()
        except:
            parent_pid = os.getppid()
            if psutil.Process(parent_pid).name() == "bash":
                print("\033[1;33m\033[5mGame has ended\033[0m")
            else:
                print("Game has ended")
            break
load()
