import re

class TPInput:

    def __init__(self, file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()

        self.lines = list(map(lambda x: re.sub('[\n]$', '', x), lines))
        self.land_idx, self.tile_idx, self.target_idx, self.size = self.get_indexes()

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

        size = len(self.lines[land_idx]) // 2

        return land_idx, tile_idx, target_idx, size

    def read_landscape(self):
        dimension = len(self.lines[self.land_idx]) // 2
        land_str = self.lines[self.land_idx:self.land_idx+dimension]

        land_arr = [[0] * len(land_str) for _ in range(len(land_str))]

        for i in range(len(land_str)):
            t = 0
            for j in range(0, 2 * len(land_str), 2):
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