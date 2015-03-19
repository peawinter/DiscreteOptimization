#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])

class Solution():
    def myNewSol(self, swaps, solution):
        tmp = solution[swaps[0]]
        solution[swaps[0]] = solution[swaps[1]]
        solution[swaps[1]] = tmp
        
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
    
    def myTotalDist(self, solution):
        obj = self.dm[solution[-1]][solution[0]]
        for index in range(0, self.nodeCount - 1):
            obj += self.dm[solution[index]][solution[index+1]]
        return obj
    
    def myDistMat(self):
        self.dm = [[0] * self.nodeCount for idx in range(self.nodeCount)]
        for idx0 in range(self.nodeCount):
            for idx1 in range(self.nodeCount):
                self.dm[idx0][idx1] = length(self.points[idx0], self.points[idx1])
    
    def myGreedyInit(self):
        solution = [0]
        for idx0 in range(self.nodeCount - 1):
            next_dist = max(self.dm[solution[-1]])
            for idx1 in range(self.nodeCount):
                if (not idx1 in solution) and next_dist > self.dm[solution[-1]][idx1]:
                    next_dist = self.dm[solution[-1]][idx1]
                    next_pt = idx1
            solution.append(next_pt)
        return solution
    
    def myLDP(self, solution):
        best_solution = solution[:3]
        obj = self.dm[best_solution[0]][best_solution[1]] + self.dm[best_solution[1]][best_solution[2]] + self.dm[best_solution[2]][best_solution[0]]
        for pt in solution[3:]:
            best_obj = obj - self.dm[best_solution[-1]][best_solution[0]] + self.dm[best_solution[-1]][pt] + self.dm[pt][best_solution[0]]
            best_idx = len(best_solution) - 1
            for idx in range(len(best_solution) - 1):
                new_obj = obj - self.dm[best_solution[idx]][best_solution[idx + 1]] + self.dm[best_solution[idx]][pt] + self.dm[pt][best_solution[idx + 1]]
                if new_obj < best_obj:
                    best_obj = new_obj
                    best_idx = idx
            best_solution = best_solution[:(best_idx + 1)] + [pt] + best_solution[(best_idx + 1):]
            obj = best_obj
        return (best_solution, best_obj)
    
    def myGreedy(self, solution):
        best_solution = []
        best_solution[:] = solution
        best_obj = self.myTotalDist(solution)
        for iteration in range(100):
            for t in range(10000):
                swaps = sorted(random.sample(range(1, self.nodeCount), 2))
                alpha = self.myAccRate(t, swaps, solution)
                if random.uniform(0, 1) < alpha:
                    self.myNewSol(swaps, solution)
                    obj = self.myTotalDist(solution)
                    if obj < best_obj:
                        best_obj = obj
                        best_solution[:] = solution
            print best_solution, best_obj
            solution[:] = best_solution
            obj = best_obj
        return (solution, obj)
    
    def mysol(self, nodeCount, points):
        self.points = points
        self.nodeCount = nodeCount
        self.tuning = 10000000000.0
        self.myDistMat()
        solution = self.myGreedyInit()
        return self.myLDP(solution)
        
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

