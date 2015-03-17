#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
import sys
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

class Solution():

    def solverBB_helper(self, layer, curr_taken, curr_weight, curr_value):
        self.flag -= 1
        if self.flag <= 0 or layer == len(self.items) or curr_weight + self.min_weights[layer] > self.capacity:
            return (curr_value, curr_taken)
        currentUpperBound = curr_value + self.items[layer].value * (self.capacity - curr_weight) / float(self.items[layer].weight)
        if currentUpperBound < self.gloBound:
            return (curr_value, curr_taken)
        if self.items[layer].weight + curr_weight > self.capacity:
            return self.solverBB_helper(layer + 1, curr_taken, curr_weight, curr_value)
        (right_value, right_taken) = self.solverBB_helper(layer + 1, curr_taken + [self.items[layer].index], curr_weight + self.items[layer].weight, curr_value + self.items[layer].value)
        self.gloBound = max(self.gloBound, right_value)
        (left_value, left_taken) = self.solverBB_helper(layer + 1, curr_taken, curr_weight, curr_value)
        self.gloBound = max(self.gloBound, left_value)
        if left_value > right_value:
            return (left_value, left_taken)
        return (right_value, right_taken)
        
    def solverBB(self, items, capacity):
        items = sorted(items, key=lambda x: x.value / float(x.weight), reverse = True)
        self.min_weight = 0
        self.items = items
        self.capacity = capacity
        loBound = 0
        loBoundWeight = 0
        tak = []
        for item in items:
            if loBoundWeight + item.weight <= capacity:
                loBound += item.value
                loBoundWeight += item.weight
                tak.append(item.index)
        min_weights = [items[-1].weight] * len(items)
        for idx in range(len(items) - 2, -1, -1):
            min_weights[idx] = min(items[idx], min_weights[idx + 1])
        self.min_weights = min_weights
        self.gloBound = loBound
        self.flag = 10 ** 20
        (value, tak) = self.solverBB_helper(0, [], 0, 0)
    
        taken = [0] * len(items)
        for i in tak:
            taken[i] = 1
    
        return (value, taken)

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0])
    capacity = int(firstLine[1])
    
    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    ## My code
    
    # sys.setrecursionlimit(len(items) + 1000)
    
    sol = Solution()
    (value, taken) = sol.solverBB(items, capacity)
    
    ## End of my code
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, taken))
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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

