import pygame
from settings import *

class Tile:
    def __init__(self, x, y, state):
        self.screen = pygame.display.get_surface()
        self.x = x
        self.y = y
        self.state = state
        self.surf = pygame.Surface((block_size, block_size))
        self.rect = self.surf.get_rect(topleft = (self.x * block_size, self.y * block_size))
        self.g_cost = 99999
        if self.state == 'start':
            self.g_cost = 0

    def draw(self):
        self.screen.blit(self.surf, self.rect)

    def open_tile(self, y, x, tile, end):
        # G cost
        if abs(x) == abs(y):
            g_cost = tile.g_cost + 14
        else:
            g_cost = tile.g_cost + 10
        if g_cost < self.g_cost:
            self.g_cost = g_cost

        if self.state == "open":
            temp = []
            temp.append(abs(self.y - end[1]))
            temp.append(abs(self.x - end[0]))
            self.h_cost = min(temp) * 14 + (max(temp) - min(temp)) * 10
            self.state = 'revealed'
            self.surf.fill((150,150,255))
        elif self.state == "end":
            self.h_cost = 0

        self.f_cost = self.g_cost + self.h_cost
