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


def euc_2d(c1, c2):

    return math.sqrt(((c1.x - c2.x) ** 2) + ((c1.y - c2.y) ** 2))

def random_permutation(cities):
    perm = range(len(cities))
    random.shuffle(perm)
    return perm

def stochastic_two_opt(permutation):
    perm = copy.copy(permutation)
    
    [c1, c2] = sorted(random.sample(range(len(perm)), 2))
    
    perm_range = perm[c1:c2]
    perm_range.reverse()
    perm[c1:c2] = perm_range

    return perm

def augmented_cost(permutation, penalties, cities, l):
    distance, augmented = 0, 0
    limit = len(permutation)

    for i in range(limit):
        c1, c2 = permutation[i - 1], permutation[i]
        # c1 = permutation[i]
        #
        # if i == (limit - 1):
        #     c2 = permutation[0]
        # else:
        #     c2 = permutation[i + 1]
        #
        # if c2 < c1:
        #     c1, c2 = c2, c1

        d = euc_2d(cities[c1], cities[c2])
        distance += d
        augmented += d + (l * penalties[c1][c2])

    return [distance, augmented]

def cost(cand, penalties, cities, l):
    cost, acost = augmented_cost(cand["vector"], penalties, cities, l)
    cand["cost"], cand["aug_cost"] = cost, acost

def local_search(current, cities, penalties, max_no_improv, l):
    cost(current, penalties, cities, l)
    count  = 0

    # begin-until hack
    while True:
        candidate = {}
        candidate["vector"] = stochastic_two_opt(current["vector"])
        cost(candidate, penalties, cities, l)

        if candidate["aug_cost"] < current["aug_cost"]:
            count = 0
            current = candidate
        else:
            count += 1

        if count >= max_no_improv:
            return current

def calculate_feature_utilities(penal, cities, permutation):
    limit = len(permutation)
    limit_list = range(limit)
    utilities = [0 for i in limit_list]

    for i in limit_list:
        c1, c2 = permutation[i - 1], permutation[i]
        # c1 = permutation[i]
        #
        # if i == (limit - 1):
        #     c2 = permutation[0]
        # else:
        #     c2 = permutation[i + 1]
        #
        # if c2 < c1:
        #     c1, c2 = c2, c1

        utilities[i] = euc_2d(cities[c1], cities[c2]) / (1 + penal[c1][c2])

    return utilities

def update_penalties(penalties, cities, permutation, utilities):
    max_util = max(utilities)
    limit = len(permutation)

    for i in range(limit):
        c1, c2 = permutation[i - 1], permutation[i]
        # c1 = permutation[i]
        #
        # if i == (limit - 1):
        #     c2 = permutation[0]
        # else:
        #     c2 = permutation[i + 1]
        #
        # if c2 < c1:
        #     c1, c2 = c2, c1

        if utilities[i] == max_util:
            penalties[c1][c2] += 1
            penalties[c2][c1] += 1
    return penalties
    
def search(nodeCount, cities):
    
    max_iterations = nodeCount * 15
    max_no_improv = nodeCount * 5
    alpha = 0.3
    
    local_search_optima = 0
    l = alpha * (local_search_optima / len(cities))
    current = {}
    current["vector"] = random_permutation(cities)
    best = None
    cities_count_list = range(len(cities))
    penalties = [[0 for i in cities_count_list] for j in cities_count_list]

    for i in range(max_iterations):
        current = local_search(current, cities, penalties, max_no_improv, l)
        utilities = calculate_feature_utilities(penalties, cities, current["vector"])
        update_penalties(penalties, cities, current["vector"], utilities)

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

