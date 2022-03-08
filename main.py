from input_parser import TPInput
from landscape import Landscape
from backtracking import solve
import os
import time


if __name__ == "__main__":
    input_name = 'tilesproblem_1326658934155700.txt'
    file = os.path.join('inputs', input_name)
    tile_input = TPInput(file)
    landscape = Landscape(tile_input)
    print(landscape)
    print(landscape.targets)
    start_time = time.time()
    solve(landscape, 0, 0)
    print(landscape)
    print(landscape.count_colors(landscape.bushes))
    print(landscape.print_output())
    print("Done in --- %.2f seconds ---" % (time.time() - start_time))
