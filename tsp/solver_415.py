#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import random
import operator
import itertools
from collections import namedtuple
from collections import defaultdict

Point = namedtuple("Point", ['x', 'y'])

class OldSolution():
    # Helper functions
    
    def length(self, point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def myTotalDist(self, sol):
        obj = self.dm[sol[-1]][sol[0]]
        for index in range(0, self.nc - 1):
            obj += self.dm[sol[index]][sol[index+1]]
        return obj
    
    def myDistMat(self):
        self.dm = [[self.length(x,y) for y in self.points] for x in self.points]
    
    # Dynamic Programming
    def myDP(self):
        A = {(frozenset([0, idx + 1]), idx + 1): (dist, [0, idx + 1]) for idx, dist in enumerate(self.dm[0][1:])}
        for m in range(2, self.nc):
            B = {}
            for S in [frozenset(C) | {0} for C in itertools.combinations(range(1, self.nc), m)]:
                for j in S - {0}:
                    B[(S, j)] = min( [(A[(S-{j},k)][0] + self.dm[k][j], A[(S-{j},k)][1] + [j]) for k in S if k != 0 and k!=j])
            A = B
        res =  min([(A[d][0] + self.dm[0][d[1]], A[d][1]) for d in iter(A)])
        print res
        return (res[1], res[0])
    
    # random
    def myRandomSol(self):
        sol = range(self.nc)
        random.shuffle(sol)
        return (sol, self.myTotalDist(sol))
    
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
        return (sol, self.myTotalDist(sol))
    
    def my2X(self):
        # start from a spanning tree
        visited = set([0])
        unvisited = set(range(1, self.nc))
        edgedict = defaultdict(list)
        max_dist = max([max(ds)] for ds in self.dm)
        while unvisited:
            next_dist = max_dist
            for idx0 in visited:
                for idx1 in unvisited:
                    if self.dm[idx0][idx1] < next_dist:
                        next_dist = self.dm[idx0][idx1]
                        next_edge = (idx0, idx1)
            visited.add(next_edge[1])
            unvisited.remove(next_edge[1])
            edgedict[next_edge[0]].append(next_edge[1])
        # preorder the spanning tree
        sol = [0]
        stack = edgedict[0]
        while stack:
            sol.append(stack.pop())
            stack += edgedict[sol[-1]]
        dist = self.myTotalDist(sol)
        return (sol, self.myTotalDist(sol))
    
    # 2-opt
    def my2OPT(self):
        (curr_sol, curr_dist) = self.myGreedy()
        print curr_dist
        flag = True
        while flag:
            flag = False
            for idx1 in range(self.nc):
                for idx2 in range(idx1 + 1, self.nc):
                    new_sol = curr_sol[:idx1] + curr_sol[idx1:idx2][::-1] + curr_sol[idx2:]
                    new_dist = self.myTotalDist(new_sol)
                    if new_dist < curr_dist:
                        flag = True
                        curr_sol[:] = new_sol
                        curr_dist = new_dist
        return (curr_sol, curr_dist)
    
    # 3 OPT
    def my3OPT(self):
        (curr_sol, curr_dist) = self.my2OPT()
        flag = True
        print curr_dist
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
                        new_dists = [self.myTotalDist(s) for s in new_sols]
                        if curr_dist > min(new_dists):
                            curr_sol[:] = new_sols[new_dists.index(min(new_dists))]
                            curr_dist = min(new_dists)
                            flag = True
        return (curr_sol, curr_dist)
    
    # simulated annealing
    def myAccRate(self, new_dist, curr_dist):
        self.T *= 0.9999
        if new_dist < curr_dist:
            return 1
        try:
            return math.exp((curr_dist - new_dist) / self.tuning)
        except:
            return 0
    
    def my4OPT(self):
        (curr_sol, curr_dist) = self.my3OPT()
        print curr_dist
        self.T = 100.0
        for rep in range(1000000):
            [idx1, idx2, idx3, idx4] = sorted(random.sample(range(self.nc), 4))
            solst = []
            solst.append(curr_sol[ : idx1][::random.choice([-1, 1])])
            solst.append(curr_sol[idx1 : idx2][::random.choice([-1, 1])])
            solst.append(curr_sol[idx2 : idx3][::random.choice([-1, 1])])
            solst.append(curr_sol[idx3 : idx4][::random.choice([-1, 1])])
            solst.append(curr_sol[idx4 :][::random.choice([-1, 1])])
            random.shuffle(solst)
            new_sol = []
            for ele in solst:
                new_sol += ele
            new_dist = self.myTotalDist(new_sol)
            if self.myAccRate(new_dist, curr_dist) > random.random():
                curr_sol = new_sol[:]
                curr_dist = new_dist
                print rep, curr_dist, self.T
        return (curr_sol, curr_dist)
    
    def mysol(self, nodeCount, points):
        self.points = points
        self.nc = nodeCount
        self.myDistMat()
        # self.myMILP()
        return self.my3OPT()
        

class NewSolution():
    
    def myTotalDist(self, sol):
        obj = self.dm[sol[-1]][sol[0]]
        for index in range(0, len(sol) - 1):
            obj += self.dm[sol[index]][sol[index+1]]
        return obj
    
    def myDistMat(self):
        self.dm = [[self.length(x,y) for y in self.points] for x in self.points]
    
    def length(self, point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)
    
    def extractTour(self, solMat):
        sol = [0]
        curr_node = 0
        while True:
            for i in range(self.nc):
                if solMat[curr_node][i] > 0:
                    sol.append(i)
                    solMat[curr_node][i] = 0
                    solMat[i][curr_node] = 0
                    curr_node = i
                    break
            if curr_node == 0:
                break
        return (sol[:-1], self.myTotalDist(sol))
    
    def findSubtour(self, solMat):
        subtour = [False] * self.nc
        curr_node = 0
        subtour[curr_node] = True
        subtour_len = 1
        while True:
            found_node = False
            for i in range(self.nc):
                if not subtour[i] and solMat[curr_node][i] > 0:
                    curr_node = i
                    subtour[i] = True
                    found_node = True
                    subtour_len += 1
                    break
            if not found_node:
                break
        return (subtour, subtour_len)
    
    def x2solMat(self, x):
        solMat = []
        for i in range(self.nc):
            solMat += [[x[str(i) + '-' + str(0)].value()]]
            for j in range(1, self.nc):
                solMat[-1].append(x[str(i) + '-' + str(j)].value())
        return solMat
    
    def myMILP(self):
        
        prob = pulp.LpProblem("tsp", pulp.LpMinimize)
        edges = [str(i) + '-' + str(j) for i in range(self.nc) for j in range(self.nc)]
        x = pulp.LpVariable.dict('%s', edges, lowBound = 0, upBound = 1, cat='Integer')
        prob += sum([self.dm[i][j] * x[str(i) + '-' + str(j)] for i in range(self.nc) for j in range(self.nc)])
        
        for i in range(self.nc):
            prob += x[str(i) + '-' + str(i)] == 0
            for j in range(i):
                prob += x[str(i) + '-' + str(j)] == x[str(j) + '-' + str(i)]
        
        for i in range(self.nc):
            prob += sum([x[str(i) + '-' + str(j)] for j in range(self.nc)]) == 2
        
        prob.solve()
        solMat = self.x2solMat(x)
        (subtour, subtour_len) = self.findSubtour(solMat)
        
        print subtour_len
        
        while subtour_len != self.nc:
            coff = dict(zip(edges, [0] * len(edges)))
            for i in range(self.nc):
                for j in range(self.nc):
                    if subtour[i] and not subtour[j]:
                        coff[str(i) + '-' + str(j)] = 1
            prob += sum([coff[e] * x[e] for e in edges]) >= 2
            prob.solve()
            solMat = self.x2solMat(x)
            (subtour, subtour_len) = self.findSubtour(solMat)
            
            # print subtour_len
            
        return self.extractTour(solMat)
        
    def mysol(self, nodeCount, points):
        self.points = points
        self.nc = nodeCount
        self.myDistMat()
        return self.myMILP()

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
    sol = OldSolution()
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

