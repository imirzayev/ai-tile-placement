def solve(landscape, startX, startY):
    """Recursive backtracking algorithm to solve the problem."""

    if landscape.has_reached_target():
        return True

    for tile in landscape.tiles:
        if tile.count == 0:
            continue

        copied = landscape.create_copy()
        
        if landscape.can_put_tile(tile, startX, startY):
            tile.count -= 1
            landscape.landscape = landscape.put_tile(tile, startX, startY)
            landscape.current = landscape.count_colors(landscape.landscape)
            landscape.solution_map[f'X{startX}Y{startY}'] = tile.type
            
            prevstartY, prevstartX = startY, startX
            startX, startY = landscape.get_next_location(startX, startY)

            if solve(landscape, startX, startY):
                return True
            
            startX, startY = prevstartX, prevstartY
            landscape.landscape = copied
            landscape.current = landscape.count_colors(landscape.landscape)
            tile.count += 1

    return False