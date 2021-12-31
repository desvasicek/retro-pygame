import pygame
from pygame.locals import *
import random
import time
from pygame import mixer
def game_loop():
    enemies = []
    game_over = False
    points = 0.0
    class Enemy(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.pos = [random.randint(-200, 1000), 0]
            self.size = [random.randint(20, 900), 10]
            self.rect = pygame.Rect(self.pos, self.size)
            enemies.append(self)
        def movedown(self):
            if not game_over:
                self.pos[1] = self.pos[1] + 3
                self.rect = pygame.Rect(self.pos, self.size)
            else:
                enemies.remove(self)
    class Player(pygame.sprite.Sprite):
        def __init__(self, name):
            super().__init__()
            self.pos = [490, 990]
            self.size = [10, 10]
            self.rect = pygame.Rect(self.pos, self.size)
        def move(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_LEFT] and self.pos[0] > 10:
                self.pos[0] -= 10
            if keys[pygame.K_RIGHT] and self.pos[0] < 990 - self.size[0]:
                self.pos[0] += 10
            if keys[pygame.K_UP] and self.pos[1] > 10:
                self.pos[1] -= 3
            if keys[pygame.K_DOWN] and self.pos[1] < 990 - self.size[1]:
                self.pos[1] += 3
            self.rect = pygame.Rect(self.pos, self.size)
        def draw(self):
            pygame.draw.rect(game, (255, 255, 255), self.rect)
        def collide(self):
            for enemy in enemies:
                if self.pos[0] >= enemy.pos[0] and self.pos[0] <= enemy.pos[0] + enemy.size[0] and self.pos[1] >= enemy.pos[1] and self.pos[1] <= enemy.pos[1] + enemy.size[1]:
                    game_over = True
    Enemy()
    pygame.init()
    mixer.init()
    pygame.font.init()
    mixer.music.load("/home/pi/retro-pygame/8-bit.ogg")
    mixer.music.play(loops=-1)
    def gameover():
        font = pygame.font.SysFont('Press Start 2P', 60)
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
    player = Player('Player 1')
    vel = 10
    while running:
        pygame.display.flip()
        for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    try:
                        pygame.quit()
                    except:
                        pass
                    print(f"Score: {points}")
        game.fill((0, 0, 12))
        player.collide()
        for enemy in enemies:
            pygame.draw.rect(game, (200, 200, 200), enemy.rect)
            enemy.movedown()
            if enemy.pos[1] == 144:
                Enemy()
            if enemy.pos[1] >= 1000:
                enemies.remove(enemy)
            if player.pos[0] >= enemy.pos[0] and player.pos[0] <= enemy.pos[0] + enemy.size[0] and player.pos[1] >= enemy.pos[1] and player.pos[1] <= enemy.pos[1] + enemy.size[1]:
                game_over = True
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
                game_loop()
        pygame.display.update()
game_loop()