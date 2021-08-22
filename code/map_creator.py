import pygame
import sys
from settings import *

pygame.init()
screen = pygame.display.set_mode((screen_width + 300, screen_height))
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    screen.fill((255, 255, 255))
    pygame.display.update()
    clock.tick(60)
