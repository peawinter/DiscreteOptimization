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
    # Helper functions
    def length(self, point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def myTotalDist(self, sol):
        sol.append(sol[0])
        dist = np.sum([self.dm[sol[i], sol[i + 1]] for i in range(self.nc)])
        aug_dist = np.sum([self.dm[sol[i], sol[i + 1]] + self.penalty[sol[i], sol[i + 1]] * self.Lambda for i in range(self.nc)])
        sol.pop()
        return dist, aug_dist
    
    def myDistMat(self):
        self.dm = [[self.length(x,y) for y in self.points] for x in self.points]
        self.dm = np.array(self.dm)
    
    def myRandom(self):
        sol = range(self.nc)
        random.shuffle(sol)
        return sol
    
    # Greedy 
    def myGreedy(self):
        sol = [0]
        for idx0 in range(self.nc - 1):
            next_dist = max(self.dm[sol[-1]])
            for idx1 in range(self.nc):
                if (not idx1 in sol) and next_dist > self.dm[sol[-1]][idx1]:
                    next_dist = self.dm[sol[-1]][idx1]
                    next_pt = idx1
            sol.append(next_pt)
        return sol
    
    # 2-opt
    def my2OPT(self, curr_sol = None):
        if not curr_sol:
            curr_sol = self.myGreedy()
        flag = True
        while flag:
            flag = False
            for idx1 in range(0, self.nc):
                for idx2 in range(idx1 + 1, self.nc):
                    i0, j0 = curr_sol[idx1 - 1], curr_sol[idx1]
                    i1, j1 = curr_sol[idx2 - 1], curr_sol[idx2]
                    gain = self.dm[i0, j0] + self.dm[i1, j1] + (self.penalty[i0, j0] + self.penalty[i1, j1]) * self.Lambda
                    cost = self.dm[i0, i1] + self.dm[j0, j1] + (self.penalty[i0, i1] + self.penalty[j0, j1]) * self.Lambda
                    if gain > cost:
                        curr_sol = curr_sol[:idx1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx2:]
                        flag = True
        return curr_sol
    
    def myA2OPT(self, curr_sol = None):
        if not curr_sol:
            curr_sol = self.myGreedy()
        count = 0
        while count <= self.max_no_improv:
            [idx1, idx2] = sorted(random.sample(range(self.nc), 2))
            i0, j0 = curr_sol[idx1 - 1], curr_sol[idx1]
            i1, j1 = curr_sol[idx2 - 1], curr_sol[idx2]
            gain = self.dm[i0, j0] + self.dm[i1, j1] + (self.penalty[i0, j0] + self.penalty[i1, j1]) * self.Lambda
            cost = self.dm[i0, i1] + self.dm[j0, j1] + (self.penalty[i0, i1] + self.penalty[j0, j1]) * self.Lambda
            if gain > cost:
                curr_sol = curr_sol[:idx1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx2:]
                flag = True
            else:
                count += 1
        return curr_sol
    
    # 3-OPT
    def my3OPT(self, curr_sol = None):
        if not curr_sol:
            curr_sol = self.my2OPT()
        curr_dist = self.myTotalDist(curr_sol)[0]
        flag = True
        while flag:
            flag = False
            for idx1 in range(self.nc):
                for idx2 in range(idx1 + 1, self.nc):
                    for idx3 in range(idx2 + 1, self.nc):
                        new_sols = []
                        new_dists = []
                        new_sols.append(curr_sol[:idx1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx2:idx3] + curr_sol[idx3:])
                        new_sols.append(curr_sol[:idx1] + curr_sol[idx1:idx2] + curr_sol[idx2:idx3][::-1] + curr_sol[idx3:])
                        new_sols.append(curr_sol[:idx1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx2:idx3][::-1] + curr_sol[idx3:])
                        new_sols.append(curr_sol[:idx1] + curr_sol[idx2:idx3] + curr_sol[idx1:idx2] + curr_sol[idx3:])
                        new_sols.append(curr_sol[:idx1] + curr_sol[idx2:idx3][::-1] + curr_sol[idx1:idx2] + curr_sol[idx3:])
                        new_sols.append(curr_sol[:idx1] + curr_sol[idx2:idx3] + curr_sol[idx1:idx2][::-1] + curr_sol[idx3:])
                        new_sols.append(curr_sol[:idx1] + curr_sol[idx2:idx3][::-1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx3:])
                        new_dists = [self.myTotalDist(s)[0] for s in new_sols]
                        if curr_dist > min(new_dists):
                            curr_sol[:] = new_sols[np.argmin(new_dists)]
                            curr_dist = min(new_dists)
                            flag = True
        return curr_sol
    
    def addPanelty(self, sol):
        # calculate utility
        util = np.zeros(self.nc)
        for idx in range(self.nc):
            util[idx] = self.dm[sol[idx - 1], sol[idx]] / (1 + self.penalty[sol[idx - 1], sol[idx]])
        edge = np.argmin(util)
        i, j = sol[edge - 1], sol[(edge) % self.nc]
        self.penalty[i, j] += 1
        self.penalty[j, i] += 1
        self.bits[i] = 1
        self.bits[j] = 1
        
    def myGLS(self):
        curr_sol = self.my2OPT()
        curr_sol = self.my3OPT(curr_sol)
        curr_dist, curr_aug_dist = self.myTotalDist(curr_sol)
        print curr_dist
        best_sol = []
        best_sol[:] = curr_sol
        best_dist = curr_dist
        self.bits = np.ones(self.nc)
        for ite in range(self.max_iterations):
            # update penality
            self.addPanelty(curr_sol)
            self.Lambda = self.a * curr_dist / self.nc
            # search for new path
            curr_sol = self.my2OPT(curr_sol)
            # find the best path
            curr_dist, curr_aug_dist = self.myTotalDist(curr_sol)
            if curr_dist < best_dist:
                best_sol[:] = curr_sol
                best_dist = curr_dist
            print curr_dist
        best_sol = self.my3OPT(best_sol)
        return best_sol
    
    def myGLSNew(self):
        curr_sol = self.myGreedy()
        curr_dist, curr_aug_dist = self.myTotalDist(curr_sol)
        best_sol = []
        best_sol[:] = curr_sol
        best_dist = curr_dist
        for ite in range(self.max_iterations):
            # update penality
            curr_sol = self.my2OPT(curr_sol)
            self.addPanelty(curr_sol)
            self.Lambda = self.a * curr_dist / self.nc
            # find the best path
            curr_dist, curr_aug_dist = self.myTotalDist(curr_sol)
            if curr_dist < best_dist:
                best_sol[:] = curr_sol
                best_dist = curr_dist
            print curr_dist
        best_sol = self.my3OPT(best_sol)
        return best_sol
    
    def mysol(self, nodeCount, points):
        self.points = points
        self.nc = nodeCount
        self.myDistMat()
        self.max_iterations = 1000
        self.penalty = np.zeros((self.nc, self.nc))
        self.Lambda = 0
        self.a = 0.3
        self.bits = np.ones(self.nc)
        sol = self.myGLSNew()
        dist, aug_dist = self.myTotalDist(sol)
        return (sol, dist)
        

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
    (solution, obj) = sol.mysol(nodeCount, points)
    
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

