import re
import config
from tile import Tile
import numpy as np
from simpleai.search import CspProblem
from simpleai.search import backtrack, MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE

#


class TPInput:

    def __init__(self, file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()

        self.lines = list(map(lambda x: re.sub('[\n]$', '', x), lines))
        self.land_idx, self.tile_idx, self.target_idx, self.land_size = self.get_indexes()
        self.COLORS = config.COLORS
        self.land_arr = self.read_landscape()
        self.tiles = self.read_tiles()
        self.targets = self.read_targets()
        self.domain=self.read_tiles()

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

        land_size = len(self.lines[land_idx]) // 2

        return land_idx, tile_idx, target_idx, land_size

    def read_landscape(self):
        land_str = self.lines[self.land_idx:self.land_idx+self.land_size]

        land_arr = [[0] * self.land_size for _ in range(self.land_size)]

        for i in range(self.land_size):
            t = 0
            for j in range(0, 2 * self.land_size, 2):
                if land_str[i][j] != ' ':
                    land_arr[i][t] = int(land_str[i][j])
                t += 1

        return land_arr


    def read_tiles(self):
        tiles = self.lines[self.tile_idx]

        tile_list = []
        domain=[]
        tiles = re.sub('[\{\}]', '', tiles)
        tiles = list(map(lambda x: x.strip(), tiles.split(',')))

        for tile in tiles:
            key, value = tile.split('=')
            tile_list.append(Tile((key, int(value))))
            
        
        for tile in tile_list:
            for i in range(0,tile.count):
                domain.append(tile.type+str(i))
            
       # print(self.domain)

     #   print(tile_list[0])
        return domain


    def read_targets(self):
        targets = self.lines[self.target_idx:self.target_idx+self.COLORS]

        taget_dict = {}

        for target in targets:
            key, value = target.split(':')
            taget_dict[key] = int(value)

        return taget_dict
    

def count_colors(self, landscape=None):
    color_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}

    if landscape is None:
        landscape = self.landscape

    for i in range(self.land_size):
        for j in range(self.land_size):
            if landscape[i][j] != 0:
                color_dict[str(landscape[i][j])] += 1

    return color_dict    

def split(array, nrows, ncols):
    """Split a matrix into sub-matrices."""

    r, h = array.shape
    return (array.reshape(h//nrows, nrows, -1, ncols)
             .swapaxes(1, 2)
             .reshape(-1, nrows, ncols))


def has_reached_target(counts,targets):
   # colors = self.count_colors(self.landscape)

    if all(counts[key] == targets[key] for key, val in counts.items()):
        
        #print(res)
        return True
    else:
      
        return False
    
    
def counter(variables, values):
    color_dict = {'1' : 0, '2' : 0, '3' : 0, '4' : 0}
   # print(variables)
    for variable in variables:
       # print(variable)
        #for value in values:
        if(values[0]=='O'):
            for i in range(1,3):
                for j in range (1,3):
                    if m[variable][i][j]:
                        color_dict[str(m[variable][i][j])]+=1
                       
        if(values[0]=='F'):
            for i in range(0,4):
                for j in range (0,4):
                    if m[variable][i][j]:
                        color_dict[str(m[variable][i][j])]+=1
                        
        if(values[0]=='E'):
            for i in range(1,4):
                for j in range (1,4):
                    if m[variable][i][j]:
                        color_dict[str(m[variable][i][j])]+=1
        
       
      #  print(values)           
                     
                
                
              # color_dict[str( )]+=1
   # print(tp_input.targets)    
    #print(color_dict)
        
    return has_reached_target(color_dict, tp_input.targets)

if __name__ == '__main__':
    tp_input = TPInput('inputs/tilesproblem_1326658913086500.txt')
    arr=np.array(tp_input.land_arr)
    m=split(arr,4,4)
    variables=tuple(range(0,len(m)))
    print(variables)
    exit()
   # for i in range (0,len(m)):
    #    variables+=tuple(str(i))    
   # variables=[*range(0,len(m))]
    domains={}
    for v in variables:
        domains[v]=tp_input.domain
    print(domains)
    exit()
   # domains={variables,tp_input.domain)}
    constraints=[(variables,counter) ]
    myproblem=CspProblem(variables, domains, constraints)
    result = backtrack(myproblem,variable_heuristic='',value_heuristic=LEAST_CONSTRAINING_VALUE,inference=True)
    
   # print(m)
    
   # print(tp_input.land_arr)
  #  print(tp_input.tiles)
   # print(tp_input.targets)