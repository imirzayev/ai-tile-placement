import unittest
from backtracking import backtrack
from landscape import Landscape
from input_parser import TPInput


class TestAlgo(unittest.TestCase):
    def test_something(self):
        tile_input = TPInput('../inputs/tilesproblem_1327003796850500.txt')
        landscape = Landscape(tile_input)
        targets = landscape.targets
        print(landscape)
        print(targets)
        backtrack(landscape, 0, 0)
        result = landscape.current
        print(landscape)
        print(result)
        self.assertEqual(targets, result)  # add assertion here


if __name__ == '__main__':
    unittest.main()
