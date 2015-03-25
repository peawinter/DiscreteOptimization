# Travelling Salesman Problem

*Wenyu Wang*

---

## Problem Statement

Given a set of nodes and distance between every pair of nodes, the problem is to find the shortest possible route that visits every node exactly once and returns to the starting point.

Note the difference between Hamiltonian Cycle and TSP. The Hamiltoninan cycle problem is to find if there exist a tour that visits every node exactly once. Here we know that Hamiltonian Tour exists (because the graph is complete) and in fact many such tours exist, the problem is to find a minimum weight Hamiltonian Cycle.

The problem is a famous NP hard problem. There is no polynomial time know solution for this problem.

![US TSP](http://robslink.com/SAS/democd62/v940/optnet_tsp.png)

## Algorithms

### Naive Algorithm

1. Consider node 1 as the starting and ending point.
2. Generate all (n-1)! Permutations of nodes.
3. Calculate cost of every permutation and keep track of minimum cost permutation.
4. Return the permutation with minimum cost.

Time Complexity:  $$O(n!)$$

### Dynamic Programming Algorithm

1. Consider node 1 as the starting and ending point.
2. For every other vertex $$i$$ (other than 1), find the the minimum cost path with 1 as the starting point and all vertices appearing exactly once. Let the cost be $$cost(i)$$. 
	1. Let $$C(S, i)$$ be the minimum cost path visiting each vertex in set $$S$$ exactly once, starting at 1 and ending at $$i$$.
	2. Start from all subsets of size 2 and calculate $$C(S, i)$$ for all subsets where $$S$$ is the subset, then we calculate $$C(S, i)$$ for all subsets $$S$$ of size 3 and so on.

	> Note that 1 must be present in every subset. For a set of size $$n$$, we consider $$n-2$$ subproblems each of size $$n-1$$.

	$$
	C(S, i) = \min_{j \in S/\{1, i\}} \{C(S/\{i\}, j) + dist(j, i)\}
	$$	
3. Return the minimum of all $$[cost(i) + dist(i, 1)]$$.

Time Complexity: $$O(n2^n)$$ subproblems, and each one takes linear time to solve. The total running time is therefore $$O(n^2 2^n)$$. 

Space complexity: exponential.

### Simulated Annealing Algorithm

costprevious = infinite
temperature = temperature_start
while temperature > temperature_end:
    costnew = cost_function(...)
    difference = costnew - costprevious
    if difference < 0 or  e(-difference/temperature) > random(0,1):
        costprevious = costnew
    temperature = temperature * cooling_factor

---
References:
http://www.geeksforgeeks.org/travelling-salesman-problem-set-1/
