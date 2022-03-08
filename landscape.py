import config
import numpy as np


def count_non_zeros(landscape, startX, startY):
    """Counts non zero elements within the given area. This is used in LCV function."""
    non_zero_colors = 0

    for i in range(startX, startX + config.TILE_SIZE):
        for j in range(startY, startX + config.TILE_SIZE):
            if landscape[i][j] != 0:
                non_zero_colors += 1

    return non_zero_colors


class Landscape:
    def __init__(self, tile_input):
        self.bushes = tile_input.land_arr
        self.tiles = tile_input.tiles
        self.targets = tile_input.targets
        self.land_size = tile_input.land_size
        self.current = self.count_colors(self.bushes)
        self.states = [self.bushes]
        self.solution_map = {}

    def put_tile(self, tile, startX, startY):
        """Puts the given tile to the given coordinate and returns the copy of the landscape"""

        if tile.type == 'OUTER_BOUNDARY':
            return tile.out(self, startX, startY)
        elif tile.type == 'EL_SHAPE':
            return tile.el(self, startX, startY)
        elif tile.type == 'FULL_BLOCK':
            return tile.full(self, startX, startY)

    def get_variable_lands(self):
        """Function to get the small sublandscapes size of 4x4"""
        new_l = []
        divider = self.land_size // config.TILE_SIZE
        arr = np.array(self.bushes)
        ver_split = np.array_split(arr, divider, axis=0)

        for a in ver_split:
            hor_split = np.array_split(a, divider, axis=1)
            hor_split = list(map(lambda x: x.tolist(), hor_split))
            new_l += hor_split

        return new_l

    def get_variables(self):
        """Gets the coordinates of 4x4 divided sublandscapes."""
        divider = self.land_size // config.TILE_SIZE
        startX, startY = 0, 0
        variables = [(startX, startY)]
        for i in range(divider ** 2):
            variables.append((startX, startY))
            startX, startY = self.get_next_location(startX, startY)

        return variables

    def count_colors(self, landscape=None):
        """Counts the color of given landscpae. If no landscape is given counts the colors of current attribute of
        the class instance"""

        color_dict = {'1': 0, '2': 0, '3': 0, '4': 0}

        if landscape is None:
            landscape = self.bushes

        for i in range(self.land_size):
            for j in range(self.land_size):
                if landscape[i][j] != 0:
                    color_dict[str(landscape[i][j])] += 1

        return color_dict

    def check_distance(self, colors):
        """Checks color distance between given colors and target"""
        diff_dict = {'1': 0, '2': 0, '3': 0, '4': 0}

        for key, val in self.targets.items():
            diff_dict[key] = colors[key] - val

        return diff_dict

    def has_reached_target(self):
        """Checks whether the current state of the landscape instance has reached the target."""
        if all(self.current[key] == self.targets[key] for key, val in self.current.items()):
            return True
        else:
            return False

    def create_copy(self):
        """Creates copy of the given list of lists."""
        cp = [[0] * self.land_size for _ in range(self.land_size)]

        for i in range(self.land_size):
            for j in range(self.land_size):
                cp[i][j] = self.bushes[i][j]

        return cp

    def can_put_tile(self, tile, startX, startY):
        """Considering the color constraints, checks whether given tile can be put on the given coordinates."""

        possible = self.put_tile(tile, startX, startY)
        colors = self.count_colors(possible)

        for key, _ in colors.items():
            if colors[key] < self.targets[key]:
                return False

        return True

    def get_next_location(self, startX, startY):
        """Considering the land size, calculates the next location to put the tile by incrementing the previous
        coordinates with tile size
        """
        if startX + config.TILE_SIZE < self.land_size:
            startX += config.TILE_SIZE
        else:
            startX = 0

            if startY + config.TILE_SIZE < self.land_size:
                startY += config.TILE_SIZE
        return startX, startY

    def print_output(self):
        """Prints the solution map as the output"""
        res = '# Tiles:\n'
        for i, (key, val) in enumerate(self.solution_map.items()):
            res += f'{i} {config.TILE_SIZE} {val}\n'
        return res

    def __str__(self) -> str:
        """Str function to print the landscape instance in readable format"""
        res = "\n_______________________________________\n"
        for i in range(self.land_size):
            for j in range(self.land_size):
                if self.bushes[i][j] > 0:
                    res += str(self.bushes[i][j]) + config.CELL_SEPARATOR
                else:
                    res += ' ' + config.CELL_SEPARATOR
            res += config.LINE_SEPARATOR
        res += "_______________________________________"
        return res

    #####################################################################################################################
    """The below heuristics have been tested. However, since they did not perform desirable result, they have not
     been included to solver function."""

    def heuristic1(self, startX, startY):
        """The heuristic in order to choose the next tile. The heuristic considers the distance between the target and
        the case there the specific tile is placed on the landscape. The heuristic considers the distance to the target
        for each color. The tile which causes the minimum distance for the most of the colors is used."""
        first_tiles = []
        second_tiles = []
        third_tiles = []

        el_shape = next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
        el_shape = self.count_colors(self.put_tile(el_shape, startX, startY))
        el_shape_dist = self.check_distance(el_shape)

        out_shape = next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
        out_shape = self.count_colors(self.put_tile(out_shape, startX, startY))
        out_shape_dist = self.check_distance(out_shape)

        full_shape = next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)
        full_shape = self.count_colors(self.put_tile(full_shape, startX, startY))
        full_shape_dist = self.check_distance(full_shape)

        def most_common(lst):
            return max(set(lst), key=lst.count)

        for el, out, full in zip(el_shape_dist.items(), out_shape_dist.items(), full_shape_dist.items()):
            sorted_by = sorted((el, out, full), key=lambda tup: tup[1])
            for i in range(3):
                if i == 0:
                    if sorted_by[i] == el:
                        first_tiles.append('EL_SHAPE')
                    elif sorted_by[i] == out:
                        first_tiles.append('OUTER_BOUNDARY')
                    elif sorted_by[i] == full:
                        first_tiles.append('FULL_BLOCK')
                elif i == 1:
                    if sorted_by[i] == el:
                        second_tiles.append('EL_SHAPE')
                    elif sorted_by[i] == out:
                        second_tiles.append('OUTER_BOUNDARY')
                    elif sorted_by[i] == full:
                        second_tiles.append('FULL_BLOCK')
                elif i == 2:
                    if sorted_by[i] == el:
                        third_tiles.append('EL_SHAPE')
                    elif sorted_by[i] == out:
                        third_tiles.append('OUTER_BOUNDARY')
                    elif sorted_by[i] == full:
                        third_tiles.append('FULL_BLOCK')

        tile1 = most_common(first_tiles)
        tile1 = next((x for x in self.tiles if x.type == tile1), None)

        tile2 = most_common(second_tiles)
        tile2 = next((x for x in self.tiles if x.type == tile2), None)

        tile3 = most_common(third_tiles)
        tile3 = next((x for x in self.tiles if x.type == tile3), None)

        if tile1.count > 0:
            print(tile1.type)
            return tile1
        elif tile2.count > 0:
            print('second_tiles')
            return tile2
        elif tile3.count > 0:
            print('third_tiles')
            return tile3

    def heuristic2(self, startX, startY):
        """The heuristic considers the sum of the distances to the target. It considers the distance as a whole
        sum of all color differences. The tile causing minimum sum is chosen as it approaches to the target most."""

        el_shape = next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
        el_shape = self.put_tile(el_shape, startX, startY)
        el_shape_dist = sum(self.check_distance(self.count_colors(el_shape)).values())
        print(f'El {el_shape_dist}')

        out_shape = next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
        out_shape = self.put_tile(out_shape, startX, startY)
        out_shape_dist = sum(self.check_distance(self.count_colors(out_shape)).values())
        print(f'Out {out_shape_dist}')

        full_shape = next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)
        full_shape = self.put_tile(full_shape, startX, startY)
        full_shape_dist = sum(self.check_distance(self.count_colors(full_shape)).values())
        print(f'Full {full_shape_dist}')

        minimum = min([el_shape_dist, out_shape_dist, full_shape_dist])

        if el_shape_dist == minimum:
            print("El shape")
            return next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
        elif out_shape_dist == minimum:
            print("Outer shape")
            return next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
        elif full_shape_dist == minimum:
            print("Full shape")
            return next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)

    def simple_lcv(self):
        """A simple least constraining value approach for choosing the next tile. Since the el shape tile covers less
        area than other tiles it has priority to be used among other. Second least constraining value is outer block,
        and final is full block."""
        el_shape = next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
        out_shape = next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
        full_shape = next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)

        if el_shape.count > 0:
            if el_shape.count == 1:
                exit()
            return el_shape
        elif out_shape.count > 0:
            print("out el shape")
            return out_shape
        elif full_shape.count > 0:
            print("Sent full shape")
            return full_shape

    def lcv(self, startX, startY):
        """Considers the number of non zero colors in the area and choses maximum one after the placement of the tile.
        This way we can achieve to choose the least constraining tile."""
        el_shape = next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
        el_shape = count_non_zeros(self.put_tile(el_shape, startX, startY))

        out_shape = next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
        out_shape = count_non_zeros(self.put_tile(out_shape, startX, startY))

        full_shape = next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)
        full_shape = count_non_zeros(self.put_tile(full_shape, startX, startY))

        maximum = max[el_shape, out_shape, full_shape]

        if el_shape == maximum:
            print("El shape")
            return next((x for x in self.tiles if x.type == 'EL_SHAPE'), None)
        elif out_shape == maximum:
            print("Outer shape")
            return next((x for x in self.tiles if x.type == 'OUTER_BOUNDARY'), None)
        elif full_shape == maximum:
            print("Full shape")
            return next((x for x in self.tiles if x.type == 'FULL_BLOCK'), None)
