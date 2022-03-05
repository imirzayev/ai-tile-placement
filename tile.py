import config

class Tile:
    def __init__(self, tile):
        self.size = config.TILE_SIZE

        self.type = tile[0]
        self.count = tile[1]

    def full_block(self, landscape, startX, startY):
        self.count -= 1
        
        for i in range(startX, startX + self.size):
            for j in range(startY, startY + self.size):
                landscape.landscape[i][j] = 0
        return startX + self.size, startY + self.size

    def outer_block(self, landscape, startX, startY):
        self.count -= 1

        for i in range(startX, startX + self.size):
            for j in range(startY, startY + self.size):
                if (i == startX) or (i == startX + self.size - 1) or (j == startY) or (j == startY + self.size - 1):
                    landscape.landscape[i][j] = 0
        return startX + self.size, startY + self.size

    def el_block(self, landscape, startX, startY):
        self.count -= 1
        
        for i in range(startX, startX + self.size):
            for j in range(startY, startY + self.size):
                if (i == startX) or (j == startY):
                    landscape.landscape[i][j] = 0
        return startX + self.size, startY + self.size