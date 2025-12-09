import os, platform
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import Counter, deque

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
            largest = area if area > largest else largest

    return largest

def star2(data):
    on_tiles = set()
    for i, pos1 in enumerate(data):
        if i == len(data)-1:
            pos2 = data[0]
        else:
            pos2 = data[i+1]
        min_x, max_x = min(pos1[0], pos2[0]), max(pos1[0], pos2[0])
        min_y, max_y = min(pos1[1], pos2[1]), max(pos1[1], pos2[1])
        for x in range(min_x, max_x+1):
            for y in range(min_y, max_y+1):
                pos = (x,y)
                on_tiles.add(pos)
    print(len(on_tiles))
    show_on_tiles(on_tiles)
    largest = 0
    for i, pos1 in enumerate(data):
        for pos2 in data[i+1:]:
            min_x, max_x = min(pos1[0], pos2[0]), max(pos1[0], pos2[0])
            min_y, max_y = min(pos1[1], pos2[1]), max(pos1[1], pos2[1])
            is_valid = True
            for y in range(min_y, max_y+1):
                if (min_x, y) not in on_tiles or (max_x, y) not in on_tiles:
                    is_valid = False
                    break
            if is_valid == False:
                continue
            for x in range(min_x, max_x+1):
                if (x, min_y) not in on_tiles or (x, max_y) not in on_tiles:
                    is_valid = False
                    break
            if is_valid == False:
                continue
            area = abs((pos1[0]-pos2[0]+1)*(pos1[1]-pos2[1]+1))
            largest = area if area > largest else largest
    return largest

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