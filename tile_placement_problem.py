from typing import Tuple
import re


f = open("test.txt", "r")
lines = f.readlines()
f.close()


lines = list(map(lambda x: re.sub('[\n]$', '', x), lines))

def get_indexes(lines) -> Tuple[int, int, int]:
    land_idx, tile_idx, target_idx = 0, 0, 0
    tiles_found = False

    for i, x in enumerate(lines):
        if x.startswith('# Landscape'):
            land_idx = i + 1
        elif x.startswith('# Tiles:') and not tiles_found:
            tile_idx = i + 1
            tiles_found = True
        elif x.startswith('# Targets:'):
            target_idx = i + 1

    return land_idx, tile_idx, target_idx

def get_landscape(lines, land_idx) -> int:
    dimension = len(lines[land_idx]) // 2
    landscape = lines[land_idx:land_idx+dimension]
    
    return landscape


def read_landscape(landscape):
    bushes = [[0] * len(landscape) for _ in range(len(landscape))]

    for i in range(len(landscape)):
        t = 0
        for j in range(0, 2 * len(landscape), 2):
            if landscape[i][j] != ' ':
                bushes[i][t] = int(landscape[i][j])
            t += 1
    return bushes

def get_tiles(lines, tile_idx):
    return lines[tile_idx]

def read_tiles(tiles):
    my_dict = {}
    tiles = re.sub('[\{\}]', '', tiles)
    tiles = list(map(lambda x: x.strip(), tiles.split(',')))
    for tile in tiles:
        key, value = tile.split('=')
        my_dict[key] = value
    return my_dict

def get_targets(lines, target_idx, colors=4):
    return lines[target_idx:target_idx+colors]

def read_targets(targets):
    my_dict = {}
    for target in targets:
        key, value = target.split(':')
        my_dict[key] = value
    return my_dict


def full_block(startX, startY):
    for i in range(startX, startX + 4):
        for j in range(startY, startY) + 4:
            bushes[i][j] = 0
    return startX + 4, startY + 4

def outer_block(startX, startY):
    for i in range(startX, startX + 4):
        for j in range(startY, startY) + 4:
            if (i == startX) or (i == startX + 4) or (j == startY) or (j == startY + 4):
                bushes[i][j] = 0
    return startX + 4, startY + 4

def l_block(startX, startY):
    for i in range(startX, startX + 4):
        for j in range(startY, startY) + 4:
            if (i == startX) or (j == startY):
                bushes[i][j] = 0
    return startX + 4, startY + 4


land_idx, tile_idx, target_idx = get_indexes(lines)
print(land_idx, tile_idx, target_idx)
landscape = get_landscape(lines, land_idx)
bushes = read_landscape(landscape)
print(landscape)
print(bushes)
tiles = get_tiles(lines, tile_idx)
tiles_dict = read_tiles(tiles)
print(tiles)
print(tiles_dict)

targets = get_targets(lines, target_idx)
targets_dict = read_targets(targets)
# print(targets)
# print(targets_dict)


