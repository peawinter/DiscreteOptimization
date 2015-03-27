#!/usr/bin/python
# -*- coding: utf-8 -*-
from collections import defaultdict
from collections import Counter
from random import shuffle
from random import choice
from time import time
from math import exp
from collections import deque
import random

class Solution():
    def edgeToLst(self, edges):
        self.lst = defaultdict(set)
        for (node0, node1) in edges:
            self.lst[node0].add(node1)
            self.lst[node1].add(node0)
        self.node_sorted = sorted(self.lst, key = lambda k: len(self.lst[k]), reverse=True)
    
    # Welsh Powell Algorithm
    def greedyWP(self):
        color_dict = dict()
        color_index = 0
        while len(color_dict) < len(self.lst):
            # find the largest uncolor 
            neighbor = set()
            for node in self.node_sorted:
                if node not in neighbor and node not in color_dict:
                    color_dict[node] = color_index
                    neighbor = neighbor | self.lst[node]
            color_index += 1
        sol = [value for (key, value) in sorted(color_dict.items())]
        return (sol, max(sol) + 1)
    
    # basic greedy algorithm
    def greedyBC(self):
        visited = [self.node_sorted[0]]
        color_set = set(range(len(self.lst)))
        color_dict = {}
        color_dict[self.node_sorted[0]] = 0
        for node in self.node_sorted[1:]:
            visited.append(node)
            taken = set([color_dict[n] for n in self.lst[node] if n in visited])
            color_dict[node] = min(color_set - taken)
        sol = [value for (key, value) in sorted(color_dict.items())]
        return (sol, max(sol) + 1)
    
    # iterated greedy reorder sequence
    def greedReorder(self, sol):
        level = range(max(sol) + 1)
        shuffle(level)
        disturb_node = range(len(sol))
        shuffle(disturb_node)
        sol = [level[idx] for idx in sol]
        self.node_sorted = [x for (z, y, x) in sorted(zip(sol, disturb_node, range(len(sol))), reverse = True)]
    
    # iterated greedy algorithm
    def greedyIte(self):
        for idx in range(100):
            (sol, cnt) = self.greedyBC()
            self.greedReorder(sol)
        return (sol, cnt)
    
    ##############
    # backtrack
    def isValidBT(self, node, color):
        for n in self.lst[node]:
            if n != node and self.bt_sol[n] == color:
                return False
        return True
    
    def backTrackHelper(self, node):
        if node == len(self.lst):
            return True
        for color in range(100):
            self.bt_sol[node] = color
            if self.isValidBT(node, color):
                if self.backTrackHelper(node + 1):
                    return True
            self.bt_sol[node] = -1
        return False
        
    def backTrack(self):
        self.bt_sol = [-1] * len(self.lst)
        self.backTrackHelper(0)
        return (self.bt_sol, max(self.bt_sol) + 1)
    # end of backtrack
    ################
    
    ################
    # tabu searching
    def isConflict(self, sol, node):
        for n in self.lst[node]:
            if n != node and sol[n] == sol[node]:
                return True
        return False
    
    def conflictLst(self, sol):
        node_conflict = []
        for node in range(len(self.lst)):
            if self.isConflict(sol, node):
                node_conflict.append(node)
        return node_conflict
    
    def isValidTB(self, sol):
        if self.conflictLst(sol):
            return False
        return True
    
    def tabu(self):
        # step 0, count time
        ptime = time()
        # step 1, generate a valid input
        (sol, cnt) = self.greedyBC()
        
        neighbor_sol = []
        neighbor_sol_best = []
        neighbor_confLst = []
        neighbor_confLst_best = []
        
        for macroIte in range(100):
            # step 2.0, Iterated Greedy
            for idx in range(50):
                self.greedReorder(sol)
                (sol, cnt) = self.greedyBC()
            
            # step 2.1, decrease color 
            tb_cnt = cnt - 1
            tb_sol = []
            tb_sol[:] = sol
            for idx, col in enumerate(tb_sol):
                if col == tb_cnt:
                    tb_sol[idx] = choice(range(tb_cnt))
            
            tabu_moves = deque(maxlen = 20)
            print macroIte, cnt
            # step 3, find best neighbor
            for ite in range(100):
                tb_confLst = self.conflictLst(tb_sol)
                if not tb_confLst:
                    sol[:] = tb_sol
                    cnt = tb_cnt
                    break
                neighbor_confLst_best[:] = tb_confLst
                # step 3.1, generate new neighbors
                for idx in range(len(tb_confLst)):
                    neighbor_sol[:] = tb_sol
                    new_move = (choice(tb_confLst), choice(range(tb_cnt)))
                    while new_move in tabu_moves:
                        new_move = (choice(tb_confLst), choice(range(tb_cnt)))
                    tabu = (new_move[0], neighbor_sol[new_move[0]])
                    neighbor_sol[new_move[0]] = new_move[1]
                    neighbor_confLst = self.conflictLst(neighbor_sol)
                    if len(neighbor_confLst) <= len(neighbor_confLst_best):
                        neighbor_confLst_best[:] = neighbor_confLst
                        neighbor_sol_best[:] = neighbor_sol
                        tabu_best = tabu
                    if not neighbor_confLst:
                        break
                tb_sol[:] = neighbor_sol_best
                tb_cnt = max(tb_sol) + 1
                tabu_moves.append(tabu_best)
            print macroIte, cnt
        return (sol, cnt)
    
    
    
    ###################
    # simulated annealing strategy
    def costFun(self, sol):
        C = Counter()
        E = Counter()
        for node, col in enumerate(sol):
            C[col] += 1
            for neighbor in self.lst[node]:
                if sol[neighbor] == col:
                    E[col] += 1
        cost1 = 0
        cost2 = 0
        for col in C:
            cost1 += - C[col] ** 2 + C[col] * E[col]
            cost2 += E[col]
        return (cost1, cost2, len(C))
    
    def AccRate(self, cost1, new_cost1):
        self.T *= 0.99995
        return exp((cost1 - new_cost1) / self.T)
    
    def SA(self):
        # step 1, generate a valid input
        (best_sol, best_cnt) = self.greedyBC()
        # step 2, iterated greedy to improve the result
        for idx in range(50):
            self.greedReorder(best_sol)
            (best_sol, best_cnt) = self.greedyBC()
        
        (best_cost1, best_cost2, best_cnt) = self.costFun(best_sol)
        # step 3, simulated annealing
        # for idx in range(1000):
        curr_sol = []
        next_sol = []
        for macIte in range(10):
            self.T = 10
            curr_sol[:] = best_sol
            curr_cnt = best_cnt
            curr_cost1 = best_cost1
            curr_cost2 = best_cost2
            for ite in range(80000):
                next_sol[:] = curr_sol
                next_sol[choice(range(len(next_sol)))] = choice(range(curr_cnt))
                (next_cost1, next_cost2, next_cnt) = self.costFun(next_sol)
                print ite, curr_cost1, next_cost1
                if self.AccRate(curr_cost1, next_cost1) > random.random():
                    curr_sol[:] = next_sol
                    curr_cnt = next_cnt
                    curr_cost1 = next_cost1
                    curr_cost2 = next_cost2
                if curr_cost2 == 0 and curr_cnt < best_cnt:
                    best_sol[:] = curr_sol
                    best_cnt = curr_cnt
                    best_cost1 = curr_cost1
                    best_cost2 = curr_cost2
        print best_cnt
        return (best_sol, best_cnt)
        
    # main function
    def colorGraph(self, node_count, edge_count, edges):
        self.edgeToLst(edges)
        return self.SA()
    
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
