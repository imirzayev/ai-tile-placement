import re


class Landscape:
    def __init__(self, lines) -> None:
        self.COLORS = 4
        self.lines = lines
        self.land_idx, self.tile_idx, self.target_idx, self.size = self.get_indexes()
        self.CELL_SEPARATOR = " "
        self.LINE_SEPARATOR = "\n"
        self.bushes = self.read_landscape()
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

        size = len(self.lines[land_idx]) // 2

        return land_idx, tile_idx, target_idx, size

    def read_landscape(self):
        dimension = len(self.lines[self.land_idx]) // 2
        landscape = self.lines[self.land_idx:self.land_idx+dimension]

        bushes = [[0] * len(landscape) for _ in range(len(landscape))]

        for i in range(len(landscape)):
            t = 0
            for j in range(0, 2 * len(landscape), 2):
                if landscape[i][j] != ' ':
                    bushes[i][t] = int(landscape[i][j])
                t += 1
        return bushes


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

    def full_block(self, startX, startY):
        for i in range(startX, startX + 4):
            for j in range(startY, startY + 4):
                self.bushes[i][j] = 0
        return startX + 4, startY + 4

    def outer_block(self, startX, startY):
        for i in range(startX, startX + 4):
            for j in range(startY, startY + 4):
                if (i == startX) or (i == startX +3) or (j == startY) or (j == startY + 3):
                    self.bushes[i][j] = 0
        return startX + 4, startY + 4

    def l_block(self, startX, startY):
        for i in range(startX, startX + 4):
            for j in range(startY, startY + 4):
                if (i == startX) or (j == startY):
                    self.bushes[i][j] = 0
        return startX + 4, startY + 4

    def count_colors(self):
        color_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

        for i in range(self.size):
            for j in range(self.size):
                if self.bushes[i][j] != 0:
                    color_dict[str(self.bushes[i][j])] += 1

        return color_dict

    def __str__(self) -> str:
        res = ""
        for i in range(self.size):
            for j in range(self.size):
                if self.bushes[i][j] > 0:
                    res += str(self.bushes[i][j]) + self.CELL_SEPARATOR
                else:
                    res += ' ' + self.CELL_SEPARATOR
            res += self.LINE_SEPARATOR
        return res


if __name__ == "__main__":
    f = open("test.txt", "r")
    lines = f.readlines()
    f.close()

    lines = list(map(lambda x: re.sub('[\n]$', '', x), lines))
    landscape = Landscape(lines)
    print(landscape.count_colors())
    landscape.outer_block(0, 0)
    print('\n\n')
    print(landscape)

    