#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
from random import shuffle
from random import choice
import random

class Solution():
    def edgeToLst(self, edges):
        lst = defaultdict(set)
        for (node0, node1) in edges:
            lst[node0].add(node1)
            lst[node1].add(node0)
        node_sorted = sorted(lst, key = lambda k: len(lst[k]), reverse=True)
        return (lst, node_sorted)
    
    # Welsh Powell Algorithm
    def greedyWP(self, lst, node_sorted):
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
    
    # basic greedy algorithm
    def greedyBasic(self, lst, node_seq):
        n = len(node_seq)
        visited = [node_seq[0]]
        unvisited = node_seq[1:]
        color_set = set(range(n))
        color_dict = {}
        color_dict[node_seq[0]] = 0
        for nextNode in node_seq[1:]:
            visited.append(nextNode)
            taken = set([color_dict[node] for node in lst[nextNode] if node in visited])
            color_dict[nextNode] = min(color_set - taken)
        solution = [value for (key, value) in sorted(color_dict.items())]
        return (solution, max(solution) + 1)
    
    # iterated greedy reorder sequence
    def greedReorder(self, solution, idx):
        level = range(max(solution) + 1)
        shuffle(level)
        disturb_node = range(len(solution))
        shuffle(disturb_node)
        new_solution = [level[idx] for idx in solution]
        node_lst = [x for (z, y, x) in sorted(zip(new_solution, disturb_node, range(len(solution))), reverse = True)]
        # print [solution[idx] for idx in node_lst]
        return node_lst
    
    # iterated greedy algorithm
    def greedyIte(self, lst, node_sorted):
        best_count = len(lst)
        for idx in range(100):
            (current_solution, current_count) = self.greedyBasic(lst, node_sorted)
            node_sorted = self.greedReorder(current_solution, idx)
            print current_count
            if best_count > current_count:
                best_solution = current_solution
                best_count = current_count
        return (best_solution, best_count)
    
    # backtrack
    def isValidBT(self, nodeIdx, colorIdx):
        for node in self.lst[nodeIdx]:
            if node != nodeIdx and self.btsol[node] == colorIdx:
                return False
        return True
    
    def backTrackHelper(self, nodeIdx):
        if nodeIdx == len(self.lst):
            return True
        for colorIdx in range(self.upbound):
            self.btsol[nodeIdx] = colorIdx
            print self.btsol
            if self.isValidBT(nodeIdx, colorIdx):
                print nodeIdx + 1
                if self.backTrackHelper(nodeIdx + 1):
                    return True
            self.btsol[nodeIdx] = -1
        return False
        
    def backTrack(self, lst, node_sorted):
        self.btsol = [-1] * len(lst)
        self.upbound = 17
        self.lst = lst
        self.backTrackHelper(0)
        return (self.btsol, max(self.btsol) + 1)
    
    # tabu searching
    def isConflict(self, solution, nodeIdx):
        for node in self.lst[nodeIdx]:
            if node != nodeIdx and solution[node] == solution[nodeIdx]:
                return True
        return False
    
    def conflictLst(self, solution):
        node_conflict = []
        for nodeIdx in range(len(self.lst)):
            if self.isConflict(solution, nodeIdx):
                node_conflict.append(nodeIdx)
        return node_conflict
    
    def isValidTB(self, solution):
        if self.conflictLst(solution):
            return False
        return True
    
    def tabu(self, lst, node_sorted):
        self.lst = lst
        # step 1, generate a valid input
        (sol, cnt) = self.greedyBasic(lst, node_sorted)
        
        neighbor_sol = []
        neighbor_sol_best = []
        neighbor_confLst = []
        neighbor_confLst_best = []
        
        for layer in range(50):
            # step 2.0, Iterated Greedy
            for idx in range(100):
                node_sorted = self.greedReorder(sol, idx)
                (sol, cnt) = self.greedyBasic(lst, node_sorted)
            
            print layer, cnt
            
            # step 2, decrease color 
            tb_cnt = cnt - 1
            tb_sol = []
            
            for col in sol:
                if col == tb_cnt:
                    tb_sol.append(choice(range(tb_cnt)))
                else:
                    tb_sol.append(col)
            # step 3, find best neighbor
            for ite in range(10 * (layer + 1)):
                tb_confLst = self.conflictLst(tb_sol)
                if not tb_confLst:
                    sol[:] = tb_sol
                    cnt = max(sol) + 1
                    break
                neighbor_confLst_best[:] = tb_confLst
                # step 3.1, generate new neighbors
                for idx in range(len(tb_sol) / 4):
                    neighbor_sol[:] = tb_sol
                    neighbor_sol[choice(tb_confLst)] = choice(range(tb_cnt))
                    neighbor_confLst = self.conflictLst(neighbor_sol)
                    if len(neighbor_confLst) <= len(neighbor_confLst_best):
                        neighbor_confLst_best[:] = neighbor_confLst
                        neighbor_sol_best[:] = neighbor_sol
                    if not neighbor_confLst:
                        break
                tb_sol[:] = neighbor_sol_best
                tb_cnt = max(tb_sol) + 1
            print layer, cnt
        return (sol, cnt)
    
    # main function
    def colorGraph(self, node_count, edge_count, edges):
        (lst, node_sorted) = self.edgeToLst(edges)
        return self.tabu(lst, node_sorted)
    
    # def degree(self, lst):
    #     for key, val in lst.iteritems():
    #         print key, val
    
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
    (solution, color_count) = sol.colorGraph(node_count, edge_count, edges)
    
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

# Leader Board
# gc1  gc2  gc3  gc4  gc5  gc6 
#   6   17   15   73   12   88  --- 2015 session (per March 16th) 
#   6   17   15   74   12   86  --- 2014 session 
#   6   17   15   73   13   86  --- 2013 session 
