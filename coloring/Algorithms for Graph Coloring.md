# Notes on Graph Coloring Algorithms

*Wenyu Wang*

---

## Problem Statement

Given an undirected graph, graph coloring or vertex color problem is to assign minimum number of different colors to nodes such that no adjacent nodes share the same color. 

The problem comes from coloring a map such that no two neighbor regions have the same color. Here is a map of the United States colored with only 4 colors:

![US map with four colors](http://www.cs.cornell.edu/courses/cs3110/2011sp/recitations/rec21-graphs/images/USA.png)

## Application

**Scheduling** schedule final exams. College offers multiple courses and each student may take multiple courses. To resolve conflict, if a student takes two courses, then these two courses cannot be scheduled at the same time.

**Register Allocation** when compiling a program, the computer needs to allocate registers to the most frequently used values of the program, while putting the other ones in memory. This can be modeled as a graph coloring problem: the compiler constructs an interference graph, where vertices are symbolic registers and an edge connects two nodes if they are needed at the same time. If the graph can be colored with k colors then the variables can be stored in k registers.

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

#### Greedy algorithm

Algorithm:
	
1. Number the vertices $$V=\{v_1, v_2, ...,v_n\}$$.
2. For $$i = 1, ..., n$$, color $$v_i$$ with the lowest color that is not yet used for its neighbors.

> - In general, the greedy algorithm is not optimal, but it provides a reasonable coloring while still being reasonably expensive.
> - This algorithm finds a reasonable coloring in time $$O(|V|+|E|)$$.
> - The number of colors used depends strongly on the chosen vertex order. But any order with give a color using at most $$\Delta(G) + 1$$ colors.

- Observations: 
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

- Observations:
	- Usually performs better than just coloring the vertices without a plan will.

#### Naive algorithm

#### Simulated Annealing algorithm