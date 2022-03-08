import config
import numpy as np


def count_non_zeros(landscape, startX, startY):
    non_zero_colors = 0

    for i in range(startX, startX+config.TILE_SIZE):
        for j in range(startY, startX+config.TILE_SIZE):
            if landscape[i][j] != 0:
                non_zero_colors += 1

    return non_zero_colors


class Landscape:
    def __init__(self, tile_input):
        self.landscape = tile_input.land_arr
        self.tiles = tile_input.tiles
        self.targets = tile_input.targets
        self.land_size = tile_input.land_size
        self.current = self.count_colors(self.landscape)
        self.states = [self.landscape]
        self.solution_map = {}

    def put_tile(self, tile, startX, startY):
        if tile.type == 'OUTER_BOUNDARY':
            return tile.outer_block(self, startX, startY)
        elif tile.type == 'EL_SHAPE':
            return tile.el_block(self, startX, startY)
        elif tile.type == 'FULL_BLOCK':
            return tile.full_block(self, startX, startY)


    # def get_domains(self):
    #     new_l = []
    #     divider = self.land_size // config.TILE_SIZE
    #     arr = np.array(self.landscape)
    #     ver_split = np.array_split(arr,divider,axis=0)

    #     for a in ver_split:
    #         hor_split = np.array_split(a,divider,axis=1)
    #         hor_split = list(map(lambda x: x.tolist(), hor_split))
    #         new_l += hor_split

    #     return new_l

    def get_variables(self):
        divider = self.land_size // config.TILE_SIZE
        startX, startY = 0, 0
        variables = [(startX, startY)]
        for i in range(divider**2):
            variables.append((startX, startY))
            startX, startY = self.get_next_location(startX, startY)

        return variables

    # def get_lcv_tile(self, startX, startY):
    #     first_tiles = []
    #     second_tiles = []
    #     third_tiles = []

    #     el_shape = next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
    #     el_shape = self.count_colors(self.put_tile(el_shape, startX, startY))
    #     el_shape_dist = self.check_distance(el_shape)

    #     out_shape = next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
    #     out_shape = self.count_colors(self.put_tile(out_shape, startX, startY))
    #     out_shape_dist = self.check_distance(out_shape)

    #     full_shape = next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)
    #     full_shape = self.count_colors(self.put_tile(full_shape, startX, startY))
    #     full_shape_dist = self.check_distance(full_shape)

    #     def most_common(lst):
    #         return max(set(lst), key=lst.count)

    #     for el, out, full in zip(el_shape_dist.items(), out_shape_dist.items(), full_shape_dist.items()):
    #         sorted_by = sorted((el, out, full), key=lambda tup: tup[1])
    #         for i in range(3):
    #             if i == 0:
    #                 if sorted_by[i] == el:
    #                     first_tiles.append('EL_SHAPE')
    #                 elif sorted_by[i] == out:
    #                     first_tiles.append('OUTER_BOUNDARY')
    #                 elif sorted_by[i] == full:
    #                     first_tiles.append('FULL_BLOCK')
    #             elif i == 1:
    #                 if sorted_by[i] == el:
    #                     second_tiles.append('EL_SHAPE')
    #                 elif sorted_by[i] == out:
    #                     second_tiles.append('OUTER_BOUNDARY')
    #                 elif sorted_by[i] == full:
    #                     second_tiles.append('FULL_BLOCK')
    #             elif i == 2:
    #                 if sorted_by[i] == el:
    #                     third_tiles.append('EL_SHAPE')
    #                 elif sorted_by[i] == out:
    #                     third_tiles.append('OUTER_BOUNDARY')
    #                 elif sorted_by[i] == full:
    #                     third_tiles.append('FULL_BLOCK')
        
    #     tile1 = most_common(first_tiles)
    #     tile1 = next((x for x in self.tiles if x.type == tile1), None)

    #     tile2 = most_common(second_tiles)
    #     tile2 = next((x for x in self.tiles if x.type == tile2), None)

    #     tile3 = most_common(third_tiles)
    #     tile3 = next((x for x in self.tiles if x.type == tile3), None)
    
    #     if tile1.count > 0:
    #         print('first_tiles')
    #         return tile1
    #     elif tile2.count > 0:
    #         print('second_tiles')
    #         return tile2
    #     elif tile3.count > 0:
    #         print('third_tiles')
    #         return tile3

    def heuristic(self, startX, startY):
        el_shape = next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
        el_shape = self.put_tile(el_shape, startX, startY)
        el_shape_cnt = count_non_zeros(el_shape, startX, startY)
        # el_shape_dist = sum(self.check_distance(el_shape).values())

        out_shape = next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
        out_shape = self.put_tile(out_shape, startX, startY)
        out_shape_cnt = count_non_zeros(out_shape, startX, startY)
        # out_shape_dist = sum(self.check_distance(out_shape).values())

        full_shape = next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)
        full_shape = self.put_tile(full_shape, startX, startY)
        full_shape_cnt = count_non_zeros(full_shape, startX, startY)
        # full_shape_dist = sum(self.check_distance(full_shape).values())

        maximum = max([el_shape_cnt, out_shape_cnt, full_shape_cnt])

        if el_shape_cnt == maximum:
            print("El shape")
            return next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
        elif out_shape_cnt == maximum:
            print("Outer shape")
            return next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
        elif full_shape_cnt == maximum:
            print("Full shape")
            return next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)


    def count_colors(self, landscape=None):
        color_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

        if landscape is None:
            landscape = self.landscape

        for i in range(self.land_size):
            for j in range(self.land_size):
                if landscape[i][j] != 0:
                    color_dict[str(landscape[i][j])] += 1

        return color_dict

    def check_distance(self, colors):
        diff_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

        for key, val in self.targets.items():
            diff_dict[key] = colors[key] - val

        return diff_dict

    def has_reached_target(self):
        if all(self.current[key] == self.targets[key] for key, val in self.current.items()):
            return True
        else:
            return False

    def create_copy(self):
        cp = [[0] * self.land_size for _ in range(self.land_size)]

        for i in range(self.land_size):
            for j in range(self.land_size):
                cp[i][j] = self.landscape[i][j]
        
        return cp

    def can_put_tile(self, tile, startX, startY):
        possible = self.put_tile(tile, startX, startY)
        colors = self.count_colors(possible)

        for key, _ in colors.items():
            if colors[key] < self.targets[key]:
                return False
            
        return True

    def get_next_location(self, startX, startY):
        if startX + config.TILE_SIZE < self.land_size:
            startX += config.TILE_SIZE
        else:
            startX = 0

            if startY + config.TILE_SIZE < self.land_size:
                startY += config.TILE_SIZE
        return startX, startY

    def __str__(self) -> str:
        res = "\n_______________________________________\n"
        for i in range(self.land_size):
            for j in range(self.land_size):
                if self.landscape[i][j] > 0:
                    res += str(self.landscape[i][j]) + config.CELL_SEPARATOR
                else:
                    res += ' ' + config.CELL_SEPARATOR
            res += config.LINE_SEPARATOR
        res += "_______________________________________"
        return res

    