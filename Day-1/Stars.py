import os
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import Counter, deque

def day_():
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
        rotation = int(row[1:])
        data.append(-rotation if row[0] == 'L' else rotation)
    return data
    
def star1(data):
    count = 0
    dial = 50
    for rotation in data:
        dial = (dial+rotation)%100
        count += dial==0
    return count

def star2(data):
    count = 0
    current_dial = 50
    for rotation in data:
        full_laps = abs(rotation) // 100
        count += full_laps
        direction = 1 if rotation > 0 else -1
        rotation -= 100*direction*full_laps


        new_dial = (current_dial+rotation)%100
        if new_dial == 0:
            count += 1
        elif current_dial != 0 and direction < 0 and new_dial > current_dial:
            count += 1
        elif direction > 0 and new_dial < current_dial:
            count += 1
        
        current_dial = new_dial
    return count


def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    # stats.print_stats()
    day = int(__file__.split('\\')[-2].split('-')[1].split('.')[0])
    stats.dump_stats(filename = f'profiling{day}.prof')

# run with `py day_n.py -- a b` to submit both stars for day n
if __name__ == '__main__':
    main()