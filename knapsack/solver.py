#!/usr/bin/python
# -*- coding: utf-8 -*-
import copy
from collections import namedtuple
Item = namedtuple("Item", ['index', 'value', 'weight'])

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
    
    itemDict = {}
    for item in items:
        itemDict[item] = item.value / float(item.weight)
    itemStack = sorted(itemDict, key = itemDict.__getitem__, reverse = True)
    
    valueTrack = {0: 0}
    takenTrack = {0: []}
    
    slope = 0
    
    for item in itemStack:
        new_valueTrack = {}
        new_takenTrack = {}
        if itemDict[item] <= slope:
            break
        for w in valueTrack:
            new_valueTrack[w] = valueTrack[w]
            new_takenTrack[w] = takenTrack[w]
            new_w = w + item.weight
            if new_w <= capacity and (not new_w in new_valueTrack or new_valueTrack[new_w] < valueTrack[w] + item.value): 
                new_valueTrack[new_w] = valueTrack[w] + item.value
                new_takenTrack[new_w] = takenTrack[w] + [item.index]
        # clean new_valueTrack and new_takenTrack
        threshold = -1
        for w in sorted(new_valueTrack):
            if new_valueTrack[w] > threshold:
                threshold = new_valueTrack[w]
            else:
                del new_valueTrack[w]
                del new_takenTrack[w]
        valueTrack = copy.deepcopy(new_valueTrack)
        takenTrack = copy.deepcopy(new_takenTrack)
        if max(valueTrack) == capacity:
            second_w = sorted(valueTrack)[-2]
            slope = (valueTrack[capacity] - valueTrack[second_w]) / float(capacity - second_w)
    
    value = valueTrack[max(valueTrack)]
    taken = [0] * len(items)
    for i in takenTrack[max(takenTrack)]:
        taken[i] = 1
    
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

