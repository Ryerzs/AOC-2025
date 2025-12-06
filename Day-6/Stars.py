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

    ans2 = star2(raw_data)
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
    data = defaultdict(list)
    for row in raw.splitlines():
        if '+' in row or '*' in row: #Last row
            operators = [operator for operator in row.strip().split(' ') if operator != '']
            for i, operator in enumerate(operators):
                data[i].append(operator)
            continue
        numbers = [int(number) for number in row.strip().split(' ') if number != '']# Remove leading spaces
        for i, number in enumerate(numbers):
            data[i].append(number)
    return data
    
def star1(data):
    total = 0
    for row in data.values():
        operator = row[-1]
        if operator == '+':
            count = 0
        else:
            count = 1
        for number in row[:-1]:
            if operator == '+':
                count += number
            else:
                count *= number
        total += count
    return total

def star2(raw):
    height = len(raw.splitlines())
    width = max([len(raw.splitlines()[i]) for i in range(height)])
    new_column = False
    total = 0
    numbers = []
    for i in range(width):
        number = []
        if new_column:
            new_column = False
            continue
        for j, row in enumerate(raw.splitlines()):
            if len(row) <= width-1-i:
                if j != height-1:
                    number.append('0')
                continue
            char = row[width-1-i]
            if char == '+'  or char == '*': #Last row
                new_column = True
                continue
            if char == '' and j != height-1:
                number.append('0')
            else:
                number.append(char)
        numbers.append(int(''.join(number)))
        if new_column == False:
            continue
        if char == '+':
            operator = (lambda x,y:x+y)
            count = 0
        if char == '*':
            operator = (lambda x,y:x*y)
            count = 1
        print(numbers)
        for number in numbers:
            count = operator(count, number)
        total += count
        numbers = []
    return total

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