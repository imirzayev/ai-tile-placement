from re import S
from tkinter.messagebox import NO
from django import conf
from urllib3 import Retry
import config
from input import TPInput
from tile import Tile
import random


class Landscape:
    def __init__(self, tile_input):
        self.landscape = tile_input.land_arr
        self.tiles = tile_input.tiles
        self.targets = tile_input.targets
        self.land_size = tile_input.land_size

        # self.current = self.count_colors(self.)
        self.states = [self.landscape]
        self.solution_map = []

    def put_tile(self, tile, startX, startY):
        if tile.type == 'OUTER_BOUNDARY':
            return tile.outer_block(self, startX, startY)
        elif tile.type == 'EL_SHAPE':
            return tile.el_block(self, startX, startY)
        elif tile.type == 'FULL_BLOCK':
            return tile.full_block(self, startX, startY)


    def count_colors(self, landscape=None):
        color_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

        if landscape is None:
            landscape = self.landscape

        for i in range(self.land_size):
            for j in range(self.land_size):
                if landscape[i][j] != 0:
                    color_dict[str(landscape[i][j])] += 1

        return color_dict

    def check_distance(self):
        diff_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

        for key, val in self.targets:
            diff_dict[key] = val - self.current[key]

        return diff_dict

    def has_reached_target(self):
        colors = self.count_colors(self.landscape)

        if all(colors[key] == self.targets[key] for key, val in colors.items()):
            return True
        else:
            return False

    def create_copy(self):
        cp = [[0] * self.land_size for _ in range(self.land_size)]

        for i in range(self.land_size):
            for j in range(self.land_size):
                cp[i][j] = self.landscape[i][j]
        
        return cp

    def can_put_tile(self, tile, locX, locY):
        possible = self.put_tile(tile, locX, locY)
        colors = self.count_colors(possible)

        for key, _ in colors.items():
            if colors[key] < self.targets[key]:
                return False
            
        return True

    def get_next_location(self, locX, locY):
        if locX + config.TILE_SIZE < self.land_size:
            locX += config.TILE_SIZE
        else:
            locX = 0

            if locY + config.TILE_SIZE < self.land_size:
                locY += config.TILE_SIZE
        return locX, locY
    

    def __str__(self) -> str:
        res = "\n________________________________________\n"
        for i in range(self.land_size):
            for j in range(self.land_size):
                if self.landscape[i][j] > 0:
                    res += str(self.landscape[i][j]) + config.CELL_SEPARATOR
                else:
                    res += ' ' + config.CELL_SEPARATOR
            res += config.LINE_SEPARATOR
        res += "________________________________________"
        return res

    def backtrack(self, locX, locY):
        if self.has_reached_target():
            return True

        for tile in self.tiles:
            if tile.count == 0:
                continue

            copied = self.create_copy()
            
            if self.can_put_tile(tile, locX, locY):
                tile.count -= 1
                self.landscape = self.put_tile(tile, locX, locY)
                self.solution_map.append(f'Tile: {tile.type}. X: {locX}. Y: {locY}.')
                
                prevLocY, prevLocX = locY, locX
                locX, locY = self.get_next_location(locX, locY)

                if self.backtrack(locX, locY):
                    return True
                
                locX, locY = prevLocX, prevLocY
                self.landscape = copied
                tile.count += 1

        return False


if __name__ == "__main__":
    tile_input = TPInput('inputs/tilesproblem_1326658934155700.txt')
    landscape = Landscape(tile_input)
    print(landscape)
    print(landscape.targets)
    landscape.backtrack(0, 0)
    print(landscape)
    print(landscape.count_colors(landscape.landscape))

    