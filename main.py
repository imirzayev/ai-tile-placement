from input_parser import TPInput
from landscape import Landscape
from backtracking import backtrack
import os



if __name__ == "__main__":
    file = os.path.join('inputs', 'tilesproblem_1326658913086500.txt')
    tile_input = TPInput(file)
    landscape = Landscape(tile_input)
    print(landscape)
    print(landscape.targets)
    # landscape.get_lcv_tile(0, 0)
    # landscape.get_domains()

    backtrack(landscape, 0, 0)
    print(landscape)
    print(landscape.count_colors(landscape.landscape))
    print(landscape.solution_map)
    print('Done')