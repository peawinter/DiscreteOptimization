#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE

def solve_it(input_data):

    # Writes the inputData to a temporay file

    tmp_file_name = 'tmp'
    tmp_file = open(tmp_file_name, 'w')
    tmp_file.write(input_data)
    tmp_file.close()

    # Runs the command: java Solver -file=tmp.data

    process = Popen(['julia', 'Solver.jl', tmp_file_name], stdout=PIPE)
    (stdout, stderr) = process.communicate()
    
    print stdout.strip()
    
    # removes the temporay file
    os.remove(tmp_file_name)
    
    fop = 'tmp_sol'
    op_file = open(fop, 'r')
    op = ''.join(op_file.readlines())
    op_file.close()
    
    return op
    
    

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        input_data_file = open(file_location, 'r')
        input_data = ''.join(input_data_file.readlines())
        input_data_file.close()
        print solve_it(input_data)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

