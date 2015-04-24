#!/usr/bin/python
# -*- coding: utf-8 -*-

import math
import numpy as np
from collections import namedtuple

Customer = namedtuple("Customer", ['index', 'demand', 'x', 'y'])

def length(customer1, customer2):
    return math.sqrt((customer1.x - customer2.x)**2 + (customer1.y - customer2.y)**2)

class Solution():
    
    def parseInput(self, lines):
        parts = lines[0].split()
        
        self.customer_count = int(parts[0])
        self.vehicle_count = int(parts[1])
        self.vehicle_capacity = int(parts[2])
    
        self.customers = []
        for i in range(1, self.customer_count + 1):
            line = lines[i]
            parts = line.split()
            self.customers.append(Customer(i-1, int(parts[0]), float(parts[1]), float(parts[2])))

        self.depot = self.customers[0]
    
    def totalDist(self, vehicle_tours):
        # checks that the number of customers served is correct
        assert sum([len(v) for v in vehicle_tours]) == len(self.customers) - 1

        # calculate the cost of the solution; for each vehicle the length of the route
        obj = 0
        for v in range(0, self.vehicle_count):
            vehicle_tour = vehicle_tours[v]
            if len(vehicle_tour) > 0:
                obj += length(self.depot, vehicle_tour[0])
                for i in range(0, len(vehicle_tour)-1):
                    obj += length(vehicle_tour[i], vehicle_tour[i+1])
                obj += length(vehicle_tour[-1], self.depot)
        
        return obj
    
    def solverNaive(self):
        vehicle_tours = []
    
        remaining_customers = set(self.customers)
        remaining_customers.remove(self.depot)
    
        for v in range(0, self.vehicle_count):
            # print "Start Vehicle: ",v
            vehicle_tours.append([])
            capacity_remaining = self.vehicle_capacity
            while sum([capacity_remaining >= customer.demand for customer in remaining_customers]) > 0:
                used = set()
                order = sorted(remaining_customers, key=lambda customer: -customer.demand)
                for customer in order:
                    if capacity_remaining >= customer.demand:
                        capacity_remaining -= customer.demand
                        vehicle_tours[v].append(customer)
                        # print '   add', ci, capacity_remaining
                        used.add(customer)
                remaining_customers -= used
        
        return (self.totalDist(vehicle_tours), vehicle_tours)
    
    def solver2OPT(self, vehicle_tours = None):
        if not vehicle_tours:
            (obj, vehicle_tours) = self.solverNaive(self)
        pass
    
    def solver(self, lines):
        
        self.parseInput(lines)
        
        return self.solverNaive()

def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')
    
    sol = Solution()
    (obj, vehicle_tours) = sol.solver(lines)
    
    # prepare the solution in the specified output format
    vehicle_count = len(vehicle_tours)
    
    outputData = str(obj) + ' ' + str(0) + '\n'
    for v in range(0, vehicle_count):
        outputData += str(0) + ' ' + ' '.join([str(customer.index) for customer in vehicle_tours[v]]) + ' ' + str(0) + '\n'

    return outputData


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

        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/vrp_5_4_1)'

