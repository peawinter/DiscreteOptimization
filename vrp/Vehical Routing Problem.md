# Vehical Routing Problem
*Wenyu Wang*

---

## Problem Statement

The vehicle routing problem (VRP) is a combinatorial optimization and integer programming problem seeking to service a number of customers with a fleet of vehicles. Proposed by Dantzig and Ramser in 1959, VRP is an important problem in the fields of transportation, distribution, and logistics.

VRP is a generic name given to a whole class of problems in which a set of routes for a fleet of vehicles based at one or several depots must be determined for a number of geographically dispersed cities or customers. The objective of the VRP is to deliver a set of customers with known demands on minimum-cost vehicle routes originating and terminating at a depot.

![](http://neo.lcc.uma.es/vrp/wp-content/uploads/vrp.png)

The VRP is a combinatorial problem whose ground set is the edges of a graph $$G(V,E)$$. The notation used for this problem is as follows:

- $$V=\{v_0,v_1,...,v_n\}$$ is a vertex set, where: $$v_0$$ is the depot. $$V'=V - \{v_0\}$$ is the set of n cities.
- $$A=\{(v_i,v_j)|v_i,\forall j \in V;i≠j\}$$ is an arc set.
- $$C$$ is a matrix of non-negative costs or distances $$c_{ij}$$ between customers $$v_i$$ and $$v_j$$.
- $$d$$ is a vector of the customer demands.
- $$R_i$$ is the route for vehicle $$i$$.
- m is the number of vehicles (all identical). One route is assigned to each vehicle.
- $$\delta_i$$, service time required by a vehicle to unload the quantity $$q_i$$ at $$v_i$$.

When $$c_{ij}=c_{ji}$$ for all $$(v_i,v_j)\in A$$ the problem is said to be symmetric and it is then common to replace A with the edge set $$E=\{(v_i,v_j)|v_i,v_j\in V;i<j\}$$.

With each vertex $$v_i$$ in $$V'$$ is associated a quantity $$q_i$$ of some goods to be delivered by a vehicle. The VRP thus consists of determining a set of m vehicle routes of minimal total cost, starting and ending at a depot, such that every vertex in $$V'$$ is visited exactly once by one vehicle.

It is required that the total duration of any vehicle route (travel plus service times) may not surpass a given bound $$D$$, so, in this context the cost $$c_{ij}$$ is taken to be the travel time between the cities. The VRP defined above is NP-hard.

A feasible solution is composed of:

- a partition $$R_1,...,R_m$$ of $$V$$;
- a permutation $$\sigma_i$$ of $$R_i \cup 0$$ specifying the order of the customers on route i.

The cost of a given route $$R_i=\{v_0,v_1,…,v_{m+1}\}$$, where $$v_i\in V$$ and $$v_0=v_{m+1}=0$$, is given by $$C(R_i)=\sum^m_{i=0}c_i + \sum_{i=1}^m \delta_i$$.

A route Ri is feasible if the vehicle stop exactly once in each customer and the total duration of the route does not exceed a prespecified bound $$D:C(R_i)\leq D$$.

Finally, the cost of the problem solution $$S$$ is: $$F_{VRP}=\sum^ m_{i=1}F(R_i)$$.

## Algorithm

For easy computation, it can be defined $$b(V)=⌈∑vi∈Vdi)/C⌉$$, an obvious lower bound on the number of trucks needed to service the customers in set V.


References:
http://neo.lcc.uma.es/vrp/vehicle-routing-problem/