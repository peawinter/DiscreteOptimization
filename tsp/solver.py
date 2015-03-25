#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
import operator
import itertools
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

class Solution():
    def myNewSol(self, swaps, solution):
        tmp = solution[swaps[0]]
        solution[swaps[0]] = solution[swaps[1]]
        solution[swaps[1]] = tmp
        return solution
    
    def myAccRate(self, t, swaps, solution):
        self.tuning *= 0.99
        pt1, pt2, pt3 = solution[swaps[0] - 1], solution[swaps[0]], solution[swaps[0] + 1]
        pt4, pt5, pt6 = solution[swaps[1] - 1], solution[swaps[1]], solution[(swaps[1] + 1) % self.nodeCount]
        prev = self.dm[pt1][pt2] + self.dm[pt2][pt3] + self.dm[pt4][pt5] + self.dm[pt5][pt6]
        curr = self.dm[pt1][pt5] + self.dm[pt5][pt3] + self.dm[pt4][pt2] + self.dm[pt2][pt6]
        if curr < prev:
            return 1
        try:
            alpha = math.exp((prev - curr) / self.tuning)
        except:
            alpha = 0
        return alpha
    
    def mySA(self, solution):
        best_solution = solution
        best_obj = self.myTotalDist(solution)
        for iteration in range(100):
            for t in range(10000):
                swaps = sorted(random.sample(range(1, self.nodeCount), 2))
                alpha = self.myAccRate(t, swaps, solution)
                if random.uniform(0, 1) < alpha:
                    solution = self.myNewSol(swaps, solution)
                    obj = self.myTotalDist(solution)
                    if obj < best_obj:
                        best_obj = obj
                        best_solution[:] = solution
            solution = best_solution
            obj = best_obj
        return (solution, obj)
    
    def myTotalDist(self, solution):
        obj = self.dm[solution[-1]][solution[0]]
        for index in range(0, self.nodeCount - 1):
            obj += self.dm[solution[index]][solution[index+1]]
        return obj
    
    def myDistMat(self):
        self.dm = [[length(x,y) for y in self.points] for x in self.points]
    
    def myInit(self):
        solution = [0]
        for idx0 in range(self.nodeCount - 1):
            next_dist = max(self.dm[solution[-1]])
            for idx1 in range(self.nodeCount):
                if (not idx1 in solution) and next_dist > self.dm[solution[-1]][idx1]:
                    next_dist = self.dm[solution[-1]][idx1]
                    next_pt = idx1
            solution.append(next_pt)
        return (solution, self.myTotalDist(solution))
    
    def myDP(self):
        A = {(frozenset([0, idx + 1]), idx + 1): (dist, [0, idx + 1]) for idx, dist in enumerate(self.dm[0][1:])}
        for m in range(2, self.nodeCount):
            B = {}
            for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, self.nodeCount), m)]:
                for j in S - {0}:
                    B[(S, j)] = min( [(A[(S-{j},k)][0] + self.dm[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])
            A = B
        res =  min([(A[d][0] + self.dm[0][d[1]], A[d][1]) for d in iter(A)])
        print res
        return (res[1], res[0])
    
    def mysol(self, nodeCount, points):
        self.points = points
        self.nodeCount = nodeCount
        self.tuning = 10000000000.0
        self.myDistMat()
        return self.myDP()
        
def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

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

