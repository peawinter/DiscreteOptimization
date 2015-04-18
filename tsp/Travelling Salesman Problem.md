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

### Nearest Neighbor Algorithm

1. Start from node 0, and set 0 as the end.
2. Find the next closest node to the end. Add this node to the solution and call this node the end.
3. Repeat 2 until all nodes are visited.
4. Connect the end to 0.

### 2-X Algorithm

> When the cost function satisfies the triangle inequality, we can design an approximate algorithm for TSP that returns a tour whose cost is not more than twice the cost of an optimal tour.
> 
> First, compute a MST (minimum spanning tree) whose weight is a lower bound on the length of an optimal TSP tour. Then, use MST to build a tour whose cost is no more than twice that of MST's weight as long as the cost function satisfies triangle inequality.

Algorithm

1. Let root r be a in following given set of points (graph).
	
	![](http://www.personal.kent.edu/~rmuhamma/Algorithms/MyAlgorithms/AproxAlgor/Gifs/tsp_a.gif)

2. Construct MST from root a using MST-PRIM $$(G, c, r)$$.
	
	![](http://www.personal.kent.edu/~rmuhamma/Algorithms/MyAlgorithms/AproxAlgor/Gifs/tsp_b.gif)

3. List vertices visited in preorder walk. $$L = {a, b, c, h, d, e, f, g}$$.

	![](http://www.personal.kent.edu/~rmuhamma/Algorithms/MyAlgorithms/AproxAlgor/Gifs/tsp_c.gif)

4. Return Hamiltonian cycle.

	![](http://www.personal.kent.edu/~rmuhamma/Algorithms/MyAlgorithms/AproxAlgor/Gifs/tsp_d.gif)

### Simulated Annealing

### 2-Opt, 3-Opt, and k-Opt

### Guided local search

---
References:
http://www.geeksforgeeks.org/travelling-salesman-problem-set-1/
http://www.personal.kent.edu/~rmuhamma/Algorithms/MyAlgorithms/AproxAlgor/TSP/tsp.htm
