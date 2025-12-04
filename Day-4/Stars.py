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

def format_data(raw) -> dict[(int,int):str]:
    data = {}
    for y, row in enumerate(raw.splitlines()):
        for x, char in enumerate(row):
            if char == '@':
                data[(x,y)] = char
    return data
    
def star1(data):
    neighbour_map = get_total_neighbours(data)
    return sum([1 for nr_neighbour in neighbour_map.values() if nr_neighbour < 4])

def get_total_neighbours(data) -> dict[(int,int),int]:
    neighbour_map = {}
    for (x,y) in data.keys():
        total = 0
        for i in range(-1,2):
            for j in range(-1,2):
                if (x+i,y+j) in data.keys() and (i,j) != (0,0):
                    total += 1
        neighbour_map[(x,y)] = total
    return neighbour_map

def star2(data):
    possible_options = []
    for i in range(-1,2):
        for j in range(-1,2):
            if (i,j) != (0,0):
                possible_options.append((i,j))
    neighbour_map = get_total_neighbours(data)
    checked = set()
    to_check = deque([(x,y) for (x,y), nr_neighbour in neighbour_map.items() if nr_neighbour < 4])
    while len(to_check) > 0:
        (x,y) = to_check.popleft()
        if (x,y) in checked:
            continue
        checked.add((x,y))
        for (i,j) in possible_options:
            neighbour = (x+i, y+j)
            if neighbour in data:
                neighbour_map[neighbour] -= 1
                if neighbour_map [neighbour] < 4:
                    to_check.append(neighbour)
    return len(checked)

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