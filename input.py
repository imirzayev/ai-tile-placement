import re
import config

class TPInput:

    def __init__(self, file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()

        self.lines = list(map(lambda x: re.sub('[\n]$', '', x), lines))
        self.land_idx, self.tile_idx, self.target_idx, self.land_size = self.get_indexes()
        self.COLORS = config.COLORS
        self.land_arr = self.read_landscape()
        self.tiles = self.read_tiles()
        self.targets = self.read_targets()

    def get_indexes(self):
        land_idx, tile_idx, target_idx = 0, 0, 0
        tiles_found = False

        for i, x in enumerate(self.lines):
            if x.startswith('# Landscape'):
                land_idx = i + 1

            elif x.startswith('# Tiles:') and not tiles_found:
                tile_idx = i + 1
                tiles_found = True

            elif x.startswith('# Targets:'):
                target_idx = i + 1

        land_size = len(self.lines[land_idx]) // 2

        return land_idx, tile_idx, target_idx, land_size

    def read_landscape(self):
        land_str = self.lines[self.land_idx:self.land_idx+self.land_size]

        land_arr = [[0] * self.land_size for _ in range(self.land_size)]

        for i in range(self.land_size):
            t = 0
            for j in range(0, 2 * self.land_size, 2):
                if land_str[i][j] != ' ':
                    land_arr[i][t] = int(land_str[i][j])
                t += 1

        return land_arr


    def read_tiles(self):
        tiles = self.lines[self.tile_idx]

        tile_dict = {}
        tiles = re.sub('[\{\}]', '', tiles)
        tiles = list(map(lambda x: x.strip(), tiles.split(',')))

        for tile in tiles:
            key, value = tile.split('=')
            tile_dict[key] = value

        return tile_dict


    def read_targets(self):
        targets = self.lines[self.target_idx:self.target_idx+self.COLORS]

        taget_dict = {}

        for target in targets:
            key, value = target.split(':')
            taget_dict[key] = value

        return taget_dict


if __name__ == '__main__':
    tp_input = TPInput('inputs/tilesproblem_1326658913086500.txt')
    print(tp_input.land_arr)
    print(tp_input.tiles)
    print(tp_input.targets)