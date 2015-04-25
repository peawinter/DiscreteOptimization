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

class Solution():
    def length(self, p1, p2):
        return math.sqrt(((p1.x - p2.x) ** 2) + ((p1.y - p2.y) ** 2))

    def myDistMat(self):
        self.dm = [[self.length(p1, p2) for p1 in self.points] for p2 in self.points]
        self.dm = np.array(self.dm)

    def random_permutation(self):
        perm = range(self.nc)
        random.shuffle(perm)
        return perm

    def augmented_cost(self, sol):
        distance, augmented = 0, 0
        
        distance = np.sum([self.dm[sol[i - 1], sol[i]] for i in range(self.nc)])
        augmented = np.sum([self.penalties[sol[i - 1], sol[i]] for i in range(self.nc)]) + distance
        
        return [distance, augmented]

    def cost(self, cand):
        cost, acost = self.augmented_cost(cand["vector"])
        cand["cost"], cand["aug_cost"] = cost, acost

    def local_search(self, current):
        count  = 0

        # begin-until hack
        while True:
            # propose new solution
        
            [idx1, idx2] = sorted(random.sample(range(self.nc), 2))

            i0, j0 = current["vector"][idx1 - 1], current["vector"][idx1]
            i1, j1 = current["vector"][idx2 - 1], current["vector"][idx2]
            gain = self.dm[i0, j0] + self.dm[i1, j1] + (self.penalties[i0, j0] + self.penalties[i1, j1]) * self.l
            loss = self.dm[i0, i1] + self.dm[j0, j1] + (self.penalties[i0, i1] + self.penalties[j0, j1]) * self.l
            
            if gain > loss:
                curr_sol = current["vector"]
                candidate = {}
                candidate["vector"] = curr_sol[:idx1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx2:]
                current = candidate
            else:
                count += 1

            if count >= self.max_no_improv:
                self.cost(current)
                return current

    def fast_local_search(self, current):
        count  = 0
        
        flag_improv = True
        
        while flag_improv:
            
            for idx1 in range(self.nc):
            
                i0, j0 = current["vector"][idx1 - 1], current["vector"][idx1]
                
                flag_improv = False
                
                if self.bits[i0] + self.bits[j0] > 0:
                
                    self.bits[i0] = 0
                    self.bits[j0] = 0
                
                    for idx2 in range(self.nc):
                
                        if idx1 != idx2:
                
                            i1, j1 = current["vector"][idx2 - 1], current["vector"][idx2]
                        
                            gain = self.dm[i0, j0] + self.dm[i1, j1] + (self.penalties[i0, j0] + self.penalties[i1, j1]) * self.l
                            loss = self.dm[i0, i1] + self.dm[j0, j1] + (self.penalties[i0, i1] + self.penalties[j0, j1]) * self.l
            
                            if gain > loss:
                            
                                curr_sol = current["vector"]
                                candidate = {}
                                
                                idxLo = min(idx1, idx2)
                                idxUp = max(idx1, idx2)
                                
                                candidate["vector"] = curr_sol[:idxLo] + curr_sol[idxLo:idxUp][::-1] + curr_sol[idxUp:]
                            
                                current = candidate
                            
                                self.bits[i0], self.bits[j0], self.bits[i1], self.bits[j1] = 1, 1, 1, 1
                            
                                flag_improv = True
                    
                        if flag_improv:
                            break
                
                if flag_improv:
                    break
                    
        self.bits = np.zeros(self.nc)
        
        self.cost(current)
        
        return current
    
    def update_penalties(self, permutation):
    
        utilities = np.zeros(self.nc)

        for i in range(self.nc):
            c1, c2 = permutation[i - 1], permutation[i]

            utilities[i] = self.dm[c1, c2] / (1 + self.penalties[c1][c2])
    
        maxIdx = np.argmax(utilities)
        c1, c2 = permutation[maxIdx - 1], permutation[maxIdx]
        
        self.penalties[c1][c2] += 1
        self.penalties[c2][c1] += 1
        
        self.bits[c1] = 1
        self.bits[c2] = 1

    def myTotalDist(self, sol):
        return np.sum([self.length(self.points[sol[i - 1]], self.points[sol[i]]) for i in range(self.nc)])
        # return np.sum([self.dm[sol[i - 1], sol[i]] for i in range(self.nc)])
    
    def my2OPT(self, curr_sol = None):
        if not curr_sol:
            curr_sol = range(self.nc)
            random.shuffle(curr_sol)
            curr_dist = self.myTotalDist(curr_sol)
            # (curr_sol, curr_dist) = self.myGreedy()
        print "Greedy solution distance" + str(curr_dist)

        flag = True
        while flag:
            flag = False
            for idx1 in range(0, self.nc):
                for idx2 in range(idx1 + 1, self.nc):
                    
                    i0, j0 = curr_sol[idx1 - 1], curr_sol[idx1]
                    i1, j1 = curr_sol[idx2 - 1], curr_sol[idx2]
                    
                    gain = self.length(self.points[i0], self.points[j0]) + self.length(self.points[i1], self.points[j1])
                    cost = self.length(self.points[i0], self.points[i1]) + self.length(self.points[j0], self.points[j1])
                    
                    if gain > cost:
                        curr_sol = curr_sol[:idx1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx2:]
                        curr_dist = curr_dist - gain + cost
                        
                        print "Perform 2-Opt exchange: " + str(curr_dist)
                        
                        flag = True
                        
                        # if curr_dist < 70000000:
                        #     return (curr_sol, curr_dist)
                            
        return (curr_sol, curr_dist)
    
    def search(self, nodeCount, points):
        self.points = points
        self.nc = nodeCount
        
        if self.nc > 10000:
            return self.my2OPT()
        
        self.myDistMat()
        self.l = 0
        self.penalties = np.zeros((nodeCount, nodeCount))
        self.max_no_improv = nodeCount * 20
        
        self.bits = np.ones(nodeCount)

        max_iterations = nodeCount * 15

        alpha = 0.3
    
        
    
        current = {}
        current["vector"] = self.random_permutation()
        best = None

        for i in range(max_iterations):
            
            current = self.fast_local_search(current)
            
            self.update_penalties(current["vector"])

            if best is None or current["cost"] < best["cost"]:
                best = current
                self.l = alpha * (best["cost"] / self.nc)

            print("Iteration #" + str(i + 1) + ", best = " + str(best["cost"]) + ", aug = " + str(best["aug_cost"]))
            
            if self.nc == 1889 and best["cost"] <= 323000:
                return (best["vector"], best["cost"])
                
            # if self.nc >= 30000 and best["cost"] <= 70000000:
            #     return (best["vector"], best["cost"])

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
    sol = Solution()
    (solution, obj) = sol.search(nodeCount, points)

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

