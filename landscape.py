import config
from input import TPInput
from tile import Tile


class Landscape:
    def __init__(self, tile_input):
        self.landscape = tile_input.land_arr
        self.tiles = tile_input.tiles
        self.targets = tile_input.targets
        self.land_size = tile_input.land_size

        self.current = self.count_colors()
        self.states = [self.landscape]

    def put_tile(self, tile, startX, startY):
        if tile.type == 'OUTER_BOUNDARY':
            tile.outer_block(self, startX, startY)
        elif tile.type == 'EL_SHAPE':
            tile.el_block(self, startX, startY)
        elif tile.type == 'FULL_BLOCK':
            tile.full_block(self, startX, startY)

        self.current = self.count_colors()


    def count_colors(self):
        color_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

        for i in range(self.land_size):
            for j in range(self.land_size):
                if self.landscape[i][j] != 0:
                    color_dict[str(self.landscape[i][j])] += 1

        return color_dict

    def check_distance(self):
        diff_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

        for key, val in self.targets:
            diff_dict[key] = val - self.current[key]

        return diff_dict

    def has_reached_target(self):
        if all(v == 0 for v in self.current.values()):
            return True
        else:
            return False

    def constr_check(self, tile, startX, startY):
        def constr_ok():
            for key, val in self.current.items():
                if val < self.targets[key]:
                    return False
                else:
                    return True

        self.put_tile(tile, startX, startY)
        if constr_ok():
            self.states.append(self.landscape)
            return True
        else:
            self.landscape = self.states[-1]
            return False

    def __str__(self) -> str:
        res = ""
        for i in range(self.land_size):
            for j in range(self.land_size):
                if self.landscape[i][j] > 0:
                    res += str(self.landscape[i][j]) + config.CELL_SEPARATOR
                else:
                    res += ' ' + config.CELL_SEPARATOR
            res += config.LINE_SEPARATOR
        return res


if __name__ == "__main__":
    tile_input = TPInput('inputs/tilesproblem_1326658913086500.txt')
    landscape = Landscape(tile_input)
    tile = Tile(next(iter(landscape.tiles.items())))
    print(tile.count)
    print(landscape)
    print(landscape.count_colors())
    landscape.put_tile(tile, 0, 0)
    print('\n\n')
    print(landscape)
    print(landscape.count_colors())

    