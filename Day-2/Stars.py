import os, platform
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import Counter, deque
from tqdm import tqdm

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
        data = [(int(r.split('-')[0]), int(r.split('-')[1])) for r in row.split(',')]
    return data
    
def star1(data: list[(int,int)]) -> int:
    count:int = 0
    for start, end in data:
        for i in range(start,end+1):
            if len(str(i))%2 == 1:
                continue
            count += i if not valid_id(i) else 0
    return count

def valid_id(cur_id:int, splits = 2) -> bool:
    s = str(cur_id)
    length = len(s)
    split_size = length//splits
    if length < 2:
        return True
    parts = set(s[i*split_size:(i+1)*split_size] for i in range(splits))
    if len(parts) == 1:
        return False
    return True

def divisiors(n: int) -> list[int]:
    options: list[int] = []
    for i in range(2,n+1):
        if n%i == 0:
            options.append(i)
    return options

def star2(data):
    count:int = 0
    for start, end in tqdm(data):
        for i in range(start,end+1):
            factors = divisiors(len(str(i)))
            isValid = True
            for factor in factors:
                if not valid_id(i, factor):
                    count += i
                    break
    return count

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