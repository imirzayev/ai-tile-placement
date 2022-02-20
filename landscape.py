import random

class landscape:
    def __init__(self, width, height) -> None:
        self.COLORS = 4
        self.CELL_SEPARATOR = " "
        self.LINE_SEPARATOR = "\n"
        self.width = width
        self.height = height
        self.bushes = [[0] * width for _ in range(height)]
        self.generate_random_bushes()

    def generate_random_bushes(self) -> None:
        for i in range(self.height):
            for j in range(self.width):
                self.generate_one_bush(i, j)
    
    def generate_one_bush(self, i, j) -> None:
        self.bushes[i][j] = random.randint(0, self.COLORS)

    def __str__(self) -> str:
        res = ""
        for i in range(self.height):
            for j in range(self.width):
                if self.bushes[i][j] > 0:
                    res += str(self.bushes[i][j]) + self.CELL_SEPARATOR
                else:
                    res += ' ' + self.CELL_SEPARATOR
            res += self.LINE_SEPARATOR
        return res

if __name__ == "__main__":
    my_land = landscape(5, 7)
    print(my_land)

    


