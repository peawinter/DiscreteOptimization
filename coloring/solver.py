#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict

class Solution():
    def edgeToLst(self, edges):
        lst = defaultdict(set)
        for (node0, node1) in edges:
            lst[node0].add(node1)
            lst[node1].add(node0)
        node_sorted = sorted(lst, key = lambda k: len(lst[k]), reverse=True)
        return (lst, node_sorted)
    
    def greedyCG_helper(self, lst, node_sorted):
        color_dict = dict()
        color_index = 0
        while len(color_dict) < len(lst):
            # find the largest uncolor 
            neighbor = set()
            for node in node_sorted:
                if node not in neighbor and node not in color_dict:
                    color_dict[node] = color_index
                    neighbor = neighbor | lst[node]
            color_index += 1
        solution = [value for (key, value) in sorted(color_dict.items())]
        return (solution, color_index + 1)
    
    def greedyCG_
    
    def greedyCG(self, node_count, edge_count, edges):
        (lst, node_sorted) = self.edgeToLst(edges)
        return self.greedyCG_helper(lst, node_sorted)
        
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
        
    ## my code
    
    sol = Solution()
    (solution, color_count) = sol.greedyCG(node_count, edge_count, edges)
    
    # end of my code
    
    # prepare the solution in the specified output format
    output_data = str(color_count) + ' ' + str(0) + '\n'
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
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)'

