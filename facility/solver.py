#!/usr/bin/python

from gurobipy import *
import math
import copy
import random
import numpy as np
from collections import namedtuple

Point = namedtuple("Point", ['x', 'y'])
Facility = namedtuple("Facility", ['index', 'setup_cost', 'capacity', 'location'])
Customer = namedtuple("Customer", ['index', 'demand', 'location'])

def length(point1, point2):
    return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

class Solution():
    
    def parseInput(self, lines):

        parts = lines[0].split()
        facility_count = int(parts[0])
        self.N = int(parts[0])
        customer_count = int(parts[1])
        self.M = int(parts[1])

        facilities = []
        for i in range(1, facility_count+1):
            parts = lines[i].split()
            facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))

        customers = []
        for i in range(facility_count+1, facility_count+1+customer_count):
            parts = lines[i].split()
            customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))

        ######### process data

        self.capacity = np.zeros(self.N)
        self.fixedCosts = np.zeros(self.N)
        
        for i in range(self.N):
            self.capacity[i] = facilities[i].capacity
            self.fixedCosts[i] = facilities[i].setup_cost
    
        self.demand = np.zeros(self.M)

        for j in range(self.M):
            self.demand[j] = customers[j].demand
    
        self.transCosts = np.zeros((self.M, self.N))

        self.transCosts = [[length(facilities[i].location, customers[j].location) for i in range(self.N)] for j in range(self.M)]
        
        self.sumDemand = np.sum(self.demand)
        
    def solverGRB(self):
        
        # Range of plants and warehouses
        plants = range(self.N)
        warehouses = range(self.M)

        # Model
        m = Model("facility")
        m.params.TimeLimit = 30 * 60

        # Plant open decision variables: open[p] == 1 if plant p is open.
        open = []
        for p in plants:
            open.append(m.addVar(vtype=GRB.BINARY, name="Open%d" % p))

        # Transportation decision variables: how much to transport from
        # a plant p to a warehouse w
        transport = []
        for w in warehouses:
            transport.append([])
            for p in plants:
                transport[w].append(m.addVar(vtype=GRB.BINARY, # obj=self.transCosts[w][p],
                                             name="Trans%d.%d" % (p, w)))

        # The objective is to minimize the total fixed and variable costs
        m.modelSense = GRB.MINIMIZE

        # Update model to integrate new variables
        m.update()

        # Set optimization objective - minimize sum of fixed costs
        m.setObjective(quicksum([quicksum(self.transCosts[w][p]*transport[w][p] for w in warehouses) + self.fixedCosts[p]*open[p] for p in plants]))

        # Production constraints
        # Note that the right-hand limit sets the production to zero if the plant
        # is closed
        for p in plants:
            m.addConstr(
                quicksum(self.demand[w] * transport[w][p] for w in warehouses) <= self.capacity[p] * open[p],
                "Capacity%d" % p)

        # Demand constraints
        for w in warehouses:
            m.addConstr(quicksum(transport[w][p] for p in plants) == 1,
                        "Demand%d" % w)

        # Guess at the starting point: close the plant with the highest fixed costs;
        # open all others

        # First, open all plants
        for p in plants:
            open[p].start = 1.0

        # Now close the plant with the highest fixed cost
        print('Initial guess:')
        maxFixed = max(self.fixedCosts)
        for p in plants:
            if self.fixedCosts[p] == maxFixed:
                open[p].start = 0.0
                print('Closing plant %s' % p)
                break
        print('')

        # Use barrier to solve root relaxation
        m.params.method = 2

        # Solve
        m.optimize()
        
        
        sol = [0] * self.M

        # Print solution
        print('\nTOTAL COSTS: %g' % m.objVal)
        print('SOLUTION:')
        for p in plants:
            if open[p].x == 1.0:
                print('Plant %s open' % p)
                for w in warehouses:
                    if transport[w][p].x > 0:
                        sol[w] = p
                        print('  Transport %g units to warehouse %s' % \
                              (transport[w][p].x, w))
            else:
                print('Plant %s closed!' % p)
        
        return (m.objVal, sol)
    
    
    def solverGRBHeur_helper(self, openLst):
        
        # Range of plants and warehouses
        plants = range(self.N)
        warehouses = range(self.M)

        # Model
        m = Model("facility")
        m.params.TimeLimit = 20 * 60

        # Transportation decision variables: how much to transport from
        # a plant p to a warehouse w
        transport = []
        for w in warehouses:
            transport.append([])
            for p in plants:
                transport[w].append(m.addVar(vtype=GRB.BINARY, name="Trans%d.%d" % (p, w)))

        # The objective is to minimize the total fixed and variable costs
        m.modelSense = GRB.MINIMIZE

        # Update model to integrate new variables
        m.update()

        # Set optimization objective - minimize sum of fixed costs
        m.setObjective(quicksum([quicksum(self.transCosts[w][p]*transport[w][p] for w in warehouses) + self.fixedCosts[p]*openLst[p] for p in plants]))

        # Production constraints
        # Note that the right-hand limit sets the production to zero if the plant
        # is closed
        for p in plants:
            m.addConstr(
                quicksum(self.demand[w] * transport[w][p] for w in warehouses) <= self.capacity[p] * openLst[p],
                "Capacity%d" % p)

        # Demand constraints
        for w in warehouses:
            m.addConstr(quicksum(transport[w][p] for p in plants) == 1,
                        "Demand%d" % w)

        # Use barrier to solve root relaxation
        m.params.method = 2

        # Solve
        m.optimize()
        
        sol = [0] * self.M

        # Print solution
        print('\nTOTAL COSTS: %g' % m.objVal)
        # print('SOLUTION:')
        for p in plants:
            if openLst[p] == 1.0:
                # print('Plant %s open' % p)
                for w in warehouses:
                    if transport[w][p].x > 0:
                        sol[w] = p
                        # print('  Transport %g units to warehouse %s' % \
                        #       (transport[w][p].x, w))
            # else:
            #     print('Plant %s closed!' % p)
        
        return (m.objVal, sol)
    
    def solverGRBHeur_accRate(self, curr_obj, new_obj):
        
        self.temp *= 0.95
        
        return min([math.exp((curr_obj - new_obj) / self.temp), 1])
    
    def solverGRBHeur(self):
        
        # open all facility
        self.temp = 100
        
        openLst = np.ones(self.N)
        (obj, sol) = self.solverGRBHeur_helper(openLst)
        
        curr_openSet = set(sol)
        curr_closeSet = set(range(self.N)).difference(curr_openSet)
        curr_openLst = np.zeros(self.N)
        for openIdx in curr_openSet:
            curr_openLst[openIdx] = 1
        (curr_obj, curr_sol) = self.solverGRBHeur_helper(curr_openLst)
        
        best_obj = curr_obj
        best_sol = copy.copy(curr_sol)
        
        for ite in range(1000):

            # permute openLst
            new_openLst = copy.copy(curr_openLst)
            new_openSet = copy.copy(curr_openSet)
            new_closeSet = copy.copy(curr_closeSet)
            closeIdx = random.sample(new_openSet, 1)[0]
            new_openLst[closeIdx] = 0
            new_openSet.remove(closeIdx)
            new_closeSet.add(closeIdx)

            while np.dot(new_openLst, self.capacity) < self.sumDemand:
                openIdx = random.sample(new_closeSet, 1)[0]
                new_openLst[openIdx] = 1
                new_openSet.add(openIdx)
                new_closeSet.remove(closeIdx)

            (new_obj, new_sol) = self.solverGRBHeur_helper(new_openLst)

            if random.random() < self.solverGRBHeur_accRate(curr_obj, new_obj):
                curr_obj = new_obj
                curr_sol = new_sol
                curr_openLst = copy.copy(new_openLst)
                curr_openSet = copy.copy(new_openSet)
                curr_closeSet = copy.copy(new_closeSet)
            
            if best_obj > new_obj:
                best_obj = new_obj
                best_sol = copy.copy(new_sol)
            
        return (best_obj, best_sol)
    
    
    def solverMain(self, lines):
        self.parseInput(lines)
        return self.solverGRB()

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    
    sol = Solution()
    (obj, solution) = sol.solverMain(lines)
    
    #
    # parts = lines[0].split()
    # facility_count = int(parts[0])
    # customer_count = int(parts[1])
    #
    # facilities = []
    # for i in range(1, facility_count+1):
    #     parts = lines[i].split()
    #     facilities.append(Facility(i-1, float(parts[0]), int(parts[1]), Point(float(parts[2]), float(parts[3])) ))
    #
    # customers = []
    # for i in range(facility_count+1, facility_count+1+customer_count):
    #     parts = lines[i].split()
    #     customers.append(Customer(i-1-facility_count, int(parts[0]), Point(float(parts[1]), float(parts[2]))))
    #
    # # build a trivial solution
    # # pack the facilities one by one until all the customers are served
    # solution = [-1]*len(customers)
    # capacity_remaining = [f.capacity for f in facilities]
    #
    # facility_index = 0
    # for customer in customers:
    #     if capacity_remaining[facility_index] >= customer.demand:
    #         solution[customer.index] = facility_index
    #         capacity_remaining[facility_index] -= customer.demand
    #     else:
    #         facility_index += 1
    #         assert capacity_remaining[facility_index] >= customer.demand
    #         solution[customer.index] = facility_index
    #         capacity_remaining[facility_index] -= customer.demand
    #
    # used = [0]*len(facilities)
    # for facility_index in solution:
    #     used[facility_index] = 1
    #
    # # calculate the cost of the solution
    # obj = sum([f.setup_cost*used[f.index] for f in facilities])
    # for customer in customers:
    #     obj += length(customer.location, facilities[solution[customer.index]].location)

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
        print 'Solving:', file_location
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/fl_16_2)'