import pygame
from settings import *
from random import random
from tile import Tile

class Map:
    def __init__(self, path = None):
        self.block_size = block_size
        self.x_size = x_size
        self.y_size = y_size
        self.path = path
        self.end_reached = False
        self.revealed_tiles = []

        if self.path == None:
            self.tiles = []
            for i in range(y_size):
                temp = []
                for j in range(x_size):
                    if i == 0 or j == 0 or i == y_size - 1 or j == x_size - 1:
                        state = "obstacle"
                        color = (0,0,0)
                    elif i == 1 and j == 1:
                        self.start = (j,i)
                        state = "start"
                        color = (255,0,0)
                    elif i == y_size - 2 and j == x_size - 2:
                        self.end = (j,i)
                        state = "end"
                        color = (0,255,0)
                    else:
                        if random() < wall_chance:
                            state = "obstacle"
                            color = (0,0,0)
                        else:
                            state = "open"
                            color = (255,255,255)
                    tile = Tile(j, i, state)
                    tile.surf.fill(color)
                    temp.append(tile)
                self.tiles.append(temp)

        #self.initiate_board()

    def draw_board(self):
        for i in range(y_size):
            for j in range(x_size):
                self.tiles[i][j].draw()

    def initiate_board(self):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                xpos = self.start[1] + j
                ypos = self.start[0] + i
                if self.tiles[ypos][xpos].state in ['open', 'revealed']:
                    if i == 0 and j == 0:
                        pass
                    else:
                        if self.tiles[ypos][xpos].state == 'open':
                            self.revealed_tiles.append((ypos, xpos))
                        self.tiles[ypos][xpos].open_tile(i, j, self.tiles[self.start[0]][self.start[1]], self.end)
                elif self.tiles[ypos][xpos].state == 'end':
                    next = False

    def reveal_next_tile(self):
        next = True
        if not self.revealed_tiles:
            next = False
        else:
            min_f = 999999
            min_h = 999999
            for coords in self.revealed_tiles:
                tile = self.tiles[coords[0]][coords[1]]
                if tile.f_cost <= min_f:
                    if tile.f_cost < min_f:
                        min_h = 999999
                    min_f = tile.f_cost
                    if tile.h_cost <= min_h:
                        min_h = tile.h_cost
                        closest = coords

            for i in [-1, 0, 1]:
                for j in [-1, 0, 1]:
                    xpos = closest[1] + j
                    ypos = closest[0] + i
                    if self.tiles[ypos][xpos].state in ['open', 'revealed', 'end']:
                        if i == 0 and j == 0:
                            pass
                        else:
                            if self.tiles[ypos][xpos].state == 'open':
                                self.revealed_tiles.append((ypos, xpos))
                            self.tiles[ypos][xpos].open_tile(i, j, self.tiles[closest[0]][closest[1]], self.end)
                    if self.tiles[ypos][xpos].state == 'end':
                        next = False
                        self.last_path = (self.end[1], self.end[0])
            self.tiles[closest[0]][closest[1]].state = 'closed'
            self.tiles[closest[0]][closest[1]].surf.fill((255,150, 150))
            self.revealed_tiles.remove(closest)
        return next

    def back_propagation(self):
        for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
                ypos = self.last_path[0] + j
                xpos = self.last_path[1] + i
                if self.tiles[ypos][xpos].state in ['closed', 'start']:
                    if self.tiles[ypos][xpos].state == 'start':
                        return False
                    elif i == 0 and j == 0:
                        pass
                    else:
                        if abs(i) == abs(j):
                            if self.tiles[ypos][xpos].g_cost == self.tiles[ypos - j][xpos - i].g_cost - 14:
                                self.tiles[ypos][xpos].state = 'path'
                                self.tiles[ypos][xpos].surf.fill((255,150,0))
                                self.last_path = (ypos, xpos)
                                return True
                        else:
                            if self.tiles[ypos][xpos].g_cost == self.tiles[ypos - j][xpos - i].g_cost - 10:
                                self.tiles[ypos][xpos].state = 'path'
                                self.tiles[ypos][xpos].surf.fill((255,150,0))
                                self.last_path = (ypos, xpos)
                                return True
