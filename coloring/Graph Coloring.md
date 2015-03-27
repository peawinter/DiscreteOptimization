# Graph Coloring

*Wenyu Wang*

---

## Problem Statement

Given an undirected graph, graph coloring or vertex color problem is to assign minimum number of different colors to nodes such that no adjacent nodes share the same color. 

The problem comes from coloring a map such that no two neighbor regions have the same color. Here is a map of the United States colored with only 4 colors:

![US map with four colors](http://www.cs.cornell.edu/courses/cs3110/2011sp/recitations/rec21-graphs/images/USA.png)

## Application

**Scheduling** schedule final exams. College offers multiple courses and each student may take multiple courses. To resolve conflict, if a student takes two courses, then these two courses cannot be scheduled at the same time.

**Register Allocation** when compiling a program, the computer needs to allocate registers to the most frequently used values of the program, while putting the other ones in memory. This can be modeled as a graph coloring problem: the compiler constructs an interference graph, where vertices are symbolic registers and an edge connects two nodes if they are needed at the same time. If the graph can be colored with k colors then the variables can be stored in k registers.

- time tabling and scheduling
- frequency assignment
- register allocation
- printed circuit testing
- parallel numerical computation and optimization

## Properties

- A color of a graph $$G$$ is a mapping $$c:V(G) \rightarrow S$$. If the graph $$G$$ has a coloring such that $$|S| = k$$ and all adjacent vertices have different colors, then we say that $$G$$ is $$k$$-colorable.

- The **chromatic number** $$\chi(G)$$ is the least $$k$$ such that the graph $$G$$ is $$k$$-colorable.

- A $$k$$-coloring can be seen as a partition of the vertex set of $$G$$ into $$k$$ groups. 

- The **clique number** $$\omega(G)$$ is the largest $$k$$ such that $$G$$ contains a $$K_k$$ subgraph.

- A *planar* graph is a graph which can be embedded in the plane, i.e., it can be drawn on the plane in such a way that its edges intersect only at their endpoints. The conjecture that any planar graph was 4-colorable was proposed in 1852, and finally proven in 1976 by Kenneth Appel and Wolfgang Haken using a proof by computer (K. Appel and W. Haken, "Every map is four colorable", Bulletin of the American Mathematical Society 82 (1976), 711–12).

- Complexity
	- For $$k \leq 2$$, $$k-colorability$$ is polynomial-time solvable. Do a breadth-first search, assigning "red" to the first layer, "blue" to the second layer, "red" to the third layer, etc. Then go over all the edges and check whether the two endpoints of this edge have different colors.
	- For $$k \geq 3$$, $$k-colorability$$ is **NP-complete**. The direct approach is brute-force search: consider every possible assignment of k colors to the vertices, and check whether any of them are correct. This of course is very expensive, on the order of O((n+1)!), and impractical.

- Approximation boundaries
	- Lower bound: $$\chi(G) \geq \omega(G)$$
	- Upper bound: $$\chi(G) \leq \Delta(G) + 1$$, $$2|E(G)| \geq \chi(G) (\chi(G) - 1)$$

## Algorithms

#### Dynamic Programming algorithm

Algorithm:

1. Find and list all sets that are $$1-colorable$$. 
2. Proceed in an inductive manner. Given all sets that are $$1-colorable$$ and all sets that are $$(j-1)-colorable$$, find all sets that are $$j-colorable$$.

	> - For each candidate set, try all ways of partitioning it in two and checking whether one part is $$1-colorable$$ and other is $$(j-1)-colorable$$. The total number of checks is $$\sum_{S \in V} 2^{|S|} = 3^n$$. (A ternary vector can represent a check. The 0 entries are those vertices not in S. the 1 entries are those vertices in the independent set. The 2 entries are those in the $$(j − 1)-colorable$$ set.)

Time complexity: $$O(3^n)$$

Space complexity: $$O(2^n)$$

- Remark
	- By considering only maximal independent sets, the dynamic
programming based algorithm can be modified to have an improved running time of $$O(2.45^n)$$.
	- Dynamic programming is a method that avoids redoing computations
over and over again in exhaustive search. This leads to significant savings in running times, typically at the expense of requiring more space to store previously computed values.

#### Backtrack algorithm

Suppose we have an upper bound for our graph coloring. During the brute force algorithm we can then determine that we need to backtrack when we can’t color a node with a color less than our upper bound.

1. When a node is colored, keep track of the index of when that node is colored. 
2. For each unique color that is adjacent to the current node that needs backtracking, determine the minimum index calculated in step 1.
3. Find the maximum of all the minimums calculated in step 2.
4. Backtrack up to the index found in step 3.

#### Greedy algorithm

Algorithm:
	
1. Number the vertices $$V=\{v_1, v_2, ...,v_n\}$$.
2. For $$i = 1, ..., n$$, color $$v_i$$ with the lowest color that is not yet used for its neighbors.

> - In general, the greedy algorithm is not optimal, but it provides a reasonable coloring while still being reasonably expensive.
> - This algorithm finds a reasonable coloring in time $$O(|V|+|E|)$$.
> - The number of colors used depends strongly on the chosen vertex order. But any order with give a color using at most $$\Delta(G) + 1$$ colors.

- Remark: 
	- **For every graph $$G$$, there exists an order for $$V$$ such that the greedy coloring algorithm uses exactly $$\chi(G)$$ colors.**
	- For a good heuristic, one may also choose a dynamic order: at any point, color the uncolored vertex that currently has the highest number of different colors in its neighborhood.
	- If the vertices of a graph $$G$$ can be numbered $$v_1, ..., v_n$$ such that for every $$i$$ , $$|N(v_i)  \cap \{v_1 , . . . , v_{i-1} \}| \leq k$$ , then $$\chi(G)\leq k+1$$.

#### Welsh-Powell algorithm

Algorithm:

1. Find the degree of every vertex.
2. Sort the vertices in order of descending degrees. 
3. Color the first vertex in the list with color 1.
4. Go down the list and color every vertex not connected to the colored vertices above the same color. Then cross out all colored vertices in the list.
5. Repeat the process on the uncolored vertices with a new color.

- Remark:
	- Usually performs better than just coloring the vertices without a plan will.

#### Iterated Greedy algorithm

Algorithm:
1. Run simple greedy algorithm.
2. Permutate the solution such that nodes with the same label are grouped together. 
3. Iterate until the color count reach the optimal value.

> - The idea is to use previous information obtained in previous coloring to produce an improved coloring. If we take any permutation in which the vertices of each color class are adjacent in the permutation, then applying the greedy algorithm will produce a coloring at least as good.
> - Reorder the color labels randomly.

#### Tabu searching algorithm

The basic idea behind TABU search is to take a graph coloring that contains conflicts, and then try to repair the conflicts to produce a valid graph coloring. When a graph coloring contains conflicts, it means that there are some nodes in the graph whose color is the same as an adjacent node.

1. Take a valid graph coloring solution as input.
2. Reduce the amount of colors used by assigning a random color to the nodes that are colored with the maximum color.
3. Generate (number of nodes)/4 neighbors for the current coloring by selecting a random node which is in conflict and assign a random color to that node.
4. Select the neighbor that contains the least amount of conflicts.
5. Use the neighbor selected in step 4 as the new coloring.
6. If no conflicts exist, exit the search, otherwise goto step 3 until the maximum number of iterations are reached.
7. If no solution has been found, increase the number of colors to use and go to step 3.

> Tabu list: during the TABU search, keep a list which contains the reverse move that was done, and don’t allow moves in the list during the following iterations. A list in a FIFO manner of size 15 is proper.

#### Mixed Strategy

1. Execute the Iterative Greedy algorithm for X amount of iterations.
2. Execute the TABU search algorithm on the best solution found thus far.
3. Use Y amount of iterations for the search. Goto step 1 until the time is up.

#### Simulated Annealing algorithm


