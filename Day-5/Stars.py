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
    ranges = []
    foods = []
    getting_ranges = True
    for row in raw.splitlines():
        if row == '':
            getting_ranges = False
            continue
        if getting_ranges:
            ranges.append((int(row.split('-')[0]),int(row.split('-')[1])))
        else:
            foods.append(int(row))
    return (ranges, foods)
    
def star1(data):
    ranges, foods = data
    fresh = 0
    for food in foods:
        for r in ranges:
            if food in range(r[0], r[1]+1):
                fresh += 1
                break
    return fresh

def star2(data):
    ranges, food = data
    valid_foods = 0
    ranges = simplify_ranges(ranges)
    for r in ranges:
        valid_foods += r[1]-r[0]+1
    return valid_foods

def simplify_ranges(ranges):
    new_ranges = [ranges[0]]
    for (a,b) in ranges[1:]:
        temp = []
        for (c,d) in new_ranges:
            if a <= c and c <= b and b <= d: # a c b d
                temp.append((a, d))
            elif a <= c and c <= b and d <= b: # a c d b
                temp.append((a, b))
            elif c <= a and a <= d and d <= b: # c a d b
                temp.append((c, b))
            elif c <= a and a <= d and b <= d: # c a b d
                temp.append((c, d))
            else: # No intersection, add both ranges
                if (c,d) not in temp:
                    temp.append((c,d))
                if (a,b) not in temp:
                    temp.append((a,b))
            new_ranges = temp
        print(new_ranges)
    return new_ranges



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