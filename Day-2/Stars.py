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

    # ans2 = star2(data)
    ans2 = star2_alternative(data)
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
    ids = []
    for row in raw.splitlines():
        for r in row.split(','):
            start, end = int(r.split('-')[0]), int(r.split('-')[1])+1
            for cur_id in range(start, end):
                ids.append(str(cur_id))
    print(max(len(x) for x in ids)) # Max length is 10
    return ids
    
def star1(data: list[str]) -> int:
    count:int = 0
    for cur_id in data:
        if len(cur_id)%2 == 1: # We only consider even id's to have repeats
            continue
        count += 0 if valid_id(cur_id) else int(cur_id)
    return count

def valid_id(cur_id:str, splits: list[int] = [2]) -> bool:
    """
    Takes an id and checks for repeats in all splitting sizes in 'spltis'
    This function assumes that cur_id can be split evenly into all splitting sizes in 'splits'
    """
    length:int = len(cur_id)
    if length < 2: # Can't have duplicates, so it's valid
        return True
    for split in splits:
        split_size:int = length//split
        parts = set(cur_id[i*split_size:(i+1)*split_size] for i in range(split)) # Spltis string into split sized pieces
        if len(parts) == 1:
            return False
    return True # If it now splitting creates repeats then it is valid

def find_divisiors(n: int) -> list[int]:
    return [i for i in range(2, n+1) if n%i == 0]

def star2(data: list[str]) -> str:
    count:int = 0
    for cur_id in tqdm(data):
        divisors = find_divisiors(len(cur_id))
        count += 0 if valid_id(cur_id, divisors) else int(cur_id)
    return count

def star2_alternative(data: list[str]) -> str:
    count:int = 0
    possible_divisors = possible_repeating_divisors()
    for cur_id in tqdm(data):
        for divisor in possible_divisors[len(cur_id)]:
            if int(cur_id)%divisor == 0:
                count += int(cur_id)
                break
    return count


def possible_repeating_divisors() -> dict[int:list[int]]:
    possible_divisors:dict[int:list[int]] =  {}
    for i in range(1,11): # Biggest number is 10 digits
        possible_divisors[i] = [] # Need to create for 1, some ints are length 1
    for i in range(2,11): # Biggest number is 10 digits
        possible_divisors[i].append(int('1'*i))
        if i > 2 and i%2 == 0:
            possible_divisors[i].append(int('01'*(i//2)))
        if i > 3 and i%3 == 0:
            possible_divisors[i].append(int('001'*(i//3)))
        if i > 4 and i%4 == 0:
            possible_divisors[i].append(int('0001'*(i//3)))
        if i > 5 and i%5 == 0:
            possible_divisors[i].append(int('00001'*(i//5)))
    return possible_divisors

def main():
    import cProfile
    import pstats
    with cProfile.Profile() as pr:
        day_()
    
    stats = pstats.Stats(pr)
    stats.sort_stats(pstats.SortKey.TIME)
    if platform.system() == "Linux":
        day = int(__file__.split('/')[-2].split('-')[1].split('.')[0])
    else:
        day = int(__file__.split('\\')[-2].split('-')[1].split('.')[0])
    stats.dump_stats(filename = f'profiling{day}.prof')

if __name__ == '__main__':
    main()