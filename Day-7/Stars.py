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
    data:dict[(int,int):str] = {}
    start_info = []
    for j, row in enumerate(raw.splitlines()):
        for i, char in enumerate(row):
            if char == '.':
                continue
            if char == 'S':
                start_info = ((i,j), len(raw.splitlines())) # Store start pos and height
                continue
            data[(i,j)] = char
    return (data, start_info)
    
def star1(data):
    return simulate_beam(data, return_splits=True)

def star2(data):
    return simulate_beam(data, return_splits=False)

def simulate_beam(data, return_splits = False) -> int:
    splits = 0
    data, (start_pos, height) = data[0], data[1] # Get start pos
    beams:dict[(int,int):int] = defaultdict(int) # Keep track of beams and timelines
    beams[start_pos]+= 1

    for j in range(height):
        new_beams = defaultdict(int)
        for pos, timelines in beams.items():
            pos = (pos[0], pos[1]+1)
            if pos in data: # Split
                new_beams[(pos[0]-1,pos[1])] += timelines
                new_beams[(pos[0]+1,pos[1])] += timelines
                splits += 1
            else:
                new_beams[pos] += timelines

        beams = new_beams
    if return_splits:
        return splits
    return sum([timelines for timelines in beams.values()])

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