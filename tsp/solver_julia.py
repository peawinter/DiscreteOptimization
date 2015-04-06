#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from subprocess import Popen, PIPE

def solve_it(fin):

    process = Popen(['julia', 'Solver.jl', fin], stdout=PIPE)
    (stdout, stderr) = process.communicate()
    
    fop = fin + '_sol'
    op_file = open(fop, 'r')
    op = ''.join(op_file.readlines())
    op_file.close()
    
    return op

import sys

if __name__ == '__main__':
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        print solve_it(file_location)
    else:
        print 'This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)'

