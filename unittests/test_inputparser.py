import os
import unittest
from input_parser import TPInput


class TestInput(unittest.TestCase):
    def test_indexes(self):
        for file in os.listdir('../inputs'):
            tp_input = TPInput(os.path.join('../inputs', file))
            self.assertEqual(tp_input.land_idx, 2)
            self.assertEqual(tp_input.tile_idx, 24)
            self.assertEqual(tp_input.target_idx, 27)
            self.assertEqual(tp_input.land_size, 20)

    def test_read_landscape(self):
        tp_input = TPInput('../inputs/tilesproblem_1326658913086500.txt')
        correct_arr = [[2, 2, 1, 3, 0, 3, 4, 0, 4, 2, 2, 4, 0, 4, 0, 0, 0, 2, 4, 3], 
                        [0, 2, 1, 3, 2, 2, 0, 0, 0, 1, 0, 1, 2, 2, 0, 2, 3, 4, 4, 4], 
                        [2, 1, 0, 0, 0, 2, 2, 4, 3, 2, 2, 2, 1, 2, 2, 0, 0, 1, 1, 0], 
                        [0, 3, 2, 0, 1, 0, 1, 1, 4, 1, 3, 4, 2, 1, 0, 0, 0, 1, 4, 1], 
                        [4, 2, 3, 4, 4, 4, 0, 2, 2, 0, 0, 3, 2, 3, 0, 2, 0, 2, 3, 2], 
                        [2, 4, 1, 0, 1, 1, 1, 4, 1, 0, 1, 3, 0, 3, 2, 0, 4, 0, 1, 2], 
                        [4, 3, 1, 4, 3, 3, 1, 4, 0, 1, 1, 1, 4, 2, 2, 4, 1, 4, 3, 4], 
                        [2, 1, 1, 1, 4, 4, 3, 4, 4, 2, 0, 3, 0, 3, 0, 3, 4, 4, 0, 0], 
                        [1, 0, 0, 3, 0, 3, 2, 2, 4, 3, 3, 2, 4, 0, 0, 0, 1, 4, 3, 0], 
                        [0, 1, 3, 1, 3, 2, 3, 2, 1, 0, 0, 1, 4, 3, 2, 1, 2, 4, 1, 3], 
                        [0, 3, 0, 2, 3, 4, 3, 3, 1, 0, 0, 1, 2, 3, 3, 0, 2, 1, 2, 3], 
                        [1, 3, 1, 1, 4, 4, 4, 2, 0, 4, 4, 3, 4, 1, 1, 2, 2, 3, 2, 3], 
                        [2, 1, 0, 1, 1, 1, 0, 1, 2, 1, 3, 2, 2, 3, 3, 4, 0, 0, 3, 4], 
                        [4, 2, 0, 0, 2, 3, 2, 1, 1, 1, 4, 0, 4, 4, 3, 2, 2, 0, 2, 3], 
                        [3, 1, 4, 3, 0, 1, 4, 4, 1, 1, 3, 1, 1, 1, 0, 0, 2, 1, 2, 0], 
                        [3, 2, 2, 4, 3, 1, 1, 4, 1, 0, 0, 3, 1, 2, 3, 2, 2, 2, 3, 4], 
                        [0, 2, 2, 1, 3, 3, 1, 1, 0, 0, 0, 3, 0, 4, 4, 2, 2, 2, 4, 4], 
                        [0, 1, 4, 3, 0, 0, 1, 1, 3, 3, 0, 4, 3, 4, 4, 4, 4, 1, 1, 1], 
                        [3, 2, 1, 2, 0, 3, 1, 1, 3, 4, 2, 4, 0, 3, 0, 2, 0, 0, 4, 1], 
                        [4, 0, 3, 4, 0, 4, 3, 4, 3, 2, 2, 2, 1, 4, 3, 4, 3, 0, 0, 1]]
        self.assertEqual(tp_input.land_arr, correct_arr)

    def test_targets(self):
        correct_targets = [{'1': 18, '2': 19, '3': 16, '4': 17}, 
                            {'1': 27, '2': 22, '3': 15, '4': 35}, 
                            {'1': 12, '2': 17, '3': 19, '4': 21}, 
                            {'1': 18, '2': 16, '3': 13, '4': 22}, 
                            {'1': 23, '2': 18, '3': 20, '4': 18}, 
                            {'1': 21, '2': 16, '3': 26, '4': 23}, 
                            {'1': 20, '2': 25, '3': 25, '4': 29}, 
                            {'1': 17, '2': 37, '3': 24, '4': 29}, 
                            {'1': 24, '2': 24, '3': 16, '4': 15}, 
                            {'1': 17, '2': 20, '3': 19, '4': 18}, 
                            {'1': 34, '2': 30, '3': 28, '4': 28}, 
                            {'1': 11, '2': 26, '3': 21, '4': 20}, 
                            {'1': 24, '2': 21, '3': 18, '4': 17}, 
                            {'1': 21, '2': 25, '3': 22, '4': 22}, 
                            {'1': 25, '2': 31, '3': 19, '4': 28}, 
                            {'1': 19, '2': 30, '3': 19, '4': 30}, 
                            {'1': 25, '2': 25, '3': 21, '4': 24}, 
                            {'1': 11, '2': 16, '3': 22, '4': 12}, 
                            {'1': 21, '2': 23, '3': 31, '4': 27}, 
                            {'1': 18, '2': 22, '3': 17, '4': 26}]
        for i, file in enumerate(sorted(os.listdir('../inputs'))):
            tp_input = TPInput(os.path.join('../inputs', file))
            self.assertEqual(tp_input.targets, correct_targets[i])

    def test_tiles(self):
        correct_tiles = [{'OUTER_BOUNDARY': 6, 'EL_SHAPE': 7, 'FULL_BLOCK': 12}, 
                        {'OUTER_BOUNDARY': 6, 'EL_SHAPE': 11, 'FULL_BLOCK': 8}, 
                        {'OUTER_BOUNDARY': 8, 'EL_SHAPE': 6, 'FULL_BLOCK': 11}, 
                        {'OUTER_BOUNDARY': 9, 'EL_SHAPE': 6, 'FULL_BLOCK': 10}, 
                        {'OUTER_BOUNDARY': 2, 'EL_SHAPE': 11, 'FULL_BLOCK': 12}, 
                        {'OUTER_BOUNDARY': 9, 'EL_SHAPE': 8, 'FULL_BLOCK': 8}, 
                        {'OUTER_BOUNDARY': 7, 'EL_SHAPE': 11, 'FULL_BLOCK': 7}, 
                        {'OUTER_BOUNDARY': 4, 'EL_SHAPE': 13, 'FULL_BLOCK': 8}, 
                        {'OUTER_BOUNDARY': 14, 'EL_SHAPE': 5, 'FULL_BLOCK': 6}, 
                        {'OUTER_BOUNDARY': 12, 'EL_SHAPE': 5, 'FULL_BLOCK': 8}, 
                        {'EL_SHAPE': 12, 'OUTER_BOUNDARY': 8, 'FULL_BLOCK': 5}, 
                        {'EL_SHAPE': 7, 'OUTER_BOUNDARY': 7, 'FULL_BLOCK': 11}, 
                        {'EL_SHAPE': 7, 'OUTER_BOUNDARY': 10, 'FULL_BLOCK': 8}, 
                        {'EL_SHAPE': 7, 'OUTER_BOUNDARY': 11, 'FULL_BLOCK': 7}, 
                        {'EL_SHAPE': 9, 'OUTER_BOUNDARY': 12, 'FULL_BLOCK': 4}, 
                        {'EL_SHAPE': 8, 'OUTER_BOUNDARY': 11, 'FULL_BLOCK': 6}, 
                        {'EL_SHAPE': 9, 'OUTER_BOUNDARY': 10, 'FULL_BLOCK': 6}, 
                        {'EL_SHAPE': 5, 'OUTER_BOUNDARY': 10, 'FULL_BLOCK': 10}, 
                        {'EL_SHAPE': 9, 'OUTER_BOUNDARY': 10, 'FULL_BLOCK': 6}, 
                        {'EL_SHAPE': 10, 'OUTER_BOUNDARY': 5, 'FULL_BLOCK': 10}]

        for i, file in enumerate(sorted(os.listdir('../inputs'))):
            tp_input = TPInput(os.path.join('../inputs', file))
            tiles_dict = {}
            for tile in tp_input.tiles:
                tiles_dict[tile.type] = tile.count
            self.assertEqual(tiles_dict, correct_tiles[i])


if __name__ == '__main__':
    unittest.main()