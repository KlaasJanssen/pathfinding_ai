import pygame
import sys
from settings import *
from map import Map

pygame.init()
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

map = Map()
next = True
initiated = False
prop_continue = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    map.draw_board()
    if not initiated:
        map.initiate_board()
        initiated = True
    if next:
        next = map.reveal_next_tile()
    if not next and prop_continue:
        prop_continue = map.back_propagation()
    pygame.display.update()
    #clock.tick(100)
