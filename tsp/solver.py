#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import copy
import random
import operator
import itertools
import numpy as np
from collections import namedtuple
from collections import defaultdict

Point = namedtuple("Point", ['x', 'y'])

def length(c1, c2):
    return math.sqrt(((c1.x - c2.x) ** 2) + ((c1.y - c2.y) ** 2))

def myDistMat(cities):
    dm = [[length(x, y) for y in cities] for x in cities]
    dm = np.array(dm)
    return dm

def random_permutation(cities):
    perm = range(len(cities))
    random.shuffle(perm)
    return perm

def augmented_cost(permutation, penalties, cities, l):
    distance, augmented = 0, 0
    limit = len(permutation)

    for i in range(limit):
        c1, c2 = permutation[i - 1], permutation[i]

        d = length(cities[c1], cities[c2])
        distance += d
        augmented += d + (l * penalties[c1][c2])

    return [distance, augmented]

def cost(cand, penalties, cities, l):
    cost, acost = augmented_cost(cand["vector"], penalties, cities, l)
    cand["cost"], cand["aug_cost"] = cost, acost

def local_search(nodeCount, current, cities, penalties, max_no_improv, l, dm):
    count  = 0
    cost(current, penalties, cities, l)

    # begin-until hack
    while True:
        # propose new solution
        
        [idx1, idx2] = sorted(random.sample(range(nodeCount), 2))

        i0, j0 = current["vector"][idx1 - 1], current["vector"][idx1]
        i1, j1 = current["vector"][idx2 - 1], current["vector"][idx2]
        gain = dm[i0, j0] + dm[i1, j1] + (penalties[i0, j0] + penalties[i1, j1]) * l
        loss = dm[i0, i1] + dm[j0, j1] + (penalties[i0, i1] + penalties[j0, j1]) * l
        if gain > loss:
            curr_sol = current["vector"]
            candidate = {}
            candidate["vector"] = curr_sol[:idx1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx2:]
            current = candidate
        else:
            count += 1

        if count >= max_no_improv:
            cost(current, penalties, cities, l)
            return current

def update_penalties(nodeCount, penalties, cities, permutation):
    
    utilities = np.zeros(nodeCount)

    for i in range(nodeCount):
        c1, c2 = permutation[i - 1], permutation[i]

        utilities[i] = length(cities[c1], cities[c2]) / (1 + penalties[c1][c2])
    
    maxIdx = np.argmax(utilities)
    c1, c2 = permutation[maxIdx - 1], permutation[maxIdx]
    penalties[c1][c2] += 1
    penalties[c2][c1] += 1
    return penalties
    
def search(nodeCount, cities):
    
    max_iterations = nodeCount * 10
    max_no_improv = nodeCount * 20
    alpha = 0.3
    l = 0
    
    dm = myDistMat(cities)
    
    current = {}
    current["vector"] = random_permutation(cities)
    best = None
    penalties = np.zeros((nodeCount, nodeCount))

    for i in range(max_iterations):
        current = local_search(nodeCount, current, cities, penalties, max_no_improv, l, dm)
        update_penalties(nodeCount, penalties, cities, current["vector"])

        if best is None or current["cost"] < best["cost"]:
            best = current
            l = alpha * (best["cost"] / len(cities))

        print("Iteration #" + str(i + 1) + ", best = " + str(best["cost"]) + ", aug = " + str(best["aug_cost"]))

    return (best["vector"], best["cost"])

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    nodeCount = int(lines[0])

    points = []
    for i in range(1, nodeCount+1):
        line = lines[i]
        parts = line.split()
        points.append(Point(float(parts[0]), float(parts[1])))

    # build a trivial solution
    # visit the nodes in the order they appear in the file
    (solution, obj) = search(nodeCount, points)

    # prepare the solution in the specified output format
    output_data = str(obj) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))

    return output_data


import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/tsp_51_1)'

