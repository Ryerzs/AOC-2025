import os, platform
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import Counter, deque, defaultdict


def day_():
    if platform.system() == "Linux":
        year = int(os.getcwd().split('/')[-2][-4:]) 
        day = int(__file__.split('/')[-2].split('-')[1].split('.')[0])
    else:
        year = int(os.getcwd().split('\\')[-2][-4:]) 
        day = int(__file__.split('\\')[-2].split('-')[1].split('.')[0])
    puzzle = Puzzle(year=year, day=day) 
    submit_a = "a" in sys.argv
    submit_b = "b" in sys.argv
    example = "e" in sys.argv

    if (submit_a or submit_b) and example:
        print("Cannot submit examples")
        return

    raw_data = puzzle.input_data
    if example:
        print("Using example")
        #use 'aocd year day --example' to get the example data
        with open('test-data.txt', 'r') as f:
            raw_data = f.read()
            
    start_time = time.perf_counter()
    data = format_data(raw_data)

    time1 = time.perf_counter()

    ans1 = star1(data)
    time2 = time.perf_counter()

    ans2 = star2(data)
    time3 = time.perf_counter()

    load_time = time1 - start_time
    star1_time = time2 - time1
    star2_time = time3 - time2

    if submit_a:
        print("Submitting star 1")
        puzzle.answer_a = ans1
    if submit_b:
        print("Submitting star 2")
        puzzle.answer_b = ans2
    if 1:
        print(f'Load time: {load_time}')
        print(f'Star 1 time: {star1_time}')
        print(f'Star 2 time: {star2_time}')
        print(f'Star 1 answer: {ans1}')
        print(f'Star 2 answer: {ans2}')

def format_data(raw):
    data = []
    for row in raw.splitlines():
        pos = [int(number) for number in row.split(',')]
        data.append(pos)
    return data
    
def star1(data):
    largest = 0
    for i, pos1 in enumerate(data):
        for pos2 in data[i+1:]:
            area = abs((pos1[0]-pos2[0]+1)*(pos1[1]-pos2[1]+1))
            largest = max(largest, area)

    return largest

def sign(number):
    if number < 0:
        return -1
    elif number > 0:
        return 1
    else:
        return 0

def add_pos(pos1, pos2):
    return (pos1[0]+pos2[0], pos1[1]+pos2[1])

def sub_pos(pos1, pos2):
    return (pos1[0]-pos2[0], pos1[1]-pos2[1])

def normalize(pos):
    return (sign(pos[0]), sign(pos[1]))

def rotate_right(pos):
    return (pos[1], -pos[0])

def rotate_left(pos):
    return (-pos[1], pos[0])

def star2(data):
    on_tiles = set()
    directions = {}
    for i, pos1 in enumerate(data):
        if i == len(data)-1:
            pos2 = tuple(data[0])
        else:
            pos2 = tuple(data[i+1])
        direction = normalize(sub_pos(pos2, pos1))
        inside = rotate_right(direction)

        current = tuple(pos1)
        on_tiles.add(current)
        while current != pos2:
            current = add_pos(current, direction)
            on_tiles.add(current)
            directions[current] = inside
        on_tiles.add(current)
        directions[current] = inside

    print(len(on_tiles))
    on_tiles_x_sorted = sorted(on_tiles, key=lambda pos: -pos[0])
    on_tiles_y_sorted = sorted(on_tiles, key=lambda pos: -pos[1])
    x_sorted = defaultdict(list)# For a given y value, display all points at the same y in decreasing order
    y_sorted = defaultdict(list)# For a given x value, display all points at the same x in decreasing order
    for tile in on_tiles_x_sorted:
        x_sorted[tile[1]].append(tile)
    for tile in on_tiles_y_sorted:
        y_sorted[tile[0]].append(tile)
    # show_on_tiles(on_tiles)

    largest = 0
    for i, pos1 in enumerate(data):
        for j, pos2 in enumerate(data[i+1:]):
            print(i,j, len(data))
            min_x, max_x = min(pos1[0], pos2[0]), max(pos1[0], pos2[0])
            min_y, max_y = min(pos1[1], pos2[1]), max(pos1[1], pos2[1])
            # Valid if all 4 corners are inside the shape. How do I know if a point is inside?
            corners = [(min_x, min_y),
                       (min_x, max_y),
                       (max_x, min_y),
                       (max_x, max_y)]
            valids = [1 for corner in corners if is_inside(corner, on_tiles, x_sorted, y_sorted, directions) == False]

            if sum(valids) > 0:
                continue

            area = abs((pos1[0]-pos2[0]+1)*(pos1[1]-pos2[1]+1))
            largest = max(largest, area)
    return largest

def is_inside(corner, on_tiles, x_sorted, y_sorted, directions):

    # If corner already on, then point is inside
    if corner in on_tiles:
        return True
    
    left_borders = [tile for tile in x_sorted[corner[1]] if tile[0] < corner[0]]
    up_borders   = [tile for tile in y_sorted[corner[0]] if tile[1] < corner[1]]

    if len(left_borders) == 0 or len(up_borders) == 0:
        return False

    # If first border to the left points inwards, then point is inside
    for border in left_borders:
        if border not in directions:
            continue
        if directions[border][0] == 1:
            return True
        break
        
    # If first border to upwards points inwards, then point is inside
    for border in up_borders:
        if border not in directions:
            continue
        if directions[border][0] == 1 or directions[border][1] == -1:
            return True
        break
    
    return False


    

def show_on_tiles(on_tiles):
    grid = []
    for j in range(9):
        grid.append(['.' for i in range(14)])
    for tile in on_tiles:
        grid[tile[1]][tile[0]] = 'X'
    for row in grid:
        print(''.join(row))

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    if platform.system() == "Linux":
        day = int(__file__.split('/')[-2].split('-')[1].split('.')[0])
    else:
        day = int(__file__.split('\\')[-2].split('-')[1].split('.')[0])
    stats.dump_stats(filename = f'profiling{day}.prof')

# run with `py day_n.py -- a b` to submit both stars for day n
if __name__ == '__main__':
    main()