import os, platform
import sys
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import Counter, deque
from heapq import heapify, heappush, heappop

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
    machines = []
    for row in raw.splitlines():
        machine = [0, [], 0]
        size = 0
        for i, part in enumerate(row.split(' ')):
            if i == 0:
                goal = part.strip('[]')
                goal = [0 if char =='.' else 1 for char in goal]
                machine[0] = goal
                size = len(goal)
                continue
            if i == len(row.split(' '))-1:
                joltage = part.strip('{}')
                joltage = [int(char) for char in joltage.split(',')]
                machine[2] = joltage
                continue
            bits = part.strip('()')
            # instruction = ['0']*size
            # for char in bits.split(','):
            #     toggle_str(instruction, int(char))
            machine[1].append([int(char) for char in bits.split(',')])
        machines.append(machine)
    return machines

def toggle_str(instruction:list[str], index):
    instruction[index] = str((int(instruction[index]) + 1)%2)
def toggle(instruction:list[int], index):
    instruction[index] = (instruction[index] + 1)%2
    
def star1(data):
    total = 0
    for machine in data:
        goal = machine[0]
        total += search_for_goal(goal, machine[1], operation=perform_instruction)
        print(total)
    return total

def search_for_goal(goal:list[int], instructions:list[int], operation):
    goal = tuple(goal)
    to_search = []
    start = (0, tuple([0]*len(goal)))
    heappush(to_search, start)
    searched = set()
    while len(to_search) > 0:
        flips, current = heappop(to_search)

        if current in searched:
            continue
        searched.add(current)
        
        if current == goal:
            return flips

        for instruction in instructions:
            next_state = operation(current, instruction)
            heappush(to_search, (flips+1, next_state))

def perform_instruction(state:tuple, instruction:list[int]):
    next_state = list(state)
    for bit in instruction:
        toggle(next_state, bit)
    return tuple(next_state)


def star2(data):
    total = 0
    for machine in data:
        goal = machine[2]
        total += search_for_goal(goal, machine[1], operation = add)
        print(total)
    return total

def add(state:tuple, instruction: list[int]):
    next_state = list(state)
    for bit in instruction:
        next_state[bit] += 1
    return tuple(next_state)


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