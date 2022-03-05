import re
import simpleai


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
        self.current = self.count_colors()

    

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

    def check_distance(self):
        diff_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

        for key, val in self.targets:
            diff_dict[key] = self.targets[key] - self.current[key]

        return diff_dict

    def has_reached_target(self):
        if all(v == 0 for v in self.current.values()):
            return True
        else:
            return False

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
    landscape = Landscape(lines)
    print(landscape.count_colors())
    landscape.outer_block(0, 0)
    print('\n\n')
    print(landscape)

    