import config

class Tile:
    def __init__(self, tile):
        self.size = config.TILE_SIZE

        self.type = tile[0]
        self.count = tile[1]

    def full_block(self, landscape, startX, startY):
        land_copy = landscape.landscape.copy()
        for i in range(startX, startX + self.size):
            for j in range(startY, startY + self.size):
                land_copy[i][j] = 0
        return land_copy

    def outer_block(self, landscape, startX, startY):
        land_copy = landscape.landscape.copy()
        for i in range(startX, startX + self.size):
            for j in range(startY, startY + self.size):
                if (i == startX) or (i == startX + self.size - 1) or (j == startY) or (j == startY + self.size - 1):
                    land_copy[i][j] = 0
        return land_copy

    def el_block(self, landscape, startX, startY):
        land_copy = landscape.landscape.copy()
        for i in range(startX, startX + self.size):
            for j in range(startY, startY + self.size):
                if (i == startX) or (j == startY):
                    landscape.landscape[i][j] = 0
        return land_copy

    def __str__(self) -> str:
        return f'Tile: {self.type}. Count: {self.count}.'