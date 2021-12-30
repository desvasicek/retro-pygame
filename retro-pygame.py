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
    player = pygame.Rect((x, y), (width, height))
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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if width == 10:
                            width = 5
                        else:
                            width = 10
        keys = pygame.key.get_pressed()
        game.fill((0, 0, 0))
        for enemy in enemies:
            pygame.draw.rect(game, (200, 200, 200), enemy.rect)
            enemy.movedown()
            if enemy.pos[1] == 144:
                Enemy()
            if enemy.pos[1] >= 1000:
                enemies.remove(enemy)
            if x >= enemy.pos[0] and x <= enemy.pos[0] + enemy.size[0] and y == enemy.pos[1]:
                game_over = True
        if game_over:
            gameover()
            pygame.draw.rect(game, (255, 255, 255), (490, 990, 10, 10))
        else:
            points += 1.5
            if keys[pygame.K_LEFT] and x > 10:
                x -= 10
            if keys[pygame.K_RIGHT] and x < 990 - width:
                x += 10
            if keys[pygame.K_UP] and y > 10:
                y -= 3
            if keys[pygame.K_DOWN] and y < 990 - height:
                y += 3
            pygame.draw.rect(game, (255, 255, 255), (x, y, width, height))
        if game_over:
            if keys[pygame.K_SPACE]:
                pygame.quit()
                game_loop()
        pygame.display.update()
game_loop()