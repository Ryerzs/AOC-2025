import os, platform
import sys; sys.setrecursionlimit(100000)
import time
from aocd import submit
from aocd.models import Puzzle
import itertools
import functools
from collections import Counter, deque, defaultdict
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
    data = []
    for row in raw.splitlines():
        pos = tuple(int(number) for number in row.split(','))
        data.append(pos)
    return data


def print_network(network) -> None:
    for pos, connections in network.items():
        print(pos, connections)

def star1(data):
    network = defaultdict(set)
    to_connect = []
    heapify(to_connect)
    for i, pos in enumerate(data):
        for pos2 in data:
            if pos == pos2:
                continue
            distance = distance_squared(pos, pos2)
            heappush(to_connect, tuple((distance, (pos, pos2))))

    connections = 0
    searched = set()
    while len(to_connect) > 0:
        if connections == 10:
            break
        distance, (pos1, pos2) = heappop(to_connect)
        if (pos1, pos2) in searched or (pos2, pos1) in searched:
            continue
        add_to_network(network, pos1,pos2)
        # if connections == 10:
        #     print_network(network)
        searched.add(tuple((pos1,pos2)))
        searched.add(tuple((pos2,pos1)))
        connections += 1
    
    # print_network(network)
    checked = set()
    sizes = []
    for pos in data:
        if pos in checked:
            continue
        count = 0
        to_search = deque([pos])
        while len(to_search) > 0:
            current = to_search.pop()
            if current in checked:
                continue
            checked.add(current)
            count += 1
            for connection in network[current]:
                to_search.append(connection)
        sizes.append(count)
    sizes = sorted(sizes, key=lambda x: -x)
    return sizes[0]*sizes[1]*sizes[2]

def add_to_network(network, pos1, pos2):
    network[pos1].add(pos2)
    network[pos2].add(pos1)


def distance_squared(pos1, pos2) -> int:
    return sum((coord1-coord2)**2 for coord1,coord2 in zip(pos1,pos2))


def star2(data):
    network = defaultdict(set)
    to_connect = []
    heapify(to_connect)
    for i, pos in enumerate(data):
        for pos2 in data:
            if pos == pos2:
                continue
            distance = distance_squared(pos, pos2)
            heappush(to_connect, tuple((distance, (pos, pos2))))

    connections = 0
    searched = set()
    last_added = None
    length = len(to_connect)
    i = 0
    while len(to_connect) > 0:
        # if connections == 10:
        #     break
        distance, (pos1, pos2) = heappop(to_connect)
        if (pos1, pos2) in searched or (pos2, pos1) in searched:
            continue
        last_added = (pos1, pos2)
        add_to_network_recurse(network, pos1,pos2)
        # if connections == 12:
        #     print_network(network)
        searched.add(tuple((pos1,pos2)))
        searched.add(tuple((pos2,pos1)))
        connections += 1
        if len(network[pos1]) == len(data)-1:
            # print(connections)
            print_network(network)
            break
        print(i*100/length)
        i += 1
    
    print(last_added)
    return last_added[0][0]*last_added[1][0]

def add_to_network_recurse(network, pos1, pos2) -> None:
    added = set()
    connection = (pos1,pos2)
    to_add = deque()
    to_add.append(connection)
    # print(to_add)
    while len(to_add) > 0:
        [current1, current2] = to_add.pop()
        # print(current1)
        # print(current2)
        if (current1,current2) in added:
            continue
        if current1 == current2:
            continue
        if current1 in network:
            network[current1].add(current2)
        else:
            network[current2].add(current1)
        added.add(tuple([current1,current2]))
        added.add(tuple([current2,current1]))
        for connection in network[current1]:
            to_add.append(tuple((current2,connection)))
        for connection in network[current2]:
            to_add.append(tuple((current1,connection)))




    to_add = deque()
    if pos1 in network[pos2]:
        return
    network[pos1].add(pos2)
    network[pos2].add(pos1)
    to_add = list(network[pos2])
    for connection in to_add:
        if connection == pos1:
            continue
        add_to_network_recurse(network,pos1,connection)
    to_add = list(network[pos1])
    for connection in to_add:
        if connection == pos2:
            continue
        add_to_network_recurse(network,pos2,connection)

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