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
    name1 = input("Enter player 1 name: ")
    name2 = input("Enter player 2 name: ")
    other = False
    game_loop(name1, name2, other)
def game_loop(name1, name2, other):
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
            self.size = [random.randint(20, 900), 10]
            self.rect = pygame.Rect(self.pos, self.size)
            self.no = random.randint(10000, 99999)
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
        def __init__(self, name):
            super().__init__()
            self.pos = [490, 990]
            self.size = [10, 10]
            self.rect = pygame.Rect(self.pos, self.size)
            self.name = name
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
            pygame.draw.rect(game, (255, 255, 255), self.rect)
            font = pygame.font.SysFont('Press Start 2P', 10)
            self.namedisplay = font.render(self.name, False, self.color)
            game.blit(self.namedisplay, (self.pos[0] - (math.ceil(len(self.name))) - 15, self.pos[1] - 15))
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
    if other:
        player = Player(name1)
    else:
        player = Player(name2)
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
                pygame.draw.rect(game, (200, 200, 200), enemy.rect)
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
                    game_loop(name1, name2, other)
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
